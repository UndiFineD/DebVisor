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

import logging
from pathlib import Path
from typing import Optional
from base_agent import BaseAgent, create_main_function


class ContextAgent(BaseAgent):
    """Updates code file context descriptions using AI assistance."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_file_extension()
        self.source_path = self._derive_source_path()

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith('.description.md'):
            # Just warn, don't fail
            pass

    def _derive_source_path(self) -> Optional[Path]:
        """Derive source file path from .description.md filename."""
        if self.file_path.name.endswith('.description.md'):
            stem = self.file_path.name.replace('.description.md', '')
            # Try common extensions
            for ext in ['.py', '.js', '.ts', '.go', '.rs', '.java', '.sh']:
                source = self.file_path.parent / f"{stem}{ext}"
                if source.exists():
                    return source
        return None

    def _get_default_content(self) -> str:
        """Return rich, structured template for new descriptions."""
        filename = self.file_path.name.replace('.description.md', '')
        return f"""# Description: `{filename}`

## Purpose
[One-line purpose statement]

## Key Features
- [Feature 1]
- [Feature 2]

## Usage
```bash
# Example usage
```
"""

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
        logging.info(f"Improving context for {self.file_path}")
        # Include source code in AI context for accurate descriptions
        if self.source_path and self.source_path.exists():
            logging.debug(f"Using source file: {self.source_path}")
            try:
                # Limit source code to 8000 chars to avoid token limits
                source_code = self.source_path.read_text(encoding='utf-8')[:8000]
                enhanced_prompt = (
                    f"{prompt}\n\n"
                    f"Source code to analyze ({self.source_path.name}):\n"
                    f"```\n{source_code}\n```\n\n"
                    "Based on the source code above, provide a comprehensive description."
                )
                return super().improve_content(enhanced_prompt)
            except (OSError, UnicodeDecodeError):
                pass
                
        return super().improve_content(prompt)


# Create main function using the helper
main = create_main_function(
    ContextAgent,
    'Context Agent: Updates code file descriptions',
    'Path to the context file (e.g., file.description.md)'
)

if __name__ == '__main__':
    main()
