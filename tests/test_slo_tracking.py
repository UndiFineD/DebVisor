# !/usr/bin/env python3
"""
Tests for SLO Tracking Framework.

Tests SLI recording, SLO target validation, error budget management,
and alerting functionality.

Author: DebVisor Team
Date: November 28, 2025
"""

import asyncio
import pytest
from datetime import datetime, timedelta, timezone

from services.slo_tracking import (
    SLIType,
    SLOTarget,
    SLIRecord,
    SLOViolation,
    ErrorBudget,
    SLOTracker,
    track_latency_sli,
    track_availability_sli,
)

# =============================================================================
# SLI Type Tests
# =============================================================================


class TestSLIType:
    """Test suite for SLI types."""

    def test_all_sli_types_exist(self) -> None:
        """All expected SLI types should exist."""
        assert hasattr(SLIType, "LATENCY")
        assert hasattr(SLIType, "AVAILABILITY")
        assert hasattr(SLIType, "ERROR_RATE")
        assert hasattr(SLIType, "THROUGHPUT")

    def test_sli_type_values(self) -> None:
        """SLI type values should be correct."""
        assert SLIType.LATENCY.value == "latency"
        assert SLIType.AVAILABILITY.value == "availability"
        assert SLIType.ERROR_RATE.value == "error_rate"
        assert SLIType.THROUGHPUT.value == "throughput"


# =============================================================================
# SLO Target Tests
# =============================================================================


class TestSLOTarget:
    """Test suite for SLO targets."""

    def test_target_creation(self) -> None:
        """Should create SLO target correctly."""
        target = SLOTarget(
            name="api-latency",
            sli_type=SLIType.LATENCY,
            target_value=200.0,
            threshold_type="max",
            window_hours=24,
            burn_rate_threshold=2.0,
        )

        assert target.name == "api-latency"
        assert target.sli_type == SLIType.LATENCY
        assert target.target_value == 200.0
        assert target.threshold_type == "max"
        assert target.window_hours == 24
        assert target.burn_rate_threshold == 2.0

    def test_target_with_percentile(self) -> None:
        """Should create target with percentile."""
        target = SLOTarget(
            name="api-latency-p99",
            sli_type=SLIType.LATENCY,
            target_value=500.0,
            threshold_type="percentile",
            percentile=99,
        )

        assert target.percentile == 99


# =============================================================================
# SLI Record Tests
# =============================================================================


class TestSLIRecord:
    """Test suite for SLI records."""

    def test_record_creation(self) -> None:
        """Should create SLI record correctly."""
        now = datetime.now(timezone.utc)
        record = SLIRecord(
            sli_type=SLIType.LATENCY,
            service="api-gateway",
            operation="get_user",
            value=150.0,
            timestamp=now,
            success=True,
            metadata={"endpoint": "/users/{id}"},
        )

        assert record.sli_type == SLIType.LATENCY
        assert record.service == "api-gateway"
        assert record.value == 150.0
        assert record.success is True
        assert record.metadata["endpoint"] == "/users/{id}"

    def test_record_auto_timestamp(self) -> None:
        """Should auto-generate timestamp if not provided."""
        record = SLIRecord(
            sli_type=SLIType.AVAILABILITY,
            service="test",
            operation="test",
            value=1.0,
            success=True,
        )

        assert record.timestamp is not None
        assert isinstance(record.timestamp, datetime)


# =============================================================================
# SLO Violation Tests
# =============================================================================


class TestSLOViolation:
    """Test suite for SLO violations."""

    def test_violation_creation(self) -> None:
        """Should create violation record correctly."""
        target = SLOTarget(
            name="test-target", sli_type=SLIType.LATENCY, target_value=200.0
        )

        violation = SLOViolation(
            target=target,
            actual_value=350.0,
            expected_value=200.0,
            severity="critical",
            message="Latency exceeded target",
        )

        assert violation.target.name == "test-target"
        assert violation.actual_value == 350.0
        assert violation.severity.value == "critical"    # Compare enum value


# =============================================================================
# Error Budget Tests
# =============================================================================


class TestErrorBudget:
    """Test suite for Error Budget management."""

    def test_budget_creation(self) -> None:
        """Should create error budget correctly."""
        budget = ErrorBudget(
            service="api", slo_target=99.9, window_hours=720    # 30 days
        )

        assert budget.service == "api"
        assert budget.slo_target == 99.0
        assert abs(budget.total_budget - 0.01) < 0.0001    # Float precision

    def test_budget_consumption(self) -> None:
        """Should track budget consumption."""
        budget = ErrorBudget(service="api", slo_target=99.0, window_hours=24)

        # Consume some budget
        budget.consume(0.005)    # 0.5%

        assert budget.consumed == 0.005
        assert budget.remaining == 0.005    # 1% - 0.5%
        assert budget.remaining_percentage == 50.0

    def test_budget_exhausted(self) -> None:
        """Should detect exhausted budget."""
        budget = ErrorBudget(service="api", slo_target=99.0, window_hours=24)

        budget.consume(0.01)    # Consume entire 1% budget

        assert budget.is_exhausted
        assert budget.remaining == 0.0

    def test_burn_rate_calculation(self) -> None:
        """Should calculate burn rate correctly."""
        budget = ErrorBudget(service="api", slo_target=99.0, window_hours=24)

        # Consume half budget in 6 hours (25% of window)
        # If 50% consumed in 25% of time, burn rate = 2.0
        budget.consumed = 0.005
        budget.window_start = datetime.now(timezone.utc) - timedelta(hours=6)

        burn_rate = budget.current_burn_rate
        # Burn rate should be around 2.0 (burning 2x faster than allowed)
        assert 1.5 < burn_rate < 2.5

    def test_budget_reset(self) -> None:
        """Should reset budget."""
        budget = ErrorBudget(service="api", slo_target=99.0, window_hours=24)

        budget.consume(0.005)
        budget.reset()

        assert budget.consumed == 0.0
        assert budget.remaining_percentage == 100.0


# =============================================================================
# SLO Tracker Tests
# =============================================================================


class TestSLOTracker:
    """Test suite for SLO Tracker."""

    @pytest.fixture
    def tracker(self) -> None:
        """Create SLO tracker for testing."""
        return SLOTracker(service="test-service")

    def test_register_target(self, tracker):
        """Should register SLO target."""
        target = SLOTarget(
            name="test-latency", sli_type=SLIType.LATENCY, target_value=200.0
        )

        tracker.register_target(target)

        assert "test-latency" in tracker.targets

    def test_record_sli(self, tracker):
        """Should record SLI measurement."""
        # Register target first
        target = SLOTarget(
            name="test-latency", sli_type=SLIType.LATENCY, target_value=200.0
        )
        tracker.register_target(target)

        # Record SLI
        record = tracker.record(
            sli_type=SLIType.LATENCY, operation="test_op", value=150.0, success=True
        )

        assert record.value == 150.0
        assert record.sli_type == SLIType.LATENCY

    def test_check_compliance(self, tracker):
        """Should check SLO compliance."""
        target = SLOTarget(
            name="test-latency",
            sli_type=SLIType.LATENCY,
            target_value=200.0,
            threshold_type="max",
        )
        tracker.register_target(target)

        # Record compliant values
        for _ in range(10):
            tracker.record(
                sli_type=SLIType.LATENCY, operation="test_op", value=150.0, success=True
            )

        compliance = tracker.check_compliance("test-latency")

        assert compliance is not None
        assert compliance.target_name == "test-latency"
        assert compliance.compliant is True

    def test_detect_violation(self, tracker):
        """Should detect SLO violations."""
        target = SLOTarget(
            name="test-latency",
            sli_type=SLIType.LATENCY,
            target_value=200.0,
            threshold_type="max",
        )
        tracker.register_target(target)

        # Record violating values
        for _ in range(10):
            tracker.record(
                sli_type=SLIType.LATENCY,
                operation="test_op",
                value=500.0,    # Above target
                success=True,
            )

        compliance = tracker.check_compliance("test-latency")

        assert compliance is not None
        assert compliance.compliant is False

    def test_get_summary(self, tracker):
        """Should generate summary report."""
        target = SLOTarget(
            name="test-latency", sli_type=SLIType.LATENCY, target_value=200.0
        )
        tracker.register_target(target)

        for i in range(10):
            tracker.record(
                sli_type=SLIType.LATENCY,
                operation="test_op",
                value=100.0 + i * 10,
                success=True,
            )

        summary = tracker.get_summary()

        # Service key is "test-service" from fixture
        assert "test-service" in summary
        assert "targets" in summary["test-service"]
        assert "test-latency" in summary["test-service"]["targets"]


# =============================================================================
# Decorator Tests
# =============================================================================


class TestSLIDecorators:
    """Test suite for SLI tracking decorators."""

    @pytest.mark.asyncio
    async def test_track_latency_sli(self) -> None:
        """track_latency_sli should measure function execution time."""
        tracker = SLOTracker(service="test")
        target = SLOTarget(
            name="op-latency", sli_type=SLIType.LATENCY, target_value=1000.0
        )
        tracker.register_target(target)

        @track_latency_sli(tracker, "test_operation")
        async def slow_function() -> str:
            await asyncio.sleep(0.01)
            return "done"
        result = await slow_function()

        assert result == "done"
        # Verify SLI was recorded
        assert len(tracker.records) > 0
        record = tracker.records[0]
        assert record.sli_type == SLIType.LATENCY
        assert record.value > 0    # Should have measured time

    @pytest.mark.asyncio
    async def test_track_availability_sli(self) -> None:
        """track_availability_sli should track success/failure."""
        tracker = SLOTracker(service="test")
        target = SLOTarget(
            name="op-availability", sli_type=SLIType.AVAILABILITY, target_value=99.0
        )
        tracker.register_target(target)

        @track_availability_sli(tracker, "test_operation")
        async def successful_function() -> str:
            return "success"

        result = await successful_function()

        assert result == "success"
        assert len(tracker.records) > 0
        record = tracker.records[0]
        assert record.sli_type == SLIType.AVAILABILITY
        assert record.value == 1.0    # Success
        assert record.success is True

    @pytest.mark.asyncio
    async def test_track_availability_on_failure(self) -> None:
        """track_availability_sli should record failure."""
        tracker = SLOTracker(service="test")

        @track_availability_sli(tracker, "test_operation")
        async def failing_function() -> None:
            raise ValueError("test error")

        with pytest.raises(ValueError):
            await failing_function()

        assert len(tracker.records) > 0
        record = tracker.records[0]
        assert record.sli_type == SLIType.AVAILABILITY
        assert record.value == 0.0    # Failure
        assert record.success is False


# =============================================================================
# Integration Tests
# =============================================================================


class TestSLOIntegration:
    """Integration tests for SLO tracking."""

    @pytest.mark.asyncio
    async def test_full_slo_workflow(self) -> None:
        """Test complete SLO tracking workflow."""
        # Create tracker
        tracker = SLOTracker(service="api-gateway")

        # Register multiple targets
        tracker.register_target(
            SLOTarget(
                name="latency-p99",
                sli_type=SLIType.LATENCY,
                target_value=200.0,
                threshold_type="percentile",
                percentile=99,
            )
        )

        tracker.register_target(
            SLOTarget(
                name="availability",
                sli_type=SLIType.AVAILABILITY,
                target_value=99.9,
                threshold_type="min",
            )
        )

        # Simulate some traffic
        for i in range(100):
        # Most requests are fast
            latency = 50.0 if i < 95 else 500.0    # 5% slow
            success = i < 98    # 2% failures

            tracker.record(
                sli_type=SLIType.LATENCY,
                operation="get_user",
                value=latency,
                success=True,
            )

            tracker.record(
                sli_type=SLIType.AVAILABILITY,
                operation="get_user",
                value=1.0 if success else 0.0,
                success=success,
            )

        # Check compliance
        _latency_compliance = tracker.check_compliance("latency-p99")
        _availability_compliance = tracker.check_compliance("availability")

        # Get overall summary
        summary = tracker.get_summary()

        assert summary["service"] == "api-gateway"
        assert "targets" in summary
        assert len(tracker.records) == 200    # 100 latency + 100 availability


# =============================================================================
# Main
# =============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
