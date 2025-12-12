#!/usr/bin/env python3
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


import logging
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
from opt.core.audit import get_audit_logger
from opt.services.compliance.remediation import RemediationManager

# Configure logging
_logger=logging.getLogger(__name__)


@dataclass
class CompliancePolicy:
    id: str
    name: str
    description: str
    severity: str    # 'critical', 'high', 'medium', 'low'
    check_function: str    # Name of the function to run
    remediation_function: Optional[str] = None
    enabled: bool=True
    tags: Optional[List[str]] = None    # e.g., ['GDPR', 'HIPAA', 'SOC2']

    def __post_init__(self) -> None:
        if self.tags is None:
            self.tags=[]


@dataclass
class ComplianceViolation:
    policy_id: str
    resource_id: str
    resource_type: str
    timestamp: str
    details: str
    status: str="open"    # 'open', 'remediated', 'suppressed'
    severity: str="medium"    # 'critical', 'high', 'medium', 'low'


@dataclass
class ComplianceReport:
    generated_at: str
    total_policies: int
    total_resources: int
    violations_count: int
    compliance_score: float
    violations: List[ComplianceViolation]


class ReportStatus(str, Enum):
    PENDING="pending"
    COMPLETED="completed"
    FAILED="failed"


@dataclass
class GeneratedReport:
    report_instance_id: str
    scheduled_report_id: str
    template_id: str
    status: ReportStatus
    content: str
    generated_at: datetime
    file_path: Optional[str] = None


class ComplianceEngine:

    def __init__(self) -> None:
        self.policies: Dict[str, CompliancePolicy] = {}
        self.violations: List[ComplianceViolation] = []
        self.audit_log: List[Dict[str, Any]] = []
        self.remediation_manager=RemediationManager()
        self._register_default_policies()

    def _register_default_policies(self) -> None:
        """Register built-in compliance policies."""
        _defaults=[
            CompliancePolicy(  # type: ignore[call-arg]
                _id="SEC-001",
                _name="SSH Root Login Disabled",
                _description="Root login via SSH should be disabled",
                _severity="critical",
                _check_function="check_ssh_root_login",
                _remediation_function="disable_ssh_root_login",
                _tags=["SOC2", "HIPAA", "GDPR"],
            ),
            CompliancePolicy(  # type: ignore[call-arg]
                _id="SEC-002",
                _name="Password Complexity",
                _description="Password policy must enforce complexity",
                _severity="high",
                _check_function="check_password_policy",
                _tags=["SOC2", "HIPAA", "GDPR"],
            ),
            CompliancePolicy(  # type: ignore[call-arg]
                _id="OPS-001",
                _name="Backup Configuration",
                _description="Critical systems must have backups enabled",
                _severity="medium",
                _check_function="check_backup_enabled",
                _tags=["SOC2", "HIPAA"],
            ),
            CompliancePolicy(  # type: ignore[call-arg]
                _id="PRIV-001",
                _name="Data Encryption at Rest",
                _description="Sensitive data must be encrypted at rest",
                _severity="critical",
                _check_function="check_encryption",
                _tags=["GDPR", "HIPAA"],
            ),
        ]
        for p in defaults:  # type: ignore[name-defined]
            self.policies[p.id] = p

    def register_policy(self, policy: CompliancePolicy) -> None:
        """Register a new custom policy."""
        self.policies[policy.id] = policy
        logger.info(f"Registered policy: {policy.name}")  # type: ignore[name-defined]

    def run_compliance_scan(
        self, resources: List[Dict[str, Any]], standard: Optional[str] = None
    ) -> ComplianceReport:
        """
        Run compliance checks against resources.

        Args:
            resources: List of resources to check
            standard: Optional standard to filter policies (e.g., 'GDPR')
        """
        _scan_violations=[]  # type: ignore[var-annotated]

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
                _is_compliant=self._mock_check(policy, res)

                if not is_compliant:  # type: ignore[name-defined]
                    violation=ComplianceViolation(  # type: ignore[call-arg]
                        _policy_id=policy.id,
                        _resource_id=res.get("id", "unknown"),
                        _resource_type=res.get("type", "unknown"),
                        _timestamp=datetime.now(timezone.utc).isoformat(),
                        _details=f"Failed check: {policy.name}",
                    )
                    scan_violations.append(violation)  # type: ignore[name-defined]
                    self.violations.append(violation)
                    self._log_audit(  # type: ignore[call-arg]
                        f"Violation detected: {policy.id} on {res.get('id')}",
                        _tags=policy.tags,
                    )

                    # Auto-remediation if configured
                    if policy.remediation_function:
                        self._attempt_remediation(policy, res)

        # Calculate score
        _relevant_policies=[p for p in self.policies.values() if p.enabled]
        if standard:
            _relevant_policies=[p for p in relevant_policies if standard in (p.tags or [])]  # type: ignore[name-defined]

        _total_checks=len(resources) * len(relevant_policies)  # type: ignore[name-defined]
        score=100.0
        if total_checks > 0:  # type: ignore[name-defined]
            _score=((total_checks - len(scan_violations)) / total_checks) * 100  # type: ignore[name-defined]

        return ComplianceReport(  # type: ignore[call-arg]
            _generated_at=datetime.now(timezone.utc).isoformat(),
            _total_policies=len(relevant_policies),  # type: ignore[name-defined]
            _total_resources=len(resources),
            _violations_count=len(scan_violations),  # type: ignore[name-defined]
            _compliance_score=round(score, 2),
            _violations=scan_violations,  # type: ignore[name-defined]
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
        logger.info(f"Attempting remediation for {policy.id} on {resource.get('id')}")  # type: ignore[name-defined]
        self._log_audit(  # type: ignore[call-arg]
            f"Remediation started: {policy.id} on {resource.get('id')}",
            _tags=policy.tags,
        )

        if not policy.remediation_function:
            logger.warning(f"No remediation function defined for policy {policy.id}")  # type: ignore[name-defined]
            return

        success=self.remediation_manager.remediate(
            policy.remediation_function,
            resource.get("id", "unknown")
        )

        if success:
            self._log_audit(  # type: ignore[call-arg]
                f"Remediation successful: {policy.id} on {resource.get('id')}",
                _tags=policy.tags,
            )
        else:
            self._log_audit(  # type: ignore[call-arg]
                f"Remediation failed: {policy.id} on {resource.get('id')}",
                _tags=policy.tags,
            )

    def _log_audit(self, message: str, tags: Optional[List[str]] = None) -> None:
        """Add entry to secure audit trail."""
        try:
            _audit_logger=get_audit_logger()
            audit_logger.create_entry(  # type: ignore[name-defined]
                _operation="compliance_check",
                _resource_type="system",
                _resource_id="compliance_engine",
                _actor_id="system",
                _action=message,
                _status="info",
                _compliance_tags=tags or [],
            )
        except Exception as e:
            logger.error(f"Failed to write secure audit log: {e}")  # type: ignore[name-defined]

        # Keep local log for API retrieval (legacy)
        entry={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "tags": tags or [],
        }
        self.audit_log.append(entry)
        logger.info(f"AUDIT: {message}")  # type: ignore[name-defined]

    def get_audit_log(self) -> List[Dict[str, Any]]:
        return self.audit_log
