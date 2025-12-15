● I'll examine the current code in `agent-tests.py` to update its description with accurate
   information.

● Now I'll check the base_agent.py to understand the `create_main_function` and `improve_content`
   implementations:

● Now let me check what the actual prompt is in the main execution flow:

● Now let me check how the agent is called in the main function to understand the full workflow:

● Now let me look at how TestsAgent is actually used and what prompts are typically sent to it:

● Now let me check the current description file to understand what needs to be updated:

● Now I have a complete picture. Let me update the description based on the current code. The
   description needs to reflect:

   1. TestsAgent has syntax validation using `ast.parse()`
   2. It overrides `improve_content()` to add validation
   3. It overrides `update_file()` to skip markdown fixing (writes raw Python)
   4. It provides default content for new test files with pytest import
   5. The main function is created using `create_main_function` helper
   6. It accepts `--context` (path to test file) and `--prompt` (improvement instructions) as CLI
   args
   7. It also supports `--backend`, `--describe-backends`, and `-v/--verbose` flags

● I need to read the file first, then make the edit:

● Let me check what's happening - it seems I need to read the current content properly first:

● It seems permissions are restricted. Let me try a different approach using the edit tool
   properly by ensuring the old_str exactly matches:

● It appears I don't have write permissions for this file. Let me check what files I can access
   and understand the permission restrictions:

   I apologize, but I don't have write permissions to modify the `agent-tests.description.md` file.
    Based on my analysis of the current code in `agent-tests.py`, here are the key updates that
   should be made to the description:

   ## Recommended Updates to `agent-tests.description.md`:

   **Current code analysis reveals:**

   1. **Syntax Validation**: The `TestsAgent` class implements `_validate_syntax()` using
   `ast.parse()` to validate Python syntax before accepting AI-generated changes

   2. **Error Recovery**: The `improve_content()` method reverts to previous content if syntax
   validation fails

   3. **Raw Python Output**: The `update_file()` method writes raw Python content without markdown
   post-processing

   4. **Default Content**: Provides pytest skeleton for new test files with `import pytest`

   5. **CLI Arguments**: Uses `create_main_function` which provides:
      - `--context` (required): Path to test file
      - `--prompt` (required): Improvement instructions
      - `--backend` (optional): AI backend selection
      - `--describe-backends`: Show available backends
      - `-v/--verbose`: Verbosity control

   6. **Integration**: Called by `agent.py` with prompts like `"Update and expand the test suite
   for {code_file.name}"`

   The description should be updated to reflect these implementation details, particularly the
   syntax validation feature and the complete CLI interface.
