import logging
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ResourceCost:
    cpu_hourly_rate: float  # per core
    memory_hourly_rate: float  # per GB
    storage_hourly_rate: float  # per GB
    network_gb_rate: float  # per GB transfer


@dataclass
class CostReport:
    period_start: str
    period_end: str
    total_cost: float
    resource_breakdown: Dict[str, float]
    project_breakdown: Dict[str, float]
    forecast_next_month: float


@dataclass
class OptimizationRecommendation:
    resource_id: str
    resource_type: str
    recommendation_type: str  # 'rightsizing', 'idle', 'storage'
    description: str
    estimated_savings_monthly: float
    confidence_score: float
    action: str


class CostOptimizer:
    def __init__(self, pricing_config: Optional[Dict] = None):
        self.pricing = pricing_config or {
            "cpu_hourly": 0.05,
            "memory_hourly": 0.02,
            "storage_hourly": 0.001,
            "network_gb": 0.08
        }
        self.recommendations: List[OptimizationRecommendation] = []
        self.usage_history: List[Dict] = []

    def set_pricing(self, pricing: Dict[str, float]) -> None:
        """Update pricing model."""
        self.pricing.update(pricing)
        logger.info(f"Updated pricing model: {self.pricing}")

    def analyze_resource_usage(
            self, resources: List[Dict[str, Any]]) -> List[OptimizationRecommendation]:
        """
        Analyze resources for cost optimization opportunities.
        Expected resource format:
        {
            "id": "vm-123",
            "type": "vm",
            "specs": {"cpu": 4, "memory_gb": 16},
            "metrics": {"cpu_avg": 10, "mem_avg": 40, "uptime_hours": 720}
        }
        """
        recommendations = []

        for res in resources:
            if res["type"] == "vm":
                # Check for idle resources
                if res["metrics"].get(
                        "cpu_avg",
                        0) < 5 and res["metrics"].get(
                        "network_io",
                        0) < 100:
                    savings = self._calculate_monthly_cost(res["specs"])
                    rec = OptimizationRecommendation(
                        resource_id=res["id"],
                        resource_type="vm",
                        recommendation_type="idle",
                        description=(f"VM {res['id']} appears idle (CPU < 5%). "
                                     "Consider terminating or stopping."),
                        estimated_savings_monthly=savings,
                        confidence_score=0.9,
                        action="stop")
                    recommendations.append(rec)

                # Check for over-provisioning
                elif res["metrics"].get("cpu_avg", 0) < 20:
                    current_cost = self._calculate_monthly_cost(res["specs"])
                    # Suggest halving resources
                    new_specs = {
                        "cpu": max(1, res["specs"]["cpu"] // 2),
                        "memory_gb": max(1, res["specs"]["memory_gb"] // 2)
                    }
                    new_cost = self._calculate_monthly_cost(new_specs)
                    savings = current_cost - new_cost

                    rec = OptimizationRecommendation(
                        resource_id=res["id"],
                        resource_type="vm",
                        recommendation_type="rightsizing",
                        description=(f"VM {res['id']} is underutilized (CPU < 20%). "
                                     f"Resize from {res['specs']['cpu']}vCPU/"
                                     f"{res['specs']['memory_gb']}GB to "
                                     f"{new_specs['cpu']}vCPU/"
                                     f"{new_specs['memory_gb']}GB."),
                        estimated_savings_monthly=savings,
                        confidence_score=0.85,
                        action="resize")
                    recommendations.append(rec)

        self.recommendations = recommendations
        return recommendations

    def _calculate_monthly_cost(self, specs: Dict[str, float]) -> float:
        """Calculate estimated monthly cost for a resource spec."""
        hours = 730  # Average hours in a month
        cpu_cost = specs.get("cpu", 0) * self.pricing["cpu_hourly"] * hours
        mem_cost = specs.get("memory_gb", 0) * self.pricing["memory_hourly"] * hours
        storage_cost = specs.get("storage_gb", 0) * self.pricing["storage_hourly"] * hours
        return cpu_cost + mem_cost + storage_cost

    def generate_cost_report(self, resources: List[Dict[str, Any]], days: int = 30) -> CostReport:
        """Generate a cost report for the specified period."""
        total_cost = 0.0
        resource_breakdown = {}
        project_breakdown = {}

        for res in resources:
            monthly_cost = self._calculate_monthly_cost(res["specs"])
            # Adjust for actual uptime if available, otherwise assume 100% for projection
            uptime_ratio = res.get("metrics", {}).get("uptime_hours", 730) / 730
            actual_cost = monthly_cost * uptime_ratio

            total_cost += actual_cost

            r_type = res.get("type", "unknown")
            resource_breakdown[r_type] = resource_breakdown.get(r_type, 0) + actual_cost

            project = res.get("project", "default")
            project_breakdown[project] = project_breakdown.get(project, 0) + actual_cost

        # Simple linear forecast
        forecast = total_cost  # Assuming steady state for next month

        return CostReport(
            period_start=(datetime.now() - timedelta(days=days)).isoformat(),
            period_end=datetime.now().isoformat(),
            total_cost=round(total_cost, 2),
            resource_breakdown={k: round(v, 2) for k, v in resource_breakdown.items()},
            project_breakdown={k: round(v, 2) for k, v in project_breakdown.items()},
            forecast_next_month=round(forecast, 2)
        )

    def get_recommendations(self) -> List[Dict]:
        """Return current recommendations as dicts."""
        return [asdict(r) for r in self.recommendations]
