# CI/CD Error Report

This document tracks active errors and technical debt in the repository.

## Active Errors

### 1. Security & Linting (Local Scan)

**Source:** `security-scan.md`
**Status:** Resolved

| Type | Count | Description | Resolution |
|---|---|---|---|
| **Flake8** | 0 | `W504` Line break after binary operator | Fixed by autopep8 |
| **Flake8** | 0 | `E704` Multiple statements on one line | Fixed manually |
| **Bandit** | 0 | `B101` Assert used in production code | Excluded tests in .bandit |
| **Bandit** | 0 | `B603` Subprocess call without shell=True check | Fixed/Verified safe |
| **Bandit** | 0 | `B104` Bind to all interfaces (0.0.0.0) | Marked as intended |
| **Bandit** | 0 | `B105` Hardcoded password strings | Verified false positives |

### 2. CI/CD Pipeline (Inferred)

**Status:** Failing

- **Unit Tests:** `pytest` failing with exit code 4 (missing dependencies).
- **Linting:** Markdown lint errors in documentation.
- **Release:** Permission issues with `release-please`.

## Next Steps

1. Fix Flake8 formatting issues (`autopep8` or manual).
1. Address Bandit security warnings (suppress false positives in tests, fix real issues in app code).
1. Update `requirements-test.txt` to fix CI failures.
