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


from flask import Blueprint, jsonify, request, Flask
from typing import Dict, Any

from opt.core.config import Settings
from opt.core.health import create_health_blueprint

from .core import CostOptimizer

cost_bp = Blueprint("cost_optimization", __name__)
optimizer = CostOptimizer()

# Mock data store for API demo
mock_resources = [
    {
        "id": "vm-prod-1",
        "type": "vm",
        "project": "production",
        "specs": {"cpu": 8, "memory_gb": 32, "storage_gb": 100},
        "metrics": {"cpu_avg": 45, "uptime_hours": 730},
    },
    {
        "id": "vm-dev-1",
        "type": "vm",
        "project": "development",
        "specs": {"cpu": 4, "memory_gb": 16, "storage_gb": 50},
        "metrics": {"cpu_avg": 2, "uptime_hours": 730},
    },
]


@cost_bp.route("/report", methods=["GET"])
def get_cost_report() -> Any:
    days = int(request.args.get("days", 30))
    report = optimizer.generate_cost_report(mock_resources, days=days)
    return jsonify(report.__dict__)


@cost_bp.route("/recommendations", methods=["GET"])
def get_recommendations() -> Any:
    recommendations = optimizer.analyze_resource_usage(mock_resources)
    return jsonify([rec.__dict__ for rec in recommendations])


@cost_bp.route("/pricing", methods=["GET", "POST"])
def manage_pricing() -> Any:
    if request.method == "POST":
        new_pricing = request.json
        optimizer.set_pricing(new_pricing)
        return jsonify({"status": "success", "pricing": optimizer.pricing})
    return jsonify(optimizer.pricing)


# Create Flask app
app = Flask(__name__)

# Load and validate configuration (INFRA-003)
settings = Settings.load_validated_config()
app.config["SETTINGS"] = settings

# Initialize graceful shutdown and health checks
try:
    from opt.web.panel.graceful_shutdown import init_graceful_shutdown
    shutdown_manager = init_graceful_shutdown(app)

    def check_optimizer() -> bool:
        return optimizer is not None

    shutdown_manager.register_health_check("optimizer", check_optimizer)

except ImportError:
    # Fallback if graceful shutdown not available
    def check_optimizer_fallback() -> Dict[str, Any]:
        if optimizer:
            return {"status": "ok", "message": "CostOptimizer active"}
        return {"status": "error", "message": "CostOptimizer missing"}

    health_bp = create_health_blueprint("cost-optimization-service", {"optimizer": check_optimizer_fallback})
    app.register_blueprint(health_bp)

app.register_blueprint(cost_bp, url_prefix="/api/v1/cost")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
