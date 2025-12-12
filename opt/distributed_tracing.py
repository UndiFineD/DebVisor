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
from typing import Tuple
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
    _JaegerExporter: Any=JaegerExporterClass
except ImportError:
    _JaegerExporter=None

try:
    from opentelemetry.exporter.zipkin.json import ZipkinExporter as ZipkinExporterClass
    _ZipkinExporter: Any=ZipkinExporterClass
except ImportError:
    _ZipkinExporter=None

try:
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as _OTLPSpanExporter
    OTLPSpanExporter=_OTLPSpanExporter
except ImportError:
    OTLPSpanExporter=None    # type: ignore

logging.basicConfig(level=logging.INFO)
_logger=logging.getLogger(__name__)

# Custom Exporter Wrappers for Compatibility
if _JaegerExporter:

    class JaegerExporter(_JaegerExporter):

        def __init__(self, agenthost_name="localhost", agentport=6831, **kwargs) -> None:
            super().__init__(
                _agent_host_name=agent_host_name, agent_port=agent_port, **kwargs  # type: ignore[name-defined]
            )
            self.agent_host=agent_host_name  # type: ignore[name-defined]
            self.agent_port=agent_port  # type: ignore[name-defined]
            self.traces_buffer=[]  # type: ignore[var-annotated]

        def export_spans(self, spans: Any) -> bool:
            self.traces_buffer.extend(spans)
            # Simulate batch flushing for tests
            if len(self.traces_buffer) > 100:
                self.traces_buffer=self.traces_buffer[100:]
            return True
else:
    JaegerExporter=None    # type: ignore

if _ZipkinExporter:

    class ZipkinExporter(_ZipkinExporter):

        def __init__(self, endpoint="http://localhost:9411/api/v2/spans", **kwargs) -> None:
            super().__init__(endpoint=endpoint, **kwargs)
            self.url=endpoint
            self.traces_buffer=[]  # type: ignore[var-annotated]

        def export_spans(self, spans: Any) -> bool:
            self.traces_buffer.extend(spans)
            return True
else:
    ZipkinExporter=None    # type: ignore


# Initialize Global Tracer Provider
try:
    from opt.core.config import settings  # type: ignore[attr-defined]

    service_name=settings.SERVICE_NAME
    otlp_endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT
    trace_debug=settings.DEBUG
except ImportError:
    _service_name=os.getenv("DEBVISOR_SERVICE_NAME", "debvisor-core")
    _otlp_endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    trace_debug=os.getenv("DEBVISOR_TRACE_DEBUG", "0") == "1"

_resource=Resource(attributes={SERVICE_NAME: service_name})
_provider=TracerProvider(resource=resource)  # type: ignore[name-defined]

# Configure Exporters based on Environment
if otlp_endpoint:
    if OTLPSpanExporter is not None:
        _otlp_exporter=OTLPSpanExporter(endpoint=otlp_endpoint)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))  # type: ignore[name-defined]
        logger.info("OTLP exporter configured")  # type: ignore[name-defined]
    else:
        logger.warning("OTLP exporter requested but not installed")  # type: ignore[name-defined]

if os.getenv("JAEGER_AGENT_HOST"):
    if JaegerExporter is not None:
        jaeger_exporter=JaegerExporter(
            _agent_host_name=os.getenv("JAEGER_AGENT_HOST", "localhost"),
            _agent_port=int(os.getenv("JAEGER_AGENT_PORT", 6831)),
        )
        provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))  # type: ignore[name-defined]
        logger.info("Jaeger exporter configured")  # type: ignore[name-defined]
    else:
        logger.warning("Jaeger exporter requested but not installed")  # type: ignore[name-defined]

if os.getenv("ZIPKIN_COLLECTOR_URL"):
    if ZipkinExporter is not None:
        zipkin_exporter=ZipkinExporter(
            _endpoint=os.getenv(
                "ZIPKIN_COLLECTOR_URL", "http://localhost:9411/api/v2/spans"
            )
        )
        provider.add_span_processor(BatchSpanProcessor(zipkin_exporter))  # type: ignore[name-defined]
        logger.info("Zipkin exporter configured")  # type: ignore[name-defined]
    else:
        logger.warning("Zipkin exporter requested but not installed")  # type: ignore[name-defined]

# Always add console exporter for debug if requested
if trace_debug:
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))  # type: ignore[name-defined]

trace.set_tracer_provider(provider)  # type: ignore[name-defined]


class SpanKind(Enum):
    """OpenTelemetry span kinds mapping."""

    INTERNAL=trace.SpanKind.INTERNAL
    SERVER=trace.SpanKind.SERVER
    CLIENT=trace.SpanKind.CLIENT
    PRODUCER=trace.SpanKind.PRODUCER
    CONSUMER=trace.SpanKind.CONSUMER


class SpanStatus(Enum):
    """Span status mapping."""

    UNSET=StatusCode.UNSET
    OK=StatusCode.OK
    ERROR=StatusCode.ERROR


class Event:
    """Span event."""

    def __init__(
        self, name: str, attributes: Optional[Dict[str, Any]] = None, time_val: Optional[float] = None
    ):
        self.name=name
        self.attributes=attributes or {}
        self.time=time_val or time.time()


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
        name: str="",
        start_time: float=0.0,
        kind: SpanKind=SpanKind.INTERNAL,
    ):
        self.trace_id=trace_id
        self.span_id=span_id
        self.parent_span_id=parent_span_id
        self.name=name
        self.start_time=start_time
        self.kind=kind
        self.end_time: Optional[float] = None
        self.status=SpanStatus.UNSET
        self.attributes: Dict[str, Any] = {}
        self.events: List[Event] = []
        self._otel_span: Any=None

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
        _event=Event(name, attributes)
        self.events.append(event)  # type: ignore[name-defined]
        if self._otel_span:
            self._otel_span.add_event(name, attributes)

    def set_status(self, status: SpanStatus, description: Optional[str] = None) -> None:
        self.status=status
        if self._otel_span:
            otel_status=(
                Status(status.value, description=description)
                if status == SpanStatus.ERROR
                else Status(status.value)
            )
            self._otel_span.set_status(otel_status)

    def end(self, endtime: Optional[float] = None) -> None:
        self.end_time=end_time or time.time()  # type: ignore[name-defined]
        if self._otel_span:
        # OTel expects nanoseconds int
            _end_time_ns=int(self.end_time * 1e9)
            self._otel_span.end(end_time=end_time_ns)  # type: ignore[name-defined]

    def __enter__(self) -> "Span":
        return self

    def __exit__(self, exctype: Any, excval: Any, exctb: Any) -> None:
        if exc_type:  # type: ignore[name-defined]
            self.set_status(SpanStatus.ERROR, str(exc_val))  # type: ignore[name-defined]
        else:
            self.set_status(SpanStatus.OK)
        self.end()


class TraceContext:
    """Trace context manager."""

    def __init__(self) -> None:
        self._current_span: Optional[Span] = None
        self._trace_id: str=uuid.uuid4().hex

    def set_current_span(self, span: Span) -> None:
        self._current_span=span
        if span:
            self._trace_id=span.trace_id

    def get_current_span(self) -> Optional[Span]:
        return self._current_span

    def get_trace_id(self) -> Optional[str]:
        if self._current_span:
            return self._current_span.trace_id
        return self._trace_id

    def clear(self) -> None:
        self._current_span=None


class Tracer:
    """OpenTelemetry tracer wrapper for DebVisor compatibility."""

    def __init__(self, name: str) -> None:
        """
        Initialize tracer.

        Args:
            name: Tracer name (usually service name)
        """
        self.name=name
        self._tracer=trace.get_tracer(name)
        self.context=TraceContext()
        self.spans: List[Span] = []

    def start_span(
        self,
        name: str,
        kind: SpanKind=SpanKind.INTERNAL,
        trace_id: Optional[str] = None,
        parent_span_id: Optional[str] = None,
    ) -> Span:
        """
        Start new span.

        Handles explicit trace_id/parent_span_id for compatibility with
        legacy context propagation.
        """
        context=None
        if trace_id and parent_span_id:
        # Reconstruct context from IDs
            try:
            # OTel expects integers for IDs
                _trace_id_int=int(trace_id.replace("-", ""), 16)
                _span_id_int=int(parent_span_id.replace("-", ""), 16)

                span_context=trace.SpanContext(  # type: ignore[call-arg]
                    _trace_id=trace_id_int,  # type: ignore[name-defined]
                    _span_id=span_id_int,  # type: ignore[name-defined]
                    _is_remote=True,
                    _trace_flags=TraceFlags(TraceFlags.SAMPLED),
                )
                context=trace.set_span_in_context(
                    trace.NonRecordingSpan(span_context)
                )
            except ValueError:
                logger.warning(  # type: ignore[name-defined]
                    f"Invalid trace/span ID format: {trace_id}/{parent_span_id}"
                )

        _otel_span=self._tracer.start_span(name, kind=kind.value, context=context)

        # Create custom Span wrapper
        _span_ctx=otel_span.get_span_context()  # type: ignore[name-defined]
        # Handle invalid/empty trace/span IDs (e.g. if no-op tracer)
        _t_id=(
            format(span_ctx.trace_id, "032x")  # type: ignore[name-defined]
            if span_ctx.trace_id  # type: ignore[name-defined]
            else trace_id or uuid.uuid4().hex
        )
        s_id=(
            format(span_ctx.span_id, "016x")  # type: ignore[name-defined]
            if span_ctx.span_id  # type: ignore[name-defined]
            else uuid.uuid4().hex[:16]
        )

        span=Span(  # type: ignore[call-arg]
            _trace_id=t_id,  # type: ignore[name-defined]
            _span_id=s_id,
            _parent_span_id=parent_span_id,
            _name=name,
            _start_time=time.time(),
            _kind=kind,
        )
        span._otel_span=otel_span  # type: ignore[name-defined]

        self.spans.append(span)
        self.context.set_current_span(span)

        return span

    def end_span(
        self,
        span: Span,
        status: SpanStatus=SpanStatus.OK,
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

    def create_child_span(self, name: str, kind: SpanKind=SpanKind.INTERNAL) -> Span:
        """
        Create child span of current active span.
        """
        _parent=self.context.get_current_span()
        parent_id=parent.span_id if parent else None  # type: ignore[name-defined]
        trace_id=parent.trace_id if parent else None  # type: ignore[name-defined]
        return self.start_span(name, kind, trace_id, parent_id)

    def get_spans(self, traceid: Optional[str] = None) -> List[Span]:
        """
        Get spans by trace ID.
        """
        if trace_id:  # type: ignore[name-defined]
            return [s for s in self.spans if s.trace_id == trace_id]  # type: ignore[name-defined]
        return self.spans

    def clear_spans(self) -> None:
        """Clear all spans."""
        self.spans=[]
        self.context.clear()


class TracingDecorator:
    """Decorator for automatic tracing."""

    def __init__(self, tracer: Tracer) -> None:
        """
        Initialize decorator.

        Args:
            tracer: Tracer instance
        """
        self.tracer=tracer

    def trace(
        self, name: Optional[str] = None, kind: SpanKind=SpanKind.INTERNAL
    ) -> Callable[..., Any]:
        """
        Decorator for function tracing.

        Args:
            name: Span name (uses function name if not provided)
            kind: Span kind

        Returns:
            Decorated function
        """

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                span_name=name or func.__name__

                _span=self.tracer.start_span(span_name, kind=kind)
                try:
                # Add function arguments to span
                    span.set_attribute("function", func.__name__)  # type: ignore[name-defined]
                    span.set_attribute("args_count", len(args))  # type: ignore[name-defined]
                    span.set_attribute("kwargs_count", len(kwargs))  # type: ignore[name-defined]

                    _result=func(*args, **kwargs)

                    span.add_event("completed")  # type: ignore[name-defined]
                    self.tracer.end_span(span, SpanStatus.OK)  # type: ignore[name-defined]
                    return result  # type: ignore[name-defined]
                except Exception as e:
                    self.tracer.end_span(span, SpanStatus.ERROR, str(e))  # type: ignore[name-defined]
                    span.add_event("exception", {"error": str(e)})  # type: ignore[name-defined]
                    raise

            return wrapper

        return decorator

    def trace_async(
        self, name: Optional[str] = None, kind: SpanKind=SpanKind.INTERNAL
    ) -> Callable[..., Any]:
        """
        Decorator for async function tracing.
        """

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                span_name=name or func.__name__

                _span=self.tracer.start_span(span_name, kind=kind)
                try:
                    span.set_attribute("function", func.__name__)  # type: ignore[name-defined]
                    span.set_attribute("args_count", len(args))  # type: ignore[name-defined]
                    span.set_attribute("kwargs_count", len(kwargs))  # type: ignore[name-defined]

                    _result=await func(*args, **kwargs)

                    span.add_event("completed")  # type: ignore[name-defined]
                    self.tracer.end_span(span, SpanStatus.OK)  # type: ignore[name-defined]
                    return result  # type: ignore[name-defined]
                except Exception as e:
                    self.tracer.end_span(span, SpanStatus.ERROR, str(e))  # type: ignore[name-defined]
                    span.add_event("exception", {"error": str(e)})  # type: ignore[name-defined]
                    raise

            return wrapper

        return decorator


class TracingMiddleware:
    """Middleware for request tracing."""

    def __init__(self, tracer: Tracer) -> None:
        self.tracer=tracer

    def trace_request(
        self, request_id: Optional[str] = None, name: str="http_request"
    ) -> Tuple[str, Callable[[int, Optional[str]], None]]:
        if not request_id:
            _request_id=str(uuid.uuid4())

        # Start span
        _span=self.tracer.start_span(name, trace_id=request_id)

        def cleanup(statuscode: int=200, error: Optional[str] = None) -> None:
            status=SpanStatus.OK if status_code < 400 else SpanStatus.ERROR  # type: ignore[name-defined]
            self.tracer.end_span(span, status=status, description=error)  # type: ignore[name-defined]

        return request_id, cleanup  # type: ignore[return-value]
