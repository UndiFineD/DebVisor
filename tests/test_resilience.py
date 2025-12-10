#!/usr/bin/env python3
"""
Tests for Enterprise Resilience Patterns.

Tests circuit breaker, retry with backoff, bulkhead, rate limiter,
and other resilience patterns.

Author: DebVisor Team
Date: November 28, 2025
"""

import asyncio
import pytest
from services.resilience import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState,
    CircuitOpenError,
    RetryConfig,
    retry_with_backoff,
    Bulkhead,
    BulkheadFullError,
    RateLimiter,
    RateLimitExceededError,
    with_timeout,
    resilient,
    get_or_create_circuit_breaker,
)

# =============================================================================
# Circuit Breaker Tests
# =============================================================================


class TestCircuitBreaker:
    """Test suite for CircuitBreaker."""

    @pytest.fixture
    def breaker(self) -> None:
        """Create circuit breaker with test config."""
        config = CircuitBreakerConfig(
            failure_threshold=3,
            success_threshold=2,
            timeout_seconds=1.0,
            half_open_max_calls=2,
        )
        return CircuitBreaker("test-breaker", config)

    @pytest.mark.asyncio
    async def test_initial_state_closed(self, breaker):
        """Circuit should start in closed state."""
        assert breaker.state == CircuitState.CLOSED
        assert breaker.is_closed

    @pytest.mark.asyncio
    async def test_success_keeps_circuit_closed(self, breaker):
        """Successful calls should keep circuit closed."""

        @breaker
        async def success_func() -> None:
            return "success"  # type: ignore[return-value]

        result = await success_func()

        assert result == "success"
        assert breaker.state == CircuitState.CLOSED
        assert breaker.metrics.successful_calls == 1

    @pytest.mark.asyncio
    async def test_failures_open_circuit(self, breaker):
        """Failures should open circuit after threshold."""

        @breaker
        async def failing_func() -> None:
            raise ValueError("test error")

        # Fail 3 times (threshold)
        for _ in range(3):
            with pytest.raises(ValueError):
                await failing_func()

        assert breaker.state == CircuitState.OPEN
        assert breaker.metrics.failed_calls == 3

    @pytest.mark.asyncio
    async def test_open_circuit_rejects_calls(self, breaker):
        """Open circuit should reject calls immediately."""

        # Open the circuit
        @breaker
        async def failing_func() -> None:
            raise ValueError("test error")

        for _ in range(3):
            with pytest.raises(ValueError):
                await failing_func()

        assert breaker.state == CircuitState.OPEN

        # New calls should be rejected
        @breaker
        async def normal_func() -> None:
            return "success"  # type: ignore[return-value]

        with pytest.raises(CircuitOpenError):
            await normal_func()

        assert breaker.metrics.rejected_calls == 1

    @pytest.mark.asyncio
    async def test_half_open_after_timeout(self, breaker):
        """Circuit should transition to half-open after timeout."""

        @breaker
        async def failing_func() -> None:
            raise ValueError("test error")

        for _ in range(3):
            with pytest.raises(ValueError):
                await failing_func()

        assert breaker.state == CircuitState.OPEN

        # Wait for timeout
        await asyncio.sleep(1.1)

        # Next call should be allowed (half-open)
        @breaker
        async def success_func() -> None:
            return "success"  # type: ignore[return-value]

        result = await success_func()
        assert result == "success"
        # State should have transitioned
        assert breaker.state in (CircuitState.HALF_OPEN, CircuitState.CLOSED)

    @pytest.mark.asyncio
    async def test_manual_reset(self, breaker):
        """Circuit can be manually reset."""

        @breaker
        async def failing_func() -> None:
            raise ValueError("test error")

        for _ in range(3):
            with pytest.raises(ValueError):
                await failing_func()

        assert breaker.state == CircuitState.OPEN

        await breaker.reset()

        assert breaker.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_metrics_tracking(self, breaker):
        """Metrics should be tracked correctly."""

        @breaker
        async def mixed_func(succeed: bool) -> str:
            if not succeed:
                raise ValueError("test")
            return "success"

        await mixed_func(True)
        await mixed_func(True)
        with pytest.raises(ValueError):
            await mixed_func(False)

        assert breaker.metrics.total_calls == 3
        assert breaker.metrics.successful_calls == 2
        assert breaker.metrics.failed_calls == 1


# =============================================================================
# Retry Tests
# =============================================================================


class TestRetryWithBackoff:
    """Test suite for retry_with_backoff."""

    @pytest.mark.asyncio
    async def test_success_no_retry(self) -> None:
        """Successful call should not retry."""
        call_count = 0

        @retry_with_backoff(RetryConfig(max_attempts=3))
        async def success_func() -> None:
            nonlocal call_count
            call_count += 1
            return "success"  # type: ignore[return-value]

        result = await success_func()

        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_retry_on_failure(self) -> None:
        """Should retry on failure."""
        call_count = 0

        @retry_with_backoff(RetryConfig(max_attempts=3, base_delay_seconds=0.01))
        async def flaky_func() -> None:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("test error")
            return "success"  # type: ignore[return-value]

        result = await flaky_func()

        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_max_attempts_exhausted(self) -> None:
        """Should raise after max attempts."""
        call_count = 0

        @retry_with_backoff(RetryConfig(max_attempts=3, base_delay_seconds=0.01))
        async def always_fail() -> None:
            nonlocal call_count
            call_count += 1
            raise ValueError("always fails")

        with pytest.raises(ValueError, match="always fails"):
            await always_fail()

        assert call_count == 3

    @pytest.mark.asyncio
    async def test_non_retryable_exception(self) -> None:
        """Non-retryable exceptions should raise immediately."""
        call_count = 0

        @retry_with_backoff(
            RetryConfig(
                max_attempts=3,
                retryable_exceptions={ValueError},
                non_retryable_exceptions={TypeError},
            )
        )
        async def type_error_func() -> None:
            nonlocal call_count
            call_count += 1
            raise TypeError("not retryable")

        with pytest.raises(TypeError):
            await type_error_func()

        assert call_count == 1    # No retry


# =============================================================================
# Bulkhead Tests
# =============================================================================


class TestBulkhead:
    """Test suite for Bulkhead."""

    @pytest.mark.asyncio
    async def test_allows_concurrent_calls(self) -> None:
        """Should allow calls up to max_concurrent."""
        bulkhead = Bulkhead("test", max_concurrent=2, max_wait_seconds=0.1)
        results = []

        @bulkhead
        async def slow_func(id: int) -> None:
            results.append(f"start-{id}")
            await asyncio.sleep(0.05)
            results.append(f"end-{id}")
            return id  # type: ignore[return-value]

        # Start 2 concurrent calls (should succeed)
        await asyncio.gather(slow_func(1), slow_func(2))

        assert len(results) == 4

    @pytest.mark.asyncio
    async def test_rejects_over_capacity(self) -> None:
        """Should reject calls when at capacity."""
        bulkhead = Bulkhead("test", max_concurrent=1, max_wait_seconds=0.01)

        @bulkhead
        async def slow_func() -> None:
            await asyncio.sleep(0.1)
            return "done"  # type: ignore[return-value]

        # Start first call
        task1 = asyncio.create_task(slow_func())
        await asyncio.sleep(0.01)    # Let it acquire semaphore

        # Second call should be rejected (timeout waiting)
        with pytest.raises(BulkheadFullError):
            await slow_func()

        await task1    # Cleanup


# =============================================================================
# Rate Limiter Tests
# =============================================================================


class TestRateLimiter:
    """Test suite for RateLimiter."""

    @pytest.mark.asyncio
    async def test_allows_under_limit(self) -> None:
        """Should allow requests under limit."""
        limiter = RateLimiter("test", rate=10, per_seconds=1.0)

        @limiter
        async def limited_func() -> None:
            return "success"  # type: ignore[return-value]

        # Should allow 10 calls
        for _ in range(10):
            result = await limited_func()
            assert result == "success"

    @pytest.mark.asyncio
    async def test_rejects_over_limit(self) -> None:
        """Should reject requests over limit."""
        limiter = RateLimiter("test", rate=2, per_seconds=1.0, burst=2)

        @limiter
        async def limited_func() -> None:
            return "success"  # type: ignore[return-value]

        # Use up tokens
        await limited_func()
        await limited_func()

        # Third call should fail
        with pytest.raises(RateLimitExceededError):
            await limited_func()

    @pytest.mark.asyncio
    async def test_refills_over_time(self) -> None:
        """Tokens should refill over time."""
        limiter = RateLimiter("test", rate=10, per_seconds=0.1, burst=2)

        @limiter
        async def limited_func() -> None:
            return "success"  # type: ignore[return-value]

        # Use up tokens
        await limited_func()
        await limited_func()

        # Wait for refill
        await asyncio.sleep(0.15)

        # Should work again
        result = await limited_func()
        assert result == "success"


# =============================================================================
# Timeout Tests
# =============================================================================


class TestTimeout:
    """Test suite for with_timeout."""

    @pytest.mark.asyncio
    async def test_completes_within_timeout(self) -> None:
        """Should complete if within timeout."""

        @with_timeout(1.0)
        async def fast_func() -> None:
            await asyncio.sleep(0.01)
            return "success"  # type: ignore[return-value]

        result = await fast_func()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_timeout_raises(self) -> None:
        """Should raise on timeout."""

        @with_timeout(0.01)
        async def slow_func() -> None:
            await asyncio.sleep(1.0)
            return "never"  # type: ignore[return-value]

        with pytest.raises(TimeoutError):
            await slow_func()

    @pytest.mark.asyncio
    async def test_timeout_with_fallback(self) -> None:
        """Should use fallback on timeout."""

        @with_timeout(0.01, fallback=lambda: "fallback")
        async def slow_func() -> None:
            await asyncio.sleep(1.0)
            return "never"  # type: ignore[return-value]

        result = await slow_func()
        assert result == "fallback"


# =============================================================================
# Combined Resilience Tests
# =============================================================================


class TestCombinedResilience:
    """Test combined resilience patterns."""

    @pytest.mark.asyncio
    async def test_resilient_decorator(self) -> None:
        """Combined resilient decorator should work."""
        breaker = CircuitBreaker("combined", CircuitBreakerConfig(failure_threshold=5))
        limiter = RateLimiter("combined", rate=100, per_seconds=1.0)

        @resilient(circuit_breaker=breaker, rate_limiter=limiter, timeout_seconds=5.0)
        async def resilient_func() -> None:
            return "success"  # type: ignore[return-value]

        result = await resilient_func()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_global_registry(self) -> None:
        """Should create and reuse circuit breakers."""
        breaker1 = get_or_create_circuit_breaker("test-global")
        breaker2 = get_or_create_circuit_breaker("test-global")

        assert breaker1 is breaker2


# =============================================================================
# Main
# =============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
