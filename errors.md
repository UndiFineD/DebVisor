# CI/CD Error Report

This document tracks active errors and technical debt in the repository.

## Recent CI/CD Failures (GitHub Notifications)

**Status:** Fixes Applied Locally (Pending Push)
**Context:** Remote workflow runs are failing due to issues that have been resolved in the local workspace.

### 1. Unit Tests & Coverage

- **Error:** `Process completed with exit code 4` (pytest usage error / missing dependencies).
- **Fix:** Updated `test.yml` to use `requirements-test.txt` and switched to `ubuntu-latest`.

### 2. Markdown Lint

- **Error:** Multiple formatting errors (MD022, MD031, MD034, MD059).
- **Fix:** Applied comprehensive markdown formatting fixes to all documentation files.

### 3. Release Please

- **Error:** `Resource not accessible by integration`.
- **Fix:** Switched to `ubuntu-latest` to ensure proper token permissions.

### 4. Syntax Validation

- **Error:** `End-of-central-directory signature not found` (unzip failure on Windows).
- **Fix:** Switched to `ubuntu-latest` and updated `shellcheck` installation.

### 5. Security Scan Alerts

- **Error:** Bandit and Flake8 alerts (subprocess shell=True, hardcoded secrets).
- **Fix:** Resolved all 30+ alerts in `security-scan.md` and applied code fixes.
