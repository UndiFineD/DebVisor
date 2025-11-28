from flask import Blueprint, jsonify, request
from .core import CostOptimizer

cost_bp = Blueprint('cost_optimization', __name__)
optimizer = CostOptimizer()

# Mock data store for API demo
mock_resources = [
    {
        "id": "vm-prod-1", "type": "vm", "project": "production",
        "specs": {"cpu": 8, "memory_gb": 32, "storage_gb": 100},
        "metrics": {"cpu_avg": 45, "uptime_hours": 730}
    },
    {
        "id": "vm-dev-1", "type": "vm", "project": "development",
        "specs": {"cpu": 4, "memory_gb": 16, "storage_gb": 50},
        "metrics": {"cpu_avg": 2, "uptime_hours": 730}
    }
]

@cost_bp.route('/report', methods=['GET'])
def get_cost_report():
    days = int(request.args.get('days', 30))
    report = optimizer.generate_cost_report(mock_resources, days=days)
    return jsonify(report.__dict__)

@cost_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    recommendations = optimizer.analyze_resource_usage(mock_resources)
    return jsonify([rec.__dict__ for rec in recommendations])

@cost_bp.route('/pricing', methods=['GET', 'POST'])
def manage_pricing():
    if request.method == 'POST':
        new_pricing = request.json
        optimizer.set_pricing(new_pricing)
        return jsonify({"status": "success", "pricing": optimizer.pricing})
    return jsonify(optimizer.pricing)
