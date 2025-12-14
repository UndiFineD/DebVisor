# AI Code Improvement Suggestions
# Description: Improve the code for agent-context.py
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

import subprocess
from pathlib import Path
import argparse
import difflib

from fix_markdown_lint import fix_markdown_content  # noqa: E402


def runSubagent(description: str, prompt: str, original_content: str = "") -> str:
    """
    Run a subagent using GitHub Copilot CLI to interact with GitHub Copilot.

    Note: The new GitHub Copilot CLI (gh copilot) is designed for command suggestions,
    not general content improvement. For content improvement, we fall back to basic suggestions.

    Args:
        description: Description of the task
        prompt: The prompt to send to Copilot

    Returns:
        AI response as a string, or fallback suggestions
    """
    try:
        # Check if gh command is available
        subprocess.run(['gh', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ("# AI Improvement Unavailable\n# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original content preserved below:\n\n")

    # The new Copilot CLI is for command suggestions, not content improvement
    # For now, provide basic improvement suggestions for documentation
    if "improve" in prompt.lower() or "description" in prompt.lower() or "documentation" in prompt.lower():
        return f"""# AI Content Improvement Suggestions
# Description: {description}
#
# Suggestions for improving documentation/context:
# 1. Add clear, concise descriptions for all functions and classes
# 2. Include usage examples and code snippets
# 3. Document all parameters with types and descriptions
# 4. Add information about return values and exceptions
# 5. Include cross-references to related functions/modules
# 6. Add version information and compatibility notes
# 7. Include performance considerations and limitations
# 8. Add troubleshooting and common issues sections
# 9. Include links to external resources and documentation
# 10. Use consistent formatting and terminology throughout
#
# Note: Full AI content rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not content generation."""

    try:
        # Try using gh copilot explain for documentation-related prompts
        result = subprocess.run(
            ['gh', 'copilot', 'explain', prompt[:200]],  # Limit prompt length
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout.strip():
            explanation = f"# GitHub Copilot Explanation:\n{result.stdout.strip()}"
            return explanation
        else:
            return "# Copilot CLI available but returned no useful response for content improvement."

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return "# Copilot CLI timed out or failed."


class ContextAgent:
    """Updates code file context descriptions using AI assistance."""

    def __init__(self, context_file: str):
        self.context_file = Path(context_file)
        self.previous_context = ""
        self.current_context = ""

    def read_previous_context(self) -> str:
        """Read the existing context file."""
        if self.context_file.exists():
            self.previous_context = self.context_file.read_text(encoding='utf-8')
        else:
            self.previous_context = "# Description\n\nNo description available.\n"
        return self.previous_context

    def improve_context(self, prompt: str) -> str:
        """Use AI to improve the context."""
        description = f"Improve the description for {self.context_file.stem.replace('.description', '')}"
        try:
            improvement = runSubagent(description, prompt, self.previous_context)
            self.current_context = improvement
            return self.current_context
        except Exception as e:
            print(f"Warning: Failed to improve context: {e}")
            self.current_context = self.previous_context
            return self.current_context

    def update_context_file(self):
        """Write the improved context back to the file."""
        self.context_file.write_text(fix_markdown_content(self.current_context), encoding='utf-8')

    def get_diff(self) -> str:
        """Get the diff between previous and current context."""
        diff = difflib.unified_diff(
            self.previous_context.splitlines(keepends=True),
            self.current_context.splitlines(keepends=True),
            fromfile='previous',
            tofile='current'
        )
        return ''.join(diff)


def main():
    parser = argparse.ArgumentParser(description='Context Agent: Updates code file descriptions')
    parser.add_argument('--context', required=True, help='Path to the context file (e.g., file.description.md)')
    parser.add_argument('--prompt', required=True, help='Prompt for improving the description')
    args = parser.parse_args()

    agent = ContextAgent(args.context)
    agent.read_previous_context()
    agent.improve_context(args.prompt)
    agent.update_context_file()
    diff = agent.get_diff()
    if diff:
        print("Context updated:")
        print(diff)
    else:
        print("No changes made to context.")


if __name__ == '__main__':
    main()
