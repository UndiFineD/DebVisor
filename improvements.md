# DebVisor Enterprise Platform – Pending Improvements

This document tracks only PENDING / FUTURE work items. All completed sessions and historical implementation tables were migrated to `changelog.md` on November 29, 2025.

**Last Updated:** November 29, 2025

**Scope:** Focused on advanced CI/CD, security, artifact integrity, and operational excellence enhancements (Session 11).

---

## 🔍 Session 11 Advanced CI/Security (Planned)

### X. Advanced Static Analysis & Supply Chain

| # | Improvement | File/Area | Priority | Status |
|---|-------------|-----------|----------|--------|
| X1 | Add CodeQL code scanning workflow | `.github/workflows/codeql.yml` | HIGH | ✅ DONE |
| X2 | Upload SARIF from flake8/pylint/mypy | `lint.yml` | MEDIUM | PENDING |
| X3 | Add dependency SBOM diff check | `sbom.yml` | MEDIUM | PENDING |
| X4 | Add pinned action version audit script | `scripts/action_audit.py` | LOW | PENDING |

### Y. Test Quality & Coverage Gates

| # | Improvement | File/Area | Priority | Status |
|---|-------------|-----------|----------|--------|
| Y1 | Enforce minimum coverage (85%) gate | `test.yml` | HIGH | PENDING |
| Y2 | Add mutation testing (mutmut) | `test.yml` | MEDIUM | PENDING |
| Y3 | Parallel test segmentation by marker | `pytest.ini` | MEDIUM | PENDING |
| Y4 | Add flaky test auto-rerun (pytest-rerunfailures) | `test.yml` | LOW | PENDING |

### Z. Release & Artifact Hardening

| # | Improvement | File/Area | Priority | Status |
|---|-------------|-----------|----------|--------|
| Z1 | GPG signed release artifacts | `release.yml` | HIGH | PENDING |
| Z2 | Add provenance attestation (SLSA) | `release.yml` | MEDIUM | PENDING |
| Z3 | Add changelog auto-generation (release-please) | `release.yml` | MEDIUM | PENDING |
| Z4 | Add Docker image build & vulnerability scan | `security.yml` | HIGH | PENDING |

### AA. Operational Excellence

| # | Improvement | File/Area | Priority | Status |
|---|-------------|-----------|----------|--------|
| AA1 | Add health dashboard summary to PR (markdown) | `test.yml` | LOW | PENDING |
| AA2 | Add consolidated SARIF bundle upload | `lint.yml` | MEDIUM | PENDING |
| AA3 | Add performance regression smoke benchmark | `tests/benchmarks/` | LOW | PENDING |
| AA4 | Add secret scan (trufflehog) workflow | `.github/workflows/secret-scan.yml` | HIGH | ✅ DONE |

### Implementation Plan (Session 11)

1. Create CodeQL scanning workflow.
1. Extend lint workflow to dump SARIF for flake8/pylint.
1. Add coverage gate (fail if <85%).
1. Add secret scanning workflow (trufflehog) on PRs.
1. Add Docker image build + Trivy vulnerability scan.
1. Integrate artifact attestation (SLSA provenance).
1. Add GPG signing stub (key import via secret).

---
