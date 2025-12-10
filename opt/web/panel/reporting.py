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

"""
PDF report generation for DebVisor Web Panel.

Generates various reports:
- Cluster health report
- Storage capacity planning
- Performance analysis
- Compliance audit trail
- Custom reports

Features:
- Templated report generation
- Charts and visualizations
- Performance metrics
- Historical trending
- Export to PDF/HTML
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ReportType(Enum):
    """Supported report types."""

    HEALTH = "health"
    CAPACITY_PLANNING = "capacity_planning"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    CUSTOM = "custom"


class ReportFormat(Enum):
    """Report output formats."""

    PDF = "pdf"
    HTML = "html"
    JSON = "json"
    CSV = "csv"


@dataclass
class HealthMetric:
    """Health metric for reporting."""

    name: str
    value: float
    unit: str
    warning_threshold: float
    critical_threshold: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def status(self) -> str:
        """Get health status."""
        if self.value >= self.critical_threshold:
            return "critical"
        elif self.value >= self.warning_threshold:
            return "warning"
        return "healthy"

    @property
    def status_emoji(self) -> str:
        """Get status emoji."""
        status_map = {
            "healthy": "?",
            "warning": "[warn]?",
            "critical": "[U+1F534]",
        }
        return status_map.get(self.status, "?")


@dataclass
class StoragePool:
    """Storage pool information for capacity planning."""

    pool_id: str
    pool_name: str
    used_bytes: int
    total_bytes: int
    reserved_bytes: int = 0

    @property
    def used_percent(self) -> float:
        """Calculate usage percentage."""
        if self.total_bytes == 0:
            return 0.0
        return (self.used_bytes / self.total_bytes) * 100

    @property
    def available_bytes(self) -> int:
        """Calculate available bytes."""
        return self.total_bytes - self.used_bytes

    @property
    def available_percent(self) -> float:
        """Calculate available percentage."""
        return 100 - self.used_percent


@dataclass
class PerformanceMetric:
    """Performance metric for trend analysis."""

    timestamp: datetime
    metric_name: str
    value: float
    unit: str


@dataclass
class ReportConfig:
    """Configuration for report generation."""

    title: str = "DebVisor Report"
    subtitle: Optional[str] = None
    generated_by: str = "DebVisor Web Panel"
    include_recommendations: bool = True
    include_charts: bool = True
    date_format: str = "%Y-%m-%d %H:%M:%S"
    page_size: str = "A4"


class HealthReport:
    """Cluster health report generator."""

    def __init__(self, config: Optional[ReportConfig] = None):
        """
        Initialize health report.

        Args:
            config: ReportConfig instance
        """
        self.config = config or ReportConfig(title="Cluster Health Report")
        self.metrics: List[HealthMetric] = []
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.alerts: List[Dict[str, Any]] = []

    def add_metric(self, metric: HealthMetric) -> None:
        """Add health metric."""
        self.metrics.append(metric)

    def add_node_status(
        self,
        node_id: str,
        status: str,
        cpu_usage: float,
        memory_usage: float,
        disk_usage: float,
    ) -> None:
        """Add node status."""
        self.nodes[node_id] = {
            "status": status,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
        }

    def add_alert(self, alert_type: str, severity: str, message: str) -> None:
        """Add alert."""
        self.alerts.append(
            {
                "type": alert_type,
                "severity": severity,
                "message": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    def get_summary(self) -> Dict[str, Any]:
        """Get report summary."""
        healthy_nodes = sum(1 for n in self.nodes.values() if n["status"] == "online")
        total_nodes = len(self.nodes)

        healthy_metrics = sum(1 for m in self.metrics if m.status == "healthy")
        warning_metrics = sum(1 for m in self.metrics if m.status == "warning")
        critical_metrics = sum(1 for m in self.metrics if m.status == "critical")

        return {
            "nodes": {"healthy": healthy_nodes, "total": total_nodes},
            "metrics": {
                "healthy": healthy_metrics,
                "warning": warning_metrics,
                "critical": critical_metrics,
            },
            "alerts": {
                "total": len(self.alerts),
                "critical": sum(1 for a in self.alerts if a["severity"] == "critical"),
            },
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_recommendations(self) -> List[str]:
        """Get health recommendations."""
        recommendations = []

        # Check for critical metrics
        critical = [m for m in self.metrics if m.status == "critical"]
        if critical:
            for m in critical:
                recommendations.append(
                    f"CRITICAL: {m.name} at {m.value}{m.unit} "
                    f"(threshold: {m.critical_threshold}{m.unit})"
                )

        # Check for offline nodes
        offline = [n for n, s in self.nodes.items() if s["status"] != "online"]
        if offline:
            recommendations.append(f"Investigate offline nodes: {', '.join(offline)}")

        # Check for high memory usage
        high_memory = [
            (n, s["memory_usage"])
            for n, s in self.nodes.items()
            if s["memory_usage"] > 80
        ]
        if high_memory:
            nodes = ", ".join([f"{n} ({m}%)" for n, m in high_memory])
            recommendations.append(f"High memory usage on nodes: {nodes}")

        return recommendations

    def generate_html(self) -> str:
        """Generate HTML report."""
        summary = self.get_summary()
        recommendations = self.get_recommendations()

        html = f"""
        <html>
        <head>
            <title>{self.config.title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color:    #333; }}
                h2 {{ color:    #666; border-bottom: 2px solid #ddd; padding-bottom: 10px; }}
                .summary {{ background:    #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .metric {{ display: inline-block; margin: 10px 20px 10px 0; }}
                .node {{ padding: 10px; margin: 10px 0; background:    #fafafa; border-left: 4px solid #ddd; }}
                .alert {{ padding: 10px; margin: 10px 0; border-left: 4px solid; }}
                .alert.critical {{ border-color:    #dc3545; background: #f8d7da; }}
                .alert.warning {{ border-color:    #ffc107; background: #fff3cd; }}
                .recommendation {{ padding: 10px; margin: 10px 0; background:    #e7f3ff;
                                border-left: 4px solid    #2196F3; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid    #ddd; }}
                th {{ background:    #f5f5f5; font-weight: bold; }}
                .footer {{ color:    #999; font-size: 12px; margin-top: 40px; padding-top: 20px;
                        border-top: 1px solid    #ddd; }}
            </style>
        </head>
        <body>
            <h1>{self.config.title}</h1>
            {f'<h2>{self.config.subtitle}</h2>' if self.config.subtitle else ''}

            <div class="summary">
                <h2>Executive Summary</h2>
                <div class="metric">
                    <strong>Nodes Online:</strong> {summary['nodes']['healthy']}/{summary['nodes']['total']}
                </div>
                <div class="metric">
                    <strong>Healthy Metrics:</strong> {summary['metrics']['healthy']}
                </div>
                <div class="metric">
                    <strong>Warnings:</strong> {summary['metrics']['warning']}
                </div>
                <div class="metric">
                    <strong>Critical:</strong> {summary['metrics']['critical']}
                </div>
            </div>

            <h2>Nodes Status</h2>
            <table>
                <tr>
                    <th>Node ID</th>
                    <th>Status</th>
                    <th>CPU Usage</th>
                    <th>Memory Usage</th>
                    <th>Disk Usage</th>
                </tr>
                {self._generate_node_rows()}
            </table>

            <h2>Health Metrics</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                    <th>Status</th>
                    <th>Threshold</th>
                </tr>
                {self._generate_metric_rows()}
            </table>

            {self._generate_alerts_section()}
            {self._generate_recommendations_section(recommendations)}

            <div class="footer">
                <p>Generated by {self.config.generated_by}</p>
                <p>Report Date: {datetime.now(timezone.utc).strftime(self.config.date_format)}</p>
            </div>
        </body>
        </html>
        """
        return html

    def _generate_node_rows(self) -> str:
        """Generate node table rows."""
        rows = []
        for node_id, data in self.nodes.items():
            status_icon = "[U+1F7E2]" if data["status"] == "online" else "[U+1F534]"
            rows.append(
                f"""
                <tr>
                    <td>{node_id}</td>
                    <td>{status_icon} {data['status']}</td>
                    <td>{data['cpu_usage']:.1f}%</td>
                    <td>{data['memory_usage']:.1f}%</td>
                    <td>{data['disk_usage']:.1f}%</td>
                </tr>
                """
            )
        return "\n".join(rows) if rows else "<tr><td colspan='5'>No nodes</td></tr>"

    def _generate_metric_rows(self) -> str:
        """Generate metric table rows."""
        rows = []
        for metric in self.metrics:
            rows.append(
                """
                <tr>
                    <td>{metric.name}</td>
                    <td>{metric.value:.2f} {metric.unit}</td>
                    <td>{metric.status_emoji} {metric.status}</td>
                    <td>Critical: {metric.critical_threshold}</td>
                </tr>
                """
            )
        return "\n".join(rows) if rows else "<tr><td colspan='4'>No metrics</td></tr>"

    def _generate_alerts_section(self) -> str:
        """Generate alerts section."""
        if not self.alerts:
            return ""

        alerts_html = "<h2>Recent Alerts</h2>\n"
        for alert in self.alerts:
            severity_class = alert["severity"].lower()
            alerts_html += f"""
            <div class=\"alert {severity_class}\">
                <strong>[{alert['severity'].upper()}]</strong> {alert['type']}: {alert['message']}
                <br><small>{alert['timestamp']}</small>
            </div>
            """
        return alerts_html

    def _generate_recommendations_section(self, recommendations: List[str]) -> str:
        """Generate recommendations section."""
        if not recommendations:
            return ""

        recs_html = "<h2>Recommendations</h2>\n"
        for rec in recommendations:
            recs_html += f'<div class="recommendation">-> {rec}</div>\n'
        return recs_html


class CapacityPlanningReport:
    """Storage capacity planning report generator."""

    def __init__(self, config: Optional[ReportConfig] = None):
        """
        Initialize capacity planning report.

        Args:
            config: ReportConfig instance
        """
        self.config = config or ReportConfig(title="Storage Capacity Planning Report")
        self.pools: List[StoragePool] = []
        self.growth_rate: float = 0.05    # 5% monthly growth
        self.forecast_months: int = 12

    def add_pool(self, pool: StoragePool) -> None:
        """Add storage pool."""
        self.pools.append(pool)

    def calculate_full_date(self, pool: StoragePool) -> Optional[datetime]:
        """Calculate when pool will be full."""
        if pool.used_percent >= 100:
            return datetime.now(timezone.utc)

        # Calculate based on growth rate
        available_space = pool.available_bytes
        monthly_growth = pool.used_bytes * self.growth_rate
        months_to_full = (
            available_space / monthly_growth if monthly_growth > 0 else float("inf")
        )

        if months_to_full == float("inf") or months_to_full > 120:
            return None

        return datetime.now(timezone.utc) + timedelta(days=months_to_full * 30)

    def get_summary(self) -> Dict[str, Any]:
        """Get capacity planning summary."""
        total_used = sum(p.used_bytes for p in self.pools)
        total_capacity = sum(p.total_bytes for p in self.pools)

        pools_at_risk = sum(1 for p in self.pools if p.used_percent > 80)
        pools_critical = sum(1 for p in self.pools if p.used_percent > 95)

        return {
            "total_capacity_gb": total_capacity / (1024**3),
            "total_used_gb": total_used / (1024**3),
            "total_used_percent": (
                (total_used / total_capacity * 100) if total_capacity > 0 else 0
            ),
            "pools": len(self.pools),
            "pools_at_risk": pools_at_risk,
            "pools_critical": pools_critical,
        }

    def get_recommendations(self) -> List[str]:
        """Get capacity recommendations."""
        recommendations = []
        summary = self.get_summary()

        if summary["pools_critical"] > 0:
            recommendations.append(
                f"URGENT: {summary['pools_critical']} pool(s) at >95% capacity. "
                "Immediate expansion required."
            )

        if summary["pools_at_risk"] > 0:
            recommendations.append(
                f"WARNING: {summary['pools_at_risk']} pool(s) at >80% capacity. "
                "Plan expansion within 30 days."
            )

        # Check forecast
        for pool in self.pools:
            full_date = self.calculate_full_date(pool)
            if full_date:
                days_until_full = (full_date - datetime.now(timezone.utc)).days
                if days_until_full < 90:
                    recommendations.append(
                        f"Pool {pool.pool_name} projected full in {days_until_full} days "
                        f"({full_date.strftime('%Y-%m-%d')})"
                    )

        return recommendations

    def generate_html(self) -> str:
        """Generate HTML report."""
        summary = self.get_summary()
        recommendations = self.get_recommendations()

        html = f"""
        <html>
        <head>
            <title>{self.config.title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color:    #333; }}
                h2 {{ color:    #666; border-bottom: 2px solid #ddd; padding-bottom: 10px; }}
                .summary {{ background:    #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .stat {{ display: inline-block; margin: 10px 20px 10px 0; }}
                .pool {{ padding: 15px; margin: 10px 0; background:    #fafafa; border-radius: 5px; }}
                .progress-bar {{ width: 100%; height: 25px; background:    #ddd; border-radius: 3px; overflow: hidden;
                                margin: 10px 0; }}
                .progress-fill {{ height: 100%; background: linear-gradient(90deg,    #4CAF50, #FFC107, #F44336);
                                transition: width 0.3s; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid    #ddd; }}
                th {{ background:    #f5f5f5; font-weight: bold; }}
                .recommendation {{ padding: 10px; margin: 10px 0; background:    #e7f3ff;
                                border-left: 4px solid    #2196F3; }}
                .footer {{ color:    #999; font-size: 12px; margin-top: 40px; padding-top: 20px;
                        border-top: 1px solid    #ddd; }}
            </style>
        </head>
        <body>
            <h1>{self.config.title}</h1>

            <div class="summary">
                <h2>Capacity Summary</h2>
                <div class="stat">
                    <strong>Total Capacity:</strong> {summary['total_capacity_gb']:.2f} GB
                </div>
                <div class="stat">
                    <strong>Total Used:</strong> {summary['total_used_gb']:.2f} GB
                </div>
                <div class="stat">
                    <strong>Usage:</strong> {summary['total_used_percent']:.1f}%
                </div>
                <div class="stat">
                    <strong>Pools:</strong> {summary['pools']}
                </div>
            </div>

            <h2>Storage Pools</h2>
            {self._generate_pool_details()}

            {self._generate_recommendations_section(recommendations)}

            <div class="footer">
                <p>Generated by {self.config.generated_by}</p>
                <p>Report Date: {datetime.now(timezone.utc).strftime(self.config.date_format)}</p>
                <p>Forecast Period: {self.forecast_months} months</p>
            </div>
        </body>
        </html>
        """
        return html

    def _generate_pool_details(self) -> str:
        """Generate pool details."""
        pools_html = ""
        for pool in self.pools:
            full_date = self.calculate_full_date(pool)
            full_date_str = full_date.strftime("%Y-%m-%d") if full_date else "N/A"

            pools_html += f"""
            <div class="pool">
                <h3>{pool.pool_name}</h3>
                <p>ID: {pool.pool_id}</p>
                <p>Total: {pool.total_bytes / (1024**3):.2f} GB |
                Used: {pool.used_bytes / (1024**3):.2f} GB |
                Available: {pool.available_bytes / (1024**3):.2f} GB</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {pool.used_percent:.1f}%"></div>
                </div>
                <p>Usage: {pool.used_percent:.1f}% | Projected Full: {full_date_str}</p>
            </div>
            """
        return pools_html

    def _generate_recommendations_section(self, recommendations: List[str]) -> str:
        """Generate recommendations section."""
        if not recommendations:
            return "<h2>No capacity issues detected</h2>"

        recs_html = "<h2>Recommendations</h2>\n"
        for rec in recommendations:
            recs_html += f'<div class="recommendation">-> {rec}</div>\n'
        return recs_html
