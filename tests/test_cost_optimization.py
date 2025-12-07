import pytest
from opt.services.cost_optimization.core import CostOptimizer


@pytest.fixture
def optimizer():
    return CostOptimizer()


@pytest.fixture
def sample_resources():
    return [
        {
            "id": "vm-active", "type": "vm", "project": "prod",
            "specs": {"cpu": 4, "memory_gb": 16, "storage_gb": 100},
            "metrics": {"cpu_avg": 50, "uptime_hours": 730}
        },
        {
            "id": "vm-idle", "type": "vm", "project": "dev",
            "specs": {"cpu": 2, "memory_gb": 8, "storage_gb": 50},
            "metrics": {"cpu_avg": 2, "uptime_hours": 730}
        },
        {
            "id": "vm-oversized", "type": "vm", "project": "test",
            "specs": {"cpu": 8, "memory_gb": 32, "storage_gb": 100},
            "metrics": {"cpu_avg": 10, "uptime_hours": 730}
        }
    ]


def test_cost_calculation(optimizer):
    specs = {"cpu": 1, "memory_gb": 1, "storage_gb": 1}
    # Default pricing: cpu=0.05, mem=0.02, storage=0.001
    # Monthly (730h): 1*0.05*730 + 1*0.02*730 + 1*0.001*730
    # = 36.5 + 14.6 + 0.73 = 51.83
    cost = optimizer._calculate_monthly_cost(specs)
    assert cost == pytest.approx(51.83, 0.01)


def test_report_generation(optimizer, sample_resources):
    report = optimizer.generate_cost_report(sample_resources)
    assert report.total_cost > 0
    assert "prod" in report.project_breakdown
    assert "dev" in report.project_breakdown
    assert "vm" in report.resource_breakdown


def test_idle_detection(optimizer, sample_resources):
    recs = optimizer.analyze_resource_usage(sample_resources)
    idle_recs = [r for r in recs if r.recommendation_type == "idle"]
    assert len(idle_recs) == 1
    assert idle_recs[0].resource_id == "vm-idle"
    assert idle_recs[0].action == "stop"


def test_rightsizing_detection(optimizer, sample_resources):
    recs = optimizer.analyze_resource_usage(sample_resources)
    resize_recs = [r for r in recs if r.recommendation_type == "rightsizing"]
    assert len(resize_recs) == 1
    assert resize_recs[0].resource_id == "vm-oversized"
    assert resize_recs[0].action == "resize"


def test_pricing_update(optimizer):
    optimizer.set_pricing({"cpu_hourly": 1.0})
    assert optimizer.pricing["cpu_hourly"] == 1.0

    specs = {"cpu": 1, "memory_gb": 0, "storage_gb": 0}
    cost = optimizer._calculate_monthly_cost(specs)
    assert cost == 730.0  # 1 * 1.0 * 730
