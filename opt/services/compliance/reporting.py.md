# Code Issues Report: opt\services\compliance\reporting.py

Generated: 2025-12-13T15:14:48.184916
Source: opt\services\compliance\reporting.py

## Issues Summary

Total: 3 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 174 | 0 | bandit | `B108` | MEDIUM | Probable insecure usage of temp file/directory. |
| 183 | 0 | bandit | `B108` | MEDIUM | Probable insecure usage of temp file/directory. |
| 192 | 0 | bandit | `B108` | MEDIUM | Probable insecure usage of temp file/directory. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 3 issues to fix

### Issue at Line 174

**Tool:**bandit |**Code:**`B108` |**Severity:** MEDIUM

**Message:** Probable insecure usage of temp file/directory.

### Context

```python
            _content=self._generate_html(report_data)  # type: ignore[name-defined]
            # In a real scenario, we would write to a PDF file here.
            # For now, we'll save as .html but pretend it's what was asked
            _file_path=os.path.join("/tmp", f"compliance*report*{report*id}*{timestamp}.html")  # type: ignore[name-defined]
            try:
                with open(file_path, "w") as f:  # type: ignore[name-defined]
                    f.write(content)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 183

**Tool:**bandit |**Code:**`B108` |**Severity:** MEDIUM

**Message:** Probable insecure usage of temp file/directory.

### Context

```python

        elif format.lower() == "html":
            _content=self._generate_html(report_data)  # type: ignore[name-defined]
            _file_path=os.path.join("/tmp", f"compliance*report*{report*id}*{timestamp}.html")  # type: ignore[name-defined]
            try:
                with open(file_path, "w") as f:  # type: ignore[name-defined]
                    f.write(content)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 192

**Tool:**bandit |**Code:**`B108` |**Severity:** MEDIUM

**Message:** Probable insecure usage of temp file/directory.

### Context

```python

        elif format.lower() == "markdown":
            _content=self._generate_markdown(report_data)  # type: ignore[name-defined]
            _file_path=os.path.join("/tmp", f"compliance*report*{report*id}*{timestamp}.md")  # type: ignore[name-defined]
            try:
                with open(file_path, "w") as f:  # type: ignore[name-defined]
                    f.write(content)
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
