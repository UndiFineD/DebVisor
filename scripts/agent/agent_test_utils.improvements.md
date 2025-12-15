# Improvements: `agent_test_utils.py`

## Suggested improvements
- [Fixed] Add a concise module docstring describing purpose/usage.
- [Fixed] Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports. (Kept as utility, added docstring/types)
- [Fixed] Function `agent_dir_on_path` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/agent_test_utils.py`
