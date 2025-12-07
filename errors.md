# CI/CD Error Report

This document tracks active errors and technical debt in the repository.

## 1. Source Code Linting (opt/ and scripts/)

**Status:** In Progress
**Context:** The `opt/` and `scripts/` directories have been processed.

- **Syntax Errors (E999):** Fixed. (Caused by aggressive auto-formatting of f-strings).
- **Undefined Names (F821):** Fixed.
- **Whitespace/Formatting:** Mostly fixed by `autopep8`.
- **Unused Imports (F401):** Fixed.
- **Line Length (E501):** Active (Numerous violations).
- **F-strings missing placeholders (F541):** Fixed.

## 2. VS Code Diagnostics

**Error:** `Unable to find reusable workflow` in `.github/workflows/deploy.yml`
**Status:** False Positive
**Details:** The referenced file `.github/workflows/_notify.yml` exists. This is a known issue with the VS Code GitHub Actions extension validation logic.

## 3. Security Vulnerabilities (VulScan Report)

**Status:** Analysis Required
**Context:** The following vulnerabilities were reported by the local scanner. Preliminary analysis suggests high false positive rate due to name collisions (e.g., Flask/Xen).

### 1. Flask @ 3.0.3

- **Severity:** HIGH
- **CVEs:** CVE-2008-3687 (Xen), CVE-2014-1895 (Xen), etc.
- **Analysis:** **False Positive**. CVEs refer to "XSM:FLASK" in Xen Hypervisor, not Python Flask.

### 2. Werkzeug @ 3.1.4

- **Severity:** HIGH
- **CVEs:** CVE-2019-14806 (Pallets Werkzeug < 0.11.11).
- **Analysis:** **False Positive**. Current version 3.1.4 is much newer than 0.11.11.

### 3. Jinja2 @ 3.1.6

- **Severity:** CRITICAL
- **CVEs:** CVE-2014-0012 (Jinja2 2.7.2).
- **Analysis:** **False Positive**. Current version 3.1.6 is much newer than 2.7.2.

### 4. PyYAML @ 6.0.2

- **Severity:** CRITICAL
- **CVEs:** CVE-2017-18342 (PyYAML < 5.1).
- **Analysis:** **False Positive**. Current version 6.0.2 is newer than 5.1.

### 5. requests @ 2.32.4

- **Severity:** HIGH
- **CVEs:** CVE-1999-0551 (Portmapper).
- **Analysis:** **False Positive**. Name collision with "requests" concept or unrelated software.

### 6. cryptography @ 44.0.1

- **Severity:** CRITICAL
- **CVEs:** CVE-2004-2555 (Windows NT 4.0).
- **Analysis:** **False Positive**. Name collision.

### 7. SQLAlchemy @ 2.0.30

- **Severity:** HIGH
- **CVEs:** CVE-2019-7164 (SQLAlchemy < 0.7.0b4).
- **Analysis:** **False Positive**. Current version 2.0.30 is much newer.

### 8. urllib3 @ 2.6.0

- **Severity:** HIGH
- **CVEs:** CVE-2020-7212 (urllib3 < 1.26.0).
- **Analysis:** **False Positive**. Current version 2.6.0 is newer.

### 9. certifi @ 2024.7.4

- **Severity:** HIGH
- **CVEs:** CVE-2000-0409 (Netscape).
- **Analysis:** **False Positive**. Name collision.

### 10. idna @ 3.7

- **Severity:** HIGH
- **CVEs:** CVE-2016-8625 (libidn).
- **Analysis:** **False Positive**. Likely referring to C library libidn, not Python idna package, or fixed in newer versions.
