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

        # For other prompts, use the base implementation
        return super().improve_content(prompt)


# Create main function using the helper
main = create_main_function(
    CoderAgent,
    'Coder Agent: Updates code files',
    'Path to the code file'
)


if __name__ == '__main__':
    main()
