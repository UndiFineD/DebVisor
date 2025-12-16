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
    try:
        import agent_backend  # type: ignore
    except ImportError:
        # Last resort: try to find it relative to this file
        sys.path.append(str(Path(__file__).parent))
        import agent_backend  # type: ignore

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None  # type: ignore[assignment]


def setup_logging(verbosity_arg: int = 0) -> None:
    """Configure logging based on environment variable and argument.
    
    Sets up Python's logging system with level determined by environment
    variable (DV_AGENT_VERBOSITY) and/or command-line argument.
    
    Args:
        verbosity_arg: Verbosity level from --verbose argument (0-3).
                      Levels: 0=ERROR, 1=WARNING, 2=INFO, 3=DEBUG.
                      Defaults to 0 (ERROR).
                      
    Returns:
        None. Configures the global logging system.
        
    Environment Variables:
        DV_AGENT_VERBOSITY: Can be set to 'quiet', 'minimal', 'normal', or 'elaborate'.
        
    Note:
        - verbosity_arg takes precedence when provided and forces DEBUG level
        - Environment variable is used as fallback
        - Defaults to INFO level if neither is set
    """
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
    logging.debug(f"Logging configured at level: {logging.getLevelName(level)}")


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
    """Base class for all AI-powered agents.
    
    Provides common functionality for agents that use AI backends to improve
    code files, documentation, tests, and other artifacts. Handles file I/O,
    diff generation, and integration with AI services.
    
    Attributes:
        file_path (Path): Path to the file being improved.
        previous_content (str): Original file content before improvements.
        current_content (str): Improved file content after agent processing.
        
    Subclasses:
        - CoderAgent: Improves source code files
        - TestsAgent: Generates and improves test files
        - ChangesAgent: Manages changelog documentation
        - ContextAgent: Manages context/description files
        - ErrorsAgent: Analyzes and documents errors
        - ImprovementsAgent: Suggests code improvements
        - StatsAgent: Collects and reports statistics
        
    Example:
        class MyAgent(BaseAgent):
            def _get_default_content(self):
                return "# New File\\n"
        
        agent = MyAgent('path/to/file.md')
        agent.improve_content("Make it better")
        agent.update_file()
        
    Note:
        - Automatically detects markdown files for formatting cleanup
        - Provides fallback responses when AI backend unavailable
        - Supports multiple AI backends via agent_backend module
    """

    def __init__(self, file_path: str) -> None:
        """Initialize the BaseAgent with file path.
        
        Args:
            file_path: Path to the file to improve. Can be absolute or relative.
                      Will be converted to pathlib.Path object.
                      
        Note:
            Automatically reads previous content on initialization.
        """
        self.file_path = Path(file_path)
        self.previous_content = ""
        self.current_content = ""
        logging.debug(f"Initializing {self.__class__.__name__} for {file_path}")
        self.read_previous_content()

    def read_previous_content(self) -> str:
        """Read the existing file content from disk.
        
        Reads the file specified by file_path, storing content in previous_content.
        If file doesn't exist, loads default content for new files.
        
        Returns:
            str: The read content (same as previous_content attribute).
            
        Raises:
            None. Logs errors but doesn't raise. Returns empty string on failure.
            
        Note:
            - Uses UTF-8 encoding
            - Handles missing files gracefully
            - Automatically handles encoding errors
        """
        if self.file_path.exists():
            try:
                logging.debug(f"Reading content from {self.file_path}")
                self.previous_content = self.file_path.read_text(encoding='utf-8')
                logging.info(f"Read {len(self.previous_content)} bytes from {self.file_path.name}")
            except Exception as e:
                logging.error(f"Failed to read file {self.file_path}: {e}")
                self.previous_content = ""
        else:
            logging.debug(f"File does not exist, using default content: {self.file_path}")
            self.previous_content = self._get_default_content()
        return self.previous_content

    def _get_default_content(self) -> str:
        """Return default content for new files.
        
        Provides a template for new files when they don't exist yet.
        Override in subclasses to provide agent-specific defaults.
        
        Returns:
            str: Default content template for the file type.
            
        Example:
            class TestsAgent(BaseAgent):
                def _get_default_content(self):
                    return "# Tests\\n\\n# Add tests here\\n"
                    
        Note:
            Called automatically by read_previous_content() for missing files.
        """
        return "# Default content\n\n# Add content here\n"

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the content.
        
        Calls the agent_backend with the previous content and a prompt,
        receives improved content, and stores it in current_content.
        
        Args:
            prompt: The prompt describing what improvements to make.
                   e.g., "Add comprehensive docstrings to all functions"
                   
        Returns:
            str: The improved content (same as current_content attribute).
            
        Raises:
            None. Falls back to previous_content on error.
            
        Example:
            agent.improve_content("Improve error handling")
            print(agent.current_content)
            
        Note:
            - Overridable in subclasses for agent-specific behavior
            - Logs warnings on failure but doesn't raise
            - Falls back to original content if improvement fails
        """
        description = f"Improve the {self.__class__.__name__.replace('Agent', '').lower()} for {self.file_path.stem}"
        try:
            logging.info(f"Improving content with prompt: {prompt[:50]}...")
            improvement = self.run_subagent(description, prompt, self.previous_content)
            self.current_content = improvement
            logging.info(f"Content improved successfully ({len(improvement)} bytes)")
            return self.current_content
        except Exception as e:
            logging.warning(f"Failed to improve content: {e}")
            self.current_content = self.previous_content
            return self.current_content

    def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        """Run a subagent using one of several AI backends.
        
        Delegates to agent_backend.run_subagent which selects the appropriate
        AI backend (copilot, GitHub Models, etc.) and executes the request.
        
        Args:
            description: Human-readable description of the task.
            prompt: The prompt to send to the AI backend.
            original_content: The content being improved (context for AI).
                            Defaults to empty string.
                            
        Returns:
            str: Response from the AI backend, or fallback if unavailable.
            
        Raises:
            None. Returns fallback response on error.
            
        Note:
            - Backend selection is automatic or via DV_AGENT_BACKEND env var
            - Supports multiple backends: copilot, GitHub Models, local
            - Returns original_content as fallback if backend unavailable
        """
        logging.debug(f"Running subagent: {description}")
        result = agent_backend.run_subagent(description, prompt, original_content)
        if result is None:
            logging.warning("Subagent returned None, using fallback response")
            return original_content or self._get_fallback_response()
        return result

    @staticmethod
    def get_backend_status() -> dict:
        """Return a diagnostic snapshot of backend availability and configuration.
        
        Returns:
            dict: Status information for all available AI backends.
                 Includes availability, version, and configuration details.
                 
        Example:
            status = BaseAgent.get_backend_status()
            for backend, info in status.items():
                print(f"{backend}: {info}")
        """
        logging.debug("Fetching backend status")
        return agent_backend.get_backend_status()

    @staticmethod
    def describe_backends() -> str:
        """Return human-readable backend diagnostics for debugging.
        
        Returns:
            str: Formatted text describing available backends and their status.
                 Useful for troubleshooting configuration issues.
                 
        Example:
            print(BaseAgent.describe_backends())
            # Output: Available backends, versions, configuration details
        """
        logging.debug("Describing backend configuration")
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
        """Write the improved content back to the file.
        
        Writes current_content to disk, with special handling for markdown files
        which get normalized/fixed using the fix_markdown_content function.
        
        Returns:
            None.
            
        Raises:
            OSError: If file write fails.
            
        Note:
            - Automatically detects markdown files (.md, .markdown, .plan.md)
            - Applies markdown normalization only to markdown files
            - Uses UTF-8 encoding for all files
            - Creates parent directories if they don't exist
            
        Example:
            agent.current_content = "# Improved Content"
            agent.update_file()  # Writes to agent.file_path
        """
        content_to_write = self.current_content
        # Only run the markdown fixer on markdown-like files. Applying markdown
        # normalization to source code can corrupt it.
        suffix = self.file_path.suffix.lower()
        is_markdown = suffix in {'.md', '.markdown'} or self.file_path.name.lower().endswith('.plan.md')
        if is_markdown:
            logging.debug(f"Applying markdown formatting to {self.file_path.name}")
            content_to_write = fix_markdown_content(content_to_write)
        
        logging.info(f"Writing {len(content_to_write)} bytes to {self.file_path.name}")
        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(content_to_write, encoding='utf-8')

    def get_diff(self) -> str:
        """Get the diff between previous and current content.
        
        Generates a unified diff showing what changed between the original
        and improved versions of the file.
        
        Returns:
            str: Unified diff format. Empty string if no changes.
            
        Example:
            diff = agent.get_diff()
            if diff:
                print("Changes made:")
                print(diff)
            else:
                print("No changes")
                
        Note:
            - Uses difflib.unified_diff for standard format
            - Preserves line endings in diff
            - Empty string indicates no changes between versions
        """
        logging.debug("Generating diff between previous and current content")
        diff = difflib.unified_diff(
            self.previous_content.splitlines(keepends=True),
            self.current_content.splitlines(keepends=True),
            fromfile='previous',
            tofile='current'
        )
        diff_str = ''.join(diff)
        if diff_str:
            logging.debug(f"Generated {len(diff_str)} bytes of diff")
        else:
            logging.debug("No differences found")
        return diff_str


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
