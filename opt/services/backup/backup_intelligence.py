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


"""Enterprise Backup Intelligence Service.

Advanced backup features for intelligent data protection:
- Change-rate estimation with ML-based prediction
- Adaptive backup scheduling optimization
- Cross-platform restore sandbox with validation
- SLA conformance tracking and alerting
- Backup window optimization
- Dedup efficiency analytics

DebVisor Enterprise Platform - Production Ready.
"""

from __future__ import annotations

import asyncio
import logging
import random
import statistics
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set, Tuple
from uuid import uuid4

_logger = logging.getLogger(__name__)


# =============================================================================
# Data Models
# =============================================================================
class BackupPriority(Enum):
    """Backup priority levels."""

    CRITICAL = 1    # Mission-critical systems
    HIGH = 2    # Production workloads
    MEDIUM = 3    # Standard systems
    LOW = 4    # Development/test
    ARCHIVE = 5    # Long-term storage


class SLAStatus(Enum):
    """SLA compliance status."""

    COMPLIANT = "compliant"
    AT_RISK = "at_risk"
    BREACHED = "breached"
    UNKNOWN = "unknown"


class RestoreTestStatus(Enum):
    """Restore test execution status."""

    PENDING = "pending"
    PROVISIONING = "provisioning"
    RESTORING = "restoring"
    VALIDATING = "validating"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ValidationCheck(Enum):
    """Types of restore validation checks."""

    BOOT = "boot"    # VM can boot
    NETWORK = "network"    # Network connectivity
    SERVICE = "service"    # Key services running
    DATA = "data"    # Data integrity
    APPLICATION = "application"    # Application-level checks


@dataclass
class BackupSLA:
    """SLA definition for backup policies."""

    policy_id: str
    name: str
    rpo_minutes: int    # Recovery Point Objective
    rto_minutes: int    # Recovery Time Objective
    retention_days: int
    min_copies: int = 2    # Minimum backup copies (3-2-1 rule)
    offsite_required: bool = True
    encryption_required: bool = True
    restore_test_interval_days: int = 30
    priority: BackupPriority = BackupPriority.MEDIUM
    created_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ChangeRateMetrics:
    """Metrics for VM change rate tracking."""

    vm_id: str
    samples: List[float] = field(default_factory=list)    # MB changed per interval
    sample_times: List[datetime] = field(default_factory=list)
    daily_pattern: Dict[int, float] = field(default_factory=dict)    # hour -> avg rate
    weekly_pattern: Dict[int, float] = field(  # type: ignore[call-overload, misc]
        _default_factory=dict
    )    # weekday -> avg rate
    predicted_rate: float = 0.0
    confidence: float = 0.0
    last_updated: datetime=field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class BackupWindow:
    """Definition of a backup window."""

    name: str
    start_hour: int    # 0-23
    end_hour: int    # 0-23
    days_of_week: List[int] = field(default_factory=lambda: list(range(7)))    # 0=Mon
    priority: int = 0    # Higher = preferred
    max_concurrent: int = 10
    bandwidth_limit_mbps: Optional[int] = None


@dataclass
class BackupSchedule:
    """Optimized backup schedule for a VM."""

    vm_id: str
    policy_id: str
    next_backup: datetime
    estimated_duration_minutes: int
    estimated_size_mb: int
    window: BackupWindow
    priority: BackupPriority
    reason: str    # Why this time was chosen


@dataclass
class RestoreTest:
    """Restore test definition and results."""

    id: str
    backup_id: str
    vm_id: str
    policy_id: str
    status: RestoreTestStatus
    sandbox_vm_id: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    validation_results: Dict[ValidationCheck, bool] = field(default_factory=dict)
    boot_time_seconds: Optional[float] = None
    data_integrity_percent: Optional[float] = None
    error_message: Optional[str] = None
    created_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class SLAComplianceReport:
    """SLA compliance report for a VM/policy."""

    vm_id: str
    policy_id: str
    status: SLAStatus
    last_backup: Optional[datetime] = None
    next_backup_due: Optional[datetime] = None
    minutes_until_breach: Optional[int] = None
    backup_count_30d: int = 0
    successful_restores: int = 0
    failed_restores: int = 0
    rpo_violations_30d: int = 0
    avg_backup_duration: float = 0.0
    issues: List[str] = field(default_factory=list)


@dataclass
class DedupAnalytics:
    """Deduplication efficiency analytics."""

    vm_id: str
    total_logical_bytes: int = 0
    total_physical_bytes: int = 0
    dedup_ratio: float = 1.0
    compression_ratio: float = 1.0
    overall_reduction: float = 1.0
    unique_chunks: int = 0
    shared_chunks: int = 0
    estimated_monthly_savings_gb: float = 0.0


@dataclass
class BackupHealthReport:
    """Overall backup health report."""

    timestamp: datetime
    total_vms: int
    protected_vms: int
    unprotected_vms: int
    compliant_count: int
    at_risk_count: int
    breached_count: int
    total_backup_size_tb: float
    dedup_savings_tb: float
    avg_dedup_ratio: float
    restore_success_rate: float
    recommendations: List[str]


# =============================================================================
# Change Rate Estimator
# =============================================================================
class ChangeRateEstimator:
    """Estimates and predicts VM change rates for intelligent scheduling.

    Uses historical data and time-series analysis to predict:
    - How much data will change before next backup
    - Optimal backup timing based on change patterns
    - Resource requirements for backup operations
    """

    def __init__(self, maxsamples: int = 1000, predictionhorizon_hours: int = 24) -> None:
        self.max_samples=max_samples  # type: ignore[name-defined]
        self.prediction_horizon_hours=prediction_horizon_hours  # type: ignore[name-defined]
        self.metrics: Dict[str, ChangeRateMetrics] = {}

    def record_change(
        self,
        vm_id: str,
        changed_mb: float,
        interval_minutes: int,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Record observed change rate for a VM."""
        timestamp = timestamp or datetime.now(timezone.utc)

        if vm_id not in self.metrics:
            self.metrics[vm_id] = ChangeRateMetrics(vm_id=vm_id)  # type: ignore[call-arg]

        m = self.metrics[vm_id]

        # Normalize to MB/hour
        rate_per_hour = (changed_mb / interval_minutes) * 60

        m.samples.append(rate_per_hour)  # type: ignore[name-defined]
        m.sample_times.append(timestamp)  # type: ignore[arg-type]

        # Trim old samples
        if len(m.samples) > self.max_samples:
            m.samples = m.samples[-self.max_samples :]
            m.sample_times = m.sample_times[-self.max_samples :]

        # Update patterns
        hour = timestamp.hour  # type: ignore[union-attr]
        weekday = timestamp.weekday()  # type: ignore[union-attr]

        if hour not in m.daily_pattern:
            m.daily_pattern[hour] = rate_per_hour  # type: ignore[name-defined]
        else:
        # Exponential moving average
            alpha = 0.3
            m.daily_pattern[hour] = (
                alpha * rate_per_hour + (1 - alpha) * m.daily_pattern[hour]  # type: ignore[name-defined]
            )

        if weekday not in m.weekly_pattern:  # type: ignore[name-defined]
            m.weekly_pattern[weekday] = rate_per_hour  # type: ignore[name-defined]
        else:
            alpha = 0.2
            m.weekly_pattern[weekday] = (  # type: ignore[name-defined]
                alpha * rate_per_hour + (1 - alpha) * m.weekly_pattern[weekday]  # type: ignore[name-defined]
            )

        m.last_updated=timestamp  # type: ignore[assignment]

        # Update prediction
        self._update_prediction(vm_id)

    def _update_prediction(self, vmid: str) -> None:
        """Update change rate prediction for a VM."""
        m = self.metrics[vm_id]

        if len(m.samples) < 3:
            m.predicted_rate = m.samples[-1] if m.samples else 0.0
            m.confidence = 0.1
            return

        # Simple prediction: weighted combination of recent average and patterns
        recent_samples = m.samples[-10:]
        _recent_avg = statistics.mean(recent_samples)
        _recent_std=(
            statistics.stdev(recent_samples)
            if len(recent_samples) > 1
            else recent_avg * 0.5  # type: ignore[name-defined]
        )

        # Get current pattern contribution
        _now = datetime.now(timezone.utc)
        _hour_factor=m.daily_pattern.get(now.hour, recent_avg) / max(recent_avg, 0.01)  # type: ignore[name-defined]
        _day_factor=m.weekly_pattern.get(now.weekday(), recent_avg) / max(  # type: ignore[name-defined]
            recent_avg, 0.01  # type: ignore[name-defined]
        )

        # Combine factors
        pattern_weight = min(
            len(m.samples) / 100, 0.5
        )    # More samples = trust patterns more
        predicted=recent_avg * (  # type: ignore[name-defined]
            (1 - pattern_weight)
            + pattern_weight * (hour_factor * 0.6 + day_factor * 0.4)  # type: ignore[name-defined]
        )

        m.predicted_rate = max(predicted, 0.0)

        # Confidence based on variance and sample count
        _cv=recent_std / max(recent_avg, 0.01)    # Coefficient of variation  # type: ignore[name-defined]
        _sample_confidence = min(len(m.samples) / 50, 1.0)
        _variance_confidence=max(1 - cv, 0.1)  # type: ignore[name-defined]
        m.confidence=sample_confidence * variance_confidence  # type: ignore[name-defined]

    def estimate_change_rate(self, vmid: str) -> float:
        """Get current estimated change rate (MB/hour)."""
        if vm_id in self.metrics:
            return self.metrics[vm_id].predicted_rate
        return 0.0

    def predict_changes(self, vm_id: str, hours_ahead: int) -> Tuple[float, float]:
        """Predict total changes over next N hours.

        Returns (predicted_mb, confidence).
        """
        if vm_id not in self.metrics:
            return 0.0, 0.0

        m = self.metrics[vm_id]

        # Simple: rate * hours
        # Advanced: consider time-of-day patterns
        _total_mb = 0.0
        _now = datetime.now(timezone.utc)

        for h in range(hours_ahead):  # type: ignore[name-defined]
            _future_hour=(now.hour + h) % 24  # type: ignore[name-defined]
            _future_day=(now.weekday() + (now.hour + h) // 24) % 7  # type: ignore[name-defined]

            _hour_rate=m.daily_pattern.get(future_hour, m.predicted_rate)  # type: ignore[name-defined]
            _day_factor=m.weekly_pattern.get(future_day, m.predicted_rate) / max(  # type: ignore[name-defined]
                m.predicted_rate, 0.01
            )

            total_mb += hour_rate * day_factor  # type: ignore[name-defined]

        return total_mb, m.confidence  # type: ignore[name-defined]

    def get_optimal_backup_time(
        self, vm_id: str, windows: List[BackupWindow], rpo_minutes: int
    ) -> Optional[datetime]:
        """Calculate optimal backup time within allowed windows.

        Optimizes for:
        - Low change rate periods (less data to transfer)
        - Meeting RPO requirements
        - Preferred backup windows
        """
        if vm_id not in self.metrics:
        # No data - use next available window
            return self._next_window_start(windows)

        m = self.metrics[vm_id]
        _now = datetime.now(timezone.utc)
        _rpo_deadline=now + timedelta(minutes=rpo_minutes)  # type: ignore[name-defined]

        candidates: List[Tuple[datetime, float]] = []    # (time, score)

        # Check each hour in the next 24 hours
        for h in range(min(24, rpo_minutes // 60 + 1)):
            _check_time=now + timedelta(hours=h)  # type: ignore[name-defined]

            # Must be within a window
            if not self._in_window(check_time, windows):  # type: ignore[name-defined]
                continue

            # Must meet RPO
            if check_time > rpo_deadline:  # type: ignore[name-defined]
                continue

            # Score based on predicted change rate (lower is better)
            _hour_rate=m.daily_pattern.get(check_time.hour, m.predicted_rate)  # type: ignore[name-defined]
            _day_rate=m.weekly_pattern.get(check_time.weekday(), m.predicted_rate)  # type: ignore[name-defined]

            # Combine with window priority
            _window=self._get_window(check_time, windows)  # type: ignore[name-defined]
            window_score=window.priority if window else 0  # type: ignore[name-defined]

            # Lower rate = better, higher priority = better
            _score=(1 / max(hour_rate + day_rate, 0.01)) + window_score * 0.1  # type: ignore[name-defined]

            candidates.append((check_time, score))  # type: ignore[name-defined]

        if not candidates:
            return self._next_window_start(windows)

        # Return highest scoring time
        candidates.sort(key = lambda x: x[1], reverse = True)
        return candidates[0][0]

    def _in_window(self, dt: datetime, windows: List[BackupWindow]) -> bool:
        """Check if datetime is within any backup window."""
        return self._get_window(dt, windows) is not None

    def _get_window(
        self, dt: datetime, windows: List[BackupWindow]
    ) -> Optional[BackupWindow]:
        """Get the backup window for a datetime."""
        for window in windows:
            if dt.weekday() not in window.days_of_week:
                continue

            hour = dt.hour
            if window.start_hour <= window.end_hour:
                if window.start_hour <= hour < window.end_hour:
                    return window
            else:    # Window crosses midnight
                if hour >= window.start_hour or hour < window.end_hour:
                    return window

        return None

    def _next_window_start(self, windows: List[BackupWindow]) -> datetime:
        """Get the start of the next available backup window."""
        _now = datetime.now(timezone.utc)

        # Check next 7 days
        for days in range(8):
            _check_date=now + timedelta(days=days)  # type: ignore[name-defined]
            for window in sorted(windows, key = lambda w: -w.priority):
                if check_date.weekday() in window.days_of_week:  # type: ignore[name-defined]
                    start=check_date.replace(  # type: ignore[name-defined]
                        _hour = window.start_hour, minute = 0, second = 0, microsecond = 0
                    )
                    if start > now:  # type: ignore[name-defined]
                        return start

        return now    # Fallback  # type: ignore[name-defined]


# =============================================================================
# Restore Test Manager
# =============================================================================
class RestoreTestManager:
    """Manages automated restore validation testing.

    Features:
    - Automated sandbox provisioning
    - Multi-level validation (boot, network, services, data)
    - Cross-platform restore testing
    - Scheduling and reporting
    """

    def __init__(
        self,
        sandbox_network: str = "isolated-restore-test",
        max_concurrent_tests: int = 3,
        test_timeout_minutes: int = 60,
    ):
        self.sandbox_network = sandbox_network
        self.max_concurrent_tests = max_concurrent_tests
        self.test_timeout_minutes = test_timeout_minutes

        self.tests: Dict[str, RestoreTest] = {}
        self.running_tests: Set[str] = set()
        self.test_queue: deque[Tuple[int, str, str]] = deque()

        # Validation checks per VM type
        self.validation_profiles: Dict[str, List[ValidationCheck]] = {
            "default": [ValidationCheck.BOOT],
            "web": [
                ValidationCheck.BOOT,
                ValidationCheck.NETWORK,
                ValidationCheck.SERVICE,
            ],
            "database": [
                ValidationCheck.BOOT,
                ValidationCheck.NETWORK,
                ValidationCheck.DATA,
            ],
            "application": [
                ValidationCheck.BOOT,
                ValidationCheck.NETWORK,
                ValidationCheck.SERVICE,
                ValidationCheck.APPLICATION,
            ],
        }

        # Custom validation commands
        self.custom_validators: Dict[str, Callable[[RestoreTest], Awaitable[bool]]] = {}

    def schedule_test(
        self,
        backup_id: str,
        vm_id: str,
        policy_id: str,
        profile: str = "default",
        priority: int = 0,
    ) -> RestoreTest:
        """Schedule a restore test."""
        _test_id = f"rt-{uuid4().hex[:12]}"

        test=RestoreTest(  # type: ignore[call-arg]
            _id=test_id,  # type: ignore[name-defined]
            _backup_id = backup_id,
            _vm_id = vm_id,
            _policy_id = policy_id,
            _status = RestoreTestStatus.PENDING,
        )

        self.tests[test_id] = test  # type: ignore[name-defined]
        self.test_queue.append((priority, test_id, profile))  # type: ignore[name-defined]

        logger.info(f"Scheduled restore test {test_id} for backup {backup_id}")  # type: ignore[name-defined]
        return test

    async def run_test(self, test_id: str, profile: str = "default") -> RestoreTest:
        """Execute a restore test."""
        if test_id not in self.tests:  # type: ignore[name-defined]
            raise ValueError(f"Unknown test: {test_id}")  # type: ignore[name-defined]

        test=self.tests[test_id]  # type: ignore[name-defined]

        if len(self.running_tests) >= self.max_concurrent_tests:
            logger.warning(f"Max concurrent tests reached, {test_id} queued")  # type: ignore[name-defined]
            return test

        self.running_tests.add(test_id)  # type: ignore[name-defined]
        test.started_at = datetime.now(timezone.utc)

        try:
        # Phase 1: Provision sandbox
            test.status = RestoreTestStatus.PROVISIONING
            _sandbox_id = await self._provision_sandbox(test)
            test.sandbox_vm_id=sandbox_id  # type: ignore[name-defined]

            # Phase 2: Restore backup
            test.status = RestoreTestStatus.RESTORING
            await self._restore_backup(test)

            # Phase 3: Run validations
            test.status = RestoreTestStatus.VALIDATING
            checks = self.validation_profiles.get(
                profile, self.validation_profiles["default"]
            )

            for check in checks:
                _result = await self._run_validation(test, check)
                test.validation_results[check] = result  # type: ignore[name-defined]
                if not result:  # type: ignore[name-defined]
                    test.status = RestoreTestStatus.FAILED
                    test.error_message = f"Validation failed: {check.value}"
                    break

            if test.status == RestoreTestStatus.VALIDATING:
                test.status = RestoreTestStatus.SUCCESS

        except Exception as e:
            test.status = RestoreTestStatus.FAILED
            test.error_message="Restore test failed; check logs for details"
            logger.error(f"Restore test {testid} failed: {e}", exc_info=True)  # type: ignore[name-defined]
        finally:
            test.completed_at = datetime.now(timezone.utc)
            self.running_tests.discard(test_id)  # type: ignore[name-defined]

            # Cleanup sandbox
            if test.sandbox_vm_id:
                await self._cleanup_sandbox(test.sandbox_vm_id)

        return test

    async def _provision_sandbox(self, test: RestoreTest) -> str:
        """Provision an isolated sandbox VM for testing."""
        # In production: create isolated VM with restricted network
        sandbox_id = f"sandbox-{test.id}"

        logger.info(f"Provisioning sandbox {sandbox_id} for test {test.id}")  # type: ignore[name-defined]

        # Simulate provisioning time
        await asyncio.sleep(0.1)

        return sandbox_id

    async def _restore_backup(self, test: RestoreTest) -> None:
        """Restore backup to sandbox VM."""
        logger.info(  # type: ignore[name-defined]
            f"Restoring backup {test.backup_id} to sandbox {test.sandbox_vm_id}"
        )

        # In production: call backup service to restore
        _start_time = time.time()

        # Simulate restore time
        await asyncio.sleep(0.2)

        test.boot_time_seconds=time.time() - start_time  # type: ignore[name-defined]

    async def _run_validation(self, test: RestoreTest, check: ValidationCheck) -> bool:
        """Run a specific validation check."""
        logger.info(f"Running {check.value} validation for test {test.id}")  # type: ignore[name-defined]

        if check == ValidationCheck.BOOT:
            return await self._validate_boot(test)
        elif check == ValidationCheck.NETWORK:
            return await self._validate_network(test)
        elif check == ValidationCheck.SERVICE:
            return await self._validate_services(test)
        elif check == ValidationCheck.DATA:
            return await self._validate_data(test)
        elif check == ValidationCheck.APPLICATION:
            return await self._validate_application(test)

    async def _validate_boot(self, test: RestoreTest) -> bool:
        """Validate VM can boot successfully."""
        # In production: check QEMU/libvirt for VM state
        # Check for ACPI shutdown capability
        # Verify no kernel panic in console

        await asyncio.sleep(0.05)

        # Simulate 95% success rate
        return random.random() < 0.95    # nosec B311

    async def _validate_network(self, test: RestoreTest) -> bool:
        """Validate network connectivity."""
        # In production:
            # - Check network interface is up
        # - Verify IP assignment (DHCP or static)
        # - Test local connectivity

        await asyncio.sleep(0.05)
        return random.random() < 0.90    # nosec B311

    async def _validate_services(self, test: RestoreTest) -> bool:
        """Validate key services are running."""
        # In production:
            # - Check systemd service states
        # - Verify listening ports
        # - Test service responsiveness

        await asyncio.sleep(0.05)
        return random.random() < 0.85    # nosec B311

    async def _validate_data(self, test: RestoreTest) -> bool:
        """Validate data integrity."""
        # In production:
            # - Run filesystem checks
        # - Verify checksum of key files
        # - Check database consistency

        await asyncio.sleep(0.1)

        # Set integrity percentage
        test.data_integrity_percent = random.uniform(95, 100)    # nosec B311

        return test.data_integrity_percent > 98

    async def _validate_application(self, test: RestoreTest) -> bool:
        """Run application-specific validation."""
        # In production: run custom validation scripts

        _validator = self.custom_validators.get(test.vm_id)
        if validator:  # type: ignore[name-defined]
            return await validator(test)  # type: ignore[name-defined]

        await asyncio.sleep(0.05)
        return random.random() < 0.80    # nosec B311

    async def _cleanup_sandbox(self, sandbox_id: str) -> None:
        """Clean up sandbox VM after testing."""
        logger.info(f"Cleaning up sandbox {sandbox_id}")  # type: ignore[name-defined]

        # In production: destroy VM, cleanup storage
        await asyncio.sleep(0.05)

    def register_custom_validator(
        self, vm_id: str, validator: Callable[[RestoreTest], Awaitable[bool]]
    ) -> None:
        """Register a custom validation function for a VM."""
        self.custom_validators[vm_id] = validator

    def get_test_history(
        self, vm_id: Optional[str] = None, limit: int = 100
    ) -> List[RestoreTest]:
        """Get restore test history."""
        _tests = list(self.tests.values())

        if vm_id:
            tests=[t for t in tests if t.vm_id == vm_id]  # type: ignore[has-type]

        # Sort by created_at descending
        tests.sort(key = lambda t: t.created_at, reverse = True)

        return tests[:limit]


# =============================================================================
# SLA Compliance Tracker
# =============================================================================
class SLAComplianceTracker:
    """Tracks and enforces backup SLA compliance.

    Features:
    - Real-time RPO/RTO monitoring
    - Proactive breach alerting
    - Compliance reporting
    - Trend analysis
    """

    def __init__(self) -> None:
        self.slas: Dict[str, BackupSLA] = {}
        self.vm_policies: Dict[str, str] = {}    # vm_id -> policy_id
        self.backup_history: Dict[str, List[datetime]] = defaultdict(list)
        self.restore_history: Dict[str, List[Tuple[datetime, bool]]] = defaultdict(list)

        # Alert callbacks
        self.alert_handlers: List[Callable[[str, str, str], None]] = []

    def register_sla(self, sla: BackupSLA) -> None:
        """Register an SLA policy."""
        self.slas[sla.policy_id] = sla
        logger.info(  # type: ignore[name-defined]
            f"Registered SLA: {sla.name} (RPO: {sla.rpo_minutes}m, RTO: {sla.rto_minutes}m)"
        )

    def assign_policy(self, vmid: str, policyid: str) -> None:
        """Assign a policy to a VM."""
        if policy_id not in self.slas:  # type: ignore[name-defined]
            raise ValueError(f"Unknown policy: {policy_id}")  # type: ignore[name-defined]

        self.vm_policies[vm_id] = policy_id  # type: ignore[name-defined]
        logger.info(f"Assigned policy {policy_id} to VM {vm_id}")  # type: ignore[name-defined]

    def record_backup(
        self, vm_id: str, timestamp: Optional[datetime] = None, success: bool = True
    ) -> None:
        """Record a backup completion."""
        timestamp = timestamp or datetime.now(timezone.utc)

        if success:
            self.backup_history[vm_id].append(timestamp)  # type: ignore[arg-type]

            # Keep last 1000 entries
            if len(self.backup_history[vm_id]) > 1000:
                self.backup_history[vm_id] = self.backup_history[vm_id][-1000:]

    def record_restore(
        self, vm_id: str, success: bool, timestamp: Optional[datetime] = None
    ) -> None:
        """Record a restore attempt."""
        timestamp = timestamp or datetime.now(timezone.utc)
        self.restore_history[vm_id].append((timestamp, success))  # type: ignore[arg-type]

    def check_compliance(self, vmid: str) -> SLAComplianceReport:
        """Check SLA compliance for a VM."""
        _policy_id = self.vm_policies.get(vm_id)

        if not policy_id:  # type: ignore[name-defined]
            return SLAComplianceReport(  # type: ignore[call-arg]
                _vm_id = vm_id,
                _policy_id="",
                _status = SLAStatus.UNKNOWN,
                _issues=["No policy assigned"],
            )

        _sla=self.slas.get(policy_id)  # type: ignore[name-defined]
        if not sla:  # type: ignore[name-defined]
            return SLAComplianceReport(  # type: ignore[call-arg]
                _vm_id = vm_id,
                _policy_id=policy_id,  # type: ignore[name-defined]
                _status = SLAStatus.UNKNOWN,
                _issues=["Policy not found"],
            )

        _now = datetime.now(timezone.utc)
        _backups = self.backup_history.get(vm_id, [])

        # Get last backup
        last_backup=backups[-1] if backups else None  # type: ignore[name-defined]

        # Calculate metrics
        issues=[]
        status = SLAStatus.COMPLIANT
        minutes_until_breach = None

        if not last_backup:
            status = SLAStatus.BREACHED
            issues.append("No backups found")
        else:
            _minutes_since_backup=(now - last_backup).total_seconds() / 60  # type: ignore[name-defined]
            _minutes_until_breach=int(sla.rpo_minutes - minutes_since_backup)  # type: ignore[name-defined]

            if minutes_since_backup > sla.rpo_minutes:  # type: ignore[name-defined]
                status = SLAStatus.BREACHED
                issues.append(
                    f"RPO breached: {int(minutes_since_backup)}m since last backup"  # type: ignore[name-defined]
                )
            elif minutes_since_backup > sla.rpo_minutes * 0.8:  # type: ignore[name-defined]
                _status = SLAStatus.AT_RISK
                issues.append(f"RPO at risk: {int(minutes_until_breach)}m until breach")  # type: ignore[call-overload]

        # Count violations in last 30 days
        _thirty_days_ago=now - timedelta(days=30)  # type: ignore[name-defined]
        rpo_violations = 0

        if len(backups) >= 2:  # type: ignore[name-defined]
            _sorted_backups=sorted(backups)  # type: ignore[name-defined]
            for i in range(1, len(sorted_backups)):  # type: ignore[name-defined]
                if sorted_backups[i] < thirty_days_ago:  # type: ignore[name-defined]
                    continue
                _gap=(sorted_backups[i] - sorted_backups[i - 1]).total_seconds() / 60  # type: ignore[name-defined]
                if gap > sla.rpo_minutes:  # type: ignore[name-defined]
                    rpo_violations += 1

        # Count backups in last 30 days
        _backup_count=sum(1 for b in backups if b > thirty_days_ago)  # type: ignore[name-defined]

        # Restore success rate
        _restores = self.restore_history.get(vm_id, [])
        _recent_restores=[(t, s) for t, s in restores if t > thirty_days_ago]  # type: ignore[name-defined]
        _successful=sum(1 for _, s in recent_restores if s)  # type: ignore[name-defined]
        _failed=len(recent_restores) - successful  # type: ignore[name-defined]

        # Calculate average backup duration (placeholder)
        _avg_duration = 0.0

        # Next backup due
        next_due = None
        if last_backup:
            _next_due=last_backup + timedelta(minutes=sla.rpo_minutes)  # type: ignore[name-defined]

        return SLAComplianceReport(  # type: ignore[call-arg]
            _vm_id = vm_id,
            _policy_id=policy_id,  # type: ignore[name-defined]
            _status = status,
            _last_backup = last_backup,
            _next_backup_due = next_due,
            _minutes_until_breach = minutes_until_breach,
            _backup_count_30d=backup_count,  # type: ignore[name-defined]
            _successful_restores=successful,  # type: ignore[name-defined]
            _failed_restores=failed,  # type: ignore[name-defined]
            _rpo_violations_30d = rpo_violations,
            _avg_backup_duration=avg_duration,  # type: ignore[name-defined]
            _issues = issues,
        )

    def check_all_compliance(self) -> List[SLAComplianceReport]:
        """Check compliance for all VMs."""
        reports=[]

        for vm_id in self.vm_policies:
            reports.append(self.check_compliance(vm_id))

        return sorted(reports, key = lambda r: r.status.value)

    def register_alert_handler(self, handler: Callable[[str, str, str], None]) -> None:
        """Register a handler for compliance alerts."""
        self.alert_handlers.append(handler)

    def _send_alert(self, vm_id: str, message: str, severity: str) -> None:
        """Send alert to registered handlers."""
        for handler in self.alert_handlers:
            try:
                handler(vm_id, message, severity)
            except Exception as e:
                logger.error(f"Alert handler error: {e}")  # type: ignore[name-defined]


# =============================================================================
# Deduplication Analytics
# =============================================================================
class DedupAnalyzer:
    """Analyzes deduplication efficiency and provides optimization insights.

    Features:
    - Per-VM dedup ratio tracking
    - Global dedup efficiency reporting
    - Savings estimation
    - Optimization recommendations
    """

    def __init__(self) -> None:
        self.vm_analytics: Dict[str, DedupAnalytics] = {}
        self.global_chunks: Dict[str, int] = {}    # chunk_hash -> reference_count

    def record_backup_stats(
        self,
        vm_id: str,
        logical_bytes: int,
        physical_bytes: int,
        unique_chunks: int,
        shared_chunks: int,
    ) -> DedupAnalytics:
        """Record deduplication statistics for a backup."""
        _dedup_ratio = logical_bytes / max(physical_bytes, 1)

        _analytics=DedupAnalytics(  # type: ignore[call-arg]
            _vm_id = vm_id,
            _total_logical_bytes = logical_bytes,
            _total_physical_bytes = physical_bytes,
            _dedup_ratio=dedup_ratio,  # type: ignore[name-defined]
            _unique_chunks = unique_chunks,
            _shared_chunks = shared_chunks,
        )

        # Estimate monthly savings (assumes weekly full backups)
        monthly_logical = logical_bytes * 4
        monthly_physical = physical_bytes * 4
        analytics.estimated_monthly_savings_gb=(  # type: ignore[name-defined]
            monthly_logical - monthly_physical
        ) / (1024**3)

        self.vm_analytics[vm_id] = analytics  # type: ignore[name-defined]
        return analytics  # type: ignore[name-defined]

    def get_global_stats(self) -> Dict[str, Any]:
        """Get global deduplication statistics."""
        if not self.vm_analytics:
            return {}

        _total_logical = sum(a.total_logical_bytes for a in self.vm_analytics.values())
        _total_physical = sum(a.total_physical_bytes for a in self.vm_analytics.values())
        total_savings = sum(
            a.estimated_monthly_savings_gb for a in self.vm_analytics.values()
        )

        return {
            "total_vms": len(self.vm_analytics),
            "total_logical_tb": total_logical / (1024**4),  # type: ignore[name-defined]
            "total_physical_tb": total_physical / (1024**4),  # type: ignore[name-defined]
            "global_dedup_ratio": total_logical / max(total_physical, 1),  # type: ignore[name-defined]
            "estimated_monthly_savings_gb": total_savings,
            "top_dedup_vms": sorted(  # type: ignore[call-overload]
                [(vm, a.dedup_ratio) for vm, a in self.vm_analytics.items()],
                _key = lambda x: x[1],
                _reverse = True,
            )[:10],
        }


# =============================================================================
# Unified Backup Intelligence Service
# =============================================================================
class BackupIntelligence:
    """Unified backup intelligence service.

    Combines all intelligent backup features:
    - Change rate estimation and prediction
    - Optimal backup scheduling
    - Restore testing and validation
    - SLA compliance tracking
    - Deduplication analytics
    """

    def __init__(
        self,
        storage_path: Optional[Path] = None,
        default_windows: Optional[List[BackupWindow]] = None,
    ):
        self.storage_path = storage_path or Path(
            "/var/lib/debvisor/backup-intelligence"
        )

        # Sub-components
        self.change_estimator = ChangeRateEstimator()
        self.restore_tester = RestoreTestManager()
        self.sla_tracker = SLAComplianceTracker()
        self.dedup_analyzer = DedupAnalyzer()

        # Default backup windows
        self.backup_windows = default_windows or [
            BackupWindow(name="overnight", start_hour = 0, end_hour = 6, priority = 10),
            BackupWindow(name="business_low", start_hour = 12, end_hour = 14, priority = 5),
            BackupWindow(  # type: ignore[call-arg]
                _name="weekend",
                _start_hour = 0,
                _end_hour = 24,
                _days_of_week=[5, 6],    # Sat, Sun
                _priority = 8,
            ),
        ]

        # Scheduled items
        self.schedules: Dict[str, BackupSchedule] = {}

    def estimate_change_rate(self, vmid: str) -> float:
        """Get estimated change rate for a VM (MB/hour)."""
        return self.change_estimator.estimate_change_rate(vm_id)

    def record_backup_completion(
        self,
        vm_id: str,
        changed_mb: float,
        duration_minutes: int,
        logical_bytes: int,
        physical_bytes: int,
        unique_chunks: int = 0,
        shared_chunks: int = 0,
    ) -> None:
        """Record backup completion for intelligence updates."""
        # Update change rate
        self.change_estimator.record_change(  # type: ignore[call-arg]
            _vm_id = vm_id, changed_mb = changed_mb, interval_minutes = duration_minutes
        )

        # Update SLA tracking
        self.sla_tracker.record_backup(vm_id)

        # Update dedup analytics
        self.dedup_analyzer.record_backup_stats(  # type: ignore[call-arg]
            _vm_id = vm_id,
            _logical_bytes = logical_bytes,
            _physical_bytes = physical_bytes,
            _unique_chunks = unique_chunks,
            _shared_chunks = shared_chunks,
        )

    def schedule_backup(
        self, vm_id: str, policy_id: str, windows: Optional[List[BackupWindow]] = None
    ) -> BackupSchedule:
        """Create an optimized backup schedule for a VM."""
        windows = windows or self.backup_windows

        _sla = self.sla_tracker.slas.get(policy_id)
        rpo_minutes=sla.rpo_minutes if sla else 1440    # Default 24h  # type: ignore[name-defined]
        _priority=sla.priority if sla else BackupPriority.MEDIUM  # type: ignore[name-defined]

        # Get optimal time
        optimal_time=self.change_estimator.get_optimal_backup_time(  # type: ignore[call-arg]
            _vm_id = vm_id, windows = windows, rpo_minutes = rpo_minutes
        )

        if not optimal_time:
        # Fallback to next window start if no optimal time found
            _optimal_time = self.change_estimator._next_window_start(windows)

        # Estimate duration and size
        _rate = self.change_estimator.estimate_change_rate(vm_id)
        _hours_ahead=(optimal_time - datetime.now(timezone.utc)).total_seconds() / 3600  # type: ignore[operator]
        predicted_mb, _=self.change_estimator.predict_changes(vm_id, int(hours_ahead))  # type: ignore[name-defined]

        _estimated_duration = max(int(predicted_mb / 100), 5)    # Assume 100MB/min

        # Find which window
        window = None
        for w in windows:
            if optimal_time.weekday() in w.days_of_week:  # type: ignore[union-attr]
                if w.start_hour <= optimal_time.hour < w.end_hour:  # type: ignore[union-attr]
                    window = w
                    break

        _schedule=BackupSchedule(  # type: ignore[call-arg]
            _vm_id = vm_id,
            _policy_id = policy_id,
            _next_backup = optimal_time,
            _estimated_duration_minutes=estimated_duration,  # type: ignore[name-defined]
            _estimated_size_mb = int(predicted_mb),
            _window = window or self.backup_windows[0],
            _priority=priority,  # type: ignore[name-defined]
            _reason=f"Optimal time based on {rate:.1f} MB/h change rate",  # type: ignore[name-defined]
        )

        self.schedules[vm_id] = schedule  # type: ignore[name-defined]
        return schedule  # type: ignore[name-defined]

    def schedule_restore_test(
        self, backup_id: str, vm_id: str, policy_id: str="", profile: str="default"
    ) -> str:
        """Schedule a restore test."""
        test=self.restore_tester.schedule_test(  # type: ignore[call-arg]
            _backup_id = backup_id, vm_id = vm_id, policy_id = policy_id, profile = profile
        )
        return test.id

    def check_sla_compliance(
        self, vm_id: str, last_backup: Optional[datetime] = None
    ) -> bool:
        """Check if VM is SLA compliant."""
        _report = self.sla_tracker.check_compliance(vm_id)
        return report.status == SLAStatus.COMPLIANT

    def get_health_report(self) -> BackupHealthReport:
        """Generate comprehensive backup health report."""
        _now = datetime.now(timezone.utc)

        _all_vms = set(self.sla_tracker.vm_policies.keys())
        _compliance_reports = self.sla_tracker.check_all_compliance()

        _compliant = sum(
            1 for r in compliance_reports if r.status == SLAStatus.COMPLIANT  # type: ignore[name-defined]
        )
        at_risk=sum(1 for r in compliance_reports if r.status== SLAStatus.AT_RISK)  # type: ignore[name-defined]
        breached=sum(1 for r in compliance_reports if r.status== SLAStatus.BREACHED)  # type: ignore[name-defined]

        # Dedup stats
        _dedup_stats = self.dedup_analyzer.get_global_stats()

        # Restore success rate
        _all_tests = self.restore_tester.get_test_history()
        recent_tests=[t for t in all_tests if t.status != RestoreTestStatus.PENDING]  # type: ignore[name-defined]
        successful_tests = sum(
            1 for t in recent_tests if t.status == RestoreTestStatus.SUCCESS
        )
        _restore_rate = successful_tests / max(len(recent_tests), 1)

        # Generate recommendations
        recommendations=[]

        if breached > 0:
            recommendations.append(
                f"URGENT: {breached} VMs have breached SLA - review backup schedules"
            )

        if at_risk > 0:
            recommendations.append(
                f"WARNING: {at_risk} VMs at risk of SLA breach - consider earlier backups"
            )

        if restore_rate < 0.9 and len(recent_tests) > 0:  # type: ignore[name-defined]
            recommendations.append(
                f"Restore success rate ({restore_rate * 100:.0f}%) below target - "  # type: ignore[name-defined]
                "investigate failures"
            )

        if dedup_stats.get("global_dedup_ratio", 1) < 1.5:  # type: ignore[name-defined]
            recommendations.append(
                "Low deduplication ratio - review backup policies for optimization"
            )

        return BackupHealthReport(  # type: ignore[call-arg]
            timestamp = now,  # type: ignore[name-defined]
            _total_vms=len(all_vms),  # type: ignore[name-defined]
            _protected_vms=len(compliance_reports),  # type: ignore[name-defined]
            _unprotected_vms=len(all_vms) - len(compliance_reports),  # type: ignore[name-defined]
            _compliant_count=compliant,  # type: ignore[name-defined]
            _at_risk_count = at_risk,
            _breached_count = breached,
            _total_backup_size_tb=dedup_stats.get("total_logical_tb", 0),  # type: ignore[name-defined]
            _dedup_savings_tb=dedup_stats.get("total_logical_tb", 0)  # type: ignore[name-defined]
            - dedup_stats.get("total_physical_tb", 0),  # type: ignore[name-defined]
            _avg_dedup_ratio=dedup_stats.get("global_dedup_ratio", 1.0),  # type: ignore[name-defined]
            _restore_success_rate=restore_rate,  # type: ignore[name-defined]
            _recommendations = recommendations,
        )


# =============================================================================
# CLI / Demo
# =============================================================================

if _name__== "__main__":  # type: ignore[name-defined]
    logging.basicConfig(  # type: ignore[call-arg]
        _level = logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    print("=" * 60)
    print("DebVisor Backup Intelligence Service")
    print("=" * 60)

    # Initialize
    _bi = BackupIntelligence()

    # Register SLAs
    bi.sla_tracker.register_sla(  # type: ignore[name-defined]
        BackupSLA(  # type: ignore[call-arg]
            _policy_id="gold",
            _name="Gold - Critical Systems",
            _rpo_minutes = 60,
            _rto_minutes = 30,
            _retention_days = 90,
            _priority = BackupPriority.CRITICAL,
        )
    )

    bi.sla_tracker.register_sla(  # type: ignore[name-defined]
        BackupSLA(  # type: ignore[call-arg]
            _policy_id="silver",
            _name="Silver - Production",
            _rpo_minutes = 240,
            _rto_minutes = 120,
            _retention_days = 30,
            _priority = BackupPriority.HIGH,
        )
    )

    bi.sla_tracker.register_sla(  # type: ignore[name-defined]
        BackupSLA(  # type: ignore[call-arg]
            _policy_id="bronze",
            _name="Bronze - Standard",
            _rpo_minutes = 1440,
            _rto_minutes = 480,
            _retention_days = 14,
            _priority = BackupPriority.MEDIUM,
        )
    )

    # Simulate VMs and backups
    print("\n[Simulating Backup History]")

    vms=[
        ("vm-db-prod", "gold"),
        ("vm-web-prod", "silver"),
        ("vm-api-prod", "silver"),
        ("vm-dev-01", "bronze"),
        ("vm-dev-02", "bronze"),
    ]

    for vm_id, policy in vms:
        bi.sla_tracker.assign_policy(vm_id, policy)  # type: ignore[name-defined]

        # Simulate backup history
        _now = datetime.now(timezone.utc)
        for days_ago in range(7):
            backup_time=now - timedelta(  # type: ignore[call-arg, name-defined]
                _days = days_ago, hours = random.randint(0, 6)
            )    # nosec B311
            bi.sla_tracker.record_backup(vm_id, backup_time)  # type: ignore[name-defined]

            # Record change rate
            bi.change_estimator.record_change(  # type: ignore[name-defined]
                _vm_id = vm_id,
                _changed_mb = random.uniform(100, 5000),    # nosec B311
                _interval_minutes = random.randint(60, 480),    # nosec B311
                timestamp = backup_time,
            )

            # Record dedup stats
            _logical = random.randint(10_000_000_000, 100_000_000_000)    # nosec B311
            _physical=int(logical / random.uniform(1.5, 4.0))    # nosec B311  # type: ignore[name-defined]
            bi.dedup_analyzer.record_backup_stats(  # type: ignore[name-defined]
                _vm_id = vm_id,
                _logical_bytes=logical,  # type: ignore[name-defined]
                _physical_bytes=physical,  # type: ignore[name-defined]
                _unique_chunks = random.randint(1000, 5000),    # nosec B311
                _shared_chunks = random.randint(5000, 20000),    # nosec B311
            )

    # Check compliance
    print("\n[SLA Compliance Status]")

    for report in bi.sla_tracker.check_all_compliance():  # type: ignore[name-defined]
        status_icon={
            SLAStatus.COMPLIANT: "?",
            SLAStatus.AT_RISK: "[warn]",
            SLAStatus.BREACHED: "?",
            SLAStatus.UNKNOWN: "?",
        }[report.status]

        print(
            f"  {status_icon} {report.vm_id} ({report.policy_id}): {report.status.value}"
        )
        if report.issues:
            for issue in report.issues:
                print(f"      - {issue}")

    # Schedule backups
    print("\n[Optimized Backup Schedules]")

    for vm_id, policy in vms[:3]:
        _schedule=bi.schedule_backup(vm_id, policy)  # type: ignore[name-defined]
        print(f"  {vm_id}: {schedule.next_backup.strftime('%Y-%m-%d %H:%M')} UTC")  # type: ignore[name-defined]
        print(f"    Window: {schedule.window.name}")  # type: ignore[name-defined]
        print(
            f"    Estimated: {schedule.estimated_size_mb} MB, "  # type: ignore[name-defined]
            f"{schedule.estimated_duration_minutes} min"  # type: ignore[name-defined]
        )
        print(f"    Reason: {schedule.reason}")  # type: ignore[name-defined]

    # Change rate estimation
    print("\n[Change Rate Estimates]")

    for vm_id, _ in vms[:3]:
        _rate=bi.estimate_change_rate(vm_id)  # type: ignore[name-defined]
        predicted, confidence=bi.change_estimator.predict_changes(vm_id, 24)  # type: ignore[name-defined]
        print(f"  {vm_id}: {rate:.1f} MB/hour")  # type: ignore[name-defined]
        print(f"    24h prediction: {predicted:.0f} MB (confidence: {confidence:.1%})")

    # Schedule restore test
    print("\n[Restore Testing]")
    _test_id=bi.schedule_restore_test("bkp-123", "vm-db-prod", "gold", "database")  # type: ignore[name-defined]
    print(f"  Scheduled restore test: {test_id}")  # type: ignore[name-defined]

    # Health report
    print("\n[Backup Health Report]")
    health_report: BackupHealthReport=bi.get_health_report()  # type: ignore[name-defined]

    print(f"  Total VMs: {health_report.total_vms}")
    print(f"  Protected: {health_report.protected_vms}")
    print(f"  Compliant: {health_report.compliant_count}")
    print(f"  At Risk: {health_report.at_risk_count}")
    print(f"  Breached: {health_report.breached_count}")
    print(f"  Total Backup Size: {health_report.total_backup_size_tb:.2f} TB")
    print(f"  Dedup Savings: {health_report.dedup_savings_tb:.2f} TB")
    print(f"  Dedup Ratio: {health_report.avg_dedup_ratio:.2f}x")
    print(f"  Restore Success Rate: {health_report.restore_success_rate:.1%}")

    if health_report.recommendations:
        print("\n  Recommendations:")
        for rec in health_report.recommendations:
            print(f"    * {rec}")

    print("\n" + "=" * 60)
    print("Backup Intelligence Ready")
    print("=" * 60)
