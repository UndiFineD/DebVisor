# Description: `base_agent.py`

## Module purpose
Base Agent: Common functionality for all AI-powered agents.

Provides shared functionality for agents that improve code files using AI assistance.

## Location
- Path: `scripts/agent/base_agent.py`

## Public surface
- Classes: BaseAgent
- Functions: create_main_function

## Behavior summary
- Uses `argparse` for CLI parsing.
- Invokes external commands via `subprocess`.
- Mutates `sys.path` to import sibling modules.

## Key dependencies
- Top imports: `subprocess`, `pathlib`, `argparse`, `difflib`, `sys`, `fix_markdown_lint`

## File fingerprint
- SHA256(source): `9cf7e036000a9bba…`
