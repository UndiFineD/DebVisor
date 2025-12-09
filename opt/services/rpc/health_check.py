"""
Health check and service diagnostics for DebVisor RPC service.

Provides:
- Service health status checks
- Dependency verification
- Diagnostic information collection
- Health endpoint implementation
"""

import logging
import time
import os
from typing import Dict, Any, Optional, List, Callable, cast
from enum import Enum
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status levels."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthCheckResult:
    """Result of a health check."""

    def __init__(
        self,
        component: str,
        status: HealthStatus,
        message: str = "",
        details: Optional[Dict[str, Any]] = None,
        check_time: Optional[float] = None,
    ) -> None:
        self.component = component
        self.status = status
        self.message = message
        self.details = details or {}
        self.check_time = check_time or time.time()
        self.duration_ms: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "component": self.component,
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
            "duration_ms": self.duration_ms,
            "timestamp": datetime.fromtimestamp(self.check_time).isoformat(),
        }


class HealthChecker:
    """Perform health checks on the RPC service."""

    def __init__(self) -> None:
        self.checks: Dict[str, Any] = {}
        self.results: List[HealthCheckResult] = []

    def register_check(
        self, name: str, check_func: Callable[[], HealthCheckResult], critical: bool = False
    ) -> None:
        """Register a health check function."""
        self.checks[name] = {
            "func": check_func,
            "critical": critical,
            "last_result": None,
            "last_check": None,
        }

    def run_check(self, name: str) -> Optional[HealthCheckResult]:
        """Run a specific health check."""
        if name not in self.checks:
            logger.warning(f"Unknown health check: {name}")
            return None

        check_info = self.checks[name]
        start_time = time.time()

        try:
            result = cast(HealthCheckResult, check_info["func"]())
            result.duration_ms = (time.time() - start_time) * 1000
            check_info["last_result"] = result
            check_info["last_check"] = time.time()
            return result

        except Exception as e:
            logger.error(f"Error running health check '{name}': {str(e)}")
            result = HealthCheckResult(
                component=name,
                status=HealthStatus.UNHEALTHY,
                message=f"Check failed: {str(e)}",
            )
            result.duration_ms = (time.time() - start_time) * 1000
            return result

    def run_all_checks(self) -> List[HealthCheckResult]:
        """Run all health checks."""
        results = []
        for name in self.checks:
            result = self.run_check(name)
            if result:
                results.append(result)
        return results

    def get_overall_status(
        self, results: Optional[List[HealthCheckResult]] = None
    ) -> HealthStatus:
        """Determine overall health status from check results."""
        if results is None:
            results = self.run_all_checks()

        if not results:
            return HealthStatus.HEALTHY

        # If any critical check is unhealthy, service is unhealthy
        for result in results:
            check_info = self.checks.get(result.component, {})
            if check_info.get("critical") and result.status == HealthStatus.UNHEALTHY:
                return HealthStatus.UNHEALTHY

        # If any check is unhealthy or degraded
        has_degraded = any(r.status == HealthStatus.DEGRADED for r in results)
        has_unhealthy = any(r.status == HealthStatus.UNHEALTHY for r in results)

        if has_unhealthy:
            return HealthStatus.UNHEALTHY
        elif has_degraded:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY


def check_basic_requirements() -> HealthCheckResult:
    """Check basic service requirements."""
    try:
        # Check required Python modules
        required_modules = ["grpc", "google.protobuf", "threading", "socket"]
        missing = []

        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing.append(module)

        if missing:
            return HealthCheckResult(
                component="basic_requirements",
                status=HealthStatus.UNHEALTHY,
                message=f"Missing required modules: {', '.join(missing)}",
                details={"missing_modules": missing},
            )

        return HealthCheckResult(
            component="basic_requirements",
            status=HealthStatus.HEALTHY,
            message="All required modules available",
        )

    except Exception as e:
        return HealthCheckResult(
            component="basic_requirements",
            status=HealthStatus.UNHEALTHY,
            message=f"Error checking requirements: {str(e)}",
        )


def check_port_availability(port: int) -> HealthCheckResult:
    """Check if service port is available."""
    import socket

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        result = sock.connect_ex(("localhost", port))
        sock.close()

        if result == 0:
            return HealthCheckResult(
                component="port_availability",
                status=HealthStatus.HEALTHY,
                message=f"Port {port} is available",
                details={"port": port},
            )
        else:
            return HealthCheckResult(
                component="port_availability",
                status=HealthStatus.DEGRADED,
                message=f"Port {port} is in use",
                details={"port": port},
            )

    except Exception as e:
        return HealthCheckResult(
            component="port_availability",
            status=HealthStatus.DEGRADED,
            message=f"Error checking port: {str(e)}",
            details={"port": port, "error": str(e)},
        )


def check_disk_space(path: str = "/") -> HealthCheckResult:
    """Check available disk space."""
    try:
        import shutil

        stat = shutil.disk_usage(path)

        percent_used = (stat.used / stat.total) * 100

        if percent_used > 90:
            status = HealthStatus.UNHEALTHY
            message = f"Disk almost full: {percent_used:.1f}% used"
        elif percent_used > 75:
            status = HealthStatus.DEGRADED
            message = f"Disk usage high: {percent_used:.1f}% used"
        else:
            status = HealthStatus.HEALTHY
            message = f"Disk usage OK: {percent_used:.1f}% used"

        return HealthCheckResult(
            component="disk_space",
            status=status,
            message=message,
            details={
                "path": path,
                "total_bytes": stat.total,
                "used_bytes": stat.used,
                "free_bytes": stat.free,
                "percent_used": percent_used,
            },
        )

    except Exception as e:
        return HealthCheckResult(
            component="disk_space",
            status=HealthStatus.DEGRADED,
            message=f"Error checking disk space: {str(e)}",
            details={"path": path, "error": str(e)},
        )


def check_memory_availability() -> HealthCheckResult:
    """Check available system memory."""
    try:
        with open("/proc/meminfo", "r") as f:
            meminfo = {}
            for line in f:
                key, value = line.split(":")
                meminfo[key.strip()] = int(value.strip().split()[0])

        total = meminfo.get("MemTotal", 0)
        available = meminfo.get("MemAvailable", 0)
        percent_available = (available / total * 100) if total > 0 else 0

        if percent_available < 10:
            status = HealthStatus.UNHEALTHY
            message = "Memory almost exhausted"
        elif percent_available < 25:
            status = HealthStatus.DEGRADED
            message = "Memory usage high"
        else:
            status = HealthStatus.HEALTHY
            message = "Memory available"

        return HealthCheckResult(
            component="memory",
            status=status,
            message=message,
            details={
                "total_kb": total,
                "available_kb": available,
                "percent_available": percent_available,
            },
        )

    except Exception as e:
        return HealthCheckResult(
            component="memory",
            status=HealthStatus.DEGRADED,
            message=f"Error checking memory: {str(e)}",
            details={"error": str(e)},
        )


def create_diagnostics_report(health_checker: HealthChecker) -> Dict[str, Any]:
    """Create comprehensive diagnostics report."""
    results = health_checker.run_all_checks()
    overall_status = health_checker.get_overall_status(results)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status.value,
        "checks": [r.to_dict() for r in results],
        "service_info": {
            "pid": os.getpid(),
            "python_version": __import__("sys").version,
            "platform": __import__("platform").platform(),
        },
    }
