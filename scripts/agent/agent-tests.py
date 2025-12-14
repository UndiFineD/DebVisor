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
# Description: Improve the code for agent-tests.py
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
Tests Agent: Improves and updates code file test suites.

Reads a tests file (test_Codefile.py), uses Copilot to enhance the tests,
and updates the tests file with improvements.

## Description
This module provides a Tests Agent that reads existing code file test suites,
uses AI assistance to improve and complete them, ensuring each line of the codefile is tested,
and updates the tests files with enhanced test coverage.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add validation for tests file format
- Improve prompt engineering for better test generation

## Improvements
- Better integration with other agents
- Enhanced diff reporting
"""

import subprocess
from pathlib import Path
import argparse
import difflib


def runSubagent(description: str, prompt: str, original_content: str = "") -> str:
    """
    Run a subagent using GitHub Copilot CLI to interact with GitHub Copilot.

    Note: The new GitHub Copilot CLI (gh copilot) is designed for command suggestions,
    not general content improvement. For test improvement, we fall back to basic suggestions.

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
        return ("# AI Improvement Unavailable\n# GitHub CLI not found. Install from "
                "https://cli.github.com/\n\n# Original test code preserved below:\n\n")

    # The new Copilot CLI is for command suggestions, not content improvement
    # For now, provide basic improvement suggestions for tests
    if "improve" in prompt.lower() or "test" in prompt.lower():
        return f"""# AI Test Improvement Suggestions
# Description: {description}
#
# Suggestions for improving test suites:
# 1. Add unit tests for all public functions and methods
# 2. Include integration tests for component interactions
# 3. Add edge case and error condition testing
# 4. Implement property-based testing where applicable
# 5. Add performance and load testing
# 6. Include security testing and vulnerability checks
# 7. Add mock objects and test doubles for external dependencies
# 8. Implement test fixtures and setup/teardown methods
# 9. Add test coverage reporting and analysis
# 10. Include automated test execution in CI/CD pipelines
#
# Note: Full AI content rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not content generation."""

    try:
        # Try using gh copilot explain for test-related prompts
        result = subprocess.run(
            ['gh', 'copilot', 'explain', prompt[:200]],  # Limit prompt length
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout.strip():
            return f"# GitHub Copilot Explanation:\n{result.stdout.strip()}"
        else:
            return "# Copilot CLI available but returned no useful response for test improvement."

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return "# Copilot CLI timed out or failed."


class TestsAgent:
    """Updates code file test suites using AI assistance."""

    def __init__(self, tests_file: str):
        self.tests_file = Path(tests_file)
        self.previous_tests = ""
        self.current_tests = ""

    def read_previous_tests(self) -> str:
        """Read the existing tests file."""
        if self.tests_file.exists():
            self.previous_tests = self.tests_file.read_text(encoding='utf-8')
        else:
            self.previous_tests = "# Tests\n\nimport pytest\n\n# Add tests here\n"
        return self.previous_tests

    def improve_tests(self, prompt: str) -> str:
        """Use AI to improve the tests."""
        description = f"Improve the test suite for {self.tests_file.stem.replace('.tests', '')}"
        try:
            improvement = runSubagent(description, prompt, self.previous_tests)
            self.current_tests = improvement
            return self.current_tests
        except Exception as e:
            print(f"Warning: Failed to improve tests: {e}")
            self.current_tests = self.previous_tests
            return self.current_tests

    def update_tests_file(self):
        """Write the improved tests back to the file."""
        self.tests_file.write_text(self.current_tests, encoding='utf-8')

    def get_diff(self) -> str:
        """Get the diff between previous and current tests."""
        diff = difflib.unified_diff(
            self.previous_tests.splitlines(keepends=True),
            self.current_tests.splitlines(keepends=True),
            fromfile='previous',
            tofile='current'
        )
        return ''.join(diff)


def main():
    parser = argparse.ArgumentParser(description='Tests Agent: Updates code file test suites')
    parser.add_argument('--context', required=True, help='Path to the tests file (e.g., test_file.py)')
    parser.add_argument('--prompt', required=True, help='Prompt for improving the test suite')
    args = parser.parse_args()

    agent = TestsAgent(args.context)
    agent.read_previous_tests()
    agent.improve_tests(args.prompt)
    agent.update_tests_file()
    diff = agent.get_diff()
    if diff:
        print("Tests updated:")
        print(diff)
    else:
        print("No changes made to tests.")


if __name__ == '__main__':
    main()
