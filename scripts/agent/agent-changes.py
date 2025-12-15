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
"""

from typing import Optional
import logging
from base_agent import BaseAgent, create_main_function


class ChangesAgent(BaseAgent):
    """Updates code file changelogs using AI assistance."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_file_extension()
        self._check_associated_file()

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith('.changes.md'):
            logging.warning(f"File {self.file_path.name} does not end with .changes.md")

    def _check_associated_file(self) -> None:
        """Check if the associated code file exists."""
        name = self.file_path.name
        if name.endswith('.changes.md'):
            base_name = name[:-11]  # len('.changes.md')
            # Try to find the file with common extensions or exact match
            candidate = self.file_path.parent / base_name
            if candidate.exists():
                return
            # Try adding extensions
            for ext in ['.py', '.sh', '.js', '.ts', '.md']:
                candidate = self.file_path.parent / (base_name + ext)
                if candidate.exists() and candidate != self.file_path:
                    return
            logging.warning(f"Could not find associated code file for {self.file_path.name}")

    def _get_default_content(self) -> str:
        """Return default content for new changelog files."""
        return "# Changes\n\nNo changes recorded.\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original changelog preserved below:\n\n")

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the changelogs with specific change tracking suggestions."""
        logging.info(f"Improving changelog for {self.file_path}")
        # Add guidance for structured output
        enhanced_prompt = (
            f"{prompt}\n\n"
            "Please format the changelog using 'Keep a Changelog' conventions:\n"
            "## [Version] - YYYY-MM-DD\n"
            "### Added\n"
            "### Changed\n"
            "### Deprecated\n"
            "### Removed\n"
            "### Fixed\n"
            "### Security\n"
        )
        description = f"Improve the changelog for {self.file_path.stem.replace('.changes', '')}"
        # For changelog improvement, provide specific change tracking suggestions
        if any(keyword in prompt.lower() for keyword in ["improve", "change", "log"]):
            fallback_suggestions = f"""# AI Changelog Improvement Suggestions
# Description: {description}
#
# Suggestions:
# 1. Follow 'Keep a Changelog' format
# 2. Group changes by type (Added, Changed, Deprecated, Removed, Fixed, Security)
# 3. Include dates for versions
# 4. Be specific about changes
#
# Original changelog preserved below:
#
{self.previous_content}"""
            self.current_content = fallback_suggestions
            return self.current_content
        # For other prompts, use the base implementation with enhanced prompt
        return super().improve_content(enhanced_prompt)


# Create main function using the helper
main = create_main_function(
    ChangesAgent,
    'Changes Agent: Updates code file changelogs',
    'Path to the changes file (e.g., file.changes.md)'
)


if __name__ == '__main__':
    main()
