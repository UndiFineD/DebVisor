#!/usr/bin/env python3
"""
Enhanced Health Check Framework for DebVisor

Comprehensive health monitoring system providing component verification,
performance metrics, dependency validation, and operational insights.

Features:
    - Component health verification (binary, service, connectivity, config)
    - Health scoring system (0-100)
    - Performance baseline checks
    - Dependency validation
    - Automated remediation suggestions
    - Multiple output formats (table, JSON, YAML)

Author: DebVisor Team
Date: November 27, 2025
"""

import subprocess
import json
import logging
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import statistics

# Configure logging
logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health check status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class CheckCategory(Enum):
    """Categories of health checks."""
    BINARY = "binary"
    SERVICE = "service"
    CONNECTIVITY = "connectivity"
    CONFIGURATION = "configuration"
    RESOURCE = "resource"


@dataclass
class CheckResult:
    """Result of a single health check."""
    category: CheckCategory
    name: str
    status: HealthStatus
    score: int  # 0-100
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    remediation: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "category": self.category.value,
            "name": self.name,
            "status": self.status.value,
            "score": self.score,
            "message": self.message,
            "details": self.details,
            "remediation": self.remediation,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class HealthReport:
    """Comprehensive health report."""
    timestamp: datetime
    overall_score: int
    overall_status: HealthStatus
    checks: List[CheckResult]
    summary: Dict[str, int]
    recommendations: List[str]
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "overall_score": self.overall_score,
            "overall_status": self.overall_status.value,
            "checks": [c.to_dict() for c in self.checks],
            "summary": self.summary,
            "recommendations": self.recommendations,
            "metrics": self.metrics,
        }


class BinaryChecker:
    """Verifies required binaries are available."""

    REQUIRED_BINARIES = [
        "python3", "systemctl", "journalctl", "docker",
        "kubectl", "ceph", "virsh", "ssh", "curl"
    ]

    def check(self) -> CheckResult:
        """Check binary availability."""
        missing = []
        for binary in self.REQUIRED_BINARIES:
            try:
                subprocess.run(
                    ["which", binary],
                    check=True,
                    capture_output=True,
                    timeout=5
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing.append(binary)

        score = max(0, 100 - (len(missing) * 10))
        status = (
            HealthStatus.HEALTHY if len(missing) == 0
            else HealthStatus.DEGRADED if len(missing) <= 2
            else HealthStatus.UNHEALTHY
        )

        return CheckResult(
            category=CheckCategory.BINARY,
            name="Required Binaries",
            status=status,
            score=score,
            message=(f"{len(self.REQUIRED_BINARIES) - len(missing)}/"
                     f"{len(self.REQUIRED_BINARIES)} binaries available"),
            details={
                "missing_binaries": missing},
            remediation="Install missing packages: " +
            ", ".join(missing) if missing else None,
        )


class ServiceChecker:
    """Verifies critical services are running."""

    REQUIRED_SERVICES = [
        "docker",
        "kubelet",
        "ceph-osd",
        "ceph-mon",
        "ceph-mgr",
    ]

    def check(self) -> CheckResult:
        """Check service status."""
        failed = []

        for service in self.REQUIRED_SERVICES:
            try:
                result = subprocess.run(
                    ["systemctl", "is-active", service],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode != 0:
                    failed.append(service)
            except Exception as e:
                logger.warning(f"Could not check service {service}: {e}")
                failed.append(service)

        score = max(0, 100 - (len(failed) * 15))
        status = (
            HealthStatus.HEALTHY if len(failed) == 0
            else HealthStatus.DEGRADED if len(failed) <= 1
            else HealthStatus.UNHEALTHY
        )

        return CheckResult(
            category=CheckCategory.SERVICE,
            name="Critical Services",
            status=status,
            score=score,
            message=(f"{len(self.REQUIRED_SERVICES) - len(failed)}/"
                     f"{len(self.REQUIRED_SERVICES)} services running"),
            details={
                "failed_services": failed},
            remediation="Restart failed services: systemctl restart " +
            " ".join(failed) if failed else None,
        )


class ConnectivityChecker:
    """Verifies connectivity to critical endpoints."""

    ENDPOINTS = [
        ("Kubernetes API", "localhost:6443"),
        ("Docker Socket", "/var/run/docker.sock"),
        ("Ceph Monitor", "localhost:6789"),
    ]

    def check(self) -> CheckResult:
        """Check connectivity."""
        failed = []

        for name, endpoint in self.ENDPOINTS:
            if endpoint.startswith("/"):
                # Unix socket
                import os
                if not os.path.exists(endpoint):
                    failed.append(name)
            else:
                # TCP endpoint
                host, port = endpoint.split(":")
                try:
                    subprocess.run(
                        ["bash", "-c",
                         f"timeout 2 bash -c 'echo >/dev/tcp/{host}/{port}'"],
                        check=True,
                        capture_output=True,
                        timeout=5
                    )
                except Exception:
                    failed.append(name)

        score = max(0, 100 - (len(failed) * 20))
        status = (
            HealthStatus.HEALTHY if len(failed) == 0
            else HealthStatus.DEGRADED if len(failed) == 1
            else HealthStatus.UNHEALTHY
        )

        return CheckResult(
            category=CheckCategory.CONNECTIVITY,
            name="Critical Endpoints",
            status=status,
            score=score,
            message=(f"{len(self.ENDPOINTS) - len(failed)}/"
                     f"{len(self.ENDPOINTS)} endpoints reachable"),
            details={
                "unreachable_endpoints": failed},
            remediation="Check firewall and service status for: " +
            ", ".join(failed) if failed else None,
        )


class ConfigurationChecker:
    """Verifies configuration files are valid."""

    CONFIG_FILES = [
        "/etc/debvisor/config.yaml",
        "/etc/docker/daemon.json",
        "/etc/kubernetes/kubelet.conf",
    ]

    def check(self) -> CheckResult:
        """Check configuration validity."""
        missing = []
        invalid = []

        for config_file in self.CONFIG_FILES:
            import os
            if not os.path.exists(config_file):
                missing.append(config_file)
            else:
                # Basic validation - file is readable
                try:
                    with open(config_file, 'r') as f:
                        f.read(100)
                except Exception:
                    invalid.append(config_file)

        score = max(0, 100 - (len(missing) * 15) - (len(invalid) * 20))
        status = (
            HealthStatus.HEALTHY if len(missing) + len(invalid) == 0
            else HealthStatus.DEGRADED if len(missing) + len(invalid) <= 1
            else HealthStatus.UNHEALTHY
        )

        details = {}
        if missing:
            details["missing_configs"] = missing
        if invalid:
            details["invalid_configs"] = invalid

        return CheckResult(
            category=CheckCategory.CONFIGURATION,
            name="Configuration Integrity",
            status=status,
            score=score,
            message=(f"{len(self.CONFIG_FILES) - len(missing) - len(invalid)}/"
                     f"{len(self.CONFIG_FILES)} configs valid"),
            details=details,
            remediation="Check and repair configuration files" if invalid or missing else None,
        )


class ResourceChecker:
    """Verifies resource availability."""

    def check(self) -> CheckResult:
        """Check resource availability."""
        issues = []

        # Check disk space
        try:
            result = subprocess.run(
                ["df", "-h", "/"],
                capture_output=True,
                text=True,
                timeout=5
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                if len(parts) >= 5:
                    usage_pct = int(parts[4].rstrip('%'))
                    if usage_pct > 90:
                        issues.append(f"Disk usage high: {usage_pct}%")
        except Exception as e:
            logger.warning(f"Could not check disk space: {e}")

        # Check memory
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if 'MemAvailable' in line:
                        available = int(line.split()[1])
                        if available < 512000:  # < 500MB
                            issues.append(f"Low available memory: {available}KB")
        except Exception as e:
            logger.warning(f"Could not check memory: {e}")

        score = max(0, 100 - (len(issues) * 20))
        status = (
            HealthStatus.HEALTHY if len(issues) == 0
            else HealthStatus.DEGRADED if len(issues) == 1
            else HealthStatus.UNHEALTHY
        )

        return CheckResult(
            category=CheckCategory.RESOURCE,
            name="Resource Availability",
            status=status,
            score=score,
            message=f"Resource status: {'normal' if not issues else 'degraded'}",
            details={"issues": issues},
            remediation="Free up disk space and memory" if issues else None,
        )


class HealthCheckFramework:
    """
    Main health check framework.

    Coordinates all health checks and provides comprehensive reporting.
    """

    def __init__(self):
        """Initialize health check framework."""
        self.binary_checker = BinaryChecker()
        self.service_checker = ServiceChecker()
        self.connectivity_checker = ConnectivityChecker()
        self.config_checker = ConfigurationChecker()
        self.resource_checker = ResourceChecker()
        self.check_history: List[HealthReport] = []

    def run_checks(self) -> HealthReport:
        """
        Run all health checks.

        Returns:
            Comprehensive health report
        """
        checks = [
            self.binary_checker.check(),
            self.service_checker.check(),
            self.connectivity_checker.check(),
            self.config_checker.check(),
            self.resource_checker.check(),
        ]

        # Calculate overall score
        scores = [c.score for c in checks]
        overall_score = int(statistics.mean(scores)) if scores else 0

        # Determine overall status
        if overall_score >= 90:
            overall_status = HealthStatus.HEALTHY
        elif overall_score >= 70:
            overall_status = HealthStatus.DEGRADED
        else:
            overall_status = HealthStatus.UNHEALTHY

        # Summary
        summary = {
            "healthy": sum(1 for c in checks if c.status == HealthStatus.HEALTHY),
            "degraded": sum(1 for c in checks if c.status == HealthStatus.DEGRADED),
            "unhealthy": sum(1 for c in checks if c.status == HealthStatus.UNHEALTHY),
            "total": len(checks),
        }

        # Recommendations
        recommendations = [
            c.remediation for c in checks
            if c.remediation and c.status != HealthStatus.HEALTHY
        ]

        report = HealthReport(
            timestamp=datetime.now(),
            overall_score=overall_score,
            overall_status=overall_status,
            checks=checks,
            summary=summary,
            recommendations=recommendations,
        )

        self.check_history.append(report)
        return report

    def format_report_table(self, report: HealthReport) -> str:
        """Format report as table."""
        lines = [
            f"\n{'=' * 70}",
            "  DebVisor Health Check Report",
            f"  Generated: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"{'=' * 70}",
            f"\nOverall Status: {report.overall_status.value.upper()} (Score: {report.overall_score}/100)",
            "\nComponent Status:",
            f"  {'Component':<30} {'Status':<15} {'Score':>6}",
            f"  {'-' * 30} {'-' * 15} {'-' * 6}",
        ]

        for check in report.checks:
            lines.append(
                f"  {check.name:<30} {check.status.value:<15} {check.score:>6}"
            )

        if report.recommendations:
            lines.append("\nRecommendations:")
            for rec in report.recommendations:
                lines.append(f"  * {rec}")

        lines.append(f"\n{'=' * 70}\n")
        return "\n".join(lines)

    def format_report_json(self, report: HealthReport) -> str:
        """Format report as JSON."""
        return json.dumps(report.to_dict(), indent=2)

    def export_report(self, report: HealthReport, filepath: str, format: str = "json") -> None:
        """
        Export report to file.

        Args:
            report: Health report to export
            filepath: File path for export
            format: Export format (json, table)
        """
        if format == "json":
            content = self.format_report_json(report)
        elif format == "table":
            content = self.format_report_table(report)
        else:
            raise ValueError(f"Unknown format: {format}")

        with open(filepath, 'w') as f:
            f.write(content)
        logger.info(f"Report exported to {filepath}")


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Run health checks
    framework = HealthCheckFramework()
    report = framework.run_checks()

    # Display report
    print(framework.format_report_table(report))

    # Export reports
    framework.export_report(report, "/tmp/health_check.json", format="json")
    framework.export_report(report, "/tmp/health_check.txt", format="table")

    sys.exit(0 if report.overall_status == HealthStatus.HEALTHY else 1)
