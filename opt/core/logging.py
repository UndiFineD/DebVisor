#!/usr/bin/env python3
"""
DebVisor Structured Logging
===========================

Provides a centralized logging configuration for all DebVisor components.
Enables JSON-formatted logs with OpenTelemetry correlation IDs using structlog.
"""

import logging
import sys
import os
# from typing import Any, Callable, List, Optional

import structlog
from structlog.typing import EventDict

# Try to import OpenTelemetry for correlation
try:
    from opentelemetry import trace

    _OTEL_AVAILABLE = True
except ImportError:
    _OTEL_AVAILABLE = False


def add_opentelemetry_ids(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Add OpenTelemetry trace_id and span_id to the event dict."""
    if _OTEL_AVAILABLE:
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx.is_valid:
            event_dict["trace_id"] = f"{ctx.trace_id:032x}"
            event_dict["span_id"] = f"{ctx.span_id:016x}"
            event_dict["traceparent"] = (
                f"00-{event_dict['trace_id']}-{event_dict['span_id']}-01"
            )
    return event_dict


def configure_logging(
    service_name: str = "debvisor",
    log_level: Optional[str] = None,
    json_format: bool = True,
) -> None:
    """
    Configure the root logger and structlog.

    Args:
        service_name: Name of the service (added to all logs)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR).
                   Defaults to DEBVISOR_LOG_LEVEL env var or INFO.
        json_format: Whether to output JSON (default True).
                     Can be disabled via DEBVISOR_LOG_JSON=0.
    """

    # Determine settings from args or env
    if not log_level:
        log_level = os.getenv("DEBVISOR_LOG_LEVEL", "INFO").upper()

    if os.getenv("DEBVISOR_LOG_JSON", "1") == "0":
        json_format = False

    # Shared processors for both structlog and stdlib logging
    # These run BEFORE the renderer
    shared_processors: List[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        add_opentelemetry_ids,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Processors for structlog (ends with wrap_for_formatter)
    structlog_processors = shared_processors + [
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    # Configure structlog
    structlog.configure(
        processors=structlog_processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Renderer for the final output
    renderer: Any
    if json_format:
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create handler that uses structlog's ProcessorFormatter
    handler = logging.StreamHandler(sys.stdout)

    # Use ProcessorFormatter to wrap stdlib logs
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Set third-party loggers to WARNING
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("kubernetes").setLevel(logging.WARNING)

    # Bind service name to all logs
    structlog.contextvars.bind_contextvars(service_name=service_name)

    # Log startup
    logger = structlog.get_logger()
    logger.info("Logging configured", service_name=service_name, library="structlog")
