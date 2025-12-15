# Improvements: `agent-context.py`

## Suggested improvements
- Consider documenting class construction/expected invariants.
- Consider validating the input file name ends with `.description.md` to avoid accidental edits.
- Consider adding CLI args to select AI backend (`--backend`) and print diagnostics (`--describe-backends`).
- Enhance the agent to read the *source code* file corresponding to the description file. This is critical for generating accurate descriptions from scratch or updating them when code changes.
- Enforce a structured format for descriptions (e.g., sections for Purpose, Usage, Dependencies, Public Interface) to ensure consistency.
- Add logic to parse existing descriptions and only update sections that need changes, preserving manual edits where possible.

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/agent-context.py`
