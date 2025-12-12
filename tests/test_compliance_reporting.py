from unittest.mock import patch
import unittest
from unittest.mock import MagicMock, patch
from opt.services.compliance.reporting import ComplianceReporter
from opt.services.compliance.core import ComplianceReport, ComplianceViolation


from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime


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
            _generated_at = "2025-01-01T00:00:00",
            _total_policies = 10,
            _total_resources = 5,
            _violations_count = 1,
            _compliance_score = 90.0,
            _violations = [
                ComplianceViolation(
                    _policy_id = "SEC-001",
                    _resource_id = "node-1",
                    _resource_type = "node",
                    _timestamp = "2025-01-01T00:00:00",
                    _details = "Root login enabled",
                    _severity = "critical"
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
            _generated_at = "2025-01-01T00:00:00",
            _total_policies = 10,
            _total_resources = 5,
            _violations_count = 0,
            _compliance_score = 100.0,
            _violations = []
        )

        # Request PDF, expect HTML fallback (warning logged)
        report = self.reporter.generate_report("rep-002", format="pd")

        self.assertIn("<html>", report.content)
        self.assertIn("Score:</strong> 100.0%", report.content)
