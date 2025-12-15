# Description: `agent.py`

## Module purpose
Agent: Orchestrates work among sub-agents for code improvement.

Assigns tasks to various agents to improve code files, their documentation,
tests, and related artifacts.

## Description
This module provides the main Agent that coordinates the improvement process
across code files by calling specialized sub-agents for different aspects
of code quality and documentation.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add better error handling
- Implement async execution for agents

## Improvements
- Enhanced coordination between agents
- Better progress tracking

## Location
- Path: `scripts/agent/agent.py`

## Public surface
- Classes: Agent
- Functions: load_codeignore, main

## Behavior summary
- Has a CLI entrypoint (`__main__`).
- Uses `argparse` for CLI parsing.
- Invokes external commands via `subprocess`.
- Mutates `sys.path` to import sibling modules.

## AI backend configuration
This agent system delegates AI calls to `BaseAgent.run_subagent(...)`.

Backend selection and configuration are controlled via `base_agent.py`:
- `DV_AGENT_BACKEND` (or CLI `--backend` on agents that use `create_main_function`)
- GitHub Models route env vars: `GITHUB_MODELS_BASE_URL`, `GITHUB_TOKEN`, and `DV_AGENT_MODEL`/`GITHUB_MODELS_MODEL`
- Context sizing: `DV_AGENT_MAX_CONTEXT_CHARS`

See `scripts/agent/base_agent.description.md` for details.

## Key dependencies
- Top imports: `subprocess`, `sys`, `pathlib`, `typing`, `argparse`, `fnmatch`, `fix_markdown_lint`

## File fingerprint
- SHA256(source): `63b11a5b3cfb3752…`
