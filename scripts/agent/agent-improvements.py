# AI Code Improvement Suggestions
# Description: Improve the code for agent-improvements.py
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
Improvements Agent: Improves and updates code file improvement suggestions.

Reads an improvements file (Codefile.improvements.md), uses Copilot to enhance the suggestions,
and updates the improvements file with improvements.

## Description
This module provides an Improvements Agent that reads existing code file improvement suggestions,
uses AI assistance to improve and complete them, and updates the improvements files
with enhanced documentation.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add validation for improvements file format
- Improve prompt engineering for better suggestions

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
    not general content improvement. For improvement suggestions, we fall back to basic suggestions.

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
                "# Original suggestions preserved below:\n\n")

    # The new Copilot CLI is for command suggestions, not content improvement
    # For now, provide basic improvement suggestions
    if "improve" in prompt.lower() or "suggestion" in prompt.lower() or "enhancement" in prompt.lower():
        # Check if content already has AI suggestions
        if original_content.strip().startswith("# AI Improvement Suggestions"):
            return original_content

        return f"""# AI Improvement Suggestions
# Description: {description}
#
# General improvement suggestions:
# 1. Code Quality: Add comprehensive error handling and input validation
# 2. Documentation: Include detailed docstrings and usage examples
# 3. Testing: Implement unit tests and integration tests
# 4. Performance: Optimize algorithms and add caching where appropriate
# 5. Security: Implement proper authentication and authorization
# 6. Maintainability: Refactor complex functions and improve code organization
# 7. User Experience: Add progress indicators and clear error messages
# 8. Scalability: Design for horizontal scaling and load balancing
# 9. Monitoring: Add logging and metrics collection
# 10. Deployment: Implement CI/CD pipelines and automated testing
#
# Note: Full AI content rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not content generation.
#
# Original suggestions preserved below:
#

{original_content}"""

    try:
        # Try using gh copilot explain for improvement-related prompts
        result = subprocess.run(
            ['gh', 'copilot', 'explain', prompt[:200]],  # Limit prompt length
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout.strip():
            return (f"# GitHub Copilot Explanation:\n{result.stdout.strip()}\n\n"
                    "# Original suggestions preserved below:\n\n")
        else:
            return ("# Copilot CLI available but returned no useful response for improvement "
                    "suggestions.\n\n# Original suggestions preserved below:\n\n")

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return "# Copilot CLI timed out or failed.\n\n# Original suggestions preserved below:\n\n"


class ImprovementsAgent:
    """Updates code file improvement suggestions using AI assistance."""

    def __init__(self, improvements_file: str):
        self.improvements_file = Path(improvements_file)
        self.previous_improvements = ""
        self.current_improvements = ""

    def read_previous_improvements(self) -> str:
        """Read the existing improvements file."""
        if self.improvements_file.exists():
            self.previous_improvements = self.improvements_file.read_text(encoding='utf-8')
        else:
            self.previous_improvements = "# Improvements\n\nNo improvements suggested.\n"
        return self.previous_improvements

    def improve_improvements(self, prompt: str) -> str:
        """Use AI to improve the improvements."""
        base_name = self.improvements_file.stem.replace('.improvements', '')
        description = f"Improve the improvement suggestions for {base_name}"
        try:
            improvement = runSubagent(description, prompt, self.previous_improvements)
            self.current_improvements = improvement
            return self.current_improvements
        except Exception as e:
            print(f"Warning: Failed to improve improvements: {e}")
            self.current_improvements = self.previous_improvements
            return self.current_improvements

    def update_improvements_file(self):
        """Write the improved improvements back to the file."""
        self.improvements_file.write_text(fix_markdown_content(self.current_improvements), encoding='utf-8')

    def get_diff(self) -> str:
        """Get the diff between previous and current improvements."""
        diff = difflib.unified_diff(
            self.previous_improvements.splitlines(keepends=True),
            self.current_improvements.splitlines(keepends=True),
            fromfile='previous',
            tofile='current'
        )
        return ''.join(diff)


def main():
    parser = argparse.ArgumentParser(description='Improvements Agent: Updates code file improvement suggestions')
    parser.add_argument('--context', required=True, help='Path to the improvements file (e.g., file.improvements.md)')
    parser.add_argument('--prompt', required=True, help='Prompt for improving the suggestions')
    args = parser.parse_args()

    agent = ImprovementsAgent(args.context)
    agent.read_previous_improvements()
    agent.improve_improvements(args.prompt)
    agent.update_improvements_file()
    diff = agent.get_diff()
    if diff:
        print("Improvements updated:")
        print(diff)
    else:
        print("No changes made to improvements.")


if __name__ == '__main__':
    main()
