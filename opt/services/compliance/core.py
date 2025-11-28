import logging
import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timezone

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

@dataclass
class ComplianceViolation:
    policy_id: str
    resource_id: str
    resource_type: str
    timestamp: str
    details: str
    status: str = "open"  # 'open', 'remediated', 'suppressed'

@dataclass
class ComplianceReport:
    generated_at: str
    total_policies: int
    total_resources: int
    violations_count: int
    compliance_score: float
    violations: List[ComplianceViolation]

class ComplianceEngine:
    def __init__(self):
        self.policies: Dict[str, CompliancePolicy] = {}
        self.violations: List[ComplianceViolation] = []
        self.audit_log: List[Dict] = []
        self._register_default_policies()

    def _register_default_policies(self):
        """Register built-in compliance policies."""
        defaults = [
            CompliancePolicy(
                id="SEC-001",
                name="SSH Root Login Disabled",
                description="Root login via SSH should be disabled",
                severity="critical",
                check_function="check_ssh_root_login",
                remediation_function="disable_ssh_root_login"
            ),
            CompliancePolicy(
                id="SEC-002",
                name="Password Complexity",
                description="Password policy must enforce complexity",
                severity="high",
                check_function="check_password_policy"
            ),
            CompliancePolicy(
                id="OPS-001",
                name="Backup Configuration",
                description="Critical systems must have backups enabled",
                severity="medium",
                check_function="check_backup_enabled"
            )
        ]
        for p in defaults:
            self.policies[p.id] = p

    def register_policy(self, policy: CompliancePolicy):
        """Register a new custom policy."""
        self.policies[policy.id] = policy
        logger.info(f"Registered policy: {policy.name}")

    def run_compliance_scan(self, resources: List[Dict[str, Any]]) -> ComplianceReport:
        """Run compliance checks against resources."""
        scan_violations = []
        
        for res in resources:
            for policy in self.policies.values():
                if not policy.enabled:
                    continue
                
                # Simulate check execution (in real implementation, this would call actual check logic)
                # For demo, we use a mock check based on resource tags/properties
                is_compliant = self._mock_check(policy, res)
                
                if not is_compliant:
                    violation = ComplianceViolation(
                        policy_id=policy.id,
                        resource_id=res.get("id", "unknown"),
                        resource_type=res.get("type", "unknown"),
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        details=f"Failed check: {policy.name}"
                    )
                    scan_violations.append(violation)
                    self.violations.append(violation)
                    self._log_audit(f"Violation detected: {policy.id} on {res.get('id')}")

                    # Auto-remediation if configured
                    if policy.remediation_function:
                        self._attempt_remediation(policy, res)

        # Calculate score
        total_checks = len(resources) * len([p for p in self.policies.values() if p.enabled])
        score = 100.0
        if total_checks > 0:
            score = ((total_checks - len(scan_violations)) / total_checks) * 100

        return ComplianceReport(
            generated_at=datetime.now(timezone.utc).isoformat(),
            total_policies=len(self.policies),
            total_resources=len(resources),
            violations_count=len(scan_violations),
            compliance_score=round(score, 2),
            violations=scan_violations
        )

    def _mock_check(self, policy: CompliancePolicy, resource: Dict) -> bool:
        """Mock check logic for demonstration."""
        # In a real system, this would dispatch to specific check functions
        # Here we simulate failures based on resource name for testing
        if "noncompliant" in resource.get("id", ""):
            return False
        return True

    def _attempt_remediation(self, policy: CompliancePolicy, resource: Dict):
        """Attempt automatic remediation."""
        logger.info(f"Attempting remediation for {policy.id} on {resource.get('id')}")
        self._log_audit(f"Remediation started: {policy.id} on {resource.get('id')}")
        # Simulate success
        self._log_audit(f"Remediation successful: {policy.id} on {resource.get('id')}")

    def _log_audit(self, message: str):
        """Add entry to audit trail."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message
        }
        self.audit_log.append(entry)
        logger.info(f"AUDIT: {message}")

    def get_audit_log(self) -> List[Dict]:
        return self.audit_log
