# Safe Type: Ignore Management

## Overview

The `update_type_ignore.py` script has been redesigned to prevent silent suppression of real type errors while enabling safe, auditable handling of non-critical typing issues.

## Key Improvements

### 1. **Safe-by-Default Approach**

- **No destructive changes without review**: The script now generates review-ready output files instead of immediately modifying source code
- **Explicit opt-in required**: Use `--apply` flag to modify files after manual review
- **Default behavior**: Generates JSON or patch file for human review

### 2. **Whitelist/Blocklist System**

#### Critical Error Codes (Never Auto-Suppressed)
```python
CRITICAL_ERROR_CODES = {
    "assignment",        # Type mismatch in assignment (real bugs)
    "return-value",      # Return type mismatch (real bugs)
    "func-returns-value", # Function returns wrong type
    "arg-type",         # Function argument type mismatch
    "union-attr",       # Accessing attribute that doesn't exist on some union members
    "attr-defined",     # Accessing undefined attribute
}
```text
    "assignment",        # Type mismatch in assignment (real bugs)
    "return-value",      # Return type mismatch (real bugs)
    "func-returns-value", # Function returns wrong type
    "arg-type",         # Function argument type mismatch
    "union-attr",       # Accessing attribute that doesn't exist on some union members
    "attr-defined",     # Accessing undefined attribute
}
```text

#### Critical File Patterns (Never Auto-Suppressed)

- `cert_manager.py` - Cryptography/security critical
- `security/` - Security-related modules
- `auth` - Authentication code

#### Allowlist (Safe to Suppress)
```python

#### Critical File Patterns (Never Auto-Suppressed)

- `cert_manager.py` - Cryptography/security critical
- `security/` - Security-related modules
- `auth` - Authentication code

#### Allowlist (Safe to Suppress)
```python
ALLOWLIST_CODES = {
    "var-annotated",        # Non-critical annotation style
    "name-defined",         # Often false positives
    "annotation-unchecked", # Untyped function bodies
    "unused-ignore",        # Redundant suppressions
}
```text
    "var-annotated",        # Non-critical annotation style
    "name-defined",         # Often false positives
    "annotation-unchecked", # Untyped function bodies
    "unused-ignore",        # Redundant suppressions
}
```text

### 3. **Rich Context in Suggestions**

Each suggestion includes:

- Line number and file path
- Original error line
- Code before and after (context)
- Error codes (critical vs suppressible)
- Blocklist reason if applicable
- Template for human justification

Example JSON output:
```json

### 3. **Rich Context in Suggestions**

Each suggestion includes:

- Line number and file path
- Original error line
- Code before and after (context)
- Error codes (critical vs suppressible)
- Blocklist reason if applicable
- Template for human justification

Example JSON output:
```json
{
  "filepath": "opt/services/cert_manager.py",
  "line_num": 92,
  "codes": [],
  "line_text": "  return timedelta(seconds=expires_in)",
  "context_before": "def get_expiry():",
  "context_after": "# ... rest of code",
  "is_critical": true,
  "blocklisted_reason": "File 'cert_manager.py' contains critical patterns",
  "justification_required": false,
  "suggested_justification": "..."
}
```text
  "filepath": "opt/services/cert_manager.py",
  "line_num": 92,
  "codes": [],
  "line_text": "  return timedelta(seconds=expires_in)",
  "context_before": "def get_expiry():",
  "context_after": "# ... rest of code",
  "is_critical": true,
  "blocklisted_reason": "File 'cert_manager.py' contains critical patterns",
  "justification_required": false,
  "suggested_justification": "..."
}
```text

### 4. **Mandatory Justification Option**

Use `--require-comment` to enforce human-written justifications:
```bash

### 4. **Mandatory Justification Option**

Use `--require-comment` to enforce human-written justifications:
```bash
python scripts/update_type_ignore.py --apply --require-comment
```text
```text

This adds comment blocks alongside suppressions:
```python

This adds comment blocks alongside suppressions:
```python
x = some_func()  # type: ignore[return-value]  # BUG-1234: Temporary until refactor
```text
```text

### 5. **Review-Ready Output Formats**

#### JSON Format (Default)
```bash

### 5. **Review-Ready Output Formats**

#### JSON Format (Default)
```bash
python scripts/update_type_ignore.py --output-format json
# Generates: type_ignore_review.json
```text
## Generates: type_ignore_review.json
```text

Organized by file/line with full context for systematic review.

#### Patch Format
```bash

Organized by file/line with full context for systematic review.

#### Patch Format
```bash
python scripts/update_type_ignore.py --output-format patch
# Generates: type_ignore_review.patch
```text
## Generates: type_ignore_review.patch
```text

Unified diff format that can be reviewed and applied manually:
```bash
Unified diff format that can be reviewed and applied manually:
```bash
# After review and approval:
patch -p0 < type_ignore_review.patch
```text
patch -p0 < type_ignore_review.patch
```text

## Usage Workflows

### Workflow 1: Review Before Applying (Recommended)
```bash
## Usage Workflows

### Workflow 1: Review Before Applying (Recommended)
```bash
# Generate review file without modifying anything
python scripts/update_type_ignore.py

# Open and review: type_ignore_review.json
# After approval, apply with:
python scripts/update_type_ignore.py --apply

# Or with required comments:
python scripts/update_type_ignore.py --apply --require-comment
```text
python scripts/update_type_ignore.py

## Open and review: type_ignore_review.json
## After approval, apply with:
python scripts/update_type_ignore.py --apply

## Or with required comments:
python scripts/update_type_ignore.py --apply --require-comment
```text

### Workflow 2: Strict Mode (Only Whitelisted Codes)
```bash
### Workflow 2: Strict Mode (Only Whitelisted Codes)
```bash
# Only suppress known-safe codes (safer for CI)
python scripts/update_type_ignore.py --require-allowlist

# Force human review and approval:
python scripts/update_type_ignore.py --require-allowlist --apply --require-comment
```text
python scripts/update_type_ignore.py --require-allowlist

## Force human review and approval:
python scripts/update_type_ignore.py --require-allowlist --apply --require-comment
```text

### Workflow 3: Run MyPy and Review Together
```bash
### Workflow 3: Run MyPy and Review Together
```bash
# Generate fresh mypy output and build suggestions
python scripts/update_type_ignore.py --run-mypy

# Review type_ignore_review.json then apply if approved
python scripts/update_type_ignore.py --apply
```text
python scripts/update_type_ignore.py --run-mypy

## Review type_ignore_review.json then apply if approved
python scripts/update_type_ignore.py --apply
```text

## Preventing Real Bugs

### Example: cert_manager.py:92

- *Before** (blind suppression):
```python

## Preventing Real Bugs

### Example: cert_manager.py:92

- *Before** (blind suppression):
```python
def get_expiry_time() -> datetime:  # Wrong annotation!
    expires_in = get_ttl_seconds()   # Returns int
    return timedelta(seconds=expires_in)  # Returns timedelta, not datetime!
    # type: ignore[return-value]  ← Hides the real bug
```text
    expires_in = get_ttl_seconds()   # Returns int
    return timedelta(seconds=expires_in)  # Returns timedelta, not datetime!
    # type: ignore[return-value]  ← Hides the real bug
```text

- *After** (safe with our script):
```text

- *After** (safe with our script):
```text
Review file shows:

- File: cert_manager.py (CRITICAL FILE - blocked from auto-suppression)
- Error: return-value (CRITICAL ERROR - always requires fix)
- Reason: Must fix the actual type mismatch, not suppress it
```text

- File: cert_manager.py (CRITICAL FILE - blocked from auto-suppression)
- Error: return-value (CRITICAL ERROR - always requires fix)
- Reason: Must fix the actual type mismatch, not suppress it
```text

The developer MUST fix the real bug:
```python

The developer MUST fix the real bug:
```python
def get_expiry_time() -> timedelta:  # Correct annotation
    expires_in = get_ttl_seconds()
    return timedelta(seconds=expires_in)  # Now correctly returns timedelta
```text
    expires_in = get_ttl_seconds()
    return timedelta(seconds=expires_in)  # Now correctly returns timedelta
```text

## CI/CD Integration

### Safe Default for Automated Checks
```bash
## CI/CD Integration

### Safe Default for Automated Checks
```bash
# In CI: Never auto-suppress anything without review
python scripts/update_type_ignore.py --require-allowlist
# Exit code indicates issues that need manual review
```text
python scripts/update_type_ignore.py --require-allowlist
## Exit code indicates issues that need manual review
```text

### Prevent Regressions
```bash
### Prevent Regressions
```bash
# In pull requests: flag any new suppressions
python scripts/update_type_ignore.py --require-allowlist --require-comment
# Requires human justification for each suppression
```text
python scripts/update_type_ignore.py --require-allowlist --require-comment
## Requires human justification for each suppression
```text

## Configuration

Edit the CRITICAL_ERROR_CODES, CRITICAL_FILE_PATTERNS, and ALLOWLIST_CODES sets at the top of `update_type_ignore.py` to customize behavior for your project.

## Benefits

1. **Transparency**: Every suppression is documented with context and justification
1. **Safety**: Critical files and error codes are never silently suppressed
1. **Auditability**: Review files provide a complete audit trail
1. **Flexibility**: Support for whitelist, blocklist, and override options
1. **Developer Experience**: Clear guidance on which errors to fix vs suppress
1. **No Silent Bugs**: Real type errors aren't hidden by blanket suppressions

## Configuration

Edit the CRITICAL_ERROR_CODES, CRITICAL_FILE_PATTERNS, and ALLOWLIST_CODES sets at the top of `update_type_ignore.py` to customize behavior for your project.

## Benefits

1. **Transparency**: Every suppression is documented with context and justification
1. **Safety**: Critical files and error codes are never silently suppressed
1. **Auditability**: Review files provide a complete audit trail
1. **Flexibility**: Support for whitelist, blocklist, and override options
1. **Developer Experience**: Clear guidance on which errors to fix vs suppress
1. **No Silent Bugs**: Real type errors aren't hidden by blanket suppressions
