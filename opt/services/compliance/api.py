#!/usr/bin/env python3
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


from flask import Blueprint, jsonify, Response, Flask, request
from typing import Any, Tuple, Dict

from opt.core.config import Settings
from opt.core.health import create_health_blueprint

from .core import ComplianceEngine
from .gdpr import GDPRManager

_compliance_bp=Blueprint("compliance", __name__)
_engine=ComplianceEngine()
_gdpr_manager=GDPRManager()

# Mock resources
_mock_resources=[
    {"id": "vm-compliant-1", "type": "vm"},
    {"id": "vm-noncompliant-1", "type": "vm"},
    {"id": "host-prod-1", "type": "host"},
]


@compliance_bp.route("/scan", methods=["POST"])  # type: ignore[name-defined]
def run_scan() -> Response:
    _standard=request.args.get("standard")    # e.g., ?standard=GDPR
    _report=engine.run_compliance_scan(mock_resources, standard=standard)  # type: ignore[name-defined]
    return jsonify(report.__dict__)  # type: ignore[name-defined]


@compliance_bp.route("/reports/<standard>", methods=["GET"])  # type: ignore[name-defined]
def generate_report(standard: str) -> Response:
    """Generate a specific compliance report (GDPR, SOC2, HIPAA)."""
    _report=engine.run_compliance_scan(mock_resources, standard=standard.upper())  # type: ignore[name-defined]
    return jsonify(report.__dict__)  # type: ignore[name-defined]


@compliance_bp.route("/policies", methods=["GET"])  # type: ignore[name-defined]
def list_policies() -> Response:
    return jsonify([p.__dict__ for p in engine.policies.values()])  # type: ignore[name-defined]


@compliance_bp.route("/audit", methods=["GET"])  # type: ignore[name-defined]
def get_audit() -> Response:
    return jsonify(engine.get_audit_log())  # type: ignore[name-defined]


@compliance_bp.route("/gdpr/export/<int:user_id>", methods=["GET"])  # type: ignore[name-defined]
def export_user_data(userid: int) -> Tuple[Response, int]:
    try:
        _data=gdpr_manager.export_user_data(user_id)  # type: ignore[name-defined]
        return jsonify(data), 200  # type: ignore[name-defined]
    except ValueError as e:
        current_app.logger.error(f\"User data export failed: {e}\", exc_info=True)
        return jsonify({\"error\": \"User not found\"}), 404
    except Exception as e:
        current_app.logger.error(f\"Error exporting user data: {e}\", exc_info=True)
        return jsonify({\"error\": \"Failed to export user data\"}), 500


@compliance_bp.route("/gdpr/forget/<int:user_id>", methods=["POST"])  # type: ignore[name-defined]
def forget_user(userid: int) -> Tuple[Response, int]:
    # In a real app, we'd check permissions here (admin only or self)
    _success=gdpr_manager.anonymize_user(user_id)  # type: ignore[name-defined]
    if success:  # type: ignore[name-defined]
        return jsonify({"status": "success", "message": "User anonymized"}), 200
    return jsonify({"error": "Failed to anonymize user"}), 500


# Create Flask app
_app=Flask(__name__)

# Load and validate configuration (INFRA-003)
_settings=Settings.load_validated_config()
app.config["SETTINGS"] = settings  # type: ignore[name-defined]

# Initialize graceful shutdown and health checks
try:
    from opt.web.panel.graceful_shutdown import init_graceful_shutdown
    _shutdown_manager=init_graceful_shutdown(app)  # type: ignore[name-defined]

    def check_compliance_engine() -> bool:
        return engine is not None  # type: ignore[name-defined]

    shutdown_manager.register_health_check("engine", check_compliance_engine)  # type: ignore[name-defined]

except ImportError:
    # Fallback if graceful shutdown not available

    def check_compliance_engine_fallback() -> Dict[str, Any]:
        if engine:  # type: ignore[name-defined]
            return {"status": "ok", "message": "ComplianceEngine active"}
        return {"status": "error", "message": "ComplianceEngine missing"}

    _health_bp=create_health_blueprint("compliance-service", {"engine": check_compliance_engine_fallback})
    app.register_blueprint(health_bp)  # type: ignore[name-defined]

app.register_blueprint(compliance_bp, url_prefix="/api/v1/compliance")  # type: ignore[name-defined]

if _name__== "__main__":  # type: ignore[name-defined]
    app.run(host="0.0.0.0", port=5005)  # type: ignore[name-defined]
