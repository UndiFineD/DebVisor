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

"""
Distributed Tracing Integration for DebVisor.

Implements OpenTelemetry-compatible distributed tracing with:
- Automatic span creation and context propagation
- Integration with popular tracing backends (Jaeger, Zipkin)
- Custom span attributes for DebVisor operations
- Sampling strategies
- Error tracking and exception recording

Author: DebVisor Team
Date: November 28, 2025
"""

from typing import TypeVar
from typing import Tuple
from datetime import datetime, timezone
import asyncio
import functools
import logging
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Generator, List, Optional

logger = logging.getLogger(__name__)

# Type variable for decorated functions
F = TypeVar("F", bound=Callable[..., Any])


# =============================================================================
# Enums
# =============================================================================


class SpanKind(Enum):
    """Type of span."""

    INTERNAL = "internal"
    SERVER = "server"
    CLIENT = "client"
    PRODUCER = "producer"
    CONSUMER = "consumer"


class SpanStatus(Enum):
    """Span completion status."""

    UNSET = "unset"
    OK = "ok"
    ERROR = "error"


class SamplingDecision(Enum):
    """Sampling decision."""

    DROP = "drop"
    RECORD_ONLY = "record_only"
    RECORD_AND_SAMPLE = "record_and_sample"


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class TraceContext:
    """W3C Trace Context."""

    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    trace_flags: int = 1    # Sampled flag
    trace_state: str = ""

    def __post_init__(self) -> None:
        if not self.trace_id:
            self.trace_id = self._generate_trace_id()
        if not self.span_id:
            self.span_id = self._generate_span_id()

    @staticmethod
    def _generate_trace_id() -> str:
        """Generate 128-bit trace ID."""
        return uuid.uuid4().hex

    @staticmethod
    def _generate_span_id() -> str:
        """Generate 64-bit span ID."""
        return uuid.uuid4().hex[:16]

    def to_traceparent(self) -> str:
        """Convert to W3C traceparent header."""
        return f"00-{self.trace_id}-{self.span_id}-{self.trace_flags:02x}"

    @classmethod
    def from_traceparent(cls, traceparent: str) -> Optional["TraceContext"]:
        """Parse W3C traceparent header."""
        try:
            parts = traceparent.split("-")
            if len(parts) != 4:
                return None

            version, trace_id, span_id, flags = parts

            if version != "00":
                return None

            return cls(
                trace_id=trace_id,
                span_id=cls._generate_span_id(),    # New span
                parent_span_id=span_id,
                trace_flags=int(flags, 16),
            )
        except Exception:
            return None

    def create_child(self) -> "TraceContext":
        """Create child context."""
        return TraceContext(
            trace_id=self.trace_id,
            span_id=self._generate_span_id(),
            parent_span_id=self.span_id,
            trace_flags=self.trace_flags,
            trace_state=self.trace_state,
        )


@dataclass
class SpanEvent:
    """Event within a span."""

    name: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SpanLink:
    """Link to another span."""

    trace_id: str
    span_id: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Span:
    """Represents a trace span."""

    name: str
    context: TraceContext
    kind: SpanKind = SpanKind.INTERNAL
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    status: SpanStatus = SpanStatus.UNSET
    status_message: str = ""

    # Attributes
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[SpanEvent] = field(default_factory=list)
    links: List[SpanLink] = field(default_factory=list)

    # Resource info
    service_name: str = "debvisor"
    service_version: str = "2.0.0"

    @property
    def trace_id(self) -> str:
        return self.context.trace_id

    @property
    def span_id(self) -> str:
        return self.context.span_id

    @property
    def parent_span_id(self) -> Optional[str]:
        return self.context.parent_span_id

    @property
    def duration_ms(self) -> Optional[float]:
        """Get span duration in milliseconds."""
        if self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds() * 1000
        return None

    def set_attribute(self, key: str, value: Any) -> None:
        """Set span attribute."""
        self.attributes[key] = value

    def set_status(self, status: SpanStatus, message: str = "") -> None:
        """Set span status."""
        self.status = status
        self.status_message = message

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Add event to span."""
        self.events.append(SpanEvent(name=name, attributes=attributes or {}))

    def record_exception(self, exception: Exception) -> None:
        """Record exception in span."""
        self.add_event(
            "exception",
            {
                "exception.type": type(exception).__name__,
                "exception.message": str(exception),
                "exception.stacktrace": self._format_stacktrace(exception),
            },
        )
        self.set_status(SpanStatus.ERROR, str(exception))

    def end(self) -> None:
        """End the span."""
        if self.end_time is None:
            self.end_time = datetime.now(timezone.utc)

    @staticmethod
    def _format_stacktrace(exception: Exception) -> str:
        """Format exception stacktrace."""
        import traceback

        return "".join(
            traceback.format_exception(
                type(exception), exception, exception.__traceback__
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for export."""
        return {
            "traceId": self.trace_id,
            "spanId": self.span_id,
            "parentSpanId": self.parent_span_id,
            "name": self.name,
            "kind": self.kind.value,
            "startTime": self.start_time.isoformat(),
            "endTime": self.end_time.isoformat() if self.end_time else None,
            "durationMs": self.duration_ms,
            "status": {"code": self.status.value, "message": self.status_message},
            "attributes": self.attributes,
            "events": [
                {
                    "name": e.name,
                    "timestamp": e.timestamp.isoformat(),
                    "attributes": e.attributes,
                }
                for e in self.events
            ],
            "resource": {
                "service.name": self.service_name,
                "service.version": self.service_version,
            },
        }


# =============================================================================
# Samplers
# =============================================================================


class Sampler:
    """Base sampler class."""

    def should_sample(
        self, trace_id: str, name: str, kind: SpanKind, attributes: Dict[str, Any]
    ) -> SamplingDecision:
        """
        Determine if span should be sampled.

        Args:
            trace_id: Unique trace identifier
            name: Span name
            kind: Span kind (server, client, etc.)
            attributes: Span attributes

        Returns:
            SamplingDecision indicating whether to sample
        """
        # Default implementation: sample everything
        # Override in subclasses for custom logic
        return SamplingDecision.RECORD_AND_SAMPLE


class AlwaysOnSampler(Sampler):
    """Always sample all spans."""

    def should_sample(self, *args: Any, **kwargs: Any) -> SamplingDecision:
        return SamplingDecision.RECORD_AND_SAMPLE


class AlwaysOffSampler(Sampler):
    """Never sample any spans."""

    def should_sample(self, *args: Any, **kwargs: Any) -> SamplingDecision:
        return SamplingDecision.DROP


class RatioBasedSampler(Sampler):
    """Sample a ratio of traces."""

    def __init__(self, ratio: float = 0.1):
        """
        Initialize sampler.

        Args:
            ratio: Sampling ratio (0.0 to 1.0)
        """
        self.ratio = max(0.0, min(1.0, ratio))
        self._threshold = int(ratio * (2**32))

    def should_sample(
        self, trace_id: str, name: str, kind: SpanKind, attributes: Dict[str, Any]
    ) -> SamplingDecision:
        """Sample based on trace ID hash."""
        # Use last 8 characters of trace ID for consistency
        trace_suffix = trace_id[-8:]
        hash_value = int(trace_suffix, 16) % (2**32)

        if hash_value < self._threshold:
            return SamplingDecision.RECORD_AND_SAMPLE
        return SamplingDecision.DROP


class ParentBasedSampler(Sampler):
    """Sample based on parent span decision."""

    def __init__(self, root_sampler: Optional[Sampler] = None):
        """
        Initialize sampler.

        Args:
            root_sampler: Sampler for root spans
        """
        self.root_sampler = root_sampler or AlwaysOnSampler()

    def should_sample(
        self,
        trace_id: str,
        name: str,
        kind: SpanKind,
        attributes: Dict[str, Any],
        parent_sampled: Optional[bool] = None,
    ) -> SamplingDecision:
        """Sample based on parent decision."""
        if parent_sampled is not None:
            if parent_sampled:
                return SamplingDecision.RECORD_AND_SAMPLE
            return SamplingDecision.DROP

        return self.root_sampler.should_sample(trace_id, name, kind, attributes)


class PrioritySampler(Sampler):
    """
    Sampler that prioritizes traces based on attributes or priority flag.

    Used in conjunction with TailSamplingExporter to ensure critical traces
    are preserved.
    """

    def __init__(self, root_sampler: Optional[Sampler] = None):
        self.root_sampler = root_sampler or AlwaysOnSampler()

    def should_sample(
        self, trace_id: str, name: str, kind: SpanKind, attributes: Dict[str, Any]
    ) -> SamplingDecision:
        # Check for priority attribute
        if attributes.get("priority") == "high" or attributes.get("error") is True:
            return SamplingDecision.RECORD_AND_SAMPLE

        return self.root_sampler.should_sample(trace_id, name, kind, attributes)


# =============================================================================
# Exporters
# =============================================================================


class SpanExporter:
    """Base span exporter."""

    async def export(self, spans: List[Span]) -> bool:
        """
        Export spans to backend.

        Args:
            spans: List of spans to export

        Returns:
            True if export succeeded, False otherwise
        """
        # Default implementation: no-op exporter for testing
        # Override in subclasses for actual export logic
        logger.debug(f"No-op exporter: would export {len(spans)} spans")
        return True

    async def shutdown(self) -> None:
        """Shutdown exporter."""
        pass


class ConsoleExporter(SpanExporter):
    """Export spans to console (for debugging)."""

    async def export(self, spans: List[Span]) -> bool:
        """Print spans to console."""
        import json

        for span in spans:
            print(json.dumps(span.to_dict(), indent=2, default=str))

        return True


class JaegerExporter(SpanExporter):
    """Export spans to Jaeger."""

    def __init__(
        self,
        endpoint: str = "http://localhost:14268/api/traces",
        service_name: str = "debvisor",
    ):
        self.endpoint = endpoint
        self.service_name = service_name

    async def export(self, spans: List[Span]) -> bool:
        """Export spans to Jaeger via HTTP."""
        try:
            import aiohttp

            # Convert to Jaeger format
            payload = self._to_jaeger_format(spans)

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                ) as response:
                    return bool(response.status == 200)

        except Exception as e:
            logger.error(f"Failed to export spans to Jaeger: {e}")
            return False

    def _to_jaeger_format(self, spans: List[Span]) -> Dict[str, Any]:
        """Convert spans to Jaeger Thrift format."""
        # Simplified - in production use proper Thrift encoding
        return {
            "serviceName": self.service_name,
            "spans": [span.to_dict() for span in spans],
        }


class OTLPExporter(SpanExporter):
    """Export spans using OTLP protocol."""

    def __init__(
        self,
        endpoint: str = "http://localhost:4318/v1/traces",
        headers: Optional[Dict[str, str]] = None,
    ):
        self.endpoint = endpoint
        self.headers = headers or {}

    async def export(self, spans: List[Span]) -> bool:
        """Export spans via OTLP HTTP."""
        try:
            import aiohttp

            payload = self._to_otlp_format(spans)

            headers = {"Content-Type": "application/json", **self.headers}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.endpoint, json=payload, headers=headers
                ) as response:
                    return response.status in (200, 202)

        except Exception as e:
            logger.error(f"Failed to export spans via OTLP: {e}")
            return False

    def _to_otlp_format(self, spans: List[Span]) -> Dict[str, Any]:
        """Convert spans to OTLP format."""
        return {
            "resourceSpans": [
                {
                    "resource": {
                        "attributes": [
                            {
                                "key": "service.name",
                                "value": {
                                    "stringValue": (
                                        spans[0].service_name if spans else "debvisor"
                                    )
                                },
                            },
                            {
                                "key": "service.version",
                                "value": {
                                    "stringValue": (
                                        spans[0].service_version if spans else "2.0.0"
                                    )
                                },
                            },
                        ]
                    },
                    "scopeSpans": [
                        {
                            "scope": {"name": "debvisor.tracing"},
                            "spans": [self._span_to_otlp(span) for span in spans],
                        }
                    ],
                }
            ]
        }

    def _span_to_otlp(self, span: Span) -> Dict[str, Any]:
        """Convert single span to OTLP format."""
        return {
            "traceId": span.trace_id,
            "spanId": span.span_id,
            "parentSpanId": span.parent_span_id or "",
            "name": span.name,
            "kind": self._span_kind_to_otlp(span.kind),
            "startTimeUnixNano": int(span.start_time.timestamp() * 1e9),
            "endTimeUnixNano": (
                int(span.end_time.timestamp() * 1e9) if span.end_time else 0
            ),
            "attributes": [
                {"key": k, "value": {"stringValue": str(v)}}
                for k, v in span.attributes.items()
            ],
            "status": {
                "code": (
                    1
                    if span.status == SpanStatus.OK
                    else (2 if span.status == SpanStatus.ERROR else 0)
                ),
                "message": span.status_message,
            },
        }

    @staticmethod
    def _span_kind_to_otlp(kind: SpanKind) -> int:
        """Convert span kind to OTLP enum."""
        mapping = {
            SpanKind.INTERNAL: 1,
            SpanKind.SERVER: 2,
            SpanKind.CLIENT: 3,
            SpanKind.PRODUCER: 4,
            SpanKind.CONSUMER: 5,
        }
        return mapping.get(kind, 0)


class TailSamplingExporter(SpanExporter):
    """
    Exporter that implements tail-based sampling.

    Buffers spans and decides whether to export them based on:
    1. Errors present in the trace
    2. High latency (duration > threshold)
    3. Specific attributes (priority=high)
    """

    def __init__(
        self,
        delegate: SpanExporter,
        latency_threshold_ms: float = 1000.0,
        error_only: bool = False,
    ):
        self.delegate = delegate
        self.latency_threshold_ms = latency_threshold_ms
        self.error_only = error_only
        self._buffer: Dict[str, List[Span]] = {}
        self._lock = asyncio.Lock()

    async def export(self, spans: List[Span]) -> bool:
        """
        Process and export spans based on sampling rules.

        Note: This is a simplified implementation. In a real distributed system,
        tail sampling requires a centralized collector. This implementation
        works for single-process or when all spans for a trace are local.
        """
        async with self._lock:
            # Group spans by trace_id
            for span in spans:
                if span.trace_id not in self._buffer:
                    self._buffer[span.trace_id] = []
                self._buffer[span.trace_id].append(span)

            # Check for completed traces (simplified: assume batch contains full traces or we process what we have)
            # In reality, we'd need a timeout mechanism to flush incomplete traces.
            # Here we'll process all buffered traces that have a root span or are "old" enough.
            # For this implementation, we'll just process the current batch's traces.

            traces_to_export = []
            trace_ids_to_remove = []

            for trace_id, trace_spans in self._buffer.items():
                should_keep = False

                # Rule 1: Keep if any span has error
                if any(s.status == SpanStatus.ERROR for s in trace_spans):
                    should_keep = True

                # Rule 2: Keep if any span exceeds latency threshold
                elif any(
                    (s.end_time.timestamp() - s.start_time.timestamp()) * 1000
                    > self.latency_threshold_ms
                    for s in trace_spans
                    if s.end_time
                ):
                    should_keep = True

                # Rule 3: Keep if priority attribute is set
                elif any(s.attributes.get("priority") == "high" for s in trace_spans):
                    should_keep = True

                # Rule 4: Random sampling for the rest (if not error_only)
                elif not self.error_only:
                    # 10% sampling for normal traces
                    if int(trace_id[-8:], 16) % 100 < 10:
                        should_keep = True

                if should_keep:
                    traces_to_export.extend(trace_spans)

                # We assume we can clear the buffer for these trace_ids
                # In a real system, we'd wait for a timeout.
                trace_ids_to_remove.append(trace_id)

            for tid in trace_ids_to_remove:
                del self._buffer[tid]

        if traces_to_export:
            return await self.delegate.export(traces_to_export)

        return True

    async def shutdown(self) -> None:
        await self.delegate.shutdown()


# =============================================================================
# Tracer
# =============================================================================


class Tracer:
    """
    Distributed tracer for DebVisor.

    Features:
    - Automatic context propagation
    - Multiple export backends
    - Configurable sampling
    - Batch span export
    """

    def __init__(
        self,
        service_name: str = "debvisor",
        service_version: str = "2.0.0",
        sampler: Optional[Sampler] = None,
        exporter: Optional[SpanExporter] = None,
        batch_size: int = 100,
        flush_interval_seconds: float = 5.0,
    ):
        """
        Initialize tracer.

        Args:
            service_name: Service name for resource
            service_version: Service version
            sampler: Span sampler
            exporter: Span exporter
            batch_size: Batch size for export
            flush_interval_seconds: Export interval
        """
        self.service_name = service_name
        self.service_version = service_version
        self.sampler = sampler or AlwaysOnSampler()
        self.exporter = exporter or ConsoleExporter()
        self.batch_size = batch_size
        self.flush_interval_seconds = flush_interval_seconds

        # Span buffer
        self._spans: List[Span] = []
        self._lock = asyncio.Lock()

        # Current context (thread-local in production)
        self._current_context: Optional[TraceContext] = None

        # Background export task
        self._export_task: Optional[asyncio.Task[None]] = None

        logger.info(f"Tracer initialized for service {service_name}")

    async def start(self) -> None:
        """Start background export task."""
        if self._export_task is None:
            self._export_task = asyncio.create_task(self._export_loop())
            logger.info("Tracer background export started")

    async def shutdown(self) -> None:
        """Shutdown tracer and flush remaining spans."""
        if self._export_task:
            self._export_task.cancel()
            try:
                await self._export_task
            except asyncio.CancelledError:
                pass

        # Final flush
        await self._flush()
        await self.exporter.shutdown()

        logger.info("Tracer shutdown complete")

    @contextmanager
    def start_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Optional[Dict[str, Any]] = None,
        links: Optional[List[SpanLink]] = None,
    ) -> Generator[Optional[Span], None, None]:
        """
        Start a new span.

        Args:
            name: Span name
            kind: Span kind
            attributes: Initial attributes
            links: Links to other spans

        Yields:
            Span instance
        """
        # Determine context
        if self._current_context:
            context = self._current_context.create_child()
        else:
            context = TraceContext(trace_id="", span_id="")

        # Check sampling
        decision = self.sampler.should_sample(
            context.trace_id, name, kind, attributes or {}
        )

        if decision == SamplingDecision.DROP:
            yield None
            return

        # Create span
        span = Span(
            name=name,
            context=context,
            kind=kind,
            attributes=attributes or {},
            links=links or [],
            service_name=self.service_name,
            service_version=self.service_version,
        )

        # Set as current context
        previous_context = self._current_context
        self._current_context = context

        try:
            yield span
            if span.status == SpanStatus.UNSET:
                span.set_status(SpanStatus.OK)
        except Exception as e:
            span.record_exception(e)
            raise
        finally:
            span.end()
            self._current_context = previous_context

            # Add to buffer
            asyncio.create_task(self._add_span(span))

    async def _add_span(self, span: Span) -> None:
        """Add span to export buffer."""
        async with self._lock:
            self._spans.append(span)

            if len(self._spans) >= self.batch_size:
                await self._flush()

    async def _flush(self) -> None:
        """Flush span buffer to exporter."""
        async with self._lock:
            if not self._spans:
                return

            spans_to_export = self._spans.copy()
            self._spans.clear()

        try:
            success = await self.exporter.export(spans_to_export)
            if not success:
                logger.warning(f"Failed to export {len(spans_to_export)} spans")
        except Exception as e:
            logger.error(f"Span export error: {e}")

    async def _export_loop(self) -> None:
        """Background export loop."""
        while True:
            try:
                await asyncio.sleep(self.flush_interval_seconds)
                await self._flush()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Export loop error: {e}")

    def inject_context(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Inject trace context into headers."""
        if self._current_context:
            headers["traceparent"] = self._current_context.to_traceparent()
            if self._current_context.trace_state:
                headers["tracestate"] = self._current_context.trace_state
        return headers

    def extract_context(self, headers: Dict[str, str]) -> None:
        """Extract trace context from headers."""
        traceparent = headers.get("traceparent")
        if traceparent:
            context = TraceContext.from_traceparent(traceparent)
            if context:
                self._current_context = context
                if "tracestate" in headers:
                    self._current_context.trace_state = headers["tracestate"]


# =============================================================================
# Decorators
# =============================================================================


def trace(
    name: Optional[str] = None,
    kind: SpanKind = SpanKind.INTERNAL,
    attributes: Optional[Dict[str, Any]] = None,
) -> Callable[[F], F]:
    """
    Decorator to trace a function.

    Args:
        name: Span name (defaults to function name)
        kind: Span kind
        attributes: Additional attributes
    """

    def decorator(func: F) -> F:
        span_name = name or func.__name__

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            tracer = get_tracer()
            with tracer.start_span(span_name, kind, attributes) as span:
                if span:
                    span.set_attribute("function.name", func.__name__)
                    span.set_attribute("function.module", func.__module__)
                return func(*args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            tracer = get_tracer()
            with tracer.start_span(span_name, kind, attributes) as span:
                if span:
                    span.set_attribute("function.name", func.__name__)
                    span.set_attribute("function.module", func.__module__)
                return await func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper    # type: ignore
        return sync_wrapper    # type: ignore

    return decorator


# =============================================================================
# Flask Integration
# =============================================================================


def create_flask_middleware(tracer: Tracer) -> Tuple[Callable[[], None], Callable[[Any], Any]]:
    """
    Create Flask middleware for automatic tracing.

    Args:
        tracer: Tracer instance

    Returns:
        Tuple of (before_request, after_request) handlers
    """
    from flask import request, g

    def before_request() -> None:
        """Extract context and start span."""
        # Extract context from headers
        tracer.extract_context(dict(request.headers))

        # Start span
        span_name = f"{request.method} {request.path}"
        g.trace_span = tracer.start_span(
            span_name,
            kind=SpanKind.SERVER,
            attributes={
                "http.method": request.method,
                "http.url": request.url,
                "http.route": request.path,
                "http.user_agent": request.user_agent.string,
                "http.client_ip": request.remote_addr,
            },
        ).__enter__()

    def after_request(response: Any) -> Any:
        """End span and add response attributes."""
        span = getattr(g, "trace_span", None)
        if span:
            span.set_attribute("http.status_code", response.status_code)
            span.set_attribute(
                "http.response_content_length", response.content_length or 0
            )

            if response.status_code >= 500:
                span.set_status(SpanStatus.ERROR, f"HTTP {response.status_code}")
            else:
                span.set_status(SpanStatus.OK)

            span.end()

        return response

    return before_request, after_request


# =============================================================================
# Global Instance
# =============================================================================

_tracer: Optional[Tracer] = None


def get_tracer() -> Tracer:
    """Get global tracer instance."""
    global _tracer
    if _tracer is None:
        _tracer = Tracer()
    return _tracer


def configure_tracer(
    service_name: str = "debvisor",
    exporter_type: str = "console",
    exporter_endpoint: Optional[str] = None,
    sampling_ratio: float = 1.0,
) -> Tracer:
    """
    Configure global tracer.

    Args:
        service_name: Service name
        exporter_type: 'console', 'jaeger', or 'otlp'
        exporter_endpoint: Exporter endpoint URL
        sampling_ratio: Sampling ratio (0.0 to 1.0)

    Returns:
        Configured Tracer
    """
    global _tracer

    # Select exporter
    exporter: SpanExporter
    if exporter_type == "jaeger":
        exporter = JaegerExporter(
            endpoint=exporter_endpoint or "http://localhost:14268/api/traces",
            service_name=service_name,
        )
    elif exporter_type == "otlp":
        exporter = OTLPExporter(
            endpoint=exporter_endpoint or "http://localhost:4318/v1/traces"
        )
    else:
        exporter = ConsoleExporter()

    # Select sampler
    sampler: Sampler
    if sampling_ratio < 1.0:
        sampler = RatioBasedSampler(sampling_ratio)
    else:
        sampler = AlwaysOnSampler()

    _tracer = Tracer(service_name=service_name, sampler=sampler, exporter=exporter)

    logger.info(
        f"Tracer configured: service={service_name}, exporter={exporter_type}, sampling={sampling_ratio}"
    )

    return _tracer


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    @trace(name="example_operation")
    def example_sync_function() -> str:
        time.sleep(0.1)
        return "done"

    @trace(name="example_async_operation")
    async def example_async_function() -> str:
        await asyncio.sleep(0.1)
        return "async done"

    async def main() -> None:
        tracer = configure_tracer(
            service_name="test-service", exporter_type="console", sampling_ratio=1.0
        )

        await tracer.start()

        # Manual span
        with tracer.start_span("manual_span", kind=SpanKind.INTERNAL) as span:
            if span:
                span.set_attribute("custom.key", "custom.value")
                span.add_event("processing_started")
                await asyncio.sleep(0.05)
                span.add_event("processing_completed")

        # Decorated functions
        example_sync_function()
        await example_async_function()

        await tracer.shutdown()

    asyncio.run(main())
