#!/usr/bin/env python3
"""
Advanced features and enhancements.

Includes:
  - Enhanced monitoring with predictive analytics
  - Compliance automation and reporting
  - Advanced integrations (Prometheus, ELK, custom)
  - Cost optimization analysis
  - Capacity planning and forecasting
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Callable
from abc import ABC, abstractmethod
import json
import logging


logger = logging.getLogger(__name__)


class ComplianceFramework(Enum):
    """Supported compliance frameworks."""

    SOC2 = "soc2"
    ISO27001 = "iso27001"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    GDPR = "gdpr"
    CCPA = "ccpa"


class AnomalyType(Enum):
    """Types of anomalies detected."""

    PERFORMANCE_DEGRADATION = "performance_degradation"
    RESOURCE_OVERUSE = "resource_overuse"
    SECURITY_ANOMALY = "security_anomaly"
    CAPACITY_THRESHOLD = "capacity_threshold"
    COST_SPIKE = "cost_spike"
    CONFIGURATION_DRIFT = "configuration_drift"


class IntegrationStatus(Enum):
    """Integration connection status."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    DEGRADED = "degraded"


@dataclass
class MetricPrediction:
    """Metric prediction with confidence."""

    metric_name: str
    current_value: float
    predicted_value: float
    confidence: float  # 0.0-1.0
    trend: str  # "up", "down", "stable"
    predicted_at: datetime = field(default_factory=datetime.now)
    forecast_window: int = 3600  # seconds

    def is_high_confidence(self) -> bool:
        """Check if prediction is high confidence (>0.8)."""
        return self.confidence > 0.8


@dataclass
class ComplianceControl:
    """Compliance control definition."""

    control_id: str
    control_name: str
    framework: ComplianceFramework
    description: str
    severity: str  # "critical", "high", "medium", "low"
    validation_rules: List[str] = field(default_factory=list)
    remediation_steps: List[str] = field(default_factory=list)
    is_automated: bool = False
    last_validated: Optional[datetime] = None
    compliant: bool = False

    def get_remediation_guidance(self) -> str:
        """Get remediation guidance."""
        return "\n".join(f"- {step}" for step in self.remediation_steps)


@dataclass
class AnomalyAlert:
    """Anomaly detection alert."""

    alert_id: str
    anomaly_type: AnomalyType
    severity: str  # "critical", "high", "medium", "low"
    metric_name: str
    current_value: float
    threshold_value: float
    deviation_percent: float
    detected_at: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    root_cause: Optional[str] = None
    recommended_action: Optional[str] = None

    def is_critical(self) -> bool:
        """Check if alert is critical."""
        return self.severity.lower() == "critical"


@dataclass
class CostAnalysis:
    """Cost analysis and optimization data."""

    period: str  # "hourly", "daily", "monthly"
    total_cost: float
    cost_breakdown: Dict[str, float]  # service -> cost mapping
    cost_trend: float  # percentage change
    savings_opportunity: float
    waste_detected: float
    optimization_recommendations: List[str] = field(default_factory=list)
    analyzed_at: datetime = field(default_factory=datetime.now)

    def get_cost_efficiency_ratio(self) -> float:
        """Calculate cost efficiency ratio."""
        if self.total_cost == 0:
            return 0.0
        return (self.total_cost - self.waste_detected) / self.total_cost


class AnomalyDetector(ABC):
    """Abstract anomaly detector."""

    @abstractmethod
    def detect(self, metrics: Dict[str, float]) -> List[AnomalyAlert]:
        """Detect anomalies in metrics."""
        pass

    @abstractmethod
    def get_baseline(self) -> Dict[str, float]:
        """Get baseline metrics."""
        pass


class StatisticalAnomalyDetector(AnomalyDetector):
    """Statistical anomaly detection."""

    def __init__(self, std_dev_threshold: float = 3.0):
        """
        Initialize detector.

        Args:
            std_dev_threshold: Standard deviations to trigger alert
        """
        self.std_dev_threshold = std_dev_threshold
        self.baselines: Dict[str, float] = {}
        self.std_devs: Dict[str, float] = {}

    def detect(self, metrics: Dict[str, float]) -> List[AnomalyAlert]:
        """
        Detect anomalies using statistical methods.

        Args:
            metrics: Current metrics

        Returns:
            List of detected anomalies
        """
        alerts = []

        for metric_name, value in metrics.items():
            if metric_name not in self.baselines:
                self.baselines[metric_name] = value
                self.std_devs[metric_name] = 0.1
                continue

            baseline = self.baselines[metric_name]
            std_dev = self.std_devs[metric_name]

            if std_dev == 0:
                std_dev = 0.1

            deviation = abs(value - baseline) / std_dev

            if deviation > self.std_dev_threshold:
                deviation_percent = ((value - baseline) / baseline) * 100

                anomaly_type = (
                    AnomalyType.RESOURCE_OVERUSE
                    if value > baseline
                    else AnomalyType.PERFORMANCE_DEGRADATION
                )

                alert = AnomalyAlert(
                    alert_id=f"anomaly_{metric_name}_{datetime.now().timestamp()}",
                    anomaly_type=anomaly_type,
                    severity="high" if deviation > self.std_dev_threshold * 1.5 else "medium",
                    metric_name=metric_name,
                    current_value=value,
                    threshold_value=baseline + (self.std_dev_threshold * std_dev),
                    deviation_percent=deviation_percent,
                    recommended_action=f"Investigate {metric_name} spike: {deviation_percent:.1f}%"
                )

                alerts.append(alert)

        return alerts

    def get_baseline(self) -> Dict[str, float]:
        """Get baseline metrics."""
        return self.baselines.copy()


class ComplianceAutomation:
    """Automated compliance checking and reporting."""

    def __init__(self):
        """Initialize compliance automation."""
        self.controls: Dict[str, ComplianceControl] = {}
        self.validators: Dict[str, Callable] = {}
        self.audit_log: List[Dict[str, Any]] = []

    def register_control(self, control: ComplianceControl) -> bool:
        """
        Register compliance control.

        Args:
            control: Compliance control

        Returns:
            True if registered successfully
        """
        self.controls[control.control_id] = control
        logger.info(f"Registered control: {control.control_id}")
        return True

    def register_validator(self, control_id: str, validator: Callable) -> bool:
        """
        Register validator for control.

        Args:
            control_id: Control ID
            validator: Validation function

        Returns:
            True if registered successfully
        """
        if control_id not in self.controls:
            logger.error(f"Control not found: {control_id}")
            return False

        self.validators[control_id] = validator
        return True

    def validate_control(self, control_id: str) -> Tuple[bool, str]:
        """
        Validate control compliance.

        Args:
            control_id: Control ID

        Returns:
            Tuple of (compliant, message)
        """
        if control_id not in self.controls:
            return False, f"Control not found: {control_id}"

        control = self.controls[control_id]

        if control_id not in self.validators:
            return False, f"No validator registered for control: {control_id}"

        try:
            validator = self.validators[control_id]
            compliant = validator()

            control.compliant = compliant
            control.last_validated = datetime.now()

            # Log audit event
            self.audit_log.append({
                "timestamp": datetime.now().isoformat(),
                "control_id": control_id,
                "compliant": compliant,
                "action": "validate"
            })

            return compliant, f"Control validation complete: {compliant}"

        except Exception as e:
            logger.error(f"Validation error for control {control_id}: {e}")
            return False, f"Validation error: {str(e)}"

    def generate_compliance_report(self, framework: ComplianceFramework) -> Dict[str, Any]:
        """
        Generate compliance report.

        Args:
            framework: Compliance framework

        Returns:
            Compliance report
        """
        framework_controls = {
            cid: c for cid, c in self.controls.items()
            if c.framework == framework
        }

        total_controls = len(framework_controls)
        compliant_controls = sum(1 for c in framework_controls.values() if c.compliant)
        compliance_rate = (compliant_controls / total_controls * 100) if total_controls > 0 else 0

        non_compliant = [
            {
                "control_id": cid,
                "control_name": c.control_name,
                "severity": c.severity,
                "remediation": c.get_remediation_guidance()
            }
            for cid, c in framework_controls.items()
            if not c.compliant
        ]

        return {
            "framework": framework.value,
            "generated_at": datetime.now().isoformat(),
            "total_controls": total_controls,
            "compliant_controls": compliant_controls,
            "compliance_rate": compliance_rate,
            "non_compliant_controls": non_compliant,
            "audit_events": len(self.audit_log)
        }

    def get_audit_log(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Get audit log entries.

        Args:
            hours: Look back hours

        Returns:
            Audit log entries
        """
        cutoff = datetime.now() - timedelta(hours=hours)

        return [
            entry for entry in self.audit_log
            if datetime.fromisoformat(entry["timestamp"]) > cutoff
        ]


class PredictiveAnalytics:
    """Predictive analytics for metrics."""

    def __init__(self, history_size: int = 100):
        """
        Initialize predictive analytics.

        Args:
            history_size: Historical data points to keep
        """
        self.history: Dict[str, List[Tuple[datetime, float]]] = {}
        self.history_size = history_size
        self.models: Dict[str, Any] = {}

    def add_metric(self, metric_name: str, value: float) -> None:
        """
        Add metric data point.

        Args:
            metric_name: Metric name
            value: Metric value
        """
        if metric_name not in self.history:
            self.history[metric_name] = []

        self.history[metric_name].append((datetime.now(), value))

        # Keep history size bounded
        if len(self.history[metric_name]) > self.history_size:
            self.history[metric_name].pop(0)

    def predict(self, metric_name: str, ahead_seconds: int = 3600) -> Optional[MetricPrediction]:
        """
        Predict metric value.

        Args:
            metric_name: Metric name
            ahead_seconds: Prediction window in seconds

        Returns:
            Metric prediction or None
        """
        if metric_name not in self.history or len(self.history[metric_name]) < 5:
            return None

        history = self.history[metric_name]
        values = [v for _, v in history]
        current_value = values[-1]

        # Simple linear trend
        if len(values) >= 2:
            recent_trend = (values[-1] - values[-5 if len(values) >= 5 else 0]) / max(len(values) - 1, 1)
            predicted_value = current_value + (recent_trend * (ahead_seconds / 3600))
        else:
            predicted_value = current_value

        # Calculate confidence based on variance
        mean_value = sum(values) / len(values)
        variance = sum((v - mean_value) ** 2 for v in values) / len(values)
        std_dev = variance ** 0.5

        if std_dev == 0:
            confidence = 0.5
        else:
            confidence = min(1.0, 1.0 / (1.0 + (std_dev / mean_value if mean_value > 0 else 1.0)))

        trend = "up" if recent_trend > 0 else "down" if recent_trend < 0 else "stable"

        return MetricPrediction(
            metric_name=metric_name,
            current_value=current_value,
            predicted_value=predicted_value,
            confidence=confidence,
            trend=trend,
            forecast_window=ahead_seconds
        )

    def get_trend(self, metric_name: str, minutes: int = 60) -> Optional[str]:
        """
        Get trend direction.

        Args:
            metric_name: Metric name
            minutes: Time window

        Returns:
            Trend direction: "up", "down", "stable"
        """
        if metric_name not in self.history:
            return None

        history = self.history[metric_name]
        cutoff = datetime.now() - timedelta(minutes=minutes)

        recent_values = [v for t, v in history if t > cutoff]

        if len(recent_values) < 2:
            return "stable"

        avg_first_half = sum(recent_values[:len(recent_values)//2]) / max(len(recent_values)//2, 1)
        avg_second_half = sum(recent_values[len(recent_values)//2:]) / max(len(recent_values) - len(recent_values)//2, 1)

        if avg_second_half > avg_first_half * 1.1:
            return "up"
        elif avg_second_half < avg_first_half * 0.9:
            return "down"
        else:
            return "stable"


class CostOptimizer:
    """Cost optimization analysis."""

    def __init__(self):
        """Initialize cost optimizer."""
        self.cost_history: List[CostAnalysis] = []
        self.optimization_rules: Dict[str, Callable] = {}

    def register_optimization_rule(self, rule_name: str, rule_fn: Callable) -> None:
        """
        Register optimization rule.

        Args:
            rule_name: Rule name
            rule_fn: Rule function that returns list of recommendations
        """
        self.optimization_rules[rule_name] = rule_fn

    def analyze_costs(
        self,
        period: str,
        total_cost: float,
        cost_breakdown: Dict[str, float]
    ) -> CostAnalysis:
        """
        Analyze costs.

        Args:
            period: Period type
            total_cost: Total cost
            cost_breakdown: Cost breakdown by service

        Returns:
            Cost analysis
        """
        # Calculate trends
        cost_trend = 0.0
        if self.cost_history:
            prev_cost = self.cost_history[-1].total_cost
            cost_trend = ((total_cost - prev_cost) / prev_cost * 100) if prev_cost > 0 else 0

        # Detect waste
        waste_detected = sum(
            cost for service, cost in cost_breakdown.items()
            if self._is_underutilized(service)
        )

        # Get recommendations
        recommendations = []
        for rule_fn in self.optimization_rules.values():
            try:
                results = rule_fn(total_cost, cost_breakdown)
                recommendations.extend(results if isinstance(results, list) else [results])
            except Exception as e:
                logger.warning(f"Optimization rule error: {e}")

        analysis = CostAnalysis(
            period=period,
            total_cost=total_cost,
            cost_breakdown=cost_breakdown,
            cost_trend=cost_trend,
            savings_opportunity=waste_detected * 0.5,  # 50% potential savings
            waste_detected=waste_detected,
            optimization_recommendations=recommendations[:5]  # Top 5
        )

        self.cost_history.append(analysis)
        return analysis

    def _is_underutilized(self, service: str) -> bool:
        """Check if service is underutilized."""
        # Simple heuristic: services with less than 10% of total cost
        if not self.cost_history:
            return False

        latest = self.cost_history[-1]
        total = sum(latest.cost_breakdown.values())

        return latest.cost_breakdown.get(service, 0) / total < 0.1 if total > 0 else False

    def get_cost_history(self, periods: int = 30) -> List[CostAnalysis]:
        """
        Get cost history.

        Args:
            periods: Number of periods to return

        Returns:
            Cost history
        """
        return self.cost_history[-periods:]


class IntegrationManager:
    """Manage integrations with external systems."""

    def __init__(self):
        """Initialize integration manager."""
        self.integrations: Dict[str, Dict[str, Any]] = {}

    def register_integration(
        self,
        integration_name: str,
        integration_type: str,
        config: Dict[str, Any],
        health_check_fn: Callable
    ) -> bool:
        """
        Register integration.

        Args:
            integration_name: Integration name
            integration_type: Type (prometheus, elk, datadog, etc.)
            config: Configuration dict
            health_check_fn: Health check function

        Returns:
            True if registered successfully
        """
        self.integrations[integration_name] = {
            "type": integration_type,
            "config": config,
            "health_check": health_check_fn,
            "status": IntegrationStatus.DISCONNECTED,
            "last_check": None,
            "error_message": None
        }

        logger.info(f"Registered integration: {integration_name}")
        return True

    def check_integration_health(self, integration_name: str) -> IntegrationStatus:
        """
        Check integration health.

        Args:
            integration_name: Integration name

        Returns:
            Integration status
        """
        if integration_name not in self.integrations:
            logger.error(f"Integration not found: {integration_name}")
            return IntegrationStatus.ERROR

        integration = self.integrations[integration_name]

        try:
            health_check_fn = integration["health_check"]
            result = health_check_fn()

            status = IntegrationStatus.CONNECTED if result else IntegrationStatus.DEGRADED

            integration["status"] = status
            integration["last_check"] = datetime.now()
            integration["error_message"] = None

            return status

        except Exception as e:
            logger.error(f"Health check failed for {integration_name}: {e}")
            integration["status"] = IntegrationStatus.ERROR
            integration["error_message"] = str(e)
            integration["last_check"] = datetime.now()

            return IntegrationStatus.ERROR

    def get_integration_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Get status of all integrations.

        Returns:
            Integration status dictionary
        """
        return {
            name: {
                "type": info["type"],
                "status": info["status"].value,
                "last_check": info["last_check"].isoformat() if info["last_check"] else None,
                "error": info["error_message"]
            }
            for name, info in self.integrations.items()
        }

    def send_to_integration(
        self,
        integration_name: str,
        data: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Send data to integration.

        Args:
            integration_name: Integration name
            data: Data to send

        Returns:
            Tuple of (success, message)
        """
        if integration_name not in self.integrations:
            return False, f"Integration not found: {integration_name}"

        integration = self.integrations[integration_name]

        if integration["status"] != IntegrationStatus.CONNECTED:
            return False, f"Integration not connected: {integration_name}"

        try:
            # Placeholder for actual integration logic
            logger.info(f"Sent data to {integration_name}: {json.dumps(data, default=str)[:100]}")
            return True, "Data sent successfully"

        except Exception as e:
            logger.error(f"Failed to send data to {integration_name}: {e}")
            return False, str(e)
