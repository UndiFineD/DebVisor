# CI/CD Error Report

## Active Errors

### Security Alerts (Code Scanning)

1.  **High Severity**: Untrusted URL redirection in `opt/web/panel/app.py` (Line 475).
    *   Rule: `py/url-redirection`
2.  **High Severity**: Clear text logging of sensitive data in `opt/services/secrets_management.py` (Line 654).
    *   Rule: `py/clear-text-logging-sensitive-data`
3.  **Medium Severity**: Weak sensitive data hashing in `opt/services/api_key_rotation.py` (Line 251).
    *   Rule: `py/weak-sensitive-data-hashing`

### Linting Errors (Flake8/Style)

#### `scripts/generate_security_report_v2.py`

*   `E305`: Expected 2 blank lines after class/function definition (Line 74).
*   `W293`: Blank line contains whitespace (Lines 10, 16, 18, 25, 46, 50, 61).
*   `E501`: Line too long (Line 9).
*   `E302`: Expected 2 blank lines (Line 7).
*   `F401`: 'os' imported but unused (Line 3).

#### `opt/web/panel/routes/auth.py`

*   `W293`: Blank line contains whitespace (Lines 120, 124).
*   `E402`: Module level import not at top of file (Lines 28-34).
*   `E305`: Expected 2 blank lines after class/function definition (Line 28).
*   `E127`: Continuation line over-indented (Line 27).
*   `E302`: Expected 2 blank lines (Line 22).
*   `F401`: 'os' imported but unused (Line 20).

#### Other Files

*   `opt/web/panel/models/audit_log.py`: `W293` (Line 179).
*   `opt/services/rpc/audit.py`: `W293` (Lines 82, 89).

## Plan

1.  **Fix Security Issues**:
    *   Investigate and fix URL redirection in `opt/web/panel/app.py`.
    *   Redact sensitive data in logs in `opt/services/secrets_management.py`.
    *   Use stronger hashing (e.g., bcrypt/argon2) or salt for passwords in `opt/services/api_key_rotation.py`.
    
2.  **Fix Linting Issues**:
    *   Run `autopep8` or manually fix whitespace and imports in `scripts/generate_security_report_v2.py` and `opt/web/panel/routes/auth.py`.
    *   Fix specific errors like `E402` (imports) by moving them to the top.
