#!/usr/bin/env python3
"""
Performance Testing Suite - Framework Implementation

Comprehensive performance testing including:
  - RPC latency benchmarks
  - Throughput testing
  - Scalability testing (100/1000/10000 nodes)
  - Resource utilization profiling
  - Performance regression detection
  - Load testing with concurrent operations
  - SLA validation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import time
import statistics
import json
from datetime import datetime, timezone
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


logger = logging.getLogger(__name__)


class PerformanceMetric(Enum):
    """Types of performance metrics."""
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    MEMORY = "memory"
    CPU = "cpu"
    DISK_IO = "disk_io"
    NETWORK_IO = "network_io"
    P50 = "p50"
    P95 = "p95"
    P99 = "p99"


class TestScenario(Enum):
    """Performance test scenarios."""
    LOW_LOAD = "low_load"        # 10 concurrent operations
    MEDIUM_LOAD = "medium_load"  # 100 concurrent operations
    HIGH_LOAD = "high_load"      # 1000 concurrent operations
    STRESS = "stress"            # 10000 concurrent operations
    SPIKE = "spike"              # Sudden load increase
    __test__ = False


class SLALevel(Enum):
    """SLA compliance levels."""
    GOLD = "gold"        # 99.99% uptime, <100ms p99
    SILVER = "silver"    # 99.9% uptime, <500ms p99
    BRONZE = "bronze"    # 99% uptime, <1000ms p99


@dataclass
class PerformanceResult:
    """Result of a performance measurement."""
    metric: PerformanceMetric
    value: float
    unit: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class BenchmarkRun:
    """Single benchmark execution."""
    operation: str
    scenario: TestScenario
    duration_ms: float
    iterations: int
    latencies: List[float] = field(default_factory=list)
    errors: int = 0
    throughput: float = 0.0
    memory_peak_mb: float = 0.0
    cpu_avg_percent: float = 0.0

    @property
    def p50(self) -> float:
        """50th percentile latency."""
        if not self.latencies:
            return 0.0
        return statistics.median(self.latencies)

    @property
    def p95(self) -> float:
        """95th percentile latency."""
        if not self.latencies:
            return 0.0
        sorted_latencies = sorted(self.latencies)
        index = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[index] if index < len(sorted_latencies) else 0.0

    @property
    def p99(self) -> float:
        """99th percentile latency."""
        if not self.latencies:
            return 0.0
        sorted_latencies = sorted(self.latencies)
        index = int(len(sorted_latencies) * 0.99)
        return sorted_latencies[index] if index < len(sorted_latencies) else 0.0

    @property
    def avg_latency(self) -> float:
        """Average latency."""
        if not self.latencies:
            return 0.0
        return statistics.mean(self.latencies)

    @property
    def max_latency(self) -> float:
        """Maximum latency."""
        return max(self.latencies) if self.latencies else 0.0

    @property
    def min_latency(self) -> float:
        """Minimum latency."""
        return min(self.latencies) if self.latencies else 0.0


@dataclass
class SLABenchmark:
    """SLA compliance benchmark."""
    sla_level: SLALevel
    max_p99_ms: float
    max_error_rate: float
    min_uptime: float
    results: List[BenchmarkRun] = field(default_factory=list)

    def validate(self, run: BenchmarkRun) -> bool:
        """Validate run against SLA."""
        if run.p99 > self.max_p99_ms:
            return False
        if run.errors / max(1, run.iterations) > self.max_error_rate:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "sla_level": self.sla_level.value,
            "max_p99_ms": self.max_p99_ms,
            "max_error_rate": self.max_error_rate,
            "min_uptime": self.min_uptime,
            "compliance": all(self.validate(r) for r in self.results)
        }


@dataclass
class PerformanceReport:
    """Complete performance report."""
    report_id: str
    test_name: str
    total_operations: int
    total_duration_s: float
    runs: List[BenchmarkRun]
    sla_results: List[SLABenchmark]
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def overall_throughput(self) -> float:
        """Operations per second."""
        if self.total_duration_s == 0:
            return 0.0
        return self.total_operations / self.total_duration_s

    @property
    def error_rate(self) -> float:
        """Overall error rate (0-1)."""
        total_errors = sum(r.errors for r in self.runs)
        total_ops = sum(r.iterations for r in self.runs)
        if total_ops == 0:
            return 0.0
        return total_errors / total_ops

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "report_id": self.report_id,
            "test_name": self.test_name,
            "total_operations": self.total_operations,
            "total_duration_s": self.total_duration_s,
            "overall_throughput_ops_sec": f"{self.overall_throughput:.2f}",
            "error_rate": f"{self.error_rate * 100:.2f}%",
            "run_count": len(self.runs),
            "sla_results": [s.to_dict() for s in self.sla_results],
            "generated_at": self.generated_at.isoformat(),
        }


class RPCLatencyBenchmark:
    """RPC latency benchmarking."""

    @staticmethod
    def benchmark_operation(
        operation: Callable,
        iterations: int,
        scenario: TestScenario
    ) -> BenchmarkRun:
        """Benchmark an operation."""
        latencies: List[float] = []
        errors = 0
        start_time = time.time()

        for _ in range(iterations):
            try:
                op_start = time.time()
                operation()
                op_end = time.time()
                latencies.append((op_end - op_start) * 1000)  # Convert to ms
            except Exception as e:
                logger.error(f"Operation error: {e}")
                errors += 1

        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000
        throughput = iterations / (duration_ms / 1000) if duration_ms > 0 else 0

        return BenchmarkRun(
            operation="rpc_call",
            scenario=scenario,
            duration_ms=duration_ms,
            iterations=iterations,
            latencies=latencies,
            errors=errors,
            throughput=throughput
        )


class ThroughputBenchmark:
    """Throughput testing."""

    @staticmethod
    def benchmark_concurrent(
        operation: Callable,
        concurrent_count: int,
        scenario: TestScenario,
        duration_seconds: float = 10.0
    ) -> BenchmarkRun:
        """Benchmark throughput with concurrent operations."""
        latencies: List[float] = []
        errors = 0
        operations_completed = 0

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=concurrent_count) as executor:
            futures = []

            while time.time() - start_time < duration_seconds:
                futures.append(executor.submit(operation))

            for future in as_completed(futures):
                try:
                    op_start = time.time()
                    result = future.result(timeout=5)
                    op_end = time.time()
                    latencies.append((op_end - op_start) * 1000)
                    operations_completed += 1
                except Exception as e:
                    logger.error(f"Concurrent operation error: {e}")
                    errors += 1

        duration_ms = (time.time() - start_time) * 1000
        throughput = operations_completed / (duration_ms / 1000) if duration_ms > 0 else 0

        return BenchmarkRun(
            operation="concurrent_ops",
            scenario=scenario,
            duration_ms=duration_ms,
            iterations=operations_completed,
            latencies=latencies,
            errors=errors,
            throughput=throughput
        )


class ScalabilityBenchmark:
    """Scalability testing (horizontal scaling)."""

    SCALE_LEVELS = [10, 100, 1000, 10000]

    @staticmethod
    def benchmark_scalability(
        operation: Callable,
        node_counts: Optional[List[int]] = None
    ) -> List[BenchmarkRun]:
        """Benchmark scalability at different node counts."""
        if node_counts is None:
            node_counts = ScalabilityBenchmark.SCALE_LEVELS

        results: List[BenchmarkRun] = []

        for node_count in node_counts:
            logger.info(f"Testing with {node_count} nodes...")

            run = BenchmarkRun(
                operation=f"nodes_{node_count}",
                scenario=TestScenario.MEDIUM_LOAD,
                duration_ms=0,
                iterations=100,
                latencies=[],
                throughput=0
            )

            # Simulate operations at scale
            for _ in range(100):
                try:
                    start = time.time()
                    operation()
                    latency = (time.time() - start) * 1000
                    run.latencies.append(latency)
                except Exception as e:
                    logger.error(f"Scale test error: {e}")
                    run.errors += 1

            results.append(run)

        return results


class ResourceProfilingBenchmark:
    """Resource utilization profiling."""

    @staticmethod
    def profile_operation(
        operation: Callable,
        iterations: int = 1000
    ) -> BenchmarkRun:
        """Profile resource usage of an operation."""
        latencies: List[float] = []
        memory_samples: List[float] = []
        cpu_samples: List[float] = []

        start_time = time.time()

        for _ in range(iterations):
            try:
                op_start = time.time()
                operation()
                op_end = time.time()
                latencies.append((op_end - op_start) * 1000)

                # Simulate resource monitoring
                # In production, would use psutil
                memory_samples.append(50.0)  # Mock data
                cpu_samples.append(25.0)     # Mock data
            except Exception as e:
                logger.error(f"Profile error: {e}")

        duration_ms = (time.time() - start_time) * 1000

        return BenchmarkRun(
            operation="profiled",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=duration_ms,
            iterations=iterations,
            latencies=latencies,
            memory_peak_mb=max(memory_samples) if memory_samples else 0,
            cpu_avg_percent=statistics.mean(cpu_samples) if cpu_samples else 0
        )


class PerformanceTestingFramework:
    """Main performance testing framework."""

    SLA_BENCHMARKS = {
        SLALevel.GOLD: SLABenchmark(
            sla_level=SLALevel.GOLD,
            max_p99_ms=100.0,
            max_error_rate=0.0001,  # 0.01%
            min_uptime=0.9999
        ),
        SLALevel.SILVER: SLABenchmark(
            sla_level=SLALevel.SILVER,
            max_p99_ms=500.0,
            max_error_rate=0.001,   # 0.1%
            min_uptime=0.999
        ),
        SLALevel.BRONZE: SLABenchmark(
            sla_level=SLALevel.BRONZE,
            max_p99_ms=1000.0,
            max_error_rate=0.01,    # 1%
            min_uptime=0.99
        ),
    }

    def __init__(self):
        """Initialize framework."""
        self.results: List[BenchmarkRun] = []
        self.start_time = None

    def benchmark_latency(
        self,
        operation: Callable,
        iterations: int = 1000,
        scenario: TestScenario = TestScenario.MEDIUM_LOAD
    ) -> BenchmarkRun:
        """Benchmark latency."""
        logger.info(f"Benchmarking latency with {iterations} iterations...")
        result = RPCLatencyBenchmark.benchmark_operation(
            operation, iterations, scenario
        )
        self.results.append(result)
        return result

    def benchmark_throughput(
        self,
        operation: Callable,
        concurrent_count: int = 10,
        scenario: TestScenario = TestScenario.MEDIUM_LOAD
    ) -> BenchmarkRun:
        """Benchmark throughput."""
        logger.info(f"Benchmarking throughput with {concurrent_count} concurrent...")
        result = ThroughputBenchmark.benchmark_concurrent(
            operation, concurrent_count, scenario
        )
        self.results.append(result)
        return result

    def benchmark_scalability(
        self,
        operation: Callable,
        node_counts: Optional[List[int]] = None
    ) -> List[BenchmarkRun]:
        """Benchmark scalability."""
        logger.info("Benchmarking scalability...")
        results = ScalabilityBenchmark.benchmark_scalability(
            operation, node_counts
        )
        self.results.extend(results)
        return results

    def profile_resources(
        self,
        operation: Callable,
        iterations: int = 1000
    ) -> BenchmarkRun:
        """Profile resource usage."""
        logger.info("Profiling resource usage...")
        result = ResourceProfilingBenchmark.profile_operation(
            operation, iterations
        )
        self.results.append(result)
        return result

    def validate_sla(
        self,
        sla_level: SLALevel = SLALevel.SILVER
    ) -> SLABenchmark:
        """Validate SLA compliance."""
        sla = self.SLA_BENCHMARKS[sla_level]
        sla.results = self.results
        return sla

    def generate_report(self, test_name: str) -> PerformanceReport:
        """Generate performance report."""
        total_operations = sum(r.iterations for r in self.results)
        total_duration = sum(r.duration_ms for r in self.results) / 1000

        sla_results = []
        for level in SLALevel:
            sla = self.SLA_BENCHMARKS[level]
            sla.results = self.results
            sla_results.append(sla)

        report_id = f"perf-{datetime.now(timezone.utc).timestamp()}"

        return PerformanceReport(
            report_id=report_id,
            test_name=test_name,
            total_operations=total_operations,
            total_duration_s=total_duration,
            runs=self.results,
            sla_results=sla_results
        )

    def to_json(self, report: PerformanceReport) -> str:
        """Convert report to JSON."""
        return json.dumps(report.to_dict(), indent=2)
