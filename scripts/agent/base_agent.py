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

import argparse
import difflib
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
from typing import Optional

try:
    from scripts.agent import agent_backend
except ImportError:
    # Fallback for when running directly or in tests without package structure
    import agent_backend  # type: ignore

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None  # type: ignore[assignment]


def setup_logging(verbosity_arg: int = 0) -> None:
    """Configure logging based on environment variable and argument."""
    env_verbosity = os.environ.get('DV_AGENT_VERBOSITY')
    levels = {
        'quiet': logging.ERROR,
        'minimal': logging.WARNING,
        'normal': logging.INFO,
        'elaborate': logging.DEBUG,
        '0': logging.ERROR,
        '1': logging.WARNING,
        '2': logging.INFO,
        '3': logging.DEBUG,
    }
    # Determine level from environment
    if env_verbosity:
        level = levels.get(env_verbosity.lower(), logging.INFO)
    else:
        level = logging.INFO
    # If argument is provided, it forces DEBUG (elaborate)
    if verbosity_arg > 0:
        level = logging.DEBUG
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


# Import markdown fixing functionality (optional).
try:
    from scripts.fix.fix_markdown_lint import fix_markdown_content  # type: ignore
except ImportError:
    try:
        import importlib.util
        fix_dir = Path(__file__).parent.parent / 'fix'
        spec = importlib.util.spec_from_file_location("fix_markdown_lint", str(fix_dir / "fix_markdown_lint.py"))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules["fix_markdown_lint"] = module
            spec.loader.exec_module(module)
            fix_markdown_content = module.fix_markdown_content
        else:
            raise ImportError
    except (ImportError, AttributeError):  # pragma: no cover
        def fix_markdown_content(text: str) -> str:
            return text


class BaseAgent:
    """Base class for all AI-powered agents."""

    def __init__(self, file_path: str) -> None:
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
            logging.warning(f"Failed to improve content: {e}")
            self.current_content = self.previous_content
            return self.current_content

    def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        """
        Run a subagent using one of several AI backends.
        Delegates to agent_backend.run_subagent.
        """
        result = agent_backend.run_subagent(description, prompt, original_content)
        if result is None:
            return original_content or self._get_fallback_response()
        return result

    @staticmethod
    def get_backend_status() -> dict:
        """Return a diagnostic snapshot of backend availability/config."""
        return agent_backend.get_backend_status()

    @staticmethod
    def describe_backends() -> str:
        """Human-readable backend diagnostics for debugging."""
        return agent_backend.describe_backends()

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot CLI is unavailable. Override in subclasses."""
        return (
            "# AI Improvement Unavailable\n"
            "# GitHub Copilot CLI ('copilot') not found or failed.\n"
            "# Install Copilot CLI: https://github.com/github/copilot-cli\n"
            "# Windows: winget install GitHub.Copilot\n"
            "# npm: npm install -g @github/copilot\n"
        )

    def update_file(self) -> None:
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


from typing import Optional, Type, Callable, Any

# ... (imports)

def create_main_function(agent_class: Type[BaseAgent], description: str, context_help: str) -> Callable[[], None]:
    """Create a main function for an agent class."""
    def main() -> None:
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            '--describe-backends',
            action='store_true',
            help='Print which AI backends are available/configured and exit',
        )
        parser.add_argument(
            '--backend',
            choices=['auto', 'copilot', 'gh', 'github-models'],
            default=None,
            help='Select backend (overrides DV_AGENT_BACKEND for this run only)',
        )
        parser.add_argument(
            '--verbose',
            '-v',
            action='count',
            default=0,
            help='Increase verbosity (can be used multiple times, e.g. -vv)',
        )
        parser.add_argument('--context', required=True, help=context_help)
        parser.add_argument('--prompt', required=True, help='Prompt for improving the content')
        args = parser.parse_args()
        setup_logging(args.verbose)
        if args.backend:
            os.environ['DV_AGENT_BACKEND'] = args.backend
        if args.describe_backends:
            print(agent_class.describe_backends())
            return
        agent = agent_class(args.context)
        agent.read_previous_content()
        agent.improve_content(args.prompt)
        agent.update_file()
        diff = agent.get_diff()
        if diff:
            logging.info(f"{agent_class.__name__.replace('Agent', '').lower()} updated:")
            logging.info(diff)
        else:
            logging.info(f"No changes made to {agent_class.__name__.replace('Agent', '').lower()}.")
    return main
