import unittest
import pytest
from opt.services.compliance.core import ComplianceEngine, CompliancePolicy


@pytest.fixture


def engine() -> None:
    return ComplianceEngine()  # type: ignore[return-value]


@pytest.fixture


def sample_resources() -> None:
    return [{"id": "res-1", "type": "vm"}, {"id": "res-noncompliant", "type": "vm"}]  # type: ignore[return-value]


def test_default_policies(engine):
    assert len(engine.policies) >= 3
    assert "SEC-001" in engine.policies


def test_policy_registration(engine):
    p = CompliancePolicy(
        _id = "TEST-001",
        _name = "Test Policy",
        _description = "Test",
        _severity = "low",
        _check_function = "check_test",
    )
    engine.register_policy(p)
    assert "TEST-001" in engine.policies


def test_compliance_scan(engine, sample_resources):
    report = engine.run_compliance_scan(sample_resources)
    assert report.total_resources == 2
    assert report.violations_count > 0
    # res-noncompliant should trigger violations in mock check
    assert any(v.resource_id == "res-noncompliant" for v in report.violations)


def test_audit_logging(engine, sample_resources):
    engine.run_compliance_scan(sample_resources)
    logs = engine.get_audit_log()
    assert len(logs) > 0
    assert any("Violation detected" in line_item["message"] for line_item in logs)


def test_remediation_trigger(engine):
    # Create a policy with remediation
    p = CompliancePolicy(
        id="REM-001",
        _name = "Remediation Test",
        _description = "Test",
        _severity = "high",
        _check_function = "check_rem",
        _remediation_function = "do_rem",
    )
    engine.register_policy(p)

    resources = [{"id": "res-noncompliant", "type": "vm"}]
    engine.run_compliance_scan(resources)

    logs = engine.get_audit_log()
    assert any("Remediation started" in line_item["message"] for line_item in logs)
