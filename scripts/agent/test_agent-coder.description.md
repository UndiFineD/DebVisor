● I'll help you update the description for `test_agent-coder.py` by first examining the current
   code to understand its actual structure and purpose.

● Now let me find and view the context file that needs updating:

● Now I'll update the description file based on the actual current code:

● I don't have write permissions to make edits. Based on my analysis of the current code, here are
    the recommended updates to `test_agent-coder.description.md`:

   **Public surface section** - Change to distinguish fixtures from test functions:
   - Fixtures: base_agent_module
   - Test functions: test_coder_agent_keyword_prompt_generates_suggestions,
   test_coder_agent_non_keyword_delegates_to_base

   **Behavior summary** - Expand with actual test behaviors:
   - Tests CoderAgent class from agent-coder.py module
   - Verifies keyword prompts trigger AI code improvement suggestions
   - Verifies non-keyword prompts delegate to BaseAgent.run_subagent
   - Uses pytest fixtures, monkeypatching, and temporary file paths for testing

   **Key dependencies** - Restructure for clarity:
   - Top imports: `__future__`, `pathlib`, `pytest`
   - Test utilities: `agent_test_utils` (agent_dir_on_path, load_agent_module)
   - Tested module: `base_agent` (BaseAgent class)
