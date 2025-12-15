● I'll examine the current test file and update its description based on the actual code.

● Now let me check the agent-context.py file to understand what's being tested:

● Now I'll update the description with accurate information about the current code:

● Let me check the file permissions:

● I don't have permission to modify files in this environment. Based on my analysis of the current
    code, here's the improved description that should be applied to
   `test_agent-context.description.md`:

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
   ```

   The updated description is more accurate, removing "Legacy tests" label and providing specific
   details about what's being tested and how.
