"""
Test suite for Advanced Diagnostics Framework

Tests for DiagnosticsFramework including:
- CPU diagnostics
- Memory diagnostics
- Disk diagnostics
- Network diagnostics
- Anomaly detection
- Remediation suggestions
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from opt.services.diagnostics import (
    DiagnosticsFramework,
    DiagnosticCheck,
    DiagnosticSeverity,
    CheckStatus,
    DiagnosticIssue,
    CheckResult,
    CPUDiagnostics,
    MemoryDiagnostics,
    DiskDiagnostics,
    NetworkDiagnostics,
)


class TestDiagnosticsFramework(unittest.TestCase):
    """Test DiagnosticsFramework functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.framework = DiagnosticsFramework()

    def test_register_check(self):
        """Test registering diagnostic checks."""
        initial_count = len(self.framework.checks)
        
        custom_check = Mock(spec=DiagnosticCheck)
        custom_check.name = "Custom Check"
        
        self.framework.register_check(custom_check)
        
        self.assertEqual(len(self.framework.checks), initial_count + 1)
        self.assertIn("Custom Check", self.framework.checks)

    def test_default_checks_registered(self):
        """Test that default checks are registered."""
        check_names = {'CPU', 'Memory', 'Disk', 'Network'}
        
        registered_names = set(self.framework.checks.keys())
        
        self.assertTrue(check_names.issubset(registered_names))

    @patch('psutil.cpu_percent', return_value=45.0)
    @patch('psutil.cpu_count', return_value=4)
    @patch('psutil.cpu_freq')
    @patch('psutil.getloadavg', return_value=(1.0, 1.5, 2.0))
    def test_cpu_diagnostics_normal(self, mock_load, mock_freq, mock_count, mock_cpu):
        """Test CPU diagnostics with normal values."""
        mock_freq_obj = Mock()
        mock_freq_obj.current = 2400
        mock_freq.return_value = mock_freq_obj
        
        check = CPUDiagnostics()
        result = check.execute()
        
        self.assertEqual(result.status, CheckStatus.PASSED)
        self.assertEqual(result.check_name, "CPU")
        self.assertIn('cpu_percent', result.metrics)

    @patch('psutil.cpu_percent', return_value=90.0)
    @patch('psutil.cpu_count', return_value=4)
    @patch('psutil.cpu_freq')
    @patch('psutil.getloadavg', return_value=(3.0, 3.0, 3.0))
    def test_cpu_diagnostics_high_usage(self, mock_load, mock_freq, mock_count, mock_cpu):
        """Test CPU diagnostics with high usage."""
        mock_freq_obj = Mock()
        mock_freq_obj.current = 2400
        mock_freq.return_value = mock_freq_obj
        
        check = CPUDiagnostics()
        result = check.execute()
        
        self.assertEqual(result.status, CheckStatus.WARNING)
        self.assertGreater(len(result.issues), 0)
        self.assertEqual(result.issues[0].severity, DiagnosticSeverity.WARNING)

    @patch('psutil.virtual_memory')
    @patch('psutil.swap_memory')
    def test_memory_diagnostics_normal(self, mock_swap, mock_vmem):
        """Test memory diagnostics with normal values."""
        mock_mem_obj = Mock()
        mock_mem_obj.total = 8589934592  # 8GB
        mock_mem_obj.used = 2147483648   # 2GB
        mock_mem_obj.available = 6442450944  # 6GB
        mock_mem_obj.percent = 25
        mock_vmem.return_value = mock_mem_obj
        
        mock_swap_obj = Mock()
        mock_swap_obj.total = 2147483648  # 2GB
        mock_swap_obj.used = 268435456    # 256MB
        mock_swap_obj.percent = 12.5
        mock_swap.return_value = mock_swap_obj
        
        check = MemoryDiagnostics()
        result = check.execute()
        
        self.assertEqual(result.status, CheckStatus.PASSED)
        self.assertEqual(result.check_name, "Memory")
        self.assertIn('percent', result.metrics)

    @patch('psutil.virtual_memory')
    @patch('psutil.swap_memory')
    def test_memory_diagnostics_high_usage(self, mock_swap, mock_vmem):
        """Test memory diagnostics with high usage."""
        mock_mem_obj = Mock()
        mock_mem_obj.total = 8589934592
        mock_mem_obj.used = 7298023008   # ~85%
        mock_mem_obj.available = 1291911584
        mock_mem_obj.percent = 85
        mock_vmem.return_value = mock_mem_obj
        
        mock_swap_obj = Mock()
        mock_swap_obj.total = 2147483648
        mock_swap_obj.used = 1073741824  # 50%
        mock_swap_obj.percent = 50
        mock_swap.return_value = mock_swap_obj
        
        check = MemoryDiagnostics()
        result = check.execute()
        
        self.assertEqual(result.status, CheckStatus.WARNING)
        self.assertGreater(len(result.issues), 0)

    @patch('psutil.disk_usage')
    @patch('psutil.disk_io_counters')
    def test_disk_diagnostics_normal(self, mock_io, mock_usage):
        """Test disk diagnostics with normal values."""
        mock_disk_obj = Mock()
        mock_disk_obj.total = 1099511627776  # 1TB
        mock_disk_obj.used = 219902325555    # 20%
        mock_disk_obj.free = 879609302221
        mock_disk_obj.percent = 20
        mock_usage.return_value = mock_disk_obj
        
        mock_io_obj = Mock()
        mock_io_obj.read_bytes = 1000000000
        mock_io_obj.write_bytes = 500000000
        mock_io_obj.read_count = 10000
        mock_io_obj.write_count = 5000
        mock_io.return_value = mock_io_obj
        
        check = DiskDiagnostics()
        result = check.execute()
        
        self.assertEqual(result.status, CheckStatus.PASSED)
        self.assertIn('percent', result.metrics)

    @patch('psutil.disk_usage')
    @patch('psutil.disk_io_counters')
    def test_disk_diagnostics_critical(self, mock_io, mock_usage):
        """Test disk diagnostics with critical space usage."""
        mock_disk_obj = Mock()
        mock_disk_obj.total = 1099511627776
        mock_disk_obj.used = 1044482717696  # ~95%
        mock_disk_obj.free = 55028910080
        mock_disk_obj.percent = 95
        mock_usage.return_value = mock_disk_obj
        
        mock_io_obj = Mock()
        mock_io_obj.read_bytes = 1000000000
        mock_io_obj.write_bytes = 500000000
        mock_io_obj.read_count = 10000
        mock_io_obj.write_count = 5000
        mock_io.return_value = mock_io_obj
        
        check = DiskDiagnostics()
        result = check.execute()
        
        self.assertEqual(result.status, CheckStatus.FAILED)
        critical_issues = [i for i in result.issues if i.severity == DiagnosticSeverity.CRITICAL]
        self.assertGreater(len(critical_issues), 0)

    def test_run_diagnostics(self):
        """Test running all diagnostics."""
        report = self.framework.run_diagnostics()
        
        self.assertIsNotNone(report)
        self.assertGreater(len(report.checks), 0)
        self.assertGreaterEqual(report.overall_health_score, 0)
        self.assertLessEqual(report.overall_health_score, 100)

    def test_diagnostics_history(self):
        """Test diagnostics history tracking."""
        initial_count = len(self.framework.history)
        
        self.framework.run_diagnostics()
        self.framework.run_diagnostics()
        
        self.assertEqual(len(self.framework.history), initial_count + 2)

    def test_get_remediation_suggestions(self):
        """Test remediation suggestion retrieval."""
        report = self.framework.run_diagnostics()
        
        suggestions = self.framework.get_remediation_suggestions(report)
        
        self.assertIsInstance(suggestions, list)
        # Suggestions will be non-empty if there are issues
        if report.issues_found > 0:
            self.assertGreater(len(suggestions), 0)

    def test_get_health_trend(self):
        """Test health trend retrieval."""
        # Run multiple diagnostics
        for _ in range(3):
            self.framework.run_diagnostics()
        
        trend = self.framework.get_health_trend(hours=24)
        
        self.assertIsInstance(trend, list)
        self.assertGreater(len(trend), 0)
        for entry in trend:
            self.assertIn('timestamp', entry)
            self.assertIn('health_score', entry)
            self.assertIn('issues', entry)

    def test_get_diagnostics_summary(self):
        """Test diagnostics summary generation."""
        self.framework.run_diagnostics()
        
        summary = self.framework.get_diagnostics_summary()
        
        self.assertIn('last_run', summary)
        self.assertIn('overall_health', summary)
        self.assertIn('checks_registered', summary)
        self.assertIn('reports_generated', summary)
        self.assertIn('check_details', summary)


class TestDiagnosticIssue(unittest.TestCase):
    """Test DiagnosticIssue dataclass."""
    
    def test_issue_creation(self):
        """Test creating diagnostic issues."""
        issue = DiagnosticIssue(
            check_name="Test",
            severity=DiagnosticSeverity.WARNING,
            message="Test issue",
            remediation="Fix it"
        )
        
        self.assertEqual(issue.check_name, "Test")
        self.assertEqual(issue.severity, DiagnosticSeverity.WARNING)
        self.assertIsNotNone(issue.timestamp)


class TestCheckResult(unittest.TestCase):
    """Test CheckResult dataclass."""
    
    def test_check_result_with_issues(self):
        """Test check result with issues."""
        issue = DiagnosticIssue(
            check_name="Test",
            severity=DiagnosticSeverity.ERROR,
            message="Test error"
        )
        
        result = CheckResult(
            check_name="Test Check",
            status=CheckStatus.FAILED,
            duration_ms=100.5,
            message="Check failed",
            issues=[issue]
        )
        
        self.assertEqual(result.status, CheckStatus.FAILED)
        self.assertEqual(len(result.issues), 1)


if __name__ == '__main__':
    unittest.main()

