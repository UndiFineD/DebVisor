"""
ML Anomaly Detection - REST API

HTTP interface for anomaly detection operations.

Author: DebVisor Development Team
Version: 1.0.0
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

try:
    from flask import Flask, request

    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

from opt.services.anomaly.core import (
    get_anomaly_engine,
    AnomalyDetectionEngine,
    MetricType,
    SeverityLevel,
    DetectionMethod,
)
from opt.core.health import create_health_blueprint

# Configure logging
try:
    from opt.core.logging import configure_logging
except ImportError:

    def configure_logging(**kwargs) -> None:
        pass


class AnomalyAPI:
    """REST API for anomaly detection."""

    def __init__(self, engine: AnomalyDetectionEngine) -> None:
        """Initialize API.

        Args:
            engine: AnomalyDetectionEngine instance
        """
        self.engine = engine
        self.logger = logging.getLogger("DebVisor.AnomalyAPI")

    def _json_response(self, data: Any, status_code: int = 200) -> Tuple[str, int]:
        """Create JSON response.

        Args:
            data: Response data
            status_code: HTTP status code

        Returns:
            Tuple of (json_string, status_code)
        """
        return json.dumps(data), status_code

    def _error_response(
        self, message: str, status_code: int = 400, details: Optional[Dict] = None
    ) -> Tuple[str, int]:
        """Create error response.

        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details

        Returns:
            Tuple of (json_string, status_code)
        """
        error = {
            "error": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if details:
            error["details"] = details

        return json.dumps(error), status_code

    # ========================================================================
    # Metric Endpoints
    # ========================================================================

    def add_metric(self) -> Tuple[str, int]:
        """POST /metrics - Add metric data point.

        Request:
            {
                "resource_id": "vm-001",
                "metric_type": "cpu_usage",
                "value": 75.5
            }
        """
        try:
            data = request.get_json()

            if not data:
                return self._error_response("No JSON data provided", 400)

            resource_id = data.get("resource_id")
            metric_type_str = data.get("metric_type")
            value = data.get("value")

            if not resource_id or not metric_type_str or value is None:
                return self._error_response(
                    "Missing required fields",
                    400,
                    {"required": ["resource_id", "metric_type", "value"]},
                )

            try:
                metric_type = MetricType[metric_type_str.upper().replace("-", "_")]
            except KeyError:
                return self._error_response(
                    f"Unknown metric type: {metric_type_str}", 400
                )

            self.engine.add_metric(resource_id, metric_type, value)

            return self._json_response(
                {
                    "status": "success",
                    "message": "Metric added",
                    "resource_id": resource_id,
                    "metric_type": metric_type_str,
                    "value": value,
                },
                201,
            )

        except Exception as e:
            self.logger.error(f"Error adding metric: {e}")
            return self._error_response(str(e), 500)

    def list_metrics(self) -> Tuple[str, int]:
        """GET /metrics - List metrics.

        Query params:
            resource_id: Optional filter by resource
            metric_type: Optional filter by metric type
        """
        try:
            resource_filter = request.args.get("resource_id")
            metric_filter = request.args.get("metric_type")

            metrics_list = []

            for (resource_id, metric_type), history in self.engine.metrics.items():
                if resource_filter and resource_id != resource_filter:
                    continue
                if metric_filter and metric_type.value != metric_filter:
                    continue

                metrics_list.append(
                    {
                        "resource_id": resource_id,
                        "metric_type": metric_type.value,
                        "point_count": len(history),
                        "latest_value": history[-1].value if history else None,
                        "latest_timestamp": (
                            history[-1].timestamp.isoformat() if history else None
                        ),
                    }
                )

            return self._json_response(
                {
                    "status": "success",
                    "count": len(metrics_list),
                    "metrics": metrics_list,
                },
                200,
            )

        except Exception as e:
            self.logger.error(f"Error listing metrics: {e}")
            return self._error_response(str(e), 500)

    def get_metric_history(
        self, resource_id: str, metric_type_str: str
    ) -> Tuple[str, int]:
        """GET /metrics/{resource_id}/{metric_type} - Get metric history.

        Query params:
            limit: Maximum records (default: 50)
        """
        try:
            limit = int(request.args.get("limit", 50))

            try:
                metric_type = MetricType[metric_type_str.upper().replace("-", "_")]
            except KeyError:
                return self._error_response(
                    f"Unknown metric type: {metric_type_str}", 400
                )

            key = (resource_id, metric_type)

            if key not in self.engine.metrics:
                return self._error_response(
                    f"No data for {resource_id}/{metric_type_str}", 404
                )

            history = list(self.engine.metrics[key])[-limit:]

            return self._json_response(
                {
                    "status": "success",
                    "resource_id": resource_id,
                    "metric_type": metric_type_str,
                    "count": len(history),
                    "data": [
                        {"timestamp": p.timestamp.isoformat(), "value": p.value}
                        for p in history
                    ],
                },
                200,
            )

        except ValueError:
            return self._error_response("Invalid limit parameter", 400)
        except Exception as e:
            self.logger.error(f"Error getting history: {e}")
            return self._error_response(str(e), 500)

    # ========================================================================
    # Baseline Endpoints
    # ========================================================================

    def establish_baseline(self) -> Tuple[str, int]:
        """POST /baselines - Establish baseline.

        Request:
            {
                "resource_id": "vm-001",
                "metric_type": "cpu_usage",
                "percentile_based": false
            }
        """
        try:
            data = request.get_json()

            if not data:
                return self._error_response("No JSON data provided", 400)

            resource_id = data.get("resource_id")
            metric_type_str = data.get("metric_type")
            percentile_based = data.get("percentile_based", False)

            if not resource_id or not metric_type_str:
                return self._error_response(
                    "Missing required fields",
                    400,
                    {"required": ["resource_id", "metric_type"]},
                )

            try:
                metric_type = MetricType[metric_type_str.upper().replace("-", "_")]
            except KeyError:
                return self._error_response(
                    f"Unknown metric type: {metric_type_str}", 400
                )

            baseline = self.engine.establish_baseline(
                resource_id, metric_type, percentile_based=percentile_based
            )

            if not baseline:
                return self._error_response(
                    "Failed to establish baseline (insufficient data)", 400
                )

            return self._json_response(
                {"status": "success", "baseline": baseline.to_dict()}, 201
            )

        except Exception as e:
            self.logger.error(f"Error establishing baseline: {e}")
            return self._error_response(str(e), 500)

    def list_baselines(self) -> Tuple[str, int]:
        """GET /baselines - List baselines.

        Query params:
            resource_id: Optional filter by resource
        """
        try:
            resource_filter = request.args.get("resource_id")

            baselines_list = []

            for (resource_id, metric_type), baseline in self.engine.baselines.items():
                if resource_filter and resource_id != resource_filter:
                    continue

                baselines_list.append(baseline.to_dict())

            return self._json_response(
                {
                    "status": "success",
                    "count": len(baselines_list),
                    "baselines": baselines_list,
                },
                200,
            )

        except Exception as e:
            self.logger.error(f"Error listing baselines: {e}")
            return self._error_response(str(e), 500)

    def get_baseline(self, resource_id: str, metric_type_str: str) -> Tuple[str, int]:
        """GET /baselines/{resource_id}/{metric_type} - Get baseline details."""
        try:
            try:
                metric_type = MetricType[metric_type_str.upper().replace("-", "_")]
            except KeyError:
                return self._error_response(
                    f"Unknown metric type: {metric_type_str}", 400
                )

            key = (resource_id, metric_type)

            if key not in self.engine.baselines:
                return self._error_response(
                    f"Baseline not found for {resource_id}/{metric_type_str}", 404
                )

            baseline = self.engine.baselines[key]

            return self._json_response(
                {"status": "success", "baseline": baseline.to_dict()}, 200
            )

        except Exception as e:
            self.logger.error(f"Error getting baseline: {e}")
            return self._error_response(str(e), 500)

    # ========================================================================
    # Detection Endpoints
    # ========================================================================

    def detect_anomalies(self) -> Tuple[str, int]:
        """POST /detect - Detect anomalies.

        Request:
            {
                "resource_id": "vm-001",
                "metric_type": "cpu_usage",
                "value": 95.5,
                "methods": ["z_score", "iqr"]
            }
        """
        try:
            data = request.get_json()

            if not data:
                return self._error_response("No JSON data provided", 400)

            resource_id = data.get("resource_id")
            metric_type_str = data.get("metric_type")
            value = data.get("value")
            methods_str = data.get("methods", ["z_score", "iqr", "ewma"])

            if not resource_id or not metric_type_str or value is None:
                return self._error_response(
                    "Missing required fields",
                    400,
                    {"required": ["resource_id", "metric_type", "value"]},
                )

            try:
                metric_type = MetricType[metric_type_str.upper().replace("-", "_")]
            except KeyError:
                return self._error_response(
                    f"Unknown metric type: {metric_type_str}", 400
                )

            # Parse detection methods
            methods = []
            for method_str in methods_str:
                try:
                    methods.append(DetectionMethod[method_str.upper()])
                except KeyError:
                    return self._error_response(
                        f"Unknown detection method: {method_str}", 400
                    )

            # Add metric and detect
            self.engine.add_metric(resource_id, metric_type, value)
            alerts = self.engine.detect_anomalies(
                resource_id, metric_type, value, methods
            )

            return self._json_response(
                {
                    "status": "success",
                    "anomalies_detected": len(alerts),
                    "alerts": [a.to_dict() for a in alerts],
                },
                200,
            )

        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {e}")
            return self._error_response(str(e), 500)

    def get_recent_detections(self) -> Tuple[str, int]:
        """GET /detect/recent - Get recent detections.

        Query params:
            resource_id: Optional filter
            hours: Look back hours (default: 24)
            limit: Maximum results (default: 50)
        """
        try:
            resource_filter = request.args.get("resource_id")
            hours = int(request.args.get("hours", 24))
            limit = int(request.args.get("limit", 50))

            alerts = self.engine.get_alert_history(
                resource_id=resource_filter, hours=hours, limit=limit
            )

            return self._json_response(
                {
                    "status": "success",
                    "count": len(alerts),
                    "detections": [a.to_dict() for a in alerts],
                },
                200,
            )

        except ValueError:
            return self._error_response("Invalid query parameters", 400)
        except Exception as e:
            self.logger.error(f"Error getting detections: {e}")
            return self._error_response(str(e), 500)

    # ========================================================================
    # Alert Endpoints
    # ========================================================================

    def list_alerts(self) -> Tuple[str, int]:
        """GET /alerts - List active alerts.

        Query params:
            resource_id: Optional filter
            severity: Optional filter (info, warning, critical)
        """
        try:
            resource_filter = request.args.get("resource_id")
            severity_str = request.args.get("severity")

            severity = None
            if severity_str:
                try:
                    severity = SeverityLevel[severity_str.upper()]
                except KeyError:
                    return self._error_response(
                        f"Unknown severity level: {severity_str}", 400
                    )

            alerts = self.engine.get_active_alerts(
                resource_id=resource_filter, severity=severity
            )

            return self._json_response(
                {
                    "status": "success",
                    "count": len(alerts),
                    "alerts": [a.to_dict() for a in alerts],
                },
                200,
            )

        except Exception as e:
            self.logger.error(f"Error listing alerts: {e}")
            return self._error_response(str(e), 500)

    def get_alert_history(self) -> Tuple[str, int]:
        """GET /alerts/history - Get alert history.

        Query params:
            resource_id: Optional filter
            hours: Look back hours (default: 24)
            limit: Maximum results (default: 100)
        """
        try:
            resource_filter = request.args.get("resource_id")
            hours = int(request.args.get("hours", 24))
            limit = int(request.args.get("limit", 100))

            alerts = self.engine.get_alert_history(
                resource_id=resource_filter, hours=hours, limit=limit
            )

            return self._json_response(
                {
                    "status": "success",
                    "count": len(alerts),
                    "history": [a.to_dict() for a in alerts],
                },
                200,
            )

        except ValueError:
            return self._error_response("Invalid query parameters", 400)
        except Exception as e:
            self.logger.error(f"Error getting alert history: {e}")
            return self._error_response(str(e), 500)

    def acknowledge_alert(self) -> Tuple[str, int]:
        """POST /alerts/{alert_id}/acknowledge - Acknowledge alert.

        Request:
            {
                "acknowledged_by": "admin",
                "notes": "Investigating issue"
            }
        """
        alert_id = request.view_args.get("alert_id")

        try:
            data = request.get_json()

            if not data:
                return self._error_response("No JSON data provided", 400)

            acknowledged_by = data.get("acknowledged_by")
            notes = data.get("notes", "")

            if not acknowledged_by:
                return self._error_response(
                    "Missing required field: acknowledged_by", 400
                )

            success = self.engine.acknowledge_alert(alert_id, acknowledged_by, notes)

            if success:
                return self._json_response(
                    {
                        "status": "success",
                        "message": "Alert acknowledged",
                        "alert_id": alert_id,
                    },
                    200,
                )
            else:
                return self._error_response(f"Alert not found: {alert_id}", 404)

        except Exception as e:
            self.logger.error(f"Error acknowledging alert: {e}")
            return self._error_response(str(e), 500)

    def get_alert(self, alert_id: str) -> Tuple[str, int]:
        """GET /alerts/{alert_id} - Get alert details."""
        try:
            for alert in self.engine.alerts:
                if alert.alert_id == alert_id:
                    return self._json_response(
                        {"status": "success", "alert": alert.to_dict()}, 200
                    )

            return self._error_response(f"Alert not found: {alert_id}", 404)

        except Exception as e:
            self.logger.error(f"Error getting alert: {e}")
            return self._error_response(str(e), 500)

    # ========================================================================
    # Trend Endpoints
    # ========================================================================

    def analyze_trend(self) -> Tuple[str, int]:
        """POST /trends - Analyze trend.

        Request:
            {
                "resource_id": "vm-001",
                "metric_type": "cpu_usage",
                "hours": 24
            }
        """
        try:
            data = request.get_json()

            if not data:
                return self._error_response("No JSON data provided", 400)

            resource_id = data.get("resource_id")
            metric_type_str = data.get("metric_type")
            hours = data.get("hours", 24)

            if not resource_id or not metric_type_str:
                return self._error_response(
                    "Missing required fields",
                    400,
                    {"required": ["resource_id", "metric_type"]},
                )

            try:
                metric_type = MetricType[metric_type_str.upper().replace("-", "_")]
            except KeyError:
                return self._error_response(
                    f"Unknown metric type: {metric_type_str}", 400
                )

            trend = self.engine.analyze_trend(resource_id, metric_type, hours=hours)

            if trend:
                return self._json_response(
                    {"status": "success", "trend": trend.to_dict()}, 201
                )
            else:
                return self._error_response("Insufficient data for trend analysis", 400)

        except Exception as e:
            self.logger.error(f"Error analyzing trend: {e}")
            return self._error_response(str(e), 500)

    def list_trends(self) -> Tuple[str, int]:
        """GET /trends - List trends.

        Query params:
            resource_id: Optional filter
        """
        try:
            resource_filter = request.args.get("resource_id")

            trends_list = []

            for (resource_id, metric_type), trend in self.engine.trends.items():
                if resource_filter and resource_id != resource_filter:
                    continue

                trends_list.append(trend.to_dict())

            return self._json_response(
                {"status": "success", "count": len(trends_list), "trends": trends_list},
                200,
            )

        except Exception as e:
            self.logger.error(f"Error listing trends: {e}")
            return self._error_response(str(e), 500)

    # ========================================================================
    # System Endpoints
    # ========================================================================

    def get_statistics(self) -> Tuple[str, int]:
        """GET /system/stats - Get system statistics."""
        try:
            stats = self.engine.get_statistics()

            return self._json_response({"status": "success", "statistics": stats}, 200)

        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return self._error_response(str(e), 500)

    def get_health(self) -> Tuple[str, int]:
        """GET /health - Health check."""
        return self._json_response(
            {
                "status": "healthy",
                "service": "anomaly-detection",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            200,
        )


# ============================================================================
# Flask Integration
# ============================================================================


def create_flask_app(engine: Optional[AnomalyDetectionEngine] = None) -> Any:
    """Create Flask application.

    Args:
        engine: AnomalyDetectionEngine instance (default: global instance)

    Returns:
        Flask application
    """
    if not HAS_FLASK:
        raise ImportError("Flask is required for REST API support")

    if engine is None:
        engine = get_anomaly_engine()

    app = Flask(__name__)

    # Load and validate configuration (INFRA-003)
    from opt.core.config import Settings
    settings = Settings.load_validated_config()
    app.config["SETTINGS"] = settings

    # Initialize graceful shutdown
    from opt.web.panel.graceful_shutdown import init_graceful_shutdown

    shutdown_manager = init_graceful_shutdown(app)

    # Register standard health checks
    def check_anomaly_engine() -> bool:
        return engine is not None

    shutdown_manager.register_health_check("engine", check_anomaly_engine)

    api = AnomalyAPI(engine)

    # ========================================================================
    # Metric Routes
    # ========================================================================

    @app.route("/metrics", methods=["POST"])
    def add_metric() -> Any:
        return api.add_metric()

    @app.route("/metrics", methods=["GET"])
    def list_metrics() -> Any:
        return api.list_metrics()

    @app.route("/metrics/<resource_id>/<metric_type>", methods=["GET"])
    def get_metric_history(resource_id: str, metric_type: str) -> Any:
        return api.get_metric_history(resource_id, metric_type)

    # ========================================================================
    # Baseline Routes
    # ========================================================================

    @app.route("/baselines", methods=["POST"])
    def establish_baseline() -> Any:
        return api.establish_baseline()

    @app.route("/baselines", methods=["GET"])
    def list_baselines() -> Any:
        return api.list_baselines()

    @app.route("/baselines/<resource_id>/<metric_type>", methods=["GET"])
    def get_baseline(resource_id: str, metric_type: str) -> Any:
        return api.get_baseline(resource_id, metric_type)

    # ========================================================================
    # Detection Routes
    # ========================================================================

    @app.route("/detect", methods=["POST"])
    def detect_anomalies() -> Any:
        return api.detect_anomalies()

    @app.route("/detect/recent", methods=["GET"])
    def get_recent_detections() -> Any:
        return api.get_recent_detections()

    # ========================================================================
    # Alert Routes
    # ========================================================================

    @app.route("/alerts", methods=["GET"])
    def list_alerts() -> Any:
        return api.list_alerts()

    @app.route("/alerts/history", methods=["GET"])
    def get_alert_history() -> Any:
        return api.get_alert_history()

    @app.route("/alerts/<alert_id>", methods=["GET"])
    def get_alert(alert_id: str) -> Any:
        return api.get_alert(alert_id)

    @app.route("/alerts/<alert_id>/acknowledge", methods=["POST"])
    def acknowledge_alert(alert_id: str) -> Any:
        request.view_args = {"alert_id": alert_id}
        return api.acknowledge_alert()

    # ========================================================================
    # Trend Routes
    # ========================================================================

    @app.route("/trends", methods=["POST"])
    def analyze_trend() -> Any:
        return api.analyze_trend()

    @app.route("/trends", methods=["GET"])
    def list_trends() -> Any:
        return api.list_trends()

    # ========================================================================
    # System Routes
    # ========================================================================

    @app.route("/system/stats", methods=["GET"])
    def get_statistics() -> Any:
        return api.get_statistics()

    @app.route("/health", methods=["GET"])
    def get_health() -> Any:
        return api.get_health()

    return app


if __name__ == "__main__":
    if not HAS_FLASK:
        print("Flask is required to run the API server")
        print("Install with: pip install flask")
        sys.exit(1)

    configure_logging(service_name="anomaly-detection-api")

    engine = get_anomaly_engine()
    app = create_flask_app(engine)
    app.run(host="0.0.0.0", port=5000, debug=False)  # nosec B104
