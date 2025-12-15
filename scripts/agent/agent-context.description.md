● I'll analyze the current code in `agent-context.py` and update its description file to
   accurately reflect the implementation.

● Now I'll update the description file with accurate information based on the actual
   implementation:

● Let me try viewing and understanding the actual file structure better:

● I see that I don't have write permissions. Based on my analysis, here's the improved description
    that should replace the current content:

   ## Updated Description for `agent-context.description.md`

   The current file contains outdated notes and placeholder content. Here's what it should contain
   based on the actual implementation:

   ```markdown
   # Description: `agent-context.py`

   ## Module purpose
   Context Agent: Improves and updates code file descriptions.

   Reads context files (*.description.md), uses AI assistance to enhance descriptions,
   and updates files with improved documentation.

   # Description
   This module provides a Context Agent that:
   - Extends `BaseAgent` to handle `.description.md` files
   - Reads existing file descriptions or creates default content for new files
   - Uses AI to improve content through inherited `improve_content()` method
   - Gracefully handles missing AI backends by preserving original content
   - Provides CLI interface via `create_main_function` helper

   The agent ensures robust behavior when AI tools are unavailable:
   - Returns default content ("# Description\n\nNo description available.") for new files
   - Preserves original content unchanged when GitHub CLI is not found
   - Uses `BaseAgent.improve_content()` with proper fallback handling

   AI backend selection and configuration is handled by `scripts/agent/base_agent.py`.
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
   - `improve_content()` method delegates to parent class implementation

   ## Key dependencies
   - `base_agent.BaseAgent`: Core agent functionality
   - `base_agent.create_main_function`: CLI helper for agent creation

   ## Implementation details
   - Minimal implementation: only 70 lines including license header and docstring
   - Clean separation of concerns through inheritance
   - No direct AI backend logic (delegated to BaseAgent)
   ```

   **Key improvements in this updated description:**

   1. **Accurate architecture** - Correctly describes the inheritance from BaseAgent
   2. **Precise method documentation** - Details the two overridden methods and one delegated
   method
   3. **Clearer behavior** - Explains fallback handling and default content
   4. **Correct public API** - Lists both the class and the main function
   5. **Better dependencies** - Specifies both BaseAgent and create_main_function imports
   6. **Implementation insights** - Adds details about minimal LOC and separation of concerns

   This replaces the previous content which was just notes from a previous session rather than
   actual documentation.
