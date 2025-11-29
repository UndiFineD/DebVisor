"""
Multi-Cluster Foundation for DebVisor

Provides:
- Cluster registry and discovery
- Cross-cluster service communication
- Unified cluster management interface
- Cross-cluster resource operations
- Cluster state synchronization
- Federation support
- Load balancing across clusters

Enables:
- Horizontal scaling across multiple clusters
- High availability with cluster failover
- Distributed workload management
- Cross-cluster service discovery
- Centralized monitoring and control
"""

import logging
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any, Callable, Set
from enum import Enum
import uuid
import asyncio
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ClusterStatus(Enum):
    """Cluster operational status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


class ResourceType(Enum):
    """Types of resources that can be managed across clusters."""
    NODE = "node"
    JOB = "job"
    SERVICE = "service"
    VOLUME = "volume"
    NETWORK = "network"


class ReplicationStrategy(Enum):
    """Data replication strategy."""
    NONE = "none"
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    MULTI_MASTER = "multi_master"


@dataclass
class ClusterMetrics:
    """Cluster performance metrics."""
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    node_count: int
    active_jobs: int
    active_services: int
    network_latency_ms: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def is_healthy(self) -> bool:
        """Check if cluster metrics are within healthy bounds."""
        return (
            self.cpu_usage_percent < 85 and
            self.memory_usage_percent < 80 and
            self.disk_usage_percent < 85
        )


@dataclass
class ClusterNode:
    """Represents a cluster."""
    cluster_id: str
    name: str
    endpoint: str  # API endpoint
    region: str
    version: str
    status: ClusterStatus = ClusterStatus.UNKNOWN
    last_heartbeat: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metrics: Optional[ClusterMetrics] = None
    replicas: Set[str] = field(default_factory=set)  # Replica cluster IDs
    capabilities: List[str] = field(default_factory=list)
    
    def is_responsive(self, timeout_seconds: int = 30) -> bool:
        """Check if cluster is responsive."""
        age = (datetime.now(timezone.utc) - self.last_heartbeat).total_seconds()
        return age < timeout_seconds


@dataclass
class CrossClusterService:
    """Service running across multiple clusters."""
    service_id: str
    name: str
    type: str
    clusters: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # cluster_id -> config
    replication_strategy: ReplicationStrategy = ReplicationStrategy.ASYNCHRONOUS
    failover_enabled: bool = True
    load_balancing_policy: str = "round_robin"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class SyncState:
    """State synchronization entry."""
    resource_id: str
    resource_type: ResourceType
    source_cluster: str
    target_clusters: List[str]
    state_hash: str
    timestamp: datetime
    sync_status: str = "pending"  # pending, in_progress, completed, failed
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class FederationPolicy:
    """Federation policy for clusters."""
    name: str
    description: str
    clusters: List[str]
    replication_strategy: ReplicationStrategy
    failover_enabled: bool
    auto_scaling_enabled: bool
    min_cluster_count: int = 1
    max_cluster_count: int = 10
    sync_interval_seconds: int = 60


class ClusterRegistry:
    """Central registry for managing cluster nodes."""
    
    def __init__(self):
        """Initialize cluster registry."""
        self.clusters: Dict[str, ClusterNode] = {}
        self.services: Dict[str, CrossClusterService] = {}
        self.policies: Dict[str, FederationPolicy] = {}
        self.sync_queue: List[SyncState] = []

    def register_cluster(self, cluster: ClusterNode) -> bool:
        """
        Register a new cluster.
        
        Args:
            cluster: ClusterNode to register
            
        Returns:
            True if successful
        """
        if cluster.cluster_id in self.clusters:
            logger.warning(f"Cluster {cluster.cluster_id} already registered")
            return False
        
        self.clusters[cluster.cluster_id] = cluster
        logger.info(f"Cluster registered: {cluster.name} ({cluster.cluster_id})")
        return True

    def deregister_cluster(self, cluster_id: str) -> bool:
        """
        Deregister a cluster.
        
        Args:
            cluster_id: Cluster to remove
            
        Returns:
            True if successful
        """
        if cluster_id not in self.clusters:
            logger.warning(f"Cluster {cluster_id} not found")
            return False
        
        cluster = self.clusters.pop(cluster_id)
        logger.info(f"Cluster deregistered: {cluster.name}")
        return True

    def get_cluster(self, cluster_id: str) -> Optional[ClusterNode]:
        """Get cluster by ID."""
        return self.clusters.get(cluster_id)

    def list_clusters(self, region: Optional[str] = None) -> List[ClusterNode]:
        """
        List all clusters, optionally filtered by region.
        
        Args:
            region: Optional region filter
            
        Returns:
            List of clusters
        """
        clusters = list(self.clusters.values())
        if region:
            clusters = [c for c in clusters if c.region == region]
        return clusters

    def update_cluster_status(self, cluster_id: str, status: ClusterStatus, 
                             metrics: Optional[ClusterMetrics] = None) -> bool:
        """
        Update cluster status and metrics.
        
        Args:
            cluster_id: Cluster to update
            status: New status
            metrics: Optional metrics
            
        Returns:
            True if successful
        """
        cluster = self.get_cluster(cluster_id)
        if not cluster:
            return False
        
        cluster.status = status
        cluster.last_heartbeat = datetime.now(timezone.utc)
        if metrics:
            cluster.metrics = metrics
        
        logger.debug(f"Updated cluster {cluster_id}: {status.value}")
        return True

    def get_healthy_clusters(self, region: Optional[str] = None) -> List[ClusterNode]:
        """
        Get healthy clusters, optionally filtered by region.
        
        Args:
            region: Optional region filter
            
        Returns:
            List of healthy clusters
        """
        clusters = self.list_clusters(region)
        return [
            c for c in clusters 
            if c.is_responsive() and c.status in [ClusterStatus.HEALTHY, ClusterStatus.DEGRADED]
        ]

    def get_cluster_distance(self, cluster_id_1: str, cluster_id_2: str) -> Optional[float]:
        """
        Get distance between two clusters (based on latency).
        
        Args:
            cluster_id_1: First cluster
            cluster_id_2: Second cluster
            
        Returns:
            Distance in milliseconds or None
        """
        c1 = self.get_cluster(cluster_id_1)
        c2 = self.get_cluster(cluster_id_2)
        
        if not c1 or not c2 or not c1.metrics or not c2.metrics:
            return None
        
        # Simplified distance metric based on region and latency
        if c1.region == c2.region:
            return c1.metrics.network_latency_ms
        else:
            return c1.metrics.network_latency_ms * 2  # Inter-region penalty


class ServiceDiscovery:
    """Cross-cluster service discovery."""
    
    def __init__(self, registry: ClusterRegistry):
        """
        Initialize service discovery.
        
        Args:
            registry: ClusterRegistry instance
        """
        self.registry = registry
        self.dns_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = 300  # 5 minutes

    def register_service(self, service: CrossClusterService) -> bool:
        """
        Register a cross-cluster service.
        
        Args:
            service: CrossClusterService to register
            
        Returns:
            True if successful
        """
        self.registry.services[service.service_id] = service
        logger.info(f"Service registered: {service.name} ({service.service_id})")
        return True

    def discover_service(self, service_name: str, region: Optional[str] = None) -> Optional[CrossClusterService]:
        """
        Discover a service by name.
        
        Args:
            service_name: Name of service to discover
            region: Optional region filter
            
        Returns:
            CrossClusterService or None
        """
        for service in self.registry.services.values():
            if service.name == service_name:
                # Filter by region if specified
                if region:
                    clusters_in_region = [
                        c for c_id, c in service.clusters.items()
                        if self.registry.get_cluster(c_id) and 
                        self.registry.get_cluster(c_id).region == region
                    ]
                    if not clusters_in_region:
                        continue
                
                return service
        
        return None

    def get_service_endpoints(self, service_id: str, region: Optional[str] = None) -> List[str]:
        """
        Get all service endpoints for a given service.
        
        Args:
            service_id: Service ID
            region: Optional region filter
            
        Returns:
            List of endpoint URLs
        """
        service = self.registry.services.get(service_id)
        if not service:
            return []
        
        endpoints = []
        for cluster_id in service.clusters.keys():
            cluster = self.registry.get_cluster(cluster_id)
            if cluster and cluster.is_responsive():
                if not region or cluster.region == region:
                    endpoints.append(cluster.endpoint)
        
        return endpoints


class StateSynchronizer:
    """Synchronizes state across clusters."""
    
    def __init__(self, registry: ClusterRegistry):
        """
        Initialize state synchronizer.
        
        Args:
            registry: ClusterRegistry instance
        """
        self.registry = registry
        self.sync_callbacks: Dict[ResourceType, List[Callable]] = {
            rt: [] for rt in ResourceType
        }

    def queue_sync(self, resource_id: str, resource_type: ResourceType,
                   source_cluster: str, target_clusters: List[str]) -> SyncState:
        """
        Queue a resource for synchronization.
        
        Args:
            resource_id: Resource to sync
            resource_type: Type of resource
            source_cluster: Source cluster
            target_clusters: Target clusters for replication
            
        Returns:
            SyncState entry
        """
        sync_state = SyncState(
            resource_id=resource_id,
            resource_type=resource_type,
            source_cluster=source_cluster,
            target_clusters=target_clusters,
            state_hash="",
            timestamp=datetime.now(timezone.utc),
        )
        
        self.registry.sync_queue.append(sync_state)
        logger.info(f"Queued sync: {resource_type.value}/{resource_id} -> {target_clusters}")
        
        return sync_state

    def register_sync_callback(self, resource_type: ResourceType, 
                               callback: Callable) -> None:
        """
        Register callback for resource synchronization.
        
        Args:
            resource_type: Type of resource
            callback: Callback function
        """
        self.sync_callbacks[resource_type].append(callback)

    async def process_sync_queue(self) -> Dict[str, Any]:
        """
        Process pending synchronizations.
        
        Returns:
            Sync summary
        """
        summary = {
            'total': len(self.registry.sync_queue),
            'completed': 0,
            'failed': 0,
            'pending': 0,
        }
        
        for sync_state in self.registry.sync_queue:
            if sync_state.sync_status == 'completed':
                continue
            
            try:
                # Execute sync callbacks
                callbacks = self.sync_callbacks.get(sync_state.resource_type, [])
                for callback in callbacks:
                    await callback(sync_state)
                
                sync_state.sync_status = 'completed'
                summary['completed'] += 1
                
            except Exception as e:
                logger.error(f"Sync failed: {sync_state.resource_id}: {e}")
                sync_state.retry_count += 1
                
                if sync_state.retry_count >= sync_state.max_retries:
                    sync_state.sync_status = 'failed'
                    summary['failed'] += 1
                else:
                    sync_state.sync_status = 'pending'
                    summary['pending'] += 1
        
        return summary


class LoadBalancer:
    """Cross-cluster load balancing."""
    
    def __init__(self, registry: ClusterRegistry):
        """
        Initialize load balancer.
        
        Args:
            registry: ClusterRegistry instance
        """
        self.registry = registry

    def get_next_cluster(self, policy: str = "round_robin", 
                         region: Optional[str] = None) -> Optional[ClusterNode]:
        """
        Get next cluster for work distribution.
        
        Args:
            policy: Load balancing policy
            region: Optional region constraint
            
        Returns:
            ClusterNode or None
        """
        healthy_clusters = self.registry.get_healthy_clusters(region)
        if not healthy_clusters:
            return None
        
        if policy == "round_robin":
            return healthy_clusters[0]
        
        elif policy == "least_loaded":
            return min(
                healthy_clusters,
                key=lambda c: c.metrics.cpu_usage_percent if c.metrics else 100
            )
        
        elif policy == "nearest":
            # Find nearest cluster based on latency
            return min(
                healthy_clusters,
                key=lambda c: c.metrics.network_latency_ms if c.metrics else 1000
            )
        
        return healthy_clusters[0]

    def distribute_work(self, work_items: int, region: Optional[str] = None) -> Dict[str, int]:
        """
        Distribute work across clusters.
        
        Args:
            work_items: Number of work items to distribute
            region: Optional region constraint
            
        Returns:
            Mapping of cluster_id -> work_count
        """
        healthy_clusters = self.registry.get_healthy_clusters(region)
        if not healthy_clusters:
            return {}
        
        distribution = {}
        
        # Distribute based on capacity (inverse of CPU usage)
        total_capacity = sum(100 - (c.metrics.cpu_usage_percent if c.metrics else 0) 
                            for c in healthy_clusters)
        
        if total_capacity <= 0:
            # Even distribution if all saturated
            count_per_cluster = work_items // len(healthy_clusters)
            for cluster in healthy_clusters:
                distribution[cluster.cluster_id] = count_per_cluster
        else:
            # Capacity-weighted distribution
            for cluster in healthy_clusters:
                capacity = 100 - (cluster.metrics.cpu_usage_percent if cluster.metrics else 0)
                proportion = capacity / total_capacity
                distribution[cluster.cluster_id] = max(1, int(work_items * proportion))
        
        return distribution


class MultiClusterManager:
    """
    High-level multi-cluster management interface.
    
    Coordinates all multi-cluster operations.
    """
    
    def __init__(self):
        """Initialize multi-cluster manager."""
        self.registry = ClusterRegistry()
        self.discovery = ServiceDiscovery(self.registry)
        self.synchronizer = StateSynchronizer(self.registry)
        self.load_balancer = LoadBalancer(self.registry)
        self.policies: Dict[str, FederationPolicy] = {}

    def add_cluster(self, name: str, endpoint: str, region: str, 
                    version: str) -> str:
        """
        Add a new cluster to the federation.
        
        Args:
            name: Cluster name
            endpoint: API endpoint
            region: Geographic region
            version: Cluster version
            
        Returns:
            Cluster ID
        """
        cluster_id = str(uuid.uuid4())
        cluster = ClusterNode(
            cluster_id=cluster_id,
            name=name,
            endpoint=endpoint,
            region=region,
            version=version,
        )
        
        self.registry.register_cluster(cluster)
        return cluster_id

    def get_federation_status(self) -> Dict[str, Any]:
        """Get overall federation status."""
        clusters = self.registry.list_clusters()
        healthy = self.registry.get_healthy_clusters()
        
        return {
            'total_clusters': len(clusters),
            'healthy_clusters': len(healthy),
            'total_nodes': sum(c.metrics.node_count if c.metrics else 0 for c in clusters),
            'total_jobs': sum(c.metrics.active_jobs if c.metrics else 0 for c in clusters),
            'total_services': len(self.registry.services),
            'clusters': [
                {
                    'id': c.cluster_id,
                    'name': c.name,
                    'region': c.region,
                    'status': c.status.value,
                    'metrics': asdict(c.metrics) if c.metrics else None,
                }
                for c in clusters
            ],
        }

    def create_federation_policy(self, name: str, description: str,
                                clusters: List[str],
                                replication_strategy: ReplicationStrategy = ReplicationStrategy.ASYNCHRONOUS,
                                failover_enabled: bool = True) -> str:
        """
        Create a federation policy.
        
        Args:
            name: Policy name
            description: Policy description
            clusters: List of cluster IDs
            replication_strategy: Replication strategy
            failover_enabled: Enable failover
            
        Returns:
            Policy ID
        """
        policy_id = str(uuid.uuid4())
        policy = FederationPolicy(
            name=name,
            description=description,
            clusters=clusters,
            replication_strategy=replication_strategy,
            failover_enabled=failover_enabled,
        )
        
        self.policies[policy_id] = policy
        logger.info(f"Federation policy created: {name}")
        return policy_id

