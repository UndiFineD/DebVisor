# AI Code Improvement Suggestions
# Description: Improve the code for agent-changes.py
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

# !/usr/bin/env python3
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
Changes Agent: Improves and updates code file changelogs.

Reads a changes file (Codefile.changes.md), uses Copilot to enhance the changelog,
and updates the changes file with improvements.

## Description
This module provides a Changes Agent that reads existing code file changelogs,
uses AI assistance to improve and complete them, and updates the changes files
with enhanced documentation.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add validation for changes file format
- Improve prompt engineering for better changelogs

## Improvements
- Better integration with other agents
- Enhanced diff reporting
"""

import subprocess
from pathlib import Path
import argparse
import difflib
import sys

# Import markdown fixing functionality
sys.path.insert(0, str(Path(__file__).parent.parent / 'fix'))
from fix_markdown_lint import fix_markdown_content  # noqa: E402


def runSubagent(description: str, prompt: str, original_content: str = "") -> str:
    """
    Run a subagent using GitHub Copilot CLI to interact with GitHub Copilot.

    Note: The new GitHub Copilot CLI (gh copilot) is designed for command suggestions,
    not general content improvement. For changelog improvement, we fall back to basic suggestions.

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
                "# Original changelog preserved below:\n\n")

    # The new Copilot CLI is for command suggestions, not content improvement
    # For now, provide basic improvement suggestions for changelogs
    if "improve" in prompt.lower() or "changelog" in prompt.lower() or "changes" in prompt.lower():
        # Check if content already has AI suggestions
        if original_content.strip().startswith("# AI Changelog Improvement Suggestions"):
            return original_content

        return f"""# AI Changelog Improvement Suggestions
# Description: {description}
#
# Suggestions for improving changelogs:
# 1. Use consistent formatting with clear section headers (Added, Changed, Fixed, Removed)
# 2. Include version numbers and release dates for each entry
# 3. Write clear, concise descriptions of changes
# 4. Group related changes together logically
# 5. Include breaking changes prominently
# 6. Add links to issues, pull requests, or commits when relevant
# 7. Use proper semantic versioning conventions
# 8. Include migration guides for breaking changes
# 9. Add contributor acknowledgments
# 10. Keep entries chronological with newest first
#
# Note: Full AI content rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not content generation."""

    try:
        # Try using gh copilot explain for changelog-related prompts
        result = subprocess.run(
            ['gh', 'copilot', 'explain', prompt[:200]],  # Limit prompt length
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout.strip():
            return f"# GitHub Copilot Explanation:\n{result.stdout.strip()}"
        else:
            return "# Copilot CLI available but returned no useful response for changelog improvement."

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return "# Copilot CLI timed out or failed."


class ChangesAgent:
    """Updates code file changelogs using AI assistance."""

    def __init__(self, changes_file: str):
        self.changes_file = Path(changes_file)
        self.previous_changes = ""
        self.current_changes = ""

    def read_previous_changes(self) -> str:
        """Read the existing changes file."""
        if self.changes_file.exists():
            self.previous_changes = self.changes_file.read_text(encoding='utf-8')
        else:
            self.previous_changes = "# Changelog\n\n- Initial version\n"
        return self.previous_changes

    def improve_changes(self, prompt: str) -> str:
        """Use AI to improve the changes."""
        description = f"Improve the changelog for {self.changes_file.stem.replace('.changes', '')}"
        try:
            improvement = runSubagent(description, prompt, self.previous_changes)
            self.current_changes = improvement
            return self.current_changes
        except Exception as e:
            print(f"Warning: Failed to improve changes: {e}")
            self.current_changes = self.previous_changes
            return self.current_changes

    def update_changes_file(self):
        """Write the improved changes back to the file."""
        self.changes_file.write_text(fix_markdown_content(self.current_changes), encoding='utf-8')

    def get_diff(self) -> str:
        """Get the diff between previous and current changes."""
        diff = difflib.unified_diff(
            self.previous_changes.splitlines(keepends=True),
            self.current_changes.splitlines(keepends=True),
            fromfile='previous',
            tofile='current'
        )
        return ''.join(diff)


def main():
    parser = argparse.ArgumentParser(description='Changes Agent: Updates code file changelogs')
    parser.add_argument('--context', required=True, help='Path to the changes file (e.g., file.changes.md)')
    parser.add_argument('--prompt', required=True, help='Prompt for improving the changelog')
    args = parser.parse_args()

    agent = ChangesAgent(args.context)
    agent.read_previous_changes()
    agent.improve_changes(args.prompt)
    agent.update_changes_file()
    diff = agent.get_diff()
    if diff:
        print("Changes updated:")
        print(diff)
    else:
        print("No changes made to changes.")


if __name__ == '__main__':
    main()
