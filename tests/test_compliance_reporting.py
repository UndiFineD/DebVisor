from unittest.mock import patch, MagicMock
import unittest
from opt.services.compliance.reporting import ComplianceReporter
from opt.services.compliance.core import ComplianceReport, ComplianceViolation


class TestComplianceReporting(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_engine = MagicMock()
        self.reporter = ComplianceReporter(self.mock_engine)

    @patch('opt.services.compliance.reporting.Node')
    @patch('opt.services.compliance.reporting.User')

    def test_generate_report_markdown(self, mock_user, mock_node):
        # Mock DB
        mock_node.query.all.return_value = []
        mock_user.query.all.return_value = []

        # Mock Engine Result
        self.mock_engine.run_compliance_scan.return_value = ComplianceReport(
            generated_at="2025-01-01T00:00:00",
            total_policies=10,
            total_resources=5,
            violations_count=1,
            compliance_score=90.0,
            violations=[
                ComplianceViolation(
                    policy_id="SEC-001",
                    resource_id="node-1",
                    resource_type="node",
                    timestamp="2025-01-01T00:00:00",
                    details="Root login enabled",
                    severity="critical"
                )
            ]
        )

        report = self.reporter.generate_report("rep-001", format="markdown")

        self.assertIn("    # Compliance Report", report.content)
        self.assertIn("Score:** 90.0%", report.content)
        self.assertIn("SEC-001", report.content)
        self.assertIn("Root login enabled", report.content)

    @patch('opt.services.compliance.reporting.Node')
    @patch('opt.services.compliance.reporting.User')

    def test_generate_report_html_fallback(self, mock_user, mock_node):
        # Mock DB
        mock_node.query.all.return_value = []
        mock_user.query.all.return_value = []

        self.mock_engine.run_compliance_scan.return_value = ComplianceReport(
            generated_at="2025-01-01T00:00:00",
            total_policies=10,
            total_resources=5,
            violations_count=0,
            compliance_score=100.0,
            _violations = []
        )

        # Request PDF, expect HTML fallback (warning logged)
        report = self.reporter.generate_report("rep-002", format="pd")

        self.assertIn("<html>", report.content)
        self.assertIn("Score:</strong> 100.0%", report.content)
