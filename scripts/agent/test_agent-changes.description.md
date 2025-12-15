● I'll analyze the current test file and update its description with accurate context.

● Now let me check the agent-changes.py file to better understand what's being tested:

● Now let me update the description file with improved context based on the actual code:

● Let me check the current content of the description file first:

● I'm unable to edit the file due to write permissions. Let me provide you with the improved
   description content that should be used:

   ```markdown
   # Description: `test_agent-changes.py`

   ## Module purpose
   Test suite for ChangesAgent functionality in agent-changes.py.

   Verifies the behavior of the ChangesAgent class which improves code file changelogs:
   - Tests keyword-based prompt recognition that generates changelog improvement suggestions
   - Tests delegation to BaseAgent for non-changelog-specific prompts

   Run directly via:

       pytest scripts/agent/test_agent-changes.py

   ## Location
   - Path: `scripts/agent/test_agent-changes.py`

   ## Public surface
   - Fixtures: `base_agent_module` - provides base_agent module with proper path context
   - Tests:
     - `test_changes_agent_keyword_prompt_generates_suggestions` - validates that prompts
   containing keywords like "improve", "change", or "log" trigger AI changelog suggestions with
   10-point improvement guidelines
     - `test_changes_agent_non_keyword_delegates_to_base` - validates that non-keyword prompts
   delegate to BaseAgent.run_subagent()

   ## Behavior summary
   - Pure test module using pytest fixtures and monkeypatching
   - Tests ChangesAgent instantiation with temporary .changes.md files
   - Validates prompt detection logic and content generation
   - Uses agent_test_utils for module loading with proper Python path context

   ## Key dependencies
   - Standard library: `pathlib`, `__future__`
   - Test framework: `pytest` (fixtures, MonkeyPatch)
   - Project modules: `agent_test_utils` (agent_dir_on_path, load_agent_module), `base_agent`
   - Tested module: `agent-changes.py` (ChangesAgent class)

   ## Test coverage
   - Keyword prompt detection (improve/change/log keywords)
   - Changelog suggestion format (10-point guidelines with original content preserved)
   - BaseAgent delegation for non-changelog prompts
   - File I/O with temporary paths
   ```

   The updated description provides more accurate context including detailed test function
   purposes, improved dependency information, and a new "Test coverage" section that summarizes
   what aspects are tested.
