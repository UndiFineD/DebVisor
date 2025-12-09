#!/usr/bin/env python3
"""
Unit tests for security testing framework.

Tests for:
- OWASP Top 10 checks
- Dependency vulnerability scanning
- Container security scanning
- Security report generation
"""

import unittest


from security_testing import (
    SecurityTestingFramework,
    OWASPTop10Checker,
    DependencyVulnerabilityChecker,
    ContainerSecurityChecker,
    VulnerabilitySeverity,
    SecurityCheckType,
    ComplianceFramework,
)


class TestOWASPTop10Checker(unittest.TestCase):
    """Tests for OWASP Top 10 checker."""

    def test_check_input_validation_missing(self) -> None:
        """Test detecting missing input validation."""
        code = "user_input = request.args.get('name')\nprint(user_input)"

        result = OWASPTop10Checker.check_input_validation(code)

        self.assertFalse(result.passed)
        self.assertGreater(len(result.vulnerabilities), 0)

    def test_check_input_validation_present(self) -> None:
        """Test detecting valid input validation."""
        code = """
user_input = request.args.get('name')
user_input = user_input.strip()
validate_input(user_input)
"""

        result = OWASPTop10Checker.check_input_validation(code)

        self.assertTrue(result.passed)

    def test_check_sql_injection_vulnerable(self) -> None:
        """Test detecting SQL injection vulnerability."""
        code = 'query = f"SELECT * FROM users WHERE id = {user_id}"'

        result = OWASPTop10Checker.check_sql_injection(code)

        self.assertFalse(result.passed)
        self.assertGreater(len(result.vulnerabilities), 0)
        self.assertEqual(
            result.vulnerabilities[0].severity, VulnerabilitySeverity.CRITICAL
        )

    def test_check_sql_injection_safe(self) -> None:
        """Test detecting safe SQL queries."""
        code = "query = 'SELECT * FROM users WHERE id = ?'"

        result = OWASPTop10Checker.check_sql_injection(code)

        self.assertTrue(result.passed)

    def test_check_xss_vulnerable(self) -> None:
        """Test detecting XSS vulnerability."""
        code = "html = f'<div>{user_input}</div>'"

        result = OWASPTop10Checker.check_xss(code)

        self.assertFalse(result.passed)

    def test_check_xss_safe(self) -> None:
        """Test detecting safe HTML escaping."""
        code = "html = f'<div>{escape(user_input)}</div>'"

        result = OWASPTop10Checker.check_xss(code)

        self.assertTrue(result.passed)

    def test_check_authentication_hardcoded_password(self) -> None:
        """Test detecting hardcoded credentials."""
        code = 'password = "secret123"'

        result = OWASPTop10Checker.check_authentication(code)

        self.assertFalse(result.passed)
        self.assertGreater(len(result.vulnerabilities), 0)
        self.assertEqual(
            result.vulnerabilities[0].severity, VulnerabilitySeverity.CRITICAL
        )

    def test_check_authentication_weak_hashing(self) -> None:
        """Test detecting weak password hashing."""
        code = "hashed = hashlib.md5(password.encode()).hexdigest()"

        result = OWASPTop10Checker.check_authentication(code)

        self.assertFalse(result.passed)

    def test_check_authentication_strong_hashing(self) -> None:
        """Test detecting strong password hashing."""
        code = "hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())"

        result = OWASPTop10Checker.check_authentication(code)

        self.assertTrue(result.passed)

    def test_check_authorization_missing(self) -> None:
        """Test detecting missing authorization."""
        code = "@app.route('/admin')\ndef admin_panel():\n    return 'admin panel'"

        result = OWASPTop10Checker.check_authorization(code)

        self.assertFalse(result.passed)

    def test_check_authorization_present(self) -> None:
        """Test detecting present authorization."""
        code = """
@app.route('/admin')
@require_role('admin')
def admin_panel():
    return 'admin panel'
"""

        result = OWASPTop10Checker.check_authorization(code)

        self.assertTrue(result.passed)

    def test_check_cryptography_weak_algorithm(self) -> None:
        """Test detecting weak encryption."""
        code = "digest = hashlib.md5(data).hexdigest()"

        result = OWASPTop10Checker.check_cryptography(code)

        self.assertFalse(result.passed)

    def test_check_cryptography_weak_random(self) -> None:
        """Test detecting weak random generator."""
        code = "token = random.randint(0, 1000)"

        result = OWASPTop10Checker.check_cryptography(code)

        self.assertFalse(result.passed)

    def test_check_cryptography_secure_random(self) -> None:
        """Test detecting secure random generator."""
        code = "token = secrets.token_hex(32)"

        result = OWASPTop10Checker.check_cryptography(code)

        self.assertTrue(result.passed)


class TestDependencyVulnerabilityChecker(unittest.TestCase):
    """Tests for dependency vulnerability checker."""

    def test_scan_safe_requirements(self) -> None:
        """Test scanning safe requirements."""
        requirements = {"requests": "2.28.0", "django": "4.0.0", "flask": "2.0.0"}

        result = DependencyVulnerabilityChecker.scan_requirements(requirements)

        self.assertTrue(result.passed)
        self.assertEqual(len(result.vulnerabilities), 0)

    def test_scan_vulnerable_requirements(self) -> None:
        """Test scanning vulnerable requirements."""
        requirements = {"requests": "2.0.0", "django": "4.0.0"}

        result = DependencyVulnerabilityChecker.scan_requirements(requirements)

        self.assertFalse(result.passed)
        self.assertGreater(len(result.vulnerabilities), 0)

    def test_scan_multiple_vulnerabilities(self) -> None:
        """Test scanning multiple vulnerabilities."""
        requirements = {"requests": "2.0.0", "django": "1.0.0", "flask": "0.1.0"}

        result = DependencyVulnerabilityChecker.scan_requirements(requirements)

        self.assertFalse(result.passed)
        self.assertGreaterEqual(len(result.vulnerabilities), 3)

    def test_vulnerability_details(self) -> None:
        """Test vulnerability details."""
        requirements = {
            "requests": "2.0.0",
        }

        result = DependencyVulnerabilityChecker.scan_requirements(requirements)

        self.assertEqual(len(result.vulnerabilities), 1)
        vuln = result.vulnerabilities[0]
        self.assertEqual(vuln.type, SecurityCheckType.DEPENDENCY)
        self.assertEqual(vuln.severity, VulnerabilitySeverity.HIGH)


class TestContainerSecurityChecker(unittest.TestCase):
    """Tests for container security checker."""

    def test_scan_dockerfile_root_user(self) -> None:
        """Test detecting root user in container."""
        dockerfile = """
FROM ubuntu:20.04
RUN apt-get update
USER root
"""

        result = ContainerSecurityChecker.scan_dockerfile(dockerfile)

        self.assertFalse(result.passed)
        self.assertGreater(len(result.vulnerabilities), 0)

    def test_scan_dockerfile_no_user(self) -> None:
        """Test detecting missing USER directive."""
        dockerfile = """
FROM ubuntu:20.04
RUN apt-get update
RUN echo 'test'
"""

        result = ContainerSecurityChecker.scan_dockerfile(dockerfile)

        self.assertFalse(result.passed)

    def test_scan_dockerfile_non_root_user(self) -> None:
        """Test detecting non-root user."""
        dockerfile = """
FROM ubuntu:20.04
RUN useradd -m appuser
USER appuser
"""

        result = ContainerSecurityChecker.scan_dockerfile(dockerfile)

        # Should pass for non-root user
        self.assertTrue(result.passed)

    def test_scan_dockerfile_hardcoded_secrets(self) -> None:
        """Test detecting hardcoded secrets."""
        dockerfile = """
FROM ubuntu:20.04
ENV PASSWORD=secret123
ENV API_KEY=xyz789
"""

        result = ContainerSecurityChecker.scan_dockerfile(dockerfile)

        self.assertFalse(result.passed)
        self.assertGreater(len(result.vulnerabilities), 0)
        # Find the secrets vulnerability (CONT-002)
        secrets_vuln = next(
            (v for v in result.vulnerabilities if v.id == "CONT-002"), None
        )
        self.assertIsNotNone(secrets_vuln)
        self.assertEqual(secrets_vuln.severity, VulnerabilitySeverity.CRITICAL)

    def test_scan_dockerfile_latest_base(self) -> None:
        """Test detecting latest base image."""
        dockerfile = """
FROM ubuntu:latest
RUN apt-get update
"""

        result = ContainerSecurityChecker.scan_dockerfile(dockerfile)

        self.assertFalse(result.passed)

    def test_scan_dockerfile_pinned_base(self) -> None:
        """Test detecting pinned base image."""
        dockerfile = """
FROM ubuntu:20.04
RUN apt-get update
USER appuser
"""

        result = ContainerSecurityChecker.scan_dockerfile(dockerfile)

        self.assertTrue(result.passed)


class TestSecurityTestingFramework(unittest.TestCase):
    """Tests for security testing framework."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.framework = SecurityTestingFramework()

    def test_run_owasp_checks(self) -> None:
        """Test running OWASP checks."""
        code = """
user_input = request.args.get('name')
password = "secret123"
"""

        self.framework.run_owasp_checks(code)

        self.assertGreater(len(self.framework.results), 0)
        self.assertGreater(len(self.framework.vulnerabilities), 0)

    def test_scan_dependencies(self) -> None:
        """Test scanning dependencies."""
        requirements = {"requests": "2.0.0", "django": "4.0.0"}

        self.framework.scan_dependencies(requirements)

        self.assertGreater(len(self.framework.results), 0)

    def test_scan_container(self) -> None:
        """Test scanning container."""
        dockerfile = """
FROM ubuntu:latest
ENV PASSWORD=secret
"""

        self.framework.scan_container(dockerfile)

        self.assertGreater(len(self.framework.results), 0)

    def test_generate_report(self) -> None:
        """Test generating security report."""
        code = 'query = f"SELECT * FROM users WHERE id = {id}"'
        requirements = {"requests": "2.0.0"}
        dockerfile = "FROM ubuntu:latest\nUSER root"

        self.framework.run_owasp_checks(code)
        self.framework.scan_dependencies(requirements)
        self.framework.scan_container(dockerfile)

        report = self.framework.generate_report(ComplianceFramework.OWASP_TOP_10)

        self.assertIsNotNone(report)
        self.assertEqual(report.framework, ComplianceFramework.OWASP_TOP_10)
        self.assertGreater(report.total_checks, 0)
        self.assertGreater(report.failed_checks, 0)

    def test_compliance_score_calculation(self) -> None:
        """Test compliance score calculation."""
        code = 'query = f"SELECT * FROM users WHERE id = {id}"'
        self.framework.run_owasp_checks(code)

        report = self.framework.generate_report(ComplianceFramework.OWASP_TOP_10)

        self.assertGreaterEqual(report.compliance_score, 0)
        self.assertLessEqual(report.compliance_score, 100)

    def test_report_json_serialization(self) -> None:
        """Test report JSON serialization."""
        code = 'password = "secret"'
        self.framework.run_owasp_checks(code)

        report = self.framework.generate_report(ComplianceFramework.OWASP_TOP_10)
        json_str = self.framework.to_json(report)

        self.assertIn('"report_id"', json_str)
        self.assertIn('"compliance_score"', json_str)
        self.assertIn('"vulnerabilities"', json_str)

    def test_vulnerability_severity_critical(self) -> None:
        """Test critical vulnerability detection."""
        code = 'query = f"SELECT * FROM users WHERE id = {id}"'
        self.framework.run_owasp_checks(code)

        report = self.framework.generate_report(ComplianceFramework.OWASP_TOP_10)

        self.assertGreater(report.critical_count, 0)

    def test_vulnerability_severity_distribution(self) -> None:
        """Test vulnerability severity distribution."""
        code = """
password = "secret"
query = f"SELECT * FROM users WHERE id = {id}"
html = f"<div>{user_input}</div>"
"""
        self.framework.run_owasp_checks(code)

        report = self.framework.generate_report(ComplianceFramework.OWASP_TOP_10)

        total_severity = (
            report.critical_count
            + report.high_count
            + report.medium_count
            + report.low_count
        )

        self.assertEqual(total_severity, len(report.vulnerabilities))


class TestSecurityIntegration(unittest.TestCase):
    """Integration tests."""

    def test_complete_security_audit(self) -> None:
        """Test complete security audit flow."""
        framework = SecurityTestingFramework()

        # Test code
        code = """
import hashlib
password = input('Enter password: ')
hashed = hashlib.md5(password.encode()).hexdigest()
query = f"UPDATE users SET password='{hashed}'"
print(f"<div>{query}</div>")
"""

        # Dependencies
        requirements = {"requests": "2.0.0"}

        # Container
        dockerfile = """
FROM ubuntu:latest
USER root
ENV API_KEY=secret123
"""

        framework.run_owasp_checks(code)
        framework.scan_dependencies(requirements)
        framework.scan_container(dockerfile)

        report = framework.generate_report(ComplianceFramework.OWASP_TOP_10)

        self.assertGreater(report.total_checks, 3)
        self.assertGreater(report.failed_checks, 0)
        self.assertGreater(report.critical_count, 0)
        self.assertLess(report.compliance_score, 100)


if __name__ == "__main__":
    unittest.main()
