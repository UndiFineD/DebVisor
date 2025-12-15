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

from base_agent import BaseAgent, create_main_function


class ErrorsAgent(BaseAgent):
    """Updates code file error reports using AI assistance."""

    def _get_default_content(self) -> str:
        """Return default content for new error files."""
        return "# Errors\n\nNo errors reported.\n"

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
