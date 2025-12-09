#!/usr/bin/env python3
"""
Tests for advanced documentation system.

Tests for:
  - Architecture Decision Records
  - Operational playbooks
  - Security procedures
  - Troubleshooting guides
  - Performance tuning guides
  - Disaster recovery procedures
  - Documentation library
"""

import unittest

from advanced_documentation import (
    ArchitectureDecisionRecord,
    DecisionStatus,
    PlaybookStep,
    OperationalPlaybook,
    PlaybookType,
    SecurityProcedure,
    TroubleshootingGuide,
    PerformanceTuningGuide,
    DisasterRecoveryProcedure,
    DocumentationLibrary,
    Severity,
)


class TestArchitectureDecisionRecord(unittest.TestCase):
    """Tests for ADRs."""

    def test_adr_creation(self) -> None:
        """Test creating ADR."""
        adr = ArchitectureDecisionRecord(
            adr_id="ADR-001",
            title="Use microservices architecture",
            status=DecisionStatus.ACCEPTED,
            context="Need scalable system",
            decision="Implement microservices",
            consequences=["Increased complexity", "Better scalability"],
            alternatives={"Monolith": "Simpler but less scalable"},
        )

        self.assertEqual(adr.adr_id, "ADR-001")
        self.assertEqual(adr.status, DecisionStatus.ACCEPTED)

    def test_adr_to_dict(self) -> None:
        """Test ADR conversion to dictionary."""
        adr = ArchitectureDecisionRecord(
            adr_id="ADR-001",
            title="Use microservices",
            status=DecisionStatus.ACCEPTED,
            context="Scaling requirement",
            decision="Microservices",
            consequences=["Increased complexity"],
            alternatives={"Monolith": "Simpler"},
        )

        adr_dict = adr.to_dict()

        self.assertEqual(adr_dict["adr_id"], "ADR-001")
        self.assertEqual(adr_dict["status"], "accepted")


class TestPlaybookStep(unittest.TestCase):
    """Tests for playbook steps."""

    def test_step_creation(self) -> None:
        """Test creating playbook step."""
        step = PlaybookStep(
            step_number=1,
            title="Verify prerequisites",
            description="Ensure all prerequisites are met",
            commands=["docker --version", "kubectl version"],
        )

        self.assertEqual(step.step_number, 1)
        self.assertEqual(len(step.commands), 2)
        self.assertFalse(step.critical)

    def test_critical_step(self) -> None:
        """Test marking step as critical."""
        step = PlaybookStep(
            step_number=1,
            title="Backup data",
            description="Backup all critical data",
            critical=True,
        )

        self.assertTrue(step.critical)

    def test_step_to_dict(self) -> None:
        """Test step conversion to dictionary."""
        step = PlaybookStep(
            step_number=1,
            title="Verify",
            description="Verification step",
            commands=["echo test"],
        )

        step_dict = step.to_dict()

        self.assertEqual(step_dict["step_number"], 1)
        self.assertEqual(step_dict["title"], "Verify")


class TestOperationalPlaybook(unittest.TestCase):
    """Tests for operational playbooks."""

    def test_playbook_creation(self) -> None:
        """Test creating playbook."""
        playbook = OperationalPlaybook(
            playbook_id="PB-001",
            title="Deployment procedure",
            playbook_type=PlaybookType.DEPLOYMENT,
            description="Standard deployment steps",
            severity=Severity.HIGH,
        )

        self.assertEqual(playbook.playbook_id, "PB-001")
        self.assertEqual(playbook.playbook_type, PlaybookType.DEPLOYMENT)

    def test_add_step(self) -> None:
        """Test adding step to playbook."""
        playbook = OperationalPlaybook(
            playbook_id="PB-001",
            title="Deployment",
            playbook_type=PlaybookType.DEPLOYMENT,
            description="Deploy",
            severity=Severity.HIGH,
        )

        step = PlaybookStep(step_number=1, title="Verify", description="Verification")

        playbook.add_step(step)

        self.assertEqual(len(playbook.steps), 1)

    def test_total_duration(self) -> None:
        """Test calculating total duration."""
        playbook = OperationalPlaybook(
            playbook_id="PB-001",
            title="Deployment",
            playbook_type=PlaybookType.DEPLOYMENT,
            description="Deploy",
            severity=Severity.HIGH,
        )

        step1 = PlaybookStep(
            step_number=1,
            title="Step 1",
            description="First",
            estimated_duration_seconds=60,
        )

        step2 = PlaybookStep(
            step_number=2,
            title="Step 2",
            description="Second",
            estimated_duration_seconds=120,
        )

        playbook.add_step(step1)
        playbook.add_step(step2)

        duration = playbook.total_duration_minutes()

        self.assertAlmostEqual(duration, 3.0, places=1)

    def test_get_critical_steps(self) -> None:
        """Test getting critical steps."""
        playbook = OperationalPlaybook(
            playbook_id="PB-001",
            title="Deployment",
            playbook_type=PlaybookType.DEPLOYMENT,
            description="Deploy",
            severity=Severity.HIGH,
        )

        step1 = PlaybookStep(
            step_number=1, title="Backup", description="Backup data", critical=True
        )

        step2 = PlaybookStep(
            step_number=2, title="Deploy", description="Deploy app", critical=False
        )

        playbook.add_step(step1)
        playbook.add_step(step2)

        critical = playbook.get_critical_steps()

        self.assertEqual(len(critical), 1)
        self.assertEqual(critical[0].title, "Backup")


class TestSecurityProcedure(unittest.TestCase):
    """Tests for security procedures."""

    def test_procedure_creation(self) -> None:
        """Test creating security procedure."""
        procedure = SecurityProcedure(
            procedure_id="SEC-001",
            title="Access control",
            description="Implement access controls",
            severity=Severity.CRITICAL,
            affected_systems=["web_server", "database"],
            steps=["Step 1", "Step 2"],
            compliance_frameworks=["SOC2", "ISO27001"],
        )

        self.assertEqual(procedure.procedure_id, "SEC-001")
        self.assertEqual(len(procedure.affected_systems), 2)

    def test_procedure_to_dict(self) -> None:
        """Test converting procedure to dictionary."""
        procedure = SecurityProcedure(
            procedure_id="SEC-001",
            title="Access control",
            description="Implement access controls",
            severity=Severity.HIGH,
            affected_systems=["web_server"],
            steps=["Step 1"],
            compliance_frameworks=["SOC2"],
        )

        proc_dict = procedure.to_dict()

        self.assertEqual(proc_dict["procedure_id"], "SEC-001")
        self.assertEqual(proc_dict["severity"], "high")


class TestTroubleshootingGuide(unittest.TestCase):
    """Tests for troubleshooting guides."""

    def test_guide_creation(self) -> None:
        """Test creating troubleshooting guide."""
        guide = TroubleshootingGuide(
            guide_id="TG-001",
            title="High memory usage",
            symptom_description="Pod memory usage exceeds limits",
            root_cause="Memory leak in application",
            resolution_steps=["Check logs", "Restart pod"],
            diagnostic_commands=["kubectl logs", "kubectl describe"],
        )

        self.assertEqual(guide.guide_id, "TG-001")
        self.assertEqual(guide.severity, Severity.MEDIUM)

    def test_guide_to_dict(self) -> None:
        """Test converting guide to dictionary."""
        guide = TroubleshootingGuide(
            guide_id="TG-001",
            title="Issue",
            symptom_description="Symptom",
            root_cause="Cause",
            resolution_steps=["Fix"],
            diagnostic_commands=["diagnose"],
        )

        guide_dict = guide.to_dict()

        self.assertEqual(guide_dict["guide_id"], "TG-001")
        self.assertIn("symptom", guide_dict)


class TestPerformanceTuningGuide(unittest.TestCase):
    """Tests for performance tuning guides."""

    def test_guide_creation(self) -> None:
        """Test creating performance guide."""
        guide = PerformanceTuningGuide(
            guide_id="PG-001",
            component="database",
            description="Optimize database",
            parameter_name="max_connections",
            current_value=100,
            recommended_value=500,
            tuning_impact="high",
            prerequisites=["Backup DB"],
            rollback_steps=["Restore setting"],
            monitoring_metrics=["connection_count"],
        )

        self.assertEqual(guide.guide_id, "PG-001")
        self.assertEqual(guide.component, "database")

    def test_guide_to_dict(self) -> None:
        """Test converting guide to dictionary."""
        guide = PerformanceTuningGuide(
            guide_id="PG-001",
            component="database",
            description="Optimize",
            parameter_name="setting",
            current_value=100,
            recommended_value=200,
            tuning_impact="medium",
            prerequisites=[],
            rollback_steps=[],
            monitoring_metrics=[],
        )

        guide_dict = guide.to_dict()

        self.assertEqual(guide_dict["parameter"], "setting")


class TestDisasterRecoveryProcedure(unittest.TestCase):
    """Tests for disaster recovery procedures."""

    def test_dr_procedure_creation(self) -> None:
        """Test creating DR procedure."""
        procedure = DisasterRecoveryProcedure(
            procedure_id="DR-001",
            title="Full system recovery",
            disaster_type="data_center_failure",
            rpo_minutes=60,
            rto_minutes=120,
            affected_systems=["web", "db", "cache"],
            pre_disaster_checklist=["Verify backups", "Test restore"],
            recovery_steps=["Restore DB", "Restore apps"],
            validation_steps=["Health check"],
            communication_plan="Notify stakeholders",
            backup_location="s3://backup-bucket",
        )

        self.assertEqual(procedure.procedure_id, "DR-001")
        self.assertEqual(procedure.rpo_minutes, 60)

    def test_dr_procedure_to_dict(self) -> None:
        """Test converting DR procedure to dictionary."""
        procedure = DisasterRecoveryProcedure(
            procedure_id="DR-001",
            title="Recovery",
            disaster_type="failure",
            rpo_minutes=60,
            rto_minutes=120,
            affected_systems=["system"],
            pre_disaster_checklist=["Check"],
            recovery_steps=["Step"],
            validation_steps=["Validate"],
            communication_plan="Notify",
            backup_location="location",
        )

        proc_dict = procedure.to_dict()

        self.assertEqual(proc_dict["rpo_minutes"], 60)
        self.assertEqual(proc_dict["rto_minutes"], 120)


class TestDocumentationLibrary(unittest.TestCase):
    """Tests for documentation library."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.library = DocumentationLibrary()

    def test_add_adr(self) -> None:
        """Test adding ADR."""
        adr = ArchitectureDecisionRecord(
            adr_id="ADR-001",
            title="Microservices",
            status=DecisionStatus.ACCEPTED,
            context="Scaling",
            decision="Use microservices",
            consequences=["Complexity"],
            alternatives={"Monolith": "Simpler"},
        )

        result = self.library.add_adr(adr)

        self.assertTrue(result)
        self.assertIn("ADR-001", self.library.adrs)

    def test_get_adr(self) -> None:
        """Test retrieving ADR."""
        adr = ArchitectureDecisionRecord(
            adr_id="ADR-001",
            title="Microservices",
            status=DecisionStatus.ACCEPTED,
            context="Scaling",
            decision="Use microservices",
            consequences=["Complexity"],
            alternatives={"Monolith": "Simpler"},
        )

        self.library.add_adr(adr)

        retrieved = self.library.get_adr("ADR-001")

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.adr_id, "ADR-001")

    def test_add_playbook(self) -> None:
        """Test adding playbook."""
        playbook = OperationalPlaybook(
            playbook_id="PB-001",
            title="Deployment",
            playbook_type=PlaybookType.DEPLOYMENT,
            description="Deploy",
            severity=Severity.HIGH,
        )

        result = self.library.add_playbook(playbook)

        self.assertTrue(result)
        self.assertIn("PB-001", self.library.playbooks)

    def test_get_playbooks_by_type(self) -> None:
        """Test getting playbooks by type."""
        pb1 = OperationalPlaybook(
            playbook_id="PB-001",
            title="Deploy",
            playbook_type=PlaybookType.DEPLOYMENT,
            description="Deploy",
            severity=Severity.HIGH,
        )

        pb2 = OperationalPlaybook(
            playbook_id="PB-002",
            title="Incident",
            playbook_type=PlaybookType.INCIDENT_RESPONSE,
            description="Incident",
            severity=Severity.CRITICAL,
        )

        self.library.add_playbook(pb1)
        self.library.add_playbook(pb2)

        deployments = self.library.get_playbooks_by_type(PlaybookType.DEPLOYMENT)

        self.assertEqual(len(deployments), 1)
        self.assertEqual(deployments[0].playbook_id, "PB-001")

    def test_add_security_procedure(self) -> None:
        """Test adding security procedure."""
        procedure = SecurityProcedure(
            procedure_id="SEC-001",
            title="Access control",
            description="Control access",
            severity=Severity.HIGH,
            affected_systems=["web"],
            steps=["Step 1"],
            compliance_frameworks=["SOC2"],
        )

        result = self.library.add_security_procedure(procedure)

        self.assertTrue(result)
        self.assertIn("SEC-001", self.library.security_procedures)

    def test_get_procedures_by_framework(self) -> None:
        """Test getting procedures by framework."""
        proc1 = SecurityProcedure(
            procedure_id="SEC-001",
            title="Access",
            description="Control",
            severity=Severity.HIGH,
            affected_systems=["web"],
            steps=["Step"],
            compliance_frameworks=["SOC2"],
        )

        proc2 = SecurityProcedure(
            procedure_id="SEC-002",
            title="Encryption",
            description="Encrypt",
            severity=Severity.HIGH,
            affected_systems=["db"],
            steps=["Step"],
            compliance_frameworks=["ISO27001", "SOC2"],
        )

        self.library.add_security_procedure(proc1)
        self.library.add_security_procedure(proc2)

        soc2_procs = self.library.get_procedures_by_framework("SOC2")

        self.assertEqual(len(soc2_procs), 2)

    def test_get_documentation_index(self) -> None:
        """Test getting documentation index."""
        adr = ArchitectureDecisionRecord(
            adr_id="ADR-001",
            title="Test",
            status=DecisionStatus.ACCEPTED,
            context="Context",
            decision="Decision",
            consequences=[],
            alternatives={},
        )

        playbook = OperationalPlaybook(
            playbook_id="PB-001",
            title="Test",
            playbook_type=PlaybookType.DEPLOYMENT,
            description="Test",
            severity=Severity.HIGH,
        )

        self.library.add_adr(adr)
        self.library.add_playbook(playbook)

        index = self.library.get_documentation_index()

        self.assertEqual(index["architecture_decisions"], 1)
        self.assertEqual(index["playbooks"], 1)
        self.assertEqual(index["total_documents"], 2)

    def test_export_documentation(self) -> None:
        """Test exporting documentation."""
        adr = ArchitectureDecisionRecord(
            adr_id="ADR-001",
            title="Test",
            status=DecisionStatus.ACCEPTED,
            context="Context",
            decision="Decision",
            consequences=[],
            alternatives={},
        )

        self.library.add_adr(adr)

        export = self.library.export_documentation()

        self.assertIn("adrs", export)
        self.assertEqual(len(export["adrs"]), 1)

    def test_validate_references(self) -> None:
        """Test validating references."""
        adr1 = ArchitectureDecisionRecord(
            adr_id="ADR-001",
            title="Test",
            status=DecisionStatus.ACCEPTED,
            context="Context",
            decision="Decision",
            consequences=[],
            alternatives={},
            related_adrs=["ADR-002"],  # Non-existent
        )

        self.library.add_adr(adr1)

        issues = self.library.validate_references()

        self.assertIn("ADR-001 -> ADR-002", issues["broken_adr_references"])


if __name__ == "__main__":
    unittest.main()
