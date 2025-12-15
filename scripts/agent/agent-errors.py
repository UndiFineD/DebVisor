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
Errors Agent: Improves and updates code file error reports.

Reads an errors file (Codefile.errors.md), uses Copilot to enhance the error analysis,
and updates the errors file with improvements.

# Description
This module provides an Errors Agent that reads existing code file error reports,
uses AI assistance to improve and complete them, and updates the errors files
with enhanced documentation.

# Changelog
- 1.0.0: Initial implementation

# Suggested Fixes
- Add validation for errors file format
- Improve prompt engineering for better error analysis

# Improvements
- Better integration with other agents
- Enhanced diff reporting
"""

from typing import Optional
import logging
from base_agent import BaseAgent, create_main_function


class ErrorsAgent(BaseAgent):
    """Updates code file error reports using AI assistance."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self._validate_error_file_path()
        self._check_associated_file()

    def _validate_error_file_path(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith('.errors.md'):
            logging.warning(f"File {self.file_path.name} does not end with .errors.md")

    def _check_associated_file(self) -> None:
        """Check if the associated code file exists."""
        name = self.file_path.name
        if name.endswith('.errors.md'):
            base_name = name[:-10]  # len('.errors.md')
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
        """Return structured error report template."""
        return (
            "# Error Report\n\n"
            "## Summary\n\n"
            "No errors detected.\n\n"
            "## Details\n\n"
            "- **File**: (not specified)\n"
            "- **Last Analyzed**: (not specified)\n"
            "- **Status**: ✓ Clean\n\n"
            "## Static Analysis\n\n"
            "No issues found.\n\n"
            "## Linting Results\n\n"
            "No violations detected.\n\n"
            "## Type Checking\n\n"
            "No type errors.\n\n"
            "## Security Scan\n\n"
            "No vulnerabilities identified.\n"
        )

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original error report preserved below:\n\n")

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the error report.

        When Copilot CLI is unavailable, BaseAgent keeps the existing content
        unchanged (avoids duplicated wrapper sections).
        """
        return super().improve_content(prompt)


# Create main function using the helper
main = create_main_function(
    ErrorsAgent,
    'Errors Agent: Updates code file error reports',
    'Path to the errors file (e.g., file.errors.md)'
)

if __name__ == '__main__':
    main()
