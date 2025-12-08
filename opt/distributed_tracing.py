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
    SimpleSpanProcessor
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.trace import Status, StatusCode

# Exporters (conditional import to avoid hard crashes if not installed)
try:
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
except ImportError:
    JaegerExporter = None

try:
    from opentelemetry.exporter.zipkin.json import ZipkinExporter
except ImportError:
    ZipkinExporter = None

try:
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
except ImportError:
    OTLPSpanExporter = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

resource = Resource(attributes={
    SERVICE_NAME: service_name
})
provider = TracerProvider(resource=resource)

# Configure Exporters based on Environment
if otlp_endpoint:
    if OTLPSpanExporter:
        otlp_exporter = OTLPSpanExporter(
            endpoint=otlp_endpoint
        )
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        logger.info("OTLP exporter configured")
    else:
        logger.warning("OTLP exporter requested but not installed")

if os.getenv("JAEGER_AGENT_HOST"):
    if JaegerExporter:
        jaeger_exporter = JaegerExporter(
            agent_host_name=os.getenv("JAEGER_AGENT_HOST", "localhost"),
            agent_port=int(os.getenv("JAEGER_AGENT_PORT", 6831)),
        )
        provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
        logger.info("Jaeger exporter configured")
    else:
        logger.warning("Jaeger exporter requested but not installed")

if os.getenv("ZIPKIN_COLLECTOR_URL"):
    if ZipkinExporter:
        zipkin_exporter = ZipkinExporter(
            endpoint=os.getenv("ZIPKIN_COLLECTOR_URL", "http://localhost:9411/api/v2/spans")
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

    def start_span(self, name: str, kind: SpanKind = SpanKind.INTERNAL,
                   trace_id: Optional[str] = None,
                   parent_span_id: Optional[str] = None) -> trace.Span:
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
                    trace_flags=trace.TraceFlags.SAMPLED
                )
                context = trace.set_span_in_context(trace.NonRecordingSpan(span_context))
            except ValueError:
                logger.warning(f"Invalid trace/span ID format: {trace_id}/{parent_span_id}")

        return self._tracer.start_span(name, kind=kind.value, context=context)

    def end_span(self, span: trace.Span, status: SpanStatus = SpanStatus.OK,
                 description: Optional[str] = None) -> None:
        """
        End span.

        Args:
            span: Span to end
            status: Span status
            description: Status description
        """
        if status == SpanStatus.ERROR:
            span.set_status(Status(status.value, description=description))
        else:
            span.set_status(Status(status.value))
        
        span.end()

    def create_child_span(self, name: str, kind: SpanKind = SpanKind.INTERNAL) -> trace.Span:
        """
        Create child span of current active span.
        
        OTel handles parent context automatically if running in the same context.
        """
        return self._tracer.start_span(name, kind=kind.value)

    def get_spans(self, trace_id: Optional[str] = None) -> List[Any]:
        """
        Get spans by trace ID.
        
        NOT SUPPORTED in standard OTel SDK without a custom memory exporter.
        Returns empty list to prevent crashes.
        """
        logger.warning("get_spans() is not supported with OTel SDK")
        return []

    def clear_spans(self) -> None:
        """Clear all spans."""
        pass


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
                
                # Use OTel's start_as_current_span to handle context automatically
                with self.tracer._tracer.start_as_current_span(span_name, kind=kind.value) as span:
                    try:
                        # Add function arguments to span
                        span.set_attribute("function", func.__name__)
                        span.set_attribute("args_count", len(args))
                        span.set_attribute("kwargs_count", len(kwargs))

                        result = func(*args, **kwargs)

                        span.add_event("completed")
                        span.set_status(Status(StatusCode.OK))
                        return result
                    except Exception as e:
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                        span.record_exception(e)
                        raise

            return wrapper
        return decorator
