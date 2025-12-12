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


from flask import Blueprint, render_template, jsonify
import psutil
from datetime import datetime
from opt.services.compliance.core import ComplianceEngine
from opt.services.compliance.reporting import ComplianceReporter

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


@dashboard_bp.route("/compliance")
def compliance_dashboard():
    """Render the compliance dashboard page."""
    return render_template("compliance.html")


@dashboard_bp.route("/api/compliance/overview")  # type: ignore[type-var]
def get_compliance_overview() -> None:
    """Get compliance overview statistics."""
    try:
        engine = ComplianceEngine()
        reporter = ComplianceReporter(engine)
        resources = reporter.fetch_resources()
        report_data = engine.run_compliance_scan(resources)

        return jsonify(  # type: ignore[return-value]
            {
                "compliance_score": report_data.compliance_score,
                "total_policies": report_data.total_policies,
                "total_resources": report_data.total_resources,
                "violations_count": report_data.violations_count,
                "critical_violations": len([v for v in report_data.violations if v.severity == "critical"]),
                "high_violations": len([v for v in report_data.violations if v.severity == "high"]),
                "medium_violations": len([v for v in report_data.violations if v.severity == "medium"]),
                "low_violations": len([v for v in report_data.violations if v.severity == "low"]),
                "generated_at": report_data.generated_at,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # type: ignore[return-value]


@dashboard_bp.route("/api/compliance/violations")  # type: ignore[type-var]
def get_compliance_violations() -> None:
    """Get detailed list of compliance violations."""
    try:
        engine = ComplianceEngine()
        reporter = ComplianceReporter(engine)
        resources = reporter.fetch_resources()
        report_data = engine.run_compliance_scan(resources)

        violations = [
            {
                "policy_id": v.policy_id,
                "resource_id": v.resource_id,
                "resource_type": v.resource_type,
                "severity": v.severity,
                "status": v.status,
                "details": v.details,
                "timestamp": v.timestamp,
            }
            for v in report_data.violations
        ]

        return jsonify(violations)  # type: ignore[return-value]
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # type: ignore[return-value]


@dashboard_bp.route("/api/compliance/policies")  # type: ignore[type-var]
def get_compliance_policies() -> None:
    """Get list of all compliance policies."""
    try:
        engine = ComplianceEngine()

        policies = [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "severity": p.severity,
                "enabled": p.enabled,
                "tags": p.tags or [],
            }
            for p in engine.policies.values()
        ]

        return jsonify(policies)  # type: ignore[return-value]
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # type: ignore[return-value]


@dashboard_bp.route("/api/compliance/by-framework")  # type: ignore[type-var]
def get_compliance_by_framework() -> None:
    """Get compliance status grouped by framework (GDPR, HIPAA, SOC2)."""
    try:
        engine = ComplianceEngine()
        reporter = ComplianceReporter(engine)
        resources = reporter.fetch_resources()
        report_data = engine.run_compliance_scan(resources)

        frameworks = {}
        for policy in engine.policies.values():
            if policy.tags:
                for tag in policy.tags:
                    if tag not in frameworks:
                        frameworks[tag] = {
                            "total_policies": 0,
                            "violations": 0,
                            "compliant": 0,
                        }
                    frameworks[tag]["total_policies"] += 1

        for violation in report_data.violations:
            policy = engine.policies.get(violation.policy_id)
            if policy and policy.tags:
                for tag in policy.tags:
                    if tag in frameworks:
                        frameworks[tag]["violations"] += 1

        for tag in frameworks:
            frameworks[tag]["compliant"] = (
                frameworks[tag]["total_policies"] - frameworks[tag]["violations"]
            )
            frameworks[tag]["compliance_rate"] = (
                frameworks[tag]["compliant"] / frameworks[tag]["total_policies"] * 100
                if frameworks[tag]["total_policies"] > 0 else 100
            )

        return jsonify(frameworks)  # type: ignore[return-value]
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # type: ignore[return-value]
