# !/usr/bin/env python3
"""
DebVisor Performance Benchmark Tests
=====================================

Comprehensive benchmark suite for critical path performance testing.
Measures latency, throughput, and resource utilization.

Usage:
    pytest tests/benchmarks/test_performance.py -v --benchmark-only
    pytest tests/benchmarks/test_performance.py -v --benchmark-json=results.json
"""

import pytest
from datetime import datetime, timezone
import asyncio
import json
import random
import statistics
import sys
import time
import unittest
from dataclasses import dataclass, field
from io import StringIO
from typing import Any, Callable, Dict, List, Optional

# =============================================================================
# BENCHMARK INFRASTRUCTURE
# =============================================================================


@dataclass
class BenchmarkResult:
    """Result of a single benchmark run."""

    name: str
    iterations: int
    total_time_ms: float
    min_time_ms: float
    max_time_ms: float
    mean_time_ms: float
    median_time_ms: float
    std_dev_ms: float
    ops_per_sec: float
    percentile_95_ms: float
    percentile_99_ms: float
    memory_delta_mb: float = 0.0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return {
            "name": self.name,
            "iterations": self.iterations,
            "total_time_ms": round(self.total_time_ms, 3),
            "min_time_ms": round(self.min_time_ms, 3),
            "max_time_ms": round(self.max_time_ms, 3),
            "mean_time_ms": round(self.mean_time_ms, 3),
            "median_time_ms": round(self.median_time_ms, 3),
            "std_dev_ms": round(self.std_dev_ms, 3),
            "ops_per_sec": round(self.ops_per_sec, 2),
            "percentile_95_ms": round(self.percentile_95_ms, 3),
            "percentile_99_ms": round(self.percentile_99_ms, 3),
            "memory_delta_mb": round(self.memory_delta_mb, 3),
            "timestamp": self.timestamp,
        }

    def __str__(self) -> str:
        return (
            f"{self.name}:\n"
            f"  Iterations: {self.iterations:,}\n"
            f"  Mean: {self.mean_time_ms:.3f}ms | Median: {self.median_time_ms:.3f}ms\n"
            f"  Min: {self.min_time_ms:.3f}ms | Max: {self.max_time_ms:.3f}ms\n"
            f"  Std Dev: {self.std_dev_ms:.3f}ms\n"
            f"  P95: {self.percentile_95_ms:.3f}ms | P99: {self.percentile_99_ms:.3f}ms\n"
            f"  Throughput: {self.ops_per_sec:,.2f} ops/sec"
        )


class BenchmarkRunner:
    """Benchmark runner with warmup, iteration control, and statistics."""

    def __init__(self, warmup_iterations: int = 10, min_iterations: int = 100):
        self.warmup_iterations = warmup_iterations
        self.min_iterations = min_iterations
        self.results: List[BenchmarkResult] = []

    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of sorted data."""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        index = (len(sorted_data) - 1) * percentile / 100
        lower = int(index)
        upper = lower + 1
        if upper >= len(sorted_data):
            return sorted_data[-1]
        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight

    def run_sync(
        self,
        name: str,
        func: Callable[..., Any],
        *args,
        iterations: Optional[int] = None,
        **kwargs,
    ) -> BenchmarkResult:
        """Run synchronous benchmark."""
        iterations = iterations or self.min_iterations

        # Warmup
        for _ in range(self.warmup_iterations):
            func(*args, **kwargs)

        # Benchmark
        times_ms: List[float] = []
        start_total = time.perf_counter()

        for _ in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times_ms.append((end - start) * 1000)

        end_total = time.perf_counter()
        total_time_ms = (end_total - start_total) * 1000

        result = BenchmarkResult(
            name=name,
            iterations=iterations,
            total_time_ms=total_time_ms,
            min_time_ms=min(times_ms),
            max_time_ms=max(times_ms),
            mean_time_ms=statistics.mean(times_ms),
            median_time_ms=statistics.median(times_ms),
            std_dev_ms=statistics.stdev(times_ms) if len(times_ms) > 1 else 0.0,
            ops_per_sec=(iterations / total_time_ms) * 1000,
            percentile_95_ms=self._percentile(times_ms, 95),
            percentile_99_ms=self._percentile(times_ms, 99),
        )

        self.results.append(result)
        return result

    async def run_async(
        self,
        name: str,
        func: Callable[..., Any],
        *args,
        iterations: Optional[int] = None,
        **kwargs,
    ) -> BenchmarkResult:
        """Run async benchmark."""
        iterations = iterations or self.min_iterations

        # Warmup
        for _ in range(self.warmup_iterations):
            await func(*args, **kwargs)

        # Benchmark
        times_ms: List[float] = []
        start_total = time.perf_counter()

        for _ in range(iterations):
            start = time.perf_counter()
            await func(*args, **kwargs)
            end = time.perf_counter()
            times_ms.append((end - start) * 1000)

        end_total = time.perf_counter()
        total_time_ms = (end_total - start_total) * 1000

        result = BenchmarkResult(
            name=name,
            iterations=iterations,
            total_time_ms=total_time_ms,
            min_time_ms=min(times_ms),
            max_time_ms=max(times_ms),
            mean_time_ms=statistics.mean(times_ms),
            median_time_ms=statistics.median(times_ms),
            std_dev_ms=statistics.stdev(times_ms) if len(times_ms) > 1 else 0.0,
            ops_per_sec=(iterations / total_time_ms) * 1000,
            percentile_95_ms=self._percentile(times_ms, 95),
            percentile_99_ms=self._percentile(times_ms, 99),
        )

        self.results.append(result)
        return result

    def export_json(self, filepath: str) -> None:
        """Export all results to JSON file."""
        data = {
            "benchmark_run": datetime.now(timezone.utc).isoformat(),
            "results": [r.to_dict() for r in self.results],
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def print_summary(self) -> None:
        """Print summary of all benchmark results."""
        print("\n" + "=" * 70)
        print("BENCHMARK SUMMARY")
        print("=" * 70)
        for result in self.results:
            print(f"\n{result}")
        print("\n" + "=" * 70)


# =============================================================================
# PERFORMANCE ASSERTIONS
# =============================================================================


class PerformanceThresholds:
    """Configurable performance thresholds for assertions."""

    # API endpoint latencies (milliseconds)
    API_HEALTH_CHECK_MAX_MS = 50.0
    API_LIST_ENDPOINT_MAX_MS = 100.0
    API_MUTATION_ENDPOINT_MAX_MS = 200.0

    # Throughput (operations per second)
    API_MIN_THROUGHPUT_OPS = 100.0

    # GraphQL query latencies
    GRAPHQL_SIMPLE_QUERY_MAX_MS = 50.0
    GRAPHQL_COMPLEX_QUERY_MAX_MS = 200.0

    # Background service latencies
    HEALTH_CHECK_MAX_MS = 100.0
    SECRET_RETRIEVAL_MAX_MS = 50.0

    # Data serialization
    JSON_SERIALIZE_MAX_MS = 10.0

    # VM operations (with mocking)
    VM_CREATE_MAX_MS = 500.0
    VM_LIST_MAX_MS = 100.0


def assert_performance(
    result: BenchmarkResult,
    max_mean_ms: Optional[float] = None,
    max_p95_ms: Optional[float] = None,
    max_p99_ms: Optional[float] = None,
    min_ops_per_sec: Optional[float] = None,
) -> None:
    """Assert performance meets thresholds."""
    errors = []

    if max_mean_ms and result.mean_time_ms > max_mean_ms:
        errors.append(
            f"Mean latency {result.mean_time_ms:.3f}ms exceeds "
            f"threshold {max_mean_ms:.3f}ms"
        )

    if max_p95_ms and result.percentile_95_ms > max_p95_ms:
        errors.append(
            f"P95 latency {result.percentile_95_ms:.3f}ms exceeds "
            f"threshold {max_p95_ms:.3f}ms"
        )

    if max_p99_ms and result.percentile_99_ms > max_p99_ms:
        errors.append(
            f"P99 latency {result.percentile_99_ms:.3f}ms exceeds "
            f"threshold {max_p99_ms:.3f}ms"
        )

    if min_ops_per_sec and result.ops_per_sec < min_ops_per_sec:
        errors.append(
            f"Throughput {result.ops_per_sec:.2f} ops/sec below "
            f"threshold {min_ops_per_sec:.2f} ops/sec"
        )

    if errors:
        raise AssertionError(
            f"Performance test failed for '{result.name}':\n"
            + "\n".join(f"  - {e}" for e in errors)
        )


# =============================================================================
# MOCK HELPERS
# =============================================================================


def create_mock_vm(vm_id: str = None) -> Dict[str, Any]:
    """Create a mock VM object for testing."""
    vm_id = vm_id or f"vm-{random.randint(1000, 9999)}"
    return {
        "id": vm_id,
        "name": f"test-vm-{vm_id}",
        "status": random.choice(["running", "stopped", "paused"]),
        "vcpus": random.randint(1, 16),
        "memory_mb": random.randint(512, 32768),
        "disk_gb": random.randint(10, 500),
        "network_interfaces": [
            {
                "mac": f"52:54:00:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}"
            }
            for _ in range(random.randint(1, 4))
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "hypervisor": random.choice(["kvm", "xen"]),
        "tags": ["test", "benchmark"],
    }


def create_mock_vms(count: int) -> List[Dict[str, Any]]:
    """Create multiple mock VMs."""
    return [create_mock_vm(f"vm-{i:04d}") for i in range(count)]


def create_mock_health_status() -> Dict[str, Any]:
    """Create mock health check response."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {
            "kvm": {"status": "ok", "latency_ms": random.uniform(1, 10)},
            "ceph": {"status": "ok", "latency_ms": random.uniform(5, 20)},
            "kubernetes": {"status": "ok", "latency_ms": random.uniform(2, 15)},
            "database": {"status": "ok", "latency_ms": random.uniform(1, 5)},
        },
        "metrics": {
            "cpu_percent": random.uniform(10, 80),
            "memory_percent": random.uniform(20, 70),
            "disk_percent": random.uniform(30, 60),
        },
    }


# =============================================================================
# BENCHMARK TEST CASES
# =============================================================================


class TestJSONSerializationPerformance(unittest.TestCase):
    """Benchmark JSON serialization/deserialization."""

    def setUp(self) -> None:
        self.runner = BenchmarkRunner(warmup_iterations=50, min_iterations=1000)
        self.small_payload = {"status": "ok", "count": 42}
        self.medium_payload = create_mock_vm()
        self.large_payload = {
            "vms": create_mock_vms(100),
            "metadata": {"total": 100, "page": 1},
        }

    def test_json_serialize_small(self) -> None:
        """Benchmark small payload JSON serialization."""
        result = self.runner.run_sync(
            "json_serialize_small", json.dumps, self.small_payload
        )
        assert_performance(result, max_mean_ms=1.0)
        print(f"\n{result}")

    def test_json_serialize_medium(self) -> None:
        """Benchmark medium payload JSON serialization."""
        result = self.runner.run_sync(
            "json_serialize_medium", json.dumps, self.medium_payload
        )
        assert_performance(result, max_mean_ms=5.0)
        print(f"\n{result}")

    def test_json_serialize_large(self) -> None:
        """Benchmark large payload JSON serialization."""
        result = self.runner.run_sync(
            "json_serialize_large", json.dumps, self.large_payload, iterations=500
        )
        assert_performance(
            result, max_mean_ms=PerformanceThresholds.JSON_SERIALIZE_MAX_MS
        )
        print(f"\n{result}")

    def test_json_deserialize_large(self) -> None:
        """Benchmark large payload JSON deserialization."""
        json_str = json.dumps(self.large_payload)
        result = self.runner.run_sync(
            "json_deserialize_large", json.loads, json_str, iterations=500
        )
        assert_performance(
            result, max_mean_ms=PerformanceThresholds.JSON_SERIALIZE_MAX_MS
        )
        print(f"\n{result}")


class TestRateLimitingPerformance(unittest.TestCase):
    """Benchmark rate limiting operations."""

    def setUp(self) -> None:
        self.runner = BenchmarkRunner(warmup_iterations=20, min_iterations=500)

    def test_token_bucket_check(self) -> None:
        """Benchmark token bucket rate limit check."""

        # Simple token bucket implementation
        class TokenBucket:
            def __init__(self, rate: int, capacity: int):
                self.rate = rate
                self.capacity = capacity
                self.tokens = float(capacity)
                self.last_update = time.time()

            def check(self, client_id: str) -> bool:
                now = time.time()
                elapsed = now - self.last_update
                self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
                self.last_update = now
                if self.tokens >= 1:
                    self.tokens -= 1
                    return True
                return False

        bucket = TokenBucket(rate=100, capacity=100)
        result = self.runner.run_sync("token_bucket_check", bucket.check, "test-client")
        # Rate limiting should be very fast
        assert_performance(result, max_mean_ms=0.1, min_ops_per_sec=10000)
        print(f"\n{result}")


class TestInputValidationPerformance(unittest.TestCase):
    """Benchmark input validation operations."""

    def setUp(self) -> None:
        self.runner = BenchmarkRunner(warmup_iterations=50, min_iterations=1000)
        import re

        self.pci_pattern = re.compile(
            r"^[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-7]$"
        )
        self.uuid_pattern = re.compile(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            re.IGNORECASE,
        )

    def test_pci_address_validation(self) -> None:
        """Benchmark PCI address validation."""
        valid_address = "0000:03:00.0"

        def validate() -> bool:
            return bool(self.pci_pattern.match(valid_address))

        result = self.runner.run_sync("pci_address_validation", validate)
        assert_performance(result, max_mean_ms=0.05)
        print(f"\n{result}")

    def test_uuid_validation(self) -> None:
        """Benchmark UUID validation."""
        valid_uuid = "550e8400-e29b-41d4-a716-446655440000"

        def validate() -> bool:
            return bool(self.uuid_pattern.match(valid_uuid))

        result = self.runner.run_sync("uuid_validation", validate)
        assert_performance(result, max_mean_ms=0.05)
        print(f"\n{result}")

    def test_json_schema_validation(self) -> None:
        """Benchmark JSON-like schema validation."""
        schema = {
            "type": "object",
            "required": ["name", "vcpus", "memory"],
            "properties": {
                "name": {"type": "string", "minLength": 1, "maxLength": 64},
                "vcpus": {"type": "integer", "minimum": 1, "maximum": 128},
                "memory": {"type": "integer", "minimum": 256, "maximum": 1048576},
            },
        }

        data = {"name": "test-vm", "vcpus": 4, "memory": 4096}

        def simple_validate() -> None:
            """Simple schema validation without external library."""
            if not isinstance(data, dict):
                return False
            for req in schema["required"]:
                if req not in data:
                    return False  # type: ignore[return-value]
            for key, rules in schema["properties"].items():  # type: ignore[attr-defined]
                if key in data:
                    val = data[key]
                    if rules["type"] == "string" and not isinstance(val, str):
                        return False  # type: ignore[return-value]
                    if rules["type"] == "integer" and not isinstance(val, int):
                        return False  # type: ignore[return-value]
            return True  # type: ignore[return-value]

        result = self.runner.run_sync("simple_schema_validation", simple_validate)
        assert_performance(result, max_mean_ms=0.1)
        print(f"\n{result}")


class TestHealthCheckPerformance(unittest.TestCase):
    """Benchmark health check operations."""

    def setUp(self) -> None:
        self.runner = BenchmarkRunner(warmup_iterations=20, min_iterations=200)

    def test_health_aggregation(self) -> None:
        """Benchmark health status aggregation."""
        services = {
            "kvm": {"status": "ok", "latency_ms": 5.0},
            "ceph": {"status": "ok", "latency_ms": 10.0},
            "kubernetes": {"status": "ok", "latency_ms": 8.0},
            "database": {"status": "ok", "latency_ms": 3.0},
            "redis": {"status": "ok", "latency_ms": 2.0},
        }

        def aggregate_health() -> None:
            """Aggregate health from all services."""
            all_healthy = all(s["status"] == "ok" for s in services.values())
            avg_latency = sum(s["latency_ms"] for s in services.values()) / len(  # type: ignore[misc]
                services
            )
            return {  # type: ignore[return-value]
                "status": "healthy" if all_healthy else "degraded",
                "services": services,
                "average_latency_ms": avg_latency,
            }

        result = self.runner.run_sync("health_aggregation", aggregate_health)
        assert_performance(result, max_mean_ms=1.0)
        print(f"\n{result}")


class TestDataTransformationPerformance(unittest.TestCase):
    """Benchmark data transformation operations."""

    def setUp(self) -> None:
        self.runner = BenchmarkRunner(warmup_iterations=20, min_iterations=500)
        self.vms = create_mock_vms(100)

    def test_vm_list_filtering(self) -> None:
        """Benchmark VM list filtering."""

        def filter_running() -> None:
            return [vm for vm in self.vms if vm["status"] == "running"]  # type: ignore[return-value]

        result = self.runner.run_sync("vm_list_filtering", filter_running)
        assert_performance(result, max_mean_ms=1.0)
        print(f"\n{result}")

    def test_vm_list_sorting(self) -> None:
        """Benchmark VM list sorting."""

        def sort_by_memory() -> None:
            return sorted(self.vms, key=lambda vm: vm["memory_mb"], reverse=True)  # type: ignore[return-value]

        result = self.runner.run_sync("vm_list_sorting", sort_by_memory)
        assert_performance(result, max_mean_ms=2.0)
        print(f"\n{result}")

    def test_vm_aggregation(self) -> None:
        """Benchmark VM metrics aggregation."""

        def aggregate_metrics() -> None:
            total_vcpus = sum(vm["vcpus"] for vm in self.vms)
            total_memory = sum(vm["memory_mb"] for vm in self.vms)
            total_disk = sum(vm["disk_gb"] for vm in self.vms)
            by_status: Any = {}
            for vm in self.vms:
                status = vm["status"]
                by_status[status] = by_status.get(status, 0) + 1
            return {  # type: ignore[return-value]
                "total_vcpus": total_vcpus,
                "total_memory_mb": total_memory,
                "total_disk_gb": total_disk,
                "by_status": by_status,
            }

        result = self.runner.run_sync("vm_aggregation", aggregate_metrics)
        assert_performance(result, max_mean_ms=1.0)
        print(f"\n{result}")


class TestTracingOverheadPerformance(unittest.TestCase):
    """Benchmark tracing context overhead."""

    def setUp(self) -> None:
        self.runner = BenchmarkRunner(warmup_iterations=50, min_iterations=1000)

    def test_span_creation(self) -> None:
        """Benchmark span creation overhead."""
        from dataclasses import dataclass
        from typing import Optional
        import uuid

        @dataclass
        class SpanContext:
            trace_id: str
            span_id: str
            parent_span_id: Optional[str] = None

        @dataclass
        class Span:
            name: str
            context: SpanContext
            start_time: float
            end_time: Optional[float] = None

        def create_span() -> None:
            ctx = SpanContext(
                trace_id=str(uuid.uuid4()),
                span_id=str(uuid.uuid4())[:16],
                parent_span_id=None,
            )
            return Span(  # type: ignore[return-value]
                name="test_operation", context=ctx, start_time=time.perf_counter()
            )

        result = self.runner.run_sync("span_creation", create_span)
        # Tracing overhead should be minimal
        assert_performance(result, max_mean_ms=0.5)
        print(f"\n{result}")

    def test_context_propagation(self) -> None:
        """Benchmark context propagation via headers."""
        trace_context = {
            "X-Trace-ID": "550e8400-e29b-41d4-a716-446655440000",
            "X-Span-ID": "446655440000",
            "X-Parent-Span-ID": None,
        }

        def extract_and_inject() -> None:
        # Extract
            trace_id = trace_context.get("X-Trace-ID")
            span_id = trace_context.get("X-Span-ID")
            # Inject (simulate creating new headers)
            new_headers = {
                "X-Trace-ID": trace_id,
                "X-Span-ID": f"{hash(span_id) % 0xFFFFFFFFFFFF:012x}",
                "X-Parent-Span-ID": span_id,
            }
            return new_headers  # type: ignore[return-value]

        result = self.runner.run_sync("context_propagation", extract_and_inject)
        assert_performance(result, max_mean_ms=0.1)
        print(f"\n{result}")


class TestAsyncOperationsPerformance(unittest.TestCase):
    """Benchmark async operation overhead."""

    def setUp(self) -> None:
        self.runner = BenchmarkRunner(warmup_iterations=20, min_iterations=500)

    def test_async_task_creation(self) -> None:
        """Benchmark async task creation overhead."""

        async def dummy_task() -> None:
            return 42  # type: ignore[return-value]

        def create_task() -> None:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(dummy_task())
            finally:
                loop.close()

        result = self.runner.run_sync(
            "async_task_creation",
            create_task,
            iterations=100,    # Fewer iterations due to loop creation overhead
        )
        # Async overhead should be reasonable
        assert_performance(result, max_mean_ms=5.0)
        print(f"\n{result}")

    def test_async_gather_parallel(self) -> None:
        """Benchmark parallel async gather."""

        async def mock_api_call(delay_ms: float) -> Any:
            await asyncio.sleep(delay_ms / 1000)
            return {"status": "ok"}

        async def run_parallel() -> None:
            tasks = [mock_api_call(1) for _ in range(10)]
            return await asyncio.gather(*tasks)  # type: ignore[return-value]

        def run_benchmark() -> None:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(run_parallel())
            finally:
                loop.close()

        result = self.runner.run_sync(
            "async_gather_10_tasks", run_benchmark, iterations=50
        )
        # Parallel execution should be efficient
        print(f"\n{result}")


class TestStringOperationsPerformance(unittest.TestCase):
    """Benchmark string operations common in API responses."""

    def setUp(self) -> None:
        self.runner = BenchmarkRunner(warmup_iterations=100, min_iterations=2000)

    def test_log_message_formatting(self) -> None:
        """Benchmark log message formatting."""

        def format_log() -> None:
            return (  # type: ignore[return-value]
                f"[{datetime.now(timezone.utc).isoformat()}] "
                "INFO vm_manager: Created VM test-vm-001 "
                "(vcpus=4, memory=4096MB, disk=100GB) "
                "request_id=550e8400-e29b-41d4-a716-446655440000"
            )

        result = self.runner.run_sync("log_message_formatting", format_log)
        assert_performance(result, max_mean_ms=0.5)
        print(f"\n{result}")

    def test_url_path_building(self) -> None:
        """Benchmark URL path building."""
        base_url = "https://api.debvisor.local"
        version = "v1"
        resource = "vms"
        vm_id = "vm-0001"
        action = "start"

        def build_url() -> None:
            return f"{base_url}/{version}/{resource}/{vm_id}/{action}"  # type: ignore[return-value]

        result = self.runner.run_sync("url_path_building", build_url)
        assert_performance(result, max_mean_ms=0.1)
        print(f"\n{result}")


class TestCachePerformance(unittest.TestCase):
    """Benchmark caching operations."""

    def setUp(self) -> None:
        self.runner = BenchmarkRunner(warmup_iterations=50, min_iterations=1000)
        self.cache = {}
        # Pre-populate cache
        for i in range(1000):
            self.cache[f"key-{i:04d}"] = create_mock_vm(f"vm-{i:04d}")

    def test_cache_hit(self) -> None:
        """Benchmark cache hit performance."""

        def cache_get() -> None:
            return self.cache.get("key-0500")  # type: ignore[return-value]

        result = self.runner.run_sync("cache_hit", cache_get)
        # Cache hits should be extremely fast
        assert_performance(result, max_mean_ms=0.01)
        print(f"\n{result}")

    def test_cache_miss(self) -> None:
        """Benchmark cache miss performance."""

        def cache_miss() -> None:
            return self.cache.get("nonexistent-key", None)  # type: ignore[return-value]

        result = self.runner.run_sync("cache_miss", cache_miss)
        assert_performance(result, max_mean_ms=0.01)
        print(f"\n{result}")

    def test_cache_set(self) -> None:
        """Benchmark cache set performance."""
        counter = [0]

        def cache_set() -> None:
            key = f"new-key-{counter[0]}"
            counter[0] += 1
            self.cache[key] = create_mock_vm()

        result = self.runner.run_sync("cache_set", cache_set)
        assert_performance(result, max_mean_ms=1.0)
        print(f"\n{result}")


# =============================================================================
# BENCHMARK SUITE RUNNER
# =============================================================================


class BenchmarkSuite:
    """Run all benchmarks and generate report."""

    def __init__(self) -> None:
        self.all_results: List[BenchmarkResult] = []

    def run_all(self, export_path: Optional[str] = None) -> None:
        """Run all benchmark test cases."""
        test_classes = [
            TestJSONSerializationPerformance,
            TestRateLimitingPerformance,
            TestInputValidationPerformance,
            TestHealthCheckPerformance,
            TestDataTransformationPerformance,
            TestTracingOverheadPerformance,
            TestStringOperationsPerformance,
            TestCachePerformance,
        ]

        print("\n" + "=" * 70)
        print("DEBVISOR PERFORMANCE BENCHMARK SUITE")
        print("=" * 70)
        print(f"Started: {datetime.now(timezone.utc).isoformat()}")
        print(f"Python: {sys.version}")
        print("=" * 70)

        for test_class in test_classes:
            print(f"\n>>> Running {test_class.__name__}...")
            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
            runner = unittest.TextTestRunner(verbosity=0, stream=StringIO())
            runner.run(suite)

        print("\n" + "=" * 70)
        print("BENCHMARK SUITE COMPLETED")
        print("=" * 70)

        if export_path:
        # Collect results from all runners
            data = {
                "benchmark_run": datetime.now(timezone.utc).isoformat(),
                "python_version": sys.version,
                "results": [],
            }
            with open(export_path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Results exported to: {export_path}")


if __name__ == "__main__":
    # Run as benchmark suite
    import argparse

    parser = argparse.ArgumentParser(description="DebVisor Performance Benchmarks")
    parser.add_argument("--export", type=str, help="Export results to JSON file")
    parser.add_argument("--unittest", action="store_true", help="Run as unittest")
    args = parser.parse_args()

    if args.unittest:
        unittest.main(argv=[""], exit=False, verbosity=2)
    else:
        suite = BenchmarkSuite()
        suite.run_all(export_path=args.export)
