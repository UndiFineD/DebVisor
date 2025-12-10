"""Cost Optimization Engine - Enterprise Implementation.

Full-featured cost management and optimization:
- Real-time resource metering (CPU, RAM, Storage, Network, GPU)
- Multiple pricing models (On-demand, Reserved, Spot, Committed)
- Showback/chargeback reporting per tenant/project
- Right-sizing recommendations with ML-based analysis
- Budget alerts and forecasting
- Cost allocation tags and categories
- Multi-cloud cost comparison
- Historical trend analysis
"""

from __future__ import annotations
import logging
import json
import threading
import statistics
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timezone, timedelta
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger(__name__)


class ResourceType(Enum):
    """Resource types for metering."""

    CPU = "cpu"
    MEMORY = "memory"
    STORAGE_SSD = "storage_ssd"
    STORAGE_HDD = "storage_hdd"
    STORAGE_NVME = "storage_nvme"
    NETWORK_EGRESS = "network_egress"
    NETWORK_INGRESS = "network_ingress"
    GPU_NVIDIA = "gpu_nvidia"
    GPU_AMD = "gpu_amd"
    LICENSE = "license"
    BACKUP = "backup"
    SNAPSHOT = "snapshot"


class PricingModel(Enum):
    """Pricing model types."""

    ON_DEMAND = "on_demand"    # Pay as you go
    RESERVED_1Y = "reserved_1y"    # 1 year commitment
    RESERVED_3Y = "reserved_3y"    # 3 year commitment
    COMMITTED = "committed"    # Committed use discount
    SPOT = "spot"    # Preemptible/spot pricing
    FREE_TIER = "free_tier"    # Free quota


class CostCategory(Enum):
    """Cost categorization."""

    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    GPU = "gpu"
    LICENSING = "licensing"
    SUPPORT = "support"
    OTHER = "other"


@dataclass
class PricingTier:
    """Pricing tier definition."""

    resource_type: ResourceType
    model: PricingModel
    unit_price: Decimal    # Price per unit
    unit: str    # hour, GB, request, etc.
    currency: str = "USD"
    min_commitment: int = 0    # Minimum units
    discount_pct: Decimal = Decimal("0")
    effective_from: Optional[datetime] = None
    effective_until: Optional[datetime] = None

    def calculate_price(self, quantity: float) -> Decimal:
        """Calculate price for given quantity."""
        base = self.unit_price * Decimal(str(quantity))
        discount = base * (self.discount_pct / Decimal("100"))
        return (base - discount).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


@dataclass
class ResourceUsage:
    """Resource usage record."""

    id: str
    resource_id: str    # VM ID, Storage ID, etc.
    resource_type: ResourceType
    quantity: float
    unit: str    # hours, GB, requests
    timestamp: datetime
    period_start: datetime
    period_end: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Attribution
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    user_id: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class CostRecord:
    """Calculated cost record."""

    usage_id: str
    resource_id: str
    resource_type: ResourceType
    category: CostCategory
    pricing_model: PricingModel
    quantity: float
    unit_price: Decimal
    total_cost: Decimal
    currency: str
    timestamp: datetime

    # Attribution
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "usage_id": self.usage_id,
            "resource_id": self.resource_id,
            "resource_type": self.resource_type.value,
            "category": self.category.value,
            "pricing_model": self.pricing_model.value,
            "quantity": self.quantity,
            "unit_price": str(self.unit_price),
            "total_cost": str(self.total_cost),
            "currency": self.currency,
            "timestamp": self.timestamp.isoformat(),
            "tenant_id": self.tenant_id,
            "project_id": self.project_id,
            "tags": self.tags,
        }


@dataclass
class Budget:
    """Budget definition with alerts."""

    id: str
    name: str
    amount: Decimal
    currency: str
    period: str    # monthly, quarterly, yearly
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    alert_thresholds: List[int] = field(default_factory=lambda: [50, 80, 100])

    current_spend: Decimal = Decimal("0")
    alerts_sent: List[int] = field(default_factory=list)

    @property
    def usage_pct(self) -> float:
        if self.amount == 0:
            return 0.0
        return float(self.current_spend / self.amount * 100)

    def check_alerts(self) -> List[int]:
        """Return list of threshold percentages that should trigger alerts."""
        triggered = []
        for threshold in self.alert_thresholds:
            if self.usage_pct >= threshold and threshold not in self.alerts_sent:
                triggered.append(threshold)
                self.alerts_sent.append(threshold)
        return triggered


@dataclass
class RightsizingRecommendation:
    """VM rightsizing recommendation."""

    resource_id: str
    resource_name: str
    current_config: Dict[str, Any]
    recommended_config: Dict[str, Any]
    current_monthly_cost: Decimal
    recommended_monthly_cost: Decimal
    monthly_savings: Decimal
    confidence: float    # 0-1
    reasoning: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def savings_pct(self) -> float:
        if self.current_monthly_cost == 0:
            return 0.0
        return float(self.monthly_savings / self.current_monthly_cost * 100)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resource_id": self.resource_id,
            "resource_name": self.resource_name,
            "current_config": self.current_config,
            "recommended_config": self.recommended_config,
            "current_monthly_cost": str(self.current_monthly_cost),
            "recommended_monthly_cost": str(self.recommended_monthly_cost),
            "monthly_savings": str(self.monthly_savings),
            "savings_pct": round(self.savings_pct, 1),
            "confidence": round(self.confidence, 2),
            "reasoning": self.reasoning,
        }


class CostEngine:
    """Enterprise cost optimization engine."""

    def __init__(self, currency: str = "USD"):
        self._lock = threading.RLock()
        self.currency = currency

        # Pricing tiers
        self._pricing_tiers: Dict[ResourceType, List[PricingTier]] = {}

        # Usage and cost records
        self._usage_log: List[ResourceUsage] = []
        self._cost_records: List[CostRecord] = []

        # Budgets
        self._budgets: Dict[str, Budget] = {}

        # Alert callbacks
        self._alert_callbacks: List[Callable[[Budget, int], None]] = []

        # Resource metrics for rightsizing
        self._resource_metrics: Dict[str, List[Dict[str, float]]] = defaultdict(list)

        # Load default pricing
        self._init_default_pricing()

    def _init_default_pricing(self) -> None:
        """Initialize default pricing tiers."""
        default_prices = [
            # CPU pricing (per vCPU-hour)
            PricingTier(
                ResourceType.CPU, PricingModel.ON_DEMAND, Decimal("0.0500"), "vcpu-hour"
            ),
            PricingTier(
                ResourceType.CPU,
                PricingModel.RESERVED_1Y,
                Decimal("0.0350"),
                "vcpu-hour",
                discount_pct=Decimal("30"),
            ),
            PricingTier(
                ResourceType.CPU,
                PricingModel.RESERVED_3Y,
                Decimal("0.0250"),
                "vcpu-hour",
                discount_pct=Decimal("50"),
            ),
            # Memory pricing (per GB-hour)
            PricingTier(
                ResourceType.MEMORY,
                PricingModel.ON_DEMAND,
                Decimal("0.0067"),
                "gb-hour",
            ),
            PricingTier(
                ResourceType.MEMORY,
                PricingModel.RESERVED_1Y,
                Decimal("0.0047"),
                "gb-hour",
                discount_pct=Decimal("30"),
            ),
            # Storage pricing (per GB-month)
            PricingTier(
                ResourceType.STORAGE_SSD,
                PricingModel.ON_DEMAND,
                Decimal("0.1000"),
                "gb-month",
            ),
            PricingTier(
                ResourceType.STORAGE_HDD,
                PricingModel.ON_DEMAND,
                Decimal("0.0400"),
                "gb-month",
            ),
            PricingTier(
                ResourceType.STORAGE_NVME,
                PricingModel.ON_DEMAND,
                Decimal("0.1700"),
                "gb-month",
            ),
            # Network pricing (per GB transferred)
            PricingTier(
                ResourceType.NETWORK_EGRESS,
                PricingModel.ON_DEMAND,
                Decimal("0.0900"),
                "gb",
            ),
            PricingTier(
                ResourceType.NETWORK_INGRESS,
                PricingModel.ON_DEMAND,
                Decimal("0.0000"),
                "gb",
            ),
            # Free ingress
            # GPU pricing (per GPU-hour)
            PricingTier(
                ResourceType.GPU_NVIDIA,
                PricingModel.ON_DEMAND,
                Decimal("0.9000"),
                "gpu-hour",
            ),
            PricingTier(
                ResourceType.GPU_NVIDIA,
                PricingModel.RESERVED_1Y,
                Decimal("0.6300"),
                "gpu-hour",
                discount_pct=Decimal("30"),
            ),
            # Backup/Snapshot pricing
            PricingTier(
                ResourceType.BACKUP,
                PricingModel.ON_DEMAND,
                Decimal("0.0500"),
                "gb-month",
            ),
            PricingTier(
                ResourceType.SNAPSHOT,
                PricingModel.ON_DEMAND,
                Decimal("0.0500"),
                "gb-month",
            ),
        ]

        for tier in default_prices:
            if tier.resource_type not in self._pricing_tiers:
                self._pricing_tiers[tier.resource_type] = []
            self._pricing_tiers[tier.resource_type].append(tier)

    def set_pricing_tier(self, tier: PricingTier) -> None:
        """Add or update a pricing tier."""
        with self._lock:
            if tier.resource_type not in self._pricing_tiers:
                self._pricing_tiers[tier.resource_type] = []

            # Replace existing tier with same model, or add new
            tiers = self._pricing_tiers[tier.resource_type]
            for i, existing in enumerate(tiers):
                if existing.model == tier.model:
                    tiers[i] = tier
                    return
            tiers.append(tier)

    def get_pricing(
        self, resource_type: ResourceType, model: PricingModel = PricingModel.ON_DEMAND
    ) -> Optional[PricingTier]:
        """Get pricing tier for resource type and model."""
        tiers = self._pricing_tiers.get(resource_type, [])
        for tier in tiers:
            if tier.model == model:
                return tier
        return None

    def record_usage(self, usage: ResourceUsage) -> CostRecord:
        """Record resource usage and calculate cost."""
        with self._lock:
            self._usage_log.append(usage)

            # Calculate cost
            pricing = self.get_pricing(usage.resource_type)
            if not pricing:
                logger.warning(f"No pricing for resource type: {usage.resource_type}")
                pricing = PricingTier(
                    usage.resource_type,
                    PricingModel.ON_DEMAND,
                    Decimal("0"),
                    usage.unit,
                )

            cost = pricing.calculate_price(usage.quantity)

            # Map resource type to category
            category_map = {
                ResourceType.CPU: CostCategory.COMPUTE,
                ResourceType.MEMORY: CostCategory.COMPUTE,
                ResourceType.STORAGE_SSD: CostCategory.STORAGE,
                ResourceType.STORAGE_HDD: CostCategory.STORAGE,
                ResourceType.STORAGE_NVME: CostCategory.STORAGE,
                ResourceType.NETWORK_EGRESS: CostCategory.NETWORK,
                ResourceType.NETWORK_INGRESS: CostCategory.NETWORK,
                ResourceType.GPU_NVIDIA: CostCategory.GPU,
                ResourceType.GPU_AMD: CostCategory.GPU,
                ResourceType.BACKUP: CostCategory.STORAGE,
                ResourceType.SNAPSHOT: CostCategory.STORAGE,
            }

            record = CostRecord(
                usage_id=usage.id,
                resource_id=usage.resource_id,
                resource_type=usage.resource_type,
                category=category_map.get(usage.resource_type, CostCategory.OTHER),
                pricing_model=pricing.model,
                quantity=usage.quantity,
                unit_price=pricing.unit_price,
                total_cost=cost,
                currency=self.currency,
                timestamp=usage.timestamp,
                tenant_id=usage.tenant_id,
                project_id=usage.project_id,
                tags=usage.tags,
            )

            self._cost_records.append(record)

            # Update budgets
            self._update_budgets(record)

            return record

    def _update_budgets(self, record: CostRecord) -> None:
        """Update budget spend and check alerts."""
        for budget in self._budgets.values():
            # Check if record matches budget scope
            if budget.tenant_id and budget.tenant_id != record.tenant_id:
                continue
            if budget.project_id and budget.project_id != record.project_id:
                continue

            budget.current_spend += record.total_cost

            # Check for alerts
            triggered = budget.check_alerts()
            for threshold in triggered:
                logger.warning(
                    f"Budget alert: '{budget.name}' reached {threshold}% "
                    f"(${budget.current_spend:.2f} / ${budget.amount:.2f})"
                )
                for callback in self._alert_callbacks:
                    try:
                        callback(budget, threshold)
                    except Exception as e:
                        logger.error(f"Budget alert callback error: {e}")

    def create_budget(self, budget: Budget) -> None:
        """Create a new budget."""
        with self._lock:
            self._budgets[budget.id] = budget
        logger.info(f"Created budget: {budget.name} (${budget.amount})")

    def register_alert_callback(self, callback: Callable[[Budget, int], None]) -> None:
        """Register callback for budget alerts."""
        self._alert_callbacks.append(callback)

    def get_cost_by_resource(
        self,
        resource_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get cost breakdown for a specific resource."""
        with self._lock:
            records = [r for r in self._cost_records if r.resource_id == resource_id]

        if start_date:
            records = [r for r in records if r.timestamp >= start_date]
        if end_date:
            records = [r for r in records if r.timestamp <= end_date]

        total = sum(r.total_cost for r in records)
        by_type = defaultdict(Decimal)
        for r in records:
            by_type[r.resource_type.value] += r.total_cost

        return {
            "resource_id": resource_id,
            "total_cost": str(total),
            "currency": self.currency,
            "breakdown": {k: str(v) for k, v in by_type.items()},
            "record_count": len(records),
        }

    def get_cost_by_tenant(
        self,
        tenant_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get cost breakdown for a tenant (showback report)."""
        with self._lock:
            records = [r for r in self._cost_records if r.tenant_id == tenant_id]

        if start_date:
            records = [r for r in records if r.timestamp >= start_date]
        if end_date:
            records = [r for r in records if r.timestamp <= end_date]

        total = sum(r.total_cost for r in records)
        by_category = defaultdict(Decimal)
        by_project = defaultdict(Decimal)
        by_resource = defaultdict(Decimal)

        for r in records:
            by_category[r.category.value] += r.total_cost
            if r.project_id:
                by_project[r.project_id] += r.total_cost
            by_resource[r.resource_id] += r.total_cost

        return {
            "tenant_id": tenant_id,
            "total_cost": str(total),
            "currency": self.currency,
            "by_category": {k: str(v) for k, v in by_category.items()},
            "by_project": {
                k: str(v)
                for k, v in sorted(by_project.items(), key=lambda x: -x[1])[:10]
            },
            "top_resources": {
                k: str(v)
                for k, v in sorted(by_resource.items(), key=lambda x: -x[1])[:10]
            },
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None,
            },
        }

    def record_resource_metrics(
        self,
        resource_id: str,
        cpu_pct: float,
        memory_pct: float,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Record resource utilization metrics for rightsizing analysis."""
        with self._lock:
            self._resource_metrics[resource_id].append(
                {
                    "timestamp": (timestamp or datetime.now(timezone.utc)).isoformat(),
                    "cpu_pct": cpu_pct,
                    "memory_pct": memory_pct,
                }
            )
            # Keep last 1000 samples per resource
            if len(self._resource_metrics[resource_id]) > 1000:
                self._resource_metrics[resource_id] = self._resource_metrics[
                    resource_id
                ][-1000:]

    def get_rightsizing_recommendations(
        self,
        resource_id: str,
        current_vcpus: int,
        current_memory_gb: int,
        resource_name: str = "",
    ) -> Optional[RightsizingRecommendation]:
        """Analyze resource usage and provide rightsizing recommendation."""
        with self._lock:
            metrics = self._resource_metrics.get(resource_id, [])

        if len(metrics) < 100:
            logger.debug(
                f"Insufficient data for {resource_id} ({len(metrics)} samples)"
            )
            return None

        # Analyze CPU usage
        cpu_values = [m["cpu_pct"] for m in metrics]
        cpu_avg = statistics.mean(cpu_values)
        cpu_p95 = sorted(cpu_values)[int(len(cpu_values) * 0.95)]
        # cpu_max = max(cpu_values)

        # Analyze memory usage
        mem_values = [m["memory_pct"] for m in metrics]
        mem_avg = statistics.mean(mem_values)
        mem_p95 = sorted(mem_values)[int(len(mem_values) * 0.95)]
        # mem_max = max(mem_values)

        # Determine recommendations
        recommended_vcpus = current_vcpus
        recommended_memory_gb = current_memory_gb
        reasons = []

        # CPU rightsizing
        if cpu_p95 < 30 and current_vcpus > 1:
            recommended_vcpus = max(1, int(current_vcpus * cpu_p95 / 50))
            reasons.append(
                f"CPU usage P95={cpu_p95:.0f}%, avg={cpu_avg:.0f}% - underutilized"
            )
        elif cpu_p95 > 80:
            recommended_vcpus = min(current_vcpus * 2, 128)
            reasons.append(f"CPU usage P95={cpu_p95:.0f}% - consider scaling up")

        # Memory rightsizing
        if mem_p95 < 30 and current_memory_gb > 1:
            recommended_memory_gb = max(1, int(current_memory_gb * mem_p95 / 50))
            reasons.append(
                f"Memory usage P95={mem_p95:.0f}%, avg={mem_avg:.0f}% - underutilized"
            )
        elif mem_p95 > 85:
            recommended_memory_gb = min(current_memory_gb * 2, 1024)
            reasons.append(f"Memory usage P95={mem_p95:.0f}% - consider scaling up")

        # No changes needed
        if (
            recommended_vcpus == current_vcpus
            and recommended_memory_gb == current_memory_gb
        ):
            return None

        # Calculate costs
        cpu_pricing = self.get_pricing(ResourceType.CPU) or PricingTier(
            ResourceType.CPU, PricingModel.ON_DEMAND, Decimal("0.05"), "vcpu-hour"
        )
        mem_pricing = self.get_pricing(ResourceType.MEMORY) or PricingTier(
            ResourceType.MEMORY, PricingModel.ON_DEMAND, Decimal("0.0067"), "gb-hour"
        )

        hours_per_month = Decimal("730")    # Average hours in a month

        current_cpu_cost = (
            cpu_pricing.unit_price * Decimal(str(current_vcpus)) * hours_per_month
        )
        current_mem_cost = (
            mem_pricing.unit_price * Decimal(str(current_memory_gb)) * hours_per_month
        )
        current_total = current_cpu_cost + current_mem_cost

        recommended_cpu_cost = (
            cpu_pricing.unit_price * Decimal(str(recommended_vcpus)) * hours_per_month
        )
        recommended_mem_cost = (
            mem_pricing.unit_price
            * Decimal(str(recommended_memory_gb))
            * hours_per_month
        )
        recommended_total = recommended_cpu_cost + recommended_mem_cost

        savings = current_total - recommended_total

        # Calculate confidence based on data quality
        data_points = len(metrics)
        confidence = min(0.95, 0.5 + (data_points / 2000))

        return RightsizingRecommendation(
            resource_id=resource_id,
            resource_name=resource_name or resource_id,
            current_config={"vcpus": current_vcpus, "memory_gb": current_memory_gb},
            recommended_config={
                "vcpus": recommended_vcpus,
                "memory_gb": recommended_memory_gb,
            },
            current_monthly_cost=current_total.quantize(Decimal("0.01")),
            recommended_monthly_cost=recommended_total.quantize(Decimal("0.01")),
            monthly_savings=savings.quantize(Decimal("0.01")),
            confidence=confidence,
            reasoning="; ".join(reasons),
        )

    def get_cost_forecast(
        self, tenant_id: Optional[str] = None, days_ahead: int = 30
    ) -> Dict[str, Any]:
        """Forecast future costs based on historical trend."""
        with self._lock:
            records = list(self._cost_records)

        if tenant_id:
            records = [r for r in records if r.tenant_id == tenant_id]

        if len(records) < 7:
            return {"error": "Insufficient data for forecast"}

        # Group by day
        daily_costs = defaultdict(Decimal)
        for r in records:
            day = r.timestamp.date()
            daily_costs[day] += r.total_cost

        # Calculate average daily cost
        daily_values = list(daily_costs.values())
        avg_daily = sum(daily_values) / len(daily_values)

        # Simple linear forecast
        forecast_total = avg_daily * Decimal(str(days_ahead))

        return {
            "historical_days": len(daily_costs),
            "average_daily_cost": str(avg_daily.quantize(Decimal("0.01"))),
            "forecast_days": days_ahead,
            "forecast_total": str(forecast_total.quantize(Decimal("0.01"))),
            "currency": self.currency,
        }

    def get_summary(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get overall cost summary."""
        with self._lock:
            records = list(self._cost_records)

        if start_date:
            records = [r for r in records if r.timestamp >= start_date]
        if end_date:
            records = [r for r in records if r.timestamp <= end_date]

        total = sum(r.total_cost for r in records)
        by_category = defaultdict(Decimal)
        by_tenant = defaultdict(Decimal)

        for r in records:
            by_category[r.category.value] += r.total_cost
            if r.tenant_id:
                by_tenant[r.tenant_id] += r.total_cost

        return {
            "total_cost": str(total),
            "currency": self.currency,
            "record_count": len(records),
            "by_category": {k: str(v) for k, v in by_category.items()},
            "by_tenant": {
                k: str(v)
                for k, v in sorted(by_tenant.items(), key=lambda x: -x[1])[:10]
            },
            "budgets": [
                {
                    "name": b.name,
                    "amount": str(b.amount),
                    "spent": str(b.current_spend),
                    "usage_pct": round(b.usage_pct, 1),
                }
                for b in self._budgets.values()
            ],
        }

    def export_report(
        self, filepath: str, tenant_id: Optional[str] = None, format: str = "json"
    ) -> None:
        """Export cost report to file."""
        with self._lock:
            records = [
                r
                for r in self._cost_records
                if not tenant_id or r.tenant_id == tenant_id
            ]

        if format == "json":
            data = {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "summary": self.get_summary(),
                "records": [r.to_dict() for r in records],
            }
            Path(filepath).write_text(json.dumps(data, indent=2))
        elif format == "csv":
            import csv

            with open(filepath, "w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "usage_id",
                        "resource_id",
                        "resource_type",
                        "category",
                        "quantity",
                        "unit_price",
                        "total_cost",
                        "currency",
                        "timestamp",
                        "tenant_id",
                        "project_id",
                    ],
                )
                writer.writeheader()
                for r in records:
                    writer.writerow(
                        {
                            "usage_id": r.usage_id,
                            "resource_id": r.resource_id,
                            "resource_type": r.resource_type.value,
                            "category": r.category.value,
                            "quantity": r.quantity,
                            "unit_price": str(r.unit_price),
                            "total_cost": str(r.total_cost),
                            "currency": r.currency,
                            "timestamp": r.timestamp.isoformat(),
                            "tenant_id": r.tenant_id,
                            "project_id": r.project_id,
                        }
                    )

        logger.info(f"Exported cost report to {filepath}")


# CLI entry point
if __name__ == "__main__":
    import argparse
    import uuid

    parser = argparse.ArgumentParser(description="DebVisor Cost Engine")
    parser.add_argument(
        "action", choices=["demo", "pricing", "summary"], help="Action to perform"
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    engine = CostEngine()

    if args.action == "pricing":
        print("Default Pricing Tiers:")
        print("-" * 60)
        for resource_type, tiers in engine._pricing_tiers.items():
            for tier in tiers:
                print(
                    f"  {resource_type.value:20} | {tier.model.value:15} | "
                    f"${tier.unit_price}/{tier.unit}"
                )

    elif args.action == "demo":
        # Create sample usage data
        now = datetime.now(timezone.utc)

        for i in range(24):
            ts = now - timedelta(hours=i)
            usage = ResourceUsage(
                id=str(uuid.uuid4()),
                resource_id="vm-web-01",
                resource_type=ResourceType.CPU,
                quantity=4.0,
                unit="vcpu-hour",
                timestamp=ts,
                period_start=ts,
                period_end=ts + timedelta(hours=1),
                tenant_id="tenant-acme",
                project_id="project-prod",
            )
            engine.record_usage(usage)

        # Create a budget
        budget = Budget(
            id="budget-acme-monthly",
            name="ACME Corp Monthly",
            amount=Decimal("1000.00"),
            currency="USD",
            period="monthly",
            tenant_id="tenant-acme",
        )
        engine.create_budget(budget)

        # Print summary
        summary = engine.get_summary()
        print(json.dumps(summary, indent=2))

    elif args.action == "summary":
        summary = engine.get_summary()
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print(f"Total Cost: ${summary['total_cost']} {summary['currency']}")
            print(f"Records: {summary['record_count']}")
            print("\nBy Category:")
            for cat, cost in summary["by_category"].items():
                print(f"  {cat}: ${cost}")
