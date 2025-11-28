#!/usr/bin/env python3
"""
SLI/SLO Tracking Infrastructure for DebVisor.

Implements Service Level Indicator (SLI) and Service Level Objective (SLO)
tracking for enterprise reliability monitoring.

Features:
- SLI definitions for latency, availability, throughput, error rate
- SLO targets with burn rate alerting
- Error budget tracking and forecasting
- Rolling window calculations
- Multi-window alerting (for page-able incidents)
- Integration with Prometheus metrics

Based on Google SRE best practices.

Author: DebVisor Team
Date: November 28, 2025
"""

import asyncio
import logging
import statistics
import time
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Callable, Deque, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# =============================================================================
# SLI Types and Definitions
# =============================================================================

class SLIType(Enum):
    """Types of Service Level Indicators."""
    AVAILABILITY = "availability"      # Percentage of successful requests
    LATENCY = "latency"               # Request latency percentiles
    THROUGHPUT = "throughput"         # Requests per second
    ERROR_RATE = "error_rate"         # Percentage of error responses
    SATURATION = "saturation"         # Resource utilization
    FRESHNESS = "freshness"           # Data staleness
    CORRECTNESS = "correctness"       # Accuracy of responses


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    PAGE = "page"  # Requires immediate attention


@dataclass
class SLIDataPoint:
    """Single SLI measurement."""
    timestamp: datetime
    value: float
    success: bool
    latency_ms: Optional[float] = None
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class SLODefinition:
    """
    Service Level Objective definition.
    
    Attributes:
        name: Human-readable name
        sli_type: Type of SLI being measured
        target: Target value (e.g., 99.9 for 99.9% availability)
        window_days: Rolling window size in days
        burn_rate_thresholds: Burn rate thresholds for alerting
    """
    name: str
    sli_type: SLIType
    target: float  # Target percentage (0-100)
    window_days: int = 30
    burn_rate_thresholds: Dict[AlertSeverity, float] = field(default_factory=lambda: {
        AlertSeverity.WARNING: 2.0,
        AlertSeverity.CRITICAL: 10.0,
        AlertSeverity.PAGE: 14.4,  # 2% budget consumed in 1 hour
    })
    description: str = ""
    

@dataclass
class SLOStatus:
    """Current SLO status."""
    slo: SLODefinition
    current_value: float
    target_value: float
    is_meeting_target: bool
    error_budget_remaining: float
    error_budget_consumed: float
    burn_rate: float
    burn_rate_1h: float
    burn_rate_6h: float
    data_points: int
    window_start: datetime
    window_end: datetime
    alert_severity: Optional[AlertSeverity] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "slo_name": self.slo.name,
            "sli_type": self.slo.sli_type.value,
            "current_value": round(self.current_value, 4),
            "target_value": self.target_value,
            "is_meeting_target": self.is_meeting_target,
            "error_budget_remaining_percent": round(self.error_budget_remaining, 4),
            "error_budget_consumed_percent": round(self.error_budget_consumed, 4),
            "burn_rate": round(self.burn_rate, 2),
            "burn_rate_1h": round(self.burn_rate_1h, 2),
            "burn_rate_6h": round(self.burn_rate_6h, 2),
            "data_points": self.data_points,
            "window_start": self.window_start.isoformat(),
            "window_end": self.window_end.isoformat(),
            "alert_severity": self.alert_severity.value if self.alert_severity else None,
        }


# =============================================================================
# SLI Calculators
# =============================================================================

class SLICalculator(ABC):
    """Base class for SLI calculations."""
    
    @abstractmethod
    def calculate(self, data_points: List[SLIDataPoint]) -> float:
        """Calculate SLI value from data points."""
        pass


class AvailabilitySLI(SLICalculator):
    """
    Availability SLI calculator.
    
    Calculates: (successful_requests / total_requests) * 100
    """
    
    def calculate(self, data_points: List[SLIDataPoint]) -> float:
        if not data_points:
            return 100.0  # No data = assume healthy
        
        successful = sum(1 for dp in data_points if dp.success)
        return (successful / len(data_points)) * 100


class LatencySLI(SLICalculator):
    """
    Latency SLI calculator.
    
    Calculates percentage of requests within latency threshold.
    """
    
    def __init__(self, threshold_ms: float, percentile: float = 95.0):
        """
        Args:
            threshold_ms: Latency threshold in milliseconds
            percentile: Percentile to measure (e.g., 95 for p95)
        """
        self.threshold_ms = threshold_ms
        self.percentile = percentile
    
    def calculate(self, data_points: List[SLIDataPoint]) -> float:
        if not data_points:
            return 100.0
        
        latencies = [dp.latency_ms for dp in data_points if dp.latency_ms is not None]
        if not latencies:
            return 100.0
        
        # Calculate percentage within threshold
        within_threshold = sum(1 for lat in latencies if lat <= self.threshold_ms)
        return (within_threshold / len(latencies)) * 100
    
    def get_percentile(self, data_points: List[SLIDataPoint]) -> float:
        """Get the actual percentile value."""
        latencies = sorted([dp.latency_ms for dp in data_points if dp.latency_ms is not None])
        if not latencies:
            return 0.0
        
        index = int(len(latencies) * (self.percentile / 100))
        return latencies[min(index, len(latencies) - 1)]


class ErrorRateSLI(SLICalculator):
    """
    Error rate SLI calculator.
    
    Calculates: (1 - error_rate) * 100
    Target is inverted - higher is better.
    """
    
    def calculate(self, data_points: List[SLIDataPoint]) -> float:
        if not data_points:
            return 100.0  # No data = no errors
        
        errors = sum(1 for dp in data_points if not dp.success)
        error_rate = errors / len(data_points)
        return (1 - error_rate) * 100  # Convert to "good" percentage


class ThroughputSLI(SLICalculator):
    """
    Throughput SLI calculator.
    
    Calculates requests per second, compared to target.
    """
    
    def __init__(self, target_rps: float):
        self.target_rps = target_rps
    
    def calculate(self, data_points: List[SLIDataPoint]) -> float:
        if not data_points or len(data_points) < 2:
            return 100.0
        
        # Calculate time span
        timestamps = sorted([dp.timestamp for dp in data_points])
        duration_seconds = (timestamps[-1] - timestamps[0]).total_seconds()
        
        if duration_seconds == 0:
            return 100.0
        
        actual_rps = len(data_points) / duration_seconds
        
        # Return percentage of target achieved (capped at 100%)
        return min(100.0, (actual_rps / self.target_rps) * 100)


# =============================================================================
# SLO Tracker
# =============================================================================

class SLOTracker:
    """
    Tracks SLO compliance and error budgets.
    
    Example:
        tracker = SLOTracker()
        
        # Define SLO
        slo = SLODefinition(
            name="api-availability",
            sli_type=SLIType.AVAILABILITY,
            target=99.9,
            window_days=30
        )
        tracker.register_slo(slo)
        
        # Record data points
        tracker.record(slo.name, SLIDataPoint(
            timestamp=datetime.now(timezone.utc),
            value=1.0,
            success=True
        ))
        
        # Get status
        status = tracker.get_slo_status(slo.name)
    """
    
    def __init__(self, max_data_points: int = 1_000_000):
        """
        Initialize SLO tracker.
        
        Args:
            max_data_points: Maximum data points to retain per SLO
        """
        self._slos: Dict[str, SLODefinition] = {}
        self._calculators: Dict[str, SLICalculator] = {}
        self._data: Dict[str, Deque[SLIDataPoint]] = {}
        self._max_data_points = max_data_points
        self._lock = asyncio.Lock()
        self._alert_callbacks: List[Callable[[str, SLOStatus], None]] = []
    
    def register_slo(
        self,
        slo: SLODefinition,
        calculator: Optional[SLICalculator] = None
    ) -> None:
        """
        Register an SLO for tracking.
        
        Args:
            slo: SLO definition
            calculator: Custom SLI calculator (auto-selected if not provided)
        """
        self._slos[slo.name] = slo
        self._data[slo.name] = deque(maxlen=self._max_data_points)
        
        # Auto-select calculator based on SLI type
        if calculator:
            self._calculators[slo.name] = calculator
        else:
            self._calculators[slo.name] = self._get_default_calculator(slo.sli_type)
        
        logger.info(f"Registered SLO: {slo.name} (target: {slo.target}%)")
    
    def _get_default_calculator(self, sli_type: SLIType) -> SLICalculator:
        """Get default calculator for SLI type."""
        if sli_type == SLIType.AVAILABILITY:
            return AvailabilitySLI()
        elif sli_type == SLIType.LATENCY:
            return LatencySLI(threshold_ms=200)  # 200ms default
        elif sli_type == SLIType.ERROR_RATE:
            return ErrorRateSLI()
        elif sli_type == SLIType.THROUGHPUT:
            return ThroughputSLI(target_rps=100)  # 100 RPS default
        else:
            return AvailabilitySLI()  # Fallback
    
    async def record(self, slo_name: str, data_point: SLIDataPoint) -> None:
        """
        Record a data point for an SLO.
        
        Args:
            slo_name: Name of the SLO
            data_point: Measurement data point
        """
        async with self._lock:
            if slo_name not in self._slos:
                logger.warning(f"Unknown SLO: {slo_name}")
                return
            
            self._data[slo_name].append(data_point)
        
        # Check for alerts asynchronously
        asyncio.create_task(self._check_alerts(slo_name))
    
    def record_sync(self, slo_name: str, data_point: SLIDataPoint) -> None:
        """Synchronous version of record for non-async contexts."""
        if slo_name not in self._slos:
            logger.warning(f"Unknown SLO: {slo_name}")
            return
        self._data[slo_name].append(data_point)
    
    def get_slo_status(self, slo_name: str) -> Optional[SLOStatus]:
        """
        Get current status for an SLO.
        
        Args:
            slo_name: Name of the SLO
        
        Returns:
            SLOStatus or None if SLO not found
        """
        if slo_name not in self._slos:
            return None
        
        slo = self._slos[slo_name]
        calculator = self._calculators[slo_name]
        
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(days=slo.window_days)
        
        # Filter data points within window
        data_points = [
            dp for dp in self._data[slo_name]
            if dp.timestamp >= window_start
        ]
        
        # Calculate current SLI value
        current_value = calculator.calculate(data_points)
        
        # Calculate error budget
        error_budget_total = 100 - slo.target  # e.g., 0.1% for 99.9% target
        error_budget_consumed = max(0, slo.target - current_value)
        error_budget_remaining = max(0, error_budget_total - error_budget_consumed)
        
        # Calculate burn rates
        burn_rate = self._calculate_burn_rate(
            slo_name, calculator, slo.window_days
        )
        burn_rate_1h = self._calculate_burn_rate(
            slo_name, calculator, 1/24  # 1 hour
        )
        burn_rate_6h = self._calculate_burn_rate(
            slo_name, calculator, 6/24  # 6 hours
        )
        
        # Determine alert severity
        alert_severity = self._get_alert_severity(slo, burn_rate_1h)
        
        return SLOStatus(
            slo=slo,
            current_value=current_value,
            target_value=slo.target,
            is_meeting_target=current_value >= slo.target,
            error_budget_remaining=error_budget_remaining,
            error_budget_consumed=error_budget_consumed,
            burn_rate=burn_rate,
            burn_rate_1h=burn_rate_1h,
            burn_rate_6h=burn_rate_6h,
            data_points=len(data_points),
            window_start=window_start,
            window_end=now,
            alert_severity=alert_severity,
        )
    
    def _calculate_burn_rate(
        self,
        slo_name: str,
        calculator: SLICalculator,
        window_days: float
    ) -> float:
        """
        Calculate burn rate for a time window.
        
        Burn rate = actual error rate / allowed error rate
        A burn rate of 1.0 means consuming budget exactly as planned.
        >1.0 means consuming faster, <1.0 means consuming slower.
        """
        slo = self._slos[slo_name]
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(days=window_days)
        
        data_points = [
            dp for dp in self._data[slo_name]
            if dp.timestamp >= window_start
        ]
        
        if not data_points:
            return 0.0
        
        current_value = calculator.calculate(data_points)
        
        # Calculate burn rate
        allowed_error_rate = 100 - slo.target  # e.g., 0.1%
        actual_error_rate = 100 - current_value
        
        if allowed_error_rate == 0:
            return float('inf') if actual_error_rate > 0 else 0.0
        
        return actual_error_rate / allowed_error_rate
    
    def _get_alert_severity(
        self,
        slo: SLODefinition,
        burn_rate_1h: float
    ) -> Optional[AlertSeverity]:
        """Determine alert severity based on burn rate."""
        for severity in [AlertSeverity.PAGE, AlertSeverity.CRITICAL, AlertSeverity.WARNING]:
            threshold = slo.burn_rate_thresholds.get(severity)
            if threshold and burn_rate_1h >= threshold:
                return severity
        return None
    
    async def _check_alerts(self, slo_name: str) -> None:
        """Check for alert conditions and trigger callbacks."""
        status = self.get_slo_status(slo_name)
        if status and status.alert_severity:
            for callback in self._alert_callbacks:
                try:
                    callback(slo_name, status)
                except Exception as e:
                    logger.error(f"Alert callback error: {e}")
    
    def register_alert_callback(
        self,
        callback: Callable[[str, SLOStatus], None]
    ) -> None:
        """Register callback for SLO alerts."""
        self._alert_callbacks.append(callback)
    
    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status for all registered SLOs."""
        return {
            name: status.to_dict()
            for name in self._slos
            if (status := self.get_slo_status(name))
        }
    
    def get_error_budget_forecast(
        self,
        slo_name: str,
        forecast_days: int = 7
    ) -> Optional[Dict[str, Any]]:
        """
        Forecast error budget exhaustion.
        
        Args:
            slo_name: Name of the SLO
            forecast_days: Days to forecast
        
        Returns:
            Forecast information including days until exhaustion
        """
        status = self.get_slo_status(slo_name)
        if not status:
            return None
        
        # If not consuming budget, no exhaustion forecast
        if status.burn_rate <= 1.0:
            return {
                "slo_name": slo_name,
                "days_until_exhaustion": None,
                "forecast_confidence": "high",
                "status": "within_budget",
                "burn_rate": status.burn_rate,
            }
        
        # Calculate days until budget exhaustion at current burn rate
        remaining_budget = status.error_budget_remaining
        daily_consumption = (status.burn_rate - 1.0) * ((100 - status.slo.target) / status.slo.window_days)
        
        if daily_consumption <= 0:
            return {
                "slo_name": slo_name,
                "days_until_exhaustion": None,
                "forecast_confidence": "high",
                "status": "recovering",
                "burn_rate": status.burn_rate,
            }
        
        days_until_exhaustion = remaining_budget / daily_consumption
        
        return {
            "slo_name": slo_name,
            "days_until_exhaustion": round(days_until_exhaustion, 1),
            "forecast_confidence": "medium" if status.data_points < 1000 else "high",
            "status": "at_risk" if days_until_exhaustion < forecast_days else "healthy",
            "burn_rate": status.burn_rate,
            "remaining_budget_percent": status.error_budget_remaining,
        }


# =============================================================================
# Convenience Decorator for SLI Recording
# =============================================================================

def track_sli(
    tracker: SLOTracker,
    slo_name: str,
    labels: Optional[Dict[str, str]] = None
) -> Callable:
    """
    Decorator to automatically track SLI for async functions.
    
    Records success/failure and latency for each call.
    
    Example:
        @track_sli(tracker, "api-availability", labels={"endpoint": "/users"})
        async def get_users():
            return await db.fetch_users()
    """
    labels = labels or {}
    
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.monotonic()
            success = True
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                raise
            finally:
                latency_ms = (time.monotonic() - start_time) * 1000
                
                data_point = SLIDataPoint(
                    timestamp=datetime.now(timezone.utc),
                    value=1.0 if success else 0.0,
                    success=success,
                    latency_ms=latency_ms,
                    labels=labels,
                )
                
                await tracker.record(slo_name, data_point)
        
        return wrapper
    return decorator


# Must import after class definitions
import functools


# =============================================================================
# Global SLO Tracker Instance
# =============================================================================

_global_tracker: Optional[SLOTracker] = None


def get_global_tracker() -> SLOTracker:
    """Get or create global SLO tracker."""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = SLOTracker()
        
        # Register default SLOs for DebVisor
        _global_tracker.register_slo(SLODefinition(
            name="api-availability",
            sli_type=SLIType.AVAILABILITY,
            target=99.9,
            window_days=30,
            description="API endpoint availability"
        ))
        
        _global_tracker.register_slo(SLODefinition(
            name="api-latency-p95",
            sli_type=SLIType.LATENCY,
            target=95.0,  # 95% of requests under threshold
            window_days=7,
            description="API p95 latency under 200ms"
        ), LatencySLI(threshold_ms=200, percentile=95))
        
        _global_tracker.register_slo(SLODefinition(
            name="vm-operation-success",
            sli_type=SLIType.AVAILABILITY,
            target=99.5,
            window_days=30,
            description="VM lifecycle operation success rate"
        ))
        
        logger.info("Global SLO tracker initialized with default SLOs")
    
    return _global_tracker


def log_slo_alert(slo_name: str, status: SLOStatus) -> None:
    """Default alert callback - logs to logger."""
    logger.warning(
        f"SLO ALERT: {slo_name} - Severity: {status.alert_severity.value if status.alert_severity else 'none'}, "
        f"Current: {status.current_value:.2f}%, Target: {status.target_value}%, "
        f"Burn Rate (1h): {status.burn_rate_1h:.2f}x"
    )


# Register default alert callback
get_global_tracker().register_alert_callback(log_slo_alert)
