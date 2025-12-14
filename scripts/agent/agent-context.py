# AI Code Improvement Suggestions
## Description: Improve the code for agent-context.py
#
## Suggestions:
## 1. Add comprehensive docstrings to all functions
## 2. Implement proper error handling with try/except blocks
## 3. Add type hints for better code clarity
## 4. Break down complex functions into smaller, focused functions
## 5. Add input validation and sanitization
## 6. Implement logging for debugging and monitoring
## 7. Add unit tests for all functions
## 8. Follow PEP 8 style guidelines
## 9. Add configuration management for customizable behavior
## 10. Implement proper resource cleanup with context managers
#
## Note: Full AI code rewriting requires additional AI service integration.
## The new GitHub Copilot CLI focuses on command-line suggestions, not code generation.
#
## Original code preserved below:
#
## !/usr/bin/env python3
## Copyright (c) 2025 DebVisor contributors
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##     http://www.apache.org/licenses/LICENSE-2.0
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
"""
Context Agent: Improves and updates code file descriptions.

Reads a context file (Codefile.description.md), uses Copilot to enhance the description,
and updates the context file with improvements.

## Description
This module provides a Context Agent that reads existing code file descriptions,
uses AI assistance to improve and complete them, and updates the context files
with enhanced documentation.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add validation for context file format
- Improve prompt engineering for better descriptions

## Improvements
- Better integration with other agents
- Enhanced diff reporting
"""

from base_agent import BaseAgent, create_main_function

class ContextAgent(BaseAgent):
    """Updates code file context descriptions using AI assistance."""

    def _get_default_content(self) -> str:
        """Return default content for new context files."""
        return "# Description\n\nNo description available.\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original content preserved below:\n\n")

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the context with specific documentation suggestions."""
        description = f"Improve the description for {self.file_path.stem.replace('.description', '')}"

        # For documentation improvement, provide specific content suggestions
        if any(keyword in prompt.lower()
                for keyword in ["improve", "description", "documentation"]):
            fallback_suggestions = (
                f"# AI Content Improvement Suggestions\n"
                f"# Description: {description}\n"
                f"#\n"
                f"# Suggestions for improving documentation/context:\n"
                f"# 1. Add clear, concise descriptions for all functions and classes\n"
                f"# 2. Include usage examples and code snippets\n"
                f"# 3. Document all parameters with types and descriptions\n"
                f"# 4. Add information about return values and exceptions\n"
                f"# 5. Include cross-references to related functions/modules\n"
                f"# 6. Add version information and compatibility notes\n"
                f"# 7. Include performance considerations and limitations\n"
                f"# 8. Add troubleshooting and common issues sections\n"
                f"# 9. Include links to external resources and documentation\n"
                f"# 10. Use consistent formatting and terminology throughout\n"
                f"#\n"
                f"# Note: Full AI content rewriting requires additional AI service integration.\n"
                f"# The new GitHub Copilot CLI focuses on command-line suggestions, "
                f"not content generation.\n"
                f"#\n"
                f"# Original content preserved below:\n"
                f"#\n"
                f"{self.previous_content}"
            )
            self.current_content = fallback_suggestions
            return self.current_content

        # For other prompts, use the base implementation
        return super().improve_content(prompt)

## Create main function using the helper
main = create_main_function(
    ContextAgent,
    'Context Agent: Updates code file descriptions',
    'Path to the context file (e.g., file.description.md)'
)

if __name__ == '__main__':
    main()
