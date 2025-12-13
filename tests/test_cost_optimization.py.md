# Code Issues Report: tests\test_cost_optimization.py

Generated: 2025-12-13T15:23:39.829763
Source: tests\test_cost_optimization.py

## Issues Summary

Total: 13 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 44 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 49 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 50 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 51 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 52 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 58 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 59 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 60 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 66 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 67 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 68 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 73 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 77 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 13 issues to fix

### Issue at Line 44

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    # Monthly (730h): 1*0.05*730 + 1*0.02*730 + 1*0.001*730
    # = 36.5 + 14.6 + 0.73 = 51.83
    cost = optimizer._calculate_monthly_cost(specs)
    assert cost == pytest.approx(51.83, 0.01)

def test_report_generation(optimizer, sample_resources):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 49

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

def test_report_generation(optimizer, sample_resources):
    report = optimizer.generate_cost_report(sample_resources)
    assert report.total_cost > 0
    assert "prod" in report.project_breakdown
    assert "dev" in report.project_breakdown
    assert "vm" in report.resource_breakdown
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 50

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
def test_report_generation(optimizer, sample_resources):
    report = optimizer.generate_cost_report(sample_resources)
    assert report.total_cost > 0
    assert "prod" in report.project_breakdown
    assert "dev" in report.project_breakdown
    assert "vm" in report.resource_breakdown

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 51

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    report = optimizer.generate_cost_report(sample_resources)
    assert report.total_cost > 0
    assert "prod" in report.project_breakdown
    assert "dev" in report.project_breakdown
    assert "vm" in report.resource_breakdown

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 52

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    assert report.total_cost > 0
    assert "prod" in report.project_breakdown
    assert "dev" in report.project_breakdown
    assert "vm" in report.resource_breakdown

def test_idle_detection(optimizer, sample_resources):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 58

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
def test_idle_detection(optimizer, sample_resources):
    recs = optimizer.analyze_resource_usage(sample_resources)
    idle_recs = [r for r in recs if r.recommendation_type == "idle"]
    assert len(idle_recs) == 1
    assert idle_recs[0].resource_id == "vm-idle"
    assert idle_recs[0].action == "stop"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 59

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    recs = optimizer.analyze_resource_usage(sample_resources)
    idle_recs = [r for r in recs if r.recommendation_type == "idle"]
    assert len(idle_recs) == 1
    assert idle_recs[0].resource_id == "vm-idle"
    assert idle_recs[0].action == "stop"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 60

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    idle_recs = [r for r in recs if r.recommendation_type == "idle"]
    assert len(idle_recs) == 1
    assert idle_recs[0].resource_id == "vm-idle"
    assert idle_recs[0].action == "stop"

def test_rightsizing_detection(optimizer, sample_resources):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 66

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
def test_rightsizing_detection(optimizer, sample_resources):
    recs = optimizer.analyze_resource_usage(sample_resources)
    resize_recs = [r for r in recs if r.recommendation_type == "rightsizing"]
    assert len(resize_recs) == 1
    assert resize_recs[0].resource_id == "vm-oversized"
    assert resize_recs[0].action == "resize"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 67

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    recs = optimizer.analyze_resource_usage(sample_resources)
    resize_recs = [r for r in recs if r.recommendation_type == "rightsizing"]
    assert len(resize_recs) == 1
    assert resize_recs[0].resource_id == "vm-oversized"
    assert resize_recs[0].action == "resize"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 68

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python
    resize_recs = [r for r in recs if r.recommendation_type == "rightsizing"]
    assert len(resize_recs) == 1
    assert resize_recs[0].resource_id == "vm-oversized"
    assert resize_recs[0].action == "resize"

def test_pricing_update(optimizer):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 73

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

def test_pricing_update(optimizer):
    optimizer.set_pricing({"cpu_hourly": 1.0})
    assert optimizer.pricing["cpu_hourly"] == 1.0

    specs = {"cpu": 1, "memory_gb": 0, "storage_gb": 0}
    cost = optimizer._calculate_monthly_cost(specs)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 77

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to
optimised
byte code.

### Context

```python

    specs = {"cpu": 1, "memory_gb": 0, "storage_gb": 0}
    cost = optimizer._calculate_monthly_cost(specs)
    assert cost == 730.0    # 1 *1.0* 730
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
