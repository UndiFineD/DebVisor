#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Tests Agent: Improves and updates code file test suites.

Reads a tests file (test_Codefile.py), uses Copilot to enhance the tests,
and updates the tests file with improvements.

# Description
This module provides a Tests Agent that reads existing code file test suites,
uses AI assistance to improve and complete them, ensuring each line of the codefile is tested,
and updates the tests files with enhanced test coverage.

# Changelog
- 1.0.0: Initial implementation

# Suggested Fixes
- Add validation for tests file format
- Improve prompt engineering for better test generation

# Improvements
- Better integration with other agents
- Enhanced diff reporting
"""

import ast
import logging
from pathlib import Path
from typing import Optional
from base_agent import BaseAgent, create_main_function


class TestsAgent(BaseAgent):
    """Updates code file test suites using AI assistance."""

    def _get_default_content(self) -> str:
        """Return default content for new test files."""
        return "# Tests\n\nimport pytest\n\n# Add tests here\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n# GitHub CLI not found. Install from "
                "https://cli.github.com/\n\n# Original test code preserved below:\n\n")

    def _find_source_file(self) -> Optional[Path]:
        """Locate source file for test file (test_foo.py -> foo.py)."""
        if not self.file_path.name.startswith('test_'):
            return None
        
        source_name = self.file_path.name[5:]  # Remove test_ prefix
        # Try to find source file in common locations
        # 1. Same directory
        source_path = self.file_path.parent / source_name
        if source_path.exists():
            return source_path
            
        # 2. Parent directory (if tests are in tests/)
        if self.file_path.parent.name == 'tests':
            source_path = self.file_path.parent.parent / source_name
            if source_path.exists():
                return source_path
                
        # 3. scripts/agent directory (specific to this project structure)
        agent_dir = self.file_path.parent.parent / 'scripts' / 'agent'
        source_path = agent_dir / source_name
        if source_path.exists():
            return source_path
            
        return None

    def _validate_syntax(self, content: str) -> bool:
        """Validate Python syntax using ast."""
        try:
            ast.parse(content)
            return True
        except SyntaxError as e:
            logging.error(f"Syntax error in generated tests: {e}")
            return False

    def _validate_test_structure(self, content: str) -> bool:
        """Validate pytest/unittest-specific patterns."""
        try:
            tree = ast.parse(content)
            issues = []
            
            # Check 1: All test functions follow naming convention
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.startswith('test_') and 'test' in node.name.lower():
                        # Just a warning, might be a helper
                        pass

            # Check 2: Tests contain assertions
            test_funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')]
            for func in test_funcs:
                has_assert = any(isinstance(n, ast.Assert) for n in ast.walk(func))
                # Simple check for pytest.raises context manager
                has_raises = False
                for node in ast.walk(func):
                    if isinstance(node, ast.With):
                        for item in node.items:
                            if isinstance(item.context_expr, ast.Call):
                                if isinstance(item.context_expr.func, ast.Attribute):
                                    if item.context_expr.func.attr == 'raises':
                                        has_raises = True
                
                if not (has_assert or has_raises):
                    issues.append(f"Test '{func.name}' lacks assertions")
            
            if issues:
                logging.warning(f"Test structure issues: {', '.join(issues)}")
                # We don't fail validation for this yet, just warn
            
            return True
        except Exception as e:
            logging.warning(f"Failed to validate test structure: {e}")
            return True

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the test suites.

        When Copilot CLI is unavailable, BaseAgent keeps the existing content
        unchanged (avoids injecting duplicated placeholder markdown blocks).
        """
        # Enhance prompt with source code context if available
        source_path = self._find_source_file()
        enhanced_prompt = prompt
        if source_path and source_path.exists():
            try:
                source_content = source_path.read_text(encoding='utf-8')
                enhanced_prompt = (
                    f"{prompt}\n\n"
                    f"# Source Code being tested ({source_path.name}):\n"
                    f"```python\n{source_content}\n```\n\n"
                    "Ensure tests cover the public API and edge cases of the source code."
                )
            except Exception as e:
                logging.warning(f"Failed to read source file context: {e}")

        new_content = super().improve_content(enhanced_prompt)

        # Validate syntax
        if not self._validate_syntax(new_content):
            logging.error("Generated tests failed syntax validation. Reverting.")
            self.current_content = self.previous_content
            return self.previous_content
            
        # Validate structure
        self._validate_test_structure(new_content)

        return new_content

    def update_file(self):
        """Write the improved content back to the file (no markdown fixing for test files)."""
        self.file_path.write_text(self.current_content, encoding='utf-8')


# Create main function using the helper

main = create_main_function(
    TestsAgent,
    'Tests Agent: Updates code file test suites',
    'Path to the tests file (e.g., test_file.py)'
)

if __name__ == '__main__':
    main()
