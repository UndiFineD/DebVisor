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

# Description
This module provides an Improvements Agent that reads existing code file improvement suggestions,
uses AI assistance to improve and complete them, and updates the improvements files
with enhanced documentation.

# Changelog
- 1.0.0: Initial implementation

# Suggested Fixes
- Add validation for improvements file format
- Improve prompt engineering for better suggestions

# Improvements
- Better integration with other agents
- Enhanced diff reporting
"""

from base_agent import BaseAgent, create_main_function


class ImprovementsAgent(BaseAgent):
    """Updates code file improvement suggestions using AI assistance."""

    def _get_default_content(self) -> str:
        """Return default content for new improvement files."""
        return "# Improvements\n\nNo improvements suggested.\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original suggestions preserved below:\n\n")

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the improvement suggestions.

        When Copilot CLI is unavailable, BaseAgent keeps the existing content
        unchanged (avoids duplicated wrapper sections).
        """
        return super().improve_content(prompt)


# Create main function using the helper

main = create_main_function(
    ImprovementsAgent,
    'Improvements Agent: Updates code file improvement suggestions',
    'Path to the improvements file (e.g., file.improvements.md)'
)

if __name__ == '__main__':
    main()
