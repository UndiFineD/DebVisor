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
# Description: Improve the code for agent.py
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
Agent: Orchestrates work among sub-agents for code improvement.

Assigns tasks to various agents to improve code files, their documentation,
tests, and related artifacts.

## Description
This module provides the main Agent that coordinates the improvement process
across code files by calling specialized sub-agents for different aspects
of code quality and documentation.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add better error handling
- Implement async execution for agents

## Improvements
- Enhanced coordination between agents
- Better progress tracking
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Set
import argparse
import fnmatch

# Import markdown fixing functionality
sys.path.insert(0, str(Path(__file__).parent.parent / 'fix'))
from fix_markdown_lint import fix_markdown_content  # noqa: E402


def load_codeignore(root: Path) -> Set[str]:
    """Load ignore patterns from .codeignore file."""
    codeignore_path = root / ".codeignore"
    if codeignore_path.exists():
        try:
            content = codeignore_path.read_text(encoding='utf-8')
            return {
                line.strip() for line in content.split('\n')
                if line.strip() and not line.strip().startswith('#')
            }
        except Exception as e:
            print(f"Warning: Could not read .codeignore file: {e}")
    return set()


class Agent:
    """Main agent that orchestrates sub-agents for code improvement."""

    SUPPORTED_EXTENSIONS = {'.py', '.sh', '.js', '.ts', '.go', '.rb'}

    def __init__(self, repo_root: str = '.', agents_only: bool = False,
                 max_files: int = None, loop: int = 1):
        self.repo_root = self._find_repo_root(Path(repo_root))
        self.agents_only = agents_only
        self.max_files = max_files
        self.loop = loop
        self.ignored_patterns = load_codeignore(self.repo_root)

    def _find_repo_root(self, start_path: Path) -> Path:
        """Find the repository root by looking for .git directory or other markers."""
        current = start_path.resolve()

        # Walk up the directory tree looking for repository markers
        for path in [current] + list(current.parents):
            if (path / '.git').exists() or (path / 'README.md').exists() or \
                    (path / 'package.json').exists():
                return path

        # If no markers found, return the original path
        return start_path

    def find_code_files(self) -> List[Path]:
        """Recursively find all supported code files."""
        code_files = []
        for ext in self.SUPPORTED_EXTENSIONS:
            code_files.extend(self.repo_root.rglob(f'*{ext}'))

        # Filter to scripts/agent directory if agents_only is True
        if self.agents_only:
            scripts_agent_dir = self.repo_root / 'scripts' / 'agent'
            code_files = [f for f in code_files if f.is_relative_to(scripts_agent_dir)]

        code_files = sorted([f for f in code_files if not self._is_ignored(f)])

        if self.max_files:
            code_files = code_files[:self.max_files]

        return code_files

    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored."""
        path_str = str(path)
        return any(fnmatch.fnmatch(path_str, pattern) or
                   fnmatch.fnmatch(path.name, pattern) or
                   any(fnmatch.fnmatch(part, pattern) for part in path.parts)
                   for pattern in self.ignored_patterns)

    def run_stats_update(self, files: List[Path]):
        """Run stats update."""
        file_paths = [str(f) for f in files]
        cmd = [sys.executable, str(self.repo_root / 'scripts/agent/agent-stats.py'),
               '--files'] + file_paths
        subprocess.run(cmd, cwd=self.repo_root)

    def run_tests(self, code_file: Path):
        """Run tests for the code file."""
        # Look for test_{filename}.py (pytest convention)
        test_name = f"test_{code_file.stem}.py"
        tests_file = code_file.parent / test_name
        if tests_file.exists():
            print(f"[Agent] Running tests for {code_file.name}...")
            cmd = [sys.executable, '-m', 'pytest', str(tests_file), '-v']
            result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Tests failed for {code_file.name}:")
                print(result.stdout)
                print(result.stderr)
            else:
                print(f"Tests passed for {code_file.name}")
        else:
            print(f"[Agent] No tests file found for {code_file.name}")

    def update_errors_improvements(self, code_file: Path) -> bool:
        """Update errors and improvements."""
        base = code_file.stem
        dir_path = code_file.parent

        errors_file = dir_path / f"{base}.errors.md"
        improvements_file = dir_path / f"{base}.improvements.md"

        changes_made = False

        # Create errors file if it doesn't exist
        if not errors_file.exists():
            content = f"# Errors\n\nNo errors reported for {code_file.name}.\n"
            errors_file.write_text(fix_markdown_content(content), encoding='utf-8')
            print(f"[Agent] Created {errors_file.relative_to(self.repo_root)}")
            changes_made = True

        # Update errors
        prompt = f"Analyze and improve the error report for {code_file.name}"
        cmd = [sys.executable, str(self.repo_root / 'scripts/agent/agent-errors.py'),
               '--context', str(errors_file), '--prompt', prompt]
        result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)
        if "No changes made" not in result.stdout and "No changes made" not in result.stderr:
            changes_made = True

        # Create improvements file if it doesn't exist
        if not improvements_file.exists():
            content = f"# Improvements\n\nNo improvements suggested for {code_file.name}.\n"
            improvements_file.write_text(
                fix_markdown_content(content),
                encoding='utf-8'
            )
            print(f"[Agent] Created {improvements_file.relative_to(self.repo_root)}")
            changes_made = True

        # Update improvements
        prompt = f"Suggest and improve improvements for {code_file.name}"
        cmd = [sys.executable, str(self.repo_root / 'scripts/agent/agent-improvements.py'),
               '--context', str(improvements_file), '--prompt', prompt]
        result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)
        if "No changes made" not in result.stdout and "No changes made" not in result.stderr:
            changes_made = True

        return changes_made

    def update_code(self, code_file: Path) -> bool:
        """Update the code file."""
        prompt = (f"Improve the code in {code_file.name} based on its context, "
                  f"errors, and improvements")
        cmd = [sys.executable, str(self.repo_root / 'scripts/agent/agent-coder.py'),
               '--context', str(code_file), '--prompt', prompt]
        result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True,
                                text=True)
        return ("No changes made" not in result.stdout and
                "No changes made" not in result.stderr)

    def update_changelog_context_tests(self, code_file: Path) -> bool:
        """Update changelog, context, and tests."""
        base = code_file.stem
        dir_path = code_file.parent

        changes_file = dir_path / f"{base}.changes.md"
        context_file = dir_path / f"{base}.description.md"
        tests_file = dir_path / f"test_{base}.py"

        changes_made = False

        # Create changelog file if it doesn't exist
        if not changes_file.exists():
            content = f"# Changelog\n\n- Initial version of {code_file.name}\n"
            changes_file.write_text(fix_markdown_content(content), encoding='utf-8')
            print(f"[Agent] Created {changes_file.relative_to(self.repo_root)}")
            changes_made = True

        # Update changelog
        prompt = f"Update the changelog for {code_file.name} with recent changes"
        cmd = [sys.executable, str(self.repo_root / 'scripts/agent/agent-changes.py'),
               '--context', str(changes_file), '--prompt', prompt]
        result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)
        if "No changes made" not in result.stdout and "No changes made" not in result.stderr:
            changes_made = True

        # Create context file if it doesn't exist
        if not context_file.exists():
            content = f"# Description\n\n{code_file.name} - Description to be added.\n"
            context_file.write_text(fix_markdown_content(content), encoding='utf-8')
            print(f"[Agent] Created {context_file.relative_to(self.repo_root)}")
            changes_made = True

        # Update context
        prompt = f"Update the description for {code_file.name} based on current code"
        cmd = [sys.executable, str(self.repo_root / 'scripts/agent/agent-context.py'),
               '--context', str(context_file), '--prompt', prompt]
        result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)
        if "No changes made" not in result.stdout and "No changes made" not in result.stderr:
            changes_made = True

        # Create tests file if it doesn't exist
        if not tests_file.exists():
            content = f"""# Tests for {code_file.name}
import pytest

def test_placeholder():
    \"\"\"Placeholder test - replace with actual tests.\"\"\"
    assert True

# Add more tests here
"""
            tests_file.write_text(fix_markdown_content(content), encoding='utf-8')
            print(f"[Agent] Created {tests_file.relative_to(self.repo_root)}")
            changes_made = True

        # Update tests
        prompt = f"Update and expand the test suite for {code_file.name}"
        cmd = [sys.executable, str(self.repo_root / 'scripts/agent/agent-tests.py'),
               '--context', str(tests_file), '--prompt', prompt]
        result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)
        if "No changes made" not in result.stdout and "No changes made" not in result.stderr:
            changes_made = True

        return changes_made

    def process_file(self, code_file: Path):
        """Process a single code file through the improvement loop."""
        print(f"[Agent] Processing {code_file.relative_to(self.repo_root)}...")

        max_iterations = 1
        iteration = 0
        all_fixed = False

        while not all_fixed and iteration < max_iterations:
            iteration += 1
            print(f"[Agent] Iteration {iteration} for {code_file.name}")

            # Track if any changes were made in this iteration
            changes_made = False
            base = code_file.stem
            dir_path = code_file.parent

            context_file = dir_path / f"{base}.description.md"
            changes_file = dir_path / f"{base}.changes.md"
            errors_file = dir_path / f"{base}.errors.md"
            improvements_file = dir_path / f"{base}.improvements.md"

            # Check if all supporting files exist and have content beyond AI suggestions
            files_ready = (
                context_file.exists() and len(context_file.read_text().strip()) > 100 and
                changes_file.exists() and len(changes_file.read_text().strip()) > 100 and
                errors_file.exists() and len(errors_file.read_text().strip()) > 100 and
                improvements_file.exists() and len(improvements_file.read_text().strip()) > 100
            )

            if not files_ready and iteration == 1:
                print(f"[Agent] Creating initial supporting files for {code_file.name}")

            # Give a Stats update
            self.run_stats_update([code_file])

            # Run the Tests on the Codefile
            self.run_tests(code_file)

            # Update Errors, Improvements
            changes_made |= self.update_errors_improvements(code_file)

            # Update Code
            changes_made |= self.update_code(code_file)

            # Update Changelog, Context, Tests
            changes_made |= self.update_changelog_context_tests(code_file)

            # Check if all is marked as fixed (no more changes needed)
            if not changes_made:
                all_fixed = True
                print(f"[Agent] No changes made in iteration {iteration}, marking as fixed")
            else:
                print(f"[Agent] Changes made in iteration {iteration}, continuing...")

        if iteration >= max_iterations:
            print(f"[Agent] Reached maximum iterations ({max_iterations}) for {code_file.name}")

        print(f"[Agent] Completed processing {code_file.name} in {iteration} iterations")

        # git add -A, git commit, git push
        print(f"[Agent] Committing changes for {code_file.name}")
        try:
            # git add -A
            subprocess.run(['git', 'add', '-A'], cwd=self.repo_root, check=True)

            # git commit
            commit_msg = (
                f"Agent improvements for {code_file.name}"
            )
            result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"[Agent] Committed changes for {code_file.name}")
                # git push
                push_result = subprocess.run(['git', 'push'], cwd=self.repo_root,
                                             capture_output=True, text=True)
                if push_result.returncode == 0:
                    print(f"[Agent] Pushed changes for {code_file.name}")
                else:
                    print(f"[Agent] Failed to push changes: {push_result.stderr}")
            else:
                print(f"[Agent] No changes to commit for {code_file.name}")

        except subprocess.CalledProcessError as e:
            print(f"[Agent] Git operation failed for {code_file.name}: {e}")
        except FileNotFoundError:
            print(f"[Agent] Git not available for {code_file.name}")

    def run(self):
        """Run the main agent loop."""
        code_files = self.find_code_files()
        print(f"[Agent] Found {len(code_files)} code files to process")

        for loop_iteration in range(1, self.loop + 1):
            print(f"[Agent] Starting loop iteration {loop_iteration}/{self.loop}")

            for code_file in code_files:
                self.process_file(code_file)

            print(f"[Agent] Completed loop iteration {loop_iteration}/{self.loop}")

        # Final stats update
        print("[Agent] Final stats:")
        self.run_stats_update(code_files)


def main():
    parser = argparse.ArgumentParser(
        description='Agent: Orchestrates code improvement agents'
    )
    parser.add_argument('--dir', default='.', help='Directory to process (default: .)')
    parser.add_argument('--agents-only', action='store_true',
                        help='Only process files in the scripts/agent directory')
    parser.add_argument('--max-files', type=int, help='Maximum number of files to process')
    parser.add_argument('--loop', type=int, default=1,
                        help='Number of times to loop through all files (default: 1)')
    args = parser.parse_args()

    agent = Agent(repo_root=args.dir, agents_only=args.agents_only,
                  max_files=args.max_files, loop=args.loop)
    agent.run()


if __name__ == '__main__':
    main()
