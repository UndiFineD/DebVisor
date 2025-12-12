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
Error handling and recovery utilities for DebVisor RPC service.

Provides:
- Custom exception hierarchy
- Error context and recovery information
- Retry mechanisms with exponential backoff
- Error recovery procedures
- Error logging and metrics integration
"""

import logging
import time
from typing import Callable, Type, TypeVar, Optional, List, Dict, Any, Tuple
from functools import wraps
from enum import Enum

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ErrorSeverity(Enum):
    """Error severity levels for classification."""

    LOW = "low"    # User error, non-critical
    MEDIUM = "medium"    # Service error, recoverable
    HIGH = "high"    # Service error, may impact operations
    CRITICAL = "critical"    # Service failure, immediate action required


class DebVisorRPCError(Exception):
    """Base exception for DebVisor RPC service."""

    def __init__(
        self,
        message: str,
        error_code: str = "RPC_ERROR",
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        recoverable: bool = False,
        recovery_steps: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.severity = severity
        self.recoverable = recoverable
        self.recovery_steps = recovery_steps or []
        self.context = context or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging/response."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "severity": self.severity.value,
            "recoverable": self.recoverable,
            "recovery_steps": self.recovery_steps,
            "context": self.context,
        }


class AuthenticationError(DebVisorRPCError):
    """Authentication failure."""

    def __init__(self, message: str, reason: str = "invalid_credentials", **kwargs: Any) -> None:
        super().__init__(
            message,
            error_code="AUTH_ERROR",
            severity=ErrorSeverity.MEDIUM,
            recoverable=True,
            recovery_steps=[
                "Verify credentials are correct",
                "Check certificate validity (mTLS)",
                "Verify API key has not been revoked",
                "Check JWT token has not expired",
            ],
            **kwargs,
        )
        self.reason = reason


class AuthorizationError(DebVisorRPCError):
    """Authorization failure (insufficient permissions)."""

    def __init__(self, resource: str, action: str, role: str, **kwargs: Any) -> None:
        message = f"User role '{role}' cannot {action} {resource}"
        super().__init__(
            message,
            error_code="AUTHZ_ERROR",
            severity=ErrorSeverity.MEDIUM,
            recoverable=False,
            recovery_steps=[
                f"Request elevated privileges for {action} on {resource}",
                "Contact administrator to grant required permissions",
            ],
            context={"resource": resource, "action": action, "role": role},
            **kwargs,
        )


class ValidationError(DebVisorRPCError):
    """Input validation failure."""

    def __init__(self, field: str, reason: str, value: str = "", **kwargs: Any) -> None:
        message = f"Validation failed for field '{field}': {reason}"
        super().__init__(
            message,
            error_code="VALIDATION_ERROR",
            severity=ErrorSeverity.LOW,
            recoverable=True,
            recovery_steps=[
                f"Verify {field} format is correct",
                "Check for special characters or invalid values",
                "Consult API documentation for field requirements",
            ],
            context={"field": field, "reason": reason, "value": value},
            **kwargs,
        )


class RateLimitError(DebVisorRPCError):
    """Rate limit exceeded."""

    def __init__(self, client_id: str, limit: int, window_seconds: int, **kwargs: Any) -> None:
        message = f"Rate limit exceeded: {limit} requests per {window_seconds}s"
        super().__init__(
            message,
            error_code="RATE_LIMIT_ERROR",
            severity=ErrorSeverity.LOW,
            recoverable=True,
            recovery_steps=[
                f"Wait {window_seconds} seconds before retrying",
                "Consider reducing request frequency",
                "Contact administrator for rate limit increase",
            ],
            context={
                "client_id": client_id,
                "limit": limit,
                "window_seconds": window_seconds,
            },
            **kwargs,
        )


class ServiceUnavailableError(DebVisorRPCError):
    """Service temporarily unavailable."""

    def __init__(self, service: str, reason: str = "unknown", **kwargs: Any) -> None:
        message = f"Service '{service}' is temporarily unavailable"
        super().__init__(
            message,
            error_code="SERVICE_UNAVAILABLE",
            severity=ErrorSeverity.HIGH,
            recoverable=True,
            recovery_steps=[
                "Wait a few moments and retry",
                f"Check health status of {service}",
                "Review recent logs for errors",
                "Contact administrator if problem persists",
            ],
            context={"service": service, "reason": reason},
            **kwargs,
        )


class ConnectionError(DebVisorRPCError):
    """Connection failure (network, timeout, etc)."""

    def __init__(self, target: str, reason: str, timeout_seconds: int = 0, **kwargs: Any) -> None:
        message = f"Connection failed to {target}: {reason}"
        super().__init__(
            message,
            error_code="CONNECTION_ERROR",
            severity=ErrorSeverity.HIGH,
            recoverable=True,
            recovery_steps=[
                "Check network connectivity to target service",
                "Verify target service is running and accessible",
                "Check firewall rules and network configuration",
                "Verify DNS resolution if using hostnames",
            ],
            context={
                "target": target,
                "reason": reason,
                "timeout_seconds": timeout_seconds,
            },
            **kwargs,
        )


class CertificateError(DebVisorRPCError):
    """TLS certificate error."""

    def __init__(self, cert_name: str, reason: str, **kwargs: Any) -> None:
        message = f"Certificate error for '{cert_name}': {reason}"
        super().__init__(
            message,
            error_code="CERTIFICATE_ERROR",
            severity=ErrorSeverity.CRITICAL,
            recoverable=True,
            recovery_steps=[
                f"Check certificate validity: openssl x509 -in {cert_name} -noout -dates",
                "Verify certificate has not expired",
                "Check certificate is properly signed",
                "Renew certificate if expired or approaching expiration",
            ],
            context={"cert_name": cert_name, "reason": reason},
            **kwargs,
        )


class DatabaseError(DebVisorRPCError):
    """Database operation failure."""

    def __init__(self, operation: str, reason: str, recoverable: bool = True, **kwargs: Any) -> None:
        message = f"Database operation failed: {operation}"
        super().__init__(
            message,
            error_code="DATABASE_ERROR",
            severity=ErrorSeverity.HIGH if recoverable else ErrorSeverity.CRITICAL,
            recoverable=recoverable,
            recovery_steps=[
                "Check database connectivity",
                "Verify database service is running",
                "Check available disk space",
                "Review database logs for detailed errors",
                "Consider database recovery procedures if data corruption suspected",
            ],
            context={"operation": operation, "reason": reason},
            **kwargs,
        )


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    on_retry: Optional[Callable[[int, float, Exception], None]] = None,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for automatic retry with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        max_delay: Maximum delay between retries
        exponential_base: Base for exponential backoff calculation
        jitter: Add random jitter to delay to prevent thundering herd
        on_retry: Callback function called on each retry
        retryable_exceptions: Exception types that trigger retry
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Optional[Exception] = None
            delay = initial_delay

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e

                    if attempt < max_retries:
                    # Calculate delay with exponential backoff
                        delay = min(
                            initial_delay * (exponential_base**attempt), max_delay
                        )

                        # Add jitter if enabled
                        if jitter:
                            import random

                            delay = delay * (0.5 + random.random())    # nosec B311

                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}. "
                            f"Retrying in {delay:.2f}s. Error: {str(e)}"
                        )

                        if on_retry:
                            on_retry(attempt, delay, e)

                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}. "
                            f"Last error: {str(e)}"
                        )

            if last_exception:
                raise last_exception
            raise DebVisorRPCError("Retry failed without exception")

        return wrapper

    return decorator


def log_error_with_context(
    error: DebVisorRPCError, request_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log error with full context for debugging.

    Args:
        error: The error to log
        request_info: Additional request context to include in log
    """
    error_dict = error.to_dict()
    if request_info:
        error_dict["request_context"] = request_info

    log_func = {
        ErrorSeverity.LOW: logger.info,
        ErrorSeverity.MEDIUM: logger.warning,
        ErrorSeverity.HIGH: logger.error,
        ErrorSeverity.CRITICAL: logger.critical,
    }[error.severity]

    log_func(f"Error [{error.error_code}]: {error_dict}")


def error_to_grpc_status(error: DebVisorRPCError) -> Any:
    """
    Convert DebVisor error to gRPC status code.

    Maps error types to appropriate gRPC status codes.
    """
    import grpc

    mapping = {
        "AUTH_ERROR": grpc.StatusCode.UNAUTHENTICATED,
        "AUTHZ_ERROR": grpc.StatusCode.PERMISSION_DENIED,
        "VALIDATION_ERROR": grpc.StatusCode.INVALID_ARGUMENT,
        "RATE_LIMIT_ERROR": grpc.StatusCode.RESOURCE_EXHAUSTED,
        "SERVICE_UNAVAILABLE": grpc.StatusCode.UNAVAILABLE,
        "CONNECTION_ERROR": grpc.StatusCode.UNAVAILABLE,
        "CERTIFICATE_ERROR": grpc.StatusCode.UNAVAILABLE,
        "DATABASE_ERROR": grpc.StatusCode.INTERNAL,
        "RPC_ERROR": grpc.StatusCode.INTERNAL,
    }

    return mapping.get(error.error_code, grpc.StatusCode.UNKNOWN)
