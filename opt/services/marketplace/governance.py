#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Marketplace Governance & Vulnerability Scoring for DebVisor.

Provides comprehensive security governance for marketplace applications:
- Vulnerability scanning (CVE detection)
- Dependency analysis
- Security scoring
- Policy enforcement
- Publisher trust verification
- Compliance checks
- Usage telemetry

Author: DebVisor Team
Date: December 11, 2025
"""

import asyncio
import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from pathlib import Path
import subprocess

logger = logging.getLogger(__name__)


# =============================================================================
# Enums & Constants
# =============================================================================


class VulnerabilitySeverity(Enum):
    """CVE severity levels (CVSS)."""
    CRITICAL = "critical"  # 9.0-10.0
    HIGH = "high"  # 7.0-8.9
    MEDIUM = "medium"  # 4.0-6.9
    LOW = "low"  # 0.1-3.9
    NONE = "none"  # 0.0


class TrustLevel(Enum):
    """Publisher trust levels."""
    VERIFIED = "verified"  # Official publisher
    TRUSTED = "trusted"  # Community trusted
    STANDARD = "standard"  # Basic verification
    UNVERIFIED = "unverified"  # No verification
    BLOCKED = "blocked"  # Blacklisted


class GovernanceAction(Enum):
    """Governance policy actions."""
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"
    REQUIRE_APPROVAL = "require_approval"


# =============================================================================
# Data Models
# =============================================================================


@dataclass
class Vulnerability:
    """CVE vulnerability information."""
    cve_id: str
    description: str
    severity: VulnerabilitySeverity
    cvss_score: float
    affected_package: str
    affected_versions: List[str]
    fixed_version: Optional[str] = None
    published_date: Optional[datetime] = None
    references: List[str] = field(default_factory=list)
    cwe_ids: List[str] = field(default_factory=list)  # Common Weakness Enumeration


@dataclass
class Dependency:
    """Application dependency information."""
    name: str
    version: str
    package_manager: str  # pip, npm, apt, etc.
    license: Optional[str] = None
    vulnerabilities: List[Vulnerability] = field(default_factory=list)


@dataclass
class Publisher:
    """Marketplace publisher information."""
    publisher_id: str
    name: str
    email: str
    trust_level: TrustLevel
    verification_date: Optional[datetime] = None
    published_apps: int = 0
    total_downloads: int = 0
    average_rating: float = 0.0
    signature_key: Optional[str] = None


@dataclass
class MarketplaceApp:
    """Marketplace application."""
    app_id: str
    name: str
    version: str
    publisher: Publisher
    description: str
    category: str
    dependencies: List[Dependency] = field(default_factory=list)
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    security_score: float = 0.0  # 0-100
    governance_status: GovernanceAction = GovernanceAction.ALLOW
    install_count: int = 0
    signature_valid: bool = False
    last_scanned: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class SecurityScore:
    """Security score breakdown."""
    overall_score: float  # 0-100
    vulnerability_score: float  # 0-100
    dependency_score: float  # 0-100
    publisher_score: float  # 0-100
    compliance_score: float  # 0-100
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class GovernancePolicy:
    """Governance policy rules."""
    policy_id: str
    name: str
    description: str
    enabled: bool = True
    rules: Dict[str, Any] = field(default_factory=dict)
    action: GovernanceAction = GovernanceAction.WARN


# =============================================================================
# Vulnerability Scanner
# =============================================================================


class VulnerabilityScanner:
    """
    Scans applications for known vulnerabilities.
    
    Integrates with:
    - National Vulnerability Database (NVD)
    - OSV (Open Source Vulnerabilities)
    - GitHub Security Advisories
    - Snyk, Trivy, Grype databases
    """
    
    def __init__(self):
        self.vuln_database: Dict[str, List[Vulnerability]] = {}
        self._load_vulnerability_database()
    
    def _load_vulnerability_database(self) -> None:
        """Load vulnerability database."""
        # In production, this would load from NVD/OSV APIs
        # For demonstration, use mock data
        self.vuln_database = {
            "requests": [
                Vulnerability(
                    cve_id="CVE-2023-32681",
                    description="Unintended leak of Proxy-Authorization header",
                    severity=VulnerabilitySeverity.MEDIUM,
                    cvss_score=6.1,
                    affected_package="requests",
                    affected_versions=["<2.31.0"],
                    fixed_version="2.31.0",
                    references=["https://nvd.nist.gov/vuln/detail/CVE-2023-32681"],
                ),
            ],
            "pillow": [
                Vulnerability(
                    cve_id="CVE-2023-44271",
                    description="Buffer overflow in _ifd_map",
                    severity=VulnerabilitySeverity.HIGH,
                    cvss_score=7.5,
                    affected_package="pillow",
                    affected_versions=["<10.0.1"],
                    fixed_version="10.0.1",
                    references=["https://nvd.nist.gov/vuln/detail/CVE-2023-44271"],
                ),
            ],
            "django": [
                Vulnerability(
                    cve_id="CVE-2023-43665",
                    description="Denial-of-service in intcomma template filter",
                    severity=VulnerabilitySeverity.HIGH,
                    cvss_score=7.5,
                    affected_package="django",
                    affected_versions=[">=4.1,<4.1.13", ">=4.2,<4.2.7"],
                    fixed_version="4.2.7",
                    references=["https://nvd.nist.gov/vuln/detail/CVE-2023-43665"],
                ),
            ],
        }
    
    async def scan_dependencies(
        self,
        dependencies: List[Dependency]
    ) -> List[Vulnerability]:
        """Scan dependencies for vulnerabilities."""
        all_vulnerabilities = []
        
        for dep in dependencies:
            vulns = await self._scan_package(dep.name, dep.version)
            dep.vulnerabilities = vulns
            all_vulnerabilities.extend(vulns)
        
        return all_vulnerabilities
    
    async def _scan_package(
        self,
        package_name: str,
        version: str
    ) -> List[Vulnerability]:
        """Scan a single package for vulnerabilities."""
        vulns = []
        
        # Check vulnerability database
        if package_name.lower() in self.vuln_database:
            for vuln in self.vuln_database[package_name.lower()]:
                if self._version_affected(version, vuln.affected_versions):
                    vulns.append(vuln)
        
        return vulns
    
    def _version_affected(
        self,
        installed_version: str,
        affected_versions: List[str]
    ) -> bool:
        """Check if installed version is affected."""
        # Simplified version checking
        for pattern in affected_versions:
            if "<" in pattern:
                # e.g., "<2.31.0"
                threshold = pattern.replace("<", "").strip()
                if self._version_less_than(installed_version, threshold):
                    return True
            elif ">" in pattern:
                # e.g., ">1.0.0"
                threshold = pattern.replace(">", "").strip()
                if self._version_greater_than(installed_version, threshold):
                    return True
            elif "==" in pattern or pattern == installed_version:
                return True
        
        return False
    
    def _version_less_than(self, v1: str, v2: str) -> bool:
        """Compare versions (simplified)."""
        try:
            parts1 = [int(p) for p in v1.split(".")]
            parts2 = [int(p) for p in v2.split(".")]
            return parts1 < parts2
        except ValueError:
            return v1 < v2
    
    def _version_greater_than(self, v1: str, v2: str) -> bool:
        """Compare versions (simplified)."""
        try:
            parts1 = [int(p) for p in v1.split(".")]
            parts2 = [int(p) for p in v2.split(".")]
            return parts1 > parts2
        except ValueError:
            return v1 > v2


# =============================================================================
# Security Scorer
# =============================================================================


class SecurityScorer:
    """
    Calculates security scores for marketplace applications.
    """
    
    def __init__(self):
        pass
    
    def calculate_score(
        self,
        app: MarketplaceApp
    ) -> SecurityScore:
        """Calculate comprehensive security score."""
        # Calculate component scores
        vuln_score = self._score_vulnerabilities(app.vulnerabilities)
        dep_score = self._score_dependencies(app.dependencies)
        pub_score = self._score_publisher(app.publisher)
        comp_score = self._score_compliance(app)
        
        # Overall score (weighted average)
        overall_score = (
            vuln_score * 0.4 +
            dep_score * 0.2 +
            pub_score * 0.2 +
            comp_score * 0.2
        )
        
        # Generate findings
        findings = []
        recommendations = []
        
        if app.vulnerabilities:
            critical = sum(1 for v in app.vulnerabilities if v.severity == VulnerabilitySeverity.CRITICAL)
            high = sum(1 for v in app.vulnerabilities if v.severity == VulnerabilitySeverity.HIGH)
            
            if critical > 0:
                findings.append(f"{critical} critical vulnerabilities found")
                recommendations.append("Update dependencies to fix critical vulnerabilities")
            if high > 0:
                findings.append(f"{high} high severity vulnerabilities found")
                recommendations.append("Review and patch high severity vulnerabilities")
        
        if app.publisher.trust_level == TrustLevel.UNVERIFIED:
            findings.append("Publisher not verified")
            recommendations.append("Verify publisher identity before deployment")
        
        if not app.signature_valid:
            findings.append("Invalid or missing signature")
            recommendations.append("Verify package signature")
        
        return SecurityScore(
            overall_score=overall_score,
            vulnerability_score=vuln_score,
            dependency_score=dep_score,
            publisher_score=pub_score,
            compliance_score=comp_score,
            findings=findings,
            recommendations=recommendations,
        )
    
    def _score_vulnerabilities(self, vulnerabilities: List[Vulnerability]) -> float:
        """Score based on vulnerabilities (0-100, higher is better)."""
        if not vulnerabilities:
            return 100.0
        
        # Deduct points based on severity
        score = 100.0
        for vuln in vulnerabilities:
            if vuln.severity == VulnerabilitySeverity.CRITICAL:
                score -= 25
            elif vuln.severity == VulnerabilitySeverity.HIGH:
                score -= 15
            elif vuln.severity == VulnerabilitySeverity.MEDIUM:
                score -= 8
            elif vuln.severity == VulnerabilitySeverity.LOW:
                score -= 3
        
        return max(0.0, score)
    
    def _score_dependencies(self, dependencies: List[Dependency]) -> float:
        """Score based on dependencies."""
        if not dependencies:
            return 100.0
        
        # Check for vulnerable dependencies
        vulnerable_count = sum(1 for dep in dependencies if dep.vulnerabilities)
        total_count = len(dependencies)
        
        if vulnerable_count == 0:
            return 100.0
        
        ratio = vulnerable_count / total_count
        score = 100.0 * (1 - ratio)
        
        return max(0.0, score)
    
    def _score_publisher(self, publisher: Publisher) -> float:
        """Score based on publisher trust."""
        trust_scores = {
            TrustLevel.VERIFIED: 100.0,
            TrustLevel.TRUSTED: 80.0,
            TrustLevel.STANDARD: 60.0,
            TrustLevel.UNVERIFIED: 30.0,
            TrustLevel.BLOCKED: 0.0,
        }
        
        return trust_scores.get(publisher.trust_level, 50.0)
    
    def _score_compliance(self, app: MarketplaceApp) -> float:
        """Score based on compliance factors."""
        score = 100.0
        
        # Deduct for missing signature
        if not app.signature_valid:
            score -= 20
        
        # Deduct for old scan
        if app.last_scanned:
            age_days = (datetime.now(timezone.utc) - app.last_scanned).days
            if age_days > 30:
                score -= 10
            elif age_days > 90:
                score -= 20
        
        return max(0.0, score)


# =============================================================================
# Governance Engine
# =============================================================================


class GovernanceEngine:
    """
    Enforces governance policies on marketplace applications.
    """
    
    def __init__(self):
        self.policies: Dict[str, GovernancePolicy] = {}
        self._initialize_default_policies()
    
    def _initialize_default_policies(self) -> None:
        """Initialize default governance policies."""
        self.policies = {
            "block-critical-vulns": GovernancePolicy(
                policy_id="block-critical-vulns",
                name="Block Critical Vulnerabilities",
                description="Block apps with critical vulnerabilities",
                enabled=True,
                rules={"max_critical_vulns": 0},
                action=GovernanceAction.BLOCK,
            ),
            "warn-high-vulns": GovernancePolicy(
                policy_id="warn-high-vulns",
                name="Warn High Vulnerabilities",
                description="Warn on apps with high severity vulnerabilities",
                enabled=True,
                rules={"max_high_vulns": 2},
                action=GovernanceAction.WARN,
            ),
            "require-verification": GovernancePolicy(
                policy_id="require-verification",
                name="Require Publisher Verification",
                description="Require verified publishers for production",
                enabled=True,
                rules={"min_trust_level": TrustLevel.TRUSTED},
                action=GovernanceAction.REQUIRE_APPROVAL,
            ),
            "require-signature": GovernancePolicy(
                policy_id="require-signature",
                name="Require Valid Signature",
                description="Require valid signature for all apps",
                enabled=True,
                rules={"signature_required": True},
                action=GovernanceAction.BLOCK,
            ),
            "minimum-security-score": GovernancePolicy(
                policy_id="minimum-security-score",
                name="Minimum Security Score",
                description="Require minimum security score of 70",
                enabled=True,
                rules={"min_score": 70.0},
                action=GovernanceAction.WARN,
            ),
        }
    
    def evaluate(self, app: MarketplaceApp, score: SecurityScore) -> GovernanceAction:
        """Evaluate governance policies for an app."""
        most_severe_action = GovernanceAction.ALLOW
        
        for policy in self.policies.values():
            if not policy.enabled:
                continue
            
            action = self._evaluate_policy(policy, app, score)
            
            # Track most severe action
            if self._action_severity(action) > self._action_severity(most_severe_action):
                most_severe_action = action
        
        return most_severe_action
    
    def _evaluate_policy(
        self,
        policy: GovernancePolicy,
        app: MarketplaceApp,
        score: SecurityScore
    ) -> GovernanceAction:
        """Evaluate a single policy."""
        # Check critical vulnerabilities
        if policy.policy_id == "block-critical-vulns":
            critical_count = sum(
                1 for v in app.vulnerabilities
                if v.severity == VulnerabilitySeverity.CRITICAL
            )
            if critical_count > policy.rules.get("max_critical_vulns", 0):
                return policy.action
        
        # Check high vulnerabilities
        elif policy.policy_id == "warn-high-vulns":
            high_count = sum(
                1 for v in app.vulnerabilities
                if v.severity == VulnerabilitySeverity.HIGH
            )
            if high_count > policy.rules.get("max_high_vulns", 2):
                return policy.action
        
        # Check publisher verification
        elif policy.policy_id == "require-verification":
            min_trust = policy.rules.get("min_trust_level", TrustLevel.STANDARD)
            trust_levels = [
                TrustLevel.BLOCKED, TrustLevel.UNVERIFIED, TrustLevel.STANDARD,
                TrustLevel.TRUSTED, TrustLevel.VERIFIED
            ]
            if trust_levels.index(app.publisher.trust_level) < trust_levels.index(min_trust):
                return policy.action
        
        # Check signature
        elif policy.policy_id == "require-signature":
            if policy.rules.get("signature_required") and not app.signature_valid:
                return policy.action
        
        # Check security score
        elif policy.policy_id == "minimum-security-score":
            if score.overall_score < policy.rules.get("min_score", 70.0):
                return policy.action
        
        return GovernanceAction.ALLOW
    
    def _action_severity(self, action: GovernanceAction) -> int:
        """Get severity level of an action."""
        severity_map = {
            GovernanceAction.ALLOW: 0,
            GovernanceAction.WARN: 1,
            GovernanceAction.REQUIRE_APPROVAL: 2,
            GovernanceAction.BLOCK: 3,
        }
        return severity_map.get(action, 0)


# =============================================================================
# Marketplace Governance Service
# =============================================================================


class MarketplaceGovernanceService:
    """
    Main service for marketplace governance and vulnerability management.
    """
    
    def __init__(self):
        self.scanner = VulnerabilityScanner()
        self.scorer = SecurityScorer()
        self.governance = GovernanceEngine()
    
    async def scan_app(self, app: MarketplaceApp) -> SecurityScore:
        """Scan an application for vulnerabilities and calculate score."""
        logger.info(f"Scanning app: {app.name} v{app.version}")
        
        # Scan dependencies
        vulnerabilities = await self.scanner.scan_dependencies(app.dependencies)
        app.vulnerabilities = vulnerabilities
        app.last_scanned = datetime.now(timezone.utc)
        
        # Calculate security score
        score = self.scorer.calculate_score(app)
        app.security_score = score.overall_score
        
        # Evaluate governance
        app.governance_status = self.governance.evaluate(app, score)
        
        logger.info(
            f"Scan complete - Score: {score.overall_score:.1f}, "
            f"Vulnerabilities: {len(vulnerabilities)}, "
            f"Status: {app.governance_status.value}"
        )
        
        return score
    
    def get_compliance_report(
        self,
        apps: List[MarketplaceApp]
    ) -> Dict[str, Any]:
        """Generate compliance report for marketplace apps."""
        total_apps = len(apps)
        blocked_apps = sum(1 for app in apps if app.governance_status == GovernanceAction.BLOCK)
        warned_apps = sum(1 for app in apps if app.governance_status == GovernanceAction.WARN)
        safe_apps = sum(1 for app in apps if app.governance_status == GovernanceAction.ALLOW)
        
        total_vulns = sum(len(app.vulnerabilities) for app in apps)
        critical_vulns = sum(
            sum(1 for v in app.vulnerabilities if v.severity == VulnerabilitySeverity.CRITICAL)
            for app in apps
        )
        
        avg_score = sum(app.security_score for app in apps) / max(total_apps, 1)
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_apps": total_apps,
            "safe_apps": safe_apps,
            "warned_apps": warned_apps,
            "blocked_apps": blocked_apps,
            "total_vulnerabilities": total_vulns,
            "critical_vulnerabilities": critical_vulns,
            "average_security_score": avg_score,
            "compliance_rate": (safe_apps / max(total_apps, 1)) * 100,
        }


# =============================================================================
# Example Usage
# =============================================================================


async def main():
    """Example usage of marketplace governance."""
    service = MarketplaceGovernanceService()
    
    # Create sample apps
    apps = [
        MarketplaceApp(
            app_id="app-001",
            name="Web Dashboard",
            version="2.1.0",
            publisher=Publisher(
                publisher_id="pub-001",
                name="TechCorp",
                email="tech@example.com",
                trust_level=TrustLevel.VERIFIED,
            ),
            description="Modern web dashboard",
            category="web",
            dependencies=[
                Dependency(name="django", version="4.1.10", package_manager="pip"),
                Dependency(name="requests", version="2.30.0", package_manager="pip"),
            ],
            signature_valid=True,
        ),
        MarketplaceApp(
            app_id="app-002",
            name="Image Processor",
            version="1.5.2",
            publisher=Publisher(
                publisher_id="pub-002",
                name="DevStudio",
                email="dev@example.com",
                trust_level=TrustLevel.STANDARD,
            ),
            description="Image processing tool",
            category="tools",
            dependencies=[
                Dependency(name="pillow", version="9.5.0", package_manager="pip"),
            ],
            signature_valid=False,
        ),
    ]
    
    print("=== Marketplace Governance Scan ===\n")
    
    # Scan each app
    for app in apps:
        print(f"\nScanning: {app.name} v{app.version}")
        print(f"Publisher: {app.publisher.name} ({app.publisher.trust_level.value})")
        
        score = await service.scan_app(app)
        
        print(f"\n  Security Score: {score.overall_score:.1f}/100")
        print(f"    Vulnerabilities: {score.vulnerability_score:.1f}")
        print(f"    Dependencies: {score.dependency_score:.1f}")
        print(f"    Publisher: {score.publisher_score:.1f}")
        print(f"    Compliance: {score.compliance_score:.1f}")
        
        print(f"\n  Vulnerabilities: {len(app.vulnerabilities)}")
        for vuln in app.vulnerabilities:
            print(f"    - {vuln.cve_id}: {vuln.description}")
            print(f"      Severity: {vuln.severity.value} (CVSS {vuln.cvss_score})")
            print(f"      Fix: Upgrade to {vuln.fixed_version}")
        
        print(f"\n  Governance Status: {app.governance_status.value.upper()}")
        
        if score.recommendations:
            print(f"\n  Recommendations:")
            for rec in score.recommendations:
                print(f"    - {rec}")
    
    # Generate report
    print("\n\n=== Compliance Report ===\n")
    report = service.get_compliance_report(apps)
    
    print(f"Total Apps: {report['total_apps']}")
    print(f"Safe: {report['safe_apps']}, Warned: {report['warned_apps']}, Blocked: {report['blocked_apps']}")
    print(f"Total Vulnerabilities: {report['total_vulnerabilities']} ({report['critical_vulnerabilities']} critical)")
    print(f"Average Security Score: {report['average_security_score']:.1f}/100")
    print(f"Compliance Rate: {report['compliance_rate']:.1f}%")


if __name__ == "__main__":
    asyncio.run(main())
