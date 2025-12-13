# Code Issues Report: opt\build\test-firstboot.sh

Generated: 2025-12-13T17:07:39.991543
Source: opt\build\test-firstboot.sh

## Issues Summary

Total: 23 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 1 | 20 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 2 | 18 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 3 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 4 | 56 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 5 | 77 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 6 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 7 | 30 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 8 | 93 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 9 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 10 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 11 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 12 | 49 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 13 | 99 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 14 | 5 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 15 | 72 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 16 | 25 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 17 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 18 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 19 | 103 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 20 | 31 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 21 | 76 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 22 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 23 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 23 issues to fix

### Issue at Line 1

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## !/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 2

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## !/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="${ROOT}/config/includes.chroot/usr/local/sbin/debvisor-firstboot.sh"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 3

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## !/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="${ROOT}/config/includes.chroot/usr/local/sbin/debvisor-firstboot.sh"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 4

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## !/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="${ROOT}/config/includes.chroot/usr/local/sbin/debvisor-firstboot.sh"

if [[! -x "$SCRIPT"]]; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 5

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="${ROOT}/config/includes.chroot/usr/local/sbin/debvisor-firstboot.sh"

if [[! -x "$SCRIPT"]]; then
    echo "[test-firstboot] ERROR: firstboot script not found or not executable: $SCRIPT" >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 6

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="${ROOT}/config/includes.chroot/usr/local/sbin/debvisor-firstboot.sh"

if [[! -x "$SCRIPT"]]; then
    echo "[test-firstboot] ERROR: firstboot script not found or not executable: $SCRIPT" >&2
    exit 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 7

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="${ROOT}/config/includes.chroot/usr/local/sbin/debvisor-firstboot.sh"

if [[! -x "$SCRIPT"]]; then
    echo "[test-firstboot] ERROR: firstboot script not found or not executable: $SCRIPT" >&2
    exit 1
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 8

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
SCRIPT="${ROOT}/config/includes.chroot/usr/local/sbin/debvisor-firstboot.sh"

if [[! -x "$SCRIPT"]]; then
    echo "[test-firstboot] ERROR: firstboot script not found or not executable: $SCRIPT" >&2
    exit 1
fi

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 9

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

if [[! -x "$SCRIPT"]]; then
    echo "[test-firstboot] ERROR: firstboot script not found or not executable: $SCRIPT" >&2
    exit 1
fi

if ! command -v shellcheck >/dev/null 2>&1; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 10

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
if [[! -x "$SCRIPT"]]; then
    echo "[test-firstboot] ERROR: firstboot script not found or not executable: $SCRIPT" >&2
    exit 1
fi

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[test-firstboot] shellcheck not found; install it with: sudo apt install shellcheck" >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 11

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    echo "[test-firstboot] ERROR: firstboot script not found or not executable: $SCRIPT" >&2
    exit 1
fi

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[test-firstboot] shellcheck not found; install it with: sudo apt install shellcheck" >&2
else
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 12

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    exit 1
fi

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[test-firstboot] shellcheck not found; install it with: sudo apt install shellcheck" >&2
else
    echo "[test-firstboot] Running shellcheck on debvisor-firstboot.sh"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 13

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
fi

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[test-firstboot] shellcheck not found; install it with: sudo apt install shellcheck" >&2
else
    echo "[test-firstboot] Running shellcheck on debvisor-firstboot.sh"
    shellcheck "$SCRIPT"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 14

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[test-firstboot] shellcheck not found; install it with: sudo apt install shellcheck" >&2
else
    echo "[test-firstboot] Running shellcheck on debvisor-firstboot.sh"
    shellcheck "$SCRIPT"
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 15

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[test-firstboot] shellcheck not found; install it with: sudo apt install shellcheck" >&2
else
    echo "[test-firstboot] Running shellcheck on debvisor-firstboot.sh"
    shellcheck "$SCRIPT"
fi

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 16

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    echo "[test-firstboot] shellcheck not found; install it with: sudo apt install shellcheck" >&2
else
    echo "[test-firstboot] Running shellcheck on debvisor-firstboot.sh"
    shellcheck "$SCRIPT"
fi

echo "[test-firstboot] Running debvisor-firstboot.sh in dry-run mode (this should be non-destructive)"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 17

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
else
    echo "[test-firstboot] Running shellcheck on debvisor-firstboot.sh"
    shellcheck "$SCRIPT"
fi

echo "[test-firstboot] Running debvisor-firstboot.sh in dry-run mode (this should be non-destructive)"
if ! "$SCRIPT" --dry-run; then
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 18

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    echo "[test-firstboot] Running shellcheck on debvisor-firstboot.sh"
    shellcheck "$SCRIPT"
fi

echo "[test-firstboot] Running debvisor-firstboot.sh in dry-run mode (this should be non-destructive)"
if ! "$SCRIPT" --dry-run; then
    echo "[test-firstboot] ERROR: dry-run exited non-zero (check logs)" >&2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 19

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
    shellcheck "$SCRIPT"
fi

echo "[test-firstboot] Running debvisor-firstboot.sh in dry-run mode (this should be non-destructive)"
if ! "$SCRIPT" --dry-run; then
    echo "[test-firstboot] ERROR: dry-run exited non-zero (check logs)" >&2
    exit 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 20

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
fi

echo "[test-firstboot] Running debvisor-firstboot.sh in dry-run mode (this should be non-destructive)"
if ! "$SCRIPT" --dry-run; then
    echo "[test-firstboot] ERROR: dry-run exited non-zero (check logs)" >&2
    exit 1
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 21

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python

echo "[test-firstboot] Running debvisor-firstboot.sh in dry-run mode (this should be non-destructive)"
if ! "$SCRIPT" --dry-run; then
    echo "[test-firstboot] ERROR: dry-run exited non-zero (check logs)" >&2
    exit 1
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 22

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
echo "[test-firstboot] Running debvisor-firstboot.sh in dry-run mode (this should be non-destructive)"
if ! "$SCRIPT" --dry-run; then
    echo "[test-firstboot] ERROR: dry-run exited non-zero (check logs)" >&2
    exit 1
fi
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 23

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
if ! "$SCRIPT" --dry-run; then
    echo "[test-firstboot] ERROR: dry-run exited non-zero (check logs)" >&2
    exit 1
fi
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
