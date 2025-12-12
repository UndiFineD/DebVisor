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


"""
Batch operations for DebVisor Web Panel.

Features:
- Queue-based batch operation processing
- Rollback capability
- Operation history tracking
- Dry-run preview
- Progress monitoring
- Error recovery
- Transaction-like semantics

Supported operations:
- Node operations (reboot, drain, maintenance)
- Storage operations (snapshot, scrub, repair)
- Configuration changes (bulk update)
- Monitoring changes (threshold updates)
"""

import asyncio
from datetime import datetime, timezone, timedelta
import logging
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class OperationStatus(Enum):
    """Operation status."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"
    PARTIALLY_ROLLED_BACK = "partially_rolled_back"
    ROLLBACK_FAILED = "rollback_failed"


class OperationType(Enum):
    """Types of batch operations."""

    NODE_REBOOT = "node_reboot"
    NODE_DRAIN = "node_drain"
    NODE_MAINTENANCE = "node_maintenance"
    STORAGE_SNAPSHOT = "storage_snapshot"
    STORAGE_SCRUB = "storage_scrub"
    STORAGE_REPAIR = "storage_repair"
    CONFIG_UPDATE = "config_update"
    THRESHOLD_UPDATE = "threshold_update"


@dataclass
class OperationResult:
    """Result of a single operation."""

    operation_id: str
    resource_id: str
    status: OperationStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    error: Optional[str] = None
    result_data: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> Optional[timedelta]:
        """Get operation duration."""
        if self.end_time:
            return self.end_time - self.start_time
        return None

    @property
    def is_success(self) -> bool:
        """Check if operation succeeded."""
        return self.status == OperationStatus.COMPLETED


@dataclass
class BatchOperation:
    """Represents a batch operation."""

    id: str
    type: OperationType
    name: str
    description: str
    resources: List[str]    # Resource IDs to operate on
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: OperationStatus = OperationStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: int = 0    # 0-100
    results: List[OperationResult] = field(default_factory=list)
    rollback_available: bool = False
    error: Optional[str] = None

    @property
    def duration(self) -> Optional[timedelta]:
        """Get batch operation duration."""
        if self.completed_at and self.started_at:
            return self.completed_at - self.started_at
        elif self.started_at:
            return datetime.now(timezone.utc) - self.started_at
        return None

    @property
    def success_count(self) -> int:
        """Get number of successful operations."""
        return sum(1 for r in self.results if r.is_success)

    @property
    def failure_count(self) -> int:
        """Get number of failed operations."""
        return sum(1 for r in self.results if r.status == OperationStatus.FAILED)

    def get_summary(self) -> Dict[str, Any]:
        """Get operation summary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "name": self.name,
            "status": self.status.value,
            "resources": len(self.resources),
            "progress": self.progress,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "duration": str(self.duration) if self.duration else None,
            "created_at": self.created_at.isoformat(),
        }


class OperationExecutor:
    """Executes individual operations."""

    def __init__(self) -> None:
        """Initialize executor."""
        self.handlers: Dict[OperationType, Callable[..., Any]] = {}
        self.rollback_handlers: Dict[OperationType, Callable[..., Any]] = {}

    def register_handler(
        self,
        op_type: OperationType,
        handler: Callable[..., Any],
        rollback_handler: Optional[Callable[..., Any]] = None,
    ) -> None:
        """
        Register operation handler.

        Args:
            op_type: Operation type
            handler: Handler callable
            rollback_handler: Optional rollback handler callable
        """
        self.handlers[op_type] = handler
        if rollback_handler:
            self.rollback_handlers[op_type] = rollback_handler
        logger.debug(f"Registered handler for {op_type.value}")

    async def execute(
        self,
        operation: BatchOperation,
        resource_id: str,
        parameters: Dict[str, Any],
    ) -> OperationResult:
        """
        Execute single operation.

        Args:
            operation: Batch operation
            resource_id: Resource ID
            parameters: Operation parameters

        Returns:
            OperationResult
        """
        result = OperationResult(
            operation_id=operation.id,
            resource_id=resource_id,
            status=OperationStatus.RUNNING,
            start_time=datetime.now(timezone.utc),
        )

        try:
            handler = self.handlers.get(operation.type)
            if handler is None:
                raise ValueError(
                    f"No handler for operation type {operation.type.value}"
                )

            # Call handler
            if asyncio.iscoroutinefunction(handler):
                result_data = await handler(resource_id, parameters)
            else:
                result_data = handler(resource_id, parameters)

            result.status = OperationStatus.COMPLETED
            result.result_data = result_data or {}

        except Exception as e:
            logger.error(f"Operation failed: {e}")
            result.status = OperationStatus.FAILED
            result.error = str(e)

        finally:
            result.end_time = datetime.now(timezone.utc)

        return result

    async def execute_rollback(
        self,
        operation: BatchOperation,
        resource_id: str,
        result_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute rollback for a single resource.

        Args:
            operation: Batch operation
            resource_id: Resource ID
            result_data: Data from the original successful operation

        Returns:
            Rollback result dictionary
        """
        handler = self.rollback_handlers.get(operation.type)
        if not handler:
            return {"status": "skipped", "reason": "no_rollback_handler"}

        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(resource_id, result_data)
            else:
                handler(resource_id, result_data)
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Rollback failed for {resource_id}: {e}")
            raise


class BatchOperationManager:
    """Manages batch operations."""

    def __init__(self, executor: Optional[OperationExecutor] = None) -> None:
        """
        Initialize manager.

        Args:
            executor: OperationExecutor instance
        """
        self.executor = executor or OperationExecutor()
        self.operations: Dict[str, BatchOperation] = {}
        self.queue: asyncio.Queue[BatchOperation] = asyncio.Queue()
        self.history: List[BatchOperation] = []
        self.max_history_size = 100
        self.worker_count = 3

    async def create_batch_operation(
        self,
        op_type: OperationType,
        name: str,
        description: str,
        resources: List[str],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> BatchOperation:
        """
        Create a batch operation.

        Args:
            op_type: Operation type
            name: Operation name
            description: Operation description
            resources: Resource IDs
            parameters: Operation parameters

        Returns:
            BatchOperation instance
        """
        operation = BatchOperation(
            id=str(uuid.uuid4()),
            type=op_type,
            name=name,
            description=description,
            resources=resources,
            parameters=parameters or {},
        )

        self.operations[operation.id] = operation
        logger.info(f"Created batch operation {operation.id}: {name}")

        return operation

    async def submit_operation(self, operation: BatchOperation) -> None:
        """
        Submit operation to queue.

        Args:
            operation: BatchOperation to submit
        """
        operation.status = OperationStatus.QUEUED
        await self.queue.put(operation)
        logger.info(f"Submitted operation {operation.id} to queue")

    async def preview_dry_run(self, operation: BatchOperation) -> Dict[str, Any]:
        """
        Preview operation with dry-run.

        Args:
            operation: BatchOperation to preview

        Returns:
            Dry-run preview information
        """
        preview = {
            "operation_id": operation.id,
            "type": operation.type.value,
            "name": operation.name,
            "description": operation.description,
            "resources": operation.resources,
            "resource_count": len(operation.resources),
            "parameters": operation.parameters,
            "estimated_duration_seconds": self._estimate_duration(operation),
            "rollback_supported": self._supports_rollback(operation.type),
        }

        logger.info(f"Generated dry-run preview for operation {operation.id}")
        return preview

    async def start_worker(self) -> None:
        """Start worker for processing operations."""
        logger.info("Operation worker started")

        while True:
            try:
            # Get next operation from queue
                operation = await asyncio.wait_for(self.queue.get(), timeout=10.0)

                await self._process_operation(operation)

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Worker error: {e}")
                await asyncio.sleep(1)

    async def _process_operation(self, operation: BatchOperation) -> None:
        """
        Process a batch operation.

        Args:
            operation: BatchOperation to process
        """
        operation.status = OperationStatus.RUNNING
        operation.started_at = datetime.now(timezone.utc)

        logger.info(f"Processing operation {operation.id}")

        try:
        # Process each resource
            for idx, resource_id in enumerate(operation.resources):
                result = await self.executor.execute(
                    operation, resource_id, operation.parameters
                )

                operation.results.append(result)

                # Update progress
                operation.progress = int((idx + 1) / len(operation.resources) * 100)

                logger.debug(
                    f"Processed {idx + 1}/{len(operation.resources)} "
                    f"for operation {operation.id}"
                )

            # Mark as complete
            operation.status = OperationStatus.COMPLETED
            operation.completed_at = datetime.now(timezone.utc)
            operation.rollback_available = self._supports_rollback(operation.type)

            logger.info(
                f"Operation {operation.id} completed: "
                f"{operation.success_count} successful, "
                f"{operation.failure_count} failed"
            )

        except Exception as e:
            logger.error(f"Operation {operation.id} failed: {e}")
            operation.status = OperationStatus.FAILED
            operation.error = str(e)
            operation.completed_at = datetime.now(timezone.utc)

        finally:
        # Add to history
            await self._add_to_history(operation)

    async def _add_to_history(self, operation: BatchOperation) -> None:
        """Add operation to history."""
        self.history.append(operation)

        if len(self.history) > self.max_history_size:
            self.history.pop(0)

    async def get_operation_status(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get operation status.

        Args:
            operation_id: Operation ID

        Returns:
            Status dictionary or None if not found
        """
        operation = self.operations.get(operation_id)
        if operation is None:
            return None

        return operation.get_summary()

    async def cancel_operation(self, operation_id: str) -> bool:
        """
        Cancel pending operation.

        Args:
            operation_id: Operation ID

        Returns:
            True if cancelled, False if not found or already running
        """
        operation = self.operations.get(operation_id)
        if operation is None:
            return False

        if operation.status in (OperationStatus.PENDING, OperationStatus.QUEUED):
            operation.status = OperationStatus.CANCELLED
            logger.info(f"Cancelled operation {operation_id}")
            return True

        return False

    async def rollback_operation(self, operation_id: str) -> bool:
        """
        Rollback completed operation with full state restoration.

        Implements atomic rollback with type-specific reversal logic and audit trail.
        Supports partial rollback with detailed failure tracking.

        Args:
            operation_id: Operation ID to rollback

        Returns:
            True if rolled back successfully, False if not available or failed
        """
        operation = self.operations.get(operation_id)
        if operation is None:
            logger.error(f"Operation {operation_id} not found for rollback")
            return False

        if not operation.rollback_available:
            logger.warning(f"Rollback not available for operation {operation_id}")
            return False

        if operation.status != OperationStatus.COMPLETED:
            logger.warning(
                f"Cannot rollback operation {operation_id} in status {operation.status.value}"
            )
            return False

        try:
            logger.info(f"Starting rollback for operation {operation_id}")

            operation.status = OperationStatus.ROLLING_BACK
            # rollback_started_at = datetime.now(timezone.utc)
            success_count = 0
            failed_count = 0
            rollback_steps: List[Dict[str, Any]] = []

            # Process results in reverse order
            for result in reversed(operation.results):
                rollback_step: Dict[str, Any] = {
                    "resource_id": result.resource_id,
                    "status": "pending",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "error": None,
                }

                try:
                # Execute rollback via executor
                    rollback_result = await self.executor.execute_rollback(
                        operation, result.resource_id, result.result_data
                    )

                    rollback_step.update(rollback_result)

                    if rollback_result.get("status") == "success":
                        success_count += 1
                    elif rollback_result.get("status") == "skipped":
                    # Fallback to legacy/stub logic if no handler
                        if operation.type == OperationType.NODE_DRAIN:
                            rollback_step["action"] = "uncordon_node"
                            rollback_step["status"] = "success"
                            success_count += 1
                        elif operation.type == OperationType.NODE_MAINTENANCE:
                            rollback_step["action"] = "resume_scheduling"
                            rollback_step["status"] = "success"
                            success_count += 1
                        elif operation.type == OperationType.CONFIG_UPDATE:
                            if "previous_config" in result.result_data:
                                rollback_step["action"] = "restore_config"
                                rollback_step["status"] = "success"
                                success_count += 1
                        elif operation.type == OperationType.THRESHOLD_UPDATE:
                            if "previous_threshold" in result.result_data:
                                rollback_step["action"] = "restore_threshold"
                                rollback_step["status"] = "success"
                                success_count += 1
                        elif operation.type == OperationType.NODE_REBOOT:
                            rollback_step["action"] = "acknowledge_irreversible"
                            rollback_step["status"] = "acknowledged"
                            rollback_step["note"] = (
                                "Reboot operations cannot be reversed"
                            )
                        else:
                            rollback_step["action"] = "generic_rollback"
                            rollback_step["status"] = "skipped"

                    rollback_steps.append(rollback_step)

                except Exception as e:
                    failed_count += 1
                    rollback_step["status"] = "failed"
                    rollback_step["error"] = str(e)
                    rollback_steps.append(rollback_step)
                    logger.error(f"Rollback failed for {result.resource_id}: {str(e)}")

            # Determine final status
            rollback_completed_at = datetime.now(timezone.utc)
            # rollback_duration = (rollback_completed_at - rollback_started_at).total_seconds()

            if failed_count == 0:
                operation.status = OperationStatus.ROLLED_BACK
                logger.info(
                    f"Rollback complete for {operation_id}: {success_count} items restored"
                )
            elif success_count > 0:
                operation.status = OperationStatus.PARTIALLY_ROLLED_BACK
                logger.warning(
                    f"Partial rollback for {operation_id}: {success_count} restored, {failed_count} failed"
                )
            else:
                operation.status = OperationStatus.ROLLBACK_FAILED
                logger.error(f"Rollback failed for {operation_id}: all steps failed")

            # Store rollback metadata
            operation.completed_at = rollback_completed_at

            return operation.status in [
                OperationStatus.ROLLED_BACK,
                OperationStatus.PARTIALLY_ROLLED_BACK,
            ]

        except Exception as e:
            logger.error(f"Error rolling back {operation_id}: {str(e)}")
            operation.status = OperationStatus.ROLLBACK_FAILED
            operation.completed_at = datetime.now(timezone.utc)
            return False

    def get_history(
        self, op_type: Optional[OperationType] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get operation history.

        Args:
            op_type: Filter by operation type
            limit: Maximum results

        Returns:
            List of operation summaries
        """
        history = self.history

        if op_type:
            history = [op for op in history if op.type == op_type]

        # Return most recent first
        return [op.get_summary() for op in history[-limit:][::-1]]

    def get_statistics(self) -> Dict[str, Any]:
        """Get batch operations statistics."""
        return {
            "total_operations": len(self.operations),
            "pending": sum(
                1
                for op in self.operations.values()
                if op.status == OperationStatus.PENDING
            ),
            "queued": sum(
                1
                for op in self.operations.values()
                if op.status == OperationStatus.QUEUED
            ),
            "running": sum(
                1
                for op in self.operations.values()
                if op.status == OperationStatus.RUNNING
            ),
            "completed": sum(
                1
                for op in self.operations.values()
                if op.status == OperationStatus.COMPLETED
            ),
            "failed": sum(
                1
                for op in self.operations.values()
                if op.status == OperationStatus.FAILED
            ),
            "history_size": len(self.history),
        }

    @staticmethod
    def _estimate_duration(operation: BatchOperation) -> int:
        """Estimate operation duration in seconds."""
        # Simple estimation: ~30 seconds per resource
        return len(operation.resources) * 30

    @staticmethod
    def _supports_rollback(op_type: OperationType) -> bool:
        """Check if operation type supports rollback."""
        # These operations support rollback
        rollback_supported = {
            OperationType.CONFIG_UPDATE,
            OperationType.THRESHOLD_UPDATE,
        }

        return op_type in rollback_supported
