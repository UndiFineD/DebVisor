#!/usr/bin/env python3
"""
Distributed Tracing with OpenTelemetry.

Provides comprehensive tracing instrumentation for DebVisor operations.

Features:
  - Request tracing with correlation IDs
  - Span collection and propagation
  - Integration with Jaeger and Zipkin
  - Performance metrics collection
  - Automatic context propagation
"""

import json
import logging
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from functools import wraps
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpanKind(Enum):
    """OpenTelemetry span kinds."""
    INTERNAL = "INTERNAL"
    SERVER = "SERVER"
    CLIENT = "CLIENT"
    PRODUCER = "PRODUCER"
    CONSUMER = "CONSUMER"


class SpanStatus(Enum):
    """Span status."""
    UNSET = "UNSET"
    OK = "OK"
    ERROR = "ERROR"


@dataclass
class SpanContext:
    """OpenTelemetry span context."""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    trace_state: Dict[str, str] = field(default_factory=dict)
    is_remote: bool = False


@dataclass
class Event:
    """Span event."""
    name: str
    timestamp: float
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Link:
    """Span link."""
    context: SpanContext
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Span:
    """OpenTelemetry span."""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: float
    end_time: Optional[float] = None
    kind: SpanKind = SpanKind.INTERNAL
    status: SpanStatus = SpanStatus.UNSET
    status_description: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Event] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        """Get span duration in milliseconds."""
        if not self.end_time:
            return 0
        return (self.end_time - self.start_time) * 1000

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """
        Add event to span.

        Args:
            name: Event name
            attributes: Event attributes
        """
        event = Event(
            name=name,
            timestamp=time.time(),
            attributes=attributes or {}
        )
        self.events.append(event)

    def set_attribute(self, key: str, value: Any) -> None:
        """
        Set span attribute.

        Args:
            key: Attribute key
            value: Attribute value
        """
        self.attributes[key] = value

    def end(self) -> None:
        """End span."""
        if not self.end_time:
            self.end_time = time.time()


class TraceContext:
    """Thread-local trace context."""

    def __init__(self):
        """Initialize trace context."""
        self._local = threading.local()

    def get_current_span(self) -> Optional[Span]:
        """Get current active span."""
        return getattr(self._local, "span", None)

    def set_current_span(self, span: Span) -> None:
        """Set current active span."""
        self._local.span = span

    def get_trace_id(self) -> str:
        """Get current trace ID."""
        span = self.get_current_span()
        if span:
            return span.trace_id
        return str(uuid.uuid4())

    def clear(self) -> None:
        """Clear trace context."""
        self._local.span = None


class Tracer:
    """OpenTelemetry tracer implementation."""

    def __init__(self, name: str):
        """
        Initialize tracer.

        Args:
            name: Tracer name (usually service name)
        """
        self.name = name
        self.spans: List[Span] = []
        self.context = TraceContext()

    def start_span(self, name: str, kind: SpanKind = SpanKind.INTERNAL,
                  trace_id: Optional[str] = None,
                  parent_span_id: Optional[str] = None) -> Span:
        """
        Start new span.

        Args:
            name: Span name
            kind: Span kind
            trace_id: Trace ID (generates if not provided)
            parent_span_id: Parent span ID

        Returns:
            Created span
        """
        if not trace_id:
            trace_id = str(uuid.uuid4())

        span_id = str(uuid.uuid4())

        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=name,
            start_time=time.time(),
            kind=kind
        )

        self.spans.append(span)
        self.context.set_current_span(span)

        logger.info(f"Started span: {name} ({span_id})")

        return span

    def end_span(self, span: Span, status: SpanStatus = SpanStatus.OK,
                description: Optional[str] = None) -> None:
        """
        End span.

        Args:
            span: Span to end
            status: Span status
            description: Status description
        """
        span.end()
        span.status = status
        span.status_description = description

        logger.info(f"Ended span: {span.name} ({span.span_id}) - {span.duration_ms:.2f}ms")

    def create_child_span(self, name: str, kind: SpanKind = SpanKind.INTERNAL) -> Span:
        """
        Create child span of current active span.

        Args:
            name: Span name
            kind: Span kind

        Returns:
            Created child span
        """
        parent_span = self.context.get_current_span()
        trace_id = parent_span.trace_id if parent_span else str(uuid.uuid4())
        parent_span_id = parent_span.span_id if parent_span else None

        child_span = self.start_span(
            name,
            kind=kind,
            trace_id=trace_id,
            parent_span_id=parent_span_id
        )

        return child_span

    def get_spans(self, trace_id: Optional[str] = None) -> List[Span]:
        """
        Get spans by trace ID.

        Args:
            trace_id: Trace ID filter

        Returns:
            List of spans
        """
        if not trace_id:
            return self.spans

        return [s for s in self.spans if s.trace_id == trace_id]

    def clear_spans(self) -> None:
        """Clear all spans."""
        self.spans.clear()


class TracingDecorator:
    """Decorator for automatic tracing."""

    def __init__(self, tracer: Tracer):
        """
        Initialize decorator.

        Args:
            tracer: Tracer instance
        """
        self.tracer = tracer

    def trace(self, name: Optional[str] = None, kind: SpanKind = SpanKind.INTERNAL) -> Callable:
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
                span = self.tracer.create_child_span(span_name, kind=kind)

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
                    span.add_event("error", {"error": str(e)})
                    self.tracer.end_span(span, SpanStatus.ERROR, str(e))
                    raise

            return wrapper

        return decorator

    def trace_async(self, name: Optional[str] = None, kind: SpanKind = SpanKind.INTERNAL) -> Callable:
        """
        Decorator for async function tracing.

        Args:
            name: Span name
            kind: Span kind

        Returns:
            Decorated async function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                span_name = name or func.__name__
                span = self.tracer.create_child_span(span_name, kind=kind)

                try:
                    span.set_attribute("function", func.__name__)
                    span.set_attribute("async", True)

                    result = await func(*args, **kwargs)

                    span.add_event("completed")
                    self.tracer.end_span(span, SpanStatus.OK)

                    return result

                except Exception as e:
                    span.add_event("error", {"error": str(e)})
                    self.tracer.end_span(span, SpanStatus.ERROR, str(e))
                    raise

            return wrapper

        return decorator


class JaegerExporter:
    """Export traces to Jaeger."""

    def __init__(self, agent_host: str = "localhost", agent_port: int = 6831):
        """
        Initialize Jaeger exporter.

        Args:
            agent_host: Jaeger agent host
            agent_port: Jaeger agent port
        """
        self.agent_host = agent_host
        self.agent_port = agent_port
        self.batch_size = 100
        self.traces_buffer: List[Span] = []

    def export_spans(self, spans: List[Span]) -> bool:
        """
        Export spans to Jaeger.

        Args:
            spans: Spans to export

        Returns:
            Success status
        """
        self.traces_buffer.extend(spans)

        if len(self.traces_buffer) >= self.batch_size:
            return self._flush()

        return True

    def _flush(self) -> bool:
        """Flush buffered spans to Jaeger."""
        if not self.traces_buffer:
            return True

        try:
            # In production, would use jaeger_client library
            logger.info(f"Exporting {len(self.traces_buffer)} spans to Jaeger")

            spans_data = []
            for span in self.traces_buffer:
                spans_data.append(asdict(span))

            logger.debug(f"Exported data: {json.dumps(spans_data[:1], default=str)}")

            self.traces_buffer.clear()
            return True

        except Exception as e:
            logger.error(f"Failed to export spans to Jaeger: {e}")
            return False


class ZipkinExporter:
    """Export traces to Zipkin."""

    def __init__(self, url: str = "http://localhost:9411"):
        """
        Initialize Zipkin exporter.

        Args:
            url: Zipkin server URL
        """
        self.url = url
        self.batch_size = 100
        self.traces_buffer: List[Span] = []

    def export_spans(self, spans: List[Span]) -> bool:
        """
        Export spans to Zipkin.

        Args:
            spans: Spans to export

        Returns:
            Success status
        """
        self.traces_buffer.extend(spans)

        if len(self.traces_buffer) >= self.batch_size:
            return self._flush()

        return True

    def _flush(self) -> bool:
        """Flush buffered spans to Zipkin."""
        if not self.traces_buffer:
            return True

        try:
            # In production, would make HTTP request to Zipkin API
            logger.info(f"Exporting {len(self.traces_buffer)} spans to Zipkin")

            # Convert spans to Zipkin format
            zipkin_spans = []
            for span in self.traces_buffer:
                zipkin_span = {
                    "traceId": span.trace_id,
                    "id": span.span_id,
                    "parentId": span.parent_span_id,
                    "name": span.name,
                    "timestamp": int(span.start_time * 1000000),
                    "duration": int(span.duration_ms * 1000),
                    "kind": span.kind.value,
                    "tags": span.attributes
                }
                zipkin_spans.append(zipkin_span)

            logger.debug(f"Exported {len(zipkin_spans)} Zipkin spans")

            self.traces_buffer.clear()
            return True

        except Exception as e:
            logger.error(f"Failed to export spans to Zipkin: {e}")
            return False


class TracingMiddleware:
    """Middleware for automatic request tracing."""

    def __init__(self, tracer: Tracer):
        """
        Initialize tracing middleware.

        Args:
            tracer: Tracer instance
        """
        self.tracer = tracer

    def trace_request(self, request_id: Optional[str] = None,
                     operation: str = "request") -> tuple[str, Callable]:
        """
        Trace HTTP request.

        Args:
            request_id: Request ID (generates if not provided)
            operation: Operation name

        Returns:
            Tuple of (trace_id, cleanup_function)
        """
        if not request_id:
            request_id = str(uuid.uuid4())

        span = self.tracer.start_span(
            operation,
            kind=SpanKind.SERVER,
            trace_id=request_id
        )

        def cleanup(status_code: int = 200, error: Optional[str] = None) -> None:
            """Cleanup span after request."""
            span.set_attribute("http.status_code", status_code)

            if error:
                self.tracer.end_span(span, SpanStatus.ERROR, error)
            else:
                self.tracer.end_span(span, SpanStatus.OK)

        return request_id, cleanup


# Example usage
if __name__ == "__main__":
    # Create tracer
    tracer = Tracer("debvisor")
    decorator = TracingDecorator(tracer)

    # Example traced function
    @decorator.trace("process_cluster_operation")
    def process_operation(cluster_name: str, operation: str) -> Dict[str, Any]:
        """Process cluster operation."""
        span = tracer.context.get_current_span()

        span.set_attribute("cluster", cluster_name)
        span.set_attribute("operation", operation)

        # Simulate nested operation
        child_span = tracer.create_child_span("validate_cluster")
        child_span.set_attribute("cluster", cluster_name)
        time.sleep(0.1)
        child_span.add_event("validation_complete")
        tracer.end_span(child_span, SpanStatus.OK)

        time.sleep(0.2)

        return {
            "cluster": cluster_name,
            "operation": operation,
            "status": "completed"
        }

    # Execute traced function
    result = process_operation("prod-cluster-1", "scale_deployment")
    print(f"Result: {result}")

    # Get trace
    trace_id = tracer.spans[0].trace_id if tracer.spans else None
    print(f"\nTrace ID: {trace_id}")
    print(f"Spans in trace:")

    for span in tracer.get_spans(trace_id):
        print(f"  - {span.name} ({span.span_id}): {span.duration_ms:.2f}ms")
        if span.events:
            for event in span.events:
                print(f"    -> {event.name}")

    # Export to Jaeger
    jaeger_exporter = JaegerExporter()
    jaeger_exporter.export_spans(tracer.get_spans(trace_id))

    # Export to Zipkin
    zipkin_exporter = ZipkinExporter()
    zipkin_exporter.export_spans(tracer.get_spans(trace_id))
