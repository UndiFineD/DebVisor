● I'll help you update the description for `agent_test_utils.py` by first examining the current
   code and then updating the documentation.

● Now let me view the current description file:

● Now I'll update the description based on the actual code content:

● I don't have permission to write to the file. Here's the updated description content that should
    be used:

   ```markdown
   # Description: `agent_test_utils.py`

   ## Module purpose
   Utilities for loading and testing agent modules within the `scripts/agent` directory. Provides
   safe dynamic module loading and path management for testing agent scripts.

   ## Location
   - Path: `scripts/agent/agent_test_utils.py`

   ## Public surface
   - Classes: (none)
   - Functions:
     - `agent_dir_on_path()` - Context manager that temporarily adds agent directory to sys.path
     - `load_agent_module(filename, module_name=None)` - Dynamically loads agent modules by
   filename

   ## Behavior summary
   - Provides context manager `agent_dir_on_path()` to temporarily modify `sys.path` for importing
   sibling agent modules
   - Loads agent modules dynamically using `importlib.util`, supporting filenames with
   non-Python-identifier characters (e.g., `agent-changes.py`)
   - Auto-generates safe module names by sanitizing filenames, ensuring valid Python identifiers
   - Handles cleanup of sys.modules on import failure to prevent polluted module state

   ## Key dependencies
   - Top imports: `__future__`, `importlib.util`, `re`, `sys`, `contextlib`, `pathlib`, `types`

   ## File fingerprint
   - SHA256(source): `d4c3fc4817d2ced6…`
   ```

   **Key improvements:**
   1. Added comprehensive module purpose explaining it's for testing and loading agent modules
   2. Expanded function descriptions with clear purposes
   3. Enhanced behavior summary with 4 specific capabilities including error handling and module
   name sanitization
   4. Maintained all existing metadata structure
