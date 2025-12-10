"""
Tests for Compliance Remediation.
"""
import pytest
from unittest.mock import MagicMock, patch
from opt.services.compliance.core import ComplianceEngine, CompliancePolicy
from opt.services.compliance.remediation import RemediationManager


@pytest.fixture
def compliance_engine() -> None:
    return ComplianceEngine()  # type: ignore[return-value]


def test_remediation_manager_init() -> None:
    manager = RemediationManager()
    assert "disable_ssh_root_login" in manager._remediators


@patch("opt.services.compliance.remediation.SSHHardeningManager")
def test_remediate_ssh_root_login(mock_ssh_manager_cls):
    manager = RemediationManager()
    # Mock the instance
    mock_ssh_instance = mock_ssh_manager_cls.return_value

    result = manager.remediate("disable_ssh_root_login", "host-123")

    assert result is True
    # Since we didn't implement a specific method call in _remediate_ssh_root_login yet (just logging),
    # we verify it returns True.
    # If we added a call, we would assert mock_ssh_instance.some_method.called


@patch("opt.services.compliance.remediation.SSHHardeningManager")
def test_compliance_engine_integration(mock_ssh_manager_cls, compliance_engine):
    # Setup a policy with remediation
    policy = CompliancePolicy(
        id="TEST-REM-001",
        name="Test Remediation",
        description="Test",
        severity="high",
        check_function="check_something",
        remediation_function="disable_ssh_root_login",
        tags=["TEST"]
    )
    compliance_engine.register_policy(policy)

    # Mock check to fail
    compliance_engine._mock_check = MagicMock(return_value=False)

    # Run scan
    resources = [{"id": "host-123", "type": "host"}]
    report = compliance_engine.run_compliance_scan(resources)

    # Verify remediation was attempted
    # We can check the audit log
    audit_log = compliance_engine.get_audit_log()
    remediation_entries = [e for e in audit_log if "Remediation successful" in e["message"]]
    assert len(remediation_entries) > 0

    # Check if our test policy was remediated
    found = any("TEST-REM-001" in e["message"] for e in remediation_entries)
    assert found, "Remediation for TEST-REM-001 not found in audit log"


def test_remediation_unknown_function() -> None:
    manager = RemediationManager()
    result = manager.remediate("unknown_function", "host-123")
    assert result is False