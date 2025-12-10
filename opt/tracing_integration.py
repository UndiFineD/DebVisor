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

"""DebVisor Tracing Integration
============================

Context propagation utilities for distributed tracing integration
with all DebVisor services.

Provides automatic trace context injection/extraction for:
- HTTP requests (Flask middleware)
- gRPC calls
- Message queue operations
- Background tasks
"""

from typing import TypeVar, Optional
import functools
import logging
import uuid
import requests
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generator

# Add project imports with graceful fallback
try:
    from opt.distributed_tracing import (
        Tracer,
        SpanKind,
        SpanStatus,
    )

    _TRACING_AVAILABLE = True
except ImportError:
    _TRACING_AVAILABLE = False


logger = logging.getLogger(__name__)

# =============================================================================
# W3C Trace Context Headers
# =============================================================================

# Standard W3C Trace Context headers
TRACEPARENT_HEADER = "traceparent"
TRACESTATE_HEADER = "tracestate"

# Additional headers for compatibility
X_TRACE_ID_HEADER = "X-Trace-ID"
X_SPAN_ID_HEADER = "X-Span-ID"
X_PARENT_SPAN_ID_HEADER = "X-Parent-Span-ID"
X_REQUEST_ID_HEADER = "X-Request-ID"
X_CORRELATION_ID_HEADER = "X-Correlation-ID"


@dataclass
class TraceHeaders:
    """Trace context headers for propagation."""

    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    trace_state: Optional[str] = None

    def to_headers(self) -> Dict[str, str]:
        """Convert to HTTP headers dict."""
        headers = {
            X_TRACE_ID_HEADER: self.trace_id,
            X_SPAN_ID_HEADER: self.span_id,
            TRACEPARENT_HEADER: self._format_traceparent(),
        }

        if self.parent_span_id:
            headers[X_PARENT_SPAN_ID_HEADER] = self.parent_span_id

        if self.trace_state:
            headers[TRACESTATE_HEADER] = self.trace_state

        return headers

    def _format_traceparent(self) -> str:
        """Format W3C traceparent header."""
        # Format: version-trace_id-span_id-flags
        # Version 00, flags 01 (sampled)
        trace_id_hex = self.trace_id.replace("-", "")[:32].ljust(32, "0")
        span_id_hex = self.span_id.replace("-", "")[:16].ljust(16, "0")
        return f"00-{trace_id_hex}-{span_id_hex}-01"

    @classmethod
    def from_headers(cls, headers: Dict[str, str]) -> Optional["TraceHeaders"]:
        """Extract trace context from HTTP headers."""
        # Try W3C traceparent first
        traceparent = headers.get(TRACEPARENT_HEADER) or headers.get(
            TRACEPARENT_HEADER.lower()
        )
        if traceparent:
            try:
                parts = traceparent.split("-")
                if len(parts) >= 4:
                    return cls(
                        trace_id=parts[1],
                        span_id=parts[2],
                        trace_state=headers.get(TRACESTATE_HEADER),
                    )
            except (IndexError, ValueError):
                pass

        # Fall back to custom headers
        trace_id = (
            headers.get(X_TRACE_ID_HEADER)
            or headers.get(X_REQUEST_ID_HEADER)
            or headers.get(X_CORRELATION_ID_HEADER)
        )

        if trace_id:
            return cls(
                trace_id=trace_id,
                span_id=headers.get(X_SPAN_ID_HEADER, str(uuid.uuid4())[:16]),
                parent_span_id=headers.get(X_PARENT_SPAN_ID_HEADER),
            )

        return None


# =============================================================================
# Global Tracer Management
# =============================================================================

_global_tracer: Optional["Tracer"] = None


def get_tracer(service_name: str = "debvisor") -> Optional["Tracer"]:
    """Get or create the global tracer instance."""
    global _global_tracer

    if not _TRACING_AVAILABLE:
        logger.warning("Distributed tracing not available")
        return None

    if _global_tracer is None:
        _global_tracer = Tracer(service_name)

    return _global_tracer


def set_tracer(tracer: "Tracer") -> None:
    """Set the global tracer instance."""
    global _global_tracer
    _global_tracer = tracer


# =============================================================================
# Context Propagation Utilities
# =============================================================================


def inject_context(headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Inject current trace context into headers for outgoing requests.

    Args:
        headers: Existing headers dict (will be modified in place)

    Returns:
        Headers dict with trace context injected
    """
    headers = headers or {}
    tracer = get_tracer()

    if not tracer:
        # Generate request ID even without tracing
        headers[X_REQUEST_ID_HEADER] = str(uuid.uuid4())
        return headers

    current_span = tracer.context.get_current_span()

    if current_span:
        trace_headers = TraceHeaders(
            trace_id=current_span.trace_id,
            span_id=current_span.span_id,
            parent_span_id=current_span.parent_span_id,
        )
        headers.update(trace_headers.to_headers())
    else:
        # No active span, generate new trace ID
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())[:16]
        headers[X_TRACE_ID_HEADER] = trace_id
        headers[X_SPAN_ID_HEADER] = span_id
        headers[X_REQUEST_ID_HEADER] = trace_id

    return headers


def extract_context(headers: Dict[str, str]) -> Optional[TraceHeaders]:
    """
    Extract trace context from incoming request headers.

    Args:
        headers: Request headers

    Returns:
        TraceHeaders if context found, None otherwise
    """
    return TraceHeaders.from_headers(headers)


@contextmanager
def trace_context(
    operation_name: str,
    kind: "SpanKind" = None,
    headers: Optional[Dict[str, str]] = None,
    attributes: Optional[Dict[str, Any]] = None,
) -> Generator[Any, None, None]:
    """
    Context manager for creating traced operations with automatic context propagation.

    Usage:
        with trace_context("process_request", headers=request.headers) as span:
            # Your code here
            span.set_attribute("key", "value")

    Args:
        operation_name: Name of the operation being traced
        kind: Span kind (defaults to INTERNAL)
        headers: Incoming headers with trace context
        attributes: Initial span attributes

    Yields:
        Span object (or mock object if tracing unavailable)
    """
    tracer = get_tracer()

    if not tracer or not _TRACING_AVAILABLE:
        # Yield a mock span that does nothing
        yield _MockSpan()
        return

    if kind is None:
        kind = SpanKind.INTERNAL

    # Extract parent context from headers
    parent_context = extract_context(headers) if headers else None

    if parent_context:
        span = tracer.start_span(
            operation_name,
            kind=kind,
            trace_id=parent_context.trace_id,
            parent_span_id=parent_context.span_id,
        )
    else:
        span = tracer.create_child_span(operation_name, kind=kind)

    # Add initial attributes
    if attributes:
        for key, value in attributes.items():
            span.set_attribute(key, value)

    try:
        yield span
        tracer.end_span(span, SpanStatus.OK)
    except Exception as e:
        span.add_event("error", {"error": str(e), "type": type(e).__name__})
        tracer.end_span(span, SpanStatus.ERROR, str(e))
        raise


class _MockSpan:
    """Mock span for when tracing is unavailable."""

    def set_attribute(self, key: str, value: Any) -> None:
        pass

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        pass


# =============================================================================
# Decorators for Service Functions
# =============================================================================

F = TypeVar("F", bound=Callable[..., Any])


def traced(
    name: Optional[str] = None,
    kind: "SpanKind" = None,
    record_args: bool = False,
) -> Callable[[F], F]:
    """
    Decorator for tracing synchronous functions.

    Args:
        name: Span name (defaults to function name)
        kind: Span kind
        record_args: Whether to record function arguments as attributes

    Usage:
        @traced("my_operation")
        def my_function(arg1, arg2):
            ...
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            span_name = name or func.__name__
            tracer = get_tracer()

            if not tracer or not _TRACING_AVAILABLE:
                return func(*args, **kwargs)

            span_kind = kind or SpanKind.INTERNAL
            span = tracer.create_child_span(span_name, kind=span_kind)

            try:
                span.set_attribute("function", func.__name__)
                span.set_attribute("module", func.__module__)

                if record_args:
                    span.set_attribute("args_count", len(args))
                    span.set_attribute("kwargs_keys", list(kwargs.keys()))

                result = func(*args, **kwargs)

                tracer.end_span(span, SpanStatus.OK)
                return result

            except Exception as e:
                span.add_event("error", {"error": str(e), "type": type(e).__name__})
                tracer.end_span(span, SpanStatus.ERROR, str(e))
                raise

        return wrapper    # type: ignore

    return decorator


def traced_async(
    name: Optional[str] = None,
    kind: "SpanKind" = None,
    record_args: bool = False,
) -> Callable[[F], F]:
    """
    Decorator for tracing async functions.

    Args:
        name: Span name (defaults to function name)
        kind: Span kind
        record_args: Whether to record function arguments as attributes

    Usage:
        @traced_async("my_async_operation")
        async def my_async_function(arg1, arg2):
            ...
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            span_name = name or func.__name__
            tracer = get_tracer()

            if not tracer or not _TRACING_AVAILABLE:
                return await func(*args, **kwargs)

            span_kind = kind or SpanKind.INTERNAL
            span = tracer.create_child_span(span_name, kind=span_kind)

            try:
                span.set_attribute("function", func.__name__)
                span.set_attribute("module", func.__module__)
                span.set_attribute("async", True)

                if record_args:
                    span.set_attribute("args_count", len(args))
                    span.set_attribute("kwargs_keys", list(kwargs.keys()))

                result = await func(*args, **kwargs)

                tracer.end_span(span, SpanStatus.OK)
                return result

            except Exception as e:
                span.add_event("error", {"error": str(e), "type": type(e).__name__})
                tracer.end_span(span, SpanStatus.ERROR, str(e))
                raise

        return wrapper    # type: ignore

    return decorator


# =============================================================================
# Flask Middleware Integration
# =============================================================================


def create_flask_middleware(app: Any) -> None:
    """
    Create Flask middleware for automatic request tracing.

    Usage:
        from flask import Flask
        from opt.tracing_integration import create_flask_middleware

        app = Flask(__name__)
        create_flask_middleware(app)

    Args:
        app: Flask application instance
    """
    from flask import request, g

    @app.before_request
    def before_request() -> None:
        tracer = get_tracer()
        if not tracer:
            return

        # Extract trace context from request headers
        headers = dict(request.headers)
        parent_context = extract_context(headers)

        # Create span for the request
        if parent_context:
            span = tracer.start_span(
                f"{request.method} {request.path}",
                kind=SpanKind.SERVER,
                trace_id=parent_context.trace_id,
                parent_span_id=parent_context.span_id,
            )
        else:
            span = tracer.start_span(
                f"{request.method} {request.path}",
                kind=SpanKind.SERVER,
            )

        # Add request attributes
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", request.url)
        span.set_attribute("http.path", request.path)
        span.set_attribute("http.host", request.host)
        span.set_attribute("http.user_agent", request.user_agent.string)

        if request.content_length:
            span.set_attribute("http.request_content_length", request.content_length)

        # Store span in Flask g object
        g.trace_span = span
        g.trace_id = span.trace_id

    @app.after_request
    def after_request(response: Any) -> Any:
        tracer = get_tracer()
        span = getattr(g, "trace_span", None)

        if span and tracer:
            span.set_attribute("http.status_code", response.status_code)
            span.set_attribute(
                "http.response_content_length", response.content_length or 0
            )

            # Add trace ID to response headers
            response.headers[X_TRACE_ID_HEADER] = span.trace_id
            response.headers[X_REQUEST_ID_HEADER] = span.trace_id

            if response.status_code >= 400:
                tracer.end_span(span, SpanStatus.ERROR, f"HTTP {response.status_code}")
            else:
                tracer.end_span(span, SpanStatus.OK)

        return response

    @app.teardown_request
    def teardown_request(exception: Optional[Exception]) -> None:
        tracer = get_tracer()
        span = getattr(g, "trace_span", None)

        if span and tracer and exception:
            span.add_event(
                "exception",
                {
                    "type": type(exception).__name__,
                    "message": str(exception),
                },
            )
            tracer.end_span(span, SpanStatus.ERROR, str(exception))


# =============================================================================
# HTTP Client Integration
# =============================================================================


def traced_request(method: str, url: str, **kwargs) -> Any:
    """
    Make an HTTP request with automatic trace context propagation.

    Wrapper around requests library that injects trace headers.

    Args:
        method: HTTP method (GET, POST, etc.)
        url: Request URL
        **kwargs: Additional arguments passed to requests

    Returns:
        Response object
    """

    # Get or create headers
    headers = kwargs.pop("headers", {})

    # Inject trace context
    headers = inject_context(headers)

    tracer = get_tracer()

    if tracer and _TRACING_AVAILABLE:
        span = tracer.create_child_span(f"HTTP {method} {url}", kind=SpanKind.CLIENT)
        span.set_attribute("http.method", method)
        span.set_attribute("http.url", url)

        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            span.set_attribute("http.status_code", response.status_code)

            if response.status_code >= 400:
                tracer.end_span(span, SpanStatus.ERROR, f"HTTP {response.status_code}")
            else:
                tracer.end_span(span, SpanStatus.OK)

            return response

        except Exception as e:
            span.add_event("error", {"error": str(e)})
            tracer.end_span(span, SpanStatus.ERROR, str(e))
            raise
    else:
        return requests.request(method, url, headers=headers, **kwargs)


async def traced_request_async(method: str, url: str, **kwargs) -> Any:
    """
    Make an async HTTP request with automatic trace context propagation.

    Wrapper around aiohttp that injects trace headers.

    Args:
        method: HTTP method (GET, POST, etc.)
        url: Request URL
        **kwargs: Additional arguments passed to aiohttp

    Returns:
        Response object
    """
    import aiohttp

    # Get or create headers
    headers = kwargs.pop("headers", {})
    headers = inject_context(headers)

    tracer = get_tracer()

    async with aiohttp.ClientSession() as session:
        if tracer and _TRACING_AVAILABLE:
            span = tracer.create_child_span(
                f"HTTP {method} {url}", kind=SpanKind.CLIENT
            )
            span.set_attribute("http.method", method)
            span.set_attribute("http.url", url)

            try:
                async with session.request(
                    method, url, headers=headers, **kwargs
                ) as response:
                    span.set_attribute("http.status_code", response.status)

                    if response.status >= 400:
                        tracer.end_span(
                            span, SpanStatus.ERROR, f"HTTP {response.status}"
                        )
                    else:
                        tracer.end_span(span, SpanStatus.OK)

                    return response

            except Exception as e:
                span.add_event("error", {"error": str(e)})
                tracer.end_span(span, SpanStatus.ERROR, str(e))
                raise
        else:
            async with session.request(
                method, url, headers=headers, **kwargs
            ) as response:
                return response


# =============================================================================
# Correlation ID Helper
# =============================================================================


def get_correlation_id() -> str:
    """
    Get the current correlation/trace ID for logging.

    Returns:
        Current trace ID or generated UUID
    """
    tracer = get_tracer()

    if tracer and _TRACING_AVAILABLE:
        current_span = tracer.context.get_current_span()
        if current_span:
            return current_span.trace_id

    return str(uuid.uuid4())


def with_correlation_id(logger_instance: logging.Logger) -> logging.LoggerAdapter[Any]:
    """
    Create a logger adapter that includes correlation ID in all log messages.

    Usage:
        logger = with_correlation_id(logging.getLogger(__name__))
        logger.info("Processing request")    # Will include trace_id in extra

    Args:
        logger_instance: Base logger

    Returns:
        LoggerAdapter with correlation ID
    """

    class CorrelationAdapter(logging.LoggerAdapter[Any]):
        def process(self, msg, kwargs):
            correlation_id = get_correlation_id()
            kwargs.setdefault("extra", {})
            kwargs["extra"]["correlation_id"] = correlation_id
            kwargs["extra"]["trace_id"] = correlation_id
            return f"[{correlation_id[:8]}] {msg}", kwargs

    return CorrelationAdapter(logger_instance, {})


# =============================================================================
# Flask Integration
# =============================================================================


class FlaskTracingMiddleware:
    """
    Flask middleware for automatic request tracing.
    """

    def __init__(self, app: Optional[Any] = None) -> None:
        if app:
            self.init_app(app)

    def init_app(self, app: Any) -> None:
        from flask import request, g

        @app.before_request
        def start_trace() -> None:
            tracer = get_tracer()
            if not tracer or not _TRACING_AVAILABLE:
                return

            # Extract context from headers
            headers = dict(request.headers)
            trace_context = extract_context(headers)

            trace_id = trace_context.trace_id if trace_context else None
            parent_span_id = trace_context.span_id if trace_context else None

            span_name = f"{request.method} {request.path}"

            span = tracer.start_span(
                span_name,
                kind=SpanKind.SERVER,
                trace_id=trace_id,
                parent_span_id=parent_span_id,
            )

            span.set_attribute("http.method", request.method)
            span.set_attribute("http.url", request.url)
            span.set_attribute("http.user_agent", request.headers.get("User-Agent", ""))

            # Store span in g for access in after_request
            g.trace_span = span

        @app.after_request
        def end_trace(response: Any) -> Any:
            span = getattr(g, "trace_span", None)
            if span:
                span.set_attribute("http.status_code", response.status_code)

                status = SpanStatus.OK
                if response.status_code >= 500:
                    status = SpanStatus.ERROR

                tracer = get_tracer()
                if tracer:
                    tracer.end_span(span, status)

            return response

        @app.teardown_request
        def handle_exception(exception: Optional[Exception] = None) -> None:
            span = getattr(g, "trace_span", None)
            if span and exception:
                span.add_event("exception", {"error": str(exception)})
                tracer = get_tracer()
                if tracer:
                    tracer.end_span(span, SpanStatus.ERROR, str(exception))
