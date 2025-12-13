# Code Issues Report: tests\test_resilience.py

Generated: 2025-12-13T17:20:24.477690
Source: tests\test_resilience.py

## Issues Summary

Total: 30 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 51 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 52 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 64 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 65 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 66 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 81 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 82 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 97 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 107 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 121 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 132 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 134 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 148 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 152 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 169 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 170 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 171 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 193 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 194 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 211 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 212 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 228 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 250 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 275 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 316 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 353 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 372 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 396 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 416 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 424 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 30 issues to fix

### Issue at Line 51

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    @pytest.mark.asyncio
    async def test_initial_state_closed(self, breaker):
        """Circuit should start in closed state."""
        assert breaker.state == CircuitState.CLOSED
        assert breaker.is_closed

    @pytest.mark.asyncio
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 52

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    async def test_initial_state_closed(self, breaker):
        """Circuit should start in closed state."""
        assert breaker.state == CircuitState.CLOSED
        assert breaker.is_closed

    @pytest.mark.asyncio
    async def test_success_keeps_circuit_closed(self, breaker):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 64

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        result = await success_func()

        assert result == "success"
        assert breaker.state == CircuitState.CLOSED
        assert breaker.metrics.successful_calls == 1

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 65

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        result = await success_func()

        assert result == "success"
        assert breaker.state == CircuitState.CLOSED
        assert breaker.metrics.successful_calls == 1

    @pytest.mark.asyncio
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 66

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        assert result == "success"
        assert breaker.state == CircuitState.CLOSED
        assert breaker.metrics.successful_calls == 1

    @pytest.mark.asyncio
    async def test_failures_open_circuit(self, breaker):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 81

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            with pytest.raises(ValueError):
                await failing_func()

        assert breaker.state == CircuitState.OPEN
        assert breaker.metrics.failed_calls == 3

    @pytest.mark.asyncio
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 82

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
                await failing_func()

        assert breaker.state == CircuitState.OPEN
        assert breaker.metrics.failed_calls == 3

    @pytest.mark.asyncio
    async def test_open_circuit_rejects_calls(self, breaker):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 97

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            with pytest.raises(ValueError):
                await failing_func()

        assert breaker.state == CircuitState.OPEN

        # New calls should be rejected
        @breaker
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 107

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        with pytest.raises(CircuitOpenError):
            await normal_func()

        assert breaker.metrics.rejected_calls == 1

    @pytest.mark.asyncio
    async def test_half_open_after_timeout(self, breaker):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 121

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            with pytest.raises(ValueError):
                await failing_func()

        assert breaker.state == CircuitState.OPEN

        # Wait for timeout
        await asyncio.sleep(1.1)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 132

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            return "success"

        result = await success_func()
        assert result == "success"
        # State should have transitioned
        assert breaker.state in (CircuitState.HALF_OPEN, CircuitState.CLOSED)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 134

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        result = await success_func()
        assert result == "success"
        # State should have transitioned
        assert breaker.state in (CircuitState.HALF_OPEN, CircuitState.CLOSED)

    @pytest.mark.asyncio
    async def test_manual_reset(self, breaker):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 148

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            with pytest.raises(ValueError):
                await failing_func()

        assert breaker.state == CircuitState.OPEN

        await breaker.reset()

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 152

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        await breaker.reset()

        assert breaker.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_metrics_tracking(self, breaker):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 169

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        with pytest.raises(ValueError):
            await mixed_func(False)

        assert breaker.metrics.total_calls == 3
        assert breaker.metrics.successful_calls == 2
        assert breaker.metrics.failed_calls == 1

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 170

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            await mixed_func(False)

        assert breaker.metrics.total_calls == 3
        assert breaker.metrics.successful_calls == 2
        assert breaker.metrics.failed_calls == 1

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 171

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        assert breaker.metrics.total_calls == 3
        assert breaker.metrics.successful_calls == 2
        assert breaker.metrics.failed_calls == 1

## =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 193

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        result = await success_func()

        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 194

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        result = await success_func()

        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_retry_on_failure(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 211

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        result = await flaky_func()

        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 212

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        result = await flaky_func()

        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_max_attempts_exhausted(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 228

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        with pytest.raises(ValueError, match="always fails"):
            await always_fail()

        assert call_count == 3

    @pytest.mark.asyncio
    async def test_non_retryable_exception(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 250

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        with pytest.raises(TypeError):
            await type_error_func()

        assert call_count == 1    # No retry

## =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 275

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        # Start 2 concurrent calls (should succeed)
        await asyncio.gather(slow_func(1), slow_func(2))

        assert len(results) == 4

    @pytest.mark.asyncio
    async def test_rejects_over*capacity(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 316

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        # Should allow 10 calls
        for * in range(10):
            result = await limited_func()
            assert result == "success"

    @pytest.mark.asyncio
    async def test_rejects_over_limit(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 353

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        # Should work again
        result = await limited_func()
        assert result == "success"

## =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 372

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            return "success"

        result = await fast_func()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_timeout_raises(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 396

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            return "never"

        result = await slow_func()
        assert result == "fallback"

## =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 416

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            return "success"

        result = await resilient_func()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_global_registry(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 424

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        breaker1 = get_or_create_circuit_breaker("test-global")
        breaker2 = get_or_create_circuit_breaker("test-global")

        assert breaker1 is breaker2

## =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

## Implementation Progress

To mark an issue as fixed, add the issue code to the line below with a ✅ emoji:

**Fixed Issues:** (none yet)

---
*Updated: (auto-populated by coding expert)*
