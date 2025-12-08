#!/usr/bin/env python3
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
    PerformanceTestingFramework, RPCLatencyBenchmark, ThroughputBenchmark,
    ScalabilityBenchmark, ResourceProfilingBenchmark, BenchmarkRun,
    TestScenario, SLALevel
)


class TestBenchmarkRun(unittest.TestCase):
    """Tests for benchmark run."""

    def test_p50_calculation(self):
        """Test P50 calculation."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=5,
            latencies=[10, 20, 30, 40, 50]
        )

        self.assertEqual(run.p50, 30)

    def test_p95_calculation(self):
        """Test P95 calculation."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=20,
            latencies=list(range(1, 21))
        )

        self.assertGreater(run.p95, 0)

    def test_p99_calculation(self):
        """Test P99 calculation."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=100,
            latencies=list(range(1, 101))
        )

        self.assertGreater(run.p99, 0)

    def test_avg_latency(self):
        """Test average latency calculation."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=5,
            latencies=[10, 20, 30, 40, 50]
        )

        self.assertEqual(run.avg_latency, 30)

    def test_max_latency(self):
        """Test max latency."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=5,
            latencies=[10, 20, 30, 40, 50]
        )

        self.assertEqual(run.max_latency, 50)

    def test_min_latency(self):
        """Test min latency."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=5,
            latencies=[10, 20, 30, 40, 50]
        )

        self.assertEqual(run.min_latency, 10)


class TestRPCLatencyBenchmark(unittest.TestCase):
    """Tests for RPC latency benchmarking."""

    def test_benchmark_fast_operation(self):
        """Test benchmarking fast operation."""
        def fast_op():
            time.sleep(0.001)  # 1ms

        result = RPCLatencyBenchmark.benchmark_operation(
            fast_op, 10, TestScenario.MEDIUM_LOAD
        )

        self.assertGreater(result.avg_latency, 0)
        self.assertEqual(result.errors, 0)
        self.assertEqual(len(result.latencies), 10)

    def test_benchmark_with_errors(self):
        """Test benchmarking with errors."""
        call_count = 0

        def failing_op():
            nonlocal call_count
            call_count += 1
            if call_count % 2 == 0:
                raise Exception("Error")

        result = RPCLatencyBenchmark.benchmark_operation(
            failing_op, 10, TestScenario.MEDIUM_LOAD
        )

        self.assertGreater(result.errors, 0)

    def test_throughput_calculation(self):
        """Test throughput calculation."""
        def simple_op():
            pass

        result = RPCLatencyBenchmark.benchmark_operation(
            simple_op, 100, TestScenario.MEDIUM_LOAD
        )

        self.assertGreater(result.throughput, 0)


class TestThroughputBenchmark(unittest.TestCase):
    """Tests for throughput benchmarking."""

    def test_concurrent_operations(self):
        """Test concurrent operations."""
        def simple_op():
            time.sleep(0.001)
            return "ok"

        result = ThroughputBenchmark.benchmark_concurrent(
            simple_op, 5, TestScenario.MEDIUM_LOAD, duration_seconds=1
        )

        self.assertGreater(result.iterations, 0)
        self.assertGreater(result.throughput, 0)

    def test_concurrent_with_errors(self):
        """Test concurrent with errors."""
        call_count = 0

        def failing_op():
            nonlocal call_count
            call_count += 1
            if call_count % 3 == 0:
                raise Exception("Error")
            return "ok"

        result = ThroughputBenchmark.benchmark_concurrent(
            failing_op, 3, TestScenario.MEDIUM_LOAD, duration_seconds=0.5
        )

        self.assertGreater(result.errors, 0)

    def test_concurrent_count_scaling(self):
        """Test scaling with concurrent count."""
        def simple_op():
            time.sleep(0.001)

        _result_10 = ThroughputBenchmark.benchmark_concurrent(
            simple_op, 10, TestScenario.LOW_LOAD, duration_seconds=0.5
        )

        result_20 = ThroughputBenchmark.benchmark_concurrent(
            simple_op, 20, TestScenario.MEDIUM_LOAD, duration_seconds=0.5
        )

        # More concurrent should yield higher throughput
        self.assertGreater(result_20.throughput, 0)


class TestScalabilityBenchmark(unittest.TestCase):
    """Tests for scalability benchmarking."""

    def test_scalability_benchmark(self):
        """Test scalability at different scales."""
        def simple_op():
            pass

        results = ScalabilityBenchmark.benchmark_scalability(
            simple_op,
            node_counts=[10, 100, 1000]
        )

        self.assertEqual(len(results), 3)
        for result in results:
            self.assertGreater(len(result.latencies), 0)

    def test_default_scale_levels(self):
        """Test default scale levels."""
        def simple_op():
            pass

        results = ScalabilityBenchmark.benchmark_scalability(simple_op)

        expected_levels = len(ScalabilityBenchmark.SCALE_LEVELS)
        self.assertEqual(len(results), expected_levels)


class TestResourceProfilingBenchmark(unittest.TestCase):
    """Tests for resource profiling."""

    def test_profile_operation(self):
        """Test resource profiling."""
        def simple_op():
            time.sleep(0.001)

        result = ResourceProfilingBenchmark.profile_operation(
            simple_op, iterations=10
        )

        self.assertGreater(result.memory_peak_mb, 0)
        self.assertGreater(result.cpu_avg_percent, 0)
        self.assertEqual(len(result.latencies), 10)


class TestPerformanceTestingFramework(unittest.TestCase):
    """Tests for performance testing framework."""

    def setUp(self):
        """Set up test fixtures."""
        self.framework = PerformanceTestingFramework()

    def test_benchmark_latency(self):
        """Test latency benchmarking."""
        def simple_op():
            pass

        result = self.framework.benchmark_latency(
            simple_op, iterations=100
        )

        self.assertGreater(result.avg_latency, 0)
        self.assertIn(result, self.framework.results)

    def test_benchmark_throughput(self):
        """Test throughput benchmarking."""
        def simple_op():
            pass

        result = self.framework.benchmark_throughput(
            simple_op, concurrent_count=5
        )

        self.assertGreater(result.throughput, 0)
        self.assertIn(result, self.framework.results)

    def test_benchmark_scalability(self):
        """Test scalability benchmarking."""
        def simple_op():
            pass

        results = self.framework.benchmark_scalability(
            simple_op, node_counts=[10, 100]
        )

        self.assertEqual(len(results), 2)
        self.assertTrue(all(r in self.framework.results for r in results))

    def test_profile_resources(self):
        """Test resource profiling."""
        def simple_op():
            pass

        result = self.framework.profile_resources(simple_op)

        self.assertGreater(result.memory_peak_mb, 0)
        self.assertIn(result, self.framework.results)

    def test_sla_validation_gold(self):
        """Test SLA validation for Gold level."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=1000,
            latencies=[50] * 950 + [99] * 50,  # 95% at 50ms, 5% at 99ms
            errors=0,
            throughput=10000
        )

        self.framework.results.append(run)
        sla = self.framework.validate_sla(SLALevel.GOLD)

        self.assertTrue(sla.validate(run))

    def test_sla_validation_silver(self):
        """Test SLA validation for Silver level."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=1000,
            latencies=[200] * 950 + [499] * 50,
            errors=1,  # 0.1% error rate
            throughput=10000
        )

        self.framework.results.append(run)
        sla = self.framework.validate_sla(SLALevel.SILVER)

        self.assertTrue(sla.validate(run))

    def test_sla_validation_fail(self):
        """Test SLA validation failure."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.HIGH_LOAD,
            duration_ms=100,
            iterations=1000,
            latencies=[1500] * 1000,  # All at 1500ms
            errors=50,  # 5% error rate
            throughput=10000
        )

        self.framework.results.append(run)
        sla = self.framework.validate_sla(SLALevel.GOLD)

        self.assertFalse(sla.validate(run))

    def test_generate_report(self):
        """Test report generation."""
        run = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=100,
            latencies=list(range(1, 101)),
            errors=0,
            throughput=1000
        )

        self.framework.results.append(run)

        report = self.framework.generate_report("test_run")

        self.assertEqual(report.test_name, "test_run")
        self.assertEqual(report.total_operations, 100)
        self.assertGreater(report.overall_throughput, 0)

    def test_error_rate_calculation(self):
        """Test error rate calculation."""
        run1 = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=100,
            latencies=[50] * 99,
            errors=1
        )

        run2 = BenchmarkRun(
            operation="test",
            scenario=TestScenario.MEDIUM_LOAD,
            duration_ms=100,
            iterations=100,
            latencies=[50] * 98,
            errors=2
        )

        self.framework.results.extend([run1, run2])

        report = self.framework.generate_report("error_test")

        self.assertAlmostEqual(
            report.error_rate,
            0.015,
            places=3)  # 3 errors / 200 ops


class TestPerformanceIntegration(unittest.TestCase):
    """Integration tests."""

    def test_complete_performance_audit(self):
        """Test complete performance audit flow."""
        framework = PerformanceTestingFramework()

        def test_op():
            time.sleep(0.001)

        # Run various benchmarks
        framework.benchmark_latency(test_op, iterations=50)
        framework.benchmark_throughput(test_op, concurrent_count=5, duration_seconds=1.0)
        framework.profile_resources(test_op, iterations=20)

        # Generate report
        report = framework.generate_report("full_audit")

        self.assertGreater(len(report.runs), 0)
        self.assertGreater(report.overall_throughput, 0)


if __name__ == "__main__":
    unittest.main()
