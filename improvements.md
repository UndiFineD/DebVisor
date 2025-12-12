# Project Improvements

This document tracks near-term improvements to DebVisor to enhance reliability,
maintainability, and developer experience. It prioritizes items, outlines
implementation steps, and defines measurable success criteria.

## Overview

- Focus: documentation quality, automation, CI reliability, and tooling consistency.

## Priority Areas

### High Priority

- Markdown quality: ensure consistent formatting and enforce checks.
- CI stability: add lint/test gates and visible reporting.
- Developer tasks: provide convenient VS Code tasks for common actions.

### Medium Priority

- Code fences: add language hints where identifiable for readability.
- Docs structure: unify headings, lists, and section patterns across docs.
- Release notes: standardize change logging and verification.

### Low Priority

- Line length guidance: recommend wrapping for readability without breaking URLs.
- Optional tooling: document opt-in enhancements and performance tips.

## Implementation Plan

1. Markdown fixer improvements
   - Refine numbered list detection to avoid version/decimal mangling.
   - Normalize headings and list markers; enforce final newline.
   - Add unit tests for fixer behaviors and a task to run them.

2. Markdown lint integration (Python)
   - Use PyMarkdown for linting; add a VS Code task to run checks.
   - Integrate a CI job to run PyMarkdown on PRs and pushes.

3. Developer ergonomics
   - Provide tasks for venv activation, fixer run, and tests.
   - Document quick commands in README for consistency.

## Metrics

- Lint warnings: reduce to zero for all tracked rules.
- Test coverage: unit tests for fixer logic pass and remain green.
- CI health: pipelines succeed consistently with clear failures if rules break.

## Timeline

- Week 1: Finalize fixer logic and add tests/tasks.
- Week 2: Introduce markdownlint, fix flagged items, wire CI.
- Week 3: Audit docs for consistent structure and code fence languages.

## Risks & Mitigations

- Over-fixing content: limit fixer scope to formatting-safe changes; use tests.
- CI noise: start with advisory checks, then enforce once passing.
- Edge cases: expand tests when new patterns are discovered.

## Quick Commands

```powershell
# Run fixer for a file
& .\.venv\Scripts\python.exe .\fix_markdown_lint.py .\docs\CONTRIBUTING.md

# Run fixer for all Markdown files
Get-ChildItem -Recurse -Filter *.md | ForEach-Object {
    & .\.venv\Scripts\python.exe .\fix_markdown_lint.py $_.FullName
}

# Run fixer unit tests
& .\.venv\Scripts\python.exe .\scripts\test_fix_markdown_lint.py
```

## Cross-References

- Fixer script: [fix_markdown_lint.py](fix_markdown_lint.py)
- Fixer tests: [scripts/test_fix_markdown_lint.py](scripts/test_fix_markdown_lint.py)
- VS Code tasks: [.vscode/tasks.json](.vscode/tasks.json)
- PyMarkdown config: [pymarkdown.json](pymarkdown.json)
- CI workflow: [.github/workflows/markdownlint.yml](.github/workflows/markdownlint.yml)
- Contributing guide: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

## Issue Checklist

- [ ] Integrate PyMarkdown and add a VS Code task
- [ ] Add GitHub Action to run PyMarkdown and fixer tests on PRs
- [ ] Audit code fences across docs and add language hints where clear
- [ ] Document common developer tasks in [README.md](README.md)
- [ ] Create a guide for optional tooling in [docs/OPTIONAL_TOOLS.md](docs/OPTIONAL_TOOLS.md)
- [ ] Ensure consistent headings and lists across [docs/](docs/) and [opt/docs/](opt/docs/)
