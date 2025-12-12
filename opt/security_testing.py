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

# !/usr/bin/env python3


"""
Security Testing Framework.

Comprehensive security testing including:
- OWASP Top 10 vulnerability checks
- Container image security scanning
- Dependency vulnerability scanning
- Automated security reporting
- Security compliance verification
"""

from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import logging


_logger=logging.getLogger(__name__)


class VulnerabilitySeverity(Enum):
    """Severity levels for vulnerabilities."""

    CRITICAL="critical"
    HIGH="high"
    MEDIUM="medium"
    LOW="low"
    INFO="info"


class ComplianceFramework(Enum):
    """Security compliance frameworks."""

    OWASP_TOP_10="owasp_top_10"
    CWE_TOP_25="cwe_top_25"
    PCI_DSS="pci_dss"
    HIPAA="hipaa"
    SOC2="soc2"


class SecurityCheckType(Enum):
    """Types of security checks."""

    INPUT_VALIDATION="input_validation"
    SQL_INJECTION="sql_injection"
    XSS="xss"
    CSRF="csrf"
    AUTHENTICATION="authentication"
    AUTHORIZATION="authorization"
    CRYPTOGRAPHY="cryptography"
    DEPENDENCY="dependency"
    CONTAINER="container"
    CONFIGURATION="configuration"


@dataclass
class Vulnerability:
    """Vulnerability finding."""

    id: str
    severity: VulnerabilitySeverity
    type: SecurityCheckType
    title: str
    description: str
    affected_component: str
    remediation: str
    cve: Optional[str] = None
    cwe: Optional[str] = None
    discovered_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class SecurityCheckResult:
    """Result of a single security check."""

    check_type: SecurityCheckType
    passed: bool
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime=field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class SecurityReport:
    """Complete security report."""

    report_id: str
    framework: ComplianceFramework
    total_checks: int
    passed_checks: int
    failed_checks: int
    vulnerabilities: List[Vulnerability]
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    compliance_score: float
    generated_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "report_id": self.report_id,
            "framework": self.framework.value,
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "vulnerability_count": len(self.vulnerabilities),
            "critical": self.critical_count,
            "high": self.high_count,
            "medium": self.medium_count,
            "low": self.low_count,
            "compliance_score": f"{self.compliance_score:.1f}%",
            "generated_at": self.generated_at.isoformat(),
        }


class OWASPTop10Checker:
    """OWASP Top 10 security vulnerability checker."""

    CHECKS=[
        ("A01:2021 - Broken Access Control", "authorization"),
        ("A02:2021 - Cryptographic Failures", "cryptography"),
        ("A03:2021 - Injection", "sql_injection"),
        ("A04:2021 - Insecure Design", "configuration"),
        ("A05:2021 - Security Misconfiguration", "configuration"),
        ("A06:2021 - Vulnerable and Outdated Components", "dependency"),
        ("A07:2021 - Authentication Failures", "authentication"),
        ("A08:2021 - Software and Data Integrity Failures", "configuration"),
        ("A09:2021 - Logging and Monitoring Failures", "configuration"),
        ("A10:2021 - SSRF", "xss"),
    ]

    @staticmethod
    def check_input_validation(code: str) -> SecurityCheckResult:
        """Check for proper input validation."""
        passed=True
        vulnerabilities=[]

        # Check for common input validation patterns
        if "strip()" not in code and "validate" not in code.lower():
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="INP-001",
                    _severity=VulnerabilitySeverity.MEDIUM,
                    _type=SecurityCheckType.INPUT_VALIDATION,
                    _title="Missing Input Validation",
                    _description="User input not properly validated",
                    _affected_component="input_handlers",
                    _remediation="Implement input validation for all user inputs",
                    _cwe="CWE-20",
                )
            )

        return SecurityCheckResult(  # type: ignore[call-arg]
            _check_type=SecurityCheckType.INPUT_VALIDATION,
            _passed=passed,
            _vulnerabilities=vulnerabilities,
            _details={"validation_patterns": "strip, validate"},
        )

    @staticmethod
    def check_sql_injection(code: str) -> SecurityCheckResult:
        """Check for SQL injection vulnerabilities."""
        passed=True
        vulnerabilities=[]

        # Check for parameterized queries
        if ".format(" in code or '"' in code and "SELECT" in code:
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="SQL-001",
                    _severity=VulnerabilitySeverity.CRITICAL,
                    _type=SecurityCheckType.SQL_INJECTION,
                    _title="Potential SQL Injection",
                    _description="String formatting used with SQL queries",
                    _affected_component="database_layer",
                    _remediation="Use parameterized queries instead of string formatting",
                    _cwe="CWE-89",
                )
            )

        return SecurityCheckResult(  # type: ignore[call-arg]
            _check_type=SecurityCheckType.SQL_INJECTION,
            _passed=passed,
            _vulnerabilities=vulnerabilities,
            _details={"parameterized": "query_params" in code},
        )

    @staticmethod
    def check_xss(code: str) -> SecurityCheckResult:
        """Check for XSS vulnerabilities."""
        passed=True
        vulnerabilities=[]

        # Check for HTML escaping
        if (
            "<" in code
            and "escape" not in code.lower()
            and "encode" not in code.lower()
        ):
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="XSS-001",
                    _severity=VulnerabilitySeverity.HIGH,
                    _type=SecurityCheckType.XSS,
                    _title="Potential XSS Vulnerability",
                    _description="User input may not be properly escaped",
                    _affected_component="template_rendering",
                    _remediation="Escape HTML special characters in user input",
                    _cwe="CWE-79",
                )
            )

        return SecurityCheckResult(  # type: ignore[call-arg]
            _check_type=SecurityCheckType.XSS,
            _passed=passed,
            _vulnerabilities=vulnerabilities,
            _details={"escaping": "html_escape" in code},
        )

    @staticmethod
    def check_authentication(code: str) -> SecurityCheckResult:
        """Check authentication mechanisms."""
        passed=True
        vulnerabilities=[]

        # Check for hardcoded credentials (look for assignment of literal strings)
        # Pattern: password = "..." or PASSWORD = "..." or api_key = "..." etc.
        import re

        _hardcoded_pattern=r'(password|api_key|secret|token)\s*=\s*["\']'
        if re.search(hardcoded_pattern, code, re.IGNORECASE):  # type: ignore[name-defined]
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="AUTH-001",
                    _severity=VulnerabilitySeverity.CRITICAL,
                    _type=SecurityCheckType.AUTHENTICATION,
                    _title="Hardcoded Credentials",
                    _description="Credentials may be hardcoded in source",
                    _affected_component="authentication",
                    _remediation="Use environment variables or secure vaults",
                    _cwe="CWE-798",
                )
            )

        # Check for password hashing
        weak_hashes=["md5", "sha1", "sha256"]    # These are too fast for passwords
        _has_weak_hash=any(weak in code.lower() for weak in weak_hashes)
        has_strong_hash=(
            "bcrypt" in code or "argon2" in code or "pbkdf2" in code.lower()
        )

        if has_weak_hash and not has_strong_hash:  # type: ignore[name-defined]
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="AUTH-002",
                    _severity=VulnerabilitySeverity.HIGH,
                    _type=SecurityCheckType.AUTHENTICATION,
                    _title="Weak Password Hashing",
                    _description="Password hashing using weak algorithms (MD5/SHA)",
                    _affected_component="authentication",
                    _remediation="Use bcrypt, argon2, or PBKDF2",
                    _cwe="CWE-916",
                )
            )
        elif (
            not has_strong_hash
            and "password" in code.lower()
            and "hash" in code.lower()
        ):
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="AUTH-002",
                    _severity=VulnerabilitySeverity.HIGH,
                    _type=SecurityCheckType.AUTHENTICATION,
                    _title="Weak Password Hashing",
                    _description="Password hashing not using strong algorithms",
                    _affected_component="authentication",
                    _remediation="Use bcrypt, argon2, or PBKDF2",
                    _cwe="CWE-916",
                )
            )

        return SecurityCheckResult(  # type: ignore[call-arg]
            _check_type=SecurityCheckType.AUTHENTICATION,
            _passed=passed,
            _vulnerabilities=vulnerabilities,
            _details={"hashing": "bcrypt" in code or "argon2" in code},
        )

    @staticmethod
    def check_authorization(code: str) -> SecurityCheckResult:
        """Check authorization mechanisms."""
        passed=True
        vulnerabilities=[]

        # Check for permission checks
        if "permission" not in code.lower() and "role" not in code.lower():
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="AUTHZ-001",
                    _severity=VulnerabilitySeverity.HIGH,
                    _type=SecurityCheckType.AUTHORIZATION,
                    _title="Missing Authorization Checks",
                    _description="No authorization checks found",
                    _affected_component="authorization_layer",
                    _remediation="Implement role-based access control (RBAC)",
                    _cwe="CWE-862",
                )
            )

        return SecurityCheckResult(  # type: ignore[call-arg]
            _check_type=SecurityCheckType.AUTHORIZATION,
            _passed=passed,
            _vulnerabilities=vulnerabilities,
            _details={"rbac": "role" in code.lower()},
        )

    @staticmethod
    def check_cryptography(code: str) -> SecurityCheckResult:
        """Check cryptographic practices."""
        passed=True
        vulnerabilities=[]

        # Check for weak encryption
        if "md5" in code.lower() or "sha1" in code.lower():
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="CRYPT-001",
                    _severity=VulnerabilitySeverity.HIGH,
                    _type=SecurityCheckType.CRYPTOGRAPHY,
                    _title="Weak Encryption Algorithm",
                    _description="MD5 or SHA1 used for hashing",
                    _affected_component="cryptography",
                    _remediation="Use SHA-256 or stronger algorithms",
                    _cwe="CWE-327",
                )
            )

        # Check for secure random
        if "random" in code.lower() and "secrets" not in code:
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="CRYPT-002",
                    _severity=VulnerabilitySeverity.MEDIUM,
                    _type=SecurityCheckType.CRYPTOGRAPHY,
                    _title="Weak Random Generator",
                    _description="Using random instead of secrets module",
                    _affected_component="cryptography",
                    _remediation="Use secrets module for cryptographic randomness",
                    _cwe="CWE-338",
                )
            )

        return SecurityCheckResult(  # type: ignore[call-arg]
            _check_type=SecurityCheckType.CRYPTOGRAPHY,
            _passed=passed,
            _vulnerabilities=vulnerabilities,
            _details={
                "weak_algorithms": "md5" in code.lower() or "sha1" in code.lower(),
                "secure_random": "secrets" in code,
            },
        )


class DependencyVulnerabilityChecker:
    """Check for vulnerable dependencies."""

    VULNERABLE_PACKAGES={
        "requests": ["2.0.0", "2.1.0"],    # Example vulnerable versions
        "django": ["1.0.0", "1.1.0"],
        "flask": ["0.1.0", "0.2.0"],
    }

    @staticmethod
    def scan_requirements(requirements: Dict[str, str]) -> SecurityCheckResult:
        """Scan requirements for vulnerabilities."""
        _vulnerabilities=[]  # type: ignore[var-annotated]
        passed=True

        for package, version in requirements.items():
            if package in DependencyVulnerabilityChecker.VULNERABLE_PACKAGES:
                vulnerable_versions=(
                    DependencyVulnerabilityChecker.VULNERABLE_PACKAGES[package]
                )
                if version in vulnerable_versions:
                    _passed=False
                    vulnerabilities.append(  # type: ignore[name-defined]
                        Vulnerability(  # type: ignore[call-arg]
                            _id=f"DEP-{package.upper()}",
                            _severity=VulnerabilitySeverity.HIGH,
                            _type=SecurityCheckType.DEPENDENCY,
                            _title=f"Vulnerable {package}",
                            _description=f"{package} {version} has known vulnerabilities",
                            _affected_component=f"dependencies/{package}",
                            _remediation=f"Update {package} to latest version",
                            _cve="CVE-XXXX-XXXXX",
                        )
                    )

        return SecurityCheckResult(  # type: ignore[call-arg]
            _check_type=SecurityCheckType.DEPENDENCY,
            _passed=passed,
            _vulnerabilities=vulnerabilities,  # type: ignore[name-defined]
            _details={"scanned_packages": len(requirements)},
        )


class ContainerSecurityChecker:
    """Check container image security."""

    @staticmethod
    def scan_dockerfile(dockerfilecontent: str) -> SecurityCheckResult:
        """Scan Dockerfile for security issues."""
        vulnerabilities=[]
        passed=True

        # Check for running as root
        if "USER root" in dockerfile_content or "USER" not in dockerfile_content:  # type: ignore[name-defined]
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="CONT-001",
                    _severity=VulnerabilitySeverity.MEDIUM,
                    _type=SecurityCheckType.CONTAINER,
                    _title="Container runs as root",
                    _description="Container processes run with root privileges",
                    _affected_component="container_image",
                    _remediation="Create non-root user and use USER directive",
                    _cwe="CWE-250",
                )
            )

        # Check for secrets in Dockerfile
        if "PASSWORD" in dockerfile_content or "API_KEY" in dockerfile_content:  # type: ignore[name-defined]
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="CONT-002",
                    _severity=VulnerabilitySeverity.CRITICAL,
                    _type=SecurityCheckType.CONTAINER,
                    _title="Secrets in Dockerfile",
                    _description="Sensitive data may be exposed in image layers",
                    _affected_component="container_image",
                    _remediation="Use build secrets or environment variables",
                    _cwe="CWE-798",
                )
            )

        # Check for outdated base images
        if (
            "ubuntu:latest" in dockerfile_content  # type: ignore[name-defined]
            or "alpine:latest" in dockerfile_content  # type: ignore[name-defined]
        ):
            _passed=False
            vulnerabilities.append(
                Vulnerability(  # type: ignore[call-arg]
                    _id="CONT-003",
                    _severity=VulnerabilitySeverity.MEDIUM,
                    _type=SecurityCheckType.CONTAINER,
                    _title="Using latest base image",
                    _description="Using 'latest' tag instead of specific version",
                    _affected_component="container_image",
                    _remediation="Pin base image to specific version",
                    _cwe="CWE-1104",
                )
            )

        return SecurityCheckResult(  # type: ignore[call-arg]
            _check_type=SecurityCheckType.CONTAINER,
            _passed=passed,
            _vulnerabilities=vulnerabilities,
            _details={
                "runs_as_root": "USER root" in dockerfile_content,  # type: ignore[name-defined]
                "has_secrets": "PASSWORD" in dockerfile_content,  # type: ignore[name-defined]
                "uses_latest": "latest" in dockerfile_content,  # type: ignore[name-defined]
            },
        )


class SecurityTestingFramework:
    """Main security testing framework."""

    def __init__(self) -> None:
        """Initialize framework."""
        self.results: List[SecurityCheckResult] = []
        self.vulnerabilities: List[Vulnerability] = []

    def run_owasp_checks(self, code: str) -> None:
        """Run OWASP Top 10 checks."""
        logger.info("Running OWASP Top 10 checks...")  # type: ignore[name-defined]

        checks=[
            OWASPTop10Checker.check_input_validation(code),
            OWASPTop10Checker.check_sql_injection(code),
            OWASPTop10Checker.check_xss(code),
            OWASPTop10Checker.check_authentication(code),
            OWASPTop10Checker.check_authorization(code),
            OWASPTop10Checker.check_cryptography(code),
        ]

        for check in checks:
            self.results.append(check)
            self.vulnerabilities.extend(check.vulnerabilities)

    def scan_dependencies(self, requirements: Dict[str, str]) -> None:
        """Scan dependencies."""
        logger.info("Scanning dependencies...")  # type: ignore[name-defined]

        _check=DependencyVulnerabilityChecker.scan_requirements(requirements)
        self.results.append(check)  # type: ignore[name-defined]
        self.vulnerabilities.extend(check.vulnerabilities)  # type: ignore[name-defined]

    def scan_container(self, dockerfilecontent: str) -> None:
        """Scan container configuration."""
        logger.info("Scanning container configuration...")  # type: ignore[name-defined]

        _check=ContainerSecurityChecker.scan_dockerfile(dockerfile_content)  # type: ignore[name-defined]
        self.results.append(check)  # type: ignore[name-defined]
        self.vulnerabilities.extend(check.vulnerabilities)  # type: ignore[name-defined]

    def generate_report(self, framework: ComplianceFramework) -> SecurityReport:
        """Generate security report."""
        _total=len(self.results)
        _passed=sum(1 for r in self.results if r.passed)
        _failed=total - passed  # type: ignore[name-defined]

        _critical=sum(
            1
            for v in self.vulnerabilities
            if v.severity == VulnerabilitySeverity.CRITICAL
        )
        _high=sum(
            1 for v in self.vulnerabilities if v.severity == VulnerabilitySeverity.HIGH
        )
        _medium=sum(
            1
            for v in self.vulnerabilities
            if v.severity == VulnerabilitySeverity.MEDIUM
        )
        _low=sum(
            1 for v in self.vulnerabilities if v.severity == VulnerabilitySeverity.LOW
        )

        # Calculate compliance score (0-100)
        # Deduct points for vulnerabilities
        score=100.0
        score -= critical * 25  # type: ignore[name-defined]
        score -= high * 15  # type: ignore[name-defined]
        score -= medium * 5  # type: ignore[name-defined]
        score -= low * 1  # type: ignore[name-defined]
        _score=max(0, min(100, score))

        _report_id=f"sec-{datetime.now(timezone.utc).timestamp()}"

        return SecurityReport(  # type: ignore[call-arg]
            _report_id=report_id,  # type: ignore[name-defined]
            _framework=framework,
            _total_checks=total,  # type: ignore[name-defined]
            _passed_checks=passed,  # type: ignore[name-defined]
            _failed_checks=failed,  # type: ignore[name-defined]
            _vulnerabilities=self.vulnerabilities,
            _critical_count=critical,  # type: ignore[name-defined]
            _high_count=high,  # type: ignore[name-defined]
            _medium_count=medium,  # type: ignore[name-defined]
            _low_count=low,  # type: ignore[name-defined]
            _compliance_score=score,
        )

    def to_json(self, report: SecurityReport) -> str:
        """Convert report to JSON."""
        _data=report.to_dict()
        data["vulnerabilities"] = [  # type: ignore[name-defined]
            {
                "id": v.id,
                "severity": v.severity.value,
                "type": v.type.value,
                "title": v.title,
                "description": v.description,
                "component": v.affected_component,
                "remediation": v.remediation,
                "cve": v.cve,
                "cwe": v.cwe,
            }
            for v in report.vulnerabilities
        ]

        return json.dumps(data, indent=2)  # type: ignore[name-defined]
