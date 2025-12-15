# Description: `test_base_agent.py`

## Module purpose
Legacy tests for base_agent.py.

These live next to the agent scripts so they can be run directly via:

    pytest scripts/agent/test_base_agent.py

## Location
- Path: `scripts/agent/test_base_agent.py`

## Public surface
- Classes: (none)
- Functions: base_agent_module, test_read_previous_content_existing_file, test_read_previous_content_missing_file_uses_default, test_improve_content_uses_run_subagent, test_update_file_writes_content, test_get_diff_contains_unified_markers

## Behavior summary
- Pure module (no obvious CLI/side effects).

## Key dependencies
- Top imports: `__future__`, `pathlib`, `pytest`, `agent_test_utils`, `base_agent`

## File fingerprint
- SHA256(source): `1ea1778db1319f48…`
