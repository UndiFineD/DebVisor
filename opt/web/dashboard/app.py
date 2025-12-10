from flask import Blueprint, render_template, jsonify
import psutil
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard_bp.route("/")
def index():
    return render_template("dashboard.html")

@dashboard_bp.route("/api/stats")  # type: ignore[type-var]
def get_stats() -> None:
    """Get real-time system stats for the dashboard."""
    return jsonify(  # type: ignore[return-value]
        {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=0.1),            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage("/")._asdict(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        }
    )


@dashboard_bp.route("/api/alerts")  # type: ignore[type-var]
def get_alerts() -> None:
    """Get recent system alerts (mock)."""
    return jsonify(  # type: ignore[return-value]
        [
            {
                "id": 1,
                "severity": "warning",
                "message": "High CPU usage detected",
                "time": "10 mins ago",
            },
            {
                "id": 2,
                "severity": "info",
                "message": "Backup completed successfully",
                "time": "1 hour ago",
            },
        ]
    )