# Code Issues Report: opt\build\sync-addons-playbook.sh

Generated: 2025-12-13T17:07:39.919651
Source: opt\build\sync-addons-playbook.sh

## Issues Summary

Total: 22 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 1 | 20 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 2 | 18 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 3 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 4 | 61 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 5 | 58 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 6 | 96 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 7 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 8 | 27 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 9 | 70 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 10 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 11 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 12 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 13 | 28 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 14 | 20 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 15 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 16 | 49 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 17 | 83 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 18 | 11 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 19 | 3 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 20 | 1 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 21 | 30 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |
| 22 | 78 | shellcheck | `1017` | ERROR | Literal carriage return. Run script through tr -d '\r' . |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 22 issues to fix

### Issue at Line 1

**Tool:**shellcheck |**Code:**`1017` |**Severity:** ERROR

**Message:** Literal carriage return. Run script through tr -d '\r' .

### Context

```python
## !/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
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

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${REPO_ROOT}/ansible/playbooks/bootstrap-addons.yml"
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

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${REPO_ROOT}/ansible/playbooks/bootstrap-addons.yml"
DST="${REPO_ROOT}/config/includes.chroot/usr/local/share/debvisor/ansible/bootstrap-addons.yml"
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

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${REPO_ROOT}/ansible/playbooks/bootstrap-addons.yml"
DST="${REPO_ROOT}/config/includes.chroot/usr/local/share/debvisor/ansible/bootstrap-addons.yml"

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

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${REPO_ROOT}/ansible/playbooks/bootstrap-addons.yml"
DST="${REPO_ROOT}/config/includes.chroot/usr/local/share/debvisor/ansible/bootstrap-addons.yml"

if [[! -f "$SRC"]]; then
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

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${REPO_ROOT}/ansible/playbooks/bootstrap-addons.yml"
DST="${REPO_ROOT}/config/includes.chroot/usr/local/share/debvisor/ansible/bootstrap-addons.yml"

if [[! -f "$SRC"]]; then
    echo "[sync-addons-playbook] Source playbook not found: $SRC" >&2
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
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${REPO_ROOT}/ansible/playbooks/bootstrap-addons.yml"
DST="${REPO_ROOT}/config/includes.chroot/usr/local/share/debvisor/ansible/bootstrap-addons.yml"

if [[! -f "$SRC"]]; then
    echo "[sync-addons-playbook] Source playbook not found: $SRC" >&2
    exit 1
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
SRC="${REPO_ROOT}/ansible/playbooks/bootstrap-addons.yml"
DST="${REPO_ROOT}/config/includes.chroot/usr/local/share/debvisor/ansible/bootstrap-addons.yml"

if [[! -f "$SRC"]]; then
    echo "[sync-addons-playbook] Source playbook not found: $SRC" >&2
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
DST="${REPO_ROOT}/config/includes.chroot/usr/local/share/debvisor/ansible/bootstrap-addons.yml"

if [[! -f "$SRC"]]; then
    echo "[sync-addons-playbook] Source playbook not found: $SRC" >&2
    exit 1
fi

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

if [[! -f "$SRC"]]; then
    echo "[sync-addons-playbook] Source playbook not found: $SRC" >&2
    exit 1
fi

DST_DIR="$(dirname "$DST")"
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
if [[! -f "$SRC"]]; then
    echo "[sync-addons-playbook] Source playbook not found: $SRC" >&2
    exit 1
fi

DST_DIR="$(dirname "$DST")"
mkdir -p "$DST_DIR"
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
    echo "[sync-addons-playbook] Source playbook not found: $SRC" >&2
    exit 1
fi

DST_DIR="$(dirname "$DST")"
mkdir -p "$DST_DIR"

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
    exit 1
fi

DST_DIR="$(dirname "$DST")"
mkdir -p "$DST_DIR"

if [[-f "$DST"]] && cmp -s "$SRC" "$DST"; then
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
fi

DST_DIR="$(dirname "$DST")"
mkdir -p "$DST_DIR"

if [[-f "$DST"]] && cmp -s "$SRC" "$DST"; then
    echo "[sync-addons-playbook] No changes; destination already up to date: $DST"
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

DST_DIR="$(dirname "$DST")"
mkdir -p "$DST_DIR"

if [[-f "$DST"]] && cmp -s "$SRC" "$DST"; then
    echo "[sync-addons-playbook] No changes; destination already up to date: $DST"
    exit 0
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
DST_DIR="$(dirname "$DST")"
mkdir -p "$DST_DIR"

if [[-f "$DST"]] && cmp -s "$SRC" "$DST"; then
    echo "[sync-addons-playbook] No changes; destination already up to date: $DST"
    exit 0
fi
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
mkdir -p "$DST_DIR"

if [[-f "$DST"]] && cmp -s "$SRC" "$DST"; then
    echo "[sync-addons-playbook] No changes; destination already up to date: $DST"
    exit 0
fi

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

if [[-f "$DST"]] && cmp -s "$SRC" "$DST"; then
    echo "[sync-addons-playbook] No changes; destination already up to date: $DST"
    exit 0
fi

install -m 0644 "$SRC" "$DST"
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
if [[-f "$DST"]] && cmp -s "$SRC" "$DST"; then
    echo "[sync-addons-playbook] No changes; destination already up to date: $DST"
    exit 0
fi

install -m 0644 "$SRC" "$DST"
echo "[sync-addons-playbook] Synced addons playbook to includes.chroot: $DST"
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
    echo "[sync-addons-playbook] No changes; destination already up to date: $DST"
    exit 0
fi

install -m 0644 "$SRC" "$DST"
echo "[sync-addons-playbook] Synced addons playbook to includes.chroot: $DST"
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
    exit 0
fi

install -m 0644 "$SRC" "$DST"
echo "[sync-addons-playbook] Synced addons playbook to includes.chroot: $DST"
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
fi

install -m 0644 "$SRC" "$DST"
echo "[sync-addons-playbook] Synced addons playbook to includes.chroot: $DST"
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
