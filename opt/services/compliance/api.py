from flask import Blueprint, jsonify, Response, Flask, request
from typing import Any, Union, Tuple, Dict
from .core import ComplianceEngine
from .gdpr import GDPRManager
from opt.core.health import create_health_blueprint

compliance_bp = Blueprint("compliance", __name__)
engine = ComplianceEngine()
gdpr_manager = GDPRManager()

# Mock resources
mock_resources = [
    {"id": "vm-compliant-1", "type": "vm"},
    {"id": "vm-noncompliant-1", "type": "vm"},
    {"id": "host-prod-1", "type": "host"},
]


@compliance_bp.route("/scan", methods=["POST"])
def run_scan() -> Response:
    from flask import request

    standard = request.args.get("standard")  # e.g., ?standard=GDPR
    report = engine.run_compliance_scan(mock_resources, standard=standard)
    return jsonify(report.__dict__)


@compliance_bp.route("/reports/<standard>", methods=["GET"])
def generate_report(standard: str) -> Response:
    """Generate a specific compliance report (GDPR, SOC2, HIPAA)."""
    report = engine.run_compliance_scan(mock_resources, standard=standard.upper())
    return jsonify(report.__dict__)


@compliance_bp.route("/policies", methods=["GET"])
def list_policies() -> Response:
    return jsonify([p.__dict__ for p in engine.policies.values()])


@compliance_bp.route("/audit", methods=["GET"])
def get_audit() -> Response:
    return jsonify(engine.get_audit_log())


@compliance_bp.route("/gdpr/export/<int:user_id>", methods=["GET"])
def export_user_data(user_id: int) -> Tuple[Response, int]:
    try:
        data = gdpr_manager.export_user_data(user_id)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@compliance_bp.route("/gdpr/forget/<int:user_id>", methods=["POST"])
def forget_user(user_id: int) -> Tuple[Response, int]:
    # In a real app, we'd check permissions here (admin only or self)
    success = gdpr_manager.anonymize_user(user_id)
    if success:
        return jsonify({"status": "success", "message": "User anonymized"}), 200
    return jsonify({"error": "Failed to anonymize user"}), 500


# Create Flask app
app = Flask(__name__)

# Load and validate configuration (INFRA-003)
from opt.core.config import Settings
settings = Settings.load_validated_config()
app.config["SETTINGS"] = settings

# Initialize graceful shutdown and health checks
try:
    from opt.web.panel.graceful_shutdown import init_graceful_shutdown
    shutdown_manager = init_graceful_shutdown(app)

    def check_compliance_engine() -> bool:
        return engine is not None

    shutdown_manager.register_health_check("engine", check_compliance_engine)

except ImportError:
    # Fallback if graceful shutdown not available
    from opt.core.health import create_health_blueprint

    def check_compliance_engine_fallback() -> Dict[str, Any]:
        if engine:
            return {"status": "ok", "message": "ComplianceEngine active"}
        return {"status": "error", "message": "ComplianceEngine missing"}

    health_bp = create_health_blueprint("compliance-service", {"engine": check_compliance_engine_fallback})
    app.register_blueprint(health_bp)

app.register_blueprint(compliance_bp, url_prefix="/api/v1/compliance")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
