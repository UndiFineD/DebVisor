from flask import Blueprint, jsonify
from .core import ComplianceEngine

compliance_bp = Blueprint('compliance', __name__)
engine = ComplianceEngine()

# Mock resources
mock_resources = [
    {"id": "vm-compliant-1", "type": "vm"},
    {"id": "vm-noncompliant-1", "type": "vm"},
    {"id": "host-prod-1", "type": "host"}
]


@compliance_bp.route('/scan', methods=['POST'])
def run_scan():
    report = engine.run_compliance_scan(mock_resources)
    return jsonify(report.__dict__)


@compliance_bp.route('/policies', methods=['GET'])
def list_policies():
    return jsonify([p.__dict__ for p in engine.policies.values()])


@compliance_bp.route('/audit', methods=['GET'])
def get_audit():
    return jsonify(engine.get_audit_log())
