#!/usr/bin/env python3
"""
Distributed Tracing with OpenTelemetry.

Provides comprehensive tracing instrumentation for DebVisor operations
using the official OpenTelemetry SDK.

Features:
  - Request tracing with correlation IDs
  - Span collection and propagation
  - Integration with Jaeger and Zipkin
  - Performance metrics collection
  - Automatic context propagation
"""

import logging
import os
import time
import uuid
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from functools import wraps

# OpenTelemetry Imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.trace import Status, StatusCode, TraceFlags

# Exporters (conditional import to avoid hard crashes if not installed)
class _MockExporter:
    pass

try:
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter as JaegerExporterClass
    _JaegerExporter: Any = JaegerExporterClass
except ImportError:
    _JaegerExporter = None

try:
    from opentelemetry.exporter.zipkin.json import ZipkinExporter as ZipkinExporterClass
    _ZipkinExporter: Any = ZipkinExporterClass
except ImportError:
    _ZipkinExporter = None

try:
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as _OTLPSpanExporter
    OTLPSpanExporter = _OTLPSpanExporter
except ImportError:
    OTLPSpanExporter = None # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom Exporter Wrappers for Compatibility
if _JaegerExporter: # type: ignore

    class JaegerExporter(_JaegerExporter):
        def __init__(self, agent_host_name="localhost", agent_port=6831, **kwargs):
            super().__init__(
                agent_host_name=agent_host_name, agent_port=agent_port, **kwargs
            )
            self.agent_host = agent_host_name
            self.agent_port = agent_port
            self.traces_buffer = []

        def export_spans(self, spans):
            self.traces_buffer.extend(spans)
            # Simulate batch flushing for tests
            if len(self.traces_buffer) > 100:
                self.traces_buffer = self.traces_buffer[100:]
            return True
else:
    JaegerExporter = None # type: ignore

if _ZipkinExporter: # type: ignore

    class ZipkinExporter(_ZipkinExporter):  # type: ignore
        def __init__(self, endpoint="http://localhost:9411/api/v2/spans", **kwargs):
            super().__init__(endpoint=endpoint, **kwargs)
            self.url = endpoint
            self.traces_buffer = []

        def export_spans(self, spans):
            self.traces_buffer.extend(spans)
            return True
else:
    ZipkinExporter = None # type: ignore


# Initialize Global Tracer Provider
try:
    from opt.core.config import settings

    service_name = settings.SERVICE_NAME
    otlp_endpoint = settings.OTEL_EXPORTER_OTLP_ENDPOINT
    trace_debug = settings.DEBUG
except ImportError:
    service_name = os.getenv("DEBVISOR_SERVICE_NAME", "debvisor-core")
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    trace_debug = os.getenv("DEBVISOR_TRACE_DEBUG", "0") == "1"

resource = Resource(attributes={SERVICE_NAME: service_name})
provider = TracerProvider(resource=resource)

# Configure Exporters based on Environment
if otlp_endpoint:
    if OTLPSpanExporter is not None:
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        logger.info("OTLP exporter configured")
    else:
        logger.warning("OTLP exporter requested but not installed")

if os.getenv("JAEGER_AGENT_HOST"):
    if JaegerExporter is not None:
        jaeger_exporter = JaegerExporter(
            agent_host_name=os.getenv("JAEGER_AGENT_HOST", "localhost"),
            agent_port=int(os.getenv("JAEGER_AGENT_PORT", 6831)),
        )
        provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
        logger.info("Jaeger exporter configured")
    else:
        logger.warning("Jaeger exporter requested but not installed")

if os.getenv("ZIPKIN_COLLECTOR_URL"):
    if ZipkinExporter is not None:
        zipkin_exporter = ZipkinExporter(
            endpoint=os.getenv(
                "ZIPKIN_COLLECTOR_URL", "http://localhost:9411/api/v2/spans"
            )
        )
        provider.add_span_processor(BatchSpanProcessor(zipkin_exporter))
        logger.info("Zipkin exporter configured")
    else:
        logger.warning("Zipkin exporter requested but not installed")

# Always add console exporter for debug if requested
if trace_debug:
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

trace.set_tracer_provider(provider)


class SpanKind(Enum):
    """OpenTelemetry span kinds mapping."""

    INTERNAL = trace.SpanKind.INTERNAL
    SERVER = trace.SpanKind.SERVER
    CLIENT = trace.SpanKind.CLIENT
    PRODUCER = trace.SpanKind.PRODUCER
    CONSUMER = trace.SpanKind.CONSUMER


class SpanStatus(Enum):
    """Span status mapping."""

    UNSET = StatusCode.UNSET
    OK = StatusCode.OK
    ERROR = StatusCode.ERROR


class Event:
    """Span event."""

    def __init__(
        self, name: str, attributes: Optional[Dict[str, Any]] = None, time_val: Optional[float] = None
    ):
        self.name = name
        self.attributes = attributes or {}
        self.time = time_val or time.time()


class Span:
    """
    Custom Span wrapper for compatibility and testing.
    Wraps OpenTelemetry span but provides storage for tests.
    """

    def __init__(
        self,
        trace_id: str,
        span_id: str,
        parent_span_id: Optional[str] = None,
        name: str = "",
        start_time: float = 0.0,
        kind: SpanKind = SpanKind.INTERNAL,
    ):
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_span_id = parent_span_id
        self.name = name
        self.start_time = start_time
        self.kind = kind
        self.end_time: Optional[float] = None
        self.status = SpanStatus.UNSET
        self.attributes: Dict[str, Any] = {}
        self.events: List[Event] = []
        self._otel_span: Any = None

    @property
    def duration_ms(self) -> float:
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value
        if self._otel_span:
            self._otel_span.set_attribute(key, value)

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        event = Event(name, attributes)
        self.events.append(event)
        if self._otel_span:
            self._otel_span.add_event(name, attributes)

    def set_status(self, status: SpanStatus, description: Optional[str] = None) -> None:
        self.status = status
        if self._otel_span:
            otel_status = (
                Status(status.value, description=description)
                if status == SpanStatus.ERROR
                else Status(status.value)
            )
            self._otel_span.set_status(otel_status)

    def end(self, end_time: Optional[float] = None) -> None:
        self.end_time = end_time or time.time()
        if self._otel_span:
            # OTel expects nanoseconds int
            end_time_ns = int(self.end_time * 1e9)
            self._otel_span.end(end_time=end_time_ns)

    def __enter__(self) -> "Span":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_type:
            self.set_status(SpanStatus.ERROR, str(exc_val))
        else:
            self.set_status(SpanStatus.OK)
        self.end()


class TraceContext:
    """Trace context manager."""

    def __init__(self) -> None:
        self._current_span: Optional[Span] = None
        self._trace_id: str = uuid.uuid4().hex

    def set_current_span(self, span: Span) -> None:
        self._current_span = span
        if span:
            self._trace_id = span.trace_id

    def get_current_span(self) -> Optional[Span]:
        return self._current_span

    def get_trace_id(self) -> Optional[str]:
        if self._current_span:
            return self._current_span.trace_id
        return self._trace_id

    def clear(self) -> None:
        self._current_span = None


class Tracer:
    """OpenTelemetry tracer wrapper for DebVisor compatibility."""

    def __init__(self, name: str):
        """
        Initialize tracer.

        Args:
            name: Tracer name (usually service name)
        """
        self.name = name
        self._tracer = trace.get_tracer(name)
        self.context = TraceContext()
        self.spans: List[Span] = []

    def start_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        trace_id: Optional[str] = None,
        parent_span_id: Optional[str] = None,
    ) -> Span:
        """
        Start new span.

        Handles explicit trace_id/parent_span_id for compatibility with
        legacy context propagation.
        """
        context = None
        if trace_id and parent_span_id:
            # Reconstruct context from IDs
            try:
                # OTel expects integers for IDs
                trace_id_int = int(trace_id.replace("-", ""), 16)
                span_id_int = int(parent_span_id.replace("-", ""), 16)

                span_context = trace.SpanContext(
                    trace_id=trace_id_int,
                    span_id=span_id_int,
                    is_remote=True,
                    trace_flags=TraceFlags(TraceFlags.SAMPLED),
                )
                context = trace.set_span_in_context(
                    trace.NonRecordingSpan(span_context)
                )
            except ValueError:
                logger.warning(
                    f"Invalid trace/span ID format: {trace_id}/{parent_span_id}"
                )

        otel_span = self._tracer.start_span(name, kind=kind.value, context=context)

        # Create custom Span wrapper
        span_ctx = otel_span.get_span_context()
        # Handle invalid/empty trace/span IDs (e.g. if no-op tracer)
        t_id = (
            format(span_ctx.trace_id, "032x")
            if span_ctx.trace_id
            else trace_id or uuid.uuid4().hex
        )
        s_id = (
            format(span_ctx.span_id, "016x")
            if span_ctx.span_id
            else uuid.uuid4().hex[:16]
        )

        span = Span(
            trace_id=t_id,
            span_id=s_id,
            parent_span_id=parent_span_id,
            name=name,
            start_time=time.time(),
            kind=kind,
        )
        span._otel_span = otel_span

        self.spans.append(span)
        self.context.set_current_span(span)

        return span

    def end_span(
        self,
        span: Span,
        status: SpanStatus = SpanStatus.OK,
        description: Optional[str] = None,
    ) -> None:
        """
        End span.

        Args:
            span: Span to end
            status: Span status
            description: Status description
        """
        span.set_status(status, description)
        span.end()

    def create_child_span(self, name: str, kind: SpanKind = SpanKind.INTERNAL) -> Span:
        """
        Create child span of current active span.
        """
        parent = self.context.get_current_span()
        parent_id = parent.span_id if parent else None
        trace_id = parent.trace_id if parent else None
        return self.start_span(name, kind, trace_id, parent_id)

    def get_spans(self, trace_id: Optional[str] = None) -> List[Span]:
        """
        Get spans by trace ID.
        """
        if trace_id:
            return [s for s in self.spans if s.trace_id == trace_id]
        return self.spans

    def clear_spans(self) -> None:
        """Clear all spans."""
        self.spans = []
        self.context.clear()


class TracingDecorator:
    """Decorator for automatic tracing."""

    def __init__(self, tracer: Tracer):
        """
        Initialize decorator.

        Args:
            tracer: Tracer instance
        """
        self.tracer = tracer

    def trace(
        self, name: Optional[str] = None, kind: SpanKind = SpanKind.INTERNAL
    ) -> Callable:
        """
        Decorator for function tracing.

        Args:
            name: Span name (uses function name if not provided)
            kind: Span kind

        Returns:
            Decorated function
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                span_name = name or func.__name__

                span = self.tracer.start_span(span_name, kind=kind)
                try:
                    # Add function arguments to span
                    span.set_attribute("function", func.__name__)
                    span.set_attribute("args_count", len(args))
                    span.set_attribute("kwargs_count", len(kwargs))

                    result = func(*args, **kwargs)

                    span.add_event("completed")
                    self.tracer.end_span(span, SpanStatus.OK)
                    return result
                except Exception as e:
                    self.tracer.end_span(span, SpanStatus.ERROR, str(e))
                    span.add_event("exception", {"error": str(e)})
                    raise

            return wrapper

        return decorator

    def trace_async(
        self, name: Optional[str] = None, kind: SpanKind = SpanKind.INTERNAL
    ) -> Callable:
        """
        Decorator for async function tracing.
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                span_name = name or func.__name__

                span = self.tracer.start_span(span_name, kind=kind)
                try:
                    span.set_attribute("function", func.__name__)
                    span.set_attribute("args_count", len(args))
                    span.set_attribute("kwargs_count", len(kwargs))

                    result = await func(*args, **kwargs)

                    span.add_event("completed")
                    self.tracer.end_span(span, SpanStatus.OK)
                    return result
                except Exception as e:
                    self.tracer.end_span(span, SpanStatus.ERROR, str(e))
                    span.add_event("exception", {"error": str(e)})
                    raise

            return wrapper

        return decorator


class TracingMiddleware:
    """Middleware for request tracing."""

    def __init__(self, tracer: Tracer):
        self.tracer = tracer

    def trace_request(self, request_id: Optional[str] = None, name: str = "http_request"):
        if not request_id:
            request_id = str(uuid.uuid4())

        # Start span
        span = self.tracer.start_span(name, trace_id=request_id)

        def cleanup(status_code: int = 200, error: Optional[str] = None):
            status = SpanStatus.OK if status_code < 400 else SpanStatus.ERROR
            self.tracer.end_span(span, status=status, description=error)

        return request_id, cleanup
