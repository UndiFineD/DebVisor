"""
Tests for AI-Assisted Runbooks.
"""
import pytest
from opt.services.ops.runbooks import RunbookGenerator


@pytest.fixture
def generator() -> None:
    return RunbookGenerator()  # type: ignore[return-value]


def test_generate_runbook_high_cpu(generator):
    context = {"hostname": "web-01"}
    runbook = generator.generate_runbook("high_cpu", context)

    assert runbook is not None
    assert runbook.title == "High CPU Usage Investigation"
    assert "web-01" in runbook.description
    assert len(runbook.steps) == 3
    assert runbook.steps[0].command == "top -b -n 1 | head -n 20"


def test_generate_runbook_disk_space(generator):
    context = {"hostname": "db-01", "partition": "/var/lib/mysql"}
    runbook = generator.generate_runbook("disk_space", context)

    assert runbook is not None
    assert "db-01" in runbook.description
    assert "/var/lib/mysql" in runbook.steps[0].command


def test_generate_runbook_missing_context(generator):
    context = {"hostname": "web-01"}    # Missing partition
    runbook = generator.generate_runbook("disk_space", context)
    assert runbook is None


def test_generate_runbook_unknown_type(generator):
    runbook = generator.generate_runbook("unknown_alert", {})
    assert runbook is None


def test_suggest_runbooks(generator):
    keywords = ["cpu", "performance"]
    suggestions = generator.suggest_runbooks(keywords)

    assert len(suggestions) > 0
    assert suggestions[0]["type"] == "high_cpu"
    assert suggestions[0]["relevance"] >= 1


def test_suggest_runbooks_service(generator):
    keywords = ["service", "restart"]
    suggestions = generator.suggest_runbooks(keywords)

    # service_down template has "service" tag and "restart" in steps (though search is on title/desc/tags currently)
    # Let's check if it matches.
    # "service_down" title: "Service {service_name} Down" -> matches "service"
    # "service_down" tags: ["service", "availability"] -> matches "service"

    found = any(s["type"] == "service_down" for s in suggestions)
    assert found