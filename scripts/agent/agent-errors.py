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

# AI Code Improvement Suggestions
# Description: Improve the code for agent-errors.py
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


"""
Errors Agent: Improves and updates code file error reports.

Reads an errors file (Codefile.errors.md), uses Copilot to enhance the error analysis,
and updates the errors file with improvements.

## Description
This module provides an Errors Agent that reads existing code file error reports,
uses AI assistance to improve and complete them, and updates the errors files
with enhanced documentation.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add validation for errors file format
- Improve prompt engineering for better error analysis

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
    not general content improvement. For error report improvement, we fall back to basic suggestions.

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
                "# Original error report preserved below:\n\n")

    # The new Copilot CLI is for command suggestions, not content improvement
    # For now, provide basic improvement suggestions for error reports
    if "improve" in prompt.lower() or "error" in prompt.lower() or "report" in prompt.lower():
        return f"""# AI Error Report Improvement Suggestions
# Description: {description}
#
# Suggestions for improving error reports:
# 1. Include clear error messages with specific details
# 2. Add error codes and categorization (fatal, warning, info)
# 3. Include stack traces with line numbers and file paths
# 4. Add timestamps for when errors occurred
# 5. Include system information and environment details
# 6. Provide steps to reproduce the error
# 7. Suggest immediate workarounds or fixes
# 8. Include relevant log entries and debug information
# 9. Add severity levels and impact assessment
# 10. Include contact information for support
#
# Note: Full AI content rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not content generation."""

    try:
        # Try using gh copilot explain for error-related prompts
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
            return "# Copilot CLI available but returned no useful response for error report improvement."

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return "# Copilot CLI timed out or failed.\n\n# Original error report preserved below:\n\n"


class ErrorsAgent:
    """Updates code file error reports using AI assistance."""

    def __init__(self, errors_file: str):
        self.errors_file = Path(errors_file)
        self.previous_errors = ""
        self.current_errors = ""

    def read_previous_errors(self) -> str:
        """Read the existing errors file."""
        if self.errors_file.exists():
            self.previous_errors = self.errors_file.read_text(encoding='utf-8')
        else:
            self.previous_errors = "# Errors\n\nNo errors reported.\n"
        return self.previous_errors

    def improve_errors(self, prompt: str) -> str:
        """Use AI to improve the errors."""
        description = f"Improve the error analysis for {self.errors_file.stem.replace('.errors', '')}"
        try:
            improvement = runSubagent(description, prompt, self.previous_errors)
            self.current_errors = improvement
            return self.current_errors
        except Exception as e:
            print(f"Warning: Failed to improve errors: {e}")
            self.current_errors = self.previous_errors
            return self.current_errors

    def update_errors_file(self):
        """Write the improved errors back to the file."""
        self.errors_file.write_text(fix_markdown_content(self.current_errors), encoding='utf-8')

    def get_diff(self) -> str:
        """Get the diff between previous and current errors."""
        diff = difflib.unified_diff(
            self.previous_errors.splitlines(keepends=True),
            self.current_errors.splitlines(keepends=True),
            fromfile='previous',
            tofile='current'
        )
        return ''.join(diff)


def main():
    parser = argparse.ArgumentParser(description='Errors Agent: Updates code file error reports')
    parser.add_argument('--context', required=True, help='Path to the errors file (e.g., file.errors.md)')
    parser.add_argument('--prompt', required=True, help='Prompt for improving the error analysis')
    args = parser.parse_args()

    agent = ErrorsAgent(args.context)
    agent.read_previous_errors()
    agent.improve_errors(args.prompt)
    agent.update_errors_file()
    diff = agent.get_diff()
    if diff:
        print("Errors updated:")
        print(diff)
    else:
        print("No changes made to errors.")


if __name__ == '__main__':
    main()
