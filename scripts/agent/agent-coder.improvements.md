# Improvements: `agent-coder.py`

## Suggested improvements
- Consider documenting class construction/expected invariants.
- Consider adding CLI args to select AI backend (`--backend`) and print diagnostics (`--describe-backends`).
- Consider tailoring prompts with language/runtime hints based on file extension.
- Improve `improve_content` to handle AI failures more gracefully than overwriting the file with comments.
- Implement actual code generation logic or integration with a more capable coding model if the current one is limited to suggestions.
- Add language detection based on file extension to provide more context-aware prompts.
- Add unit tests for `_get_fallback_response` and `improve_content` logic.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/agent-coder.py`
