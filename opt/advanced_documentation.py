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

"""
Advanced documentation support - ADRs, playbooks, and procedures.

Provides:
- Architecture Decision Records (ADRs)
- Operational playbooks
- Security procedures
- Troubleshooting guides
- Performance tuning documentation
- Disaster recovery procedures
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any


class DecisionStatus(Enum):
    """ADR decision status."""

    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"


class Severity(Enum):
    """Severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PlaybookType(Enum):
    """Types of playbooks."""

    INCIDENT_RESPONSE = "incident_response"
    DEPLOYMENT = "deployment"
    SCALING = "scaling"
    MAINTENANCE = "maintenance"
    DISASTER_RECOVERY = "disaster_recovery"
    SECURITY_INCIDENT = "security_incident"
    TROUBLESHOOTING = "troubleshooting"


@dataclass
class ArchitectureDecisionRecord:
    """Architecture Decision Record (ADR)."""

    adr_id: str
    title: str
    status: DecisionStatus
    context: str
    decision: str
    consequences: List[str]
    alternatives: Dict[str, str]    # alternative -> rationale
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)
    author: str = "Architecture Team"
    related_adrs: List[str] = field(default_factory=list)
    implementation_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "adr_id": self.adr_id,
            "title": self.title,
            "status": self.status.value,
            "context": self.context,
            "decision": self.decision,
            "consequences": self.consequences,
            "alternatives": self.alternatives,
            "created_date": self.created_date.isoformat(),
            "updated_date": self.updated_date.isoformat(),
            "author": self.author,
            "related_adrs": self.related_adrs,
            "implementation_notes": self.implementation_notes,
        }


@dataclass
class PlaybookStep:
    """Single step in a playbook."""

    step_number: int
    title: str
    description: str
    commands: List[str] = field(default_factory=list)
    expected_output: str = ""
    verification: str = ""
    rollback_steps: List[str] = field(default_factory=list)
    estimated_duration_seconds: int = 60
    critical: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "step_number": self.step_number,
            "title": self.title,
            "description": self.description,
            "commands": self.commands,
            "expected_output": self.expected_output,
            "verification": self.verification,
            "rollback_steps": self.rollback_steps,
            "estimated_duration_seconds": self.estimated_duration_seconds,
            "critical": self.critical,
        }


@dataclass
class OperationalPlaybook:
    """Operational playbook for procedures."""

    playbook_id: str
    title: str
    playbook_type: PlaybookType
    description: str
    severity: Severity
    steps: List[PlaybookStep] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)
    author: str = "Operations Team"
    estimated_duration_minutes: int = 30
    requires_approval: bool = False
    related_playbooks: List[str] = field(default_factory=list)

    def add_step(self, step: PlaybookStep) -> None:
        """Add step to playbook."""
        self.steps.append(step)

    def total_duration_minutes(self) -> float:
        """Calculate total duration."""
        total_seconds = sum(step.estimated_duration_seconds for step in self.steps)
        return total_seconds / 60

    def get_critical_steps(self) -> List[PlaybookStep]:
        """Get critical steps."""
        return [step for step in self.steps if step.critical]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "playbook_id": self.playbook_id,
            "title": self.title,
            "type": self.playbook_type.value,
            "description": self.description,
            "severity": self.severity.value,
            "steps": [step.to_dict() for step in self.steps],
            "prerequisites": self.prerequisites,
            "success_criteria": self.success_criteria,
            "created_date": self.created_date.isoformat(),
            "updated_date": self.updated_date.isoformat(),
            "author": self.author,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "requires_approval": self.requires_approval,
            "related_playbooks": self.related_playbooks,
        }


@dataclass
class SecurityProcedure:
    """Security procedure documentation."""

    procedure_id: str
    title: str
    description: str
    severity: Severity
    affected_systems: List[str]
    steps: List[str]
    compliance_frameworks: List[str]
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)
    author: str = "Security Team"
    review_frequency_days: int = 90
    requires_audit_log: bool = True
    notification_channels: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "procedure_id": self.procedure_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "affected_systems": self.affected_systems,
            "steps": self.steps,
            "compliance_frameworks": self.compliance_frameworks,
            "created_date": self.created_date.isoformat(),
            "updated_date": self.updated_date.isoformat(),
            "author": self.author,
            "review_frequency_days": self.review_frequency_days,
            "requires_audit_log": self.requires_audit_log,
            "notification_channels": self.notification_channels,
        }


@dataclass
class TroubleshootingGuide:
    """Troubleshooting guide for issues."""

    guide_id: str
    title: str
    symptom_description: str
    root_cause: str
    resolution_steps: List[str]
    diagnostic_commands: List[str] = field(default_factory=list)
    log_files_to_check: List[str] = field(default_factory=list)
    related_issues: List[str] = field(default_factory=list)
    severity: Severity = Severity.MEDIUM
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)
    author: str = "Support Team"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "guide_id": self.guide_id,
            "title": self.title,
            "symptom": self.symptom_description,
            "root_cause": self.root_cause,
            "resolution": self.resolution_steps,
            "diagnostics": self.diagnostic_commands,
            "logs": self.log_files_to_check,
            "related_issues": self.related_issues,
            "severity": self.severity.value,
            "created_date": self.created_date.isoformat(),
            "updated_date": self.updated_date.isoformat(),
            "author": self.author,
        }


@dataclass
class PerformanceTuningGuide:
    """Performance tuning recommendations."""

    guide_id: str
    component: str
    description: str
    parameter_name: str
    current_value: Any
    recommended_value: Any
    tuning_impact: str    # "high", "medium", "low"
    prerequisites: List[str]
    rollback_steps: List[str]
    monitoring_metrics: List[str]
    created_date: datetime = field(default_factory=datetime.now)
    author: str = "Performance Team"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "guide_id": self.guide_id,
            "component": self.component,
            "description": self.description,
            "parameter": self.parameter_name,
            "current_value": str(self.current_value),
            "recommended_value": str(self.recommended_value),
            "impact": self.tuning_impact,
            "prerequisites": self.prerequisites,
            "rollback": self.rollback_steps,
            "monitoring": self.monitoring_metrics,
            "created_date": self.created_date.isoformat(),
            "author": self.author,
        }


@dataclass
class DisasterRecoveryProcedure:
    """Disaster recovery procedure."""

    procedure_id: str
    title: str
    disaster_type: str
    rpo_minutes: int    # Recovery Point Objective
    rto_minutes: int    # Recovery Time Objective
    affected_systems: List[str]
    pre_disaster_checklist: List[str]
    recovery_steps: List[str]
    validation_steps: List[str]
    communication_plan: str
    backup_location: str
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)
    author: str = "Disaster Recovery Team"
    last_tested: Optional[datetime] = None
    test_frequency_days: int = 90

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "procedure_id": self.procedure_id,
            "title": self.title,
            "disaster_type": self.disaster_type,
            "rpo_minutes": self.rpo_minutes,
            "rto_minutes": self.rto_minutes,
            "affected_systems": self.affected_systems,
            "pre_disaster_checklist": self.pre_disaster_checklist,
            "recovery_steps": self.recovery_steps,
            "validation": self.validation_steps,
            "communication_plan": self.communication_plan,
            "backup_location": self.backup_location,
            "created_date": self.created_date.isoformat(),
            "updated_date": self.updated_date.isoformat(),
            "author": self.author,
            "last_tested": self.last_tested.isoformat() if self.last_tested else None,
            "test_frequency_days": self.test_frequency_days,
        }


class DocumentationLibrary:
    """Central documentation library."""

    def __init__(self) -> None:
        """Initialize documentation library."""
        self.adrs: Dict[str, ArchitectureDecisionRecord] = {}
        self.playbooks: Dict[str, OperationalPlaybook] = {}
        self.security_procedures: Dict[str, SecurityProcedure] = {}
        self.troubleshooting_guides: Dict[str, TroubleshootingGuide] = {}
        self.performance_guides: Dict[str, PerformanceTuningGuide] = {}
        self.dr_procedures: Dict[str, DisasterRecoveryProcedure] = {}

    def add_adr(self, adr: ArchitectureDecisionRecord) -> bool:
        """Add ADR."""
        self.adrs[adr.adr_id] = adr
        return True

    def add_playbook(self, playbook: OperationalPlaybook) -> bool:
        """Add playbook."""
        self.playbooks[playbook.playbook_id] = playbook
        return True

    def add_security_procedure(self, procedure: SecurityProcedure) -> bool:
        """Add security procedure."""
        self.security_procedures[procedure.procedure_id] = procedure
        return True

    def add_troubleshooting_guide(self, guide: TroubleshootingGuide) -> bool:
        """Add troubleshooting guide."""
        self.troubleshooting_guides[guide.guide_id] = guide
        return True

    def add_performance_guide(self, guide: PerformanceTuningGuide) -> bool:
        """Add performance guide."""
        self.performance_guides[guide.guide_id] = guide
        return True

    def add_dr_procedure(self, procedure: DisasterRecoveryProcedure) -> bool:
        """Add DR procedure."""
        self.dr_procedures[procedure.procedure_id] = procedure
        return True

    def get_adr(self, adr_id: str) -> Optional[ArchitectureDecisionRecord]:
        """Get ADR by ID."""
        return self.adrs.get(adr_id)

    def get_playbook(self, playbook_id: str) -> Optional[OperationalPlaybook]:
        """Get playbook by ID."""
        return self.playbooks.get(playbook_id)

    def get_playbooks_by_type(
        self, playbook_type: PlaybookType
    ) -> List[OperationalPlaybook]:
        """Get playbooks by type."""
        return [p for p in self.playbooks.values() if p.playbook_type == playbook_type]

    def get_security_procedure(self, procedure_id: str) -> Optional[SecurityProcedure]:
        """Get security procedure."""
        return self.security_procedures.get(procedure_id)

    def get_procedures_by_framework(self, framework: str) -> List[SecurityProcedure]:
        """Get procedures by compliance framework."""
        return [
            p
            for p in self.security_procedures.values()
            if framework in p.compliance_frameworks
        ]

    def get_troubleshooting_guide(
        self, guide_id: str
    ) -> Optional[TroubleshootingGuide]:
        """Get troubleshooting guide."""
        return self.troubleshooting_guides.get(guide_id)

    def get_performance_guide(self, guide_id: str) -> Optional[PerformanceTuningGuide]:
        """Get performance guide."""
        return self.performance_guides.get(guide_id)

    def get_guides_by_component(self, component: str) -> List[PerformanceTuningGuide]:
        """Get performance guides by component."""
        return [g for g in self.performance_guides.values() if g.component == component]

    def get_dr_procedure(
        self, procedure_id: str
    ) -> Optional[DisasterRecoveryProcedure]:
        """Get DR procedure."""
        return self.dr_procedures.get(procedure_id)

    def get_all_adrs(self) -> Dict[str, ArchitectureDecisionRecord]:
        """Get all ADRs."""
        return self.adrs.copy()

    def get_all_playbooks(self) -> Dict[str, OperationalPlaybook]:
        """Get all playbooks."""
        return self.playbooks.copy()

    def get_documentation_index(self) -> Dict[str, Any]:
        """Get documentation index."""
        return {
            "architecture_decisions": len(self.adrs),
            "playbooks": len(self.playbooks),
            "security_procedures": len(self.security_procedures),
            "troubleshooting_guides": len(self.troubleshooting_guides),
            "performance_guides": len(self.performance_guides),
            "dr_procedures": len(self.dr_procedures),
            "total_documents": (
                len(self.adrs)
                + len(self.playbooks)
                + len(self.security_procedures)
                + len(self.troubleshooting_guides)
                + len(self.performance_guides)
                + len(self.dr_procedures)
            ),
        }

    def export_documentation(self) -> Dict[str, Any]:
        """Export all documentation."""
        return {
            "adrs": {k: v.to_dict() for k, v in self.adrs.items()},
            "playbooks": {k: v.to_dict() for k, v in self.playbooks.items()},
            "security_procedures": {
                k: v.to_dict() for k, v in self.security_procedures.items()
            },
            "troubleshooting_guides": {
                k: v.to_dict() for k, v in self.troubleshooting_guides.items()
            },
            "performance_guides": {
                k: v.to_dict() for k, v in self.performance_guides.items()
            },
            "dr_procedures": {k: v.to_dict() for k, v in self.dr_procedures.items()},
        }

    def validate_references(self) -> Dict[str, List[str]]:
        """Validate all cross-references."""
        issues: Dict[str, List[str]] = {
            "broken_adr_references": [],
            "broken_playbook_references": [],
            "missing_documents": [],
        }

        # Check ADR references
        for adr_id, adr in self.adrs.items():
            for related_id in adr.related_adrs:
                if related_id not in self.adrs:
                    issues["broken_adr_references"].append(f"{adr_id} -> {related_id}")

        # Check playbook references
        for playbook_id, playbook in self.playbooks.items():
            for related_id in playbook.related_playbooks:
                if related_id not in self.playbooks:
                    issues["broken_playbook_references"].append(
                        f"{playbook_id} -> {related_id}"
                    )

        return issues
