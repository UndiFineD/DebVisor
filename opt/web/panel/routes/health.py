# !/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
Health Check Endpoints for Kubernetes Probes
Implements liveness and readiness checks for production deployments.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict
from flask import Blueprint, jsonify
from sqlalchemy import text
from opt.web.panel.extensions import limiter

logger = logging.getLogger(__name__)

health_bp = Blueprint("health", __name__, url_prefix="/health")


@health_bp.route("/live", methods=["GET"])
@limiter.limit("100 per minute")    # type: ignore
def liveness() -> Any:
    """
    Liveness probe - indicates if the application is running.

    Returns 200 if the process is alive, 503 if it should be restarted.
    Used by Kubernetes liveness probes.
    """
    try:
    # Basic health check - can the app respond?
        return (
            jsonify(
                {
                    "status": "ok",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "service": "debvisor-web-panel",
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Liveness check failed: {e}")
        return jsonify({"status": "error", "error": "Service unavailable"}), 503


@health_bp.route("/ready", methods=["GET"])
@limiter.limit("100 per minute")    # type: ignore
def readiness() -> Any:
    """
    Readiness probe - indicates if the application is ready to serve traffic.

    Returns 200 if ready, 503 if not ready (dependencies unavailable).
    Used by Kubernetes readiness probes.
    """
    health_checks = {
        "database": _check_database(),
        "disk": _check_disk_space(),
    }

    # Check if all dependencies are healthy
    all_healthy = all(check["status"] == "ok" for check in health_checks.values())
    status_code = 200 if all_healthy else 503

    response = {
        "status": "ready" if all_healthy else "not_ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": health_checks,
    }

    return jsonify(response), status_code


def _check_database() -> Dict[str, Any]:
    """Check database connectivity."""
    try:
        from opt.web.panel.extensions import db

        # Execute simple query to verify connection
        db.session.execute(text("SELECT 1"))
        db.session.commit()

        return {"status": "ok", "message": "Database connection healthy"}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {"status": "error", "message": "Database unavailable"}


def _check_disk_space() -> Dict[str, Any]:
    """Check available disk space."""
    try:
        import shutil

        # Check root filesystem
        total, used, free = shutil.disk_usage("/")
        free_percent = (free / total) * 100

        # Warn if less than 10% free
        if free_percent < 10:
            return {
                "status": "warning",
                "message": f"Low disk space: {free_percent:.1f}% free",
                "free_gb": free // (1024**3),
                "total_gb": total // (1024**3),
            }

        return {
            "status": "ok",
            "message": f"Disk space healthy: {free_percent:.1f}% free",
            "free_gb": free // (1024**3),
            "total_gb": total // (1024**3),
        }
    except Exception as e:
        logger.warning(f"Disk space check failed: {e}")
        return {"status": "unknown", "message": "Could not check disk space"}


@health_bp.route("/startup", methods=["GET"])
def startup() -> Any:
    """
    Startup probe - indicates if the application has finished starting.

    Returns 200 when startup is complete, 503 during startup.
    Used by Kubernetes startup probes for slow-starting applications.
    """
    # Check if critical initialization is complete
    try:
        from opt.web.panel.extensions import db

        # Verify database tables exist
        db.session.execute(text("SELECT 1"))

        return (
            jsonify(
                {
                    "status": "started",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "message": "Application startup complete",
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Startup check failed: {e}")
        return (
            jsonify(
                {"status": "starting", "message": "Startup in progress"}
            ),
            503,
        )
