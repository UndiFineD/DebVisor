# Improvements: `agent-context.py`

## Fixed
- Add logging for all major actions. (Fixed)
- Add type hints for all methods. (Fixed)

## Suggested improvements
- [ ] Automatically extract class and function signatures for context using AST parsing.
- [ ] Include recent git history in the context (last 10 commits with messages).
- [ ] Add dependency graph analysis: show imports and dependencies.
- [ ] Implement context summarization for large files (>1000 lines).
- [ ] Add related files detection: find files that import or use this module.
- [ ] Extract public API documentation from docstrings.
- [ ] Include test coverage metrics from test files.
- [ ] Add code metrics: cyclomatic complexity, lines of code, maintainability index.
- [ ] Detect code smells and anti-patterns for context.
- [ ] Include architecture decisions and design patterns used.
- [ ] Add recent change statistics: frequency, time since last change, contributors.
- [ ] Support custom context providers via plugin system.
- [ ] Implement context caching for improved performance.
- [ ] Add context prioritization: most relevant information first.
- [ ] Generate context visualization (dependency graphs, architecture diagrams).
- [ ] Support context filtering: include/exclude patterns for sensitive data.
- [ ] Add cross-module context: relationships with other files in project.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/agent-context.py`
