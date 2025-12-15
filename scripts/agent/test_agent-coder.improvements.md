# Improvements: `test_agent-coder.py`

## Suggested improvements
- [Fixed] Function `base_agent_module` is missing type annotations.
- [Fixed] Function `test_coder_agent_keyword_prompt_generates_suggestions` is missing type annotations.
- [Fixed] Function `test_coder_agent_non_keyword_delegates_to_base` is missing type annotations.
- Rename the file to be pytest-importable (avoid '-' and extra '.'), then update references.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/test_agent-coder.py`
