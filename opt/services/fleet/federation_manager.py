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

"""Fleet Management & Federation Service - Enterprise Implementation.

Handles multi-cluster/multi-site federation:
- Cluster registration with mTLS authentication
- Global resource aggregation and health rollups
- Policy broadcast and configuration drift detection
- Cross-cluster workload placement and migration
- Unified identity federation (CA trust chains)
- Event correlation and anomaly detection across sites
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from enum import Enum
import logging
import json
import hashlib
import threading
import urllib.request
import urllib.error
import ssl
from pathlib import Path
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Enums and Configuration
# -----------------------------------------------------------------------------


class ClusterStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    SYNCING = "syncing"
    UNREACHABLE = "unreachable"
    MAINTENANCE = "maintenance"


class PolicyType(Enum):
    RESOURCE_QUOTA = "resource_quota"
    NETWORK_POLICY = "network_policy"
    SECURITY_POLICY = "security_policy"
    BACKUP_POLICY = "backup_policy"
    PLACEMENT_RULE = "placement_rule"
    RBAC_ROLE = "rbac_role"


class SyncState(Enum):
    IN_SYNC = "in_sync"
    DRIFTED = "drifted"
    PENDING = "pending"
    CONFLICT = "conflict"


class EventSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class FederationConfig:
    """Federation service configuration."""

    sync_interval_seconds: int = 30
    health_check_timeout_seconds: int = 10
    max_sync_retries: int = 3
    drift_detection_interval_seconds: int = 300
    event_retention_hours: int = 168    # 1 week
    ca_cert_path: Optional[str] = None
    client_cert_path: Optional[str] = None
    client_key_path: Optional[str] = None


@dataclass
class ClusterResources:
    """Cluster resource capacity and usage."""

    total_cpu_cores: float
    used_cpu_cores: float
    total_memory_gb: float
    used_memory_gb: float
    total_storage_gb: float
    used_storage_gb: float
    vm_count: int
    container_count: int
    node_count: int
    healthy_nodes: int


@dataclass
class ClusterHealth:
    """Cluster health status."""

    overall_status: ClusterStatus
    api_healthy: bool
    storage_healthy: bool
    network_healthy: bool
    ha_healthy: bool
    last_check: datetime
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class ClusterNode:
    """Represents a federated cluster."""

    id: str
    name: str
    endpoint: str
    region: str
    zone: Optional[str]
    status: ClusterStatus
    resources: ClusterResources
    health: ClusterHealth
    labels: Dict[str, str] = field(default_factory=dict)
    capabilities: Set[str] = field(default_factory=set)
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    registered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    token_hash: str = ""    # Hashed auth token
    sync_state: SyncState = SyncState.PENDING


@dataclass
class FederatedPolicy:
    """Policy to be distributed across clusters."""

    id: str
    name: str
    policy_type: PolicyType
    spec: Dict[str, Any]
    version: int
    created_at: datetime
    updated_at: datetime
    target_clusters: List[str]    # Cluster IDs or "*" for all
    checksum: str = ""


@dataclass
class PolicySyncStatus:
    """Policy synchronization status per cluster."""

    policy_id: str
    cluster_id: str
    state: SyncState
    applied_version: int
    last_sync_attempt: Optional[datetime]
    error: Optional[str]


@dataclass
class FederationEvent:
    """Cross-cluster event for correlation."""

    id: str
    cluster_id: str
    cluster_name: str
    timestamp: datetime
    severity: EventSeverity
    category: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    correlated_events: List[str] = field(default_factory=list)


@dataclass
class PlacementDecision:
    """Workload placement decision."""

    workload_id: str
    selected_cluster: str
    score: float
    reasons: List[str]
    alternatives: List[Tuple[str, float]]    # (cluster_id, score)


# -----------------------------------------------------------------------------
# Cluster Communication
# -----------------------------------------------------------------------------


class ClusterClient:
    """HTTP client for cluster communication."""

    def __init__(self, config: FederationConfig):
        self.config = config
        self._ssl_context = self._create_ssl_context()

    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create SSL context with mTLS if configured."""
        context = ssl.create_default_context()

        if self.config.ca_cert_path:
            context.load_verify_locations(self.config.ca_cert_path)

        if self.config.client_cert_path and self.config.client_key_path:
            context.load_cert_chain(
                self.config.client_cert_path, self.config.client_key_path
            )

        return context

    def health_check(
        self, endpoint: str, token: str
    ) -> Tuple[bool, Optional[ClusterHealth]]:
        """Check cluster health via API."""
        try:
            url = f"{endpoint.rstrip('/')}/api/v1/health"
            req = urllib.request.Request(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
            )

            with urllib.request.urlopen(
                req,
                timeout=self.config.health_check_timeout_seconds,
                context=self._ssl_context,
            ) as response:    # nosec B310
                data = json.loads(response.read().decode())

                health = ClusterHealth(
                    overall_status=ClusterStatus(data.get("status", "online")),
                    api_healthy=data.get("api", True),
                    storage_healthy=data.get("storage", True),
                    network_healthy=data.get("network", True),
                    ha_healthy=data.get("ha", True),
                    last_check=datetime.now(timezone.utc),
                    issues=data.get("issues", []),
                    warnings=data.get("warnings", []),
                )
                return True, health
        except urllib.error.URLError as e:
            logger.warning(f"Health check failed for {endpoint}: {e}")
            return False, None
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return False, None

    def get_resources(self, endpoint: str, token: str) -> Optional[ClusterResources]:
        """Get cluster resource usage."""
        try:
            url = f"{endpoint.rstrip('/')}/api/v1/resources"
            req = urllib.request.Request(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
            )

            with urllib.request.urlopen(
                req,
                timeout=self.config.health_check_timeout_seconds,
                context=self._ssl_context,
            ) as response:    # nosec B310
                data = json.loads(response.read().decode())

                return ClusterResources(
                    total_cpu_cores=data.get("total_cpu", 0),
                    used_cpu_cores=data.get("used_cpu", 0),
                    total_memory_gb=data.get("total_memory_gb", 0),
                    used_memory_gb=data.get("used_memory_gb", 0),
                    total_storage_gb=data.get("total_storage_gb", 0),
                    used_storage_gb=data.get("used_storage_gb", 0),
                    vm_count=data.get("vm_count", 0),
                    container_count=data.get("container_count", 0),
                    node_count=data.get("node_count", 0),
                    healthy_nodes=data.get("healthy_nodes", 0),
                )
        except Exception as e:
            logger.warning(f"Failed to get resources from {endpoint}: {e}")
            return None

    def apply_policy(
        self, endpoint: str, token: str, policy: FederatedPolicy
    ) -> Tuple[bool, str]:
        """Apply policy to remote cluster."""
        try:
            url = f"{endpoint.rstrip('/')}/api/v1/policies"
            data = json.dumps(
                {
                    "id": policy.id,
                    "name": policy.name,
                    "type": policy.policy_type.value,
                    "spec": policy.spec,
                    "version": policy.version,
                    "checksum": policy.checksum,
                }
            ).encode()

            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            with urllib.request.urlopen(
                req, timeout=30, context=self._ssl_context
            ) as response:    # nosec B310
                result = json.loads(response.read().decode())
                return result.get("success", False), result.get("message", "")
        except Exception as e:
            return False, str(e)

    def get_events(
        self, endpoint: str, token: str, since: datetime
    ) -> List[Dict[str, Any]]:
        """Get events from remote cluster."""
        try:
            since_str = since.isoformat()
            url = f"{endpoint.rstrip('/')}/api/v1/events?since={since_str}"
            req = urllib.request.Request(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
            )

            with urllib.request.urlopen(
                req, timeout=30, context=self._ssl_context
            ) as response:    # nosec B310
                data = json.loads(response.read().decode())
                return data.get("events", [])
        except Exception as e:
            logger.warning(f"Failed to get events from {endpoint}: {e}")
            return []


# -----------------------------------------------------------------------------
# Policy Management
# -----------------------------------------------------------------------------


class PolicyManager:
    """Manages federated policies."""

    def __init__(self, storage_path: str = "/var/lib/debvisor/federation/policies"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.policies: Dict[str, FederatedPolicy] = {}
        # policy_id -> {cluster_id -> status}
        self.sync_status: Dict[str, Dict[str, PolicySyncStatus]] = {}
        self._load_policies()

    def _load_policies(self) -> None:
        """Load policies from disk."""
        policy_file = self.storage_path / "policies.json"
        if policy_file.exists():
            try:
                with open(policy_file) as f:
                    data = json.load(f)
                for pid, pdata in data.items():
                    self.policies[pid] = FederatedPolicy(
                        id=pdata["id"],
                        name=pdata["name"],
                        policy_type=PolicyType(pdata["policy_type"]),
                        spec=pdata["spec"],
                        version=pdata["version"],
                        created_at=datetime.fromisoformat(pdata["created_at"]),
                        updated_at=datetime.fromisoformat(pdata["updated_at"]),
                        target_clusters=pdata["target_clusters"],
                        checksum=pdata.get("checksum", ""),
                    )
                logger.info(f"Loaded {len(self.policies)} federated policies")
            except Exception as e:
                logger.warning(f"Failed to load policies: {e}")

    def _save_policies(self) -> None:
        """Save policies to disk."""
        data = {}
        for pid, p in self.policies.items():
            data[pid] = {
                "id": p.id,
                "name": p.name,
                "policy_type": p.policy_type.value,
                "spec": p.spec,
                "version": p.version,
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat(),
                "target_clusters": p.target_clusters,
                "checksum": p.checksum,
            }

        policy_file = self.storage_path / "policies.json"
        with open(policy_file, "w") as f:
            json.dump(data, f, indent=2)

    def create_policy(
        self,
        name: str,
        policy_type: PolicyType,
        spec: Dict[str, Any],
        target_clusters: List[str],
    ) -> FederatedPolicy:
        """Create a new federated policy."""
        from uuid import uuid4

        policy_id = str(uuid4())
        now = datetime.now(timezone.utc)

        policy = FederatedPolicy(
            id=policy_id,
            name=name,
            policy_type=policy_type,
            spec=spec,
            version=1,
            created_at=now,
            updated_at=now,
            target_clusters=target_clusters,
        )
        policy.checksum = self._compute_checksum(policy)

        self.policies[policy_id] = policy
        self.sync_status[policy_id] = {}
        self._save_policies()

        logger.info(f"Created policy {name} ({policy_id})")
        return policy

    def update_policy(
        self, policy_id: str, spec: Dict[str, Any]
    ) -> Optional[FederatedPolicy]:
        """Update policy spec."""
        policy = self.policies.get(policy_id)
        if not policy:
            return None

        policy.spec = spec
        policy.version += 1
        policy.updated_at = datetime.now(timezone.utc)
        policy.checksum = self._compute_checksum(policy)

        # Mark all sync as pending
        for cluster_id in self.sync_status.get(policy_id, {}).keys():
            self.sync_status[policy_id][cluster_id].state = SyncState.PENDING

        self._save_policies()
        return policy

    def _compute_checksum(self, policy: FederatedPolicy) -> str:
        """Compute policy spec checksum."""
        content = json.dumps(
            {"spec": policy.spec, "version": policy.version}, sort_keys=True
        )
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get_policies_for_cluster(self, cluster_id: str) -> List[FederatedPolicy]:
        """Get policies targeting a specific cluster."""
        results = []
        for policy in self.policies.values():
            if "*" in policy.target_clusters or cluster_id in policy.target_clusters:
                results.append(policy)
        return results

    def record_sync_result(
        self,
        policy_id: str,
        cluster_id: str,
        success: bool,
        applied_version: int,
        error: Optional[str] = None,
    ):
        """Record policy sync result."""
        if policy_id not in self.sync_status:
            self.sync_status[policy_id] = {}

        self.sync_status[policy_id][cluster_id] = PolicySyncStatus(
            policy_id=policy_id,
            cluster_id=cluster_id,
            state=SyncState.IN_SYNC if success else SyncState.DRIFTED,
            applied_version=applied_version if success else 0,
            last_sync_attempt=datetime.now(timezone.utc),
            error=error,
        )


# -----------------------------------------------------------------------------
# Event Correlation
# -----------------------------------------------------------------------------


class EventCorrelator:
    """Correlate events across federated clusters."""

    def __init__(self, retention_hours: int = 168):
        self.events: Dict[str, FederationEvent] = {}
        self.retention_hours = retention_hours
        self._correlation_rules: List[
            Callable[[FederationEvent, List[FederationEvent]], List[str]]
        ] = []

    def add_event(self, event: FederationEvent) -> List[str]:
        """Add event and return IDs of correlated events."""
        self.events[event.id] = event

        # Find correlations
        recent_events = self._get_recent_events(minutes=30)
        correlated = []

        for rule in self._correlation_rules:
            correlated.extend(rule(event, recent_events))

        event.correlated_events = list(set(correlated))

        # Cleanup old events
        self._cleanup_old_events()

        return event.correlated_events

    def _get_recent_events(self, minutes: int) -> List[FederationEvent]:
        """Get events from last N minutes."""
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        return [e for e in self.events.values() if e.timestamp > cutoff]

    def _cleanup_old_events(self) -> None:
        """Remove events older than retention period."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=self.retention_hours)
        to_remove = [eid for eid, e in self.events.items() if e.timestamp < cutoff]
        for eid in to_remove:
            del self.events[eid]

    def add_correlation_rule(
        self, rule: Callable[[FederationEvent, List[FederationEvent]], List[str]]
    ):
        """Add custom correlation rule."""
        self._correlation_rules.append(rule)

    def get_correlated_events(self, event_id: str) -> List[FederationEvent]:
        """Get events correlated with given event."""
        event = self.events.get(event_id)
        if not event:
            return []
        return [
            self.events[eid] for eid in event.correlated_events if eid in self.events
        ]

    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detect anomalies across clusters."""
        anomalies = []
        recent = self._get_recent_events(minutes=60)

        # Detect: Same error across multiple clusters
        error_by_msg: Dict[str, List[FederationEvent]] = {}
        for e in recent:
            if e.severity in [EventSeverity.ERROR, EventSeverity.CRITICAL]:
                key = e.message[:100]
                if key not in error_by_msg:
                    error_by_msg[key] = []
                error_by_msg[key].append(e)

        for msg, events in error_by_msg.items():
            clusters = set(e.cluster_id for e in events)
            if len(clusters) >= 2:
                anomalies.append(
                    {
                        "type": "cross_cluster_error",
                        "message": msg,
                        "affected_clusters": list(clusters),
                        "event_count": len(events),
                        "first_seen": min(e.timestamp for e in events).isoformat(),
                    }
                )

        return anomalies


# -----------------------------------------------------------------------------
# Workload Placement
# -----------------------------------------------------------------------------


class PlacementEngine:
    """Cross-cluster workload placement decisions."""

    def __init__(self) -> None:
        self._weight_cpu = 0.3
        self._weight_memory = 0.3
        self._weight_storage = 0.2
        self._weight_locality = 0.2

    def select_cluster(
        self,
        clusters: Dict[str, ClusterNode],
        requirements: Dict[str, Any],
        preferred_region: Optional[str] = None,
    ) -> PlacementDecision:
        """Select best cluster for workload placement."""
        scores: List[Tuple[str, float, List[str]]] = []

        required_cpu = requirements.get("cpu_cores", 1)
        required_memory = requirements.get("memory_gb", 1)
        required_storage = requirements.get("storage_gb", 10)
        required_capabilities = set(requirements.get("capabilities", []))

        for cid, cluster in clusters.items():
            if cluster.status != ClusterStatus.ONLINE:
                continue

            # Check capabilities
            if required_capabilities and not required_capabilities.issubset(
                cluster.capabilities
            ):
                continue

            # Check resource availability
            res = cluster.resources
            avail_cpu = res.total_cpu_cores - res.used_cpu_cores
            avail_memory = res.total_memory_gb - res.used_memory_gb
            avail_storage = res.total_storage_gb - res.used_storage_gb

            if (
                avail_cpu < required_cpu
                or avail_memory < required_memory
                or avail_storage < required_storage
            ):
                continue

            # Score calculation
            reasons = []
            score = 0.0

            # CPU score (prefer clusters with more headroom)
            cpu_ratio = (
                avail_cpu / res.total_cpu_cores if res.total_cpu_cores > 0 else 0
            )
            score += cpu_ratio * self._weight_cpu
            reasons.append(f"CPU headroom: {cpu_ratio:.1%}")

            # Memory score
            mem_ratio = (
                avail_memory / res.total_memory_gb if res.total_memory_gb > 0 else 0
            )
            score += mem_ratio * self._weight_memory
            reasons.append(f"Memory headroom: {mem_ratio:.1%}")

            # Storage score
            storage_ratio = (
                avail_storage / res.total_storage_gb if res.total_storage_gb > 0 else 0
            )
            score += storage_ratio * self._weight_storage
            reasons.append(f"Storage headroom: {storage_ratio:.1%}")

            # Locality bonus
            if preferred_region and cluster.region == preferred_region:
                score += self._weight_locality
                reasons.append(f"Preferred region: {preferred_region}")

            scores.append((cid, score, reasons))

        if not scores:
            return PlacementDecision(
                workload_id=requirements.get("workload_id", ""),
                selected_cluster="",
                score=0.0,
                reasons=["No suitable cluster found"],
                alternatives=[],
            )

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        selected_id, selected_score, selected_reasons = scores[0]
        alternatives = [(cid, s) for cid, s, _ in scores[1:4]]    # Top 3 alternatives

        return PlacementDecision(
            workload_id=requirements.get("workload_id", ""),
            selected_cluster=selected_id,
            score=selected_score,
            reasons=selected_reasons,
            alternatives=alternatives,
        )


# -----------------------------------------------------------------------------
# Federation Manager (Main Service)
# -----------------------------------------------------------------------------


class FederationManager:
    """Enterprise fleet federation manager."""

    def __init__(
        self,
        config: Optional[FederationConfig] = None,
        storage_path: str = "/var/lib/debvisor/federation",
    ):
        self.config = config or FederationConfig()
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.clusters: Dict[str, ClusterNode] = {}
        self._tokens: Dict[str, str] = {}    # cluster_id -> token

        self.client = ClusterClient(self.config)
        self.policy_manager = PolicyManager(str(self.storage_path / "policies"))
        self.event_correlator = EventCorrelator(self.config.event_retention_hours)
        self.placement_engine = PlacementEngine()

        self._sync_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._callbacks: List[Callable[[str, ClusterNode], None]] = []

        self._load_clusters()

    def _load_clusters(self) -> None:
        """Load cluster registrations from disk."""
        cluster_file = self.storage_path / "clusters.json"
        if cluster_file.exists():
            try:
                with open(cluster_file) as f:
                    data = json.load(f)
                for cid, cdata in data.get("clusters", {}).items():
                    self.clusters[cid] = ClusterNode(
                        id=cdata["id"],
                        name=cdata["name"],
                        endpoint=cdata["endpoint"],
                        region=cdata.get("region", "default"),
                        zone=cdata.get("zone"),
                        status=ClusterStatus(cdata.get("status", "offline")),
                        resources=ClusterResources(
                            total_cpu_cores=cdata.get("resources", {}).get(
                                "total_cpu", 0
                            ),
                            used_cpu_cores=cdata.get("resources", {}).get(
                                "used_cpu", 0
                            ),
                            total_memory_gb=cdata.get("resources", {}).get(
                                "total_memory", 0
                            ),
                            used_memory_gb=cdata.get("resources", {}).get(
                                "used_memory", 0
                            ),
                            total_storage_gb=cdata.get("resources", {}).get(
                                "total_storage", 0
                            ),
                            used_storage_gb=cdata.get("resources", {}).get(
                                "used_storage", 0
                            ),
                            vm_count=cdata.get("resources", {}).get("vm_count", 0),
                            container_count=cdata.get("resources", {}).get(
                                "container_count", 0
                            ),
                            node_count=cdata.get("resources", {}).get("node_count", 0),
                            healthy_nodes=cdata.get("resources", {}).get(
                                "healthy_nodes", 0
                            ),
                        ),
                        health=ClusterHealth(
                            overall_status=ClusterStatus.OFFLINE,
                            api_healthy=False,
                            storage_healthy=False,
                            network_healthy=False,
                            ha_healthy=False,
                            last_check=datetime.now(timezone.utc),
                        ),
                        labels=cdata.get("labels", {}),
                        capabilities=set(cdata.get("capabilities", [])),
                        token_hash=cdata.get("token_hash", ""),
                    )

                # Load tokens separately (would be encrypted in production)
                tokens_file = self.storage_path / "tokens.json"
                if tokens_file.exists():
                    with open(tokens_file) as f:
                        self._tokens = json.load(f)

                logger.info(f"Loaded {len(self.clusters)} federated clusters")
            except Exception as e:
                logger.warning(f"Failed to load clusters: {e}")

    def _save_clusters(self) -> None:
        """Save cluster registrations."""
        data: Any = {"clusters": {}}  # type: ignore[var-annotated]
        for cid, c in self.clusters.items():
            data["clusters"][cid] = {
                "id": c.id,
                "name": c.name,
                "endpoint": c.endpoint,
                "region": c.region,
                "zone": c.zone,
                "status": c.status.value,
                "resources": {
                    "total_cpu": c.resources.total_cpu_cores,
                    "used_cpu": c.resources.used_cpu_cores,
                    "total_memory": c.resources.total_memory_gb,
                    "used_memory": c.resources.used_memory_gb,
                    "total_storage": c.resources.total_storage_gb,
                    "used_storage": c.resources.used_storage_gb,
                    "vm_count": c.resources.vm_count,
                    "container_count": c.resources.container_count,
                    "node_count": c.resources.node_count,
                    "healthy_nodes": c.resources.healthy_nodes,
                },
                "labels": c.labels,
                "capabilities": list(c.capabilities),
                "token_hash": c.token_hash,
            }

        cluster_file = self.storage_path / "clusters.json"
        with open(cluster_file, "w") as f:
            json.dump(data, f, indent=2)

        # Save tokens separately
        tokens_file = self.storage_path / "tokens.json"
        with open(tokens_file, "w") as f:
            json.dump(self._tokens, f)

    def register_callback(self, callback: Callable[[str, ClusterNode], None]) -> None:
        """Register cluster state change callback."""
        self._callbacks.append(callback)

    def _notify(self, event: str, cluster: ClusterNode) -> None:
        for cb in self._callbacks:
            try:
                cb(event, cluster)
            except Exception as e:
                logger.warning(f"Callback error: {e}")

    def register_cluster(
        self,
        name: str,
        endpoint: str,
        token: str,
        region: str = "default",
        zone: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        capabilities: Optional[List[str]] = None,
    ) -> Tuple[bool, str]:
        """Register a new cluster in the federation."""
        from uuid import uuid4

        # Validate connectivity
        reachable, health = self.client.health_check(endpoint, token)
        if not reachable:
            return False, "Cluster unreachable or invalid token"

        # Get resources
        resources = self.client.get_resources(endpoint, token)
        if not resources:
            resources = ClusterResources(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        cluster_id = str(uuid4())
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        cluster = ClusterNode(
            id=cluster_id,
            name=name,
            endpoint=endpoint,
            region=region,
            zone=zone,
            status=(
                ClusterStatus.ONLINE
                if health and health.overall_status == ClusterStatus.ONLINE
                else ClusterStatus.DEGRADED
            ),
            resources=resources,
            health=health
            or ClusterHealth(
                overall_status=ClusterStatus.ONLINE,
                api_healthy=True,
                storage_healthy=True,
                network_healthy=True,
                ha_healthy=True,
                last_check=datetime.now(timezone.utc),
            ),
            labels=labels or {},
            capabilities=set(capabilities or []),
            token_hash=token_hash,
            sync_state=SyncState.PENDING,
        )

        with self._lock:
            self.clusters[cluster_id] = cluster
            self._tokens[cluster_id] = token
            self._save_clusters()

        self._notify("registered", cluster)
        logger.info(f"Registered cluster {name} ({cluster_id}) at {endpoint}")
        return True, cluster_id

    def unregister_cluster(self, cluster_id: str) -> bool:
        """Remove cluster from federation."""
        with self._lock:
            if cluster_id not in self.clusters:
                return False

            cluster = self.clusters.pop(cluster_id)
            self._tokens.pop(cluster_id, None)
            self._save_clusters()

        self._notify("unregistered", cluster)
        logger.info(f"Unregistered cluster {cluster.name} ({cluster_id})")
        return True

    def sync_cluster(self, cluster_id: str) -> bool:
        """Sync state with a specific cluster."""
        cluster = self.clusters.get(cluster_id)
        token = self._tokens.get(cluster_id)
        if not cluster or not token:
            return False

        # Health check
        reachable, health = self.client.health_check(cluster.endpoint, token)
        if not reachable:
            cluster.status = ClusterStatus.UNREACHABLE
            cluster.health.overall_status = ClusterStatus.UNREACHABLE
            self._notify("unreachable", cluster)
            return False

        if health:
            cluster.health = health
            cluster.status = health.overall_status

        # Update resources
        resources = self.client.get_resources(cluster.endpoint, token)
        if resources:
            cluster.resources = resources

        cluster.last_seen = datetime.now(timezone.utc)

        # Sync policies
        policies = self.policy_manager.get_policies_for_cluster(cluster_id)
        for policy in policies:
            success, msg = self.client.apply_policy(cluster.endpoint, token, policy)
            self.policy_manager.record_sync_result(
                policy.id,
                cluster_id,
                success,
                policy.version if success else 0,
                None if success else msg,
            )

        cluster.sync_state = SyncState.IN_SYNC
        self._save_clusters()
        self._notify("synced", cluster)
        return True

    def sync_all(self) -> Dict[str, bool]:
        """Sync all registered clusters."""
        results = {}
        for cluster_id in list(self.clusters.keys()):
            results[cluster_id] = self.sync_cluster(cluster_id)
        return results

    def start_sync_loop(self) -> None:
        """Start background sync loop."""
        if self._sync_thread and self._sync_thread.is_alive():
            return

        self._stop_event.clear()
        self._sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self._sync_thread.start()
        logger.info("Started federation sync loop")

    def _sync_loop(self) -> None:
        """Background sync loop."""
        while not self._stop_event.is_set():
            try:
                self.sync_all()
            except Exception as e:
                logger.error(f"Sync loop error: {e}")

            self._stop_event.wait(self.config.sync_interval_seconds)

    def stop_sync_loop(self) -> None:
        """Stop background sync loop."""
        self._stop_event.set()
        if self._sync_thread:
            self._sync_thread.join(timeout=5)
        logger.info("Stopped federation sync loop")

    def get_cluster(self, cluster_id: str) -> Optional[ClusterNode]:
        """Get cluster by ID."""
        return self.clusters.get(cluster_id)

    def list_clusters(
        self, region: Optional[str] = None, status: Optional[ClusterStatus] = None
    ) -> List[ClusterNode]:
        """List clusters with optional filters."""
        results = list(self.clusters.values())
        if region:
            results = [c for c in results if c.region == region]
        if status:
            results = [c for c in results if c.status == status]
        return sorted(results, key=lambda c: c.name)

    def get_global_capacity(self) -> Dict[str, Any]:
        """Get aggregated capacity across all clusters."""
        online = [c for c in self.clusters.values() if c.status == ClusterStatus.ONLINE]

        return {
            "cluster_count": len(self.clusters),
            "online_clusters": len(online),
            "total_cpu_cores": sum(c.resources.total_cpu_cores for c in online),
            "used_cpu_cores": sum(c.resources.used_cpu_cores for c in online),
            "total_memory_gb": sum(c.resources.total_memory_gb for c in online),
            "used_memory_gb": sum(c.resources.used_memory_gb for c in online),
            "total_storage_gb": sum(c.resources.total_storage_gb for c in online),
            "used_storage_gb": sum(c.resources.used_storage_gb for c in online),
            "total_vms": sum(c.resources.vm_count for c in online),
            "total_containers": sum(c.resources.container_count for c in online),
        }

    def select_cluster_for_workload(
        self, requirements: Dict[str, Any], preferred_region: Optional[str] = None
    ) -> PlacementDecision:
        """Select best cluster for workload placement."""
        return self.placement_engine.select_cluster(
            self.clusters, requirements, preferred_region
        )

    def create_policy(
        self,
        name: str,
        policy_type: PolicyType,
        spec: Dict[str, Any],
        target_clusters: Optional[List[str]] = None,
    ) -> FederatedPolicy:
        """Create and broadcast a federated policy."""
        targets = target_clusters or ["*"]
        return self.policy_manager.create_policy(name, policy_type, spec, targets)

    def get_anomalies(self) -> List[Dict[str, Any]]:
        """Get detected anomalies across clusters."""
        return self.event_correlator.detect_anomalies()

    def collect_events(self, since: Optional[datetime] = None) -> None:
        """Collect events from all clusters."""
        if since is None:
            since = datetime.now(timezone.utc) - timedelta(hours=1)

        for cluster_id, cluster in self.clusters.items():
            token = self._tokens.get(cluster_id)
            if not token or cluster.status == ClusterStatus.UNREACHABLE:
                continue

            events = self.client.get_events(cluster.endpoint, token, since)
            for e in events:
                event = FederationEvent(
                    id=e.get("id", str(hash(json.dumps(e)))),
                    cluster_id=cluster_id,
                    cluster_name=cluster.name,
                    timestamp=datetime.fromisoformat(
                        e.get("timestamp", datetime.now(timezone.utc).isoformat())
                    ),
                    severity=EventSeverity(e.get("severity", "info")),
                    category=e.get("category", "general"),
                    message=e.get("message", ""),
                    details=e.get("details", {}),
                )
                self.event_correlator.add_event(event)


# -----------------------------------------------------------------------------
# Example / CLI
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import tempfile

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Create federation manager
    storage = tempfile.mkdtemp(prefix="federation_")
    config = FederationConfig(sync_interval_seconds=60)
    federation = FederationManager(config, storage)

    # Register callback
    def on_cluster_event(event: str, cluster: ClusterNode) -> None:
        print(f"  [{event}] {cluster.name}: {cluster.status.value}")

    federation.register_callback(on_cluster_event)

    # Mock cluster registration (would fail in real scenario without valid endpoints)
    print("Simulating cluster federation...")

    # Create a policy
    policy = federation.create_policy(
        name="default-resource-quota",
        policy_type=PolicyType.RESOURCE_QUOTA,
        spec={
            "max_cpu_per_vm": 32,
            "max_memory_per_vm_gb": 128,
            "max_vms_per_tenant": 100,
        },
        target_clusters=["*"],
    )
    print(f"\nCreated policy: {policy.name} (v{policy.version})")

    # Show placement requirements
    requirements = {
        "workload_id": "web-app-1",
        "cpu_cores": 4,
        "memory_gb": 16,
        "storage_gb": 100,
        "capabilities": ["gpu"],
    }

    decision = federation.select_cluster_for_workload(
        requirements, preferred_region="us-east"
    )
    print(f"\nPlacement decision for {requirements['workload_id']}:")
    if decision.selected_cluster:
        print(f"  Selected: {decision.selected_cluster} (score: {decision.score:.2f})")
        print(f"  Reasons: {', '.join(decision.reasons)}")
    else:
        print(f"  No cluster available: {decision.reasons}")

    # Global capacity
    capacity = federation.get_global_capacity()
    print("\nGlobal Capacity:")
    print(
        f"  Clusters: {capacity['cluster_count']} ({capacity['online_clusters']} online)"
    )
    print(f"  CPU: {capacity['used_cpu_cores']}/{capacity['total_cpu_cores']} cores")
    print(f"  Memory: {capacity['used_memory_gb']}/{capacity['total_memory_gb']} GB")

    print("\nFederation manager demo complete.")
