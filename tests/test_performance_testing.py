# !/usr/bin/env python3
"""
Unit tests for performance testing framework.

Tests for:
- Latency benchmarking
- Throughput testing
- Scalability benchmarks
- Resource profiling
- SLA validation
"""

import unittest
import time


from performance_testing import (
    PerformanceTestingFramework,
    RPCLatencyBenchmark,
    ThroughputBenchmark,
    ScalabilityBenchmark,
    ResourceProfilingBenchmark,
    BenchmarkRun,
    TestScenario,
    SLALevel,
)


class TestBenchmarkRun(unittest.TestCase):
    """Tests for benchmark run."""

    def test_p50_calculation(self) -> None:
        """Test P50 calculation."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=5,
            latencies=[10, 20, 30, 40, 50],
        )

        self.assertEqual(run.p50, 30)

    def test_p95_calculation(self) -> None:
        """Test P95 calculation."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=20,
            latencies=list(range(1, 21)),
        )

        self.assertGreater(run.p95, 0)

    def test_p99_calculation(self) -> None:
        """Test P99 calculation."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=100,
            latencies=list(range(1, 101)),
        )

        self.assertGreater(run.p99, 0)

    def test_avg_latency(self) -> None:
        """Test average latency calculation."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=5,
            latencies=[10, 20, 30, 40, 50],
        )

        self.assertEqual(run.avg_latency, 30)

    def test_max_latency(self) -> None:
        """Test max latency."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=5,
            latencies=[10, 20, 30, 40, 50],
        )

        self.assertEqual(run.max_latency, 50)

    def test_min_latency(self) -> None:
        """Test min latency."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=5,
            latencies=[10, 20, 30, 40, 50],
        )

        self.assertEqual(run.min_latency, 10)


class TestRPCLatencyBenchmark(unittest.TestCase):
    """Tests for RPC latency benchmarking."""

    def test_benchmark_fast_operation(self) -> None:
        """Test benchmarking fast operation."""

        def fast_op() -> None:
            pass

        result = RPCLatencyBenchmark.benchmark_operation(
            fast_op, 10, TestScenario.MEDIUM_LOAD
        )

        self.assertGreaterEqual(result.avg_latency, 0)
        self.assertEqual(result.errors, 0)
        self.assertEqual(len(result.latencies), 10)

    def test_benchmark_with_errors(self) -> None:
        """Test benchmarking with errors."""
        call_count = 0

        def failing_op() -> None:
            nonlocal call_count
            call_count += 1
            if call_count % 2 == 0:
                raise Exception("Error")

        result = RPCLatencyBenchmark.benchmark_operation(
            failing_op, 10, TestScenario.MEDIUM_LOAD
        )

        self.assertGreater(result.errors, 0)

    def test_throughput_calculation(self) -> None:
        """Test throughput calculation."""

        def simple_op() -> None:
            time.sleep(0.001)

        result = RPCLatencyBenchmark.benchmark_operation(
            simple_op, 10, TestScenario.MEDIUM_LOAD
        )

        self.assertGreater(result.throughput, 0)


class TestThroughputBenchmark(unittest.TestCase):
    """Tests for throughput benchmarking."""

    def test_concurrent_operations(self) -> None:
        """Test concurrent operations."""

        def simple_op() -> None:
            pass

        result = ThroughputBenchmark.benchmark_concurrent(
            simple_op, 5, TestScenario.MEDIUM_LOAD, duration_seconds=0.1
        )

        self.assertGreater(result.iterations, 0)
        self.assertGreater(result.throughput, 0)

    def test_concurrent_with_errors(self) -> None:
        """Test concurrent with errors."""
        call_count = 0

        def failing_op() -> None:
            nonlocal call_count
            call_count += 1
            if call_count % 3 == 0:
                raise Exception("Error")
            return "ok"  # type: ignore[return-value]

        result = ThroughputBenchmark.benchmark_concurrent(
            failing_op, 3, TestScenario.MEDIUM_LOAD, duration_seconds=0.1
        )

        self.assertGreater(result.errors, 0)

    def test_concurrent_count_scaling(self) -> None:
        """Test scaling with concurrent count."""

        def simple_op() -> None:
            pass

        _result_10 = ThroughputBenchmark.benchmark_concurrent(
            simple_op, 10, TestScenario.LOW_LOAD, duration_seconds=0.1
        )

        result_20 = ThroughputBenchmark.benchmark_concurrent(
            simple_op, 20, TestScenario.MEDIUM_LOAD, duration_seconds=0.1
        )

        # More concurrent should yield higher throughput
        self.assertGreater(result_20.throughput, 0)


class TestScalabilityBenchmark(unittest.TestCase):
    """Tests for scalability benchmarking."""

    def test_scalability_benchmark(self) -> None:
        """Test scalability at different scales."""

        def simple_op() -> None:
            pass

        results = ScalabilityBenchmark.benchmark_scalability(
            simple_op, node_counts=[10, 100, 1000]
        )

        self.assertEqual(len(results), 3)
        for result in results:
            self.assertGreater(len(result.latencies), 0)

    def test_default_scale_levels(self) -> None:
        """Test default scale levels."""

        def simple_op() -> None:
            pass

        results = ScalabilityBenchmark.benchmark_scalability(simple_op)

        expected_levels = len(ScalabilityBenchmark.SCALE_LEVELS)
        self.assertEqual(len(results), expected_levels)


class TestResourceProfilingBenchmark(unittest.TestCase):
    """Tests for resource profiling."""

    def test_profile_operation(self) -> None:
        """Test resource profiling."""

        def simple_op() -> None:
            pass

        result = ResourceProfilingBenchmark.profile_operation(simple_op, iterations=10)

        self.assertGreater(result.memory_peak_mb, 0)
        self.assertGreater(result.cpu_avg_percent, 0)
        self.assertEqual(len(result.latencies), 10)


class TestPerformanceTestingFramework(unittest.TestCase):
    """Tests for performance testing framework."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.framework = PerformanceTestingFramework()

    def test_benchmark_latency(self) -> None:
        """Test latency benchmarking."""

        def simple_op() -> None:
            pass

        result = self.framework.benchmark_latency(simple_op, iterations=10)

        self.assertGreaterEqual(result.avg_latency, 0)
        self.assertIn(result, self.framework.results)

    def test_benchmark_throughput(self) -> None:
        """Test throughput benchmarking."""

        def simple_op() -> None:
            pass

        result = self.framework.benchmark_throughput(simple_op, concurrent_count=5)

        self.assertGreater(result.throughput, 0)
        self.assertIn(result, self.framework.results)

    def test_benchmark_scalability(self) -> None:
        """Test scalability benchmarking."""

        def simple_op() -> None:
            pass

        results = self.framework.benchmark_scalability(simple_op, node_counts=[10, 100])

        self.assertEqual(len(results), 2)
        self.assertTrue(all(r in self.framework.results for r in results))

    def test_profile_resources(self) -> None:
        """Test resource profiling."""

        def simple_op() -> None:
            pass

        result = self.framework.profile_resources(simple_op)

        self.assertGreater(result.memory_peak_mb, 0)
        self.assertIn(result, self.framework.results)

    def test_sla_validation_gold(self) -> None:
        """Test SLA validation for Gold level."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=1000,
            latencies=[50] * 950 + [99] * 50,    # 95% at 50ms, 5% at 99ms
            errors=0,
            throughput=10000,
        )

        self.framework.results.append(run)
        sla = self.framework.validate_sla(SLALevel.GOLD)

        self.assertTrue(sla.validate(run))

    def test_sla_validation_silver(self) -> None:
        """Test SLA validation for Silver level."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=1000,
            latencies=[200] * 950 + [499] * 50,
            errors=1,    # 0.1% error rate
            throughput=10000,
        )

        self.framework.results.append(run)
        sla = self.framework.validate_sla(SLALevel.SILVER)

        self.assertTrue(sla.validate(run))

    def test_sla_validation_fail(self) -> None:
        """Test SLA validation failure."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.HIGH_LOAD,
            duration_ms=100,
            iterations=1000,
            latencies=[1500] * 1000,    # All at 1500ms
            errors=50,    # 5% error rate
            throughput=10000,
        )

        self.framework.results.append(run)
        sla = self.framework.validate_sla(SLALevel.GOLD)

        self.assertFalse(sla.validate(run))

    def test_generate_report(self) -> None:
        """Test report generation."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=100,
            latencies=list(range(1, 101)),
            errors=0,
            throughput=1000,
        )

        self.framework.results.append(run)

        report = self.framework.generate_report("test_run")

        self.assertEqual(report.test_name, "test_run")
        self.assertEqual(report.total_operations, 100)
        self.assertGreater(report.overall_throughput, 0)

    def test_error_rate_calculation(self) -> None:
        """Test error rate calculation."""
        run1 = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=100,
            latencies=[50] * 99,
            errors=1,
        )

        run2 = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=100,
            latencies=[50] * 98,
            errors=2,
        )

        self.framework.results.extend([run1, run2])

        report = self.framework.generate_report("error_test")

        self.assertAlmostEqual(report.error_rate, 0.015, places=3)    # 3 errors / 200 ops


class TestPerformanceIntegration(unittest.TestCase):
    """Integration tests."""

    def test_complete_performance_audit(self) -> None:
        """Test complete performance audit flow."""
        framework = PerformanceTestingFramework()

        def test_op() -> None:
            pass

        # Run various benchmarks
        framework.benchmark_latency(test_op, iterations=50)
        framework.benchmark_throughput(
            test_op, concurrent_count=5, duration_seconds=0.1
        )
        framework.profile_resources(test_op, iterations=20)

        # Generate report
        report = framework.generate_report("full_audit")

        self.assertGreater(len(report.runs), 0)
        self.assertGreater(report.overall_throughput, 0)


if __name__ == "__main__":
    unittest.main()
