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
Base Agent: Common functionality for all AI-powered agents.

Provides shared functionality for agents that improve code files using AI assistance.
"""

import subprocess
from pathlib import Path
import argparse
import difflib
import sys

# Import markdown fixing functionality
sys.path.insert(0, str(Path(__file__).parent.parent / 'fix'))
from fix_markdown_lint import fix_markdown_content  # noqa: E402  # type: ignore


class BaseAgent:
    """Base class for all AI-powered agents."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.previous_content = ""
        self.current_content = ""

    def read_previous_content(self) -> str:
        """Read the existing file content."""
        if self.file_path.exists():
            self.previous_content = self.file_path.read_text(encoding='utf-8')
        else:
            self.previous_content = self._get_default_content()
        return self.previous_content

    def _get_default_content(self) -> str:
        """Return default content for new files. Override in subclasses."""
        return "# Default content\n\n# Add content here\n"

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the content. Override in subclasses."""
        description = f"Improve the {self.__class__.__name__.replace('Agent', '').lower()} for {self.file_path.stem}"
        try:
            improvement = self.run_subagent(description, prompt, self.previous_content)
            self.current_content = improvement
            return self.current_content
        except Exception as e:
            print(f"Warning: Failed to improve content: {e}")
            self.current_content = self.previous_content
            return self.current_content

    def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        """
        Run a subagent using GitHub Copilot CLI.

        Note: The gh-copilot extension has been deprecated in favor of the newer GitHub Copilot CLI.
        For more information, visit:
        - Copilot CLI: https://github.com/github/copilot-cli

        Args:
            description: Description of the task
            prompt: The prompt to send to Copilot
            original_content: Original content (for context)

        Returns:
            AI response as a string, or fallback suggestions
        """
        try:
            # Check if gh command is available
            subprocess.run(['gh', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # In environments without GitHub CLI/Copilot, do not overwrite files with
            # synthetic placeholder suggestions. Keep existing content unchanged.
            return original_content or self._get_fallback_response()

        # Try using gh copilot explain
        try:
            result = subprocess.run(
                ['gh', 'copilot', 'explain', prompt[:200]],  # Limit prompt length
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0 and result.stdout.strip():
                return f"# GitHub Copilot Explanation:\n{result.stdout.strip()}"
            else:
                return self._get_fallback_response()

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return self._get_fallback_response()

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot CLI is unavailable. Override in subclasses."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub Copilot CLI not found or failed.\n"
                "# Install GitHub CLI and Copilot extension: https://github.com/github/copilot-cli")

    def update_file(self):
        """Write the improved content back to the file."""
        content_to_write = self.current_content
        # Only run the markdown fixer on markdown-like files. Applying markdown
        # normalization to source code can corrupt it.
        suffix = self.file_path.suffix.lower()
        is_markdown = suffix in {'.md', '.markdown'} or self.file_path.name.lower().endswith('.plan.md')
        if is_markdown:
            content_to_write = fix_markdown_content(content_to_write)
        self.file_path.write_text(content_to_write, encoding='utf-8')

    def get_diff(self) -> str:
        """Get the diff between previous and current content."""
        diff = difflib.unified_diff(
            self.previous_content.splitlines(keepends=True),
            self.current_content.splitlines(keepends=True),
            fromfile='previous',
            tofile='current'
        )
        return ''.join(diff)


def create_main_function(agent_class, description: str, context_help: str):
    """Create a main function for an agent class."""
    def main():
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--context', required=True, help=context_help)
        parser.add_argument('--prompt', required=True, help='Prompt for improving the content')
        args = parser.parse_args()

        agent = agent_class(args.context)
        agent.read_previous_content()
        agent.improve_content(args.prompt)
        agent.update_file()
        diff = agent.get_diff()
        if diff:
            print(f"{agent_class.__name__.replace('Agent', '').lower()} updated:")
            print(diff)
        else:
            print(f"No changes made to {agent_class.__name__.replace('Agent', '').lower()}.")

    return main
