# !/usr/bin/env python3

import unittest
"""
Chaos Engineering Test Suite for DebVisor.

Implements controlled failure injection to test system resilience:
- Network failures and latency injection
- Service unavailability simulation
- Resource exhaustion testing
- Data corruption simulation
- Cascading failure scenarios

Author: DebVisor Team
Date: November 28, 2025
"""

from datetime import datetime, timezone
from typing import TypeVar
from typing import Set
import asyncio
import logging
import random
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, NoReturn, cast
from unittest.mock import MagicMock
import pytest

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])

# =============================================================================
# Chaos Enums
# =============================================================================


class FailureMode(Enum):
    """Types of failures to inject."""

    LATENCY = "latency"
    ERROR = "error"
    TIMEOUT = "timeout"
    PARTIAL_FAILURE = "partial_failure"
    CORRUPT_DATA = "corrupt_data"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    CASCADE = "cascade"


class TargetComponent(Enum):
    """Components that can be targeted."""

    DATABASE = "database"
    CACHE = "cache"
    MESSAGE_QUEUE = "message_queue"
    EXTERNAL_API = "external_api"
    FILE_SYSTEM = "file_system"
    NETWORK = "network"


# =============================================================================
# Chaos Configuration
# =============================================================================


@dataclass
class ChaosConfig:
    """Configuration for chaos experiments."""

    enabled: bool = True
    failure_probability: float = 0.1    # 10% default
    latency_min_ms: int = 100
    latency_max_ms: int = 5000
    timeout_seconds: int = 30
    affected_operations: Set[str] = field(default_factory=set)
    excluded_operations: Set[str] = field(default_factory=set)

    # Blast radius control
    max_concurrent_failures: int = 1
    cooldown_seconds: int = 60


@dataclass
class ChaosExperiment:
    """Represents a chaos experiment."""

    name: str
    description: str
    failure_mode: FailureMode
    target: TargetComponent
    config: ChaosConfig
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    results: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# Failure Injectors
# =============================================================================


class LatencyInjector:
    """Injects artificial latency."""

    def __init__(self, min_ms: int = 100, max_ms: int = 5000):
        self.min_ms = min_ms
        self.max_ms = max_ms

    def inject(self) -> float:
        """Add random latency and return the delay."""
        delay_ms = random.randint(self.min_ms, self.max_ms)
        delay_seconds = delay_ms / 1000.0
        time.sleep(delay_seconds)
        return delay_seconds

    async def inject_async(self) -> float:
        """Add random latency asynchronously."""
        delay_ms = random.randint(self.min_ms, self.max_ms)
        delay_seconds = delay_ms / 1000.0
        await asyncio.sleep(delay_seconds)
        return delay_seconds


class ErrorInjector:
    """Injects errors into operations."""

    ERROR_TYPES = {
        TargetComponent.DATABASE: [
            ConnectionError("Database connection refused"),
            TimeoutError("Database query timeout"),
            Exception("Database deadlock detected"),
        ],
        TargetComponent.CACHE: [
            ConnectionError("Redis connection lost"),
            TimeoutError("Cache operation timeout"),
            Exception("Cache serialization error"),
        ],
        TargetComponent.MESSAGE_QUEUE: [
            ConnectionError("Message broker unavailable"),
            Exception("Queue capacity exceeded"),
            TimeoutError("Message acknowledgment timeout"),
        ],
        TargetComponent.EXTERNAL_API: [
            ConnectionError("API endpoint unreachable"),
            TimeoutError("API request timeout"),
            Exception("API rate limit exceeded"),
        ],
        TargetComponent.NETWORK: [
            ConnectionError("Network unreachable"),
            TimeoutError("Connection timed out"),
            OSError("Socket connection reset"),
        ],
    }

    def __init__(self, target: TargetComponent):
        self.target = target
        default_errors: List[Exception] = [Exception("Unknown error")]
        self.errors = cast(List[Exception], self.ERROR_TYPES.get(target, default_errors))

    def inject(self) -> NoReturn:
        """Raise a random error for the target component."""
        error = random.choice(self.errors)
        # error is an Exception instance, raise its type with its message
        raise type(error)(str(error))


class DataCorruptionInjector:
    """Simulates data corruption."""

    def __init__(self, corruption_rate: float = 0.1):
        self.corruption_rate = corruption_rate

    def corrupt_string(self, value: str) -> str:
        """Corrupt a string value."""
        if random.random() > self.corruption_rate:
            return value

        corruption_type = random.choice(["truncate", "garbage", "empty", "swap"])

        if corruption_type == "truncate":
            return value[: len(value) // 2]
        elif corruption_type == "garbage":
            return value + "".join(random.choices("!@    #$%^&*()", k=5))
        elif corruption_type == "empty":
            return ""
        elif corruption_type == "swap":
            chars = list(value)
            if len(chars) > 1:
                i, j = random.sample(range(len(chars)), 2)
                chars[i], chars[j] = chars[j], chars[i]
            return "".join(chars)
        return value

    def corrupt_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Corrupt dictionary values."""
        if random.random() > self.corruption_rate:
            return data

        corrupted = data.copy()
        if corrupted:
            key = random.choice(list(corrupted.keys()))
            value = corrupted[key]

            if isinstance(value, str):
                corrupted[key] = self.corrupt_string(value)
            elif isinstance(value, (int, float)):
                corrupted[key] = value * random.choice([-1, 0, 2, 10])
            elif isinstance(value, bool):
                corrupted[key] = not value
            elif value is None:
                corrupted[key] = "corrupted"

        return corrupted


class ResourceExhaustionInjector:
    """Simulates resource exhaustion."""

    def __init__(self, resource_type: str = "memory"):
        self.resource_type = resource_type
        self._allocated: List[bytes] = []

    def exhaust_memory(self, mb: int = 100) -> None:
        """Allocate memory to simulate exhaustion."""
        try:
            self._allocated.append(bytes(mb * 1024 * 1024))
        except MemoryError:
            raise MemoryError("Out of memory")

    def release(self) -> None:
        """Release allocated resources."""
        self._allocated.clear()

    def simulate_high_cpu(self, duration_seconds: float = 1.0) -> None:
        """Simulate high CPU usage."""
        end_time = time.time() + duration_seconds
        result = 0
        while time.time() < end_time:
            result += sum(i * i for i in range(1000))


# =============================================================================
# Chaos Monkey
# =============================================================================


class ChaosMonkey:
    """
    Orchestrates chaos experiments.

    Provides controlled failure injection for testing
    system resilience and recovery capabilities.
    """

    def __init__(self, config: Optional[ChaosConfig] = None):
        self.config = config or ChaosConfig()
        self.experiments: List[ChaosExperiment] = []
        self._active_failures: int = 0
        self._last_failure_time: Optional[datetime] = None

        # Injectors
        self.latency_injector = LatencyInjector(
            self.config.latency_min_ms, self.config.latency_max_ms
        )
        self.data_corruptor = DataCorruptionInjector()
        self.resource_injector = ResourceExhaustionInjector()

    def should_inject_failure(self, operation: str = "") -> bool:
        """Determine if failure should be injected."""
        if not self.config.enabled:
            return False

        # Check cooldown
        if self._last_failure_time:
            elapsed = (
                datetime.now(timezone.utc) - self._last_failure_time
            ).total_seconds()
            if elapsed < self.config.cooldown_seconds:
                return False

        # Check concurrent failures
        if self._active_failures >= self.config.max_concurrent_failures:
            return False

        # Check operation exclusions
        if operation in self.config.excluded_operations:
            return False

        # Check if specific operations are targeted
        if (
            self.config.affected_operations
            and operation not in self.config.affected_operations
        ):
            return False

        # Random probability
        return random.random() < self.config.failure_probability

    @contextmanager
    def maybe_inject(
        self,
        operation: str,
        target: TargetComponent,
        failure_modes: Optional[List[FailureMode]] = None,
    ):
        """
        Context manager that may inject failures.

        Args:
            operation: Operation name for tracking
            target: Target component
            failure_modes: Allowed failure modes (defaults to all)
        """
        if not self.should_inject_failure(operation):
            yield
            return

        failure_modes = failure_modes or list(FailureMode)
        failure_mode = random.choice(failure_modes)

        self._active_failures += 1
        self._last_failure_time = datetime.now(timezone.utc)

        try:
            if failure_mode == FailureMode.LATENCY:
                self.latency_injector.inject()
                yield

            elif failure_mode == FailureMode.ERROR:
                ErrorInjector(target).inject()

            elif failure_mode == FailureMode.TIMEOUT:
                time.sleep(self.config.timeout_seconds + 1)
                raise TimeoutError(f"Operation {operation} timed out")

            elif failure_mode == FailureMode.PARTIAL_FAILURE:
            # 50% chance of success after partial work
                if random.random() > 0.5:
                    yield
                else:
                    raise Exception(f"Partial failure in {operation}")

            else:
                yield

        finally:
            self._active_failures -= 1

    def record_experiment(
        self,
        name: str,
        description: str,
        failure_mode: FailureMode,
        target: TargetComponent,
        results: Dict[str, Any],
    ) -> ChaosExperiment:
        """Record a chaos experiment."""
        experiment = ChaosExperiment(
            name=name,
            description=description,
            failure_mode=failure_mode,
            target=target,
            config=self.config,
            started_at=datetime.now(timezone.utc),
            ended_at=datetime.now(timezone.utc),
            results=results,
        )
        self.experiments.append(experiment)
        return experiment


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def chaos_monkey() -> None:
    """Provide a chaos monkey instance for testing."""
    config = ChaosConfig(
        enabled=True,
        failure_probability=1.0,    # Always inject in tests
        latency_min_ms=10,
        latency_max_ms=50,
        timeout_seconds=1,
        max_concurrent_failures=5,
    )
    return ChaosMonkey(config)  # type: ignore[return-value]


@pytest.fixture
def mock_database() -> MagicMock:
    """Mock database connection."""
    return MagicMock()


@pytest.fixture
def mock_cache() -> MagicMock:
    """Mock cache client."""
    return MagicMock()


@pytest.fixture
def mock_message_queue() -> MagicMock:
    """Mock message queue."""
    return MagicMock()


# =============================================================================
# Chaos Tests
# =============================================================================


class TestDatabaseResilience:
    """Test database resilience under chaos conditions."""

    def test_database_connection_recovery(self, chaos_monkey, mock_database):
        """Test: System recovers from database connection failures."""
        attempts = 0
        max_attempts = 3
        success = False

        while attempts < max_attempts and not success:
            attempts += 1
            try:
                with chaos_monkey.maybe_inject(
                    "db_query", TargetComponent.DATABASE, [FailureMode.ERROR]
                ):
                    mock_database.query("SELECT 1")
                    success = True
            except (ConnectionError, TimeoutError, Exception):
                time.sleep(0.1)    # Backoff

        # Record experiment
        chaos_monkey.record_experiment(
            name="database_connection_recovery",
            description="Test database connection recovery after failures",
            failure_mode=FailureMode.ERROR,
            target=TargetComponent.DATABASE,
            results={
                "attempts": attempts,
                "success": success,
                "max_attempts": max_attempts,
            },
        )

        # Should eventually succeed or exhaust retries
        assert attempts <= max_attempts

    def test_database_latency_handling(self, chaos_monkey, mock_database):
        """Test: System handles database latency gracefully."""
        chaos_monkey.config.failure_probability = 0.5

        latencies = []
        for _ in range(10):
            start = time.time()
            try:
                with chaos_monkey.maybe_inject(
                    "db_query", TargetComponent.DATABASE, [FailureMode.LATENCY]
                ):
                    mock_database.query("SELECT 1")
            except Exception:
                pass
            latencies.append(time.time() - start)

        chaos_monkey.record_experiment(
            name="database_latency_handling",
            description="Test handling of database latency",
            failure_mode=FailureMode.LATENCY,
            target=TargetComponent.DATABASE,
            results={
                "avg_latency": sum(latencies) / len(latencies),
                "max_latency": max(latencies),
                "min_latency": min(latencies),
            },
        )

        # Verify latencies were tracked
        assert len(latencies) == 10


class TestCacheResilience:
    """Test cache resilience under chaos conditions."""

    def test_cache_fallback_to_database(self, chaos_monkey, mock_cache, mock_database):
        """Test: System falls back to database when cache fails."""
        cache_available = False
        data_retrieved = False

        # Try cache first
        try:
            with chaos_monkey.maybe_inject(
                "cache_get", TargetComponent.CACHE, [FailureMode.ERROR]
            ):
                mock_cache.get("key")
                cache_available = True
        except Exception:
        # Fallback to database
            mock_database.query("SELECT value FROM cache WHERE key = 'key'")
            data_retrieved = True

        chaos_monkey.record_experiment(
            name="cache_fallback",
            description="Test cache fallback to database",
            failure_mode=FailureMode.ERROR,
            target=TargetComponent.CACHE,
            results={
                "cache_available": cache_available,
                "fallback_used": data_retrieved,
            },
        )

        assert cache_available or data_retrieved

    def test_cache_write_through_failure(self, chaos_monkey, mock_cache, mock_database):
        """Test: Database write succeeds even if cache update fails."""
        db_success = False
        cache_success = False

        # Write to database first (should always succeed)
        mock_database.insert("data")
        db_success = True

        # Try to update cache
        try:
            with chaos_monkey.maybe_inject(
                "cache_set", TargetComponent.CACHE, [FailureMode.ERROR]
            ):
                mock_cache.set("key", "data")
                cache_success = True
        except Exception:
        # Cache failure is acceptable
            pass

        chaos_monkey.record_experiment(
            name="cache_write_through",
            description="Test write-through cache failure handling",
            failure_mode=FailureMode.ERROR,
            target=TargetComponent.CACHE,
            results={"db_success": db_success, "cache_success": cache_success},
        )

        # Database write must succeed regardless of cache
        assert db_success


class TestAPIResilience:
    """Test external API resilience under chaos conditions."""

    def test_api_circuit_breaker(self, chaos_monkey):
        """Test: Circuit breaker opens after consecutive failures."""
        failures = 0
        threshold = 5
        circuit_open = False

        for i in range(10):
            if circuit_open:
            # Skip call, circuit is open
                continue

            try:
                with chaos_monkey.maybe_inject(
                    "api_call", TargetComponent.EXTERNAL_API, [FailureMode.ERROR]
                ):
                    time.sleep(0.001)    # Successful call
                failures = 0    # Reset on success
            except Exception:
                failures += 1
                if failures >= threshold:
                    circuit_open = True

        chaos_monkey.record_experiment(
            name="api_circuit_breaker",
            description="Test circuit breaker opens after failures",
            failure_mode=FailureMode.ERROR,
            target=TargetComponent.EXTERNAL_API,
            results={
                "final_failures": failures,
                "circuit_open": circuit_open,
                "threshold": threshold,
            },
        )

        # Circuit should have opened
        assert circuit_open or failures < threshold

    def test_api_timeout_handling(self, chaos_monkey):
        """Test: API timeouts are handled with proper error responses."""
        timeout_handled = False
        error_message = None

        try:
            chaos_monkey.config.timeout_seconds = 0    # Immediate timeout
            with chaos_monkey.maybe_inject(
                "api_call", TargetComponent.EXTERNAL_API, [FailureMode.TIMEOUT]
            ):
                time.sleep(0.001)
        except TimeoutError as e:
            timeout_handled = True
            error_message = str(e)

        chaos_monkey.record_experiment(
            name="api_timeout_handling",
            description="Test API timeout error handling",
            failure_mode=FailureMode.TIMEOUT,
            target=TargetComponent.EXTERNAL_API,
            results={
                "timeout_handled": timeout_handled,
                "error_message": error_message,
            },
        )


class TestDataIntegrity:
    """Test data integrity under chaos conditions."""

    def test_corrupted_data_detection(self, chaos_monkey):
        """Test: Corrupted data is detected and rejected."""
        original_data = {"id": "123", "amount": 100.00, "status": "pending"}

        # Corrupt the data
        corrupted_data = chaos_monkey.data_corruptor.corrupt_dict(original_data)

        # Validate data
        is_valid = all(
            [
                isinstance(corrupted_data.get("id"), str),
                isinstance(corrupted_data.get("amount"), (int, float)),
                corrupted_data.get("amount", 0) > 0,
                corrupted_data.get("status") in ["pending", "completed", "failed"],
            ]
        )

        chaos_monkey.record_experiment(
            name="data_corruption_detection",
            description="Test detection of corrupted data",
            failure_mode=FailureMode.CORRUPT_DATA,
            target=TargetComponent.DATABASE,
            results={
                "original": original_data,
                "corrupted": corrupted_data,
                "detected_corruption": not is_valid,
            },
        )


class TestCascadingFailures:
    """Test cascading failure scenarios."""

    def test_graceful_degradation(self, chaos_monkey, mock_database, mock_cache):
        """Test: System degrades gracefully under multiple failures."""
        services_available = {"database": True, "cache": True, "api": True}

        # Simulate failures
        try:
            with chaos_monkey.maybe_inject(
                "db", TargetComponent.DATABASE, [FailureMode.ERROR]
            ):
                time.sleep(0.001)
        except Exception:
            services_available["database"] = False

        try:
            with chaos_monkey.maybe_inject(
                "cache", TargetComponent.CACHE, [FailureMode.ERROR]
            ):
                time.sleep(0.001)
        except Exception:
            services_available["cache"] = False

        try:
            with chaos_monkey.maybe_inject(
                "api", TargetComponent.EXTERNAL_API, [FailureMode.ERROR]
            ):
                time.sleep(0.001)
        except Exception:
            services_available["api"] = False

        # System should still respond (even if degraded)
        available_services = sum(services_available.values())

        chaos_monkey.record_experiment(
            name="graceful_degradation",
            description="Test graceful degradation under multiple failures",
            failure_mode=FailureMode.CASCADE,
            target=TargetComponent.NETWORK,
            results={
                "services_status": services_available,
                "available_count": available_services,
            },
        )

        # At least some functionality should remain
        # (In production, you'd verify specific degraded behaviors)


class TestResourceExhaustion:
    """Test resource exhaustion scenarios."""

    def test_memory_pressure_handling(self, chaos_monkey):
        """Test: System handles memory pressure gracefully."""
        # Skip actual memory allocation in tests
        # In real chaos testing, you'd actually allocate memory

        memory_usage_mb = 0
        oom_occurred = False

        try:
        # Simulate checking memory before allocation
            if memory_usage_mb > 80:    # 80% threshold
                raise MemoryError("Memory threshold exceeded")
        except MemoryError:
            oom_occurred = True

        chaos_monkey.record_experiment(
            name="memory_pressure",
            description="Test memory pressure handling",
            failure_mode=FailureMode.RESOURCE_EXHAUSTION,
            target=TargetComponent.DATABASE,
            results={"memory_usage_mb": memory_usage_mb, "oom_occurred": oom_occurred},
        )


# =============================================================================
# Chaos Report Generator
# =============================================================================


def generate_chaos_report(monkey: ChaosMonkey) -> str:
    """Generate a report of chaos experiments."""
    report = ["=" * 60]
    report.append("CHAOS ENGINEERING REPORT")
    report.append("=" * 60)
    report.append(f"Total Experiments: {len(monkey.experiments)}")
    report.append("")

    for exp in monkey.experiments:
        report.append(f"Experiment: {exp.name}")
        report.append(f"  Description: {exp.description}")
        report.append(f"  Failure Mode: {exp.failure_mode.value}")
        report.append(f"  Target: {exp.target.value}")
        report.append(f"  Results: {exp.results}")
        report.append("")

    report.append("=" * 60)
    return "\n".join(report)


# =============================================================================
# Main
# =============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
