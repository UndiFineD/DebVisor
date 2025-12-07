#!/usr/bin/env python3
"""
Request ID Propagation for DebVisor Services.

Implements request ID (correlation ID) propagation across service boundaries
for distributed tracing and log correlation.

Author: DebVisor Team
Date: November 28, 2025
"""

import contextvars
import functools
import logging
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional, TypeVar

# Context variable for request ID (async-safe)
_request_context: contextvars.ContextVar['RequestContext'] = contextvars.ContextVar(
    'request_context',
    default=None
)

# Thread-local for sync code compatibility
_thread_local = threading.local()

logger = logging.getLogger(__name__)

# Type variable for function decoration
F = TypeVar('F', bound=Callable[..., Any])


# =============================================================================
# Constants
# =============================================================================

# Standard header names
HEADER_REQUEST_ID = "X-Request-ID"
HEADER_CORRELATION_ID = "X-Correlation-ID"
HEADER_TRACE_ID = "X-Trace-ID"
HEADER_SPAN_ID = "X-Span-ID"
HEADER_PARENT_SPAN_ID = "X-Parent-Span-ID"
HEADER_CAUSATION_ID = "X-Causation-ID"

# W3C Trace Context headers
HEADER_TRACEPARENT = "traceparent"
HEADER_TRACESTATE = "tracestate"

# All propagated headers
PROPAGATED_HEADERS = [
    HEADER_REQUEST_ID,
    HEADER_CORRELATION_ID,
    HEADER_TRACE_ID,
    HEADER_SPAN_ID,
    HEADER_PARENT_SPAN_ID,
    HEADER_CAUSATION_ID,
    HEADER_TRACEPARENT,
    HEADER_TRACESTATE,
]


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class RequestContext:
    """
    Context propagated across service calls.

    Contains all identifiers needed for request tracing and correlation.
    """

    # Primary identifiers
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: Optional[str] = None

    # Tracing identifiers
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    parent_span_id: Optional[str] = None

    # Causation chain
    causation_id: Optional[str] = None

    # W3C Trace Context
    traceparent: Optional[str] = None
    tracestate: Optional[str] = None

    # Metadata
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    service_name: str = "unknown"
    operation_name: str = "unknown"

    # Custom baggage
    baggage: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        """Ensure correlation_id is set."""
        if self.correlation_id is None:
            self.correlation_id = self.request_id
        if self.trace_id is None:
            self.trace_id = self.request_id
        if self.span_id is None:
            self.span_id = str(uuid.uuid4())[:16]

    def create_child_span(self, operation_name: str = "child") -> 'RequestContext':
        """
        Create a child context for nested operations.

        Args:
            operation_name: Name of the child operation

        Returns:
            New RequestContext with parent linkage
        """
        return RequestContext(
            request_id=self.request_id,
            correlation_id=self.correlation_id,
            trace_id=self.trace_id,
            span_id=str(uuid.uuid4())[:16],
            parent_span_id=self.span_id,
            causation_id=self.span_id,
            traceparent=self.traceparent,
            tracestate=self.tracestate,
            service_name=self.service_name,
            operation_name=operation_name,
            baggage=dict(self.baggage)
        )

    def to_headers(self) -> Dict[str, str]:
        """
        Convert context to HTTP headers.

        Returns:
            Dictionary of headers to propagate
        """
        headers = {
            HEADER_REQUEST_ID: self.request_id,
            HEADER_CORRELATION_ID: self.correlation_id or self.request_id,
        }

        if self.trace_id:
            headers[HEADER_TRACE_ID] = self.trace_id
        if self.span_id:
            headers[HEADER_SPAN_ID] = self.span_id
        if self.parent_span_id:
            headers[HEADER_PARENT_SPAN_ID] = self.parent_span_id
        if self.causation_id:
            headers[HEADER_CAUSATION_ID] = self.causation_id
        if self.traceparent:
            headers[HEADER_TRACEPARENT] = self.traceparent
        if self.tracestate:
            headers[HEADER_TRACESTATE] = self.tracestate

        return headers

    @classmethod
    def from_headers(cls, headers: Dict[str, str]) -> 'RequestContext':
        """
        Create context from HTTP headers.

        Args:
            headers: Dictionary of HTTP headers

        Returns:
            RequestContext populated from headers
        """
        # Case-insensitive header lookup
        def get_header(name: str) -> Optional[str]:
            for key, value in headers.items():
                if key.lower() == name.lower():
                    return value
            return None

        request_id = get_header(HEADER_REQUEST_ID) or str(uuid.uuid4())

        return cls(
            request_id=request_id,
            correlation_id=get_header(HEADER_CORRELATION_ID),
            trace_id=get_header(HEADER_TRACE_ID),
            span_id=get_header(HEADER_SPAN_ID),
            parent_span_id=get_header(HEADER_PARENT_SPAN_ID),
            causation_id=get_header(HEADER_CAUSATION_ID),
            traceparent=get_header(HEADER_TRACEPARENT),
            tracestate=get_header(HEADER_TRACESTATE),
        )

    def to_log_extra(self) -> Dict[str, Any]:
        """
        Get extra fields for structured logging.

        Returns:
            Dictionary of log extra fields
        """
        return {
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "service": self.service_name,
            "operation": self.operation_name,
        }


# =============================================================================
# Context Management
# =============================================================================

def get_current_context() -> Optional[RequestContext]:
    """
    Get the current request context.

    Returns:
        Current RequestContext or None
    """
    # Try contextvars first (works with asyncio)
    ctx = _request_context.get()
    if ctx is not None:
        return ctx

    # Fall back to thread-local
    return getattr(_thread_local, 'request_context', None)


def set_current_context(context: RequestContext) -> contextvars.Token:
    """
    Set the current request context.

    Args:
        context: RequestContext to set

    Returns:
        Token for resetting context
    """
    _thread_local.request_context = context
    return _request_context.set(context)


def clear_current_context(token: Optional[contextvars.Token] = None) -> None:
    """
    Clear the current request context.

    Args:
        token: Token from set_current_context (optional)
    """
    if token:
        _request_context.reset(token)
    else:
        _request_context.set(None)

    if hasattr(_thread_local, 'request_context'):
        del _thread_local.request_context


def get_request_id() -> Optional[str]:
    """
    Get the current request ID.

    Returns:
        Current request ID or None
    """
    ctx = get_current_context()
    return ctx.request_id if ctx else None


def get_correlation_id() -> Optional[str]:
    """
    Get the current correlation ID.

    Returns:
        Current correlation ID or None
    """
    ctx = get_current_context()
    return ctx.correlation_id if ctx else None


# =============================================================================
# Context Managers
# =============================================================================

class request_context:
    """
    Context manager for request context scope.

    Example:
        with request_context() as ctx:
            logger.info("Processing", extra=ctx.to_log_extra())
    """

    def __init__(
        self,
        request_id: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        service_name: str = "unknown",
        operation_name: str = "unknown",
        **kwargs: Any
    ):
        """
        Initialize context manager.

        Args:
            request_id: Explicit request ID
            headers: Headers to extract context from
            service_name: Name of current service
            operation_name: Name of current operation
            **kwargs: Additional context fields
        """
        if headers:
            self.context = RequestContext.from_headers(headers)
            self.context.service_name = service_name
            self.context.operation_name = operation_name
        else:
            self.context = RequestContext(
                request_id=request_id or str(uuid.uuid4()),
                service_name=service_name,
                operation_name=operation_name,
                **kwargs
            )
        self.token: Optional[contextvars.Token] = None

    def __enter__(self) -> RequestContext:
        """Enter context."""
        self.token = set_current_context(self.context)
        return self.context

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context."""
        clear_current_context(self.token)

    async def __aenter__(self) -> RequestContext:
        """Async enter context."""
        self.token = set_current_context(self.context)
        return self.context

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async exit context."""
        clear_current_context(self.token)


class child_span:
    """
    Context manager for creating child spans.

    Example:
        with child_span("database_query") as span:
            result = db.execute(query)
    """

    def __init__(self, operation_name: str):
        """
        Initialize child span.

        Args:
            operation_name: Name of the child operation
        """
        self.operation_name = operation_name
        self.parent_context: Optional[RequestContext] = None
        self.child_context: Optional[RequestContext] = None
        self.token: Optional[contextvars.Token] = None

    def __enter__(self) -> RequestContext:
        """Enter child span."""
        self.parent_context = get_current_context()

        if self.parent_context:
            self.child_context = self.parent_context.create_child_span(
                self.operation_name
            )
        else:
            self.child_context = RequestContext(operation_name=self.operation_name)

        self.token = set_current_context(self.child_context)
        return self.child_context

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit child span."""
        if self.token:
            clear_current_context(self.token)

        # Restore parent context
        if self.parent_context:
            set_current_context(self.parent_context)

    async def __aenter__(self) -> RequestContext:
        """Async enter child span."""
        return self.__enter__()

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async exit child span."""
        self.__exit__(exc_type, exc_val, exc_tb)


# =============================================================================
# Decorators
# =============================================================================

def with_request_context(
    operation_name: Optional[str] = None,
    service_name: str = "unknown"
) -> Callable[[F], F]:
    """
    Decorator to ensure request context exists.

    Creates context if none exists, uses existing otherwise.

    Args:
        operation_name: Name for the operation (defaults to function name)
        service_name: Name of the service

    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        op_name = operation_name or func.__name__

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            ctx = get_current_context()
            if ctx:
                return func(*args, **kwargs)

            with request_context(
                service_name=service_name,
                operation_name=op_name
            ):
                return func(*args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            ctx = get_current_context()
            if ctx:
                return await func(*args, **kwargs)

            async with request_context(
                service_name=service_name,
                operation_name=op_name
            ):
                return await func(*args, **kwargs)

        if asyncio_iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


def propagate_context(func: F) -> F:
    """
    Decorator to propagate context to child operations.

    Automatically creates child spans for nested operations.
    """
    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        with child_span(func.__name__):
            return func(*args, **kwargs)

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        async with child_span(func.__name__):
            return await func(*args, **kwargs)

    if asyncio_iscoroutinefunction(func):
        return async_wrapper  # type: ignore
    return sync_wrapper  # type: ignore


def asyncio_iscoroutinefunction(func: Any) -> bool:
    """Check if function is a coroutine function."""
    import asyncio
    return asyncio.iscoroutinefunction(func)


# =============================================================================
# Logging Integration
# =============================================================================

class RequestContextFilter(logging.Filter):
    """
    Logging filter that adds request context to log records.

    Example:
        handler.addFilter(RequestContextFilter())
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Add context to log record."""
        ctx = get_current_context()

        if ctx:
            record.request_id = ctx.request_id
            record.correlation_id = ctx.correlation_id
            record.trace_id = ctx.trace_id
            record.span_id = ctx.span_id
            record.service = ctx.service_name
            record.operation = ctx.operation_name
        else:
            record.request_id = "-"
            record.correlation_id = "-"
            record.trace_id = "-"
            record.span_id = "-"
            record.service = "-"
            record.operation = "-"

        return True


class ContextAwareLogger(logging.LoggerAdapter):
    """
    Logger adapter that automatically includes request context.

    Example:
        logger = ContextAwareLogger(logging.getLogger(__name__))
        logger.info("Processing request")  # Automatically includes context
    """

    def process(
        self,
        msg: str,
        kwargs: Dict[str, Any]
    ) -> tuple[str, Dict[str, Any]]:
        """Add context to log message."""
        ctx = get_current_context()

        if ctx:
            extra = kwargs.get('extra', {})
            extra.update(ctx.to_log_extra())
            kwargs['extra'] = extra

        return msg, kwargs


def get_context_logger(name: str) -> ContextAwareLogger:
    """
    Get a logger that automatically includes request context.

    Args:
        name: Logger name

    Returns:
        ContextAwareLogger instance
    """
    return ContextAwareLogger(logging.getLogger(name), {})


# =============================================================================
# Flask Integration
# =============================================================================

def create_flask_middleware():
    """
    Create Flask middleware for request context propagation.

    Returns:
        Tuple of (before_request, after_request) functions
    """
    from flask import g, request as flask_request

    def before_request() -> None:
        """Extract or create request context before handling."""
        # Extract from headers
        headers = dict(flask_request.headers)
        ctx = RequestContext.from_headers(headers)
        ctx.service_name = "debvisor-panel"
        ctx.operation_name = f"{flask_request.method} {flask_request.path}"

        # Store in Flask's g object
        g.request_context = ctx
        g.context_token = set_current_context(ctx)

    def after_request(response):
        """Add context headers to response and cleanup."""
        ctx = getattr(g, 'request_context', None)

        if ctx:
            # Add response headers
            response.headers[HEADER_REQUEST_ID] = ctx.request_id
            response.headers[HEADER_CORRELATION_ID] = ctx.correlation_id or ctx.request_id

            # Cleanup
            token = getattr(g, 'context_token', None)
            clear_current_context(token)

        return response

    return before_request, after_request


def init_flask_context_propagation(app) -> None:
    """
    Initialize request context propagation for Flask app.

    Args:
        app: Flask application
    """
    before, after = create_flask_middleware()
    app.before_request(before)
    app.after_request(after)

    logger.info("Flask request context propagation initialized")


# =============================================================================
# HTTP Client Integration
# =============================================================================

def inject_context_headers(
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    """
    Inject current context into outgoing request headers.

    Args:
        headers: Existing headers (optional)

    Returns:
        Headers with context injected
    """
    result = dict(headers) if headers else {}

    ctx = get_current_context()
    if ctx:
        # Create child span for outgoing request
        child = ctx.create_child_span("http_request")
        result.update(child.to_headers())
    else:
        # Generate new request ID
        result[HEADER_REQUEST_ID] = str(uuid.uuid4())

    return result


class ContextPropagatingSession:
    """
    HTTP session that automatically propagates request context.

    Wraps requests.Session to add context headers to all requests.

    Example:
        session = ContextPropagatingSession()
        response = session.get("http://other-service/api/data")
    """

    def __init__(self, session: Optional[Any] = None):
        """
        Initialize session wrapper.

        Args:
            session: Existing requests.Session (optional)
        """
        import requests
        self.session = session or requests.Session()

    def _prepare_headers(
        self,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        """Prepare headers with context."""
        return inject_context_headers(headers)

    def get(self, url: str, **kwargs: Any) -> Any:
        """GET request with context propagation."""
        kwargs['headers'] = self._prepare_headers(kwargs.get('headers'))
        return self.session.get(url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> Any:
        """POST request with context propagation."""
        kwargs['headers'] = self._prepare_headers(kwargs.get('headers'))
        return self.session.post(url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> Any:
        """PUT request with context propagation."""
        kwargs['headers'] = self._prepare_headers(kwargs.get('headers'))
        return self.session.put(url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> Any:
        """DELETE request with context propagation."""
        kwargs['headers'] = self._prepare_headers(kwargs.get('headers'))
        return self.session.delete(url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> Any:
        """PATCH request with context propagation."""
        kwargs['headers'] = self._prepare_headers(kwargs.get('headers'))
        return self.session.patch(url, **kwargs)


# =============================================================================
# Message Queue Integration
# =============================================================================

def inject_context_to_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inject request context into a message for queue propagation.

    Args:
        message: Message to enhance

    Returns:
        Message with context metadata
    """
    ctx = get_current_context()

    if ctx:
        message['_context'] = {
            'request_id': ctx.request_id,
            'correlation_id': ctx.correlation_id,
            'trace_id': ctx.trace_id,
            'span_id': ctx.span_id,
            'causation_id': ctx.span_id,  # Current span becomes cause
        }

    return message


def extract_context_from_message(message: Dict[str, Any]) -> Optional[RequestContext]:
    """
    Extract request context from a queue message.

    Args:
        message: Message to extract from

    Returns:
        RequestContext if present
    """
    ctx_data = message.get('_context')

    if ctx_data:
        return RequestContext(
            request_id=ctx_data.get('request_id', str(uuid.uuid4())),
            correlation_id=ctx_data.get('correlation_id'),
            trace_id=ctx_data.get('trace_id'),
            parent_span_id=ctx_data.get('span_id'),
            causation_id=ctx_data.get('causation_id'),
        )

    return None


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # Demo
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(request_id)s] %(name)s - %(message)s'
    )

    # Add filter to root logger
    for handler in logging.root.handlers:
        handler.addFilter(RequestContextFilter())

    demo_logger = get_context_logger(__name__)

    # Test context propagation
    with request_context(service_name="demo", operation_name="main") as ctx:
        demo_logger.info("Starting operation")

        with child_span("sub_operation"):
            demo_logger.info("In child span")

        demo_logger.info("Back in parent")

        # Test header injection
        headers = inject_context_headers()
        print(f"Outgoing headers: {headers}")

    print("Demo complete!")
