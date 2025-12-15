# Description: `agent-coder.py`

## Module purpose
Coder Agent: Improves and updates code files.

Reads a code file, uses `BaseAgent.run_subagent(...)` (multi-backend AI routing) to enhance the code,
and updates the code file with improvements.

## Description
This module provides a Coder Agent that reads existing code files,
uses AI assistance to improve and complete them, and updates the code files
with enhanced implementations.

AI backend selection/configuration is handled by `scripts/agent/base_agent.py`.
See `scripts/agent/base_agent.description.md` for environment variables and diagnostics.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add validation for code file format
- Improve prompt engineering for better code improvements

## Improvements
- Better integration with other agents
- Enhanced diff reporting

## Location
- Path: `scripts/agent/agent-coder.py`

## Public surface
- Classes: CoderAgent
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `base_agent`

## File fingerprint
- SHA256(source): `fc172a89fb676516…`
