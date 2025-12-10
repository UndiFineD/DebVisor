"""
Standardized Health Check Blueprint.

Provides a factory to create a Flask Blueprint with standard
/health/live and /health/ready endpoints.
"""

import logging
from datetime import datetime
from typing import Callable, Dict, Any, Optional
from flask import Blueprint, jsonify

logger = logging.getLogger(__name__)


def create_health_blueprint(
    service_name: str,
    readiness_checks: Optional[Dict[str, Callable[[], Dict[str, Any]]]] = None
) -> Blueprint:
    """
    Create a standard health check blueprint.

    Args:
        service_name: Name of the service (e.g., "scheduler").
        readiness_checks: Dictionary of check functions. Each function should return
                        a dict with "status" ("ok", "error", "warning") and "message".

    Returns:
        Flask Blueprint with /health/live and /health/ready routes.
    """
    bp = Blueprint("health_standard", __name__, url_prefix="/health")
    checks = readiness_checks or {}

    @bp.route("/live", methods=["GET"])
    def liveness() -> Any:
        """Liveness probe."""
        return jsonify({
            "status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": service_name
        }), 200

    @bp.route("/ready", methods=["GET"])
    def readiness() -> Any:
        """Readiness probe."""
        results = {}
        all_healthy = True

        for check_name, check_func in checks.items():
            try:
                result = check_func()
                results[check_name] = result
                if result.get("status") == "error":
                    all_healthy = False
            except Exception as e:
                logger.error(f"Health check '{check_name}' failed: {e}")
                results[check_name] = {
                    "status": "error",
                    "message": str(e)
                }
                all_healthy = False

        status_code = 200 if all_healthy else 503
        response = {
            "status": "ready" if all_healthy else "not_ready",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": service_name,
            "checks": results
        }
        return jsonify(response), status_code

    return bp
