import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from opt.core.audit import get_audit_logger
from opt.services.compliance.remediation import RemediationManager

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class CompliancePolicy:
    id: str
    name: str
    description: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    check_function: str  # Name of the function to run
    remediation_function: Optional[str] = None
    enabled: bool = True
    tags: Optional[List[str]] = None  # e.g., ['GDPR', 'HIPAA', 'SOC2']

    def __post_init__(self) -> None:
        if self.tags is None:
            self.tags = []


@dataclass
class ComplianceViolation:
    policy_id: str
    resource_id: str
    resource_type: str
    timestamp: str
    details: str
    status: str = "open"  # 'open', 'remediated', 'suppressed'
    severity: str = "medium"  # 'critical', 'high', 'medium', 'low'


@dataclass
class ComplianceReport:
    generated_at: str
    total_policies: int
    total_resources: int
    violations_count: int
    compliance_score: float
    violations: List[ComplianceViolation]


class ComplianceEngine:
    def __init__(self) -> None:
        self.policies: Dict[str, CompliancePolicy] = {}
        self.violations: List[ComplianceViolation] = []
        self.audit_log: List[Dict[str, Any]] = []
        self.remediation_manager = RemediationManager()
        self._register_default_policies()

    def _register_default_policies(self) -> None:
        """Register built-in compliance policies."""
        defaults = [
            CompliancePolicy(
                id="SEC-001",
                name="SSH Root Login Disabled",
                description="Root login via SSH should be disabled",
                severity="critical",
                check_function="check_ssh_root_login",
                remediation_function="disable_ssh_root_login",
                tags=["SOC2", "HIPAA", "GDPR"],
            ),
            CompliancePolicy(
                id="SEC-002",
                name="Password Complexity",
                description="Password policy must enforce complexity",
                severity="high",
                check_function="check_password_policy",
                tags=["SOC2", "HIPAA", "GDPR"],
            ),
            CompliancePolicy(
                id="OPS-001",
                name="Backup Configuration",
                description="Critical systems must have backups enabled",
                severity="medium",
                check_function="check_backup_enabled",
                tags=["SOC2", "HIPAA"],
            ),
            CompliancePolicy(
                id="PRIV-001",
                name="Data Encryption at Rest",
                description="Sensitive data must be encrypted at rest",
                severity="critical",
                check_function="check_encryption",
                tags=["GDPR", "HIPAA"],
            ),
        ]
        for p in defaults:
            self.policies[p.id] = p

    def register_policy(self, policy: CompliancePolicy) -> None:
        """Register a new custom policy."""
        self.policies[policy.id] = policy
        logger.info(f"Registered policy: {policy.name}")

    def run_compliance_scan(
        self, resources: List[Dict[str, Any]], standard: Optional[str] = None
    ) -> ComplianceReport:
        """
        Run compliance checks against resources.

        Args:
            resources: List of resources to check
            standard: Optional standard to filter policies (e.g., 'GDPR')
        """
        scan_violations = []

        for res in resources:
            for policy in self.policies.values():
                if not policy.enabled:
                    continue

                # Filter by standard if specified
                if standard and standard not in (policy.tags or []):
                    continue

                # Simulate check execution (in real implementation, this would call
                # actual check logic)
                # For demo, we use a mock check based on resource tags/properties
                is_compliant = self._mock_check(policy, res)

                if not is_compliant:
                    violation = ComplianceViolation(
                        policy_id=policy.id,
                        resource_id=res.get("id", "unknown"),
                        resource_type=res.get("type", "unknown"),
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        details=f"Failed check: {policy.name}",
                    )
                    scan_violations.append(violation)
                    self.violations.append(violation)
                    self._log_audit(
                        f"Violation detected: {policy.id} on {res.get('id')}",
                        tags=policy.tags,
                    )

                    # Auto-remediation if configured
                    if policy.remediation_function:
                        self._attempt_remediation(policy, res)

        # Calculate score
        relevant_policies = [p for p in self.policies.values() if p.enabled]
        if standard:
            relevant_policies = [p for p in relevant_policies if standard in (p.tags or [])]

        total_checks = len(resources) * len(relevant_policies)
        score = 100.0
        if total_checks > 0:
            score = ((total_checks - len(scan_violations)) / total_checks) * 100

        return ComplianceReport(
            generated_at=datetime.now(timezone.utc).isoformat(),
            total_policies=len(relevant_policies),
            total_resources=len(resources),
            violations_count=len(scan_violations),
            compliance_score=round(score, 2),
            violations=scan_violations,
        )

    def _mock_check(self, policy: CompliancePolicy, resource: Dict[str, Any]) -> bool:
        """Mock check logic for demonstration."""
        # In a real system, this would dispatch to specific check functions
        # Here we simulate failures based on resource name for testing
        if "noncompliant" in resource.get("id", ""):
            return False
        return True

    def _attempt_remediation(self, policy: CompliancePolicy, resource: Dict[str, Any]) -> None:
        """Attempt automatic remediation."""
        logger.info(f"Attempting remediation for {policy.id} on {resource.get('id')}")
        self._log_audit(
            f"Remediation started: {policy.id} on {resource.get('id')}",
            tags=policy.tags,
        )

        if not policy.remediation_function:
            logger.warning(f"No remediation function defined for policy {policy.id}")
            return

        success = self.remediation_manager.remediate(
            policy.remediation_function,
            resource.get("id", "unknown")
        )

        if success:
            self._log_audit(
                f"Remediation successful: {policy.id} on {resource.get('id')}",
                tags=policy.tags,
            )
        else:
            self._log_audit(
                f"Remediation failed: {policy.id} on {resource.get('id')}",
                tags=policy.tags,
            )

    def _log_audit(self, message: str, tags: Optional[List[str]] = None) -> None:
        """Add entry to secure audit trail."""
        try:
            audit_logger = get_audit_logger()
            audit_logger.create_entry(
                operation="compliance_check",
                resource_type="system",
                resource_id="compliance_engine",
                actor_id="system",
                action=message,
                status="info",
                compliance_tags=tags or [],
            )
        except Exception as e:
            logger.error(f"Failed to write secure audit log: {e}")

        # Keep local log for API retrieval (legacy)
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "tags": tags or [],
        }
        self.audit_log.append(entry)
        logger.info(f"AUDIT: {message}")

    def get_audit_log(self) -> List[Dict[str, Any]]:
        return self.audit_log
