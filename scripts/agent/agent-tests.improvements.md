# Improvements: `agent-tests.py`

## Suggested improvements
- Consider documenting class construction/expected invariants.
- Consider validating the input file name looks like a test module (e.g. starts with `test_`).
- Consider tailoring prompts so generated tests avoid brittle assertions and focus on behavior.
- Enhance the agent to read the *source code* file corresponding to the test file, to provide better context for test generation.
- Add support for detecting and using different test frameworks (pytest, unittest) based on existing imports or configuration.
- Add comprehensive docstrings to methods.
- Implement validation to ensure generated tests are syntactically correct before saving.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/agent-tests.py`
