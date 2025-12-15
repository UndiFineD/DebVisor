● I'll analyze the test file and improve the improvements document with more comprehensive and
   actionable suggestions.

● Now I'll enhance the improvements document with more comprehensive suggestions:

● Let me check if the file is read-only or if there's another issue:

● I see - I don't have permission to modify files. Let me provide you with the improved content
   instead:

   ---

   # Improved Improvements for `test_agent-stats.py`

   Here's a comprehensive enhancement to the improvements document:

   ```markdown
   # Improvements: `test_agent-stats.py`

   ## Critical Issues
   - **Non-discoverable test name**: The hyphen in `test_agent-stats.py` prevents pytest
   auto-discovery. Must be explicitly invoked or renamed to `test_agent_stats.py`.
   - **Missing test for output format**: No test validates that `report_stats()` produces stable
   output for both text and JSON formats.

   ## Suggested Improvements

   ### Test Coverage Enhancements
   1. **Add JSON output format test**: Test `report_stats(output_format='json')` to ensure JSON
   structure is stable and parseable.
   2. **Test edge cases**:
      - Empty file list (`StatsAgent([])`)
      - Nonexistent file paths
      - Files without any companion files
      - Files with only some companion files
   3. **Test companion file detection logic**: Verify handling of files with different extensions
   (not just `.py`).
   4. **Add percentage calculation tests**: If stats should include completion percentages, test
   those calculations.

   ### Code Quality
   5. **Output validation**: Capture stdout in tests using `capsys` fixture and validate exact
   output format for regression testing.
   6. **Parametrize test cases**: Use `@pytest.mark.parametrize` to test multiple scenarios with
   different companion file combinations.
   7. **Add docstrings**: Document what `test_stats_agent_counts_files` validates.

   ### Integration Testing
   8. **Test CLI integration**: Add test for `main()` function with argparse.
   9. **Test file discovery patterns**: Validate that companion file naming convention is correctly
    detected (e.g., `base.description.md`, `test_base.py`).

   ## Implementation Priority
   1. **High**: Add JSON format test (prevents breaking changes to API consumers)
   2. **High**: Add edge case tests (improves reliability)
   3. **Medium**: Add parametrized test cases (reduces code duplication)
   4. **Low**: Rename file to make pytest-discoverable (if consistent with project conventions)

   ## Example Test Structure
   ```python
   def test_stats_agent_json_output(tmp_path: Path, capsys):
       """Validate JSON output format stability."""
       # ... setup files ...
       agent.report_stats(output_format='json')
       captured = capsys.readouterr()
       data = json.loads(captured.out)
       assert "total_files" in data
       assert isinstance(data["total_files"], int)

   @pytest.mark.parametrize("companions,expected", [
       ([], {"files_with_context": 0, "files_with_tests": 0}),
       (["description.md"], {"files_with_context": 1, "files_with_tests": 0}),
       (["description.md", "test_a.py"], {"files_with_context": 1, "files_with_tests": 1}),
   ])
   def test_stats_companion_combinations(tmp_path: Path, companions, expected):
       """Test various companion file combinations."""
       # ... implementation ...
   ```

   ## Notes
   - Current test only validates the "happy path" with one file having all companions.
   - No tests exist for the `report_stats()` output method or error handling.
   - Consider whether tests should validate actual printed output or just the calculated stats
   dictionary.
   - File: `scripts/agent/test_agent-stats.py`
   ```

   ## Key Improvements Made:

   1. **Structured organization** with clear sections (Critical Issues, Test Coverage, Code
   Quality, Integration)
   2. **Specific actionable suggestions** with concrete examples
   3. **Priority levels** to guide implementation order
   4. **Example code snippets** showing how to implement parametrized tests and output validation
   5. **Expanded coverage areas** including edge cases, JSON format testing, and CLI integration
   6. **More detailed edge case scenarios** that the current test doesn't cover

   The improvements are now much more comprehensive and actionable compared to the original generic
    suggestions.
