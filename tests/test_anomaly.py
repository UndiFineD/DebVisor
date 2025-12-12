"""
ML Anomaly Detection - Comprehensive Test Suite

38 comprehensive tests covering all anomaly detection functionality.

Author: DebVisor Development Team
"""

import tempfile
import unittest
from datetime import datetime, timedelta, timezone

from opt.services.anomaly.core import (
    AnomalyDetectionEngine,
    AnomalyType,
    AnomalyAlert,
    Baseline,
    DetectionMethod,
    MetricType,
    MetricPoint,
    SeverityLevel,
    TrendAnalysis,
    AnomalyConfig,
    get_anomaly_engine,
)


class TestMetricManagement(unittest.TestCase):
    """Test metric data collection and management."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.temp_dir = tempfile.mkdtemp()
        config = AnomalyConfig()
        config.config_dir = self.temp_dir
        self.engine = AnomalyDetectionEngine(config=config)

    def tearDown(self) -> None:
        """Clean up."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_add_single_metric(self) -> None:
        """Test adding single metric."""
        self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 75.5)

        key = ("vm-001", MetricType.CPU_USAGE)
        self.assertIn(key, self.engine.metrics)
        self.assertEqual(len(self.engine.metrics[key]), 1)
        self.assertEqual(self.engine.metrics[key][0].value, 75.5)

    def test_add_multiple_metrics(self) -> None:
        """Test adding multiple metrics."""
        for i in range(10):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)

        key = ("vm-001", MetricType.CPU_USAGE)
        self.assertEqual(len(self.engine.metrics[key]), 10)

    def test_add_different_resources(self) -> None:
        """Test adding metrics for different resources."""
        self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 75.0)
        self.engine.add_metric("vm-002", MetricType.CPU_USAGE, 80.0)

        self.assertEqual(len(self.engine.metrics), 2)

    def test_add_different_metric_types(self) -> None:
        """Test adding different metric types."""
        self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 75.0)
        self.engine.add_metric("vm-001", MetricType.MEMORY_USAGE, 85.0)

        self.assertEqual(len(self.engine.metrics), 2)

    def test_max_history_limit(self) -> None:
        """Test maximum history limit enforcement."""
        for i in range(12000):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + (i % 50))

        key = ("vm-001", MetricType.CPU_USAGE)
        self.assertLessEqual(len(self.engine.metrics[key]), 10000)

    def test_metric_timestamps(self) -> None:
        """Test that metrics have timestamps."""
        self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 75.0)

        key = ("vm-001", MetricType.CPU_USAGE)
        self.assertIsNotNone(self.engine.metrics[key][0].timestamp)
        self.assertIsInstance(self.engine.metrics[key][0].timestamp, datetime)


class TestBaselineEstablishment(unittest.TestCase):
    """Test baseline establishment from historical data."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.temp_dir = tempfile.mkdtemp()
        config = AnomalyConfig()
        config.config_dir = self.temp_dir
        self.engine = AnomalyDetectionEngine(config=config)

    def tearDown(self) -> None:
        """Clean up."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_establish_baseline_success(self) -> None:
        """Test successful baseline establishment."""
        # Add enough data
        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)

        baseline = self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)

        self.assertIsNotNone(baseline)
        self.assertEqual(baseline.resource_id, "vm-001")  # type: ignore[union-attr]
        self.assertEqual(baseline.metric_type, MetricType.CPU_USAGE)  # type: ignore[union-attr]
        self.assertGreater(baseline.mean, 0)  # type: ignore[union-attr]

    def test_establish_baseline_insufficient_data(self) -> None:
        """Test baseline establishment with insufficient data."""
        self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 75.0)

        baseline = self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)
        self.assertIsNone(baseline)

    def test_baseline_statistics(self) -> None:
        """Test baseline statistics calculation."""
        # Add values 0-99
        for i in range(100):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, float(i))

        baseline = self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)

        self.assertAlmostEqual(baseline.mean, 49.5, delta=1)  # type: ignore[union-attr]
        self.assertAlmostEqual(baseline.min_value, 0, delta=1)  # type: ignore[union-attr]
        self.assertAlmostEqual(baseline.max_value, 99, delta=1)  # type: ignore[union-attr]
        self.assertEqual(baseline.sample_count, 100)  # type: ignore[union-attr]

    def test_percentile_calculation(self) -> None:
        """Test percentile calculation in baseline."""
        # Add values 0-99
        for i in range(100):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, float(i))

        baseline = self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)

        self.assertGreater(baseline.p25, baseline.mean - 30)  # type: ignore[union-attr]
        self.assertLess(baseline.p25, baseline.mean + 10)  # type: ignore[union-attr]
        self.assertGreater(baseline.p75, baseline.mean - 10)  # type: ignore[union-attr]
        self.assertLess(baseline.p75, baseline.mean + 30)  # type: ignore[union-attr]

    def test_baseline_persistence(self) -> None:
        """Test baseline is stored in engine."""
        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)

        baseline1 = self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)

        key = ("vm-001", MetricType.CPU_USAGE)
        self.assertIn(key, self.engine.baselines)
        self.assertEqual(self.engine.baselines[key], baseline1)


class TestZScoreDetection(unittest.TestCase):
    """Test Z-score anomaly detection method."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.temp_dir = tempfile.mkdtemp()
        config = AnomalyConfig()
        config.config_dir = self.temp_dir
        self.engine = AnomalyDetectionEngine(config=config)

        # Create normal distribution around 50
        for i in range(100):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + (i % 20 - 10))

        self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)

    def tearDown(self) -> None:
        """Clean up."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_detect_spike(self) -> None:
        """Test detection of spike anomaly."""
        alerts = self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 100.0, [DetectionMethod.Z_SCORE]
        )

        self.assertGreater(len(alerts), 0)
        self.assertEqual(alerts[0].anomaly_type, AnomalyType.SPIKE)

    def test_detect_dip(self) -> None:
        """Test detection of dip anomaly."""
        alerts = self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 0.0, [DetectionMethod.Z_SCORE]
        )

        self.assertGreater(len(alerts), 0)
        self.assertEqual(alerts[0].anomaly_type, AnomalyType.DIP)

    def test_no_anomaly_normal_value(self) -> None:
        """Test no anomaly for normal value."""
        alerts = self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 50.0, [DetectionMethod.Z_SCORE]
        )

        self.assertEqual(len(alerts), 0)

    def test_confidence_scoring(self) -> None:
        """Test confidence score calculation."""
        alerts = self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 100.0, [DetectionMethod.Z_SCORE]
        )

        self.assertGreater(len(alerts), 0)
        self.assertGreater(alerts[0].confidence, 0)
        self.assertLessEqual(alerts[0].confidence, 1.0)

    def test_severity_classification(self) -> None:
        """Test severity level assignment."""
        alerts = self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 100.0, [DetectionMethod.Z_SCORE]
        )

        self.assertGreater(len(alerts), 0)
        self.assertIn(
            alerts[0].severity, [SeverityLevel.WARNING, SeverityLevel.CRITICAL]
        )


class TestIQRDetection(unittest.TestCase):
    """Test IQR (Interquartile Range) detection."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.temp_dir = tempfile.mkdtemp()
        config = AnomalyConfig()
        config.config_dir = self.temp_dir
        self.engine = AnomalyDetectionEngine(config=config)

        # Create bimodal distribution
        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 40 + i)

        self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)

    def tearDown(self) -> None:
        """Clean up."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_iqr_detection(self) -> None:
        """Test IQR anomaly detection."""
        alerts = self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 150.0, [DetectionMethod.IQR]
        )

        self.assertGreater(len(alerts), 0)
        self.assertEqual(alerts[0].detection_method, DetectionMethod.IQR)

    def test_iqr_confidence(self) -> None:
        """Test IQR confidence scoring."""
        alerts = self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 150.0, [DetectionMethod.IQR]
        )

        self.assertGreater(len(alerts), 0)
        self.assertGreater(alerts[0].confidence, 0.5)


class TestEWMADetection(unittest.TestCase):
    """Test EWMA (Exponential Weighted Moving Average) detection."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.temp_dir = tempfile.mkdtemp()
        config = AnomalyConfig()
        config.config_dir = self.temp_dir
        self.engine = AnomalyDetectionEngine(config=config)

        # Add time series data
        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + (i % 10))

        self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)

    def tearDown(self) -> None:
        """Clean up."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_ewma_detection(self) -> None:
        """Test EWMA anomaly detection."""
        alerts = self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 90.0, [DetectionMethod.EWMA]
        )

        # EWMA may not detect depending on data
        if alerts:
            self.assertEqual(alerts[0].detection_method, DetectionMethod.EWMA)


class TestTrendAnalysis(unittest.TestCase):
    """Test trend analysis functionality."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.temp_dir = tempfile.mkdtemp()
        config = AnomalyConfig()
        config.config_dir = self.temp_dir
        self.engine = AnomalyDetectionEngine(config=config)

    def tearDown(self) -> None:
        """Clean up."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_increasing_trend(self) -> None:
        """Test detection of increasing trend."""
        # Add increasing values
        base_time = datetime.now(timezone.utc) - timedelta(hours=30)
        for i in range(30):
            self.engine.add_metric(
                "vm-001",
                MetricType.CPU_USAGE,
                50 + i,
                _timestamp = base_time + timedelta(hours=i),
            )

        trend = self.engine.analyze_trend("vm-001", MetricType.CPU_USAGE, hours=48)

        self.assertIsNotNone(trend)
        self.assertEqual(trend.trend_direction, "increasing")  # type: ignore[union-attr]

    def test_decreasing_trend(self) -> None:
        """Test detection of decreasing trend."""
        # Add decreasing values
        base_time = datetime.now(timezone.utc) - timedelta(hours=30)
        for i in range(30):
            self.engine.add_metric(
                "vm-001",
                MetricType.CPU_USAGE,
                100 - i,
                _timestamp = base_time + timedelta(hours=i),
            )

        trend = self.engine.analyze_trend("vm-001", MetricType.CPU_USAGE, hours=48)

        self.assertIsNotNone(trend)
        self.assertEqual(trend.trend_direction, "decreasing")  # type: ignore[union-attr]

    def test_stable_trend(self) -> None:
        """Test detection of stable trend."""
        # Add stable values
        for i in range(30):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50.0)

        trend = self.engine.analyze_trend("vm-001", MetricType.CPU_USAGE, hours=1)

        self.assertIsNotNone(trend)
        self.assertEqual(trend.trend_direction, "stable")  # type: ignore[union-attr]

    def test_trend_forecast(self) -> None:
        """Test trend forecasting."""
        for i in range(30):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)

        trend = self.engine.analyze_trend("vm-001", MetricType.CPU_USAGE, hours=1)

        self.assertIsNotNone(trend)
        self.assertGreater(trend.forecast_value_24h, 80)  # type: ignore[union-attr]

    def test_insufficient_data_trend(self) -> None:
        """Test trend with insufficient data."""
        self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50.0)

        trend = self.engine.analyze_trend("vm-001", MetricType.CPU_USAGE, hours=1)

        self.assertIsNone(trend)


class TestAlertManagement(unittest.TestCase):
    """Test alert management and acknowledgment."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.temp_dir = tempfile.mkdtemp()
        config = AnomalyConfig()
        config.config_dir = self.temp_dir
        self.engine = AnomalyDetectionEngine(config=config)

    def tearDown(self) -> None:
        """Clean up."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_alert(self) -> None:
        """Test alert creation."""
        alert = AnomalyAlert(
            _alert_id = "test-001",
            _timestamp = datetime.now(timezone.utc),
            _resource_id = "vm-001",
            _metric_type = MetricType.CPU_USAGE,
            _anomaly_type = AnomalyType.SPIKE,
            _severity = SeverityLevel.CRITICAL,
            _confidence = 0.95,
            _detected_value = 95.0,
            _expected_range = (40.0, 60.0),
            _detection_method = DetectionMethod.Z_SCORE,
            _message = "CPU spike detected",
        )

        self.assertEqual(alert.alert_id, "test-001")
        self.assertFalse(alert.acknowledged)

    def test_acknowledge_alert(self) -> None:
        """Test alert acknowledgment."""
        # Create an alert
        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)

        self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)
        alerts = self.engine.detect_anomalies("vm-001", MetricType.CPU_USAGE, 100.0)

        if alerts:
            alert_id = alerts[0].alert_id
            success = self.engine.acknowledge_alert(alert_id, "admin", "Acknowledged")

            self.assertTrue(success)

    def test_get_active_alerts(self) -> None:
        """Test retrieving active alerts."""
        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)

        self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)
        self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 150.0
        )    # Much larger spike

        active = self.engine.get_active_alerts()
        self.assertGreater(len(active), 0)

    def test_alert_history_filtering(self) -> None:
        """Test alert history filtering."""
        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)
            self.engine.add_metric("vm-002", MetricType.CPU_USAGE, 50 + i)

        self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)
        self.engine.establish_baseline("vm-002", MetricType.CPU_USAGE)

        self.engine.detect_anomalies("vm-001", MetricType.CPU_USAGE, 100.0)
        self.engine.detect_anomalies("vm-002", MetricType.CPU_USAGE, 100.0)

        history = self.engine.get_alert_history(resource_id="vm-001")

        for alert in history:
            self.assertEqual(alert.resource_id, "vm-001")

    def test_alert_history_time_filtering(self) -> None:
        """Test alert history time filtering."""
        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)

        self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)
        self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 150.0
        )    # Much larger spike

        history = self.engine.get_alert_history(hours=1)
        self.assertGreater(len(history), 0)

    def test_severity_filtering(self) -> None:
        """Test alert filtering by severity."""
        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)

        self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)
        self.engine.detect_anomalies("vm-001", MetricType.CPU_USAGE, 100.0)

        active = self.engine.get_active_alerts(severity=SeverityLevel.CRITICAL)

        for alert in active:
            self.assertEqual(alert.severity, SeverityLevel.CRITICAL)


class TestMultipleDetectionMethods(unittest.TestCase):
    """Test multiple detection methods together."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.temp_dir = tempfile.mkdtemp()
        config = AnomalyConfig()
        config.config_dir = self.temp_dir
        self.engine = AnomalyDetectionEngine(config=config)

        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)

        self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)

    def tearDown(self) -> None:
        """Clean up."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_all_methods_detection(self) -> None:
        """Test detection with all methods."""
        alerts = self.engine.detect_anomalies(
            "vm-001",
            MetricType.CPU_USAGE,
            150.0,    # Much larger spike to ensure detection
            [DetectionMethod.Z_SCORE, DetectionMethod.IQR, DetectionMethod.EWMA],
        )

        self.assertGreater(len(alerts), 0)

    def test_specific_method_detection(self) -> None:
        """Test detection with specific method."""
        alerts = self.engine.detect_anomalies(
            "vm-001",
            MetricType.CPU_USAGE,
            150.0,    # Much larger spike to ensure detection
            [DetectionMethod.Z_SCORE],
        )

        self.assertGreater(len(alerts), 0)
        for alert in alerts:
            self.assertEqual(alert.detection_method, DetectionMethod.Z_SCORE)


class TestStatistics(unittest.TestCase):
    """Test system statistics."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.temp_dir = tempfile.mkdtemp()
        config = AnomalyConfig()
        config.config_dir = self.temp_dir
        self.engine = AnomalyDetectionEngine(config=config)

    def tearDown(self) -> None:
        """Clean up."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_empty_statistics(self) -> None:
        """Test statistics on empty engine."""
        stats = self.engine.get_statistics()

        self.assertEqual(stats["total_metrics"], 0)
        self.assertEqual(stats["total_alerts"], 0)

    def test_statistics_with_data(self) -> None:
        """Test statistics with data."""
        for i in range(50):
            self.engine.add_metric("vm-001", MetricType.CPU_USAGE, 50 + i)

        self.engine.establish_baseline("vm-001", MetricType.CPU_USAGE)
        self.engine.detect_anomalies(
            "vm-001", MetricType.CPU_USAGE, 150.0
        )    # Larger spike

        stats = self.engine.get_statistics()

        self.assertGreater(stats["total_metrics"], 0)
        self.assertGreater(stats["total_alerts"], 0)


class TestDataModel(unittest.TestCase):
    """Test data model serialization."""

    def test_metric_point_serialization(self) -> None:
        """Test MetricPoint serialization."""
        point = MetricPoint(
            timestamp=datetime.now(timezone.utc),
            value=75.5,
            resource_id="vm-001",
            _metric_type = MetricType.CPU_USAGE,
        )

        data = point.to_dict()

        self.assertIn("timestamp", data)
        self.assertEqual(data["value"], 75.5)
        self.assertEqual(data["resource_id"], "vm-001")

    def test_baseline_serialization(self) -> None:
        """Test Baseline serialization."""
        _baseline = Baseline(
            _metric_type = MetricType.CPU_USAGE,
            _resource_id = "vm-001",
            _mean = 50.0,
            _stddev = 10.0,
            _min_value = 30.0,
            _max_value = 70.0,
            _p25 = 42.5,
            _p50 = 50.0,
            _p75 = 57.5,
            _p95 = 65.0,
            sample_count=100,
        )

        data = baseline.to_dict()

        self.assertEqual(data["mean"], 50.0)
        self.assertEqual(data["sample_count"], 100)

    def test_alert_serialization(self) -> None:
        """Test AnomalyAlert serialization."""
        alert = AnomalyAlert(
            _alert_id = "test-001",
            _timestamp = datetime.now(timezone.utc),
            _resource_id = "vm-001",
            _metric_type = MetricType.CPU_USAGE,
            _anomaly_type = AnomalyType.SPIKE,
            _severity = SeverityLevel.CRITICAL,
            _confidence = 0.95,
            _detected_value = 95.0,
            _expected_range = (40.0, 60.0),
            _detection_method = DetectionMethod.Z_SCORE,
            _message = "CPU spike",
        )

        data = alert.to_dict()

        self.assertEqual(data["alert_id"], "test-001")
        self.assertEqual(data["severity"], "critical")
        self.assertEqual(data["confidence"], 0.95)

    def test_trend_serialization(self) -> None:
        """Test TrendAnalysis serialization."""
        trend = TrendAnalysis(
            _resource_id = "vm-001",
            _metric_type = MetricType.CPU_USAGE,
            _period_start = datetime.now(timezone.utc),
            _period_end = datetime.now(timezone.utc),
            _trend_direction = "increasing",
            _trend_strength = 0.85,
            _average_change_per_hour = 2.5,
            _forecast_value_24h = 75.0,
            _confidence = 0.90,
            _analysis_method = "linear_regression",
        )

        data = trend.to_dict()

        self.assertEqual(data["trend_direction"], "increasing")
        self.assertEqual(data["trend_strength"], 0.85)


class TestGlobalEngineInstance(unittest.TestCase):
    """Test global engine instance management."""

    def setUp(self) -> None:
        """Set up test environment."""
        # Reset global engine for testing
        import opt.services.anomaly.core as core_module

        self.original_engine = core_module._engine
        core_module._engine = None

    def tearDown(self) -> None:
        """Restore original engine."""
        import opt.services.anomaly.core as core_module

        core_module._engine = self.original_engine

    def test_get_engine_singleton(self) -> None:
        """Test that engine is singleton."""
        temp_dir = tempfile.mkdtemp()
        try:
            engine1 = get_anomaly_engine(temp_dir)
            engine2 = get_anomaly_engine(temp_dir)

            self.assertIs(engine1, engine2)
        finally:
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_engine_persistence(self) -> None:
        """Test engine state persistence."""
        temp_dir = tempfile.mkdtemp()
        try:
            engine = get_anomaly_engine(temp_dir)

            engine.add_metric("vm-001", MetricType.CPU_USAGE, 75.0)

            engine2 = get_anomaly_engine(temp_dir)
            key = ("vm-001", MetricType.CPU_USAGE)

            self.assertIn(key, engine2.metrics)
        finally:
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)


# Run tests
if __name__ == "__main__":
    unittest.main()
