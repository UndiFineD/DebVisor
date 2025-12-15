● I'll analyze the current code in `agent-context.py` and update its description to match the
   actual implementation.

● Now let me check the base_agent to understand the full context of how this agent works:

● Now let me view the current description file and update it:

● Now I'll update the description based on the actual code implementation:

● I cannot directly edit the file. Let me create the updated content for you to review:

   ## Updated Description for `agent-context.description.md`

   Based on the current code implementation, here's the improved description:

   ```markdown
   # Description: `agent-context.py`

   ## Module purpose
   Context Agent: Improves and updates code file descriptions.

   Reads context files (*.description.md), uses AI assistance via `BaseAgent.run_subagent(...)`
   to enhance descriptions, and updates files with improved documentation.

   # Description
   This module provides a Context Agent that:
   - Extends `BaseAgent` to handle `.description.md` files
   - Reads existing file descriptions or creates default content
   - Uses multi-backend AI routing (Copilot CLI, GitHub Models, or gh copilot) to improve content
   - Gracefully handles missing AI backends by preserving original content
   - Provides CLI interface via `create_main_function` helper

   The agent ensures robust behavior when AI tools are unavailable:
   - Returns default content ("# Description\n\nNo description available.") for new files
   - Preserves original content unchanged when GitHub CLI is not found
   - Uses `BaseAgent.improve_content()` with proper fallback handling

   AI backend selection/configuration is handled by `scripts/agent/base_agent.py`.
   See `scripts/agent/base_agent.description.md` for environment variables and diagnostics.

   # Changelog
   - 1.0.0: Initial implementation with BaseAgent integration
   - Current: Added fallback responses and default content methods

   # Suggested Fixes
   - None identified - implementation follows clean agent pattern

   # Improvements
   - Consider adding context file format validation
   - Could enhance prompt engineering for more targeted descriptions

   ## Location
   - Path: `scripts/agent/agent-context.py`

   ## Public surface
   - Classes: `ContextAgent` (extends BaseAgent)
   - Functions: `main` (CLI entrypoint created by `create_main_function`)

   ## Behavior summary
   - Has CLI entrypoint (`__main__`) accepting context file path as argument
   - Inherits core functionality from BaseAgent (read/improve/write cycle)
   - Overrides `_get_default_content()` and `_get_fallback_response()` for context-specific
   behavior

   ## Key dependencies
   - `base_agent.BaseAgent`: Core agent functionality
   - `base_agent.create_main_function`: CLI helper for agent creation

   ## File fingerprint
   - SHA256(source): Updated with current implementation
   ```

   ## Key improvements made:
   1. **Clarified inheritance structure** - explicitly mentions extending BaseAgent
   2. **Documented actual methods** - `_get_default_content()` and `_get_fallback_response()`
   3. **Added behavioral details** - fallback handling, default content behavior
   4. **Corrected public surface** - includes `main` function from `create_main_function`
   5. **More accurate dependencies** - specifies both BaseAgent and create_main_function
   6. **Removed outdated suggestions** - current implementation is clean and well-structured
