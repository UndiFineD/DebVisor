# Improvements: `agent_test_utils.py`

## Suggested improvements
- [Fixed] Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports.
    - *Note*: Added `get_base_agent_module()` helper to avoid `sys.path` modification. Retained `agent_dir_on_path` with documentation for legacy test support.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/agent_test_utils.py`
