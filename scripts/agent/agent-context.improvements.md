# Improvements: `agent-context.py`

## Fixed
- Add logging for all major actions. (Fixed)
- Add type hints for all methods. (Fixed)

## Suggested improvements
- [x] Automatically extract class and function signatures for context using AST parsing.
- [x] Include recent git history in the context (last 10 commits with messages).
- [x] Add dependency graph analysis: show imports and dependencies.
- [x] Implement context summarization for large files (>1000 lines).
- [x] Add related files detection: find files that import or use this module.
- [x] Extract public API documentation from docstrings.
- [x] Include test coverage metrics from test files.
- [x] Add code metrics: cyclomatic complexity, lines of code, maintainability index.
- [x] Detect code smells and anti-patterns for context.
- [x] Include architecture decisions and design patterns used.
- [x] Add recent change statistics: frequency, time since last change, contributors.
- [x] Support custom context providers via plugin system.
- [x] Implement context caching for improved performance.
- [x] Add context prioritization: most relevant information first.
- [x] Generate context visualization (dependency graphs, architecture diagrams).
- [x] Support context filtering: include/exclude patterns for sensitive data.
- [x] Add cross-module context: relationships with other files in project.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/agent-context.py`
