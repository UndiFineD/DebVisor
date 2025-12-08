# CI/CD Error Report

## Active Errors

### 1. Security & Linting (Local Scan)

**Status:** Resolved (No active issues)

### 2. CI/CD Pipeline (Inferred)

**Status:** Failing

- **Unit Tests:** Passing (Fixed import collision in `tests/test_netcfg_mock.py` and timeout in `tests/test_performance_testing.py`).
- **Linting:** Passing (Markdown lint errors resolved).
- **Release:** Permission issues with `release-please`.

### 3. GitHub Issues (Remote)

**Source:** `UndiFineD/DebVisor` Issues
**Status:** Open Issues Found

| Issue # | Title | Created At | Summary |
|---|---|---|---|
| **#15** | CI Failure Summary | 2025-12-07 | Automated report listing 16 problematic runs (Lint, Unit Tests, Release Please). |

**Notifications:** No open issues mentioning `UndiFineD` found.

## Next Steps

1. Update `requirements-test.txt` to fix CI failures.

## CI Failures

Run find usr/local/bin -name "*.sh" -type f -exec shellcheck -x {} +

In usr/local/bin/debvisor-vm-enhanced.sh line 123:
    trap 'rmdir "'$lock_file'" 2>/dev/null || true' EXIT
                  ^--------^ SC2086 (info): Double quote to prevent globbing and word splitting.

Did you mean: 
    trap 'rmdir "'"$lock_file"'" 2>/dev/null || true' EXIT

For more information:
  https://www.shellcheck.net/wiki/SC2086 -- Double quote to prevent globbing ...
Error: Process completed with exit code 1.

Run googleapis/release-please-action@v4
Running release-please version: 17.1.3
❯ Fetching release-please-config.json from branch main
❯ Fetching .release-please-manifest.json from branch main
✔ Building releases
✔ Building strategies by path
❯ .: simple
❯ Found pull request #5: 'chore(main): release 0.1.1'
✔ Building release for path: .
❯ type: simple
❯ targetBranch: main
✔ Creating 1 releases for pull #5
Error: release-please failed: Resource not accessible by integration - https://docs.github.com/rest/releases/releases#create-a-release

Run googleapis/release-please-action@v4
Running release-please version: 17.1.3
❯ Fetching release-please-config.json from branch main
❯ Fetching .release-please-manifest.json from branch main
✔ Building releases
✔ Building strategies by path
❯ .: simple
❯ Found pull request #5: 'chore(main): release 0.1.1'
✔ Building release for path: .
❯ type: simple
❯ targetBranch: main
✔ Creating 1 releases for pull #5
Error: release-please failed: Resource not accessible by integration - https://docs.github.com/rest/releases/releases#create-a-release


https://github.com/UndiFineD/DebVisor/actions/runs/20004613615/job/57364936648

Run DavidAnson/markdownlint-cli2-action@v16
markdownlint-cli2 v0.13.0 (markdownlint v0.34.0)
Finding: **/*.md
Linting: 105 file(s)
Summary: 4 error(s)
Error: docs/monitoring-health-detail.md:85 MD012/no-multiple-blanks Multiple consecutive blank lines [Expected: 1; Actual: 2] https://github.com/DavidAnson/markdownlint/blob/v0.34.0/doc/md012.md
Error: iso-building.md:134 MD012/no-multiple-blanks Multiple consecutive blank lines [Expected: 1; Actual: 2] https://github.com/DavidAnson/markdownlint/blob/v0.34.0/doc/md012.md
Error: OPTIONAL_TOOLS.md:66 MD012/no-multiple-blanks Multiple consecutive blank lines [Expected: 1; Actual: 2] https://github.com/DavidAnson/markdownlint/blob/v0.34.0/doc/md012.md
Error: RUNNER_SETUP_GUIDE.md:475 MD012/no-multiple-blanks Multiple consecutive blank lines [Expected: 1; Actual: 2] https://github.com/DavidAnson/markdownlint/blob/v0.34.0/doc/md012.md
Error: Failed with exit code: 1

