● I'll examine the current code and update the description accordingly.

● The description file appears to contain a conversation rather than the actual description
   content. I'll replace it with a proper structured description based on the current code:

● I don't have write permissions. Here's the updated description content that accurately reflects
   the current code:

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
   - Auto-generates safe module names by sanitizing filenames with regex, ensuring valid Python
   identifiers (prefixes with `m_` if starts with digit)
   - Handles cleanup of sys.modules on import failure to prevent polluted module state
   - Raises `FileNotFoundError` if specified agent file doesn't exist
   - Raises `RuntimeError` if module spec cannot be created

   ## Key dependencies
   - Top imports: `__future__`, `importlib.util`, `re`, `sys`, `contextlib`, `pathlib`, `types`
   - Constants: `AGENT_DIR` - Resolved path to scripts/agent directory

   ## Implementation details
   - Module name sanitization: replaces non-alphanumeric/underscore chars with underscore, prefixes
    `_dv_legacy_`
   - Path handling: uses `Path(__file__).resolve().parent` for reliable directory location
   - Error handling: cleans up `sys.modules` entry if module execution fails
   ```

   **Key improvements from the existing content:**
   1. Added explicit error handling behavior (FileNotFoundError, RuntimeError)
   2. Detailed the module name sanitization algorithm specifics
   3. Added "Implementation details" section for clarity
   4. Included the AGENT_DIR constant in dependencies
   5. More precise description of the sanitization process
