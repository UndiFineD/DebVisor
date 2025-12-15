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
Coder Agent: Improves and updates code files.

Reads a code file, uses Copilot to enhance the code,
and updates the code file with improvements.

## Description
This module provides a Coder Agent that reads existing code files,
uses AI assistance to improve and complete them, and updates the code files
with enhanced implementations.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add validation for code file format
- Improve prompt engineering for better code improvements

## Improvements
- Better integration with other agents
- Enhanced diff reporting
"""

import ast
import logging
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional
from base_agent import BaseAgent, create_main_function


class CoderAgent(BaseAgent):
    """Updates code files using AI assistance."""

    def _get_default_content(self) -> str:
        """Return default content for new code files."""
        return "# Code file\n\n# Add code here\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original code preserved below:\n\n")

    def _validate_syntax(self, content: str) -> bool:
        """Validate Python syntax using ast."""
        if self.file_path.suffix != '.py':
            return True
        try:
            ast.parse(content)
            return True
        except SyntaxError as e:
            logging.error(f"Syntax error in generated code: {e}")
            return False

    def _validate_flake8(self, content: str) -> bool:
        """Validate Python code using flake8 if available."""
        if self.file_path.suffix != '.py':
            return True
        if not shutil.which('flake8'):
            logging.warning("flake8 not found, skipping style validation")
            return True
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            # Run flake8 on the temporary file
            # We ignore some common errors that might be acceptable in generated code
            # E501: Line too long
            # W293: Blank line contains whitespace
            result = subprocess.run(
                ['flake8', '--ignore=E501,W293', tmp_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                logging.warning(f"flake8 validation failed:\n{result.stdout}")
                return False  # Soft validation failure
            return True
        finally:
            try:
                Path(tmp_path).unlink()
            except OSError:
                pass

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the code with specific coding suggestions."""
        description = f"Improve the code for {self.file_path.name}"
        # For code improvement, provide specific coding suggestions
        if "improve" in prompt.lower() or "code" in prompt.lower():
            fallback_suggestions = f"""# AI Code Improvement Suggestions
# Description: {description}
#
# Suggestions:
# 1. Add comprehensive docstrings to all functions
# 2. Implement proper error handling with try/except blocks
# 3. Add type hints for better code clarity
# 4. Break down complex functions into smaller, focused functions
# 5. Add input validation and sanitization
# 6. Implement logging for debugging and monitoring
# 7. Add unit tests for all functions
# 8. Follow PEP 8 style guidelines
# 9. Add configuration management for customizable behavior
# 10. Implement proper resource cleanup with context managers
#
# Note: Full AI code rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not code generation.
#
# Original code preserved below:
#
{self.previous_content}"""
            self.current_content = fallback_suggestions
            return self.current_content
        # Call base implementation
        new_content = super().improve_content(prompt)
        # Validate syntax
        if not self._validate_syntax(new_content):
            logging.error("Generated code failed syntax validation. Reverting.")
            self.current_content = self.previous_content
            return self.previous_content
        # Validate style (flake8)
        if not self._validate_flake8(new_content):
            logging.warning("Generated code failed style validation (flake8). Proceeding anyway.")
        return new_content


# Create main function using the helper
main = create_main_function(
    CoderAgent,
    'Coder Agent: Updates code files',
    'Path to the code file'
)


if __name__ == '__main__':
    main()
