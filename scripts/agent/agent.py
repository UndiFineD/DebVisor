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
import os
import logging
from pathlib import Path
from typing import List, Set, Optional
import argparse
import fnmatch
import importlib.util

# Import markdown fixing functionality
def _load_fix_markdown_content():
    fix_dir = Path(__file__).parent.parent / 'fix'
    spec = importlib.util.spec_from_file_location("fix_markdown_lint", str(fix_dir / "fix_markdown_lint.py"))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules["fix_markdown_lint"] = module
        spec.loader.exec_module(module)
        return module.fix_markdown_content
    return lambda x: x  # Fallback

fix_markdown_content = _load_fix_markdown_content()


def setup_logging(verbosity: str) -> None:
    """Configure logging based on verbosity level."""
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
    level = levels.get(verbosity.lower(), logging.INFO)
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


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
            logging.warning(f"Could not read .codeignore file: {e}")
    return set()


class Agent:
    """Main agent that orchestrates sub-agents for code improvement."""
    SUPPORTED_EXTENSIONS = {'.py', '.sh', '.js', '.ts', '.go', '.rb'}

    def __init__(self, repo_root: str = '.', agents_only: bool = False,
            max_files: Optional[int] = None, loop: int = 1, skip_code_update: bool = False,
            no_git: bool = False):
        self.repo_root = self._find_repo_root(Path(repo_root))
        if not self.repo_root.exists():
            raise FileNotFoundError(f"Repository root not found: {self.repo_root}")
        self.agents_only = agents_only
        self.max_files = max_files
        self.loop = loop
        self.skip_code_update = skip_code_update
        self.no_git = no_git
        self.ignored_patterns = load_codeignore(self.repo_root)

    def _run_command(self, cmd: List[str], timeout: int = 120) -> subprocess.CompletedProcess:
        """Run a command with timeout and error handling."""
        try:
            return subprocess.run(
                cmd,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                check=False
            )
        except subprocess.TimeoutExpired:
            logging.error(f"Command timed out: {' '.join(cmd[:3])}...")
            return subprocess.CompletedProcess(cmd, returncode=-1, stdout="", stderr="Timeout expired")
        except Exception as e:
            logging.error(f"Command failed: {e}")
            return subprocess.CompletedProcess(cmd, returncode=-1, stdout="", stderr=str(e))

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
        return any(
            fnmatch.fnmatch(path_str, pattern) or
            fnmatch.fnmatch(path.name, pattern) or
            any(fnmatch.fnmatch(part, pattern) for part in path.parts)
            for pattern in self.ignored_patterns)

    def run_stats_update(self, files: List[Path]) -> None:
        """Run stats update."""
        file_paths = [str(f) for f in files]
        cmd = [
            sys.executable,
            str(self.repo_root / 'scripts/agent/agent-stats.py'),
            '--files'] + file_paths
        self._run_command(cmd)

    def run_tests(self, code_file: Path) -> None:
        """Run tests for the code file."""
        # Look for test_{filename}.py (pytest convention)
        test_name = f"test_{code_file.stem}.py"
        tests_file = code_file.parent / test_name
        if tests_file.exists():
            logging.info(f"Running tests for {code_file.name}...")
            cmd = [sys.executable, '-m', 'pytest', str(tests_file), '-v']
            result = self._run_command(cmd)
            if result.returncode != 0:
                logging.warning(f"Tests failed for {code_file.name}:")
                logging.warning(result.stdout)
                logging.warning(result.stderr)
            else:
                logging.info(f"Tests passed for {code_file.name}")
        else:
            logging.debug(f"No tests file found for {code_file.name}")

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
            logging.info(f"Created {errors_file.relative_to(self.repo_root)}")
            changes_made = True
        # Update errors
        prompt = f"Analyze and improve the error report for {code_file.name}"
        cmd = [
            sys.executable,
            str(self.repo_root / 'scripts/agent/agent-errors.py'),
            '--context', str(errors_file),
            '--prompt', prompt
            ]
        result = self._run_command(cmd)
        
        # Check if changes were made based on output
        stdout_ok = result.stdout and "No changes made" not in result.stdout
        stderr_ok = not result.stderr or "No changes made" not in result.stderr
        
        if stdout_ok and stderr_ok:
            changes_made = True
        # Create improvements file if it doesn't exist
        if not improvements_file.exists():
            content = f"# Improvements\n\nNo improvements suggested for {code_file.name}.\n"
            improvements_file.write_text(
                fix_markdown_content(content),
                encoding='utf-8'
            )
            logging.info(f"Created {improvements_file.relative_to(self.repo_root)}")
            changes_made = True
        # Update improvements
        prompt = f"Suggest and improve improvements for {code_file.name}"
        cmd = [
            sys.executable,
            str(self.repo_root / 'scripts/agent/agent-improvements.py'),
            '--context', str(improvements_file),
            '--prompt', prompt
            ]
        result = self._run_command(cmd)
        
        # Check if changes were made based on output
        stdout_ok = result.stdout and "No changes made" not in result.stdout
        stderr_ok = not result.stderr or "No changes made" not in result.stderr
        
        if stdout_ok and stderr_ok:
            changes_made = True
        return changes_made

    def _get_pending_improvements(self, improvements_file: Path) -> List[str]:
        """Extract pending improvements from the improvements file."""
        if not improvements_file.exists():
            return []
        try:
            content = improvements_file.read_text(encoding='utf-8')
            lines = content.splitlines()
            pending = []
            import re
            # Match "1. ", "1) ", "- [ ]", "- ", "* "
            list_pattern = re.compile(r'^(\d+[\.\)]|\*|\-)\s+(\[ \]\s+)?(.*)')
            
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                
                # Skip checked items
                if '[x]' in stripped or '[Fixed]' in stripped:
                    continue
                
                match = list_pattern.match(stripped)
                if match:
                    item_text = match.group(3).strip()
                    # Filter out some obvious non-tasks or headers that look like lists
                    if item_text.lower().startswith('current strengths'):
                        continue
                    if len(item_text) > 5:
                        pending.append(item_text)
            return pending
        except Exception as e:
            logging.warning(f"Failed to read improvements file: {e}")
            return []

    def _mark_improvements_fixed(self, improvements_file: Path, fixed_items: List[str]) -> None:
        """Mark improvements as fixed in the file."""
        if not improvements_file.exists() or not fixed_items:
            return
        try:
            content = improvements_file.read_text(encoding='utf-8')
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                updated = False
                for item in fixed_items:
                    if item in line:
                        if '- [ ]' in line:
                            new_lines.append(line.replace('- [ ]', '- [x]'))
                            updated = True
                            break
                        elif not '[x]' in line and not '[Fixed]' in line:
                            new_lines.append(line + " [Fixed]")
                            updated = True
                            break
                if not updated:
                    new_lines.append(line)
            improvements_file.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
            logging.info(f"Marked {len(fixed_items)} improvements as fixed in {improvements_file.name}")
        except Exception as e:
            logging.warning(f"Failed to update improvements file: {e}")

    def _log_changes(self, changes_file: Path, fixed_items: List[str]) -> None:
        """Log fixed items to the changes file."""
        if not changes_file.exists() or not fixed_items:
            return
        try:
            content = changes_file.read_text(encoding='utf-8')
            new_entries = "\n".join([f"- Fixed: {item}" for item in fixed_items])
            # Append to the end or after the header
            if "# Changelog" in content:
                # Just append to end for now
                new_content = content.rstrip() + "\n\n" + new_entries + "\n"
            else:
                new_content = content + "\n" + new_entries + "\n"
            changes_file.write_text(new_content, encoding='utf-8')
            logging.info(f"Logged {len(fixed_items)} fixes to {changes_file.name}")
        except Exception as e:
            logging.warning(f"Failed to update changes file: {e}")

    def update_code(self, code_file: Path) -> bool:
        """Update the code file."""
        base = code_file.stem
        dir_path = code_file.parent
        improvements_file = dir_path / f"{base}.improvements.md"
        changes_file = dir_path / f"{base}.changes.md"
        pending_improvements = self._get_pending_improvements(improvements_file)
        # Limit to top 3 to avoid overwhelming
        target_improvements = pending_improvements[:3]
        if target_improvements:
            improvements_text = "\n".join([f"- {item}" for item in target_improvements])
            prompt = (
                f"Improve the code in {code_file.name} by implementing the following specific improvements:\n"
                f"{improvements_text}\n\n"
                f"Ensure the code remains functional and follows best practices."
            )
            logging.info(f"Targeting {len(target_improvements)} improvements for {code_file.name}")
        else:
            prompt = (
                f"Improve the code in {code_file.name} based on its context, "
                f"errors, and improvements")
        cmd = [
            sys.executable,
            str(self.repo_root / 'scripts/agent/agent-coder.py'),
            '--context', str(code_file),
            '--prompt', prompt
            ]
        result = self._run_command(cmd, timeout=300)
        
        # Check if changes were made based on output
        stdout_ok = result.stdout and "No changes made" not in result.stdout
        stderr_ok = not result.stderr or "No changes made" not in result.stderr
        
        changes_made = stdout_ok and stderr_ok
        if changes_made and target_improvements:
            # Assume targeted improvements were fixed if code changed
            self._mark_improvements_fixed(improvements_file, target_improvements)
            self._log_changes(changes_file, target_improvements)
        return changes_made

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
            logging.info(f"Created {changes_file.relative_to(self.repo_root)}")
            changes_made = True
        # Update changelog
        prompt = f"Update the changelog for {code_file.name} with recent changes"
        cmd = [
            sys.executable,
            str(self.repo_root / 'scripts/agent/agent-changes.py'),
            '--context', str(changes_file),
            '--prompt', prompt
            ]
        result = self._run_command(cmd)
        
        # Check if changes were made based on output
        stdout_ok = result.stdout and "No changes made" not in result.stdout
        stderr_ok = not result.stderr or "No changes made" not in result.stderr
        
        if stdout_ok and stderr_ok:
            changes_made = True
        # Create context file if it doesn't exist
        if not context_file.exists():
            content = f"# Description\n\n{code_file.name} - Description to be added.\n"
            context_file.write_text(fix_markdown_content(content), encoding='utf-8')
            logging.info(f"Created {context_file.relative_to(self.repo_root)}")
            changes_made = True
        # Update context
        prompt = f"Update the description for {code_file.name} based on current code"
        cmd = [
            sys.executable,
            str(self.repo_root / 'scripts/agent/agent-context.py'),
            '--context', str(context_file),
            '--prompt', prompt
            ]
        result = self._run_command(cmd)
        if result.stdout and "No changes made" not in result.stdout and (not result.stderr or "No changes made" not in result.stderr):
            changes_made = True
        # Create tests file if it doesn't exist and the code file is not already a test file
        if not tests_file.exists() and not base.startswith('test_'):
            content = f"""# Tests for {code_file.name}
import pytest

def test_placeholder():
    \"\"\"Placeholder test - replace with actual tests.\"\"\"
    assert True

## Add more tests here
"""
            # Tests are Python files; do not run markdown normalization on them
            tests_file.write_text(content, encoding='utf-8')
            logging.info(f"Created {tests_file.relative_to(self.repo_root)}")
            changes_made = True
        # Update tests - if this is a test file, update it directly; otherwise update the associated test file
        if base.startswith('test_'):
            # This is already a test file, update it directly
            test_file_to_update = code_file
            prompt = f"Update and expand the test suite for {base.replace('test_', '')}"
        else:
            # This is a code file, update its associated test file
            test_file_to_update = tests_file
            prompt = f"Update and expand the test suite for {code_file.name}"
        cmd = [
            sys.executable,
            str(self.repo_root / 'scripts/agent/agent-tests.py'),
            '--context', str(test_file_to_update),
            '--prompt', prompt,
        ]
        result = self._run_command(cmd)
        if result.stdout and "No changes made" not in result.stdout and (not result.stderr or "No changes made" not in result.stderr):
            changes_made = True
        return changes_made

    def _check_files_ready(self, code_file: Path) -> bool:
        """Check if all supporting files exist and have content."""
        base = code_file.stem
        dir_path = code_file.parent
        context_file = dir_path / f"{base}.description.md"
        changes_file = dir_path / f"{base}.changes.md"
        errors_file = dir_path / f"{base}.errors.md"
        improvements_file = dir_path / f"{base}.improvements.md"
        return (
            context_file.exists() and len(context_file.read_text(encoding='utf-8').strip()) > 100 and
            changes_file.exists() and len(changes_file.read_text(encoding='utf-8').strip()) > 100 and
            errors_file.exists() and len(errors_file.read_text(encoding='utf-8').strip()) > 100 and
            improvements_file.exists() and len(improvements_file.read_text(encoding='utf-8').strip()) > 100
        )

    def _perform_iteration(self, code_file: Path) -> bool:
        """Perform one iteration of improvements on the code file."""
        changes_made = False
        # Give a Stats update
        self.run_stats_update([code_file])
        # Run the Tests on the Codefile
        if not self.skip_code_update:
            self.run_tests(code_file)
        # Update Errors, Improvements
        changes_made |= self.update_errors_improvements(code_file)
        # Update Code
        if not self.skip_code_update:
            changes_made |= self.update_code(code_file)
        # Update Changelog, Context, Tests
        changes_made |= self.update_changelog_context_tests(code_file)
        return changes_made

    def _commit_and_push(self, code_file: Path):
        """Commit and push changes for the code file."""
        if self.no_git:
            logging.info(f"Skipping git operations for {code_file.name} (--no-git)")
            return

        logging.info(f"Committing changes for {code_file.name}")
        try:
            # git add -A
            self._run_command(['git', 'add', '-A'])
            # git commit
            commit_msg = f"Agent improvements for {code_file.name}"
            result = self._run_command(['git', 'commit', '-m', commit_msg])
            if result.returncode == 0:
                logging.info(f"Committed changes for {code_file.name}")
                # git push
                push_result = self._run_command(['git', 'push'])
                if push_result.returncode == 0:
                    logging.info(f"Pushed changes for {code_file.name}")
                else:
                    logging.error(f"Failed to push changes: {push_result.stderr}")
            else:
                logging.info(f"No changes to commit for {code_file.name}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Git operation failed for {code_file.name}: {e}")
        except FileNotFoundError:
            logging.error(f"Git not available for {code_file.name}")

    def process_file(self, code_file: Path):
        """Process a single code file through the improvement loop."""
        logging.info(f"Processing {code_file.relative_to(self.repo_root)}...")
        max_iterations = 1
        iteration = 0
        all_fixed = False
        while not all_fixed and iteration < max_iterations:
            iteration += 1
            logging.info(f"Iteration {iteration} for {code_file.name}")
            files_ready = self._check_files_ready(code_file)
            if not files_ready and iteration == 1:
                logging.info(f"Creating initial supporting files for {code_file.name}")
            changes_made = self._perform_iteration(code_file)
            # Check if all is marked as fixed (no more changes needed)
            if not changes_made:
                all_fixed = True
                logging.info(f"No changes made in iteration {iteration}, marking as fixed")
            else:
                logging.info(f"Changes made in iteration {iteration}, continuing...")
        if iteration >= max_iterations:
            logging.info(f"Reached maximum iterations ({max_iterations}) for {code_file.name}")
        logging.info(f"Completed processing {code_file.name} in {iteration} iterations")
        self._commit_and_push(code_file)

    def run(self):
        """Run the main agent loop."""
        code_files = self.find_code_files()
        logging.info(f"Found {len(code_files)} code files to process")
        for loop_iteration in range(1, self.loop + 1):
            logging.info(f"Starting loop iteration {loop_iteration}/{self.loop}")
            for code_file in code_files:
                self.process_file(code_file)
            logging.info(f"Completed loop iteration {loop_iteration}/{self.loop}")
        # Final stats update
        logging.info("Final stats:")
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
    parser.add_argument('--skip-code-update', action='store_true',
                        help='Skip code updates and tests, only update documentation')
    parser.add_argument('--verbose', default='normal',
                        help='Verbosity level: quiet, minimal, normal, elaborate (or 0-3)')
    parser.add_argument('--no-git', action='store_true',
                        help='Skip git commit and push operations')
    args = parser.parse_args()
    setup_logging(args.verbose)
    os.environ['DV_AGENT_VERBOSITY'] = args.verbose
    agent = Agent(
        repo_root=args.dir,
        agents_only=args.agents_only,
        max_files=args.max_files, loop=args.loop,
        skip_code_update=args.skip_code_update,
        no_git=args.no_git
        )
    agent.run()


if __name__ == '__main__':
    main()
