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

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
Distributed tracing support for DebVisor RPC service using OpenTelemetry.

Provides:
- Automatic span creation for RPC calls
- Trace context propagation
- Performance profiling
- Call graph visualization support
"""

import logging
from typing import Optional, Dict, Any, List, Iterator
from contextlib import contextmanager
import time
import uuid

logger = logging.getLogger(__name__)


class TraceContext:
    """Trace context holder for distributed tracing."""

    def __init__(
        self, trace_id: Optional[str] = None, parent_span_id: Optional[str] = None
    ):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.parent_span_id = parent_span_id
        self.spans: List["Span"] = []

    def to_headers(self) -> Dict[str, str]:
        """Convert trace context to headers for propagation."""
        headers = {
            "X-Trace-ID": self.trace_id,
            "X-Trace-Span-ID": self.parent_span_id or "",
        }
        return {k: v for k, v in headers.items() if v}


class Span:
    """Represents a single span in a trace."""

    def __init__(
        self,
        trace_id: str,
        span_id: str,
        parent_span_id: Optional[str],
        operation_name: str,
        service: str = "rpc",
    ):
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_span_id = parent_span_id
        self.operation_name = operation_name
        self.service = service
        self.start_time: float = time.time()
        self.end_time: Optional[float] = None
        self.duration: Optional[float] = None
        self.status = "pending"
        self.error: Optional[Dict[str, str]] = None
        self.tags: Dict[str, Any] = {}
        self.logs: List[Dict[str, Any]] = []

    def add_tag(self, key: str, value: Any) -> None:
        """Add a tag to the span."""
        self.tags[key] = value

    def add_log(self, message: str, level: str = "info", **fields: Any) -> None:
        """Add a log event to the span."""
        self.logs.append(
            {
                "timestamp": time.time(),
                "message": message,
                "level": level,
                "fields": fields,
            }
        )

    def finish(self, status: str = "success", error: Optional[Exception] = None) -> None:
        """Mark span as finished."""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.status = status
        if error:
            self.error = {"type": type(error).__name__, "message": str(error)}

    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary for export."""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "operation_name": self.operation_name,
            "service": self.service,
            "duration_ms": self.duration * 1000 if self.duration else None,
            "status": self.status,
            "error": self.error,
            "tags": self.tags,
            "logs": self.logs,
        }


class SimpleTracer:
    """
    Simple distributed tracer implementation.

    In production, this would be replaced with OpenTelemetry SDK
    for full instrumentation and export to backend like Jaeger/Zipkin.
    """

    def __init__(self) -> None:
        self._trace_stack: List[Span] = []

    def create_trace(self, trace_id: Optional[str] = None) -> TraceContext:
        """Create a new trace context."""
        return TraceContext(trace_id)

    def start_span(
        self,
        operation_name: str,
        trace_context: TraceContext,
        service: str = "rpc",
        tags: Optional[Dict[str, Any]] = None,
    ) -> Span:
        """Start a new span within a trace."""
        parent_span_id = trace_context.parent_span_id
        span_id = str(uuid.uuid4())

        span = Span(
            trace_id=trace_context.trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            operation_name=operation_name,
            service=service,
        )

        if tags:
            for key, value in tags.items():
                span.add_tag(key, value)

        trace_context.parent_span_id = span_id
        self._trace_stack.append(span)
        trace_context.spans.append(span)

        logger.debug(
            f"Started span {span_id} for {operation_name} "
            f"(trace: {trace_context.trace_id})"
        )

        return span

    def finish_span(
        self, span: Span, status: str = "success", error: Optional[Exception] = None
    ) -> None:
        """Finish a span."""
        span.finish(status, error)
        if self._trace_stack and self._trace_stack[-1] == span:
            self._trace_stack.pop()

        logger.debug(
            f"Finished span {span.span_id} ({span.operation_name}): "
            f"status={span.status}, duration={span.duration:.3f}s"
            if span.duration is not None
            else f"status={span.status}, duration=unknown"
        )


# Global tracer instance
_tracer = SimpleTracer()


def get_tracer() -> SimpleTracer:
    """Get the global tracer instance."""
    return _tracer


@contextmanager
def trace_span(
    operation_name: str,
    trace_context: TraceContext,
    service: str = "rpc",
    tags: Optional[Dict[str, Any]] = None,
    capture_result: bool = False,
) -> Iterator[Span]:
    """
    Context manager for creating and managing a span.

    Usage:
        with trace_span('node.register', trace_ctx, tags={'node_id': '123'}) as span:
        # do work
            span.add_tag('result', 'success')
    """
    tracer = get_tracer()
    span = tracer.start_span(operation_name, trace_context, service, tags)

    try:
        yield span
        tracer.finish_span(span, "success")
    except Exception as e:
        tracer.finish_span(span, "error", e)
        raise


def export_trace_json(trace_context: TraceContext) -> Dict[str, Any]:
    """Export complete trace as JSON."""
    return {
        "trace_id": trace_context.trace_id,
        "spans": [span.to_dict() for span in trace_context.spans],
        "span_count": len(trace_context.spans),
        "total_duration_ms": (
            sum(s.duration * 1000 for s in trace_context.spans if s.duration)
            if trace_context.spans
            else 0
        ),
    }


def extract_trace_context_from_headers(headers: Dict[str, str]) -> TraceContext:
    """Extract trace context from request headers."""
    trace_id = headers.get("X-Trace-ID")
    parent_span_id = headers.get("X-Trace-Span-ID")

    return TraceContext(trace_id, parent_span_id)
