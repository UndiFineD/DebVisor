# CI/CD Error Report

This document summarizes the errors found in recent GitHub Actions workflow runs.

## 1. CodeQL Analysis

**Run ID:** 19994506311
**Status:** Failed (Resolved in later runs)
**Error Message:**

```text

##[error]Please verify that the necessary features are enabled: Code scanning is not enabled for this repository. Please enable code scanning in the repository settings. - <https://docs.github.com/rest>

```text

**Context:** This error occurred because the repository was Private. It has since been made Public, and subsequent runs (e.g., 19994570734) have passed.

## 2. Release Please

**Run ID:** 19994425513
**Status:** Failed
**Error Message:**

```text

##[error]release-please failed: Input required and not supplied: token

```text

**Context:** The `release-please` action requires a `token` input (usually `${{ secrets.GITHUB_TOKEN }}` or a PAT) which appears to be missing or not correctly passed in the workflow configuration.

## 3. Markdown Lint

**Run ID:** 19994371352
**Status:** Failed
**Summary:** Multiple markdown style violations were detected.
**Common Errors:**

- **MD050/strong-style:** Strong style should be asterisks (e.g., `**text**`) instead of underscores (`**text**`).
- **MD022/blanks-around-headings:** Headings should be surrounded by blank lines.
- **MD032/blanks-around-lists:** Lists should be surrounded by blank lines.
- **MD031/blanks-around-fences:** Fenced code blocks should be surrounded by blank lines.
- **MD029/ol-prefix:** Ordered list item prefix should be `1.` (or sequential depending on style).
- **MD034/no-bare-urls:** Bare URLs should be wrapped in angle brackets `<http://...>`.
- **MD009/no-trailing-spaces:** Lines should not have trailing spaces.
- **MD040/fenced-code-language:** Fenced code blocks should have a language specified.

## Status Update

- **CodeQL Analysis:** Resolved by changing repository visibility to Public.
- **Release Please:** Fixed by updating `.github/workflows/release-please.yml` to include `token: ${{ secrets.GITHUB_TOKEN }}`.
- **Markdown Lint:** Automated fix script `scripts/fix_markdown_lint_comprehensive.py` was created and executed. It addressed MD050, MD022, MD032, MD031, MD029, MD034, MD009, and MD040 across the codebase.

## Recent Failures (2025-12-06)

**Run #74 (CodeQL Analysis)**

- **Status:** Fix Applied
- **Step:** Perform CodeQL Analysis
- **Context:** Fails for both Python and JavaScript. This might be due to build issues or configuration.
- **Resolution:** Updated workflow to install Python dependencies and setup Python environment.

## Analysis of Recent "Failures" (2025-12-06)

Upon investigation of recent workflow runs (e.g., #19994770587, #19994770578), the reported "failures" are actually **cancellations**.

- **Cause:** The workflows are configured with `concurrency: cancel-in-progress: true`. When new commits are pushed rapidly, previous runs are automatically cancelled to save resources.
- **Impact:** These are not actual code errors and can be ignored.
- **CodeQL Status:** The CodeQL workflow has successfully passed in recent runs (e.g., #19994770584), confirming the previous fix works.

## VS Code Diagnostics

**Error:** `Unable to find reusable workflow` in `.github/workflows/deploy.yml`

- **Context:** This appears to be a false positive from the VS Code GitHub Actions extension. The referenced file `.github/workflows/_notify.yml` exists in the repository and is correctly referenced.
- **Status:** Ignored (False Positive).

## Runner Status Diagnosis

**Issue:** Self-hosted runner `DESKTOP-F4EG0P1` is **stuck**.

- **Status:** `online`
- **State:** `busy`
- **Observation:** The runner reports being busy, but no workflows targeting `self-hosted` are currently `in_progress` (they are all `queued`).
- **Diagnosis:** The runner process is likely hung or stuck processing a previous job that didn't exit cleanly.
- **Action Required:**

    1.  Access the machine `DESKTOP-F4EG0P1`.
    1.  Open PowerShell as Administrator.
    1.  Run the following command to restart the service:

        ```powershell

        Restart-Service "actions.runner.UndiFineD-DebVisor.DESKTOP-F4EG0P1"

```text

    1.  **If the runner remains busy:**

  - Stop the service: `Stop-Service "actions.runner.UndiFineD-DebVisor.DESKTOP-F4EG0P1"`
  - Wait 30 seconds.
  - Start the service: `Start-Service "actions.runner.UndiFineD-DebVisor.DESKTOP-F4EG0P1"`
  - Check the runner logs in the `_diag` folder in the runner installation directory.

## Notification Flood Investigation

**User Report:** "Many errors in action notifications"

**Status:** ✅ **RESOLVED**

**Investigation Summary:**

1.  **Root Cause:** The self-hosted runner `DESKTOP-F4EG0P1` was in a "Zombie" state—processing a job that GitHub considered dead. This caused all subsequent jobs to queue up indefinitely.
1.  **Resolution:** Force restarted the runner service (`Stop-Service -Force` / `Start-Service`).
1.  **Outcome:**

- The runner reconnected and successfully completed the stuck `SBOM Generation` job (Run ID: 19994506315).
  - The queue has started moving. Recent runs (e.g., `docs: update errors.md...`) are now `in_progress`.

**Current Status:**

- **Runner:** Healthy & Active
- **Queue:** Processing normally (backlog is clearing)
- **Action Required:** None. The system is recovering automatically.

## Code Scanning Alerts

| Number | Tool | Rule | Description | State | URL |
|---|---|---|---|---|---|
| 5113 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5113) |
| 5112 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5112) |
| 5111 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5111) |
| 5110 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5110) |
| 5109 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5109) |
| 5108 | flake8 | E305 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5108) |
| 5107 | flake8 | E501 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5107) |
| 5106 | flake8 | E302 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5106) |
| 5105 | flake8 | E302 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5105) |
| 5104 | flake8 | E302 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5104) |
| 5103 | flake8 | E302 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5103) |
| 5102 | flake8 | E302 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5102) |
| 5101 | flake8 | E306 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5101) |
| 5100 | flake8 | E302 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5100) |
| 5099 | flake8 | E302 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5099) |
| 5098 | flake8 | E117 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5098) |
| 5097 | flake8 | E111 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5097) |
| 5096 | flake8 | E302 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5096) |
| 5095 | flake8 | E302 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5095) |
| 5094 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5094) |
| 5093 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5093) |
| 5092 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5092) |
| 5091 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5091) |
| 5090 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5090) |
| 5089 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5089) |
| 5088 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5088) |
| 5087 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5087) |
| 5086 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5086) |
| 5085 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5085) |
| 5084 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5084) |
| 5083 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5083) |
| 5082 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5082) |
| 5081 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5081) |
| 5080 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5080) |
| 5079 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5079) |
| 5078 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5078) |
| 5077 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5077) |
| 5076 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5076) |
| 5075 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5075) |
| 5074 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5074) |
| 5073 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5073) |
| 5072 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5072) |
| 5071 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5071) |
| 5070 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5070) |
| 5069 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5069) |
| 5068 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5068) |
| 5067 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5067) |
| 5066 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5066) |
| 5065 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5065) |
| 5064 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5064) |
| 5063 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5063) |
| 5062 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5062) |
| 5061 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5061) |
| 5060 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5060) |
| 5059 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5059) |
| 5058 | flake8 | F541 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5058) |
| 5057 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5057) |
| 5056 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5056) |
| 5055 | flake8 | F841 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5055) |
| 5054 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5054) |
| 5053 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5053) |
| 5052 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5052) |
| 5051 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5051) |
| 5050 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5050) |
| 5049 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5049) |
| 5048 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5048) |
| 5047 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5047) |
| 5046 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5046) |
| 5045 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5045) |
| 5044 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5044) |
| 5043 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5043) |
| 5042 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5042) |
| 5041 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5041) |
| 5040 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5040) |
| 5039 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5039) |
| 5038 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5038) |
| 5037 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5037) |
| 5036 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5036) |
| 5035 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5035) |
| 5034 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5034) |
| 5033 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5033) |
| 5032 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5032) |
| 5031 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5031) |
| 5030 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5030) |
| 5029 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5029) |
| 5028 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5028) |
| 5027 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5027) |
| 5026 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5026) |
| 5025 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5025) |
| 5024 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5024) |
| 5023 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5023) |
| 5022 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5022) |
| 5021 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5021) |
| 5020 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5020) |
| 5019 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5019) |
| 5018 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5018) |
| 5017 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5017) |
| 5016 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5016) |
| 5015 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5015) |
| 5014 | flake8 | W293 |  | open | [Link](https://github.com/UndiFineD/DebVisor/security/code-scanning/5014) |

## Known Issues

### Issue #11: CI Failure Summary

**URL:** https://github.com/UndiFineD/DebVisor/issues/11

**Description:**

## CI Failure Summary (last 50 runs)

_Updated: 2025-12-06T21:27:06.616Z_

Found **9** problematic runs:

- Run **#74** (CodeQL Analysis) - conclusion: **failure** - [View Run](https://github.com/UndiFineD/DebVisor/actions/runs/19994464660)
- Run **#73** (CodeQL Analysis) - conclusion: **failure** - [View Run](https://github.com/UndiFineD/DebVisor/actions/runs/19994425642)
- Run **#79** (Syntax & Config Validation) - conclusion: **cancelled** - [View Run](https://github.com/UndiFineD/DebVisor/actions/runs/19994425468)
- Run **#78** (Syntax & Config Validation) - conclusion: **cancelled** - [View Run](https://github.com/UndiFineD/DebVisor/actions/runs/19994371357)
- Run **#72** (CodeQL Analysis) - conclusion: **failure** - [View Run](https://github.com/UndiFineD/DebVisor/actions/runs/19994371354)
- Run **#30** (Markdown Lint) - conclusion: **failure** - [View Run](https://github.com/UndiFineD/DebVisor/actions/runs/19994371352)
- Run **#66** (Release Please) - conclusion: **failure** - [View Run](https://github.com/UndiFineD/DebVisor/actions/runs/19994261251)
- Run **#71** (CodeQL Analysis) - conclusion: **failure** - [View Run](https://github.com/UndiFineD/DebVisor/actions/runs/19994261231)
- Run **#29** (Markdown Lint) - conclusion: **failure** - [View Run](https://github.com/UndiFineD/DebVisor/actions/runs/19994100913)

### Details for first failing run (#74)

- Job: **Analyze (CodeQL) (python)** - conclusion: **failure**
- Step: Perform CodeQL Analysis (conclusion: failure)
- Job: **Analyze (CodeQL) (javascript)** - conclusion: **failure**
- Step: Perform CodeQL Analysis (conclusion: failure)

---
Generated by hourly CI Diagnostics workflow.

---

### Issue #12: [Workflow Failure] Security & Dependency Scanning

**URL:** https://github.com/UndiFineD/DebVisor/issues/12

**Description:**

## Workflow Failure Alert

**Workflow**: Security & Dependency Scanning
**Status**: failure
**Run**: [View Run](https://github.com/UndiFineD/DebVisor/actions/runs/19994100903)
**Triggered by**: UndiFineD
**Ref**: refs/heads/main

Failed jobs or findings detected.

- Dependency Check: success
- Security Scan: success
- Container Scan: success

Run: https://github.com/UndiFineD/DebVisor/actions/runs/19994100903

---
*Auto-generated by workflow failure notification*

---

## Fixes Implemented (Dec 7, 2025)

### 1. Security & Dependency Scanning (Issue #12)

- **Problem:** The workflow failed because 	rivy was not found in the PATH during the version check step.
- **Fix:** Updated .github/workflows/security.yml to call ./tools/trivy directly after installation, ensuring the version check passes before the PATH update takes effect in subsequent steps.

### 2. Markdown Lint Errors (Issue #11)

- **Problem:** Multiple markdown files had formatting issues (trailing spaces, list indentation, etc.).
- **Fix:** Ran scripts/fix_markdown_lint.py across all markdown files in the repository.
- **Result:** Fixed 132 issues in 29 files.

### 3. Release Please Token (Issue #11)

- **Problem:** Workflow failed with 'Input required and not supplied: token'.
- **Fix:** Updated .github/workflows/release-please.yml to use github.token instead of secrets.GITHUB_TOKEN as the fallback, which is more robust in some runner contexts.

### 4. Code Scanning Alerts

- **Problem:** Hundreds of lake8 errors in import_wizard.py and ix_markdown_lint_comprehensive.py.
- **Fix:** Manually refactored import_wizard.py to resolve E501 (line length) and other errors. ix_markdown_lint_comprehensive.py was also cleaned up.
- **Result:** All open alerts for these files should now be resolved.

## 4. Test Suite Linting

**Status:** In Progress
**Initial State:** The 	ests/ directory contained hundreds of linting errors, primarily:
- F401: Unused imports.
- E501: Line too long.
- F841: Unused variables.
- E999: Syntax errors (trailing commas).

**Actions Taken:**
- Ran utopep8 to fix formatting issues.
- Created and ran scripts to remove unused imports (F401).
- Fixed syntax errors (E999) caused by automated cleanup.
- Renamed ambiguous variables (E741) and unused variables (F841).

**Current State:**
- All SyntaxErrors resolved.
- All F401 (unused imports) resolved.
- Remaining issues:
  - E501: Line too long (requires manual refactoring or configuration change).
  - F841: Unused variables (prefixed with _, but still reported by strict flake8).

