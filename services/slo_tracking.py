"""Re-export SLO tracking from the canonical implementation.

Pylance + tests import `services.slo_tracking`.
The implementation lives in `opt.services.slo_tracking`.
"""

from __future__ import annotations

# Re-export public API
from opt.services.slo_tracking import (  # noqa: F401
    AlertSeverity,
    ErrorBudget,
    SLIRecord,
    SLIType,
    SLOTarget,
    SLOViolation,
    SLOTracker,
    track_availability_sli,
    track_latency_sli,
    track_sli,
)

__all__ = [
    "AlertSeverity",
    "ErrorBudget",
    "SLIRecord",
    "SLIType",
    "SLOTarget",
    "SLOViolation",
    "SLOTracker",
    "track_availability_sli",
    "track_latency_sli",
    "track_sli",
]
