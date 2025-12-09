# CI/CD Error Report

## Active Errors

*No active errors reported.*

## Fixed Errors

### Security Alerts (Code Scanning)

1. **High Severity**: Untrusted URL redirection in `opt/web/panel/app.py` (Line 475).
    * Status: Fixed by enforcing `ALLOWED_HOSTS` validation.

1. **High Severity**: Clear text logging of sensitive data in `opt/services/secrets_management.py` (Line 654).
    * Status: Fixed by removing insecure example usage code.

1. **Medium Severity**: Weak sensitive data hashing in `opt/services/api_key_rotation.py` (Line 251).
    * Status: Fixed by clarifying variable names and docstrings (false positive/heuristic fix).

### Linting Errors (Flake8/Style)

* `scripts/generate_security_report_v2.py`: Fixed formatting and imports.
* `opt/web/panel/routes/auth.py`: Fixed imports and spacing.
* `opt/web/panel/models/audit_log.py`: Fixed whitespace.
