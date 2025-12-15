● I'll examine the test file and update its description based on the current code.

● Now let me check the current description file and the agent-context.py file to understand what's
    being tested:

● I don't have permission to modify files. Here's the improved description that should be applied
   to `test_agent-context.description.md`:

   ```markdown
   # Description: `test_agent-context.py`

   ## Module purpose
   Unit tests for ContextAgent class in agent-context.py, verifying delegation to BaseAgent for
   content improvement.

   ## Location
   - Path: `scripts/agent/test_agent-context.py`

   ## Public surface
   - Fixtures: `base_agent_module` - imports and exposes base_agent module for testing
   - Tests: `test_context_agent_delegates_to_base` - validates ContextAgent properly delegates to
   BaseAgent.run_subagent

   ## Behavior summary
   - Uses pytest fixtures and monkeypatching to test ContextAgent delegation
   - Creates temporary description files to test read/improve workflow
   - Mocks BaseAgent.run_subagent to verify integration without external dependencies

   ## Key dependencies
   - pytest: test framework with fixtures and monkeypatch
   - agent_test_utils: utilities for agent module loading (agent_dir_on_path, load_agent_module)
   - base_agent: BaseAgent class being tested via delegation

   ## Test coverage
   - Validates ContextAgent.improve_content() delegates to BaseAgent.run_subagent()
   - Tests reading previous content from .description.md files
   - Verifies improved content is returned correctly

   ## Implementation details
   - Test creates a temporary .description.md file with "BEFORE" content
   - Monkeypatches BaseAgent.run_subagent to return "IMPROVED" mock response
   - Verifies the ContextAgent correctly reads initial content and delegates improvement to
   BaseAgent
   - Confirms the delegation flow: read_previous_content() → improve_content() → run_subagent()
   ```

   The updated description removes the outdated "Legacy tests" label and adds a new "Implementation
    details" section that describes the test workflow.
