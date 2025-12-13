# Code Issues Report: tests\test_chaos_engineering.py

Generated: 2025-12-13T16:54:25.882726
Source: tests\test_chaos_engineering.py

## Issues Summary

Total: 20 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 112 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 119 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 163 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 176 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 179 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 184 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 190 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 197 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 202 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 208 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 296 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 319 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 338 | 0 | bandit | `B311` | LOW | Standard pseudo-random generators are not suitable for security/cryptographic purposes. |
| 446 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 460 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 477 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 511 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 529 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 542 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 584 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 20 issues to fix

### Issue at Line 112

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python

    def inject(self) -> float:
        """Add random latency and return the delay."""
        delay_ms = random.randint(self.min_ms, self.max_ms)
        delay_seconds = delay_ms / 1000.0
        time.sleep(delay_seconds)
        return delay_seconds
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 119

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python

    async def inject_async(self) -> float:
        """Add random latency asynchronously."""
        delay_ms = random.randint(self.min_ms, self.max_ms)
        delay_seconds = delay_ms / 1000.0
        await asyncio.sleep(delay_seconds)
        return delay_seconds
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 163

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python

    def inject(self) -> NoReturn:
        """Raise a random error for the target component."""
        error = random.choice(self.errors)
        # error is an Exception instance, raise its type with its message
        raise type(error)(str(error))

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 176

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python

    def corrupt_string(self, value: str) -> str:
        """Corrupt a string value."""
        if random.random() > self.corruption_rate:
            return value

        corruption_type = random.choice(["truncate", "garbage", "empty", "swap"])
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 179

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        if random.random() > self.corruption_rate:
            return value

        corruption_type = random.choice(["truncate", "garbage", "empty", "swap"])

        if corruption_type == "truncate":
            return value[: len(value) // 2]
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 184

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        if corruption_type == "truncate":
            return value[: len(value) // 2]
        elif corruption_type == "garbage":
            return value + "".join(random.choices("!@    #$%^&*()", k=5))
        elif corruption_type == "empty":
            return ""
        elif corruption_type == "swap":
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 190

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
        elif corruption_type == "swap":
            chars = list(value)
            if len(chars) > 1:
                i, j = random.sample(range(len(chars)), 2)
                chars[i], chars[j] = chars[j], chars[i]
            return "".join(chars)
        return value
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 197

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python

    def corrupt_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Corrupt dictionary values."""
        if random.random() > self.corruption_rate:
            return data

        corrupted = data.copy()
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 202

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python

        corrupted = data.copy()
        if corrupted:
            key = random.choice(list(corrupted.keys()))
            value = corrupted[key]

            if isinstance(value, str):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 208

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
            if isinstance(value, str):
                corrupted[key] = self.corrupt_string(value)
            elif isinstance(value, (int, float)):
                corrupted[key] = value * random.choice([-1, 0, 2, 10])
            elif isinstance(value, bool):
                corrupted[key] = not value
            elif value is None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 296

**Tool:**bandit |**Code:**`B311` |**Severity:** LOW

**Message:** Standard pseudo-random generators are not suitable for security/cryptographic purposes.

### Context

```python
            return False

        # Random probability
        return random.random()  0.5:
                    yield
                else:
                    raise Exception(f"Partial failure in {operation}")
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 446

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        )

        # Should eventually succeed or exhaust retries
        assert attempts <= max_attempts

    def test_database_latency_handling(self, chaos_monkey, mock_database):
        """Test: System handles database latency gracefully."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 460

**Tool:**bandit |**Code:**`B110` |**Severity:** LOW

**Message:** Try, Except, Pass detected.

### Context

```python
                    "db_query", TargetComponent.DATABASE, [FailureMode.LATENCY]
                ):
                    mock_database.query("SELECT 1")
            except Exception:
                pass
            latencies.append(time.time() - start)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 477

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        )

        # Verify latencies were tracked
        assert len(latencies) == 10

class TestCacheResilience:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 511

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            },
        )

        assert cache_available or data_retrieved

    def test_cache_write_through_failure(self, chaos_monkey, mock_cache, mock_database):
        """Test: Database write succeeds even if cache update fails."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 529

**Tool:**bandit |**Code:**`B110` |**Severity:** LOW

**Message:** Try, Except, Pass detected.

### Context

```python
            ):
                mock_cache.set("key", "data")
                cache_success = True
        except Exception:
            # Cache failure is acceptable
            pass

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 542

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        )

        # Database write must succeed regardless of cache
        assert db_success

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 584

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        )

        # Circuit should have opened
        assert circuit_open or failures < threshold

    def test_api_timeout_handling(self, chaos_monkey):
        """Test: API timeouts are handled with proper error responses."""
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
