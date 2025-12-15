# Improvements: `test_agent-coder.py`

## Suggested improvements
- Keep explicit invocation of this test file (it is not pytest-discoverable due to the `-` in the name).
- Consider adding a test for the agent’s failure path (when `run_subagent` raises) to ensure content falls back safely.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/test_agent-coder.py`
