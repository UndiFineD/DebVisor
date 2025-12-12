# !/usr/bin/env python3
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
            _title = "Use microservices architecture",
            status=DecisionStatus.ACCEPTED,
            _context = "Need scalable system",
            _decision = "Implement microservices",
            _consequences = ["Increased complexity", "Better scalability"],
            _alternatives = {"Monolith": "Simpler but less scalable"},
        )

        self.assertEqual(adr.adr_id, "ADR-001")
        self.assertEqual(adr.status, DecisionStatus.ACCEPTED)

    def test_adr_to_dict(self) -> None:
        """Test ADR conversion to dictionary."""
        adr = ArchitectureDecisionRecord(
            _adr_id = "ADR-001",
            _title = "Use microservices",
            _status = DecisionStatus.ACCEPTED,
            _context = "Scaling requirement",
            _decision = "Microservices",
            _consequences = ["Increased complexity"],
            _alternatives = {"Monolith": "Simpler"},
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
            _title = "Verify prerequisites",
            _description = "Ensure all prerequisites are met",
            commands=["docker --version", "kubectl version"],
        )

        self.assertEqual(step.step_number, 1)
        self.assertEqual(len(step.commands), 2)
        self.assertFalse(step.critical)

    def test_critical_step(self) -> None:
        """Test marking step as critical."""
        step = PlaybookStep(
            _step_number = 1,
            _title = "Backup data",
            _description = "Backup all critical data",
            critical=True,
        )

        self.assertTrue(step.critical)

    def test_step_to_dict(self) -> None:
        """Test step conversion to dictionary."""
        step = PlaybookStep(
            step_number=1,
            title="Verify",
            _description = "Verification step",
            _commands = ["echo test"],
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
            _title = "Deployment procedure",
            playbook_type=PlaybookType.DEPLOYMENT,
            _description = "Standard deployment steps",
            _severity = Severity.HIGH,
        )

        self.assertEqual(playbook.playbook_id, "PB-001")
        self.assertEqual(playbook.playbook_type, PlaybookType.DEPLOYMENT)

    def test_add_step(self) -> None:
        """Test adding step to playbook."""
        playbook = OperationalPlaybook(
            _playbook_id = "PB-001",
            title="Deployment",
            _playbook_type = PlaybookType.DEPLOYMENT,
            description="Deploy",
            _severity = Severity.HIGH,
        )

        step = PlaybookStep(step_number=1, title="Verify", description="Verification")

        playbook.add_step(step)

        self.assertEqual(len(playbook.steps), 1)

    def test_total_duration(self) -> None:
        """Test calculating total duration."""
        playbook = OperationalPlaybook(
            _playbook_id = "PB-001",
            title="Deployment",
            _playbook_type = PlaybookType.DEPLOYMENT,
            description="Deploy",
            _severity = Severity.HIGH,
        )

        _step1 = PlaybookStep(
            step_number=1,
            title="Step 1",
            description="First",
            estimated_duration_seconds=60,
        )

        step2 = PlaybookStep(
            _step_number = 2,
            _title = "Step 2",
            _description = "Second",
            _estimated_duration_seconds = 120,
        )

        playbook.add_step(step1)
        playbook.add_step(step2)

        duration = playbook.total_duration_minutes()

        self.assertAlmostEqual(duration, 3.0, places=1)

    def test_get_critical_steps(self) -> None:
        """Test getting critical steps."""
        playbook = OperationalPlaybook(
            _playbook_id = "PB-001",
            title="Deployment",
            _playbook_type = PlaybookType.DEPLOYMENT,
            description="Deploy",
            _severity = Severity.HIGH,
        )

        step1 = PlaybookStep(
            step_number=1, title="Backup", description="Backup data", critical=True
        )

        step2 = PlaybookStep(
            _step_number = 2, title="Deploy", description="Deploy app", critical=False
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
            _title = "Access control",
            _description = "Implement access controls",
            _severity = Severity.CRITICAL,
            affected_systems=["web_server", "database"],
            _steps = ["Step 1", "Step 2"],
            _compliance_frameworks = ["SOC2", "ISO27001"],
        )

        self.assertEqual(procedure.procedure_id, "SEC-001")
        self.assertEqual(len(procedure.affected_systems), 2)

    def test_procedure_to_dict(self) -> None:
        """Test converting procedure to dictionary."""
        procedure = SecurityProcedure(
            _procedure_id = "SEC-001",
            _title = "Access control",
            _description = "Implement access controls",
            severity=Severity.HIGH,
            _affected_systems = ["web_server"],
            _steps = ["Step 1"],
            _compliance_frameworks = ["SOC2"],
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
            _title = "High memory usage",
            _symptom_description = "Pod memory usage exceeds limits",
            _root_cause = "Memory leak in application",
            _resolution_steps = ["Check logs", "Restart pod"],
            _diagnostic_commands = ["kubectl logs", "kubectl describe"],
        )

        self.assertEqual(guide.guide_id, "TG-001")
        self.assertEqual(guide.severity, Severity.MEDIUM)

    def test_guide_to_dict(self) -> None:
        """Test converting guide to dictionary."""
        guide = TroubleshootingGuide(
            _guide_id = "TG-001",
            _title = "Issue",
            _symptom_description = "Symptom",
            _root_cause = "Cause",
            _resolution_steps = ["Fix"],
            _diagnostic_commands = ["diagnose"],
        )

        guide_dict = guide.to_dict()

        self.assertEqual(guide_dict["guide_id"], "TG-001")
        self.assertIn("symptom", guide_dict)


class TestPerformanceTuningGuide(unittest.TestCase):
    """Tests for performance tuning guides."""

    def test_guide_creation(self) -> None:
        """Test creating performance guide."""
        guide = PerformanceTuningGuide(
            _guide_id = "PG-001",
            _component = "database",
            _description = "Optimize database",
            _parameter_name = "max_connections",
            _current_value = 100,
            _recommended_value = 500,
            _tuning_impact = "high",
            _prerequisites = ["Backup DB"],
            _rollback_steps = ["Restore setting"],
            _monitoring_metrics = ["connection_count"],
        )

        self.assertEqual(guide.guide_id, "PG-001")
        self.assertEqual(guide.component, "database")

    def test_guide_to_dict(self) -> None:
        """Test converting guide to dictionary."""
        guide = PerformanceTuningGuide(
            _guide_id = "PG-001",
            _component = "database",
            _description = "Optimize",
            _parameter_name = "setting",
            _current_value = 100,
            _recommended_value = 200,
            _tuning_impact = "medium",
            _prerequisites = [],
            _rollback_steps = [],
            _monitoring_metrics = [],
        )

        guide_dict = guide.to_dict()

        self.assertEqual(guide_dict["parameter"], "setting")


class TestDisasterRecoveryProcedure(unittest.TestCase):
    """Tests for disaster recovery procedures."""

    def test_dr_procedure_creation(self) -> None:
        """Test creating DR procedure."""
        procedure = DisasterRecoveryProcedure(
            _procedure_id = "DR-001",
            _title = "Full system recovery",
            _disaster_type = "data_center_failure",
            _rpo_minutes = 60,
            _rto_minutes = 120,
            _affected_systems = ["web", "db", "cache"],
            _pre_disaster_checklist = ["Verify backups", "Test restore"],
            _recovery_steps = ["Restore DB", "Restore apps"],
            _validation_steps = ["Health check"],
            _communication_plan = "Notify stakeholders",
            _backup_location = "s3://backup-bucket",
        )

        self.assertEqual(procedure.procedure_id, "DR-001")
        self.assertEqual(procedure.rpo_minutes, 60)

    def test_dr_procedure_to_dict(self) -> None:
        """Test converting DR procedure to dictionary."""
        procedure = DisasterRecoveryProcedure(
            _procedure_id = "DR-001",
            _title = "Recovery",
            _disaster_type = "failure",
            _rpo_minutes = 60,
            _rto_minutes = 120,
            _affected_systems = ["system"],
            _pre_disaster_checklist = ["Check"],
            _recovery_steps = ["Step"],
            _validation_steps = ["Validate"],
            _communication_plan = "Notify",
            _backup_location = "location",
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
            _adr_id = "ADR-001",
            _title = "Microservices",
            _status = DecisionStatus.ACCEPTED,
            _context = "Scaling",
            _decision = "Use microservices",
            _consequences = ["Complexity"],
            _alternatives = {"Monolith": "Simpler"},
        )

        result = self.library.add_adr(adr)

        self.assertTrue(result)
        self.assertIn("ADR-001", self.library.adrs)

    def test_get_adr(self) -> None:
        """Test retrieving ADR."""
        adr = ArchitectureDecisionRecord(
            _adr_id = "ADR-001",
            _title = "Microservices",
            _status = DecisionStatus.ACCEPTED,
            _context = "Scaling",
            _decision = "Use microservices",
            _consequences = ["Complexity"],
            _alternatives = {"Monolith": "Simpler"},
        )

        self.library.add_adr(adr)

        retrieved = self.library.get_adr("ADR-001")

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.adr_id, "ADR-001")

    def test_add_playbook(self) -> None:
        """Test adding playbook."""
        playbook = OperationalPlaybook(
            _playbook_id = "PB-001",
            _title = "Deployment",
            _playbook_type = PlaybookType.DEPLOYMENT,
            _description = "Deploy",
            _severity = Severity.HIGH,
        )

        result = self.library.add_playbook(playbook)

        self.assertTrue(result)
        self.assertIn("PB-001", self.library.playbooks)

    def test_get_playbooks_by_type(self) -> None:
        """Test getting playbooks by type."""
        _pb1 = OperationalPlaybook(
            playbook_id="PB-001",
            title="Deploy",
            playbook_type=PlaybookType.DEPLOYMENT,
            description="Deploy",
            severity=Severity.HIGH,
        )

        pb2 = OperationalPlaybook(
            _playbook_id = "PB-002",
            _title = "Incident",
            _playbook_type = PlaybookType.INCIDENT_RESPONSE,
            _description = "Incident",
            _severity = Severity.CRITICAL,
        )

        self.library.add_playbook(pb1)
        self.library.add_playbook(pb2)

        deployments = self.library.get_playbooks_by_type(PlaybookType.DEPLOYMENT)

        self.assertEqual(len(deployments), 1)
        self.assertEqual(deployments[0].playbook_id, "PB-001")

    def test_add_security_procedure(self) -> None:
        """Test adding security procedure."""
        procedure = SecurityProcedure(
            _procedure_id = "SEC-001",
            _title = "Access control",
            _description = "Control access",
            _severity = Severity.HIGH,
            _affected_systems = ["web"],
            _steps = ["Step 1"],
            _compliance_frameworks = ["SOC2"],
        )

        result = self.library.add_security_procedure(procedure)

        self.assertTrue(result)
        self.assertIn("SEC-001", self.library.security_procedures)

    def test_get_procedures_by_framework(self) -> None:
        """Test getting procedures by framework."""
        _proc1 = SecurityProcedure(
            _procedure_id = "SEC-001",
            _title = "Access",
            _description = "Control",
            _severity = Severity.HIGH,
            _affected_systems = ["web"],
            _steps = ["Step"],
            _compliance_frameworks = ["SOC2"],
        )

        _proc2 = SecurityProcedure(
            _procedure_id = "SEC-002",
            _title = "Encryption",
            _description = "Encrypt",
            _severity = Severity.HIGH,
            _affected_systems = ["db"],
            _steps = ["Step"],
            _compliance_frameworks = ["ISO27001", "SOC2"],
        )

        self.library.add_security_procedure(proc1)
        self.library.add_security_procedure(proc2)

        soc2_procs = self.library.get_procedures_by_framework("SOC2")

        self.assertEqual(len(soc2_procs), 2)

    def test_get_documentation_index(self) -> None:
        """Test getting documentation index."""
        adr = ArchitectureDecisionRecord(
            _adr_id = "ADR-001",
            _title = "Test",
            _status = DecisionStatus.ACCEPTED,
            _context = "Context",
            _decision = "Decision",
            _consequences = [],
            _alternatives = {},
        )

        playbook = OperationalPlaybook(
            _playbook_id = "PB-001",
            _title = "Test",
            _playbook_type = PlaybookType.DEPLOYMENT,
            _description = "Test",
            _severity = Severity.HIGH,
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
            _adr_id = "ADR-001",
            _title = "Test",
            _status = DecisionStatus.ACCEPTED,
            _context = "Context",
            _decision = "Decision",
            _consequences = [],
            _alternatives = {},
        )

        self.library.add_adr(adr)

        export = self.library.export_documentation()

        self.assertIn("adrs", export)
        self.assertEqual(len(export["adrs"]), 1)

    def test_validate_references(self) -> None:
        """Test validating references."""
        _adr1 = ArchitectureDecisionRecord(
            _adr_id = "ADR-001",
            _title = "Test",
            _status = DecisionStatus.ACCEPTED,
            _context = "Context",
            _decision = "Decision",
            _consequences = [],
            _alternatives = {},
            _related_adrs = ["ADR-002"],    # Non-existent
        )

        self.library.add_adr(adr1)

        issues = self.library.validate_references()

        self.assertIn("ADR-001 -> ADR-002", issues["broken_adr_references"])


if __name__ == "__main__":
    unittest.main()
