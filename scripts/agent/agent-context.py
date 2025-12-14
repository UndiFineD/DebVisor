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

# Description
This module provides a Context Agent that reads existing code file descriptions,
uses AI assistance to improve and complete them, and updates the context files
with enhanced documentation.

# Changelog
- 1.0.0: Initial implementation

# Suggested Fixes
- Add validation for context file format
- Improve prompt engineering for better descriptions

# Improvements
- Better integration with other agents
- Enhanced diff reporting
"""

from base_agent import BaseAgent, create_main_function


class ContextAgent(BaseAgent):
    """Updates code file context descriptions using AI assistance."""

    def _get_default_content(self) -> str:
        """Return default content for new context files."""
        return "# Description\n\nNo description available.\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original content preserved below:\n\n")

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the context.

        When Copilot CLI is unavailable, BaseAgent keeps the existing file
        content unchanged instead of injecting duplicated placeholder blocks.
        """
        return super().improve_content(prompt)


# Create main function using the helper

main = create_main_function(
    ContextAgent,
    'Context Agent: Updates code file descriptions',
    'Path to the context file (e.g., file.description.md)'
)

if __name__ == '__main__':
    main()
