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

# !/usr/bin/env python3
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


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
Enterprise Replication Scheduler for DebVisor.

Provides advanced multi-region data replication scheduling with:
- Configurable sync windows and frequencies
- Bandwidth throttling and QoS
- Conflict resolution strategies
- Incremental and full sync modes
- Priority-based scheduling
- Cross-region consistency guarantees
- Disaster recovery support
- Real-time monitoring and alerting

Author: DebVisor Team
Date: November 28, 2025
"""

    # from datetime import datetime, timezoneimport asyncio
import asyncio
from datetime import datetime, timezone
import heapq
import hashlib
import json
import logging
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

_logger=logging.getLogger(__name__)


# =============================================================================
# Enums & Constants
# =============================================================================
class ReplicationMode(Enum):
    """Replication mode types."""

    SYNC="sync"    # Synchronous - wait for all replicas
    ASYNC="async"    # Asynchronous - fire and forget
    SEMI_SYNC="semi_sync"    # Semi-synchronous - wait for quorum


class SyncType(Enum):
    """Sync operation types."""

    FULL="full"    # Full data sync
    INCREMENTAL="incremental"    # Changes only
    DIFFERENTIAL="differential"    # Since last full
    SNAPSHOT="snapshot"    # Point-in-time snapshot


class ReplicationStatus(Enum):
    """Replication job status."""

    PENDING="pending"
    SCHEDULED="scheduled"
    RUNNING="running"
    COMPLETED="completed"
    FAILED="failed"
    CANCELLED="cancelled"
    PAUSED="paused"


class ConflictResolution(Enum):
    """Conflict resolution strategies."""

    SOURCE_WINS="source_wins"
    TARGET_WINS="target_wins"
    TIMESTAMP_WINS="timestamp_wins"
    MANUAL="manual"
    MERGE="merge"


class RegionStatus(Enum):
    """Region health status."""

    HEALTHY="healthy"
    DEGRADED="degraded"
    UNAVAILABLE="unavailable"
    MAINTENANCE="maintenance"


class Priority(Enum):
    """Replication priority levels."""

    CRITICAL=1
    HIGH=2
    NORMAL=3
    LOW=4
    BACKGROUND=5


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class Region:
    """Region definition."""

    id: str
    name: str
    endpoint: str
    status: RegionStatus=RegionStatus.HEALTHY
    latency_ms: float=0.0
    bandwidth_mbps: float=1000.0
    is_primary: bool=False
    last_health_check: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_available(self) -> bool:
        """Check if region is available for replication."""
        return self.status in (RegionStatus.HEALTHY, RegionStatus.DEGRADED)


@dataclass
class ReplicationPolicy:
    """Replication policy configuration."""

    id: str
    name: str
    source_region: str
    target_regions: List[str]
    mode: ReplicationMode=ReplicationMode.ASYNC
    sync_type: SyncType=SyncType.INCREMENTAL
    conflict_resolution: ConflictResolution=ConflictResolution.TIMESTAMP_WINS
    priority: Priority=Priority.NORMAL
    enabled: bool=True

    # Scheduling
    schedule_cron: Optional[str] = None    # Cron expression
    interval_seconds: int=300    # Default 5 minutes
    sync_window_start: Optional[str] = None    # HH:MM format
    sync_window_end: Optional[str] = None

    # Throttling
    max_bandwidth_mbps: float=100.0
    max_concurrent_transfers: int=4

    # Retry configuration
    max_retries: int=3
    retry_delay_seconds: int=60

    # Data filters
    include_patterns: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=list)

    # Consistency
    require_checksum: bool=True
    require_acknowledgment: bool=False
    min_replicas_for_success: int=1


@dataclass
class ReplicationJob:
    """Replication job instance."""

    id: str
    policy_id: str
    source_region: str
    target_region: str
    sync_type: SyncType
    status: ReplicationStatus=ReplicationStatus.PENDING
    priority: Priority=Priority.NORMAL

    # Timestamps
    created_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Progress
    total_items: int=0
    processed_items: int=0
    total_bytes: int=0
    transferred_bytes: int=0

    # Results
    success_count: int=0
    error_count: int=0
    conflict_count: int=0
    errors: List[str] = field(default_factory=list)

    # Metadata
    retry_count: int=0
    checksum: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def progress_percent(self) -> float:
        """Calculate progress percentage."""
        if self.total_items == 0:
            return 0.0
        return (self.processed_items / self.total_items) * 100

    @property
    def duration_seconds(self) -> float:
        """Calculate job duration."""
        if not self.started_at:
            return 0.0
        _end=self.completed_at or datetime.now(timezone.utc)
        return (end - self.started_at).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "policy_id": self.policy_id,
            "source_region": self.source_region,
            "target_region": self.target_region,
            "sync_type": self.sync_type.value,
            "status": self.status.value,
            "priority": self.priority.value,
            "progress_percent": round(self.progress_percent, 2),
            "duration_seconds": round(self.duration_seconds, 2),
            "total_items": self.total_items,
            "processed_items": self.processed_items,
            "success_count": self.success_count,
            "error_count": self.error_count,
        }


@dataclass
class SyncWindow:
    """Maintenance/sync window definition."""

    start_hour: int    # 0-23
    start_minute: int    # 0-59
    end_hour: int
    end_minute: int
    days_of_week: List[int] = field(default_factory=lambda: [0, 1, 2, 3, 4, 5, 6])
    timezone_name: str="UTC"

    def is_within_window(self, dt: Optional[datetime] = None) -> bool:
        """Check if given time is within sync window."""
        if dt is None:
            _dt=datetime.now(timezone.utc)

        if dt.weekday() not in self.days_of_week:
            return False

        current_minutes=dt.hour * 60 + dt.minute
        start_minutes=self.start_hour * 60 + self.start_minute
        end_minutes=self.end_hour * 60 + self.end_minute

        if start_minutes <= end_minutes:
            return start_minutes <= current_minutes <= end_minutes
        else:    # Window spans midnight
            return current_minutes >= start_minutes or current_minutes <= end_minutes


@dataclass
class ReplicationConflict:
    """Replication conflict record."""

    id: str
    job_id: str
    item_id: str
    source_version: str
    target_version: str
    source_timestamp: datetime
    target_timestamp: datetime
    resolution: Optional[ConflictResolution] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# Replication Engine Interface
# =============================================================================
class ReplicationEngine(ABC):
    """Abstract replication engine interface."""

    @abstractmethod
    async def sync_item(
        self, source_region: str, target_region: str, item_id: str, item_data: bytes
    ) -> bool:
        """Sync single item to target region."""
        pass

    @abstractmethod
    async def get_changes(self, region: str, since: datetime) -> List[Dict[str, Any]]:
        """Get changes from region since timestamp."""
        pass

    @abstractmethod
    async def get_checksum(self, region: str, itemid: str) -> str:
        """Get checksum for item in region."""
        pass

    @abstractmethod
    async def resolve_conflict(
        self, conflict: ReplicationConflict, resolution: ConflictResolution
    ) -> bool:
        """Resolve replication conflict."""
        pass


class MockReplicationEngine(ReplicationEngine):
    """Mock replication engine for testing."""

    def __init__(self) -> None:
        self._data: Dict[str, Dict[str, bytes]] = {}    # region -> item_id -> data
        self._timestamps: Dict[str, Dict[str, datetime]] = {}

    async def sync_item(
        self, source_region: str, target_region: str, item_id: str, item_data: bytes
    ) -> bool:
        """Sync item to target region."""
        if target_region not in self._data:
            self._data[target_region] = {}
            self._timestamps[target_region] = {}

        self._data[target_region][item_id] = item_data
        self._timestamps[target_region][item_id] = datetime.now(timezone.utc)

        # Simulate network delay
        await asyncio.sleep(0.01)
        return True

    async def get_changes(self, region: str, since: datetime) -> List[Dict[str, Any]]:
        """Get changes since timestamp."""
        changes=[]
        _timestamps=self._timestamps.get(region, {})
        _data=self._data.get(region, {})

        for item_id, ts in timestamps.items():
            if ts > since:
                changes.append(
                    {
                        "item_id": item_id,
                        "timestamp": ts.isoformat(),
                        "data": data.get(item_id, b""),
                    }
                )

        return changes

    async def get_checksum(self, region: str, itemid: str) -> str:
        """Calculate item checksum."""
        _data=self._data.get(region, {}).get(item_id, b"")
        return hashlib.sha256(data).hexdigest()

    async def resolve_conflict(
        self, conflict: ReplicationConflict, resolution: ConflictResolution
    ) -> bool:
        """Resolve conflict."""
        conflict.resolution=resolution
        conflict.resolved_at=datetime.now(timezone.utc)
        return True


# =============================================================================
# Scheduler Queue
# =============================================================================
class JobQueue:
    """Priority queue for replication jobs."""

    def __init__(self) -> None:
        self._queue: List[Tuple[int, float, ReplicationJob]] = []
        self._lock=threading.Lock()
        self._job_map: Dict[str, ReplicationJob] = {}

    def push(self, job: ReplicationJob) -> None:
        """Add job to queue."""
        with self._lock:
        # Priority tuple: (priority_value, timestamp, job)
            _priority_key=(job.priority.value, time.time())
            heapq.heappush(self._queue, (priority_key[0], priority_key[1], job))
            self._job_map[job.id] = job

    def pop(self) -> Optional[ReplicationJob]:
        """Get highest priority job."""
        with self._lock:
            while self._queue:
                _, _, job=heapq.heappop(self._queue)
                if job.id in self._job_map:
                    del self._job_map[job.id]
                    return job
            return None

    def peek(self) -> Optional[ReplicationJob]:
        """Peek at highest priority job without removing."""
        with self._lock:
            if self._queue:
                return self._queue[0][2]
            return None

    def remove(self, jobid: str) -> bool:
        """Remove job from queue."""
        with self._lock:
            if job_id in self._job_map:
                del self._job_map[job_id]
                return True
            return False

    def __len__(self) -> int:
        with self._lock:
            return len(self._job_map)


# =============================================================================
# Replication Scheduler
# =============================================================================
class ReplicationScheduler:
    """
    Advanced multi-region replication scheduler.

    Features:
    - Policy-based scheduling
    - Priority queuing
    - Bandwidth throttling
    - Sync window support
    - Conflict resolution
    - Progress tracking
    - Health monitoring
    """

    def __init__(self, engine: Optional[ReplicationEngine] = None) -> None:
        self._engine=engine or MockReplicationEngine()
        self._regions: Dict[str, Region] = {}
        self._policies: Dict[str, ReplicationPolicy] = {}
        self._jobs: Dict[str, ReplicationJob] = {}
        self._conflicts: Dict[str, ReplicationConflict] = {}
        self._job_queue=JobQueue()

        # Runtime state
        self._running=False
        self._worker_task: Optional[asyncio.Task] = None
        self._health_check_task: Optional[asyncio.Task] = None
        self._scheduler_task: Optional[asyncio.Task] = None
        self._lock=threading.Lock()

        # Configuration
        self._max_concurrent_jobs=10
        self._health_check_interval=30    # seconds
        self._default_sync_window: Optional[SyncWindow] = None

        # Metrics
        self._metrics={
            "jobs_completed": 0,
            "jobs_failed": 0,
            "total_items_synced": 0,
            "total_bytes_transferred": 0,
            "conflicts_detected": 0,
            "conflicts_resolved": 0,
        }

        # Event handlers
        self._on_job_complete: List[Callable[[ReplicationJob], None]] = []
        self._on_job_failed: List[Callable[[ReplicationJob], None]] = []
        self._on_conflict: List[Callable[[ReplicationConflict], None]] = []

    # -------------------------------------------------------------------------
    # Region Management
    # -------------------------------------------------------------------------

    def add_region(self, region: Region) -> None:
        """Register a region."""
        self._regions[region.id] = region
        logger.info(f"Added region: {region.name} ({region.id})")

    def remove_region(self, regionid: str) -> bool:
        """Remove a region."""
        if region_id in self._regions:
            del self._regions[region_id]
            logger.info(f"Removed region: {region_id}")
            return True
        return False

    def get_region(self, regionid: str) -> Optional[Region]:
        """Get region by ID."""
        return self._regions.get(region_id)

    def get_available_regions(self) -> List[Region]:
        """Get all available regions."""
        return [r for r in self._regions.values() if r.is_available()]

    def set_region_status(self, regionid: str, status: RegionStatus) -> bool:
        """Update region status."""
        _region=self._regions.get(region_id)
        if region:
            region.status=status
            region.last_health_check=datetime.now(timezone.utc)
            return True
        return False

    # -------------------------------------------------------------------------
    # Policy Management
    # -------------------------------------------------------------------------

    def add_policy(self, policy: ReplicationPolicy) -> None:
        """Add replication policy."""
        self._policies[policy.id] = policy
        logger.info(f"Added replication policy: {policy.name}")

    def remove_policy(self, policyid: str) -> bool:
        """Remove replication policy."""
        if policy_id in self._policies:
            del self._policies[policy_id]
            return True
        return False

    def get_policy(self, policyid: str) -> Optional[ReplicationPolicy]:
        """Get policy by ID."""
        return self._policies.get(policy_id)

    def enable_policy(self, policyid: str) -> bool:
        """Enable a policy."""
        _policy=self._policies.get(policy_id)
        if policy:
            policy.enabled=True
            return True
        return False

    def disable_policy(self, policyid: str) -> bool:
        """Disable a policy."""
        _policy=self._policies.get(policy_id)
        if policy:
            policy.enabled=False
            return True
        return False

    # -------------------------------------------------------------------------
    # Job Management
    # -------------------------------------------------------------------------

    def create_job(
        self,
        policy_id: str,
        target_region: Optional[str] = None,
        sync_type: Optional[SyncType] = None,
    ) -> Optional[ReplicationJob]:
        """Create a new replication job from policy."""
        _policy=self._policies.get(policy_id)
        if not policy or not policy.enabled:
            return None

        # Determine target regions
        targets=[target_region] if target_region else policy.target_regions

        _jobs=[]
        for target in targets:
            if target not in self._regions:
                continue

            if not self._regions[target].is_available():
                logger.warning(f"Target region {target} not available, skipping")
                continue

            job=ReplicationJob(
                _id=f"job_{uuid.uuid4().hex[:12]}",
                _policy_id=policy_id,
                _source_region=policy.source_region,
                _target_region=target,
                _sync_type=sync_type or policy.sync_type,
                _priority=policy.priority,
                _status=ReplicationStatus.PENDING,
            )

            with self._lock:
                self._jobs[job.id] = job

            jobs.append(job)
            logger.info(
                f"Created replication job: {job.id} ({policy.name} -> {target})"
            )

        return jobs[0] if jobs else None

    def schedule_job(
        self, job_id: str, scheduled_time: Optional[datetime] = None
    ) -> bool:
        """Schedule a job for execution."""
        _job=self._jobs.get(job_id)
        if not job:
            return False

        job.scheduled_at=scheduled_time or datetime.now(timezone.utc)
        job.status=ReplicationStatus.SCHEDULED
        self._job_queue.push(job)

        logger.info(f"Scheduled job {job_id} for {job.scheduled_at}")
        return True

    def cancel_job(self, jobid: str) -> bool:
        """Cancel a pending or running job."""
        _job=self._jobs.get(job_id)
        if not job:
            return False

        if job.status in (ReplicationStatus.PENDING, ReplicationStatus.SCHEDULED):
            job.status=ReplicationStatus.CANCELLED
            self._job_queue.remove(job_id)
            logger.info(f"Cancelled job: {job_id}")
            return True

        return False

    def get_job(self, jobid: str) -> Optional[ReplicationJob]:
        """Get job by ID."""
        return self._jobs.get(job_id)

    def get_jobs_by_status(self, status: ReplicationStatus) -> List[ReplicationJob]:
        """Get jobs by status."""
        return [j for j in self._jobs.values() if j.status== status]

    def get_jobs_by_policy(self, policyid: str) -> List[ReplicationJob]:
        """Get jobs for a policy."""
        return [j for j in self._jobs.values() if j.policy_id== policy_id]

    # -------------------------------------------------------------------------
    # Job Execution
    # -------------------------------------------------------------------------

    async def execute_job(self, job: ReplicationJob) -> bool:
        """Execute a replication job."""
        _policy=self._policies.get(job.policy_id)
        if not policy:
            job.status=ReplicationStatus.FAILED
            job.errors.append("Policy not found")
            return False

        _source=self._regions.get(job.source_region)
        _target=self._regions.get(job.target_region)

        if not source or not target:
            job.status=ReplicationStatus.FAILED
            job.errors.append("Source or target region not found")
            return False

        if not target.is_available():
            job.status=ReplicationStatus.FAILED
            job.errors.append(f"Target region {target.id} not available")
            return False

        # Start execution
        job.status=ReplicationStatus.RUNNING
        job.started_at=datetime.now(timezone.utc)

        try:
        # Get changes to sync
            if job.sync_type == SyncType.FULL:
                _since=datetime.min.replace(tzinfo=timezone.utc)
            else:
            # Get last successful sync time
                last_job=self._get_last_successful_job(
                    job.policy_id, job.target_region
                )
                since=(
                    last_job.completed_at or datetime.min.replace(tzinfo=timezone.utc)
                    if last_job and last_job.completed_at
                    else datetime.min.replace(tzinfo=timezone.utc)
                )
            _changes=await self._engine.get_changes(job.source_region, since)
            job.total_items=len(changes)

            # Apply filters
            if policy.include_patterns or policy.exclude_patterns:
                _changes=self._apply_filters(changes, policy)

            # Process changes
            for change in changes:
                _item_id=change.get("item_id", "")
                _item_data=change.get("data", b"")

                if isinstance(item_data, str):
                    _item_data=item_data.encode()

                # Check for conflicts
                if policy.require_checksum:
                    source_checksum=await self._engine.get_checksum(
                        job.source_region, item_id
                    )
                    target_checksum=await self._engine.get_checksum(
                        job.target_region, item_id
                    )

                    if target_checksum and source_checksum != target_checksum:
                        conflict=await self._handle_conflict(
                            job, item_id, source_checksum, target_checksum, policy
                        )
                        if (
                            conflict
                            and policy.conflict_resolution == ConflictResolution.MANUAL
                        ):
                            job.conflict_count += 1
                            continue

                # Sync item
                success=await self._engine.sync_item(
                    job.source_region, job.target_region, item_id, item_data
                )

                job.processed_items += 1
                job.transferred_bytes += len(item_data)

                if success:
                    job.success_count += 1
                else:
                    job.error_count += 1

            # Calculate checksum
            if policy.require_checksum:
                job.checksum=hashlib.sha256(
                    json.dumps(
                        {"items": job.success_count, "bytes": job.transferred_bytes}
                    ).encode()
                ).hexdigest()

            job.status=ReplicationStatus.COMPLETED
            job.completed_at=datetime.now(timezone.utc)

            # Update metrics
            with self._lock:
                self._metrics["jobs_completed"] += 1
                self._metrics["total_items_synced"] += job.success_count
                self._metrics["total_bytes_transferred"] += job.transferred_bytes

            # Trigger handlers
            for handler in self._on_job_complete:
                try:
                    handler(job)
                except Exception as e:
                    logger.error(f"Job complete handler error: {e}")

            logger.info(f"Completed job {job.id}: {job.success_count} items synced")
            return True

        except Exception as e:
            job.status=ReplicationStatus.FAILED
            job.completed_at=datetime.now(timezone.utc)
            job.errors.append(str(e))

            with self._lock:
                self._metrics["jobs_failed"] += 1

            for handler in self._on_job_failed:
                try:
                    handler(job)
                except Exception as he:
                    logger.error(f"Job failed handler error: {he}")

            logger.error(f"Job {job.id} failed: {e}")
            return False

    def _get_last_successful_job(
        self, policy_id: str, target_region: str
    ) -> Optional[ReplicationJob]:
        """Get last successful job for policy/region."""
        jobs=[
            j
            for j in self._jobs.values()
            if j.policy_id == policy_id
            and j.target_region == target_region
            and j.status == ReplicationStatus.COMPLETED
        ]
        if jobs:
            return max(
                jobs,
                _key=lambda j: j.completed_at
                or datetime.min.replace(tzinfo=timezone.utc),
            )
        return None

    def _apply_filters(
        self, changes: List[Dict[str, Any]], policy: ReplicationPolicy
    ) -> List[Dict[str, Any]]:
        """Apply include/exclude filters to changes."""
        import fnmatch

        _filtered=[]
        for change in changes:
            _item_id=change.get("item_id", "")

            # Check exclude patterns
            excluded=False
            for pattern in policy.exclude_patterns:
                if fnmatch.fnmatch(item_id, pattern):
                    excluded=True
                    break

            if excluded:
                continue

            # Check include patterns (if any)
            if policy.include_patterns:
                included=False
                for pattern in policy.include_patterns:
                    if fnmatch.fnmatch(item_id, pattern):
                        included=True
                        break
                if not included:
                    continue

            filtered.append(change)

        return filtered

    async def _handle_conflict(
        self,
        job: ReplicationJob,
        item_id: str,
        source_version: str,
        target_version: str,
        policy: ReplicationPolicy,
    ) -> Optional[ReplicationConflict]:
        """Handle replication conflict."""
        conflict=ReplicationConflict(
            _id=f"conflict_{uuid.uuid4().hex[:12]}",
            _job_id=job.id,
            _item_id=item_id,
            _source_version=source_version,
            _target_version=target_version,
            _source_timestamp=datetime.now(timezone.utc),
            _target_timestamp=datetime.now(timezone.utc),
        )

        self._conflicts[conflict.id] = conflict

        with self._lock:
            self._metrics["conflicts_detected"] += 1

        # Auto-resolve based on policy
        if policy.conflict_resolution != ConflictResolution.MANUAL:
            await self._engine.resolve_conflict(conflict, policy.conflict_resolution)
            conflict.resolution=policy.conflict_resolution
            conflict.resolved_at=datetime.now(timezone.utc)

            with self._lock:
                self._metrics["conflicts_resolved"] += 1

            return None

        # Trigger conflict handlers for manual resolution
        for handler in self._on_conflict:
            try:
                handler(conflict)
            except Exception as e:
                logger.error(f"Conflict handler error: {e}")

        return conflict

    # -------------------------------------------------------------------------
    # Scheduler Loop
    # -------------------------------------------------------------------------

    async def start(self) -> None:
        """Start the replication scheduler."""
        if self._running:
            return

        self._running=True

        # Start worker task
        self._worker_task=asyncio.create_task(self._worker_loop())

        # Start health check task
        self._health_check_task=asyncio.create_task(self._health_check_loop())

        # Start policy scheduler task
        self._scheduler_task=asyncio.create_task(self._policy_scheduler_loop())

        logger.info("Replication scheduler started")

    async def stop(self) -> None:
        """Stop the replication scheduler."""
        self._running=False

        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass

        if self._scheduler_task:
            self._scheduler_task.cancel()
            try:
                await self._scheduler_task
            except asyncio.CancelledError:
                pass

        logger.info("Replication scheduler stopped")

    async def _worker_loop(self) -> None:
        """Main worker loop processing jobs."""
        while self._running:
            try:
                _job=self._job_queue.pop()

                if job:
                # Check if scheduled time has passed
                    if job.scheduled_at and job.scheduled_at > datetime.now(
                        timezone.utc
                    ):
                    # Re-queue if not yet time
                        self._job_queue.push(job)
                        await asyncio.sleep(1)
                        continue

                    # Check sync window
                    if self._default_sync_window:
                        if not self._default_sync_window.is_within_window():
                            self._job_queue.push(job)
                            await asyncio.sleep(60)
                            continue

                    # Execute job
                    await self.execute_job(job)
                else:
                    await asyncio.sleep(1)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker loop error: {e}")
                await asyncio.sleep(5)

    async def _health_check_loop(self) -> None:
        """Periodic health checks for regions."""
        while self._running:
            try:
                for region in self._regions.values():
                # Simulate health check (in production, ping endpoint)
                    region.last_health_check=datetime.now(timezone.utc)

                await asyncio.sleep(self._health_check_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check error: {e}")
                await asyncio.sleep(10)

    async def _policy_scheduler_loop(self) -> None:
        """Schedule jobs based on policy intervals."""
        policy_last_run: Dict[str, datetime] = {}

        while self._running:
            try:
                _now=datetime.now(timezone.utc)

                for policy in self._policies.values():
                    if not policy.enabled:
                        continue

                    _last_run=policy_last_run.get(policy.id)

                    if last_run is None:
                    # First run
                        policy_last_run[policy.id] = now
                        continue

                    # Check if interval has passed
                    _elapsed=(now - last_run).total_seconds()
                    if elapsed >= policy.interval_seconds:
                        _job=self.create_job(policy.id)
                        if job:
                            self.schedule_job(job.id)
                        policy_last_run[policy.id] = now

                await asyncio.sleep(10)    # Check every 10 seconds

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Policy scheduler error: {e}")
                await asyncio.sleep(30)

    # -------------------------------------------------------------------------
    # Event Handlers
    # -------------------------------------------------------------------------

    def on_job_complete(self, handler: Callable[[ReplicationJob], None]) -> None:
        """Register job completion handler."""
        self._on_job_complete.append(handler)

    def on_job_failed(self, handler: Callable[[ReplicationJob], None]) -> None:
        """Register job failure handler."""
        self._on_job_failed.append(handler)

    def on_conflict(self, handler: Callable[[ReplicationConflict], None]) -> None:
        """Register conflict handler."""
        self._on_conflict.append(handler)

    # -------------------------------------------------------------------------
    # Metrics & Reporting
    # -------------------------------------------------------------------------

    def get_metrics(self) -> Dict[str, Any]:
        """Get scheduler metrics."""
        with self._lock:
            return {
                "jobs_completed": self._metrics["jobs_completed"],
                "jobs_failed": self._metrics["jobs_failed"],
                "total_items_synced": self._metrics["total_items_synced"],
                "total_bytes_transferred": self._metrics["total_bytes_transferred"],
                "conflicts_detected": self._metrics["conflicts_detected"],
                "conflicts_resolved": self._metrics["conflicts_resolved"],
                "pending_jobs": len(self._job_queue),
                "running_jobs": len(self.get_jobs_by_status(ReplicationStatus.RUNNING)),
                "regions_available": len(self.get_available_regions()),
                "policies_enabled": len(
                    [p for p in self._policies.values() if p.enabled]
                ),
            }

    def get_region_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all regions."""
        return {
            region_id: {
                "name": region.name,
                "status": region.status.value,
                "is_primary": region.is_primary,
                "latency_ms": region.latency_ms,
                "last_health_check": (
                    region.last_health_check.isoformat()
                    if region.last_health_check
                    else None
                ),
            }
            for region_id, region in self._regions.items()
        }


# =============================================================================
# Flask Integration
# =============================================================================
def create_replication_blueprint(scheduler: ReplicationScheduler) -> Any:
    """Create Flask blueprint for replication API."""
    try:
        from flask import Blueprint, request, jsonify

        _bp=Blueprint("replication", __name__, url_prefix="/api/replication")

        @bp.route("/regions", methods=["GET"])  # type: ignore[type-var]
        def list_regions() -> None:
            """List all regions."""
            return jsonify(scheduler.get_region_status())  # type: ignore[return-value]

        @bp.route("/policies", methods=["GET"])  # type: ignore[type-var]
        def list_policies() -> None:
            """List all policies."""
            return jsonify(  # type: ignore[return-value]
                {
                    pid: {
                        "name": p.name,
                        "source": p.source_region,
                        "targets": p.target_regions,
                        "enabled": p.enabled,
                        "mode": p.mode.value,
                    }
                    for pid, p in scheduler._policies.items()
                }
            )

        @bp.route("/jobs", methods=["GET"])  # type: ignore[type-var]
        def list_jobs() -> None:
            """List jobs with optional status filter."""
            _status_param=request.args.get("status")

            if status_param:
                try:
                    _status=ReplicationStatus(status_param)
                    _jobs=scheduler.get_jobs_by_status(status)
                except ValueError:
                    return jsonify({"error": "Invalid status"}), 400  # type: ignore[return-value]
            else:
                _jobs=list(scheduler._jobs.values())

            return jsonify(  # type: ignore[return-value]
                {
                    "jobs": [j.to_dict() for j in jobs[-50:]],    # Last 50
                    "total": len(jobs),
                }
            )

        @bp.route("/jobs/<job_id>", methods=["GET"])
        def get_job(jobid: str) -> Any:
            """Get job details."""
            _job=scheduler.get_job(job_id)
            if not job:
                return jsonify({"error": "Job not found"}), 404
            return jsonify(job.to_dict())

        @bp.route("/jobs", methods=["POST"])  # type: ignore[type-var]
        def create_job() -> None:
            """Create new replication job."""
            _data=request.get_json() or {}
            _policy_id=data.get("policy_id")

            if not policy_id:
                return jsonify({"error": "policy_id required"}), 400  # type: ignore[return-value]

            job=scheduler.create_job(
                policy_id,
                _target_region=data.get("target_region"),
                _sync_type=SyncType(data["sync_type"]) if "sync_type" in data else None,
            )

            if not job:
                return jsonify({"error": "Failed to create job"}), 400  # type: ignore[return-value]

            # Schedule immediately
            scheduler.schedule_job(job.id)

            return jsonify(job.to_dict()), 201  # type: ignore[return-value]

        @bp.route("/metrics", methods=["GET"])  # type: ignore[type-var]
        def get_metrics() -> None:
            """Get scheduler metrics."""
            return jsonify(scheduler.get_metrics())  # type: ignore[return-value]

        return bp

    except ImportError:
        logger.warning("Flask not available for replication blueprint")
        return None


# =============================================================================
# Module Exports
# =============================================================================

__all__=[
    "ReplicationMode",
    "SyncType",
    "ReplicationStatus",
    "ConflictResolution",
    "RegionStatus",
    "Priority",
    "Region",
    "ReplicationPolicy",
    "ReplicationJob",
    "SyncWindow",
    "ReplicationConflict",
    "ReplicationEngine",
    "MockReplicationEngine",
    "JobQueue",
    "ReplicationScheduler",
    "create_replication_blueprint",
]
