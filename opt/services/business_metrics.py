#!/usr/bin/env python3
"""
Business Metrics Module for DebVisor.

Provides custom metrics tracking for business operations:
- Operation counters (debt resolutions, payments, disputes)
- Revenue tracking metrics
- User activity metrics
- Performance histograms
- Custom labels and dimensions

Integrates with Prometheus and supports multiple backends.

Author: DebVisor Team
Date: November 28, 2025
"""

import asyncio
import functools
import logging
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar('F', bound=Callable[..., Any])


# =============================================================================
# Enums and Constants
# =============================================================================

class MetricType(Enum):
    """Types of metrics."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class AggregationType(Enum):
    """Aggregation methods."""
    SUM = "sum"
    AVERAGE = "avg"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    PERCENTILE_50 = "p50"
    PERCENTILE_90 = "p90"
    PERCENTILE_95 = "p95"
    PERCENTILE_99 = "p99"


# Default histogram buckets for latency (in seconds)
DEFAULT_LATENCY_BUCKETS = (
    0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0
)

# Default histogram buckets for amounts (in dollars)
DEFAULT_AMOUNT_BUCKETS = (
    10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000
)


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class MetricDefinition:
    """Definition of a metric."""

    name: str
    type: MetricType
    description: str
    labels: List[str] = field(default_factory=list)
    buckets: Optional[tuple] = None
    unit: str = ""

    def __post_init__(self):
        # Validate metric name
        if not self.name or not self.name.replace('_', '').replace('.', '').isalnum():
            raise ValueError(f"Invalid metric name: {self.name}")


@dataclass
class MetricSample:
    """A single metric sample."""

    name: str
    value: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class HistogramData:
    """Histogram metric data."""

    sum: float = 0.0
    count: int = 0
    buckets: Dict[float, int] = field(default_factory=dict)

    def observe(self, value: float, bucket_boundaries: tuple) -> None:
        """Record an observation."""
        self.sum += value
        self.count += 1

        for boundary in bucket_boundaries:
            if value <= boundary:
                self.buckets[boundary] = self.buckets.get(boundary, 0) + 1


# =============================================================================
# Metric Storage
# =============================================================================

class MetricStorage:
    """Thread-safe metric storage."""

    def __init__(self):
        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, HistogramData] = defaultdict(HistogramData)
        self._lock = threading.RLock()

    def increment_counter(self, key: str, value: float = 1.0) -> float:
        """Increment a counter."""
        with self._lock:
            self._counters[key] += value
            return self._counters[key]

    def set_gauge(self, key: str, value: float) -> None:
        """Set a gauge value."""
        with self._lock:
            self._gauges[key] = value

    def observe_histogram(self, key: str, value: float, buckets: tuple) -> None:
        """Record histogram observation."""
        with self._lock:
            if key not in self._histograms:
                self._histograms[key] = HistogramData()
            self._histograms[key].observe(value, buckets)

    def get_counter(self, key: str) -> float:
        """Get counter value."""
        with self._lock:
            return self._counters.get(key, 0.0)

    def get_gauge(self, key: str) -> Optional[float]:
        """Get gauge value."""
        with self._lock:
            return self._gauges.get(key)

    def get_histogram(self, key: str) -> Optional[HistogramData]:
        """Get histogram data."""
        with self._lock:
            return self._histograms.get(key)

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all metric values."""
        with self._lock:
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {
                    k: {"sum": v.sum, "count": v.count, "buckets": v.buckets}
                    for k, v in self._histograms.items()
                }
            }

    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()


# =============================================================================
# Business Metrics
# =============================================================================

class BusinessMetrics:
    """
    Business metrics collector for DebVisor.

    Tracks key business KPIs including:
    - Debt resolutions and outcomes
    - Payment processing metrics
    - User engagement metrics
    - Revenue and financial metrics
    - Operational metrics
    """

    # Metric definitions
    METRICS = {
        # Debt resolution metrics
        "debvisor_debts_created_total": MetricDefinition(
            name="debvisor_debts_created_total",
            type=MetricType.COUNTER,
            description="Total number of debts created",
            labels=["type", "source"]
        ),
        "debvisor_debts_resolved_total": MetricDefinition(
            name="debvisor_debts_resolved_total",
            type=MetricType.COUNTER,
            description="Total number of debts resolved",
            labels=["outcome", "type"]
        ),
        "debvisor_debt_amount": MetricDefinition(
            name="debvisor_debt_amount",
            type=MetricType.HISTOGRAM,
            description="Distribution of debt amounts",
            labels=["type"],
            buckets=DEFAULT_AMOUNT_BUCKETS,
            unit="dollars"
        ),
        "debvisor_debt_age_days": MetricDefinition(
            name="debvisor_debt_age_days",
            type=MetricType.HISTOGRAM,
            description="Age of debts in days at resolution",
            labels=["outcome"],
            buckets=(7, 14, 30, 60, 90, 180, 365, 730)
        ),

        # Payment metrics
        "debvisor_payments_total": MetricDefinition(
            name="debvisor_payments_total",
            type=MetricType.COUNTER,
            description="Total payment transactions",
            labels=["method", "status"]
        ),
        "debvisor_payment_amount": MetricDefinition(
            name="debvisor_payment_amount",
            type=MetricType.HISTOGRAM,
            description="Distribution of payment amounts",
            labels=["method"],
            buckets=DEFAULT_AMOUNT_BUCKETS,
            unit="dollars"
        ),
        "debvisor_payment_processing_seconds": MetricDefinition(
            name="debvisor_payment_processing_seconds",
            type=MetricType.HISTOGRAM,
            description="Payment processing duration",
            labels=["method", "gateway"],
            buckets=DEFAULT_LATENCY_BUCKETS
        ),

        # User metrics
        "debvisor_users_active": MetricDefinition(
            name="debvisor_users_active",
            type=MetricType.GAUGE,
            description="Current active users",
            labels=["role"]
        ),
        "debvisor_users_registered_total": MetricDefinition(
            name="debvisor_users_registered_total",
            type=MetricType.COUNTER,
            description="Total registered users",
            labels=["source"]
        ),
        "debvisor_user_sessions_total": MetricDefinition(
            name="debvisor_user_sessions_total",
            type=MetricType.COUNTER,
            description="Total user sessions",
            labels=["type"]
        ),

        # Dispute metrics
        "debvisor_disputes_total": MetricDefinition(
            name="debvisor_disputes_total",
            type=MetricType.COUNTER,
            description="Total disputes filed",
            labels=["reason", "status"]
        ),
        "debvisor_dispute_resolution_seconds": MetricDefinition(
            name="debvisor_dispute_resolution_seconds",
            type=MetricType.HISTOGRAM,
            description="Dispute resolution time",
            labels=["reason"],
            buckets=(3600, 86400, 172800, 604800, 1209600, 2592000)  # 1h to 30d
        ),

        # Communication metrics
        "debvisor_communications_sent_total": MetricDefinition(
            name="debvisor_communications_sent_total",
            type=MetricType.COUNTER,
            description="Total communications sent",
            labels=["channel", "template"]
        ),
        "debvisor_communication_delivery_rate": MetricDefinition(
            name="debvisor_communication_delivery_rate",
            type=MetricType.GAUGE,
            description="Communication delivery rate",
            labels=["channel"],
            unit="percent"
        ),

        # API metrics
        "debvisor_api_requests_total": MetricDefinition(
            name="debvisor_api_requests_total",
            type=MetricType.COUNTER,
            description="Total API requests",
            labels=["endpoint", "method", "status"]
        ),
        "debvisor_api_latency_seconds": MetricDefinition(
            name="debvisor_api_latency_seconds",
            type=MetricType.HISTOGRAM,
            description="API request latency",
            labels=["endpoint", "method"],
            buckets=DEFAULT_LATENCY_BUCKETS
        ),

        # Revenue metrics
        "debvisor_revenue_total": MetricDefinition(
            name="debvisor_revenue_total",
            type=MetricType.COUNTER,
            description="Total revenue collected",
            labels=["type"],
            unit="dollars"
        ),
        "debvisor_fees_collected_total": MetricDefinition(
            name="debvisor_fees_collected_total",
            type=MetricType.COUNTER,
            description="Total fees collected",
            labels=["fee_type"],
            unit="dollars"
        ),

        # Compliance metrics
        "debvisor_compliance_checks_total": MetricDefinition(
            name="debvisor_compliance_checks_total",
            type=MetricType.COUNTER,
            description="Total compliance checks performed",
            labels=["check_type", "result"]
        ),
        "debvisor_regulatory_reports_generated": MetricDefinition(
            name="debvisor_regulatory_reports_generated",
            type=MetricType.COUNTER,
            description="Regulatory reports generated",
            labels=["report_type"]
        ),
    }

    def __init__(self, storage: Optional[MetricStorage] = None):
        """Initialize business metrics."""
        self._storage = storage or MetricStorage()
        self._label_values_cache: Dict[str, Set[str]] = defaultdict(set)

        logger.info("Business metrics initialized")

    def _make_key(self, name: str, labels: Dict[str, str]) -> str:
        """Create metric key from name and labels."""
        if not labels:
            return name
        sorted_labels = sorted(labels.items())
        label_str = ",".join(f'{k}="{v}"' for k, v in sorted_labels)
        return f"{name}{{{label_str}}}"

    def _validate_labels(self, metric_name: str, labels: Dict[str, str]) -> None:
        """Validate labels against metric definition."""
        definition = self.METRICS.get(metric_name)
        if not definition:
            return

        for label in labels.keys():
            if label not in definition.labels:
                logger.warning(f"Unknown label '{label}' for metric '{metric_name}'")

    # =========================================================================
    # Counter Methods
    # =========================================================================

    def increment(
        self,
        metric_name: str,
        value: float = 1.0,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Increment a counter metric.

        Args:
            metric_name: Name of the metric
            value: Value to increment by
            labels: Metric labels
        """
        labels = labels or {}
        self._validate_labels(metric_name, labels)
        key = self._make_key(metric_name, labels)
        self._storage.increment_counter(key, value)

        # Cache label values
        for k, v in labels.items():
            self._label_values_cache[f"{metric_name}:{k}"].add(v)

    # =========================================================================
    # Gauge Methods
    # =========================================================================

    def set_gauge(
        self,
        metric_name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Set a gauge metric value.

        Args:
            metric_name: Name of the metric
            value: Value to set
            labels: Metric labels
        """
        labels = labels or {}
        self._validate_labels(metric_name, labels)
        key = self._make_key(metric_name, labels)
        self._storage.set_gauge(key, value)

    def increment_gauge(
        self,
        metric_name: str,
        value: float = 1.0,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Increment a gauge value."""
        labels = labels or {}
        key = self._make_key(metric_name, labels)
        current = self._storage.get_gauge(key) or 0.0
        self._storage.set_gauge(key, current + value)

    def decrement_gauge(
        self,
        metric_name: str,
        value: float = 1.0,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Decrement a gauge value."""
        self.increment_gauge(metric_name, -value, labels)

    # =========================================================================
    # Histogram Methods
    # =========================================================================

    def observe(
        self,
        metric_name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Record a histogram observation.

        Args:
            metric_name: Name of the metric
            value: Value to observe
            labels: Metric labels
        """
        labels = labels or {}
        self._validate_labels(metric_name, labels)
        key = self._make_key(metric_name, labels)

        # Get buckets from definition
        definition = self.METRICS.get(metric_name)
        buckets = (definition.buckets if definition and definition.buckets
                   else DEFAULT_LATENCY_BUCKETS)

        self._storage.observe_histogram(key, value, buckets)

    # =========================================================================
    # Business-Specific Methods
    # =========================================================================

    def record_debt_created(
        self,
        amount: float,
        debt_type: str = "standard",
        source: str = "api"
    ) -> None:
        """Record a new debt creation."""
        self.increment("debvisor_debts_created_total", 1, {"type": debt_type, "source": source})
        self.observe("debvisor_debt_amount", amount, {"type": debt_type})

    def record_debt_resolved(
        self,
        outcome: str,
        debt_type: str = "standard",
        age_days: int = 0
    ) -> None:
        """Record a debt resolution."""
        self.increment("debvisor_debts_resolved_total", 1, {"outcome": outcome, "type": debt_type})
        if age_days > 0:
            self.observe("debvisor_debt_age_days", age_days, {"outcome": outcome})

    def record_payment(
        self,
        amount: float,
        method: str,
        status: str = "success",
        processing_time: Optional[float] = None,
        gateway: str = "default"
    ) -> None:
        """Record a payment transaction."""
        self.increment("debvisor_payments_total", 1, {"method": method, "status": status})

        if status == "success":
            self.observe("debvisor_payment_amount", amount, {"method": method})
            self.increment("debvisor_revenue_total", amount, {"type": "payment"})

        if processing_time is not None:
            self.observe(
                "debvisor_payment_processing_seconds",
                processing_time,
                {"method": method, "gateway": gateway}
            )

    def record_user_registration(self, source: str = "web") -> None:
        """Record a new user registration."""
        self.increment("debvisor_users_registered_total", 1, {"source": source})

    def set_active_users(self, count: int, role: str = "all") -> None:
        """Set active user count."""
        self.set_gauge("debvisor_users_active", count, {"role": role})

    def record_session(self, session_type: str = "web") -> None:
        """Record a user session."""
        self.increment("debvisor_user_sessions_total", 1, {"type": session_type})

    def record_dispute(self, reason: str, status: str = "opened") -> None:
        """Record a dispute."""
        self.increment("debvisor_disputes_total", 1, {"reason": reason, "status": status})

    def record_dispute_resolution(self, reason: str, resolution_time_seconds: float) -> None:
        """Record dispute resolution time."""
        self.observe("debvisor_dispute_resolution_seconds",
                     resolution_time_seconds, {"reason": reason})

    def record_communication(
        self,
        channel: str,
        template: str = "default",
        delivered: bool = True
    ) -> None:
        """Record a communication sent."""
        self.increment("debvisor_communications_sent_total", 1, {
                       "channel": channel, "template": template})

    def set_delivery_rate(self, channel: str, rate: float) -> None:
        """Set communication delivery rate."""
        self.set_gauge("debvisor_communication_delivery_rate", rate, {"channel": channel})

    def record_api_request(
        self,
        endpoint: str,
        method: str,
        status: int,
        latency: float
    ) -> None:
        """Record an API request."""
        status_str = str(status)
        self.increment("debvisor_api_requests_total", 1, {
            "endpoint": endpoint,
            "method": method,
            "status": status_str
        })
        self.observe("debvisor_api_latency_seconds", latency, {
            "endpoint": endpoint,
            "method": method
        })

    def record_fee(self, amount: float, fee_type: str) -> None:
        """Record a fee collected."""
        self.increment("debvisor_fees_collected_total", amount, {"fee_type": fee_type})

    def record_compliance_check(self, check_type: str, passed: bool) -> None:
        """Record a compliance check."""
        result = "pass" if passed else "fail"
        self.increment("debvisor_compliance_checks_total", 1, {
                       "check_type": check_type, "result": result})

    def record_regulatory_report(self, report_type: str) -> None:
        """Record a regulatory report generation."""
        self.increment("debvisor_regulatory_reports_generated", 1, {"report_type": report_type})

    # =========================================================================
    # Export Methods
    # =========================================================================

    def to_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []
        metrics_data = self._storage.get_all_metrics()

        # Add help and type comments
        for metric_name, definition in self.METRICS.items():
            lines.append(f"# HELP {metric_name} {definition.description}")
            lines.append(f"# TYPE {metric_name} {definition.type.value}")

        lines.append("")

        # Export counters
        for key, value in metrics_data["counters"].items():
            lines.append(f"{key} {value}")

        # Export gauges
        for key, value in metrics_data["gauges"].items():
            lines.append(f"{key} {value}")

        # Export histograms
        for key, data in metrics_data["histograms"].items():
            base_name = key.split("{")[0] if "{" in key else key
            labels = key[key.index("{"):] if "{" in key else ""

            # Bucket values
            for boundary, count in sorted(data["buckets"].items()):
                bucket_labels = f'le="{boundary}"'
                if labels:
                    full_labels = labels[:-1] + "," + bucket_labels + "}"
                else:
                    full_labels = "{" + bucket_labels + "}"
                lines.append(f"{base_name}_bucket{full_labels} {count}")

            # +Inf bucket
            inf_labels = 'le="+Inf"'
            if labels:
                full_labels = labels[:-1] + "," + inf_labels + "}"
            else:
                full_labels = "{" + inf_labels + "}"
            lines.append(f"{base_name}_bucket{full_labels} {data['count']}")

            # Sum and count
            lines.append(f"{base_name}_sum{labels} {data['sum']}")
            lines.append(f"{base_name}_count{labels} {data['count']}")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Export metrics as dictionary."""
        return self._storage.get_all_metrics()

    def reset(self) -> None:
        """Reset all metrics."""
        self._storage.reset()
        self._label_values_cache.clear()


# =============================================================================
# Decorators
# =============================================================================

def track_latency(
    metric_name: str = "debvisor_api_latency_seconds",
    labels: Optional[Dict[str, str]] = None
) -> Callable[[F], F]:
    """
    Decorator to track function execution latency.

    Args:
        metric_name: Name of the histogram metric
        labels: Additional labels
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                get_metrics().observe(metric_name, duration, labels or {})

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                get_metrics().observe(metric_name, duration, labels or {})

        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


def count_calls(
    metric_name: str,
    labels: Optional[Dict[str, str]] = None,
    count_exceptions: bool = False
) -> Callable[[F], F]:
    """
    Decorator to count function calls.

    Args:
        metric_name: Name of the counter metric
        labels: Additional labels
        count_exceptions: Whether to count exception occurrences
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            call_labels = dict(labels or {})
            try:
                result = func(*args, **kwargs)
                call_labels["status"] = "success"
                return result
            except Exception:
                call_labels["status"] = "error"
                if count_exceptions:
                    get_metrics().increment(metric_name, 1, call_labels)
                raise
            finally:
                if "status" in call_labels and call_labels["status"] == "success":
                    get_metrics().increment(metric_name, 1, call_labels)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            call_labels = dict(labels or {})
            try:
                result = await func(*args, **kwargs)
                call_labels["status"] = "success"
                return result
            except Exception:
                call_labels["status"] = "error"
                if count_exceptions:
                    get_metrics().increment(metric_name, 1, call_labels)
                raise
            finally:
                if "status" in call_labels and call_labels["status"] == "success":
                    get_metrics().increment(metric_name, 1, call_labels)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


# =============================================================================
# Flask Integration
# =============================================================================

def create_metrics_endpoint(metrics: 'BusinessMetrics'):
    """
    Create Flask endpoint for metrics.

    Args:
        metrics: BusinessMetrics instance

    Returns:
        Flask response with Prometheus metrics
    """
    from flask import Response

    def metrics_endpoint():
        return Response(
            metrics.to_prometheus(),
            mimetype="text/plain; charset=utf-8"
        )

    return metrics_endpoint


def create_metrics_middleware(metrics: 'BusinessMetrics'):
    """
    Create Flask middleware for automatic request tracking.

    Args:
        metrics: BusinessMetrics instance

    Returns:
        Tuple of (before_request, after_request) handlers
    """
    from flask import request, g

    def before_request():
        g.request_start_time = time.perf_counter()

    def after_request(response):
        if hasattr(g, 'request_start_time'):
            latency = time.perf_counter() - g.request_start_time
            metrics.record_api_request(
                endpoint=request.endpoint or request.path,
                method=request.method,
                status=response.status_code,
                latency=latency
            )
        return response

    return before_request, after_request


# =============================================================================
# Global Instance
# =============================================================================

_metrics: Optional[BusinessMetrics] = None


def get_metrics() -> BusinessMetrics:
    """Get global metrics instance."""
    global _metrics
    if _metrics is None:
        _metrics = BusinessMetrics()
    return _metrics


def configure_metrics(storage: Optional[MetricStorage] = None) -> BusinessMetrics:
    """Configure global metrics instance."""
    global _metrics
    _metrics = BusinessMetrics(storage)
    return _metrics


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Initialize metrics
    metrics = configure_metrics()

    # Simulate business operations
    print("Recording business metrics...")

    # Debt operations
    metrics.record_debt_created(5000.00, "medical", "import")
    metrics.record_debt_created(2500.00, "credit_card", "api")
    metrics.record_debt_resolved("paid", "medical", 45)
    metrics.record_debt_resolved("settled", "credit_card", 90)

    # Payment operations
    metrics.record_payment(1500.00, "ach", "success", 0.5, "stripe")
    metrics.record_payment(500.00, "card", "success", 0.3, "stripe")
    metrics.record_payment(250.00, "card", "failed", 0.1, "stripe")

    # User operations
    metrics.record_user_registration("web")
    metrics.record_user_registration("api")
    metrics.set_active_users(1250, "consumer")
    metrics.set_active_users(45, "agent")

    # API operations
    metrics.record_api_request("/api/v2/debts", "GET", 200, 0.05)
    metrics.record_api_request("/api/v2/payments", "POST", 201, 0.15)
    metrics.record_api_request("/api/v2/users", "GET", 500, 0.8)

    # Print Prometheus format
    print("\n" + "=" * 60)
    print("PROMETHEUS FORMAT:")
    print("=" * 60)
    print(metrics.to_prometheus())

    # Print dict format
    print("\n" + "=" * 60)
    print("DICTIONARY FORMAT:")
    print("=" * 60)
    import json
    print(json.dumps(metrics.to_dict(), indent=2))
