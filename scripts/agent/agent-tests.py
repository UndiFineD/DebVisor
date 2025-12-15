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

    def _validate_syntax(self, content: str) -> bool:
        """Validate Python syntax using ast."""
        try:
            ast.parse(content)
            return True
        except SyntaxError as e:
            logging.error(f"Syntax error in generated tests: {e}")
            return False

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the test suites.

        When Copilot CLI is unavailable, BaseAgent keeps the existing content
        unchanged (avoids injecting duplicated placeholder markdown blocks).
        """
        new_content = super().improve_content(prompt)

        # Validate syntax
        if not self._validate_syntax(new_content):
            logging.error("Generated tests failed syntax validation. Reverting.")
            self.current_content = self.previous_content
            return self.previous_content

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
