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

"""
Prometheus metrics and monitoring integration for DebVisor RPC service.

Exports metrics for:
- RPC call latency (histograms by service/method)
- RPC error rates (counters by service/method/error_type)
- Authentication failures (counters by method)
- Cache hit rates (counters)
- Active connections (gauges)
"""

from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
from contextlib import contextmanager
from typing import Iterator, Tuple, Optional, Type
from types import TracebackType
import time

# Create custom registry for RPC metrics
rpc_registry = CollectorRegistry()

# RPC Call Metrics
rpc_calls_total = Counter(
    "rpc_calls_total",
    "Total number of RPC calls",
    ["service", "method", "status"],
    registry=rpc_registry,
)

rpc_call_duration_seconds = Histogram(
    "rpc_call_duration_seconds",
    "RPC call duration in seconds",
    ["service", "method"],
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0),
    registry=rpc_registry,
)

rpc_call_exceptions = Counter(
    "rpc_call_exceptions_total",
    "Total number of RPC exceptions",
    ["service", "method", "exception_type"],
    registry=rpc_registry,
)

# Authentication Metrics
auth_failures_total = Counter(
    "auth_failures_total",
    "Total authentication failures",
    ["method", "reason"],
    registry=rpc_registry,
)

auth_success_total = Counter(
    "auth_success_total",
    "Total successful authentications",
    ["method"],
    registry=rpc_registry,
)

# Authorization Metrics
authz_failures_total = Counter(
    "authz_failures_total",
    "Total authorization failures",
    ["resource", "action", "role"],
    registry=rpc_registry,
)

authz_successes_total = Counter(
    "authz_successes_total",
    "Total successful authorizations",
    ["resource", "action", "role"],
    registry=rpc_registry,
)

# Active Connections
active_connections = Gauge(
    "rpc_active_connections", "Number of active RPC connections", registry=rpc_registry
)

# Rate Limiting Metrics
rate_limit_exceeded_total = Counter(
    "rate_limit_exceeded_total",
    "Number of rate limit exceeded events",
    ["client_id", "endpoint"],
    registry=rpc_registry,
)

rate_limit_remaining = Gauge(
    "rate_limit_remaining",
    "Remaining rate limit requests for client",
    ["client_id"],
    registry=rpc_registry,
)

# Validation Metrics
validation_failures_total = Counter(
    "validation_failures_total",
    "Total validation failures",
    ["field_type", "error_reason"],
    registry=rpc_registry,
)

# Cache Metrics
cache_hits_total = Counter(
    "cache_hits_total", "Total cache hits", ["cache_name"], registry=rpc_registry
)

cache_misses_total = Counter(
    "cache_misses_total", "Total cache misses", ["cache_name"], registry=rpc_registry
)

cache_evictions_total = Counter(
    "cache_evictions_total",
    "Total cache evictions",
    ["cache_name", "reason"],
    registry=rpc_registry,
)

# TLS Metrics
tls_certificate_expiry_days = Gauge(
    "tls_certificate_expiry_days",
    "Days until TLS certificate expiration",
    ["certificate_name"],
    registry=rpc_registry,
)

tls_handshake_failures_total = Counter(
    "tls_handshake_failures_total",
    "Total TLS handshake failures",
    ["reason"],
    registry=rpc_registry,
)


class MetricsContext:
    """Context manager for tracking RPC metrics."""

    def __init__(self, service: str, method: str) -> None:
        self.service = service
        self.method = method
        self.start_time: float = 0.0
        self.status = "success"

    def __enter__(self) -> "MetricsContext":
        self.start_time = time.time()
        active_connections.inc()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        active_connections.dec()

        duration = time.time() - self.start_time
        rpc_call_duration_seconds.labels(
            service=self.service, method=self.method
        ).observe(duration)

        if exc_type is not None:
            self.status = "error"
            exception_name = exc_type.__name__
            rpc_call_exceptions.labels(
                service=self.service, method=self.method, exception_type=exception_name
            ).inc()

        rpc_calls_total.labels(
            service=self.service, method=self.method, status=self.status
        ).inc()


@contextmanager
def track_rpc_call(service: str, method: str) -> Iterator[None]:
    """Track RPC call metrics."""
    with MetricsContext(service, method):
        yield


def record_auth_success(method: str) -> None:
    """Record successful authentication."""
    auth_success_total.labels(method=method).inc()


def record_auth_failure(method: str, reason: str) -> None:
    """Record authentication failure."""
    auth_failures_total.labels(method=method, reason=reason).inc()


def record_authz_success(resource: str, action: str, role: str) -> None:
    """Record successful authorization."""
    authz_successes_total.labels(resource=resource, action=action, role=role).inc()


def record_authz_failure(resource: str, action: str, role: str) -> None:
    """Record authorization failure."""
    authz_failures_total.labels(resource=resource, action=action, role=role).inc()


def record_validation_failure(field_type: str, error_reason: str) -> None:
    """Record input validation failure."""
    validation_failures_total.labels(
        field_type=field_type, error_reason=error_reason
    ).inc()


def record_rate_limit_exceeded(client_id: str, endpoint: str) -> None:
    """Record rate limit exceeded event."""
    rate_limit_exceeded_total.labels(client_id=client_id, endpoint=endpoint).inc()


def set_rate_limit_remaining(client_id: str, remaining: int) -> None:
    """Set remaining rate limit for client."""
    rate_limit_remaining.labels(client_id=client_id).set(remaining)


def record_cache_hit(cache_name: str) -> None:
    """Record cache hit."""
    cache_hits_total.labels(cache_name=cache_name).inc()


def record_cache_miss(cache_name: str) -> None:
    """Record cache miss."""
    cache_misses_total.labels(cache_name=cache_name).inc()


def record_cache_eviction(cache_name: str, reason: str = "capacity") -> None:
    """Record cache eviction."""
    cache_evictions_total.labels(cache_name=cache_name, reason=reason).inc()


def set_certificate_expiry_days(cert_name: str, days_remaining: int) -> None:
    """Set TLS certificate expiration warning."""
    tls_certificate_expiry_days.labels(certificate_name=cert_name).set(days_remaining)


def record_tls_handshake_failure(reason: str) -> None:
    """Record TLS handshake failure."""
    tls_handshake_failures_total.labels(reason=reason).inc()


def get_metrics() -> Tuple[bytes, str]:
    """Get all metrics for exposition."""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

    return generate_latest(rpc_registry), CONTENT_TYPE_LATEST
