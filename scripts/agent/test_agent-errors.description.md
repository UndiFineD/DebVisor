● I'll examine the current code in test_agent-errors.py and update its description file
   accordingly.

● I don't have permission to modify files. Here's the improved description that should be applied
   to `test_agent-errors.description.md`:

   ```markdown
   # Description: `test_agent-errors.py`

   ## Module purpose

   Unit tests for ErrorsAgent class in agent-errors.py, verifying delegation to BaseAgent for
   content improvement.

   ## Location

   - Path: `scripts/agent/test_agent-errors.py`

   ## Public surface

   - Fixtures: `base_agent_module` - imports and exposes base_agent module for testing
   - Tests: `test_errors_agent_delegates_to_base` - validates ErrorsAgent properly delegates to
   BaseAgent.run_subagent

   ## Behavior summary

   - Uses pytest fixtures and monkeypatching to test ErrorsAgent delegation
   - Creates temporary .errors.md files to test read/improve workflow
   - Mocks BaseAgent.run_subagent to verify integration without external dependencies
   - Verifies ErrorsAgent.improve_content() returns improved content via delegation

   ## Key dependencies

   - pytest: test framework with fixtures and monkeypatch
   - agent_test_utils: utilities for agent module loading (agent_dir_on_path, load_agent_module)
   - base_agent: BaseAgent class being tested via delegation

   ## Test coverage

   - Validates ErrorsAgent.improve_content() delegates to BaseAgent.run_subagent()
   - Tests reading previous content from .errors.md files
   - Verifies improved content is returned correctly ("IMPROVED")
   ```

   **Key improvements:**
   1. Removed vague "Legacy tests" label - this is an active unit test
   2. Specified it tests **ErrorsAgent** (not just agent-errors.py generically)
   3. Listed actual public surface: fixtures and test functions
   4. Expanded behavior summary with specific testing approach and verification steps
   5. Added comprehensive test coverage section detailing what's validated
   6. Clarified dependencies with specific utilities being used
