# Code Issues Report: scripts\fix_all_errors.py

Generated: 2025-12-13T15:21:05.503636
Source: scripts\fix_all_errors.py

## Issues Summary

Total: 18 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 52 | 0 | bandit | `B404` | LOW | Consider possible security implications associated with the subprocess module. |
| 750 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 750 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 771 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 771 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 779 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 779 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 831 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 1149 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1187 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1228 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1313 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1376 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1405 | 0 | bandit | `B110` | LOW | Try, Except, Pass detected. |
| 1800 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 1800 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |
| 1845 | 0 | bandit | `B607` | LOW | Starting a process with a partial executable path |
| 1845 | 0 | bandit | `B603` | LOW | subprocess call - check for execution of untrusted input. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 18 issues to fix

### Issue at Line 52

**Tool:**bandit |**Code:**`B404` |**Severity:** LOW

**Message:** Consider possible security implications associated with the subprocess
module.

### Context

```python
import logging
import re
import shutil
import subprocess
import sys
import yaml
from collections import defaultdict
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 750

**Tool:**bandit |**Code:**`B607` |**Severity:** LOW

**Message:** Starting a process with a partial executable path

### Context

```python
                    self._normalize_line_endings(sh_file, stats)

                # Get JSON output for reporting
                proc = subprocess.run(
                    ["shellcheck", "-f", "json", str(sh_file)],
                    capture_output=True, text=True
                )
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 750

**Tool:**bandit |**Code:**`B603` |**Severity:** LOW

**Message:** subprocess call - check for execution of untrusted input.

### Context

```python
                    self._normalize_line_endings(sh_file, stats)

                # Get JSON output for reporting
                proc = subprocess.run(
                    ["shellcheck", "-f", "json", str(sh_file)],
                    capture_output=True, text=True
                )
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 771

**Tool:**bandit |**Code:**`B607` |**Severity:** LOW

**Message:** Starting a process with a partial executable path

### Context

```python

                if self.apply:
                    # Apply diffs
                    diff_proc = subprocess.run(
                        ["shellcheck", "-f", "diff", str(sh_file)],
                        capture_output=True, text=True
                    )
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 771

**Tool:**bandit |**Code:**`B603` |**Severity:** LOW

**Message:** subprocess call - check for execution of untrusted input.

### Context

```python

                if self.apply:
                    # Apply diffs
                    diff_proc = subprocess.run(
                        ["shellcheck", "-f", "diff", str(sh_file)],
                        capture_output=True, text=True
                    )
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 779

**Tool:**bandit |**Code:**`B607` |**Severity:** LOW

**Message:** Starting a process with a partial executable path

### Context

```python
                        # Apply patch using git apply
                        try:
                            # git apply expects input from stdin
                            subprocess.run(
                                ["git", "apply", "-"],
                                input=diff_proc.stdout, text=True, check=True, cwd=self.root
                            )
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 779

**Tool:**bandit |**Code:**`B603` |**Severity:** LOW

**Message:** subprocess call - check for execution of untrusted input.

### Context

```python
                        # Apply patch using git apply
                        try:
                            # git apply expects input from stdin
                            subprocess.run(
                                ["git", "apply", "-"],
                                input=diff_proc.stdout, text=True, check=True, cwd=self.root
                            )
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 831

**Tool:**bandit |**Code:**`B603` |**Severity:** LOW

**Message:** subprocess call - check for execution of untrusted input.

### Context

```python
        print("Running MyPy scan...")
        try:
            # Run mypy
            proc = subprocess.run(
                [sys.executable, "-m", "mypy", "opt", "scripts", "--no-error-summary"],
                capture_output=True, text=True
            )
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 1149

**Tool:**bandit |**Code:**`B110` |**Severity:** LOW

**Message:** Try, Except, Pass detected.

### Context

```python

                if self.apply and lines != original_lines:
                    file_path.write_text("\n".join(lines), encoding="utf-8")
            except Exception:
                pass

        return fixed_ids
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 1187

**Tool:**bandit |**Code:**`B110` |**Severity:** LOW

**Message:** Try, Except, Pass detected.

### Context

```python

                if self.apply and lines != original_lines:
                    file_path.write_text("\n".join(lines), encoding="utf-8")
            except Exception:
                pass

        return fixed_ids
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 1228

**Tool:**bandit |**Code:**`B110` |**Severity:** LOW

**Message:** Try, Except, Pass detected.

### Context

```python

                if self.apply and lines != original_lines:
                    file_path.write_text("\n".join(lines), encoding="utf-8")
            except Exception:
                pass

        return fixed_ids
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 1313

**Tool:**bandit |**Code:**`B110` |**Severity:** LOW

**Message:** Try, Except, Pass detected.

### Context

```python

                if content != original:
                    file_path.write_text("\n".join(content), encoding="utf-8")
            except Exception:
                pass

        return fixed*ids
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 1376

**Tool:**bandit |**Code:**`B110` |**Severity:** LOW

**Message:** Try, Except, Pass detected.

### Context

```python
                    for id* in ids:
                        fixed*ids.add(id*)
                        stats.add(str(file_path), "F404", 0, "Reordered **future** imports", fixed=True)
            except Exception:
                pass

        return fixed_ids
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 1405

**Tool:**bandit |**Code:**`B110` |**Severity:** LOW

**Message:** Try, Except, Pass detected.

### Context

```python
            return
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            pass

        # Find first complete JSON object/array
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 1800

**Tool:**bandit |**Code:**`B607` |**Severity:** LOW

**Message:** Starting a process with a partial executable path

### Context

```python
        print("Running type checking diagnostics...")

        try:
            result = subprocess.run(
                ["mypy", "opt", "tests", "--config-file", "mypy.ini", "--show-error-codes"],
                capture_output=True,
                text=True,
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 1800

**Tool:**bandit |**Code:**`B603` |**Severity:** LOW

**Message:** subprocess call - check for execution of untrusted input.

### Context

```python
        print("Running type checking diagnostics...")

        try:
            result = subprocess.run(
                ["mypy", "opt", "tests", "--config-file", "mypy.ini", "--show-error-codes"],
                capture_output=True,
                text=True,
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 1845

**Tool:**bandit |**Code:**`B607` |**Severity:** LOW

**Message:** Starting a process with a partial executable path

### Context

```python

        try:
            # Run pytest with collection-only to detect syntax errors
            result = subprocess.run(
                ["pytest", "--collect-only", "-q"],
                cwd=str(self.root),
                capture_output=True,
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 1845

**Tool:**bandit |**Code:**`B603` |**Severity:** LOW

**Message:** subprocess call - check for execution of untrusted input.

### Context

```python

        try:
            # Run pytest with collection-only to detect syntax errors
            result = subprocess.run(
                ["pytest", "--collect-only", "-q"],
                cwd=str(self.root),
                capture_output=True,
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
