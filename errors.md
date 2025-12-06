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

**Sample Log Output:**

```text

DESIGN.md:843:6 MD050/strong-style Strong style [Expected: asterisk; Actual: underscore]
README.md:13:3 MD050/strong-style Strong style [Expected: asterisk; Actual: underscore]
RUNNER_FIX_SUMMARY.md:5 MD022/blanks-around-headings Headings should be surrounded by blank lines
RUNNER_FIX_SUMMARY.md:9 MD032/blanks-around-lists Lists should be surrounded by blank lines
RUNNER_FIX_SUMMARY.md:14 MD031/blanks-around-fences Fenced code blocks should be surrounded by blank lines
RUNNER_FIX_SUMMARY.md:70:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/1/1]
TEST_API_MISMATCH_ANALYSIS.md:8 MD031/blanks-around-fences Fenced code blocks should be surrounded by blank lines

```text


## Status Update

- **CodeQL Analysis:** Resolved by changing repository visibility to Public.
- **Release Please:** Fixed by updating `.github/workflows/release-please.yml` to include `token: ${{ secrets.GITHUB_TOKEN }}`.
- **Markdown Lint:** Automated fix script `scripts/fix_markdown_lint_v2.py` was created and executed. It addressed MD050, MD022, MD032, MD031, MD029, MD034, MD009, and MD040 across the codebase.


## Recent Failures (2025-12-06)

**Run #74 (CodeQL Analysis)**
- **Status:** Failed
- **Step:** Perform CodeQL Analysis
- **Context:** Fails for both Python and JavaScript. This might be due to build issues or configuration.

**Run #79, #78 (Syntax & Config Validation)**
- **Status:** Cancelled
- **Context:** Likely cancelled due to new commits pushed to the branch.
