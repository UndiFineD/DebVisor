● I'll analyze the current improvements file and suggest enhanced improvements for agent-tests.py.

● Now let me create an improved version of the improvements file with more actionable, specific,
   and well-structured recommendations:

● Let me create a new improved version since I cannot edit:

● I see that both write and shell tools are disabled. Let me provide the improved suggestions as
   structured output instead:

   Based on my analysis of `agent-tests.py`, the existing test infrastructure at `tests/`,
   `conftest.py`, and `pytest.ini`, here are **significantly improved and actionable** suggestions:

   ---

   # **Enhanced Improvements for `agent-tests.py`**

   ## **Executive Summary**

   The TestsAgent currently provides basic test generation with AST syntax validation. These
   improvements transform it into an intelligent, context-aware testing assistant that generates
   high-quality, maintainable tests aligned with project conventions.

   ---

   ## **High Priority Improvements**

   ### **1. Source Code Context Integration**
   **Priority: Critical | Impact: High | Effort: Medium**

   **Current Gap**: Agent only sees test file content, lacking context about the source code being
   tested.

   **Proposed Solution**: Auto-discover and inject source file content into AI prompts.

   **Implementation**:
   ```python
   def _find_source_file(self) -> Optional[Path]:
       """Locate source file for test file (test_foo.py -> foo.py)"""
       # Strip test_ prefix and _test suffix
       # Search in ../opt, ../scripts/agent, etc.
       # Return first match or None

   def _build_context_prompt(self, user_prompt: str) -> str:
       """Enhance prompt with source code context"""
       source_path = self._find_source_file()
       if source_path and source_path.exists():
           source = source_path.read_text(encoding='utf-8')
           return f"{user_prompt}\n\n# Source being tested:\n{source}"
       return user_prompt
   ```

   **Benefits**:
   - AI generates tests aligned with actual implementation
   - Covers edge cases and all public APIs
   - Eliminates hallucinated test methods
   - Tests stay synchronized with code changes

   ---

   ### **2. Advanced Validation Pipeline**
   **Priority: Critical | Impact: High | Effort: Medium**

   **Current**: Only AST syntax validation exists.

   **Proposed Enhancements**:

   ```python
   def _validate_test_structure(self, content: str) -> tuple[bool, list[str]]:
       """Validate pytest/unittest-specific patterns"""
       issues = []
       tree = ast.parse(content)

       # Check 1: All test functions follow naming convention
       for node in ast.walk(tree):
           if isinstance(node, ast.FunctionDef):
               if not node.name.startswith('test_') and 'test' in node.name.lower():
                   issues.append(f"Function '{node.name}' doesn't follow test_* convention")

       # Check 2: Tests contain assertions
       for func in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and
   n.name.startswith('test_')]:
           has_assert = any(isinstance(n, ast.Assert) for n in ast.walk(func))
           has_pytest_raises = 'pytest.raises' in ast.unparse(func)
           if not (has_assert or has_pytest_raises):
               issues.append(f"Test '{func.name}' lacks assertions")

       # Check 3: Detect unused imports
       # Check 4: Validate fixture usage against conftest.py

       return len(issues) == 0, issues
   ```

   **Benefits**:
   - Catches semantic issues beyond syntax errors
   - Prevents generation of empty/meaningless tests
   - Ensures pytest conventions compliance

   ---

   ### **3. Test Framework Intelligence**
   **Priority: High | Impact: Medium | Effort: Low**

   **Current**: Hard-coded pytest assumptions in `_get_default_content()`.

   **Proposed Solution**: Auto-detect framework and adapt behavior.

   ```python
   def _detect_test_framework(self) -> str:
       """Detect testing framework from imports or config"""
       if self.file_path.exists():
           content = self.file_path.read_text(encoding='utf-8')
           if 'import unittest' in content or 'from unittest' in content:
               return 'unittest'
           if 'import pytest' in content:
               return 'pytest'

       # Check pytest.ini exists in repo
       pytest_ini = self.file_path.parent.parent / 'pytest.ini'
       if pytest_ini.exists():
           return 'pytest'

       return 'pytest'  # default

   def _get_default_content(self) -> str:
       """Return framework-specific default content"""
       framework = self._detect_test_framework()
       if framework == 'unittest':
           return "import unittest\n\nclass TestCase(unittest.TestCase):\n    pass\n"
       return "# Tests\n\nimport pytest\n\n# Add tests here\n"
   ```

   **Benefits**:
   - Supports multiple testing frameworks
   - Generates framework-appropriate code
   - Respects project conventions

   ---

   ## **Medium Priority Improvements**

   ### **4. Test Quality Guardrails**
   **Priority: High | Impact: High | Effort: Low**

   **Problem**: AI may generate brittle or low-quality tests.

   **Solution**: Enhanced prompt engineering with quality guidelines.

   ```python
   def _get_quality_guidelines(self) -> str:
       """Return test quality guidelines for AI"""
       return """
   Generate high-quality tests following these principles:
   - Test behavior, not implementation details
   - Use descriptive test names (test_function_name_condition_expected_result)
   - Avoid magic numbers; use named constants
   - Mock external dependencies (APIs, databases, file system)
   - Use parametrized tests for multiple scenarios (@pytest.mark.parametrize)
   - Include docstrings for complex test logic
   - Test happy path, edge cases, and error conditions
   - Follow project's pytest.ini configuration
   """

   def improve_content(self, prompt: str) -> str:
       """Enhanced with quality guidelines"""
       enhanced_prompt = f"{prompt}\n\n{self._get_quality_guidelines()}"
       return super().improve_content(enhanced_prompt)
   ```

   ---

   ### **5. Fixture-Aware Generation**
   **Priority: Medium | Impact: High | Effort: Medium**

   **Feature**: Parse `conftest.py` and suggest available fixtures.

   ```python
   def _discover_fixtures(self) -> dict[str, str]:
       """Scan conftest.py for available fixtures"""
       conftest = Path('tests/conftest.py')
       if not conftest.exists():
           return {}

       fixtures = {}
       tree = ast.parse(conftest.read_text(encoding='utf-8'))
       for node in ast.walk(tree):
           if isinstance(node, ast.FunctionDef):
               for decorator in node.decorator_list:
                   if 'fixture' in ast.unparse(decorator):
                       # Extract docstring as description
                       doc = ast.get_docstring(node) or "No description"
                       fixtures[node.name] = doc
       return fixtures

   def _enhance_prompt_with_fixtures(self, prompt: str) -> str:
       """Add available fixtures to prompt"""
       fixtures = self._discover_fixtures()
       if fixtures:
           fixture_list = '\n'.join([f"- {name}: {desc}" for name, desc in fixtures.items()])
           return f"{prompt}\n\nAvailable pytest fixtures:\n{fixture_list}"
       return prompt
   ```

   **Benefits**:
   - Promotes fixture reuse
   - Reduces test setup duplication
   - Leverages existing test infrastructure

   ---

   ### **6. Input Validation & Error Handling**
   **Priority: Medium | Impact: Low | Effort: Low**

   **Current**: No validation of input filename.

   **Proposed**:

   ```python
   def __init__(self, file_path: str):
       """Enhanced with input validation"""
       path = Path(file_path)

       # Validate test file naming convention
       if not (path.name.startswith('test_') or path.name.endswith('_test.py')):
           logging.warning(f"File '{path.name}' doesn't follow test naming convention (test_*.py or
    *_test.py)")

       # Warn if outside tests directory
       if 'tests' not in str(path.parent):
           logging.warning(f"File '{path}' is not in a 'tests' directory")

       super().__init__(file_path)
   ```

   ---

   ## **Low Priority Enhancements**

   ### **7. Coverage-Guided Test Generation**
   **Priority: Low | Impact: High | Effort: High**

   **Feature**: Integrate with `.coverage` to generate tests for uncovered code.

   ```python
   def _read_coverage_data(self, source_file: Path) -> set[int]:
       """Read uncovered line numbers from .coverage"""
       # Parse .coverage SQLite database
       # Return set of uncovered line numbers
       pass

   def _generate_coverage_aware_prompt(self, prompt: str) -> str:
       """Enhance prompt with coverage gaps"""
       source = self._find_source_file()
       if source:
           uncovered = self._read_coverage_data(source)
           if uncovered:
               return f"{prompt}\n\nFocus on covering lines: {sorted(uncovered)}"
       return prompt
   ```

   **Note**: Requires `coverage.py` integration.

   ---

   ### **8. Comprehensive Documentation**
   **Priority: Low | Impact: Low | Effort: Low**

   - Add detailed docstrings to all methods
   - Document class responsibilities and invariants
   - Include usage examples in module docstring
   - Document AI prompt engineering strategies

   ---

   ### **9. Test Template System**
   **Priority: Low | Impact: Medium | Effort: Medium**

   Support loading project-specific templates from `.debvisor/test-templates/`:

   ```python
   def _load_template(self, template_name: str) -> Optional[str]:
       """Load test template from project directory"""
       template_dir = Path('.debvisor/test-templates')
       template_path = template_dir / f"{template_name}.py"
       if template_path.exists():
           return template_path.read_text(encoding='utf-8')
       return None
   ```

   ---

   ## **Implementation Roadmap**

   ### **Phase 1 (Sprint 1): Foundation**
   1. Source code context integration (#1)
   2. Advanced validation pipeline (#2)
   3. Test quality guardrails (#4)

   **Deliverables**: Context-aware test generation with quality checks

   ---

   ### **Phase 2 (Sprint 2): Framework Support**
   1. Framework detection (#3)
   2. Fixture-aware generation (#5)
   3. Input validation (#6)

   **Deliverables**: Multi-framework support with fixture intelligence

   ---

   ### **Phase 3 (Sprint 3): Advanced Features**
   1. Coverage-guided mode (#7)
   2. Template system (#9)
   3. Comprehensive docs (#8)

   **Deliverables**: Production-ready test generation system

   ---

   ## **Testing Strategy for Improvements**

   Each improvement should include:

   1. **Unit Tests**: Test validation/detection logic in isolation
   2. **Integration Tests**: Test with real test files from `tests/`
   3. **Regression Tests**: Ensure existing functionality still works
   4. **Quality Review**: Manual inspection of AI-generated test quality

   **Example Test Structure**:
   ```python
   # tests/test_agent_tests_agent.py
   def test_find_source_file_with_test_prefix(tmp_path):
       # Create test_foo.py and foo.py
       # Assert _find_source_file() returns foo.py

   def test_validate_test_structure_detects_missing_assertions():
       # Parse code without assertions
       # Assert validation fails with helpful message

   def test_detect_framework_from_imports():
       # Create file with unittest imports
       # Assert framework detection returns 'unittest'
   ```

   ---

   ## **Key Insights from Codebase Analysis**

   1. **Project uses pytest extensively**: See `pytest.ini` with 32 custom markers
   2. **Consistent test structure**: All tests follow `test_*.py` convention in `tests/`
   3. **Rich conftest.py**: Has 50+ fixtures including logging, async utilities, mocks
   4. **BaseAgent is extensible**: Provides hooks for validation, content improvement
   5. **AST validation exists**: Good foundation, but insufficient for semantic checks

   ---

   ## **Metrics for Success**

   Track these KPIs after implementing improvements:

   - **Test Coverage Increase**: % increase in line/branch coverage
   - **AI Test Quality Score**: Manual review rating (1-5) of generated tests
   - **False Positive Rate**: % of generated tests requiring fixes
   - **Developer Satisfaction**: Survey responses on test quality
   - **Time Savings**: Hours saved vs manual test writing

   ---

   ## **Appendix: Real-World Usage Scenarios**

   ### **Scenario 1: New Feature Development**
   ```bash
   # Developer writes new feature
   python scripts/agent/agent-tests.py tests/test_new_feature.py

   # Agent:
   # 1. Finds opt/new_feature.py
   # 2. Reads source code
   # 3. Generates comprehensive tests covering all methods
   # 4. Validates test structure
   # 5. Writes tests/test_new_feature.py
   ```

   ### **Scenario 2: Coverage Gap Remediation**
   ```bash
   # After running coverage report
   pytest --cov=opt --cov-report=term-missing
   # Identifies gaps in opt/api.py lines 45-67

   python scripts/agent/agent-tests.py tests/test_api.py --coverage-guided
   # Agent focuses on generating tests for lines 45-67
   ```

   ### **Scenario 3: Framework Migration**
   ```bash
   # Project migrates from unittest to pytest
   python scripts/agent/agent-tests.py tests/test_legacy.py

   # Agent:
   # 1. Detects unittest imports
   # 2. Suggests pytest migration
   # 3. Converts assertions (self.assertEqual -> assert ==)
   # 4. Adds pytest fixtures
   ```

   ---

   ## **Conclusion**

   These improvements transform `agent-tests.py` from a basic test generator into an intelligent
   testing assistant that:
   - Understands context (source code, fixtures, coverage)
   - Generates high-quality, maintainable tests
   - Adapts to project conventions
   - Provides actionable validation feedback

   **Estimated Total Effort**: 4-6 weeks (1 developer)
   **Expected Impact**: 40-60% reduction in test writing time, 25-35% increase in test coverage
