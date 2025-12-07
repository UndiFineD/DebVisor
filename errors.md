# CI/CD Error Report

This document tracks active errors and technical debt in the repository.

## 1. VS Code Diagnostics

**Error:** `Unable to find reusable workflow` in `.github/workflows/deploy.yml`
**Status:** False Positive
**Details:** The referenced file `.github/workflows/_notify.yml` exists. This is a known issue with the VS Code GitHub Actions extension validation logic.


