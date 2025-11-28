#!/usr/bin/env python3
"""
Tests for advanced features and enhancements.

Tests for:
  - Anomaly detection
  - Compliance automation
  - Predictive analytics
  - Cost optimization
  - Integration management
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

import sys
from pathlib import Path

opt_path = Path(__file__).parent.parent / "opt"
sys.path.insert(0, str(opt_path))

from advanced_features import (
    AnomalyDetector, StatisticalAnomalyDetector, AnomalyAlert, AnomalyType,
    ComplianceAutomation, ComplianceControl, ComplianceFramework,
    PredictiveAnalytics, MetricPrediction,
    CostOptimizer, CostAnalysis,
    IntegrationManager, IntegrationStatus
)


class TestAnomalyAlert(unittest.TestCase):
    """Tests for anomaly alerts."""

    def test_anomaly_alert_creation(self):
        """Test creating anomaly alert."""
        alert = AnomalyAlert(
            alert_id="test_1",
            anomaly_type=AnomalyType.RESOURCE_OVERUSE,
            severity="high",
            metric_name="cpu_usage",
            current_value=95.0,
            threshold_value=80.0,
            deviation_percent=18.75
        )

        self.assertEqual(alert.alert_id, "test_1")
        self.assertEqual(alert.severity, "high")
        self.assertFalse(alert.acknowledged)

    def test_anomaly_alert_is_critical(self):
        """Test critical alert detection."""
        alert = AnomalyAlert(
            alert_id="test_1",
            anomaly_type=AnomalyType.SECURITY_ANOMALY,
            severity="critical",
            metric_name="failed_auth",
            current_value=100.0,
            threshold_value=10.0,
            deviation_percent=900.0
        )

        self.assertTrue(alert.is_critical())


class TestStatisticalAnomalyDetector(unittest.TestCase):
    """Tests for statistical anomaly detector."""

    def setUp(self):
        """Set up test fixtures."""
        self.detector = StatisticalAnomalyDetector(std_dev_threshold=2.0)

    def test_detector_initialization(self):
        """Test detector initialization."""
        self.assertIsNotNone(self.detector)
        self.assertEqual(len(self.detector.baselines), 0)

    def test_detect_normal_metrics(self):
        """Test detecting normal metrics."""
        # Initialize baseline
        self.detector.detect({"cpu": 50.0, "memory": 60.0})

        # Normal metrics
        alerts = self.detector.detect({"cpu": 51.0, "memory": 59.0})

        self.assertEqual(len(alerts), 0)

    def test_detect_anomalous_spike(self):
        """Test detecting anomalous spike."""
        # Initialize baseline
        self.detector.detect({"cpu": 50.0})
        self.detector.std_devs["cpu"] = 5.0

        # Large spike
        alerts = self.detector.detect({"cpu": 95.0})

        self.assertGreater(len(alerts), 0)
        self.assertEqual(alerts[0].metric_name, "cpu")

    def test_get_baseline(self):
        """Test getting baseline."""
        metrics = {"cpu": 50.0, "memory": 60.0}
        self.detector.detect(metrics)

        baseline = self.detector.get_baseline()

        self.assertEqual(baseline["cpu"], 50.0)
        self.assertEqual(baseline["memory"], 60.0)


class TestMetricPrediction(unittest.TestCase):
    """Tests for metric predictions."""

    def test_metric_prediction_creation(self):
        """Test creating metric prediction."""
        prediction = MetricPrediction(
            metric_name="cpu_usage",
            current_value=50.0,
            predicted_value=60.0,
            confidence=0.85,
            trend="up"
        )

        self.assertEqual(prediction.metric_name, "cpu_usage")
        self.assertTrue(prediction.is_high_confidence())

    def test_metric_prediction_low_confidence(self):
        """Test low confidence prediction."""
        prediction = MetricPrediction(
            metric_name="cpu_usage",
            current_value=50.0,
            predicted_value=60.0,
            confidence=0.7,
            trend="up"
        )

        self.assertFalse(prediction.is_high_confidence())


class TestComplianceControl(unittest.TestCase):
    """Tests for compliance controls."""

    def test_compliance_control_creation(self):
        """Test creating compliance control."""
        control = ComplianceControl(
            control_id="SOC2_AC1",
            control_name="Access Control",
            framework=ComplianceFramework.SOC2,
            description="User access control",
            severity="critical",
            remediation_steps=["Implement RBAC", "Enable MFA"]
        )

        self.assertEqual(control.control_id, "SOC2_AC1")
        self.assertEqual(control.framework, ComplianceFramework.SOC2)
        self.assertFalse(control.compliant)

    def test_compliance_control_remediation(self):
        """Test remediation guidance."""
        control = ComplianceControl(
            control_id="SOC2_AC1",
            control_name="Access Control",
            framework=ComplianceFramework.SOC2,
            description="User access control",
            severity="critical",
            remediation_steps=["Step 1", "Step 2", "Step 3"]
        )

        guidance = control.get_remediation_guidance()

        self.assertIn("Step 1", guidance)
        self.assertIn("Step 2", guidance)


class TestComplianceAutomation(unittest.TestCase):
    """Tests for compliance automation."""

    def setUp(self):
        """Set up test fixtures."""
        self.compliance = ComplianceAutomation()

    def test_register_control(self):
        """Test registering control."""
        control = ComplianceControl(
            control_id="SOC2_AC1",
            control_name="Access Control",
            framework=ComplianceFramework.SOC2,
            description="User access control",
            severity="critical"
        )

        result = self.compliance.register_control(control)

        self.assertTrue(result)
        self.assertIn("SOC2_AC1", self.compliance.controls)

    def test_register_validator(self):
        """Test registering validator."""
        control = ComplianceControl(
            control_id="SOC2_AC1",
            control_name="Access Control",
            framework=ComplianceFramework.SOC2,
            description="User access control",
            severity="critical"
        )

        self.compliance.register_control(control)

        validator = lambda: True
        result = self.compliance.register_validator("SOC2_AC1", validator)

        self.assertTrue(result)

    def test_validate_control_compliant(self):
        """Test validating compliant control."""
        control = ComplianceControl(
            control_id="SOC2_AC1",
            control_name="Access Control",
            framework=ComplianceFramework.SOC2,
            description="User access control",
            severity="critical"
        )

        self.compliance.register_control(control)
        self.compliance.register_validator("SOC2_AC1", lambda: True)

        compliant, message = self.compliance.validate_control("SOC2_AC1")

        self.assertTrue(compliant)

    def test_validate_control_non_compliant(self):
        """Test validating non-compliant control."""
        control = ComplianceControl(
            control_id="SOC2_AC1",
            control_name="Access Control",
            framework=ComplianceFramework.SOC2,
            description="User access control",
            severity="critical"
        )

        self.compliance.register_control(control)
        self.compliance.register_validator("SOC2_AC1", lambda: False)

        compliant, message = self.compliance.validate_control("SOC2_AC1")

        self.assertFalse(compliant)

    def test_generate_compliance_report(self):
        """Test generating compliance report."""
        # Register multiple controls
        for i in range(5):
            control = ComplianceControl(
                control_id=f"SOC2_C{i}",
                control_name=f"Control {i}",
                framework=ComplianceFramework.SOC2,
                description=f"Test control {i}",
                severity="high",
                compliant=(i % 2 == 0)
            )

            self.compliance.register_control(control)

        report = self.compliance.generate_compliance_report(ComplianceFramework.SOC2)

        self.assertEqual(report["framework"], "soc2")
        self.assertEqual(report["total_controls"], 5)
        self.assertGreater(report["compliance_rate"], 0)

    def test_audit_log(self):
        """Test audit logging."""
        control = ComplianceControl(
            control_id="SOC2_AC1",
            control_name="Access Control",
            framework=ComplianceFramework.SOC2,
            description="User access control",
            severity="critical"
        )

        self.compliance.register_control(control)
        self.compliance.register_validator("SOC2_AC1", lambda: True)

        self.compliance.validate_control("SOC2_AC1")

        audit_log = self.compliance.get_audit_log(hours=1)

        self.assertGreater(len(audit_log), 0)


class TestPredictiveAnalytics(unittest.TestCase):
    """Tests for predictive analytics."""

    def setUp(self):
        """Set up test fixtures."""
        self.analytics = PredictiveAnalytics(history_size=20)

    def test_add_metric(self):
        """Test adding metrics."""
        self.analytics.add_metric("cpu", 50.0)
        self.analytics.add_metric("cpu", 55.0)

        self.assertIn("cpu", self.analytics.history)
        self.assertEqual(len(self.analytics.history["cpu"]), 2)

    def test_predict_with_insufficient_data(self):
        """Test prediction with insufficient data."""
        self.analytics.add_metric("cpu", 50.0)

        prediction = self.analytics.predict("cpu")

        self.assertIsNone(prediction)

    def test_predict_with_sufficient_data(self):
        """Test prediction with sufficient data."""
        # Add multiple data points
        for i in range(10):
            self.analytics.add_metric("cpu", 50.0 + i)

        prediction = self.analytics.predict("cpu")

        self.assertIsNotNone(prediction)
        self.assertIsInstance(prediction, MetricPrediction)
        self.assertIn(prediction.trend, ["up", "down", "stable"])

    def test_get_trend(self):
        """Test getting metric trend."""
        # Increasing trend
        for i in range(10):
            self.analytics.add_metric("cpu", 50.0 + i * 2)

        trend = self.analytics.get_trend("cpu", minutes=60)

        self.assertEqual(trend, "up")

    def test_get_trend_nonexistent(self):
        """Test trend for nonexistent metric."""
        trend = self.analytics.get_trend("nonexistent")

        self.assertIsNone(trend)

    def test_history_size_bounded(self):
        """Test history is bounded."""
        for i in range(50):
            self.analytics.add_metric("cpu", 50.0 + i)

        self.assertLessEqual(len(self.analytics.history["cpu"]), 20)


class TestCostAnalysis(unittest.TestCase):
    """Tests for cost analysis."""

    def test_cost_analysis_creation(self):
        """Test creating cost analysis."""
        analysis = CostAnalysis(
            period="daily",
            total_cost=1000.0,
            cost_breakdown={"storage": 300.0, "compute": 700.0},
            cost_trend=10.0,
            savings_opportunity=50.0,
            waste_detected=100.0
        )

        self.assertEqual(analysis.total_cost, 1000.0)
        self.assertGreater(analysis.get_cost_efficiency_ratio(), 0)

    def test_cost_efficiency_ratio(self):
        """Test cost efficiency calculation."""
        analysis = CostAnalysis(
            period="daily",
            total_cost=1000.0,
            cost_breakdown={"storage": 300.0, "compute": 700.0},
            cost_trend=0.0,
            savings_opportunity=50.0,
            waste_detected=100.0
        )

        ratio = analysis.get_cost_efficiency_ratio()

        self.assertAlmostEqual(ratio, 0.9, places=1)


class TestCostOptimizer(unittest.TestCase):
    """Tests for cost optimizer."""

    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = CostOptimizer()

    def test_register_optimization_rule(self):
        """Test registering optimization rule."""
        rule = lambda total, breakdown: ["Recommendation 1"]
        self.optimizer.register_optimization_rule("rule1", rule)

        self.assertIn("rule1", self.optimizer.optimization_rules)

    def test_analyze_costs(self):
        """Test cost analysis."""
        analysis = self.optimizer.analyze_costs(
            period="daily",
            total_cost=1000.0,
            cost_breakdown={"storage": 300.0, "compute": 700.0}
        )

        self.assertEqual(analysis.total_cost, 1000.0)
        self.assertIn(analysis, self.optimizer.cost_history)

    def test_analyze_costs_with_history(self):
        """Test cost trend calculation."""
        self.optimizer.analyze_costs(
            period="daily",
            total_cost=1000.0,
            cost_breakdown={"storage": 300.0, "compute": 700.0}
        )

        analysis = self.optimizer.analyze_costs(
            period="daily",
            total_cost=1100.0,
            cost_breakdown={"storage": 320.0, "compute": 780.0}
        )

        self.assertGreater(analysis.cost_trend, 0)

    def test_get_cost_history(self):
        """Test retrieving cost history."""
        for i in range(5):
            self.optimizer.analyze_costs(
                period="daily",
                total_cost=1000.0 + i * 100,
                cost_breakdown={"storage": 300.0, "compute": 700.0}
            )

        history = self.optimizer.get_cost_history(periods=10)

        self.assertEqual(len(history), 5)


class TestIntegrationManager(unittest.TestCase):
    """Tests for integration manager."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = IntegrationManager()

    def test_register_integration(self):
        """Test registering integration."""
        health_check = MagicMock(return_value=True)

        result = self.manager.register_integration(
            "prometheus",
            "prometheus",
            {"url": "http://localhost:9090"},
            health_check
        )

        self.assertTrue(result)
        self.assertIn("prometheus", self.manager.integrations)

    def test_check_integration_health_connected(self):
        """Test health check for connected integration."""
        health_check = MagicMock(return_value=True)

        self.manager.register_integration(
            "prometheus",
            "prometheus",
            {"url": "http://localhost:9090"},
            health_check
        )

        status = self.manager.check_integration_health("prometheus")

        self.assertEqual(status, IntegrationStatus.CONNECTED)

    def test_check_integration_health_disconnected(self):
        """Test health check for disconnected integration."""
        health_check = MagicMock(return_value=False)

        self.manager.register_integration(
            "prometheus",
            "prometheus",
            {"url": "http://localhost:9090"},
            health_check
        )

        status = self.manager.check_integration_health("prometheus")

        self.assertEqual(status, IntegrationStatus.DEGRADED)

    def test_check_integration_health_error(self):
        """Test health check with error."""
        health_check = MagicMock(side_effect=Exception("Connection failed"))

        self.manager.register_integration(
            "prometheus",
            "prometheus",
            {"url": "http://localhost:9090"},
            health_check
        )

        status = self.manager.check_integration_health("prometheus")

        self.assertEqual(status, IntegrationStatus.ERROR)

    def test_get_integration_status(self):
        """Test getting integration status."""
        health_check = MagicMock(return_value=True)

        self.manager.register_integration(
            "prometheus",
            "prometheus",
            {"url": "http://localhost:9090"},
            health_check
        )

        self.manager.check_integration_health("prometheus")

        status = self.manager.get_integration_status()

        self.assertIn("prometheus", status)
        self.assertEqual(status["prometheus"]["status"], "connected")

    def test_send_to_integration_connected(self):
        """Test sending data to connected integration."""
        health_check = MagicMock(return_value=True)

        self.manager.register_integration(
            "prometheus",
            "prometheus",
            {"url": "http://localhost:9090"},
            health_check
        )

        self.manager.check_integration_health("prometheus")

        success, message = self.manager.send_to_integration(
            "prometheus",
            {"metric": "cpu_usage", "value": 50.0}
        )

        self.assertTrue(success)

    def test_send_to_integration_disconnected(self):
        """Test sending data to disconnected integration."""
        health_check = MagicMock(return_value=False)

        self.manager.register_integration(
            "prometheus",
            "prometheus",
            {"url": "http://localhost:9090"},
            health_check
        )

        self.manager.check_integration_health("prometheus")

        success, message = self.manager.send_to_integration(
            "prometheus",
            {"metric": "cpu_usage", "value": 50.0}
        )

        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
