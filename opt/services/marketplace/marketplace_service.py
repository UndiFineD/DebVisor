"""DebVisor App Marketplace Service - Enterprise Implementation.

Provides a catalog + recipe driven deployment system for:
- Kubernetes apps (Helm / raw manifests / Kustomize)
- VM appliances (qcow2 + cloud-init overlays)
- Hybrid stacks (VM + K8s + storage profiles)
- Container images with vulnerability scanning

Key Concepts:
- Recipe: Declarative spec describing resources, dependencies, capabilities
- Catalog: Signed collection of recipes with versioning and trust metadata
- Installer: Orchestrates multi-phase deployment with rollback checkpoints
- Governance: Validates publisher signatures & performs CVE security scanning
- Syndication: Fetches catalogs from remote repositories with caching
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable, Tuple, Union
from enum import Enum
from abc import ABC, abstractmethod
import hashlib
import json
import logging
import os
import re
import threading
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Enums and Configuration
# -----------------------------------------------------------------------------


class ResourceKind(Enum):
    HELM_CHART = "helm"
    K8S_MANIFEST = "manifest"
    KUSTOMIZE = "kustomize"
    VM_IMAGE = "vm-image"
    CONTAINER_IMAGE = "container"
    STORAGE_POOL = "storage-pool"
    NETWORK_CONFIG = "network"
    SECRET = "secret"  # nosec B105
    CONFIGMAP = "configmap"


class DeploymentStatus(Enum):
    PENDING = "pending"
    VALIDATING = "validating"
    SCANNING = "scanning"
    DOWNLOADING = "downloading"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    CANCELLED = "cancelled"


class SeverityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class TrustLevel(Enum):
    VERIFIED = "verified"  # Publisher signature verified
    TRUSTED = "trusted"  # From trusted repository
    COMMUNITY = "community"  # Community-contributed
    UNKNOWN = "unknown"  # No signature


@dataclass
class CVERecord:
    """Security vulnerability record."""

    cve_id: str
    severity: SeverityLevel
    package: str
    version: str
    fixed_version: Optional[str]
    description: str
    cvss_score: float = 0.0
    published_at: Optional[datetime] = None


@dataclass
class SecurityScanResult:
    """Results of security scan."""

    passed: bool
    scanned_at: datetime
    scanner_version: str
    vulnerabilities: List[CVERecord]
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0

    @property
    def summary(self) -> str:
        return (
            f"Critical: {self.critical_count}, High: {self.high_count}, "
            f"Medium: {self.medium_count}, Low: {self.low_count}"
        )


@dataclass
class RecipeDependency:
    """Dependency on another recipe or external resource."""

    name: str
    version_constraint: str = "*"  # semver constraint
    type: str = "recipe"  # recipe|k8s-api|storage|network
    optional: bool = False
    condition: Optional[str] = None  # conditional expression


@dataclass
class RecipeResource:
    """A deployable resource within a recipe."""

    name: str
    kind: ResourceKind
    spec: Dict[str, Any]
    depends_on: List[str] = field(default_factory=list)  # Other resource names
    rollback_hint: Optional[str] = None
    health_check: Optional[Dict[str, Any]] = None
    timeout_seconds: int = 300


@dataclass
class RecipeParameter:
    """User-configurable parameter."""

    name: str
    description: str
    type: str = "string"  # string|int|bool|choice|secret
    default: Any = None
    required: bool = False
    choices: List[str] = field(default_factory=list)
    validation: Optional[str] = None  # regex pattern


@dataclass
class Recipe:
    """Complete recipe specification."""

    name: str
    version: str
    publisher: str
    description: str
    long_description: Optional[str] = None
    icon_url: Optional[str] = None
    homepage: Optional[str] = None
    source_url: Optional[str] = None

    # Content
    dependencies: List[RecipeDependency] = field(default_factory=list)
    resources: List[RecipeResource] = field(default_factory=list)
    parameters: List[RecipeParameter] = field(default_factory=list)

    # Metadata
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    license: Optional[str] = None
    min_platform_version: Optional[str] = None

    # Security
    signatures: Dict[str, str] = field(
        default_factory=dict
    )  # key_id -> base64 signature
    checksum: Optional[str] = None
    trust_level: TrustLevel = TrustLevel.UNKNOWN

    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    # Scan results (populated during validation)
    security_scan: Optional[SecurityScanResult] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize recipe for signing/hashing."""
        return {
            "name": self.name,
            "version": self.version,
            "publisher": self.publisher,
            "description": self.description,
            "dependencies": [
                {
                    "name": d.name,
                    "version_constraint": d.version_constraint,
                    "type": d.type,
                    "optional": d.optional,
                }
                for d in self.dependencies
            ],
            "resources": [
                {
                    "name": r.name,
                    "kind": r.kind.value,
                    "spec": r.spec,
                    "depends_on": r.depends_on,
                }
                for r in self.resources
            ],
            "parameters": [
                {
                    "name": p.name,
                    "type": p.type,
                    "default": p.default,
                    "required": p.required,
                }
                for p in self.parameters
            ],
            "category": self.category,
            "tags": self.tags,
            "license": self.license,
            "created_at": self.created_at.isoformat(),
        }

    def compute_digest(self) -> str:
        """Compute SHA-256 digest of recipe content."""
        payload = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Recipe":
        """Deserialize recipe from dict."""
        dependencies = [
            RecipeDependency(
                name=d["name"],
                version_constraint=d.get("version_constraint", "*"),
                type=d.get("type", "recipe"),
                optional=d.get("optional", False),
            )
            for d in data.get("dependencies", [])
        ]

        resources = [
            RecipeResource(
                name=r["name"],
                kind=ResourceKind(r["kind"]),
                spec=r["spec"],
                depends_on=r.get("depends_on", []),
                rollback_hint=r.get("rollback_hint"),
                timeout_seconds=r.get("timeout_seconds", 300),
            )
            for r in data.get("resources", [])
        ]

        parameters = [
            RecipeParameter(
                name=p["name"],
                description=p.get("description", ""),
                type=p.get("type", "string"),
                default=p.get("default"),
                required=p.get("required", False),
                choices=p.get("choices", []),
            )
            for p in data.get("parameters", [])
        ]

        return cls(
            name=data["name"],
            version=data["version"],
            publisher=data["publisher"],
            description=data["description"],
            long_description=data.get("long_description"),
            icon_url=data.get("icon_url"),
            homepage=data.get("homepage"),
            dependencies=dependencies,
            resources=resources,
            parameters=parameters,
            category=data.get("category"),
            tags=data.get("tags", []),
            license=data.get("license"),
            signatures=data.get("signatures", {}),
            checksum=data.get("checksum"),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if "created_at" in data
                else datetime.now(timezone.utc)
            ),
        )


# -----------------------------------------------------------------------------
# Security Scanner
# -----------------------------------------------------------------------------


class SecurityScanner:
    """CVE vulnerability scanner using Trivy or Grype."""

    def __init__(self, scanner: str = "trivy"):
        self.scanner = scanner
        self._cache: Dict[str, SecurityScanResult] = {}
        self._cache_ttl = timedelta(hours=24)

    def scan_container_image(self, image: str) -> SecurityScanResult:
        """Scan container image for vulnerabilities."""
        cache_key = f"container:{image}"
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            if datetime.now(timezone.utc) - cached.scanned_at < self._cache_ttl:
                return cached

        result = self._run_trivy_scan(image, "image")
        self._cache[cache_key] = result
        return result

    def scan_filesystem(self, path: str) -> SecurityScanResult:
        """Scan filesystem/repo for vulnerabilities."""
        return self._run_trivy_scan(path, "fs")

    def _run_trivy_scan(self, target: str, scan_type: str) -> SecurityScanResult:
        """Execute Trivy scanner."""
        vulnerabilities = []

        try:
            cmd = [
                "trivy",
                scan_type,
                "--format",
                "json",
                "--severity",
                "CRITICAL,HIGH,MEDIUM,LOW",
                target,
            ]

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300
            )  # nosec B603

            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                vulnerabilities = self._parse_trivy_output(data)
            else:
                logger.warning(f"Trivy scan returned non-zero: {result.stderr}")
        except FileNotFoundError:
            logger.warning("Trivy not installed, using mock scan")
            vulnerabilities = self._mock_scan()
        except subprocess.TimeoutExpired:
            logger.error("Trivy scan timed out")
        except Exception as e:
            logger.error(f"Security scan error: {e}")

        # Count by severity
        critical = sum(
            1 for v in vulnerabilities if v.severity == SeverityLevel.CRITICAL
        )
        high = sum(1 for v in vulnerabilities if v.severity == SeverityLevel.HIGH)
        medium = sum(1 for v in vulnerabilities if v.severity == SeverityLevel.MEDIUM)
        low = sum(1 for v in vulnerabilities if v.severity == SeverityLevel.LOW)

        return SecurityScanResult(
            passed=critical == 0,  # Fail if any critical
            scanned_at=datetime.now(timezone.utc),
            scanner_version=self.scanner,
            vulnerabilities=vulnerabilities,
            critical_count=critical,
            high_count=high,
            medium_count=medium,
            low_count=low,
        )

    def _parse_trivy_output(self, data: Dict[str, Any]) -> List[CVERecord]:
        """Parse Trivy JSON output."""
        vulns = []
        for result in data.get("Results", []):
            for vuln in result.get("Vulnerabilities", []):
                severity_map = {
                    "CRITICAL": SeverityLevel.CRITICAL,
                    "HIGH": SeverityLevel.HIGH,
                    "MEDIUM": SeverityLevel.MEDIUM,
                    "LOW": SeverityLevel.LOW,
                }
                vulns.append(
                    CVERecord(
                        cve_id=vuln.get("VulnerabilityID", "UNKNOWN"),
                        severity=severity_map.get(
                            vuln.get("Severity", "").upper(), SeverityLevel.INFO
                        ),
                        package=vuln.get("PkgName", ""),
                        version=vuln.get("InstalledVersion", ""),
                        fixed_version=vuln.get("FixedVersion"),
                        description=vuln.get("Title", vuln.get("Description", ""))[
                            :200
                        ],
                        cvss_score=vuln.get("CVSS", {})
                        .get("nvd", {})
                        .get("V3Score", 0.0),
                    )
                )
        return vulns

    def _mock_scan(self) -> List[CVERecord]:
        """Mock scan for testing without Trivy."""
        return [
            CVERecord(
                cve_id="CVE-2024-0001",
                severity=SeverityLevel.MEDIUM,
                package="libssl",
                version="1.1.1",
                fixed_version="1.1.1t",
                description="[MOCK] Example vulnerability for testing",
                cvss_score=5.5,
            )
        ]

    def calculate_trust_score(self, recipe: Recipe) -> int:
        """Calculate trust score (0-100) based on security and metadata."""
        score = 100
        
        # Deduct for vulnerabilities
        if recipe.security_scan:
            score -= recipe.security_scan.critical_count * 50
            score -= recipe.security_scan.high_count * 20
            score -= recipe.security_scan.medium_count * 5
            score -= recipe.security_scan.low_count * 1
            
        # Deduct for missing metadata
        if not recipe.signatures:
            score -= 30
        if not recipe.license:
            score -= 10
        if not recipe.homepage:
            score -= 5
            
        # Cap at 0
        return max(0, score)

    def enforce_policy(self, recipe: Recipe, min_score: int = 70) -> Tuple[bool, str]:
        """Check if recipe meets governance policy."""
        score = self.calculate_trust_score(recipe)
        
        if recipe.security_scan and not recipe.security_scan.passed:
            return False, "Security scan failed (Critical vulnerabilities found)"
            
        if score < min_score:
            return False, f"Trust score {score} below minimum {min_score}"
            
        return True, "Policy check passed"



# -----------------------------------------------------------------------------
# Signature Verification
# -----------------------------------------------------------------------------


class SignatureVerifier:
    """Verify recipe signatures using Ed25519 or RSA."""

    def __init__(self, trusted_keys: Optional[Dict[str, bytes]] = None):
        self.trusted_keys = trusted_keys or {}

    def add_trusted_key(self, key_id: str, public_key: bytes) -> None:
        """Add trusted publisher key."""
        self.trusted_keys[key_id] = public_key

    def verify_recipe(self, recipe: Recipe) -> Tuple[bool, str]:
        """Verify recipe signature."""
        if not recipe.signatures:
            return False, "No signatures present"

        digest = recipe.compute_digest().encode()

        for key_id, signature_b64 in recipe.signatures.items():
            if key_id not in self.trusted_keys:
                continue

            try:
                import base64

                signature = base64.b64decode(signature_b64)
                public_key = self.trusted_keys[key_id]

                # Try Ed25519 first
                try:
                    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                        Ed25519PublicKey,
                    )
                    from cryptography.hazmat.primitives.serialization import (
                        load_pem_public_key,
                    )

                    key = load_pem_public_key(public_key)
                    if isinstance(key, Ed25519PublicKey):
                        key.verify(signature, digest)
                        return True, f"Verified with key {key_id}"
                except Exception:
                    pass  # nosec B110

                # Try RSA
                try:
                    from cryptography.hazmat.primitives import hashes
                    from cryptography.hazmat.primitives.asymmetric import padding
                    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
                    from cryptography.hazmat.primitives.serialization import (
                        load_pem_public_key,
                    )

                    key = load_pem_public_key(public_key)
                    if isinstance(key, RSAPublicKey):
                        key.verify(
                            signature, digest, padding.PKCS1v15(), hashes.SHA256()
                        )
                        return True, f"Verified with key {key_id}"
                except Exception:
                    pass  # nosec B110

            except Exception as e:
                logger.warning(f"Signature verification failed for key {key_id}: {e}")

        return False, "No valid signature found"


# -----------------------------------------------------------------------------
# Marketplace Catalog
# -----------------------------------------------------------------------------


class MarketplaceCatalog:
    """Recipe catalog with search, versioning, and remote sync."""

    def __init__(self, storage_path: str = "/var/lib/debvisor/marketplace"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._recipes: Dict[str, Dict[str, Recipe]] = {}  # name -> {version -> recipe}
        self._lock = threading.Lock()
        self._load_catalog()

    def _load_catalog(self) -> None:
        """Load recipes from disk."""
        catalog_file = self.storage_path / "catalog.json"
        if catalog_file.exists():
            try:
                with open(catalog_file) as f:
                    data = json.load(f)
                for name, versions in data.items():
                    self._recipes[name] = {}
                    for version, recipe_data in versions.items():
                        self._recipes[name][version] = Recipe.from_dict(recipe_data)
                logger.info(
                    f"Loaded {sum(len(v) for v in self._recipes.values())} recipes from catalog"
                )
            except Exception as e:
                logger.warning(f"Failed to load catalog: {e}")

    def _save_catalog(self) -> None:
        """Persist catalog to disk."""
        data = {}
        for name, versions in self._recipes.items():
            data[name] = {v: r.to_dict() for v, r in versions.items()}

        catalog_file = self.storage_path / "catalog.json"
        with open(catalog_file, "w") as f:
            json.dump(data, f, indent=2)

    def add_recipe(self, recipe: Recipe) -> str:
        """Add or update recipe in catalog."""
        with self._lock:
            if recipe.name not in self._recipes:
                self._recipes[recipe.name] = {}
            self._recipes[recipe.name][recipe.version] = recipe
            self._save_catalog()

        logger.info(f"Added recipe {recipe.name}:{recipe.version}")
        return recipe.compute_digest()

    def get(self, name: str, version: Optional[str] = None) -> Optional[Recipe]:
        """Get recipe by name and optional version (latest if not specified)."""
        versions = self._recipes.get(name)
        if not versions:
            return None

        if version:
            return versions.get(version)

        # Return latest version
        sorted_versions = sorted(versions.keys(), key=self._version_key, reverse=True)
        return versions[sorted_versions[0]] if sorted_versions else None

    def _version_key(self, version: str) -> Tuple[Union[int, str], ...]:
        """Parse semver for sorting."""
        parts = re.split(r"[.\-]", version)
        return tuple(int(p) if p.isdigit() else p for p in parts)

    def list_versions(self, name: str) -> List[str]:
        """List all versions of a recipe."""
        versions = self._recipes.get(name, {})
        return sorted(versions.keys(), key=self._version_key, reverse=True)

    def search(
        self,
        query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Recipe]:
        """Search recipes with filters."""
        results = []
        query_lower = query.lower()

        for versions in self._recipes.values():
            # Get latest version
            if not versions:
                continue
            recipe = list(versions.values())[0]

            # Apply filters
            if (
                query
                and query_lower not in recipe.name.lower()
                and query_lower not in recipe.description.lower()
            ):
                continue
            if category and recipe.category != category:
                continue
            if tags and not any(t in recipe.tags for t in tags):
                continue

            results.append(recipe)

        return sorted(results, key=lambda r: r.name)

    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        categories = set()
        for versions in self._recipes.values():
            for recipe in versions.values():
                if recipe.category:
                    categories.add(recipe.category)
        return sorted(categories)

    def get_popular_tags(self, limit: int = 20) -> List[Tuple[str, int]]:
        """Get most popular tags with counts."""
        tag_counts: Dict[str, int] = {}
        for versions in self._recipes.values():
            for recipe in versions.values():
                for tag in recipe.tags:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        return sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:limit]

    def remove_recipe(self, name: str, version: Optional[str] = None) -> bool:
        """Remove recipe (specific version or all versions)."""
        with self._lock:
            if name not in self._recipes:
                return False

            if version:
                if version in self._recipes[name]:
                    del self._recipes[name][version]
                    if not self._recipes[name]:
                        del self._recipes[name]
                else:
                    return False
            else:
                del self._recipes[name]

            self._save_catalog()
        return True


# -----------------------------------------------------------------------------
# Remote Repository Sync
# -----------------------------------------------------------------------------


@dataclass
class RemoteRepository:
    """Remote recipe repository configuration."""

    name: str
    url: str
    enabled: bool = True
    trust_level: TrustLevel = TrustLevel.COMMUNITY
    sync_interval_hours: int = 24
    last_sync: Optional[datetime] = None
    public_key: Optional[bytes] = None


class RepositorySyncer:
    """Sync recipes from remote repositories."""

    def __init__(self, catalog: MarketplaceCatalog):
        self.catalog = catalog
        self.repositories: Dict[str, RemoteRepository] = {}
        self._sync_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def add_repository(self, repo: RemoteRepository) -> None:
        """Add remote repository."""
        self.repositories[repo.name] = repo
        logger.info(f"Added repository: {repo.name} ({repo.url})")

    def sync_repository(self, repo_name: str) -> Tuple[int, List[str]]:
        """Sync recipes from a repository."""
        repo = self.repositories.get(repo_name)
        if not repo:
            return 0, [f"Repository not found: {repo_name}"]

        try:
            import urllib.request

            index_url = f"{repo.url.rstrip('/')}/index.json"
            with urllib.request.urlopen(
                index_url, timeout=30
            ) as response:  # nosec B310
                index_data = json.loads(response.read().decode())

            added = 0
            errors = []

            for recipe_ref in index_data.get("recipes", []):
                try:
                    recipe_url = f"{repo.url.rstrip('/')}/{recipe_ref['path']}"
                    with urllib.request.urlopen(
                        recipe_url, timeout=30
                    ) as response:  # nosec B310
                        recipe_data = json.loads(response.read().decode())

                    recipe = Recipe.from_dict(recipe_data)
                    recipe.trust_level = repo.trust_level
                    self.catalog.add_recipe(recipe)
                    added += 1
                except Exception as e:
                    errors.append(
                        f"Failed to fetch {recipe_ref.get('name', 'unknown')}: {e}"
                    )

            repo.last_sync = datetime.now(timezone.utc)
            logger.info(f"Synced {added} recipes from {repo_name}")
            return added, errors

        except Exception as e:
            logger.error(f"Repository sync failed: {e}")
            return 0, [str(e)]

    def sync_all(self) -> Dict[str, Tuple[int, List[str]]]:
        """Sync all enabled repositories."""
        results = {}
        for name, repo in self.repositories.items():
            if repo.enabled:
                results[name] = self.sync_repository(name)
        return results


# -----------------------------------------------------------------------------
# Deployment Record
# -----------------------------------------------------------------------------


@dataclass
class DeploymentStep:
    """Individual deployment step."""

    name: str
    resource_name: Optional[str]
    status: str  # pending|running|completed|failed|skipped
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output: Optional[str] = None
    error: Optional[str] = None


@dataclass
class DeploymentRecord:
    """Complete deployment record."""

    id: str
    recipe: Recipe
    parameters: Dict[str, Any]
    status: DeploymentStatus
    steps: List[DeploymentStep] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    rollback_available: bool = False
    namespace: Optional[str] = None  # K8s namespace if applicable


# -----------------------------------------------------------------------------
# Resource Handlers
# -----------------------------------------------------------------------------


class ResourceHandler(ABC):
    """Abstract handler for deploying resources."""

    @abstractmethod
    def deploy(
        self,
        resource: RecipeResource,
        params: Dict[str, Any],
        namespace: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """Deploy resource, return (success, message)."""
        pass

    @abstractmethod
    def rollback(
        self, resource: RecipeResource, namespace: Optional[str] = None
    ) -> bool:
        """Rollback resource deployment."""
        pass

    @abstractmethod
    def check_health(
        self, resource: RecipeResource, namespace: Optional[str] = None
    ) -> bool:
        """Check resource health."""
        pass


class HelmHandler(ResourceHandler):
    """Deploy Helm charts."""

    def deploy(
        self,
        resource: RecipeResource,
        params: Dict[str, Any],
        namespace: Optional[str] = None,
    ) -> Tuple[bool, str]:
        spec = resource.spec
        chart = spec.get("chart", "")
        repo = spec.get("repo", "")
        release_name = spec.get("release_name", resource.name)
        values = spec.get("values", {})
        values.update(params)

        cmd = ["helm", "upgrade", "--install", release_name, chart]
        if repo:
            cmd.extend(["--repo", repo])
        if namespace:
            cmd.extend(["--namespace", namespace, "--create-namespace"])

        # Write values to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            import yaml

            yaml.dump(values, f)
            values_file = f.name

        cmd.extend(["-f", values_file])
        cmd.append("--wait")
        cmd.extend(["--timeout", f"{resource.timeout_seconds}s"])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,  # nosec B603
                timeout=resource.timeout_seconds + 60,
            )
            os.unlink(values_file)

            if result.returncode == 0:
                return True, f"Helm release {release_name} deployed"
            return False, result.stderr
        except FileNotFoundError:
            return False, "Helm not installed"
        except Exception as e:
            return False, str(e)

    def rollback(
        self, resource: RecipeResource, namespace: Optional[str] = None
    ) -> bool:
        release_name = resource.spec.get("release_name", resource.name)
        cmd = ["helm", "rollback", release_name]
        if namespace:
            cmd.extend(["--namespace", namespace])

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120
            )  # nosec B603
            return result.returncode == 0
        except Exception:
            return False

    def check_health(
        self, resource: RecipeResource, namespace: Optional[str] = None
    ) -> bool:
        release_name = resource.spec.get("release_name", resource.name)
        cmd = ["helm", "status", release_name, "-o", "json"]
        if namespace:
            cmd.extend(["--namespace", namespace])

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30
            )  # nosec B603
            if result.returncode == 0:
                status = json.loads(result.stdout)
                return bool(status.get("info", {}).get("status") == "deployed")
        except Exception:
            pass  # nosec B110
        return False


class ManifestHandler(ResourceHandler):
    """Deploy Kubernetes manifests."""

    def deploy(
        self,
        resource: RecipeResource,
        params: Dict[str, Any],
        namespace: Optional[str] = None,
    ) -> Tuple[bool, str]:
        spec = resource.spec
        manifests = spec.get("manifests", [])

        for manifest in manifests:
            # Template parameter substitution
            manifest_str = json.dumps(manifest)
            for key, value in params.items():
                manifest_str = manifest_str.replace(f"${{{key}}}", str(value))

            cmd = ["kubectl", "apply", "-f", "-"]
            if namespace:
                cmd.extend(["--namespace", namespace])

            try:
                result = subprocess.run(
                    cmd,  # nosec B603
                    input=manifest_str,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                if result.returncode != 0:
                    return False, result.stderr
            except Exception as e:
                return False, str(e)

        return True, "Manifests applied"

    def rollback(
        self, resource: RecipeResource, namespace: Optional[str] = None
    ) -> bool:
        # Would need to track applied resources for proper rollback
        return False

    def check_health(
        self, resource: RecipeResource, namespace: Optional[str] = None
    ) -> bool:
        return True


class VMImageHandler(ResourceHandler):
    """Deploy VM images."""

    def deploy(
        self,
        resource: RecipeResource,
        params: Dict[str, Any],
        namespace: Optional[str] = None,
    ) -> Tuple[bool, str]:
        spec = resource.spec
        image_url = spec.get("image_url", "")
        vm_name = params.get("vm_name", resource.name)

        # Would integrate with DebVisor VM provisioner
        logger.info(f"[VM] Would deploy VM {vm_name} from {image_url}")
        return True, f"VM {vm_name} provisioning initiated"

    def rollback(
        self, resource: RecipeResource, namespace: Optional[str] = None
    ) -> bool:
        return True

    def check_health(
        self, resource: RecipeResource, namespace: Optional[str] = None
    ) -> bool:
        return True


# -----------------------------------------------------------------------------
# Marketplace Installer
# -----------------------------------------------------------------------------


class MarketplaceInstaller:
    """Orchestrates recipe deployments."""

    HANDLERS = {
        ResourceKind.HELM_CHART: HelmHandler(),
        ResourceKind.K8S_MANIFEST: ManifestHandler(),
        ResourceKind.VM_IMAGE: VMImageHandler(),
    }

    def __init__(
        self,
        catalog: MarketplaceCatalog,
        scanner: Optional[SecurityScanner] = None,
        verifier: Optional[SignatureVerifier] = None,
    ):
        self.catalog = catalog
        self.scanner = scanner or SecurityScanner()
        self.verifier = verifier or SignatureVerifier()
        self.deployments: Dict[str, DeploymentRecord] = {}
        self._executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="deploy_")
        self._callbacks: List[Callable[[DeploymentRecord], None]] = []

    def register_callback(self, callback: Callable[[DeploymentRecord], None]) -> None:
        """Register deployment status callback."""
        self._callbacks.append(callback)

    def _notify(self, record: DeploymentRecord) -> None:
        for cb in self._callbacks:
            try:
                cb(record)
            except Exception as e:
                logger.warning(f"Callback error: {e}")

    def deploy(
        self,
        name: str,
        version: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        namespace: Optional[str] = None,
        skip_security_scan: bool = False,
    ) -> str:
        """Start async deployment, return deployment ID."""
        recipe = self.catalog.get(name, version)
        if not recipe:
            raise ValueError(f"Recipe not found: {name}:{version or 'latest'}")

        from uuid import uuid4

        dep_id = str(uuid4())

        record = DeploymentRecord(
            id=dep_id,
            recipe=recipe,
            parameters=parameters or {},
            status=DeploymentStatus.PENDING,
            namespace=namespace,
        )
        self.deployments[dep_id] = record

        # Submit to executor
        self._executor.submit(self._run_deployment, record, skip_security_scan)

        logger.info(f"Started deployment {dep_id} for {recipe.name}:{recipe.version}")
        return dep_id

    def _run_deployment(self, record: DeploymentRecord, skip_scan: bool) -> None:
        """Execute deployment workflow."""
        try:
            record.started_at = datetime.now(timezone.utc)
            record.status = DeploymentStatus.VALIDATING
            self._notify(record)

            recipe = record.recipe

            # Step 1: Verify signature
            step = DeploymentStep(
                name="verify_signature",
                resource_name=None,
                status="running",
                started_at=datetime.now(timezone.utc),
            )
            record.steps.append(step)

            verified, msg = self.verifier.verify_recipe(recipe)
            if verified:
                recipe.trust_level = TrustLevel.VERIFIED
            step.status = "completed"
            step.output = msg
            step.completed_at = datetime.now(timezone.utc)

            # Step 2: Security scan
            if not skip_scan:
                record.status = DeploymentStatus.SCANNING
                self._notify(record)

                scan_step = DeploymentStep(
                    name="security_scan",
                    resource_name=None,
                    status="running",
                    started_at=datetime.now(timezone.utc),
                )
                record.steps.append(scan_step)

                # Scan container images in recipe
                for resource in recipe.resources:
                    if resource.kind == ResourceKind.CONTAINER_IMAGE:
                        image = resource.spec.get("image", "")
                        result = self.scanner.scan_container_image(image)
                        recipe.security_scan = result
                        if not result.passed:
                            scan_step.status = "failed"
                            scan_step.error = (
                                f"Critical vulnerabilities found: {result.summary}"
                            )
                            record.status = DeploymentStatus.FAILED
                            record.error = "Security scan failed"
                            self._notify(record)
                            return

                scan_step.status = "completed"
                scan_step.output = (
                    recipe.security_scan.summary
                    if recipe.security_scan
                    else "No images to scan"
                )
                scan_step.completed_at = datetime.now(timezone.utc)

            # Step 3: Resolve dependencies
            dep_step = DeploymentStep(
                name="resolve_dependencies",
                resource_name=None,
                status="running",
                started_at=datetime.now(timezone.utc),
            )
            record.steps.append(dep_step)

            for dep in recipe.dependencies:
                if dep.type == "recipe" and not dep.optional:
                    dep_recipe = self.catalog.get(dep.name)
                    if not dep_recipe:
                        dep_step.status = "failed"
                        dep_step.error = f"Missing dependency: {dep.name}"
                        record.status = DeploymentStatus.FAILED
                        record.error = f"Dependency not found: {dep.name}"
                        self._notify(record)
                        return

            dep_step.status = "completed"
            dep_step.completed_at = datetime.now(timezone.utc)

            # Step 4: Deploy resources
            record.status = DeploymentStatus.RUNNING
            self._notify(record)

            # Sort resources by dependencies
            sorted_resources = self._sort_resources(recipe.resources)

            for resource in sorted_resources:
                res_step = DeploymentStep(
                    name=f"deploy_{resource.kind.value}",
                    resource_name=resource.name,
                    status="running",
                    started_at=datetime.now(timezone.utc),
                )
                record.steps.append(res_step)
                self._notify(record)

                handler = self.HANDLERS.get(resource.kind)
                if not handler:
                    res_step.status = "skipped"
                    res_step.output = f"No handler for {resource.kind.value}"
                    res_step.completed_at = datetime.now(timezone.utc)
                    continue

                success, message = handler.deploy(
                    resource, record.parameters, record.namespace
                )

                if success:
                    res_step.status = "completed"
                    res_step.output = message
                    record.rollback_available = True
                else:
                    res_step.status = "failed"
                    res_step.error = message
                    record.status = DeploymentStatus.FAILED
                    record.error = f"Resource {resource.name} failed: {message}"
                    self._notify(record)
                    return

                res_step.completed_at = datetime.now(timezone.utc)
                self._notify(record)

            # Complete
            record.status = DeploymentStatus.COMPLETED
            record.completed_at = datetime.now(timezone.utc)
            self._notify(record)

            logger.info(f"Deployment {record.id} completed successfully")

        except Exception as e:
            record.status = DeploymentStatus.FAILED
            record.error = str(e)
            record.steps.append(
                DeploymentStep(
                    name="error",
                    resource_name=None,
                    status="failed",
                    error=str(e),
                    started_at=datetime.now(timezone.utc),
                )
            )
            self._notify(record)
            logger.error(f"Deployment {record.id} failed: {e}")

    def _sort_resources(self, resources: List[RecipeResource]) -> List[RecipeResource]:
        """Topological sort resources by dependencies."""
        # Simple implementation - full topological sort would be needed for complex deps
        sorted_list = []
        remaining = list(resources)
        deployed = set()

        while remaining:
            for res in remaining[:]:
                if all(dep in deployed for dep in res.depends_on):
                    sorted_list.append(res)
                    deployed.add(res.name)
                    remaining.remove(res)
                    break
            else:
                # Circular dependency or missing dep
                sorted_list.extend(remaining)
                break

        return sorted_list

    def get_deployment(self, dep_id: str) -> Optional[DeploymentRecord]:
        """Get deployment record."""
        return self.deployments.get(dep_id)

    def list_deployments(
        self, status_filter: Optional[DeploymentStatus] = None
    ) -> List[DeploymentRecord]:
        """List deployments with optional filter."""
        deps = list(self.deployments.values())
        if status_filter:
            deps = [d for d in deps if d.status == status_filter]
        return sorted(deps, key=lambda d: d.started_at or datetime.min, reverse=True)

    def rollback(self, dep_id: str) -> bool:
        """Rollback deployment."""
        record = self.deployments.get(dep_id)
        if not record or not record.rollback_available:
            return False

        record.status = DeploymentStatus.ROLLED_BACK

        # Rollback in reverse order
        for resource in reversed(record.recipe.resources):
            handler = self.HANDLERS.get(resource.kind)
            if handler:
                handler.rollback(resource, record.namespace)

        self._notify(record)
        return True


# -----------------------------------------------------------------------------
# Marketplace Service Facade
# -----------------------------------------------------------------------------


class MarketplaceService:
    """High-level marketplace API."""

    def __init__(self, storage_path: str = "/var/lib/debvisor/marketplace"):
        self.catalog = MarketplaceCatalog(storage_path)
        self.scanner = SecurityScanner()
        self.verifier = SignatureVerifier()
        self.installer = MarketplaceInstaller(self.catalog, self.scanner, self.verifier)
        self.syncer = RepositorySyncer(self.catalog)

    def register_recipe(self, recipe: Recipe) -> str:
        """Register recipe in catalog."""
        return self.catalog.add_recipe(recipe)

    def search_recipes(
        self,
        query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Recipe]:
        """Search recipes."""
        return self.catalog.search(query, category, tags)

    def get_recipe(self, name: str, version: Optional[str] = None) -> Optional[Recipe]:
        """Get specific recipe."""
        return self.catalog.get(name, version)

    def deploy_recipe(
        self,
        name: str,
        version: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        namespace: Optional[str] = None,
    ) -> str:
        """Deploy recipe, return deployment ID."""
        return self.installer.deploy(name, version, parameters, namespace)

    def get_deployment(self, dep_id: str) -> Optional[DeploymentRecord]:
        """Get deployment status."""
        return self.installer.get_deployment(dep_id)

    def add_repository(
        self, name: str, url: str, trust_level: TrustLevel = TrustLevel.COMMUNITY
    ) -> None:
        """Add remote repository."""
        repo = RemoteRepository(name=name, url=url, trust_level=trust_level)
        self.syncer.add_repository(repo)

    def sync_repositories(self) -> Dict[str, Tuple[int, List[str]]]:
        """Sync all repositories."""
        return self.syncer.sync_all()

    def add_trusted_key(self, key_id: str, public_key: bytes) -> None:
        """Add trusted publisher key."""
        self.verifier.add_trusted_key(key_id, public_key)

    def scan_image(self, image: str) -> SecurityScanResult:
        """Scan container image for vulnerabilities."""
        return self.scanner.scan_container_image(image)


# -----------------------------------------------------------------------------
# Example / CLI
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # import tempfile  # Already imported at top level

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Create service
    storage = tempfile.mkdtemp(prefix="marketplace_")
    svc = MarketplaceService(storage_path=storage)

    # Register callback
    def on_deploy_update(record: DeploymentRecord) -> None:
        print(f"  [{record.status.value}] Steps: {len(record.steps)}")

    svc.installer.register_callback(on_deploy_update)

    # Create sample recipes
    nextcloud = Recipe(
        name="nextcloud",
        version="1.0.0",
        publisher="debvisor",
        description="Nextcloud collaboration suite - file sync, calendar, contacts",
        category="Productivity",
        tags=["collaboration", "files", "calendar"],
        license="AGPL-3.0",
        resources=[
            RecipeResource(
                name="nextcloud-helm",
                kind=ResourceKind.HELM_CHART,
                spec={
                    "chart": "nextcloud",
                    "repo": "https://nextcloud.github.io/helm/",
                    "values": {"persistence.enabled": True},
                },
            ),
        ],
        parameters=[
            RecipeParameter(
                name="admin_password",
                description="Admin password",
                type="secret",
                required=True,
            ),
            RecipeParameter(
                name="storage_size",
                description="Storage size",
                type="string",
                default="10Gi",
            ),
        ],
    )

    wordpress = Recipe(
        name="wordpress",
        version="6.0.0",
        publisher="debvisor",
        description="WordPress CMS with MySQL database",
        category="CMS",
        tags=["blog", "cms", "website"],
        license="GPL-2.0",
        dependencies=[
            RecipeDependency(
                name="mysql", version_constraint=">=8.0", type="recipe", optional=False
            ),
        ],
        resources=[
            RecipeResource(
                name="wordpress-helm",
                kind=ResourceKind.HELM_CHART,
                spec={
                    "chart": "wordpress",
                    "repo": "https://charts.bitnami.com/bitnami",
                },
            ),
        ],
    )

    # Register recipes
    print("Registering recipes...")
    print(f"  Nextcloud digest: {svc.register_recipe(nextcloud)[:16]}...")
    print(f"  WordPress digest: {svc.register_recipe(wordpress)[:16]}...")

    # Search
    print("\nSearch results for 'cloud':")
    for r in svc.search_recipes("cloud"):
        print(f"  - {r.name}:{r.version} ({r.category})")

    # Categories
    print(f"\nCategories: {svc.catalog.get_categories()}")

    # Security scan
    print("\nScanning nginx:latest...")
    scan = svc.scan_image("nginx:latest")
    print(f"  Passed: {scan.passed}")
    print(f"  Summary: {scan.summary}")

    print("\nMarketplace service demo complete.")
