#!/usr/bin/env python3
"""
Unit tests for distributed tracing.

Tests for:
- Span creation and lifecycle
- Trace context management
- Automatic tracing decorators
- Jaeger and Zipkin exporters
- Tracing middleware
"""

import time
import unittest
import asyncio


from distributed_tracing import (
    Tracer,
    Span,
    SpanKind,
    SpanStatus,
    TraceContext,
    TracingDecorator,
    JaegerExporter,
    ZipkinExporter,
    TracingMiddleware,
)


class TestSpan(unittest.TestCase):
    """Tests for span operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.span = Span(
            trace_id="trace123",
            span_id="span456",
            parent_span_id=None,
            name="test_operation",
            start_time=time.time(),
        )

    def test_span_creation(self) -> None:
        """Test span creation."""
        self.assertEqual(self.span.name, "test_operation")
        self.assertEqual(self.span.trace_id, "trace123")
        self.assertIsNone(self.span.end_time)

    def test_span_duration(self) -> None:
        """Test span duration calculation."""
        time.sleep(0.001)
        self.span.end()

        self.assertGreater(self.span.duration_ms, 0)

    def test_add_event(self) -> None:
        """Test adding event to span."""
        self.span.add_event("operation_started")

        self.assertEqual(len(self.span.events), 1)
        self.assertEqual(self.span.events[0].name, "operation_started")

    def test_add_event_with_attributes(self) -> None:
        """Test adding event with attributes."""
        self.span.add_event("checkpoint", {"step": 1, "status": "ok"})

        self.assertEqual(self.span.events[0].attributes["step"], 1)

    def test_set_attribute(self) -> None:
        """Test setting span attributes."""
        self.span.set_attribute("cluster", "prod-1")
        self.span.set_attribute("operation", "scale")

        self.assertEqual(self.span.attributes["cluster"], "prod-1")
        self.assertEqual(self.span.attributes["operation"], "scale")

    def test_span_end(self) -> None:
        """Test ending span."""
        self.assertIsNone(self.span.end_time)

        self.span.end()

        self.assertIsNotNone(self.span.end_time)


class TestTraceContext(unittest.TestCase):
    """Tests for trace context."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.context = TraceContext()

    def test_set_and_get_span(self) -> None:
        """Test setting and getting current span."""
        span = Span(
            trace_id="trace123",
            span_id="span456",
            parent_span_id=None,
            name="test",
            start_time=time.time(),
        )

        self.context.set_current_span(span)
        retrieved = self.context.get_current_span()

        self.assertEqual(retrieved.span_id, "span456")

    def test_get_trace_id(self) -> None:
        """Test getting trace ID."""
        trace_id = self.context.get_trace_id()

        self.assertIsNotNone(trace_id)

    def test_clear_context(self) -> None:
        """Test clearing context."""
        span = Span(
            trace_id="trace123",
            span_id="span456",
            parent_span_id=None,
            name="test",
            start_time=time.time(),
        )

        self.context.set_current_span(span)
        self.context.clear()
        retrieved = self.context.get_current_span()

        self.assertIsNone(retrieved)


class TestTracer(unittest.TestCase):
    """Tests for tracer."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.tracer = Tracer("test_service")

    def test_tracer_initialization(self) -> None:
        """Test tracer initialization."""
        self.assertEqual(self.tracer.name, "test_service")
        self.assertEqual(len(self.tracer.spans), 0)

    def test_start_span(self) -> None:
        """Test starting span."""
        span = self.tracer.start_span("test_operation")

        self.assertIsNotNone(span)
        self.assertEqual(span.name, "test_operation")
        self.assertEqual(len(self.tracer.spans), 1)

    def test_end_span(self) -> None:
        """Test ending span."""
        span = self.tracer.start_span("test_operation")
        self.tracer.end_span(span, SpanStatus.OK)

        self.assertEqual(span.status, SpanStatus.OK)
        self.assertIsNotNone(span.end_time)

    def test_create_child_span(self) -> None:
        """Test creating child span."""
        parent_span = self.tracer.start_span("parent")
        child_span = self.tracer.create_child_span("child")

        self.assertEqual(child_span.parent_span_id, parent_span.span_id)
        self.assertEqual(child_span.trace_id, parent_span.trace_id)

    def test_get_spans_by_trace(self) -> None:
        """Test retrieving spans by trace ID."""
        span1 = self.tracer.start_span("op1")
        _span2 = self.tracer.create_child_span("op2")

        trace_id = span1.trace_id
        spans = self.tracer.get_spans(trace_id)

        self.assertEqual(len(spans), 2)

    def test_multiple_traces(self) -> None:
        """Test handling multiple traces."""
        span1 = self.tracer.start_span("trace1_op1")
        trace1_id = span1.trace_id

        span2 = self.tracer.start_span("trace2_op1")
        trace2_id = span2.trace_id

        self.assertNotEqual(trace1_id, trace2_id)
        self.assertEqual(len(self.tracer.spans), 2)

    def test_clear_spans(self) -> None:
        """Test clearing spans."""
        self.tracer.start_span("op1")
        self.tracer.start_span("op2")

        self.tracer.clear_spans()

        self.assertEqual(len(self.tracer.spans), 0)


class TestTracingDecorator(unittest.TestCase):
    """Tests for tracing decorator."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.tracer = Tracer("test_service")
        self.decorator = TracingDecorator(self.tracer)

    def test_trace_decorator(self) -> None:
        """Test function tracing decorator."""

        @self.decorator.trace("traced_function")
        def sample_function(x, y):
            return x + y

        result = sample_function(5, 3)

        self.assertEqual(result, 8)
        self.assertEqual(len(self.tracer.spans), 1)

    def test_trace_decorator_with_exception(self) -> None:
        """Test decorator with exception."""

        @self.decorator.trace("error_function")
        def error_function() -> None:
            raise ValueError("Test error")

        with self.assertRaises(ValueError):
            error_function()

        span = self.tracer.spans[0]
        self.assertEqual(span.status, SpanStatus.ERROR)

    def test_trace_decorator_captures_args(self) -> None:
        """Test decorator captures function arguments."""

        @self.decorator.trace()
        def sample_function(a, b, c=3):
            return a + b + c

        sample_function(1, 2, c=4)

        span = self.tracer.spans[0]
        self.assertEqual(span.attributes["args_count"], 2)
        self.assertEqual(span.attributes["kwargs_count"], 1)

    def test_trace_async_decorator(self) -> None:
        """Test async function tracing."""

        async def _test() -> None:
            @self.decorator.trace_async("async_operation")
            async def async_function() -> str:
                await asyncio.sleep(0.01)
                return "result"

            result = await async_function()

            self.assertEqual(result, "result")
            self.assertEqual(len(self.tracer.spans), 1)

        asyncio.run(_test())

    def test_trace_async_decorator_with_exception(self) -> None:
        """Test async decorator with exception."""

        async def _test() -> None:
            @self.decorator.trace_async("async_error")
            async def async_error_function() -> None:
                await asyncio.sleep(0.01)
                raise RuntimeError("Async error")

            with self.assertRaises(RuntimeError):
                await async_error_function()

            span = self.tracer.spans[0]
            self.assertEqual(span.status, SpanStatus.ERROR)

        asyncio.run(_test())


@unittest.skipIf(JaegerExporter is None, "JaegerExporter not available")
class TestJaegerExporter(unittest.TestCase):
    """Tests for Jaeger exporter."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.exporter = JaegerExporter()

    def test_exporter_initialization(self) -> None:
        """Test exporter initialization."""
        self.assertEqual(self.exporter.agent_host, "localhost")
        self.assertEqual(self.exporter.agent_port, 6831)

    def test_export_spans(self) -> None:
        """Test exporting spans."""
        tracer = Tracer("test")
        span = tracer.start_span("operation")
        tracer.end_span(span, SpanStatus.OK)

        success = self.exporter.export_spans(tracer.spans)

        self.assertTrue(success)

    def test_batch_buffering(self) -> None:
        """Test span buffering and automatic flushing."""
        tracer = Tracer("test")
        spans = []

        # Create more than batch_size (100) spans to trigger auto-flush
        for i in range(120):
            span = tracer.start_span(f"op_{i}")
            tracer.end_span(span, SpanStatus.OK)
            spans.append(span)

        self.exporter.export_spans(spans)
        # After exporting 120 spans with batch_size=100, buffer should have
        # only 20
        self.assertLess(len(self.exporter.traces_buffer), len(spans))


@unittest.skipIf(ZipkinExporter is None, "ZipkinExporter not available")
class TestZipkinExporter(unittest.TestCase):
    """Tests for Zipkin exporter."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.exporter = ZipkinExporter()

    def test_exporter_initialization(self) -> None:
        """Test exporter initialization."""
        self.assertIn("9411", self.exporter.url)

    def test_export_spans(self) -> None:
        """Test exporting spans to Zipkin."""
        tracer = Tracer("test")
        span = tracer.start_span("operation")
        span.set_attribute("service", "debvisor")
        tracer.end_span(span, SpanStatus.OK)

        success = self.exporter.export_spans(tracer.spans)

        self.assertTrue(success)

    def test_zipkin_format_conversion(self) -> None:
        """Test Zipkin format conversion and buffering."""
        tracer = Tracer("test")
        span = tracer.start_span("test_op", kind=SpanKind.SERVER)
        tracer.end_span(span, SpanStatus.OK)

        self.exporter.export_spans(tracer.spans)

        # With 1 span and batch_size 100, buffer should hold the span
        self.assertEqual(len(self.exporter.traces_buffer), 1)
        # Verify the span is buffered correctly
        buffered_span = self.exporter.traces_buffer[0]
        self.assertEqual(buffered_span.name, "test_op")
        self.assertEqual(buffered_span.kind, SpanKind.SERVER)


class TestTracingMiddleware(unittest.TestCase):
    """Tests for tracing middleware."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.tracer = Tracer("test_service")
        self.middleware = TracingMiddleware(self.tracer)

    def test_trace_request(self) -> None:
        """Test request tracing."""
        request_id, cleanup = self.middleware.trace_request("req123", "http_request")

        self.assertEqual(request_id, "req123")
        self.assertIsNotNone(cleanup)

    def test_trace_request_auto_id(self) -> None:
        """Test request tracing with auto-generated ID."""
        request_id, cleanup = self.middleware.trace_request()

        self.assertIsNotNone(request_id)

    def test_cleanup_success(self) -> None:
        """Test cleanup on success."""
        request_id, cleanup = self.middleware.trace_request()
        cleanup(status_code=200)

        span = self.tracer.spans[-1]
        self.assertEqual(span.status, SpanStatus.OK)

    def test_cleanup_error(self) -> None:
        """Test cleanup on error."""
        request_id, cleanup = self.middleware.trace_request()
        cleanup(status_code=500, error="Internal server error")

        span = self.tracer.spans[-1]
        self.assertEqual(span.status, SpanStatus.ERROR)


class TestTracingIntegration(unittest.TestCase):
    """Integration tests for tracing."""

    def test_end_to_end_tracing(self) -> None:
        """Test complete tracing flow."""
        tracer = Tracer("debvisor")

        # Create root span
        root_span = tracer.start_span("cluster_operation", kind=SpanKind.SERVER)
        root_span.set_attribute("cluster", "prod-1")

        # Create child operations
        validate_span = tracer.create_child_span("validate")
        validate_span.add_event("validation_started")
        time.sleep(0.01)
        validate_span.add_event("validation_complete")
        tracer.end_span(validate_span, SpanStatus.OK)

        execute_span = tracer.create_child_span("execute")
        tracer.end_span(execute_span, SpanStatus.OK)

        tracer.end_span(root_span, SpanStatus.OK)

        # Verify trace structure
        trace_spans = tracer.get_spans(root_span.trace_id)
        self.assertEqual(len(trace_spans), 3)

    def test_trace_context_propagation(self) -> None:
        """Test trace context propagation."""
        tracer = Tracer("debvisor")

        span1 = tracer.start_span("op1")
        self.assertEqual(tracer.context.get_current_span().span_id, span1.span_id)

        span2 = tracer.create_child_span("op2")
        self.assertEqual(tracer.context.get_current_span().span_id, span2.span_id)

    def test_multiple_traces_isolation(self) -> None:
        """Test isolation of multiple traces."""
        tracer = Tracer("debvisor")

        trace1_span = tracer.start_span("trace1")
        trace1_id = trace1_span.trace_id

        trace2_span = tracer.start_span("trace2")
        trace2_id = trace2_span.trace_id

        trace1_spans = tracer.get_spans(trace1_id)
        trace2_spans = tracer.get_spans(trace2_id)

        self.assertEqual(len(trace1_spans), 1)
        self.assertEqual(len(trace2_spans), 1)
        self.assertNotEqual(trace1_id, trace2_id)


if __name__ == "__main__":
    unittest.main()
