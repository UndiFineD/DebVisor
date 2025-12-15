● I'll examine the current code and update the description to accurately reflect its
   functionality.

● Now let me view the current description file:

● I can see the description file is malformed with bullet points and conversational text. Let me
   regenerate it by running the script:

● Let me create the correct description content based on the actual code analysis and edit the
   file directly:

● I don't have write permissions to update the file. However, I can provide you with the accurate
   description content that should replace the current file:

   ---

   **Updated Description for `generate_agent_reports.py`:**

   ```markdown
   # Description: `generate_agent_reports.py`

   ## Module purpose
   Generate per-file agent reports.

   For every Python file under `scripts/agent/*.py`, this script writes:
   - `<stem>.description.md`
   - `<stem>.errors.md`
   - `<stem>.improvements.md`

   The output is intentionally lightweight and based on static inspection and
   basic syntax/compile checks.

   ## Location
   - Path: `scripts/agent/generate_agent_reports.py`

   ## Public surface
   - Classes: CompileResult
   - Functions: render_description, render_errors, render_improvements, iter_agent_py_files, main

   ## Behavior summary
   - Has a CLI entrypoint (`__main__`).

   ## Key dependencies
   - Top imports: `ast`, `hashlib`, `re`, `sys`, `dataclasses`, `pathlib`, `typing`, `Iterable`,
   `List`, `Optional`, `Sequence`, `Tuple`

   ## File fingerprint
   - SHA256(source): `1e8d89653fc1dd52…`
   ```

   **Key corrections made:**
   - ❌ Removed "Uses `argparse` for CLI parsing" (not present in code)
   - ❌ Removed "Invokes external commands via `subprocess`" (not present in code)
   - ❌ Removed "Mutates `sys.path` to import sibling modules" (not present in code)
   - ✅ Correctly identifies it has a CLI entrypoint only

   The script is a pure static analysis tool using only standard library modules.
