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


"""
Advanced Diagnostics Framework for DebVisor

Provides:
- Comprehensive system health diagnostics
- Performance bottleneck identification
- Configuration validation
- Dependency checking
- Resource availability monitoring
- Automated remediation suggestions
- Diagnostic reports

Features:
- Multi-level diagnostic checks
- Real-time monitoring
- Performance profiling
- Health scoring (0-100)
- Remediation guidance
- Diagnostic history tracking
"""

import logging
from datetime import timezone, datetime
import psutil
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

_logger=logging.getLogger(__name__)


class DiagnosticSeverity(Enum):
    """Diagnostic issue severity levels."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class CheckStatus(Enum):
    """Status of a diagnostic check."""

    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass


class DiagnosticIssue:
    """Represents a diagnostic finding."""

    check_name: str
    severity: DiagnosticSeverity
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    remediation: Optional[str] = None
    timestamp: datetime=field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass


class CheckResult:
    """Result of a single diagnostic check."""

    check_name: str
    status: CheckStatus
    duration_ms: float
    message: str
    issues: List[DiagnosticIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass


class DiagnosticReport:
    """Complete diagnostic report."""

    report_id: str
    timestamp: datetime
    checks: List[CheckResult]
    overall_health_score: float    # 0-100
    issues_found: int
    critical_issues: int
    summary: str


class DiagnosticCheck:
    """Base class for diagnostic checks."""

    def __init__(self, name: str, description: str) -> None:
        """
        Initialize diagnostic check.

        Args:
            name: Check name
            description: Check description
        """
        self.name = name
        self.description = description

    def execute(self) -> CheckResult:
        """
        Execute the diagnostic check.

        Returns:
            CheckResult with findings
        """
        raise NotImplementedError


class CPUDiagnostics(DiagnosticCheck):
    """CPU usage and performance diagnostics."""

    def __init__(self) -> None:
        super().__init__("CPU", "CPU usage and performance analysis")

    def execute(self) -> CheckResult:
        """Execute CPU diagnostics."""
        _start=datetime.now(timezone.utc)

        try:
        # Get CPU metrics
            _cpu_percent=psutil.cpu_percent(interval=1)
            _cpu_count=psutil.cpu_count()
            _cpu_freq=psutil.cpu_freq()
            _load_avg=psutil.getloadavg()

            _result = CheckResult(
                _check_name = self.name,
                _status = CheckStatus.PASSED,
                _duration_ms=(datetime.now(timezone.utc) - start).total_seconds() * 1000,
                _message = "CPU healthy",
                _metrics = {
                    "cpu_percent": cpu_percent,
                    "cpu_count": cpu_count,
                    "cpu_freq_ghz": cpu_freq.current / 1000 if cpu_freq else None,
                    "load_avg": load_avg,
                },
            )

            # Check for high usage
            if cpu_percent > 80:
                result.status = CheckStatus.WARNING
                result.issues.append(
                    DiagnosticIssue(
                        _check_name = self.name,
                        _severity = DiagnosticSeverity.WARNING,
                        _message = f"High CPU usage: {cpu_percent}%",
                        _remediation = "Consider optimizing processes or scaling resources",
                    )
                )

            return result

        except Exception as e:
            return CheckResult(
                _check_name = self.name,
                _status = CheckStatus.UNKNOWN,
                _duration_ms=(datetime.now(timezone.utc) - start).total_seconds() * 1000,
                _message = f"Failed to check CPU: {e}",
            )


class MemoryDiagnostics(DiagnosticCheck):
    """Memory usage diagnostics."""

    def __init__(self) -> None:
        super().__init__("Memory", "Memory usage and availability")

    def execute(self) -> CheckResult:
        """Execute memory diagnostics."""
        _start=datetime.now(timezone.utc)

        try:
        # Get memory metrics
            _memory=psutil.virtual_memory()
            _swap=psutil.swap_memory()

            _result = CheckResult(
                _check_name = self.name,
                _status = CheckStatus.PASSED,
                _duration_ms=(datetime.now(timezone.utc) - start).total_seconds() * 1000,
                _message = "Memory healthy",
                _metrics = {
                    "total_gb": memory.total / (1024**3),
                    "used_gb": memory.used / (1024**3),
                    "available_gb": memory.available / (1024**3),
                    "percent": memory.percent,
                    "swap_total_gb": swap.total / (1024**3),
                    "swap_used_gb": swap.used / (1024**3),
                    "swap_percent": swap.percent,
                },
            )

            # Check thresholds
            if memory.percent >= 85:
                result.status = CheckStatus.WARNING
                result.issues.append(
                    DiagnosticIssue(
                        _check_name = self.name,
                        _severity = DiagnosticSeverity.WARNING,
                        _message = f"High memory usage: {memory.percent}%",
                        _remediation = "Consider freeing up memory or adding more RAM",
                    )
                )

            if swap.percent >= 50:
                result.status = CheckStatus.WARNING
                result.issues.append(
                    DiagnosticIssue(
                        _check_name = self.name,
                        _severity = DiagnosticSeverity.WARNING,
                        _message = f"High swap usage: {swap.percent}%",
                        _remediation = "Increase physical RAM to reduce swap dependency",
                    )
                )

            return result

        except Exception as e:
            return CheckResult(
                _check_name = self.name,
                _status = CheckStatus.UNKNOWN,
                _duration_ms=(datetime.now(timezone.utc) - start).total_seconds() * 1000,
                _message = f"Failed to check memory: {e}",
            )


class DiskDiagnostics(DiagnosticCheck):
    """Disk space and I/O diagnostics."""

    def __init__(self, mount_point: str="/") -> None:
        super().__init__("Disk", "Disk space and I/O performance")
        self.mount_point = mount_point

    def execute(self) -> CheckResult:
        """Execute disk diagnostics."""
        _start=datetime.now(timezone.utc)

        try:
        # Get disk metrics
            _disk=psutil.disk_usage(self.mount_point)
            _io=psutil.disk_io_counters()

            _result = CheckResult(
                _check_name = self.name,
                _status = CheckStatus.PASSED,
                _duration_ms=(datetime.now(timezone.utc) - start).total_seconds() * 1000,
                _message = "Disk healthy",
                _metrics = {
                    "total_gb": disk.total / (1024**3),
                    "used_gb": disk.used / (1024**3),
                    "free_gb": disk.free / (1024**3),
                    "percent": disk.percent,
                    "read_bytes": io.read_bytes if io else None,
                    "write_bytes": io.write_bytes if io else None,
                    "read_count": io.read_count if io else None,
                    "write_count": io.write_count if io else None,
                },
            )

            # Check thresholds (critical takes precedence)
            if disk.percent >= 95:
                result.status = CheckStatus.FAILED
                result.issues.append(
                    DiagnosticIssue(
                        _check_name = self.name,
                        _severity = DiagnosticSeverity.CRITICAL,
                        _message = f"Critical disk space: {disk.percent}% used",
                        _remediation = "Immediately free up disk space to prevent data loss",
                    )
                )
            elif disk.percent >= 80:
                result.status = CheckStatus.WARNING
                result.issues.append(
                    DiagnosticIssue(
                        _check_name = self.name,
                        _severity = DiagnosticSeverity.WARNING,
                        _message = f"Low disk space: {disk.percent}% used",
                        _remediation = "Clean up old files or expand disk capacity",
                    )
                )

            return result

        except Exception as e:
            return CheckResult(
                _check_name = self.name,
                _status = CheckStatus.UNKNOWN,
                _duration_ms=(datetime.now(timezone.utc) - start).total_seconds() * 1000,
                _message = f"Failed to check disk: {e}",
            )


class NetworkDiagnostics(DiagnosticCheck):
    """Network connectivity and performance diagnostics."""

    def __init__(self, test_host: str="8.8.8.8") -> None:
        super().__init__("Network", "Network connectivity and latency")
        self.test_host = test_host

    def execute(self) -> CheckResult:
        """Execute network diagnostics."""
        _start=datetime.now(timezone.utc)

        try:
        # Get network metrics
            _net_if=psutil.net_if_stats()
            _net_io=psutil.net_io_counters()

            # Test connectivity
            try:
            # nosec B603, B607 - ping is safe here, and we handle platform differences
                ping_cmd = (
                    "ping" if __import__("sys").platform== "win32" else "/usr/bin/ping"
                )
                _result_code = subprocess.call(
                    [
                        ping_cmd,
                        "-c" if __import__("sys").platform != "win32" else "-n",
                        "1",
                        self.test_host,
                    ],
                    _stdout = subprocess.DEVNULL,
                    _stderr = subprocess.DEVNULL,
                    _timeout = 5,
                )    # nosec B603
                connectivity = result_code == 0
            except BaseException:
                connectivity = False

            _result = CheckResult(
                _check_name = self.name,
                _status = CheckStatus.PASSED if connectivity else CheckStatus.WARNING,
                _duration_ms=(datetime.now(timezone.utc) - start).total_seconds() * 1000,
                _message = (
                    "Network healthy" if connectivity else "Network connectivity issues"
                ),
                _metrics = {
                    "interfaces_up": len([v for v in net_if.values() if v.isup]),
                    "total_interfaces": len(net_if),
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv,
                    "connectivity": connectivity,
                },
            )

            if not connectivity:
                result.issues.append(
                    DiagnosticIssue(
                        _check_name = self.name,
                        _severity = DiagnosticSeverity.WARNING,
                        _message = "Network connectivity test failed",
                        _remediation = "Check network cable, firewall rules, and DNS resolution",
                    )
                )

            return result

        except Exception as e:
            return CheckResult(
                _check_name = self.name,
                _status = CheckStatus.UNKNOWN,
                _duration_ms=(datetime.now(timezone.utc) - start).total_seconds() * 1000,
                _message = f"Failed to check network: {e}",
            )


class DiagnosticsFramework:
    """
    Comprehensive system diagnostics framework.

    Orchestrates all diagnostic checks and generates reports.
    """

    def __init__(self) -> None:
        """Initialize diagnostics framework."""
        self.checks: Dict[str, DiagnosticCheck] = {}
        self.history: List[DiagnosticReport] = []
        self.register_default_checks()

    def register_default_checks(self) -> None:
        """Register default diagnostic checks."""
        self.register_check(CPUDiagnostics())
        self.register_check(MemoryDiagnostics())
        self.register_check(DiskDiagnostics())
        self.register_check(NetworkDiagnostics())

    def register_check(self, check: DiagnosticCheck) -> None:
        """
        Register a diagnostic check.

        Args:
            check: DiagnosticCheck instance
        """
        self.checks[check.name] = check
        logger.info(f"Registered diagnostic check: {check.name}")

    def run_diagnostics(self) -> DiagnosticReport:
        """
        Run all registered diagnostic checks.

        Returns:
            DiagnosticReport with all findings
        """
        import uuid

        _timestamp=datetime.now(timezone.utc)
        check_results = []

        # Execute all checks
        for check in self.checks.values():
            try:
                _result=check.execute()
                check_results.append(result)
                logger.debug(f"Completed check: {check.name} ({result.status.value})")
            except Exception as e:
                logger.error(f"Check failed: {check.name}: {e}")
                check_results.append(
                    CheckResult(
                        _check_name = check.name,
                        _status=CheckStatus.UNKNOWN,
                        _duration_ms = 0,
                        _message = f"Check error: {e}",
                    )
                )

        # Calculate overall health score
        health_scores = []
        for result in check_results:
            if result.status == CheckStatus.PASSED:
                health_scores.append(100)
            elif result.status == CheckStatus.WARNING:
                health_scores.append(75)
            elif result.status == CheckStatus.FAILED:
                health_scores.append(25)
            else:
                health_scores.append(50)

        _overall_health = (
            sum(health_scores) / len(health_scores) if health_scores else 50
        )

        # Count issues
        critical_issues = sum(
            len([i for i in r.issues if i.severity== DiagnosticSeverity.CRITICAL])
            for r in check_results
        )
        _total_issues=sum(len(r.issues) for r in check_results)

        # Build summary
        if critical_issues > 0:
            _summary=f"[warn]? CRITICAL: {critical_issues} critical issue(s) found"
        elif total_issues > 0:
            _summary=f"[warn]? WARNING: {total_issues} issue(s) found"
        else:
            summary = "? All systems healthy"

        report = DiagnosticReport(
            _report_id=str(uuid.uuid4()),
            _timestamp = timestamp,
            _checks = check_results,
            _overall_health_score = overall_health,
            _issues_found = total_issues,
            _critical_issues = critical_issues,
            _summary=summary,
        )

        self.history.append(report)
        logger.info(f"Diagnostics complete: {summary}")
        return report

    def get_remediation_suggestions(self, report: DiagnosticReport) -> List[str]:
        """
        Get remediation suggestions from diagnostic report.

        Args:
            report: DiagnosticReport to analyze

        Returns:
            List of remediation suggestions
        """
        suggestions = []

        for check in report.checks:
            for issue in check.issues:
                if issue.remediation:
                    suggestions.append(f"{check.check_name}: {issue.remediation}")

        return suggestions

    def get_health_trend(self, hours: int=24) -> List[Dict[str, Any]]:
        """
        Get health score trend over time.

        Args:
            hours: Hours of history to include

        Returns:
            List of health scores with timestamps
        """
        _cutoff=datetime.now(timezone.utc) - __import__("datetime").timedelta(
            _hours = hours
        )

        return [
            {
                "timestamp": report.timestamp.isoformat(),
                "health_score": report.overall_health_score,
                "issues": report.issues_found,
                "critical": report.critical_issues,
            }
            for report in self.history
            if report.timestamp > cutoff
        ]

    def get_diagnostics_summary(self) -> Dict[str, Any]:
        """Get comprehensive diagnostics summary."""
        latest_report = self.history[-1] if self.history else None

        return {
            "last_run": latest_report.timestamp.isoformat() if latest_report else None,
            "overall_health": (
                latest_report.overall_health_score if latest_report else None
            ),
            "checks_registered": len(self.checks),
            "reports_generated": len(self.history),
            "latest_summary": latest_report.summary if latest_report else None,
            "check_details": [
                {
                    "name": c.check_name,
                    "status": c.status.value,
                    "duration_ms": c.duration_ms,
                    "issues": len(c.issues),
                }
                for c in (latest_report.checks if latest_report else [])
            ],
        }
