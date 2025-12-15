● I'll help you update the description for `test_agent-coder.py` by examining the current code and
    then updating its description file.

● I don't have write permissions. Here's the updated description content for
   `test_agent-coder.description.md`:

   ```markdown
   # test_agent-coder.py

   ## Purpose
   Legacy test suite for the CoderAgent class in agent-coder.py module.

   ## Public Surface
   **Fixtures:**
   - `base_agent_module`: Context manager fixture that imports base_agent module with proper path
   setup

   **Test Functions:**
   - `test_coder_agent_keyword_prompt_generates_suggestions`: Tests AI code improvement with
   keyword prompts
   - `test_coder_agent_non_keyword_delegates_to_base`: Tests delegation to BaseAgent.run_subagent
   for non-keyword prompts

   ## Behavior Summary
   - Tests CoderAgent class from agent-coder.py module
   - Verifies keyword prompts (containing "Improve") trigger AI code improvement suggestions
   - Verifies non-keyword prompts delegate to BaseAgent.run_subagent method
   - Uses pytest fixtures, monkeypatching, and temporary file paths for isolated testing
   - Validates content generation includes both "AI Code Improvement Suggestions" header and
   original content

   ## Key Dependencies
   **Standard Library:**
   - `__future__`: annotations support
   - `pathlib.Path`: file path handling

   **Testing Framework:**
   - `pytest`: test framework and fixtures (MonkeyPatch, tmp_path)

   **Test Utilities:**
   - `agent_test_utils.agent_dir_on_path`: context manager for agent module path setup
   - `agent_test_utils.load_agent_module`: dynamic agent module loader

   **Tested Modules:**
   - `base_agent.BaseAgent`: base class being mocked/tested for delegation behavior
   - `agent-coder.py` (loaded dynamically): module containing CoderAgent class under test
   ```
