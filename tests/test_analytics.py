"""
Test suite for Advanced Analytics Dashboard

Tests for AnalyticsEngine class including:
- Metric recording and aggregation
- Anomaly detection
- Trend calculation
- Forecasting
- Dashboard summary generation
"""

import unittest
from datetime import datetime, timedelta, timezone

from opt.web.panel.analytics import (
    AnalyticsEngine,
    TimeGranularity,
    MetricType,
    AggregatedMetrics,
)


class TestAnalyticsEngine(unittest.TestCase):
    """Test AnalyticsEngine functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.engine = AnalyticsEngine()
        self.resource_id = "resource_1"

    def test_record_metric(self) -> None:
        """Test recording individual metrics."""
        result = self.engine.record_metric(
            metric_type=MetricType.CPU_USAGE,
            value=45.5,
            resource_id=self.resource_id,
            tags={"host": "server1"},
        )

        self.assertTrue(result)
        self.assertIn((MetricType.CPU_USAGE, self.resource_id), self.engine.data_points)

    def test_record_multiple_metrics(self) -> None:
        """Test recording multiple metrics."""
        for i in range(100):
            value = 50 + (i % 30)
            self.engine.record_metric(
                metric_type=MetricType.CPU_USAGE,
                value=value,
                resource_id=self.resource_id,
            )

        key = (MetricType.CPU_USAGE, self.resource_id)
        self.assertGreaterEqual(len(self.engine.data_points[key]), 100)

    def test_aggregate_metrics_by_hour(self) -> None:
        """Test metric aggregation by hour."""
        base_time = datetime.now(timezone.utc)

        # Add metrics over 2 hours
        for hour in range(2):
            for minute in range(0, 60, 10):
                timestamp = base_time + timedelta(hours=hour, minutes=minute)
                self.engine.record_metric(
                    metric_type=MetricType.CPU_USAGE,
                    value=50 + hour * 10,
                    resource_id=self.resource_id,
                    timestamp=timestamp,
                )

        aggregated = self.engine.aggregate_metrics(
            metric_type=MetricType.CPU_USAGE,
            start_time=base_time,
            end_time=base_time + timedelta(hours=2),
            granularity=TimeGranularity.HOUR,
            resource_id=self.resource_id,
        )

        self.assertEqual(len(aggregated), 2)
        self.assertIsInstance(aggregated[0], AggregatedMetrics)

    def test_detect_anomalies(self) -> None:
        """Test anomaly detection."""
        # Add normal metrics
        for i in range(100):
            value = 50 + (i % 5)    # Small variance
            self.engine.record_metric(
                metric_type=MetricType.CPU_USAGE,
                value=value,
                resource_id=self.resource_id,
            )

        # Add anomalous metric
        self.engine.record_metric(
            metric_type=MetricType.CPU_USAGE,
            value=150,    # Far from normal
            resource_id=self.resource_id,
        )

        anomalies = self.engine.detect_anomalies(
            metric_type=MetricType.CPU_USAGE,
            resource_id=self.resource_id,
            threshold_stddevs=2,
        )

        self.assertGreater(len(anomalies), 0)

    def test_calculate_trend(self) -> None:
        """Test trend calculation."""
        # Add increasing metrics
        for i in range(50):
            self.engine.record_metric(
                metric_type=MetricType.MEMORY_USAGE,
                value=30 + i * 0.5,
                resource_id=self.resource_id,
            )

        trend = self.engine.calculate_trend(
            metric_type=MetricType.MEMORY_USAGE,
            resource_id=self.resource_id,
        )

        self.assertIsNotNone(trend)
        self.assertIn("slope", trend)
        self.assertIn("direction", trend)
        self.assertGreater(trend["slope"], 0)    # Increasing trend

    def test_forecast_metric(self) -> None:
        """Test metric forecasting."""
        base_time = datetime.now(timezone.utc)

        # Add historical metrics
        for i in range(30):
            timestamp = base_time - timedelta(days=30 - i)
            self.engine.record_metric(
                metric_type=MetricType.DISK_IO,
                value=100 + i * 2,
                resource_id=self.resource_id,
                timestamp=timestamp,
            )

        forecast = self.engine.forecast_metric(
            metric_type=MetricType.DISK_IO,
            periods_ahead=5,
            resource_id=self.resource_id,
        )

        self.assertEqual(len(forecast), 5)
        self.assertTrue(all(isinstance(v, (int, float)) for v in forecast))

    def test_get_dashboard_summary(self) -> None:
        """Test dashboard summary generation."""
        # Add metrics for multiple types
        metrics_data = [
            (MetricType.CPU_USAGE, 45),
            (MetricType.MEMORY_USAGE, 65),
            (MetricType.DISK_IO, 150),
        ]

        for metric_type, value in metrics_data:
            for i in range(20):
                self.engine.record_metric(
                    metric_type=metric_type,
                    value=value + (i % 5),
                    resource_id=self.resource_id,
                )

        summary = self.engine.get_dashboard_summary(time_window=3600)

        self.assertIn("summary", summary)
        self.assertIn("metrics", summary)
        self.assertGreater(len(summary["metrics"]), 0)

    def test_get_statistics(self) -> None:
        """Test statistics retrieval."""
        for i in range(50):
            self.engine.record_metric(
                metric_type=MetricType.CPU_USAGE,
                value=50 + i,
                resource_id=self.resource_id,
            )

        stats = self.engine.get_statistics()

        self.assertIn("total_data_points", stats)
        self.assertIn("datasets_tracked", stats)
        self.assertGreater(stats["total_data_points"], 0)

    def test_data_retention(self) -> None:
        """Test automatic data cleanup."""
        old_time = datetime.now(timezone.utc) - timedelta(days=40)
        recent_time = datetime.now(timezone.utc) - timedelta(days=1)

        # Add old and recent metrics
        for i in range(10):
            self.engine.record_metric(
                metric_type=MetricType.CPU_USAGE,
                value=50,
                resource_id=self.resource_id,
                timestamp=old_time,
            )
            self.engine.record_metric(
                metric_type=MetricType.CPU_USAGE,
                value=50,
                resource_id=self.resource_id,
                timestamp=recent_time,
            )

        # Trigger cleanup
        self.engine._cleanup_old_data()

        key = (MetricType.CPU_USAGE, self.resource_id)
        if key in self.engine.data_points:
        # Verify old data is removed
            for point in self.engine.data_points[key]:
                self.assertGreater(point.timestamp, old_time + timedelta(days=35))


class TestMetricAggregation(unittest.TestCase):
    """Test metric aggregation functionality."""

    def test_aggregated_metrics_calculations(self) -> None:
        """Test statistical calculations in aggregated metrics."""
        points = [10, 20, 30, 40, 50]

        metrics = AggregatedMetrics(
            metric_type=MetricType.CPU_USAGE,
            timestamp=datetime.now(timezone.utc),
            count=len(points),
            min_value=10,
            max_value=50,
            sum_value=sum(points),
        )

        self.assertEqual(metrics.min_value, 10)
        self.assertEqual(metrics.max_value, 50)
        self.assertEqual(metrics.average, 30)

    def test_aggregated_metrics_edge_cases(self) -> None:
        """Test aggregated metrics with edge cases."""
        # Single value
        metrics = AggregatedMetrics(
            metric_type=MetricType.MEMORY_USAGE,
            timestamp=datetime.now(timezone.utc),
            count=1,
            min_value=100,
            max_value=100,
            sum_value=100,
        )

        self.assertEqual(metrics.average, 100)
        self.assertEqual(metrics.min_value, metrics.max_value)


if __name__ == "__main__":
    unittest.main()
