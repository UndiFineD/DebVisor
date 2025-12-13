# Code Issues Report: tests\test_property_based.py

Generated: 2025-12-13T15:24:59.869534
Source: tests\test_property_based.py

## Issues Summary

Total: 39 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 146 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 153 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 154 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 169 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 181 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 182 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 194 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 201 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 209 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 221 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 222 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 230 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 246 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 255 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 278 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 308 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 309 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 310 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 311 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 333 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 336 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 337 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 360 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 376 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 377 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 394 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 417 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 418 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 419 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 436 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 437 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 454 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 455 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 456 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 465 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 466 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 467 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 481 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 482 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 39 issues to fix

### Issue at Line 146

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
            "original_amount",
            "status",
        }
        assert required_fields.issubset(debt.keys())

    @given(debt=debt_record())
    @settings(max_examples=100)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 153

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

    def test_debt_amounts_are_positive(self, debt: Dict[str, Any]) -> None:
        """Property: Debt amounts must be positive."""
        assert debt["original_amount"] > 0
        assert debt["current_balance"] >= 0

    @given(debt=debt_record())
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 154

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    def test_debt_amounts_are_positive(self, debt: Dict[str, Any]) -> None:
        """Property: Debt amounts must be positive."""
        assert debt["original_amount"] > 0
        assert debt["current_balance"] >= 0

    @given(debt=debt_record())
    @settings(max_examples=100)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 169

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
            "disputed",
            "cancelled",
        }
        assert debt["status"] in valid_statuses

    @given(original=money_strategy, payments=st.lists(money_strategy, max_size=10))
    @settings(max_examples=100)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 181

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        total_payments = sum(payments, Decimal("0"))
        balance = max(Decimal("0"), original - total_payments)

        assert balance >= 0
        assert balance <= original

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 182

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        balance = max(Decimal("0"), original - total_payments)

        assert balance >= 0
        assert balance <= original

class TestPaymentValidationProperties:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 194

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    def test_payment_has_required_fields(self, payment: Dict[str, Any]) -> None:
        """Property: All payments must have required fields."""
        required_fields = {"id", "debt_id", "amount", "method", "status"}
        assert required_fields.issubset(payment.keys())

    @given(payment=payment_record())
    @settings(max_examples=100)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 201

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

    def test_payment_amount_is_positive(self, payment: Dict[str, Any]) -> None:
        """Property: Payment amounts must be positive."""
        assert payment["amount"] > 0

    @given(payment=payment_record())
    @settings(max_examples=100)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 209

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    def test_payment_method_is_valid(self, payment: Dict[str, Any]) -> None:
        """Property: Payment method must be from allowed set."""
        valid_methods = {"ach", "card", "check", "wire", "cash"}
        assert payment["method"] in valid_methods

class TestUserValidationProperties:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 221

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    def test_user_email_format(self, user: Dict[str, Any]) -> None:
        """Property: User email must be valid format."""
        email = user["email"]
        assert "@" in email
        assert "." in email.split[1]("@")

    @given(user=user_record())
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 222

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        """Property: User email must be valid format."""
        email = user["email"]
        assert "@" in email
        assert "." in email.split[1]("@")

    @given(user=user_record())
    @settings(max_examples=100)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 230

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    def test_user_role_is_valid(self, user: Dict[str, Any]) -> None:
        """Property: User role must be from allowed set."""
        valid_roles = {"consumer", "agent", "admin"}
        assert user["role"] in valid_roles

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 246

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        """Property: JSON serialization roundtrip preserves data."""
        serialized = json.dumps(debt)
        deserialized = json.loads(serialized)
        assert debt == deserialized

    @given(payment=payment_record())
    @settings(max_examples=100)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 255

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        """Property: JSON serialization roundtrip preserves data."""
        serialized = json.dumps(payment)
        deserialized = json.loads(serialized)
        assert payment == deserialized

    @given(
        _data = st.dictionaries(
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 278

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        """Property: Arbitrary dictionaries survive JSON roundtrip."""
        serialized = json.dumps(data)
        deserialized = json.loads(serialized)
        assert data == deserialized

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 308

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        assert "status" in response
        assert "success" in response
        assert isinstance(response["success"], bool)
        assert response["success"] == (200 <= status_code < 300)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 309

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        }

        assert "status" in response
        assert "success" in response
        assert isinstance(response["success"], bool)
        assert response["success"] == (200 <= status_code < 300)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 310

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

        assert "status" in response
        assert "success" in response
        assert isinstance(response["success"], bool)
        assert response["success"] == (200 <= status_code < 300)

    @given(
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 311

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        assert "status" in response
        assert "success" in response
        assert isinstance(response["success"], bool)
        assert response["success"] == (200 <= status_code < 300)

    @given(
        items=st.lists(debt_record(), max_size=50),
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 333

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        page_items = items[start_idx:end_idx] if start_idx < total else []

        # Invariants
        assert len(page_items) <= per_page
        if page <= total_pages and total > 0:
            if page < total_pages:
                assert len(page_items) == per_page
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 336

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        assert len(page_items) <= per_page
        if page <= total_pages and total > 0:
            if page < total_pages:
                assert len(page_items) == per_page
        assert start_idx >= 0

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 337

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        if page <= total_pages and total > 0:
            if page < total_pages:
                assert len(page_items) == per_page
        assert start_idx >= 0

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 360

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        daily_rate = rate / Decimal("365")
        interest = principal *daily_rate* days

        assert interest >= 0

    @given(
        debt_amount=money_strategy,
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 376

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        """Property: Fees are bounded correctly."""
        fee = debt_amount * fee_percent

        assert fee >= 0
        assert fee <= debt_amount * Decimal("0.50")    # Max 50% fee

    @given(
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 377

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        fee = debt_amount * fee_percent

        assert fee >= 0
        assert fee <= debt_amount * Decimal("0.50")    # Max 50% fee

    @given(
        payments=st.lists(
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 394

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

        # Verify sorted
        for i in range(len(sorted_payments) - 1):
            assert sorted_payments[i][0] <= sorted_payments[i + 1][0]

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 417

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        is_limited = requests > limit
        remaining = max(0, limit - requests)

        assert remaining >= 0
        assert remaining <= limit
        assert is_limited == (requests > limit)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 418

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        remaining = max(0, limit - requests)

        assert remaining >= 0
        assert remaining <= limit
        assert is_limited == (requests > limit)

    @given(
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 419

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

        assert remaining >= 0
        assert remaining <= limit
        assert is_limited == (requests > limit)

    @given(
        burst_limit=st.integers(min_value=1, max_value=100),
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 436

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        # Token bucket state
        current_tokens = burst_limit    # Start full

        assert current_tokens >= 0
        assert current_tokens <= burst_limit

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 437

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        current_tokens = burst_limit    # Start full

        assert current_tokens >= 0
        assert current_tokens <= burst_limit

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 454

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        # Simple masking: show last 4
        masked = "***-**-" + ssn[-4:]

        assert len(masked) == len(ssn)
        assert masked[-4:] == ssn[-4:]
        assert "*" in masked

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 455

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        masked = "***-**-" + ssn[-4:]

        assert len(masked) == len(ssn)
        assert masked[-4:] == ssn[-4:]
        assert "*" in masked

    @given(card=st.from_regex(r"[0-9]{16}", fullmatch=True))
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 456

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

        assert len(masked) == len(ssn)
        assert masked[-4:] == ssn[-4:]
        assert "*" in masked

    @given(card=st.from_regex(r"[0-9]{16}", fullmatch=True))
    @settings(max_examples=100)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 465

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        """Property: Credit card masking preserves last 4 digits."""
        masked = "*" * 12 + card[-4:]

        assert len(masked) == 16
        assert masked[-4:] == card[-4:]
        assert masked[:12] == "*" * 12

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 466

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        masked = "*" * 12 + card[-4:]

        assert len(masked) == 16
        assert masked[-4:] == card[-4:]
        assert masked[:12] == "*" * 12

    @given(email=email_strategy)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 467

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

        assert len(masked) == 16
        assert masked[-4:] == card[-4:]
        assert masked[:12] == "*" * 12

    @given(email=email_strategy)
    @settings(max_examples=100)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 481

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
            masked_local = "*" * len(local)
        masked = f"{masked_local}@{domain}"

        assert "@" in masked
        assert domain in masked

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 482

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
        masked = f"{masked_local}@{domain}"

        assert "@" in masked
        assert domain in masked

# =============================================================================
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
