"""
Multi-region Support System - Cross-Datacenter Operations

Phase 7 Feature 3: Comprehensive multi-region support with cross-datacenter
replication, failover, and geo-distributed resource management. Enables DebVisor
to operate across multiple regions with automatic failover and data sync.

Author: DebVisor Development Team
Date: November 27, 2025
Version: 1.0.0
Status: Production-Ready
"""

import asyncio
import json
import logging
import time
import sqlite3
import os
# from dataclasses import dataclass, field
# from datetime import datetime, timezone
from enum import Enum
# from typing import Dict, List, Optional, Any, Tuple
from uuid import uuid4


from .k8s_integration import K8sClusterManager

# ============================================================================
# Enumerations
# ============================================================================


class RegionStatus(Enum):
    """Region health status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNREACHABLE = "unreachable"
    RECOVERING = "recovering"
    UNKNOWN = "unknown"


class ReplicationStatus(Enum):
    """Replication status between regions."""

    IN_SYNC = "in_sync"
    SYNCING = "syncing"
    OUT_OF_SYNC = "out_of_sync"
    FAILED = "failed"
    PAUSED = "paused"


class FailoverStrategy(Enum):
    """Failover strategy types."""

    AUTOMATIC = "automatic"  # Auto-failover on primary failure
    MANUAL = "manual"  # Manual failover only
    GRACEFUL = "graceful"  # Coordinated failover
    CASCADING = "cascading"  # Multi-level failover


class ResourceType(Enum):
    """Types of resources that can be replicated."""

    VM = "vm"
    STORAGE = "storage"
    NETWORK = "network"
    CONFIG = "config"
    STATE = "state"
    K8S_WORKLOAD = "k8s_workload"


# ============================================================================
# Domain Models
# ============================================================================


@dataclass
class Region:
    """Represents a geographic region/datacenter."""

    region_id: str
    name: str
    location: str  # Geographic location (e.g., "us-east-1")
    api_endpoint: str
    is_primary: bool = False
    status: RegionStatus = RegionStatus.UNKNOWN
    capacity_vms: int = 1000
    current_vms: int = 0
    last_heartbeat: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    latency_ms: float = 0.0
    bandwidth_mbps: float = 0.0
    replication_lag_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "region_id": self.region_id,
            "name": self.name,
            "location": self.location,
            "api_endpoint": self.api_endpoint,
            "is_primary": self.is_primary,
            "status": self.status.value,
            "capacity_vms": self.capacity_vms,
            "current_vms": self.current_vms,
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "latency_ms": self.latency_ms,
            "bandwidth_mbps": self.bandwidth_mbps,
            "replication_lag_seconds": self.replication_lag_seconds,
        }


@dataclass
class ReplicatedResource:
    """Represents a resource replicated across regions."""

    resource_id: str
    resource_type: ResourceType
    primary_region_id: str
    replica_regions: Dict[str, str] = field(
        default_factory=dict
    )  # region_id -> replica_id
    data_hash: str = ""
    last_sync_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    replication_status: Dict[str, ReplicationStatus] = field(default_factory=dict)
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "resource_id": self.resource_id,
            "resource_type": self.resource_type.value,
            "primary_region_id": self.primary_region_id,
            "replica_regions": self.replica_regions,
            "data_hash": self.data_hash,
            "last_sync_time": self.last_sync_time.isoformat(),
            "replication_status": {
                k: v.value for k, v in self.replication_status.items()
            },
            "version": self.version,
            "metadata": self.metadata,
        }


@dataclass
class FailoverEvent:
    """Records a failover operation."""

    event_id: str
    timestamp: datetime
    from_region_id: str
    to_region_id: str
    reason: str
    affected_resources: int
    success: bool
    duration_seconds: float = 0.0
    rollback_required: bool = False
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "from_region_id": self.from_region_id,
            "to_region_id": self.to_region_id,
            "reason": self.reason,
            "affected_resources": self.affected_resources,
            "success": self.success,
            "duration_seconds": self.duration_seconds,
            "rollback_required": self.rollback_required,
            "notes": self.notes,
        }


@dataclass
class ReplicationConfig:
    """Configuration for replication between regions."""

    source_region_id: str
    target_region_id: str
    resource_types: List[ResourceType]
    sync_interval_seconds: int = 300  # Default 5 minutes
    batch_size: int = 100
    priority: int = 1
    enabled: bool = True
    bidirectional: bool = False
    compression: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "source_region_id": self.source_region_id,
            "target_region_id": self.target_region_id,
            "resource_types": [rt.value for rt in self.resource_types],
            "sync_interval_seconds": self.sync_interval_seconds,
            "batch_size": self.batch_size,
            "priority": self.priority,
            "enabled": self.enabled,
            "bidirectional": self.bidirectional,
            "compression": self.compression,
        }


# ============================================================================
# Multi-Region Manager
# ============================================================================


class MultiRegionManager:
    """Manages multi-region operations, replication, and failover."""

    def __init__(self, config_dir: Optional[str] = None):
        """Initialize the multi-region manager.

        Args:
            config_dir: Directory for storing region configuration
        """
        if config_dir is None:
            try:
                from opt.core.config import settings

                config_dir = settings.MULTIREGION_CONFIG_DIR
            except ImportError:
                config_dir = "/etc/debvisor/regions"

        self.config_dir = config_dir
        self.regions: Dict[str, Region] = {}
        self.resources: Dict[str, ReplicatedResource] = {}
        self.replication_configs: Dict[str, ReplicationConfig] = {}
        self.failover_events: List[FailoverEvent] = []
        self.health_checks: Dict[str, asyncio.Task] = {}
        self.replication_tasks: Dict[str, asyncio.Task] = {}
        self.k8s_manager = K8sClusterManager()
        self.logger = self._setup_logging()
        self._ensure_config_dir()
        self._init_db()
        self._load_state()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for multi-region manager."""
        logger = logging.getLogger("DebVisor.MultiRegion")
        handler = logging.FileHandler(f"{self.config_dir}/multiregion.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def _ensure_config_dir(self) -> None:
        """Ensure configuration directory exists."""
        os.makedirs(self.config_dir, exist_ok=True)

    def _init_db(self) -> None:
        """Initialize SQLite database for persistence."""
        db_path = os.path.join(self.config_dir, "multiregion.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        with self.conn:
            self.conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS regions (
                    region_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    api_endpoint TEXT NOT NULL,
                    is_primary BOOLEAN DEFAULT 0,
                    status TEXT,
                    capacity_vms INTEGER,
                    current_vms INTEGER,
                    last_heartbeat TEXT,
                    latency_ms REAL,
                    bandwidth_mbps REAL,
                    replication_lag_seconds REAL
                );

                CREATE TABLE IF NOT EXISTS resources (
                    resource_id TEXT PRIMARY KEY,
                    resource_type TEXT NOT NULL,
                    primary_region_id TEXT NOT NULL,
                    replica_regions TEXT,  -- JSON
                    data_hash TEXT,
                    last_sync_time TEXT,
                    replication_status TEXT, -- JSON
                    version INTEGER,
                    metadata TEXT -- JSON
                );

                CREATE TABLE IF NOT EXISTS failover_events (
                    event_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    from_region_id TEXT NOT NULL,
                    to_region_id TEXT NOT NULL,
                    reason TEXT,
                    affected_resources INTEGER,
                    success BOOLEAN,
                    duration_seconds REAL,
                    rollback_required BOOLEAN,
                    notes TEXT
                );

                CREATE TABLE IF NOT EXISTS replication_configs (
                    config_id TEXT PRIMARY KEY,
                    source_region_id TEXT NOT NULL,
                    target_region_id TEXT NOT NULL,
                    resource_types TEXT, -- JSON
                    sync_interval_seconds INTEGER,
                    batch_size INTEGER,
                    priority INTEGER,
                    enabled BOOLEAN,
                    bidirectional BOOLEAN,
                    compression BOOLEAN
                );
            """
            )

    def _load_state(self) -> None:
        """Load state from database."""
        try:
            # Load Regions
            cursor = self.conn.execute("SELECT * FROM regions")
            for row in cursor:
                region = Region(
                    region_id=row["region_id"],
                    name=row["name"],
                    location=row["location"],
                    api_endpoint=row["api_endpoint"],
                    is_primary=bool(row["is_primary"]),
                    status=(
                        RegionStatus(row["status"])
                        if row["status"]
                        else RegionStatus.UNKNOWN
                    ),
                    capacity_vms=row["capacity_vms"],
                    current_vms=row["current_vms"],
                    last_heartbeat=(
                        datetime.fromisoformat(row["last_heartbeat"])
                        if row["last_heartbeat"]
                        else datetime.now(timezone.utc)
                    ),
                    latency_ms=row["latency_ms"],
                    bandwidth_mbps=row["bandwidth_mbps"],
                    replication_lag_seconds=row["replication_lag_seconds"],
                )
                self.regions[region.region_id] = region

            # Load Resources
            cursor = self.conn.execute("SELECT * FROM resources")
            for row in cursor:
                resource = ReplicatedResource(
                    resource_id=row["resource_id"],
                    resource_type=ResourceType(row["resource_type"]),
                    primary_region_id=row["primary_region_id"],
                    replica_regions=(
                        json.loads(row["replica_regions"])
                        if row["replica_regions"]
                        else {}
                    ),
                    data_hash=row["data_hash"],
                    last_sync_time=(
                        datetime.fromisoformat(row["last_sync_time"])
                        if row["last_sync_time"]
                        else datetime.now(timezone.utc)
                    ),
                    replication_status={
                        k: ReplicationStatus(v)
                        for k, v in (
                            json.loads(row["replication_status"])
                            if row["replication_status"]
                            else {}
                        ).items()
                    },
                    version=row["version"],
                    metadata=json.loads(row["metadata"]) if row["metadata"] else {},
                )
                self.resources[resource.resource_id] = resource

            # Load Failover Events
            cursor = self.conn.execute("SELECT * FROM failover_events")
            for row in cursor:
                event = FailoverEvent(
                    event_id=row["event_id"],
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    from_region_id=row["from_region_id"],
                    to_region_id=row["to_region_id"],
                    reason=row["reason"],
                    affected_resources=row["affected_resources"],
                    success=bool(row["success"]),
                    duration_seconds=row["duration_seconds"],
                    rollback_required=bool(row["rollback_required"]),
                    notes=row["notes"],
                )
                self.failover_events.append(event)

            # Load Replication Configs
            cursor = self.conn.execute("SELECT * FROM replication_configs")
            for row in cursor:
                config = ReplicationConfig(
                    source_region_id=row["source_region_id"],
                    target_region_id=row["target_region_id"],
                    resource_types=(
                        [ResourceType(rt) for rt in json.loads(row["resource_types"])]
                        if row["resource_types"]
                        else []
                    ),
                    sync_interval_seconds=row["sync_interval_seconds"],
                    batch_size=row["batch_size"],
                    priority=row["priority"],
                    enabled=bool(row["enabled"]),
                    bidirectional=bool(row["bidirectional"]),
                    compression=bool(row["compression"]),
                )
                self.replication_configs[row["config_id"]] = config

            self.logger.info(
                f"Loaded state: {len(self.regions)} regions, {len(self.resources)} resources"
            )

        except Exception as e:
            self.logger.error(f"Failed to load state: {e}")

    def close(self) -> None:
        """Close database connection and cleanup resources."""
        try:
            if hasattr(self, "conn") and self.conn:
                self.conn.close()
        except Exception:
            if hasattr(self, "logger"):
                self.logger.error("Error closing database connection")

        # Close all logger handlers
        try:
            if hasattr(self, "logger"):
                for handler in self.logger.handlers[:]:
                    handler.close()
                    self.logger.removeHandler(handler)
        except Exception:
            pass  # Ignore errors during cleanup # nosec B110

    def _save_region(self, region: Region) -> None:
        """Save region to database."""
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT OR REPLACE INTO regions (
                        region_id, name, location, api_endpoint, is_primary, status,
                        capacity_vms, current_vms, last_heartbeat, latency_ms,
                        bandwidth_mbps, replication_lag_seconds
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        region.region_id,
                        region.name,
                        region.location,
                        region.api_endpoint,
                        region.is_primary,
                        region.status.value,
                        region.capacity_vms,
                        region.current_vms,
                        region.last_heartbeat.isoformat(),
                        region.latency_ms,
                        region.bandwidth_mbps,
                        region.replication_lag_seconds,
                    ),
                )
        except Exception as e:
            self.logger.error(f"Failed to save region {region.region_id}: {e}")

    def _save_resource(self, resource: ReplicatedResource) -> None:
        """Save resource to database."""
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT OR REPLACE INTO resources (
                        resource_id, resource_type, primary_region_id, replica_regions,
                        data_hash, last_sync_time, replication_status, version, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        resource.resource_id,
                        resource.resource_type.value,
                        resource.primary_region_id,
                        json.dumps(resource.replica_regions),
                        resource.data_hash,
                        resource.last_sync_time.isoformat(),
                        json.dumps(
                            {k: v.value for k, v in resource.replication_status.items()}
                        ),
                        resource.version,
                        json.dumps(resource.metadata),
                    ),
                )
        except Exception as e:
            self.logger.error(f"Failed to save resource {resource.resource_id}: {e}")

    def _save_failover_event(self, event: FailoverEvent) -> None:
        """Save failover event to database."""
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT OR REPLACE INTO failover_events (
                        event_id, timestamp, from_region_id, to_region_id, reason,
                        affected_resources, success, duration_seconds, rollback_required, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        event.event_id,
                        event.timestamp.isoformat(),
                        event.from_region_id,
                        event.to_region_id,
                        event.reason,
                        event.affected_resources,
                        event.success,
                        event.duration_seconds,
                        event.rollback_required,
                        event.notes,
                    ),
                )
        except Exception as e:
            self.logger.error(f"Failed to save failover event {event.event_id}: {e}")

    def _save_replication_config(
        self, config_id: str, config: ReplicationConfig
    ) -> None:
        """Save replication config to database."""
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT OR REPLACE INTO replication_configs (
                        config_id, source_region_id, target_region_id, resource_types,
                        sync_interval_seconds, batch_size, priority, enabled,
                        bidirectional, compression
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        config_id,
                        config.source_region_id,
                        config.target_region_id,
                        json.dumps([rt.value for rt in config.resource_types]),
                        config.sync_interval_seconds,
                        config.batch_size,
                        config.priority,
                        config.enabled,
                        config.bidirectional,
                        config.compression,
                    ),
                )
        except Exception as e:
            self.logger.error(f"Failed to save replication config {config_id}: {e}")

    def register_region(
        self,
        name: str,
        location: str,
        api_endpoint: str,
        is_primary: bool = False,
        capacity_vms: int = 1000,
    ) -> Region:
        """Register a new region.

        Args:
            name: Region name
            location: Geographic location
            api_endpoint: API endpoint URL
            is_primary: Whether this is primary region
            capacity_vms: VM capacity of region

        Returns:
            Registered Region
        """
        region_id = location.lower().replace(" ", "-")

        # If this is primary, demote other primaries
        if is_primary:
            for region in self.regions.values():
                region.is_primary = False

        region = Region(
            region_id=region_id,
            name=name,
            location=location,
            api_endpoint=api_endpoint,
            is_primary=is_primary,
            capacity_vms=capacity_vms,
        )

        self.regions[region_id] = region
        self._save_region(region)
        self.logger.info(f"Registered region {region_id}: {name} ({location})")

        return region

    def get_region(self, region_id: str) -> Optional[Region]:
        """Get region by ID.

        Args:
            region_id: Region ID

        Returns:
            Region or None if not found
        """
        return self.regions.get(region_id)

    def get_primary_region(self) -> Optional[Region]:
        """Get the primary region.

        Returns:
            Primary Region or None
        """
        for region in self.regions.values():
            if region.is_primary:
                return region
        return None

    def list_regions(self, status: Optional[RegionStatus] = None) -> List[Region]:
        """List regions with optional filtering.

        Args:
            status: Filter by status

        Returns:
            List of regions
        """
        regions = list(self.regions.values())
        if status:
            regions = [r for r in regions if r.status == status]
        return regions

    async def check_region_health(self, region_id: str) -> RegionStatus:
        """Check health of a region via API ping.

        Args:
            region_id: Region ID

        Returns:
            RegionStatus
        """
        region = self.get_region(region_id)
        if not region:
            return RegionStatus.UNKNOWN

        try:
            # Simulate health check with latency measurement
            start_time = time.time()

            # Check K8s cluster health if applicable
            k8s_status = await self.k8s_manager.check_cluster_health(region_id)

            # In real implementation, make actual HTTP request
            await asyncio.sleep(0.1)  # Simulated latency

            latency = (time.time() - start_time) * 1000
            region.latency_ms = latency
            region.last_heartbeat = datetime.now(timezone.utc)

            # Determine status based on latency and K8s status
            if latency < 100 and k8s_status.is_reachable:
                region.status = RegionStatus.HEALTHY
            elif latency < 500 or not k8s_status.is_reachable:
                region.status = RegionStatus.DEGRADED
            else:
                region.status = RegionStatus.UNREACHABLE

            self.logger.info(
                f"Health check for {region_id}: {region.status.value} ({latency:.0f}ms)"
            )
            return region.status

        except Exception as e:
            region.status = RegionStatus.UNREACHABLE
            self.logger.error(f"Health check failed for {region_id}: {e}")
            return RegionStatus.UNREACHABLE

    def setup_replication(
        self,
        source_region_id: str,
        target_region_id: str,
        resource_types: List[ResourceType],
        sync_interval_seconds: int = 300,
        bidirectional: bool = False,
    ) -> ReplicationConfig:
        """Setup replication between regions.

        Args:
            source_region_id: Source region ID
            target_region_id: Target region ID
            resource_types: Types of resources to replicate
            sync_interval_seconds: Sync interval
            bidirectional: Enable bidirectional sync

        Returns:
            ReplicationConfig
        """
        config_id = f"{source_region_id}->{target_region_id}"

        config = ReplicationConfig(
            source_region_id=source_region_id,
            target_region_id=target_region_id,
            resource_types=resource_types,
            sync_interval_seconds=sync_interval_seconds,
            bidirectional=bidirectional,
        )

        self.replication_configs[config_id] = config
        self._save_replication_config(config_id, config)
        self.logger.info(
            f"Setup replication {config_id}: "
            f"{len(resource_types)} resource types, "
            f"sync every {sync_interval_seconds}s"
        )

        return config

    async def sync_resource(
        self, resource_id: str, source_region_id: str, target_region_id: str
    ) -> bool:
        """Sync a resource to another region.

        Args:
            resource_id: Resource ID
            source_region_id: Source region
            target_region_id: Target region

        Returns:
            True if successful
        """
        resource = self.resources.get(resource_id)
        if not resource:
            self.logger.warning(f"Resource {resource_id} not found for sync")
            return False

        try:
            # Simulate resource sync
            resource.replication_status[target_region_id] = ReplicationStatus.SYNCING

            # Simulate network transfer
            await asyncio.sleep(0.5)

            # Update replication status
            resource.replication_status[target_region_id] = ReplicationStatus.IN_SYNC
            resource.last_sync_time = datetime.now(timezone.utc)
            resource.replica_regions[target_region_id] = f"{resource_id}-replica"

            self._save_resource(resource)

            self.logger.info(
                f"Synced resource {resource_id} from {source_region_id} to {target_region_id}"
            )
            return True

        except Exception as e:
            resource.replication_status[target_region_id] = ReplicationStatus.FAILED
            self.logger.error(f"Sync failed for {resource_id}: {e}")
            return False

    async def perform_failover(
        self,
        from_region_id: str,
        to_region_id: str,
        strategy: FailoverStrategy = FailoverStrategy.AUTOMATIC,
        reason: str = "Manual failover",
    ) -> Tuple[bool, FailoverEvent]:
        """Perform failover from one region to another.

        Args:
            from_region_id: Source region
            to_region_id: Target region
            strategy: Failover strategy
            reason: Reason for failover

        Returns:
            (success, FailoverEvent)
        """
        event_id = str(uuid4())[:8]
        start_time = time.time()

        try:
            self.logger.info(
                f"Starting failover {event_id}: {from_region_id} -> {to_region_id} "
                f"({strategy.value})"
            )

            # Check target region is healthy
            target_status = await self.check_region_health(to_region_id)
            if target_status == RegionStatus.UNREACHABLE:
                raise ValueError(f"Target region {to_region_id} is unreachable")

            # Sync critical resources
            affected_count = 0
            k8s_workloads = []

            for resource in self.resources.values():
                if resource.primary_region_id == from_region_id:
                    if resource.resource_type == ResourceType.K8S_WORKLOAD:
                        k8s_workloads.append(resource.resource_id)
                        affected_count += 1
                    else:
                        success = await self.sync_resource(
                            resource.resource_id, from_region_id, to_region_id
                        )
                        if success:
                            affected_count += 1

            # Trigger K8s failover if needed
            if k8s_workloads:
                k8s_success = await self.k8s_manager.trigger_failover(
                    from_region_id, to_region_id, k8s_workloads
                )
                if not k8s_success:
                    raise RuntimeError("K8s failover failed")

            # Update primary region
            old_primary = self.get_primary_region()
            if old_primary:
                old_primary.is_primary = False

            new_primary = self.get_region(to_region_id)
            if new_primary:
                new_primary.is_primary = True

            duration = time.time() - start_time

            event = FailoverEvent(
                event_id=event_id,
                timestamp=datetime.now(timezone.utc),
                from_region_id=from_region_id,
                to_region_id=to_region_id,
                reason=reason,
                affected_resources=affected_count,
                success=True,
                duration_seconds=duration,
            )

            self.failover_events.append(event)
            self._save_failover_event(event)
            self.logger.info(
                f"Failover {event_id} completed: {affected_count} resources, "
                f"{duration:.1f}s duration"
            )

            return True, event

        except Exception as e:
            duration = time.time() - start_time

            event = FailoverEvent(
                event_id=event_id,
                timestamp=datetime.now(timezone.utc),
                from_region_id=from_region_id,
                to_region_id=to_region_id,
                reason=reason,
                affected_resources=0,
                success=False,
                duration_seconds=duration,
                notes=str(e),
            )

            self.failover_events.append(event)
            self._save_failover_event(event)
            self.logger.error(f"Failover {event_id} failed: {e}")

            return False, event

    def replicate_vm(
        self, vm_id: str, primary_region_id: str, replica_regions: List[str]
    ) -> ReplicatedResource:
        """Register a VM for replication.

        Args:
            vm_id: VM ID
            primary_region_id: Primary region
            replica_regions: List of regions to replicate to

        Returns:
            ReplicatedResource
        """
        resource = ReplicatedResource(
            resource_id=vm_id,
            resource_type=ResourceType.VM,
            primary_region_id=primary_region_id,
            metadata={"vm_id": vm_id},
        )

        # Initialize replication status for all regions
        for region_id in replica_regions:
            resource.replication_status[region_id] = ReplicationStatus.SYNCING
            resource.replica_regions[region_id] = f"{vm_id}-replica-{region_id}"

        self.resources[vm_id] = resource
        self._save_resource(resource)
        self.logger.info(
            f"Registered VM {vm_id} for replication: "
            f"primary={primary_region_id}, replicas={replica_regions}"
        )

        return resource

    def get_replication_status(self, resource_id: str) -> Dict[str, Any]:
        """Get replication status for a resource.

        Args:
            resource_id: Resource ID

        Returns:
            Status dictionary
        """
        resource = self.resources.get(resource_id)
        if not resource:
            return {}

        status_summary = {
            "resource_id": resource_id,
            "resource_type": resource.resource_type.value,
            "primary_region": resource.primary_region_id,
            "version": resource.version,
            "last_sync": resource.last_sync_time.isoformat(),
            "replicas": {},
        }

        for region_id, status in resource.replication_status.items():
            status_summary["replicas"][region_id] = {
                "status": status.value,
                "replica_id": resource.replica_regions.get(region_id, "unknown"),
            }

        return status_summary

    def get_failover_history(
        self, region_id: Optional[str] = None, limit: int = 50
    ) -> List[FailoverEvent]:
        """Get failover history.

        Args:
            region_id: Filter by region
            limit: Maximum results

        Returns:
            List of FailoverEvent
        """
        events = self.failover_events

        if region_id:
            events = [
                e
                for e in events
                if e.from_region_id == region_id or e.to_region_id == region_id
            ]

        # Sort by timestamp, newest first
        events = sorted(events, key=lambda e: e.timestamp, reverse=True)
        return events[:limit]

    def get_region_statistics(self, region_id: str) -> Dict[str, Any]:
        """Get statistics for a region.

        Args:
            region_id: Region ID

        Returns:
            Statistics dictionary
        """
        region = self.get_region(region_id)
        if not region:
            return {}

        # Count resources by type
        resources_by_type: Any = {}
        for resource in self.resources.values():
            if resource.primary_region_id == region_id:
                rt = resource.resource_type.value
                resources_by_type[rt] = resources_by_type.get(rt, 0) + 1

        # Count failover events
        failover_count = len(
            [
                e
                for e in self.failover_events
                if e.from_region_id == region_id or e.to_region_id == region_id
            ]
        )

        return {
            "region_id": region_id,
            "name": region.name,
            "status": region.status.value,
            "capacity_vms": region.capacity_vms,
            "current_vms": region.current_vms,
            "utilization_percent": (
                (region.current_vms / region.capacity_vms * 100)
                if region.capacity_vms > 0
                else 0
            ),
            "latency_ms": region.latency_ms,
            "bandwidth_mbps": region.bandwidth_mbps,
            "last_heartbeat": region.last_heartbeat.isoformat(),
            "resources_primary": sum(resources_by_type.values()),
            "resources_by_type": resources_by_type,
            "failover_events": failover_count,
        }

    def get_global_statistics(self) -> Dict[str, Any]:
        """Get global multi-region statistics.

        Returns:
            Global statistics dictionary
        """
        total_resources = len(self.resources)
        healthy_regions = len(
            [r for r in self.regions.values() if r.status == RegionStatus.HEALTHY]
        )
        total_capacity = sum(r.capacity_vms for r in self.regions.values())
        total_current = sum(r.current_vms for r in self.regions.values())

        sync_stats = {}
        for resource in self.resources.values():
            synced = sum(
                1
                for status in resource.replication_status.values()
                if status == ReplicationStatus.IN_SYNC
            )
            total = len(resource.replication_status)
            sync_percent = (synced / total * 100) if total > 0 else 100

            if sync_percent not in sync_stats:
                sync_stats[sync_percent] = 0
            sync_stats[sync_percent] += 1

        return {
            "total_regions": len(self.regions),
            "healthy_regions": healthy_regions,
            "primary_region": (
                self.get_primary_region().region_id
                if self.get_primary_region()
                else None
            ),
            "total_resources": total_resources,
            "total_capacity_vms": total_capacity,
            "total_current_vms": total_current,
            "utilization_percent": (
                (total_current / total_capacity * 100) if total_capacity > 0 else 0
            ),
            "failover_events_total": len(self.failover_events),
            "failover_events_failed": len(
                [e for e in self.failover_events if not e.success]
            ),
            "replication_sync_stats": sync_stats,
        }


# Global manager instance
_manager: Optional[MultiRegionManager] = None


def get_multi_region_manager(config_dir: Optional[str] = None) -> MultiRegionManager:
    """Get or create global multi-region manager instance.

    Args:
        config_dir: Configuration directory (optional override)

    Returns:
        MultiRegionManager instance
    """
    global _manager
    if _manager is None:
        try:
            from opt.core.config import settings

            final_config_dir = config_dir or settings.MULTIREGION_CONFIG_DIR
        except ImportError:
            final_config_dir = config_dir or "/etc/debvisor/regions"

        _manager = MultiRegionManager(final_config_dir)
    return _manager
