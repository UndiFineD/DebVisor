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
