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
Enterprise Resilience Patterns for DebVisor Services.

Implements production-grade resilience patterns:
- Circuit Breaker with exponential backoff
- Retry decorator with jitter
- Bulkhead pattern for resource isolation
- Timeout management
- Fallback mechanisms
- Health-aware load balancing

These patterns ensure graceful degradation and fault tolerance
across distributed services.

Author: DebVisor Team
Date: November 28, 2025
"""

from datetime import datetime, timezone
from typing import TypeVar
from typing import Optional
import asyncio
import functools
import logging
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Awaitable, Callable, Dict, Set, cast

logger = logging.getLogger(__name__)

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])


# =============================================================================
# Circuit Breaker Pattern
# =============================================================================


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"    # Normal operation
    OPEN = "open"    # Failing, reject requests
    HALF_OPEN = "half_open"    # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""

    failure_threshold: int = 5    # Failures before opening
    success_threshold: int = 3    # Successes to close from half-open
    timeout_seconds: float = 30.0    # Time before half-open
    half_open_max_calls: int = 3    # Max calls in half-open state
    excluded_exceptions: Set[type] = field(default_factory=set)    # Don't count these


@dataclass
class CircuitBreakerMetrics:
    """Metrics for circuit breaker monitoring."""

    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0
    state_transitions: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    current_state: CircuitState = CircuitState.CLOSED

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "rejected_calls": self.rejected_calls,
            "state_transitions": self.state_transitions,
            "last_failure_time": (
                self.last_failure_time.isoformat() if self.last_failure_time else None
            ),
            "last_success_time": (
                self.last_success_time.isoformat() if self.last_success_time else None
            ),
            "current_state": self.current_state.value,
            "success_rate": self.success_rate,
        }

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_calls == 0:
            return 100.0
        return (self.successful_calls / self.total_calls) * 100


class CircuitBreaker:
    """
    Circuit breaker implementation for fault tolerance.

    Prevents cascading failures by failing fast when a service is unhealthy.

    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Service failing, reject all requests immediately
    - HALF_OPEN: Testing recovery, allow limited requests

    Example:
        breaker = CircuitBreaker("vault-service")

        @breaker
        async def call_vault():
            return await vault_client.get_secret("key")
    """

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        """
        Initialize circuit breaker.

        Args:
            name: Identifier for this circuit breaker
            config: Configuration options
        """
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0
        self._last_failure_time: Optional[datetime] = None
        self._lock = asyncio.Lock()
        self.metrics = CircuitBreakerMetrics()

        logger.info(f"Circuit breaker '{name}' initialized with config: {self.config}")

    @property
    def state(self) -> CircuitState:
        """Current circuit state."""
        return self._state

    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed (healthy)."""
        return self._state == CircuitState.CLOSED

    async def _transition_to(self, new_state: CircuitState) -> None:
        """Transition to a new state."""
        old_state = self._state
        self._state = new_state
        self.metrics.state_transitions += 1
        self.metrics.current_state = new_state

        logger.warning(
            f"Circuit breaker '{self.name}' state transition: "
            f"{old_state.value} -> {new_state.value}"
        )

        if new_state == CircuitState.CLOSED:
            self._failure_count = 0
            self._success_count = 0
        elif new_state == CircuitState.OPEN:
            self._last_failure_time = datetime.now(timezone.utc)
        elif new_state == CircuitState.HALF_OPEN:
            self._half_open_calls = 0
            self._success_count = 0

    async def _should_allow_request(self) -> bool:
        """Determine if a request should be allowed."""
        async with self._lock:
            if self._state == CircuitState.CLOSED:
                return True

            if self._state == CircuitState.OPEN:
                # Check if timeout has elapsed
                if self._last_failure_time:
                    elapsed = (
                        datetime.now(timezone.utc) - self._last_failure_time
                    ).total_seconds()
                    if elapsed >= self.config.timeout_seconds:
                        await self._transition_to(CircuitState.HALF_OPEN)
                        return True
                self.metrics.rejected_calls += 1
                return False

            if self._state == CircuitState.HALF_OPEN:
                if self._half_open_calls < self.config.half_open_max_calls:
                    self._half_open_calls += 1
                    return True
                self.metrics.rejected_calls += 1
                return False

    async def _record_success(self) -> None:
        """Record a successful call."""
        async with self._lock:
            self.metrics.successful_calls += 1
            self.metrics.last_success_time = datetime.now(timezone.utc)

            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.config.success_threshold:
                    await self._transition_to(CircuitState.CLOSED)

    async def _record_failure(self, exception: Exception) -> None:
        """Record a failed call."""
        async with self._lock:
            # Check if exception should be excluded
            if type(exception) in self.config.excluded_exceptions:
                return

            self.metrics.failed_calls += 1
            self.metrics.last_failure_time = datetime.now(timezone.utc)
            self._failure_count += 1

            if self._state == CircuitState.CLOSED:
                if self._failure_count >= self.config.failure_threshold:
                    await self._transition_to(CircuitState.OPEN)

            elif self._state == CircuitState.HALF_OPEN:
                await self._transition_to(CircuitState.OPEN)

    def __call__(self, func: F) -> F:
        """Decorator to wrap async functions with circuit breaker."""

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.metrics.total_calls += 1

            if not await self._should_allow_request():
                raise CircuitOpenError(
                    f"Circuit breaker '{self.name}' is OPEN. "
                    "Request rejected to prevent cascade failure."
                )

            try:
                result = await func(*args, **kwargs)
                await self._record_success()
                return result
            except Exception as e:
                await self._record_failure(e)
                raise

        return wrapper    # type: ignore

    async def reset(self) -> None:
        """Manually reset circuit breaker to CLOSED state."""
        async with self._lock:
            await self._transition_to(CircuitState.CLOSED)
            self._failure_count = 0
            self._success_count = 0
            logger.info(f"Circuit breaker '{self.name}' manually reset")


class CircuitOpenError(Exception):
    """Raised when circuit breaker is open and request is rejected."""

    pass


# =============================================================================
# Retry Pattern with Exponential Backoff
# =============================================================================


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""

    max_attempts: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True    # Add randomness to prevent thundering herd
    jitter_factor: float = 0.5    # Max jitter as fraction of delay
    retryable_exceptions: Set[type] = field(default_factory=lambda: {Exception})
    non_retryable_exceptions: Set[type] = field(default_factory=set)


def retry_with_backoff(
    config: Optional[RetryConfig] = None,
    on_retry: Optional[Callable[[int, Exception, float], None]] = None,
) -> Callable[[F], F]:
    """
    Decorator for retrying async functions with exponential backoff.

    Features:
    - Exponential backoff between retries
    - Jitter to prevent thundering herd
    - Configurable retry conditions
    - Callback on retry for logging/metrics

    Args:
        config: Retry configuration
        on_retry: Callback function(attempt, exception, delay)

    Example:
        @retry_with_backoff(RetryConfig(max_attempts=5))
        async def fetch_data():
            return await external_api.get_data()
    """
    config = config or RetryConfig()

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Optional[Exception] = None

            for attempt in range(1, config.max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    # Check if exception should not be retried
                    if type(e) in config.non_retryable_exceptions:
                        raise

                    # Check if exception is retryable
                    if not any(
                        isinstance(e, exc_type)
                        for exc_type in config.retryable_exceptions
                    ):
                        raise

                    # Last attempt, don't retry
                    if attempt == config.max_attempts:
                        logger.error(
                            f"All {config.max_attempts} retry attempts exhausted "
                            f"for {func.__name__}: {e}"
                        )
                        raise

                    # Calculate delay with exponential backoff
                    delay = min(
                        config.base_delay_seconds
                        * (config.exponential_base ** (attempt - 1)),
                        config.max_delay_seconds,
                    )

                    # Add jitter if enabled
                    if config.jitter:
                        jitter_range = delay * config.jitter_factor
                        delay += random.uniform(
                            -jitter_range, jitter_range
                        )    # nosec B311
                        delay = max(0.1, delay)    # Ensure positive delay

                    logger.warning(
                        f"Retry {attempt}/{config.max_attempts} for {func.__name__} "
                        f"after {delay:.2f}s due to: {e}"
                    )

                    if on_retry:
                        on_retry(attempt, e, delay)

                    await asyncio.sleep(delay)

            # Should never reach here, but just in case
            if last_exception:
                raise last_exception
            raise RuntimeError("Unexpected retry loop exit")

        return cast(F, wrapper)

    return decorator


# =============================================================================
# Timeout Pattern
# =============================================================================


def with_timeout(
    timeout_seconds: float, fallback: Optional[Callable[[], T]] = None
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """
    Decorator to add timeout to async functions.

    Args:
        timeout_seconds: Maximum execution time
        fallback: Optional fallback function if timeout occurs

    Example:
        @with_timeout(5.0, fallback=lambda: {"status": "timeout"})
        async def slow_operation():
            await external_service.call()
    """

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs), timeout=timeout_seconds
                )
            except asyncio.TimeoutError:
                logger.warning(f"Timeout after {timeout_seconds}s for {func.__name__}")
                if fallback:
                    return fallback()
                raise TimeoutError(
                    f"Operation {func.__name__} timed out after {timeout_seconds}s"
                )

        return wrapper

    return decorator


# =============================================================================
# Bulkhead Pattern (Resource Isolation)
# =============================================================================


class Bulkhead:
    """
    Bulkhead pattern for resource isolation.

    Limits concurrent executions to prevent one failing component
    from consuming all resources.

    Example:
        bulkhead = Bulkhead("database-pool", max_concurrent=10)

        @bulkhead
        async def query_database():
            return await db.execute(query)
    """

    def __init__(
        self, name: str, max_concurrent: int = 10, max_wait_seconds: float = 30.0
    ):
        """
        Initialize bulkhead.

        Args:
            name: Identifier for this bulkhead
            max_concurrent: Maximum concurrent executions
            max_wait_seconds: Maximum time to wait for a slot
        """
        self.name = name
        self.max_concurrent = max_concurrent
        self.max_wait_seconds = max_wait_seconds
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._current_count = 0
        self._rejected_count = 0
        self._lock = asyncio.Lock()

    @property
    def available_slots(self) -> int:
        """Number of available slots."""
        return self.max_concurrent - self._current_count

    def __call__(self, func: F) -> F:
        """Decorator to apply bulkhead to async function."""

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # Try to acquire with timeout
                acquired = await asyncio.wait_for(
                    self._semaphore.acquire(), timeout=self.max_wait_seconds
                )
                if not acquired:
                    raise BulkheadFullError(f"Bulkhead '{self.name}' is full")
            except asyncio.TimeoutError:
                async with self._lock:
                    self._rejected_count += 1
                raise BulkheadFullError(
                    f"Bulkhead '{self.name}' is full, "
                    f"waited {self.max_wait_seconds}s for a slot"
                )

            async with self._lock:
                self._current_count += 1

            try:
                return await func(*args, **kwargs)
            finally:
                async with self._lock:
                    self._current_count -= 1
                self._semaphore.release()

        return wrapper    # type: ignore

    def get_metrics(self) -> Dict[str, Any]:
        """Get bulkhead metrics."""
        return {
            "name": self.name,
            "max_concurrent": self.max_concurrent,
            "current_count": self._current_count,
            "available_slots": self.available_slots,
            "rejected_count": self._rejected_count,
        }


class BulkheadFullError(Exception):
    """Raised when bulkhead is at capacity."""

    pass


# =============================================================================
# Rate Limiter (Token Bucket Algorithm)
# =============================================================================


class RateLimiter:
    """
    Token bucket rate limiter.

    Limits request rate to prevent overwhelming services.

    Example:
        limiter = RateLimiter("api-calls", rate=100, per_seconds=60)

        @limiter
        async def call_api():
            return await api.request()
    """

    def __init__(
        self,
        name: str,
        rate: int,
        per_seconds: float = 1.0,
        burst: Optional[int] = None,
    ):
        """
        Initialize rate limiter.

        Args:
            name: Identifier for this limiter
            rate: Number of allowed requests
            per_seconds: Time period for rate
            burst: Maximum burst size (defaults to rate)
        """
        self.name = name
        self.rate = rate
        self.per_seconds = per_seconds
        self.burst = burst or rate

        self._tokens = float(self.burst)
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()
        self._rejected_count = 0

    async def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        tokens_to_add = (elapsed / self.per_seconds) * self.rate
        self._tokens = min(self.burst, self._tokens + tokens_to_add)
        self._last_refill = now

    async def acquire(self, tokens: int = 1) -> bool:
        """
        Try to acquire tokens.

        Args:
            tokens: Number of tokens to acquire

        Returns:
            True if tokens were acquired, False otherwise
        """
        async with self._lock:
            await self._refill()

            if self._tokens >= tokens:
                self._tokens -= tokens
                return True

            self._rejected_count += 1
            return False

    def __call__(self, func: F) -> F:
        """Decorator to apply rate limiting to async function."""

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not await self.acquire():
                raise RateLimitExceededError(
                    f"Rate limit exceeded for '{self.name}' "
                    f"({self.rate}/{self.per_seconds}s)"
                )
            return await func(*args, **kwargs)

        return wrapper    # type: ignore

    def get_metrics(self) -> Dict[str, Any]:
        """Get rate limiter metrics."""
        return {
            "name": self.name,
            "rate": self.rate,
            "per_seconds": self.per_seconds,
            "burst": self.burst,
            "current_tokens": self._tokens,
            "rejected_count": self._rejected_count,
        }


class RateLimitExceededError(Exception):
    """Raised when rate limit is exceeded."""

    pass


# =============================================================================
# Fallback Pattern
# =============================================================================


def with_fallback(
    fallback_func: Callable[..., T], exceptions: Optional[Set[type]] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator to provide fallback for failed operations.

    Args:
        fallback_func: Function to call on failure
        exceptions: Exception types to catch (default: all)

    Example:
        def get_cached_value():
            return cache.get("key")

        @with_fallback(get_cached_value)
        async def get_from_database():
            return await db.query("key")
    """
    exceptions = exceptions or {Exception}

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                result = func(*args, **kwargs)
                if asyncio.iscoroutine(result):
                    return await result    # type: ignore
                return result
            except Exception as e:
                if any(isinstance(e, exc_type) for exc_type in exceptions):
                    logger.warning(f"Falling back for {func.__name__} due to: {e}")
                    fallback_result = fallback_func(*args, **kwargs)
                    if asyncio.iscoroutine(fallback_result):
                        return await fallback_result    # type: ignore
                    return fallback_result
                raise

        return async_wrapper    # type: ignore

    return decorator


# =============================================================================
# Health-Aware Service Registry
# =============================================================================


@dataclass
class ServiceEndpoint:
    """Service endpoint with health tracking."""

    url: str
    weight: int = 100
    healthy: bool = True
    consecutive_failures: int = 0
    last_check: Optional[datetime] = None
    latency_ms: float = 0.0


class HealthAwareRegistry:
    """
    Service registry with health-aware load balancing.

    Routes requests to healthy endpoints and automatically
    removes unhealthy ones.
    """

    def __init__(
        self, name: str, failure_threshold: int = 3, recovery_threshold: int = 2
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_threshold = recovery_threshold
        self._endpoints: Dict[str, ServiceEndpoint] = {}
        self._lock = asyncio.Lock()

    async def register(self, endpoint_id: str, url: str, weight: int = 100) -> None:
        """Register a service endpoint."""
        async with self._lock:
            self._endpoints[endpoint_id] = ServiceEndpoint(
                url=url, weight=weight, healthy=True
            )
            logger.info(f"Registered endpoint '{endpoint_id}' at {url}")

    async def deregister(self, endpoint_id: str) -> None:
        """Remove a service endpoint."""
        async with self._lock:
            if endpoint_id in self._endpoints:
                del self._endpoints[endpoint_id]
                logger.info(f"Deregistered endpoint '{endpoint_id}'")

    async def get_healthy_endpoint(self) -> Optional[ServiceEndpoint]:
        """Get a healthy endpoint using weighted random selection."""
        async with self._lock:
            healthy = [e for e in self._endpoints.values() if e.healthy]
            if not healthy:
                return None

            # Weighted random selection
            total_weight = sum(e.weight for e in healthy)
            if total_weight == 0:
                return random.choice(healthy)    # nosec B311

            r = random.uniform(0, total_weight)    # nosec B311
            cumulative = 0
            for endpoint in healthy:
                cumulative += endpoint.weight
                if r <= cumulative:
                    return endpoint

            return healthy[-1]

    async def record_success(self, endpoint_id: str, latency_ms: float) -> None:
        """Record successful call to endpoint."""
        async with self._lock:
            if endpoint_id in self._endpoints:
                ep = self._endpoints[endpoint_id]
                ep.consecutive_failures = 0
                ep.last_check = datetime.now(timezone.utc)
                ep.latency_ms = latency_ms

                if not ep.healthy:
                    ep.healthy = True
                    logger.info(f"Endpoint '{endpoint_id}' recovered")

    async def record_failure(self, endpoint_id: str) -> None:
        """Record failed call to endpoint."""
        async with self._lock:
            if endpoint_id in self._endpoints:
                ep = self._endpoints[endpoint_id]
                ep.consecutive_failures += 1
                ep.last_check = datetime.now(timezone.utc)

                if ep.consecutive_failures >= self.failure_threshold:
                    ep.healthy = False
                    logger.warning(
                        f"Endpoint '{endpoint_id}' marked unhealthy "
                        f"after {ep.consecutive_failures} consecutive failures"
                    )

    def get_status(self) -> Dict[str, Any]:
        """Get registry status."""
        return {
            "name": self.name,
            "total_endpoints": len(self._endpoints),
            "healthy_endpoints": sum(1 for e in self._endpoints.values() if e.healthy),
            "endpoints": {
                eid: {
                    "url": e.url,
                    "healthy": e.healthy,
                    "weight": e.weight,
                    "consecutive_failures": e.consecutive_failures,
                    "latency_ms": e.latency_ms,
                }
                for eid, e in self._endpoints.items()
            },
        }


# =============================================================================
# Convenience: Combined Resilience Decorator
# =============================================================================


def resilient(
    circuit_breaker: Optional[CircuitBreaker] = None,
    retry_config: Optional[RetryConfig] = None,
    bulkhead: Optional[Bulkhead] = None,
    rate_limiter: Optional[RateLimiter] = None,
    timeout_seconds: Optional[float] = None,
) -> Callable[[F], F]:
    """
    Combined resilience decorator applying multiple patterns.

    Order of application (outermost to innermost):
    1. Rate limiter
    2. Bulkhead
    3. Circuit breaker
    4. Timeout
    5. Retry

    Example:
        @resilient(
            circuit_breaker=breaker,
            retry_config=RetryConfig(max_attempts=3),
            timeout_seconds=10.0
        )
        async def call_external_service():
            return await service.call()
    """

    def decorator(func: F) -> F:
        wrapped = func

        # Apply in reverse order (innermost first)
        if retry_config:
            wrapped = retry_with_backoff(retry_config)(wrapped)

        if timeout_seconds:
            wrapped = with_timeout(timeout_seconds)(wrapped)    # type: ignore

        if circuit_breaker:
            wrapped = circuit_breaker(wrapped)

        if bulkhead:
            wrapped = bulkhead(wrapped)

        if rate_limiter:
            wrapped = rate_limiter(wrapped)

        return wrapped

    return decorator


# =============================================================================
# Global Registry
# =============================================================================

_circuit_breakers: Dict[str, CircuitBreaker] = {}
_bulkheads: Dict[str, Bulkhead] = {}
_rate_limiters: Dict[str, RateLimiter] = {}


def get_or_create_circuit_breaker(
    name: str, config: Optional[CircuitBreakerConfig] = None
) -> CircuitBreaker:
    """Get or create a named circuit breaker."""
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(name, config)
    return _circuit_breakers[name]


def get_or_create_bulkhead(
    name: str, max_concurrent: int = 10, max_wait_seconds: float = 30.0
) -> Bulkhead:
    """Get or create a named bulkhead."""
    if name not in _bulkheads:
        _bulkheads[name] = Bulkhead(name, max_concurrent, max_wait_seconds)
    return _bulkheads[name]


def get_or_create_rate_limiter(
    name: str, rate: int, per_seconds: float = 1.0
) -> RateLimiter:
    """Get or create a named rate limiter."""
    if name not in _rate_limiters:
        _rate_limiters[name] = RateLimiter(name, rate, per_seconds)
    return _rate_limiters[name]


def get_all_metrics() -> Dict[str, Any]:
    """Get metrics from all resilience components."""
    return {
        "circuit_breakers": {
            name: cb.metrics.to_dict() for name, cb in _circuit_breakers.items()
        },
        "bulkheads": {name: bh.get_metrics() for name, bh in _bulkheads.items()},
        "rate_limiters": {
            name: rl.get_metrics() for name, rl in _rate_limiters.items()
        },
    }
