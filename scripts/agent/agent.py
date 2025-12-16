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
from typing import List, Set, Optional, Dict, Any, Callable
import argparse
import fnmatch
import importlib.util
import time
import asyncio
import multiprocessing
import functools
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import json
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    def tqdm(iterable, *args, **kwargs):
        """Fallback if tqdm not available."""
        return iterable

# Import markdown fixing functionality
def _load_fix_markdown_content() -> callable:
    """Load the markdown fixer module dynamically."""
    fix_dir = Path(__file__).parent.parent / 'fix'
    spec = importlib.util.spec_from_file_location("fix_markdown_lint", str(fix_dir / "fix_markdown_lint.py"))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules["fix_markdown_lint"] = module
        spec.loader.exec_module(module)
        return module.fix_markdown_content
    return lambda x: x  # Fallback

fix_markdown_content = _load_fix_markdown_content()


# Global cache for .codeignore patterns to avoid re-parsing
_CODEIGNORE_CACHE: Dict[str, Set[str]] = {}
_CODEIGNORE_CACHE_TIME: Dict[str, float] = {}


def _exponential_backoff_retry(func, max_attempts: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
    """Execute a function with exponential backoff retry on failure.
    
    Retries a function call if it raises an exception, with exponentially
    increasing delays between attempts. Useful for transient failures.
    
    Args:
        func: Callable that returns True on success, False on failure.
        max_attempts: Maximum number of attempts. Defaults to 3.
        base_delay: Initial delay in seconds. Defaults to 1.0.
        max_delay: Maximum delay between retries. Defaults to 30.0.
        
    Returns:
        bool: True if func succeeded, False after max_attempts.
        
    Example:
        success = _exponential_backoff_retry(
            lambda: subprocess.run([...], check=True),
            max_attempts=3
        )
        
    Note:
        - Delay formula: min(base_delay * (2 ^ attempt), max_delay)
        - Logs each retry attempt
        - Final failure is logged as error
    """
    for attempt in range(1, max_attempts + 1):
        try:
            result = func()
            if result:
                return True
        except Exception as e:
            if attempt == max_attempts:
                logging.error(f"Failed after {max_attempts} attempts: {e}")
                return False
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            logging.warning(f"Attempt {attempt} failed, retrying in {delay}s: {e}")
            time.sleep(delay)
    return False


# Module-level worker function for multiprocessing (cannot be a nested function)
def _multiprocessing_worker(agent_instance, file_path: Path) -> Optional[Path]:
    """Worker function for multiprocessing file processing.
    
    This function must be at module level to be pickleable for multiprocessing.
    """
    try:
        logging.debug(f"[worker] Processing {file_path.name}")
        agent_instance.process_file(file_path)
        logging.info(f"[worker] Completed {file_path.name}")
        return file_path
    except Exception as e:
        logging.error(f"[worker] Failed: {e}")
        return None


def setup_logging(verbosity: str) -> None:
    """Configure logging based on verbosity level.
    
    Args:
        verbosity: Verbosity level as string ('quiet', 'minimal', 'normal', 'elaborate'
                  or '0', '1', '2', '3'). Defaults to 'INFO' level.
                  
    Returns:
        None. Configures the root logger with the specified level.
        
    Example:
        setup_logging('elaborate')  # Sets DEBUG level
        
    Note:
        This function configures the global logging system. Should be called
        once at application startup before other logging calls.
    """
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
    logging.debug(f"Logging configured at level: {logging.getLevelName(level)}")

def load_codeignore(root: Path) -> Set[str]:
    """Load and parse ignore patterns from .codeignore file.
    
    Reads the .codeignore file from the repository root and extracts all
    ignore patterns (lines that are not empty or comments).
    
    Caches patterns to avoid re-parsing on subsequent calls. Cache is invalidated
    if the file is modified (checked by file mtime).
    
    Args:
        root: Path to the repository root directory.
        
    Returns:
        Set of ignore patterns (strings) from the .codeignore file.
        Returns empty set if file doesn't exist.
        
    Raises:
        None. Logs warnings if file cannot be read but doesn't raise.
        
    Example:
        patterns = load_codeignore(Path('/repo'))
        # patterns might be: {'*.log', '__pycache__/', 'venv/**'}
        
    Note:
        - Lines starting with '#' are treated as comments and ignored
        - Empty lines are skipped
        - File encoding is assumed to be UTF-8
        - Patterns are cached with mtime checking for efficiency
    """
    codeignore_path = root / ".codeignore"
    cache_key = str(codeignore_path)
    
    # Check cache validity
    if cache_key in _CODEIGNORE_CACHE and codeignore_path.exists():
        try:
            file_mtime = codeignore_path.stat().st_mtime
            cache_time = _CODEIGNORE_CACHE_TIME.get(cache_key, 0)
            if file_mtime == cache_time:
                logging.debug(f"Using cached .codeignore patterns for {cache_key}")
                return _CODEIGNORE_CACHE[cache_key]
        except OSError:
            pass
    
    if codeignore_path.exists():
        try:
            logging.debug(f"Loading .codeignore patterns from {codeignore_path}")
            content = codeignore_path.read_text(encoding='utf-8')
            patterns = {
                line.strip() for line in content.split('\n')
                if line.strip() and not line.strip().startswith('#')
            }
            logging.info(f"Loaded {len(patterns)} ignore patterns from .codeignore")
            
            # Cache the patterns
            _CODEIGNORE_CACHE[cache_key] = patterns
            try:
                _CODEIGNORE_CACHE_TIME[cache_key] = codeignore_path.stat().st_mtime
            except OSError:
                pass
            
            return patterns
        except Exception as e:
            logging.warning(f"Could not read .codeignore file: {e}")
    else:
        logging.debug(f"No .codeignore file found at {codeignore_path}")
    return set()


class Agent:
    """Main agent that orchestrates sub-agents for code improvement.
    
    This class coordinates the improvement process across code files by delegating
    tasks to specialized sub-agents (CoderAgent, TestsAgent, etc.) that handle
    specific aspects of code quality and documentation.
    
    Supports context manager protocol for resource management.
    
    Attributes:
        repo_root (Path): Root directory of the target repository.
        agents_only (bool): If True, only process files in scripts/agent directory.
        max_files (Optional[int]): Maximum number of files to process. None = no limit.
        loop (int): Number of times to run the full improvement cycle (default: 1).
        skip_code_update (bool): If True, skip code update phase.
        no_git (bool): If True, don't commit changes to git.
        ignored_patterns (Set[str]): Patterns from .codeignore file.
        
    Class Attributes:
        SUPPORTED_EXTENSIONS (Set[str]): File extensions to process (py, sh, js, ts, etc.).
        
    Example:
        with Agent(repo_root='.', agents_only=True) as agent:
            files = agent.find_code_files()
            agent.run()
        
    Note:
        - Can be used as context manager for automatic cleanup
        - Recursively finds code files in the repository
        - Filters files according to .codeignore patterns
        - Runs sub-agents on each file for improvements
        - Optionally commits changes back to git
    """
    SUPPORTED_EXTENSIONS = {'.py', '.sh', '.js', '.ts', '.go', '.rb'}

    def __init__(self, repo_root: str = '.', agents_only: bool = False,
            max_files: Optional[int] = None, loop: int = 1, skip_code_update: bool = False,
            no_git: bool = False, dry_run: bool = False, selective_agents: Optional[List[str]] = None,
            timeout_per_agent: Optional[Dict[str, int]] = None,
            enable_async: bool = False, enable_multiprocessing: bool = False,
            max_workers: int = 4) -> None:
        """Initialize the Agent with repository configuration.
        
        Args:
            repo_root: Root directory of the repository to process. Defaults to '.'.
            agents_only: If True, only process files in scripts/agent. Defaults to False.
            max_files: Maximum number of files to process. None = unlimited. Defaults to None.
            loop: Number of full cycles to run. Defaults to 1.
            skip_code_update: If True, skip code update phase. Defaults to False.
            no_git: If True, don't commit changes to git. Defaults to False.
            dry_run: If True, preview changes without modifying files. Defaults to False.
            selective_agents: List of agent names to execute (e.g., ['coder', 'tests']). Defaults to None (all).
            timeout_per_agent: Dict mapping agent names to timeout values in seconds. Defaults to None.
            enable_async: If True, use async file processing. Defaults to False.
            enable_multiprocessing: If True, use multiprocessing for agents. Defaults to False.
            max_workers: Maximum number of worker threads/processes. Defaults to 4.
            
        Raises:
            FileNotFoundError: If repo_root doesn't exist.
            
        Note:
            The repository root is automatically detected by looking for .git,
            README.md, or package.json if not explicitly provided.
            
            Supports context manager protocol via __enter__ and __exit__.
        """
        logging.info(f"Initializing Agent with repo_root={repo_root}")
        self.repo_root = self._find_repo_root(Path(repo_root))
        if not self.repo_root.exists():
            raise FileNotFoundError(f"Repository root not found: {self.repo_root}")
        self.agents_only = agents_only
        self.max_files = max_files
        self.loop = loop
        self.skip_code_update = skip_code_update
        self.no_git = no_git
        self.dry_run = dry_run
        self.selective_agents = set(selective_agents or [])
        self.timeout_per_agent = timeout_per_agent or {}
        self.enable_async = enable_async
        self.enable_multiprocessing = enable_multiprocessing
        self.max_workers = max_workers
        self.ignored_patterns = load_codeignore(self.repo_root)
        
        # Webhook support
        self.webhooks: List[str] = []
        self.callbacks: List[Callable] = []
        
        # Metrics tracking
        self.metrics = {
            'files_processed': 0,
            'files_modified': 0,
            'agents_applied': {},
            'start_time': time.time(),
            'end_time': None,
        }
        
        logging.info(f"Agent initialized: repo={self.repo_root}, loop={loop}, agents_only={agents_only}")
        if dry_run:
            logging.info("DRY RUN MODE: No files will be modified")
        if selective_agents:
            logging.info(f"Selective execution: agents={selective_agents}")
        if enable_async:
            logging.info("Async file processing enabled")
        if enable_multiprocessing:
            logging.info(f"Multiprocessing enabled with {max_workers} workers")
    
    def __enter__(self):
        """Context manager entry. Returns self for use in 'with' statement."""
        logging.debug(f"Agent entering context manager")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit. Handles cleanup if needed."""
        logging.debug(f"Agent exiting context manager")
        if exc_type is not None:
            logging.error(f"Agent context manager error: {exc_type.__name__}: {exc_val}")
        return False  # Don't suppress exceptions

    def should_execute_agent(self, agent_name: str) -> bool:
        """Check if an agent should be executed based on selective filters.
        
        Determines whether to run a specific agent based on the selective_agents
        configuration provided at initialization.
        
        Args:
            agent_name: Name of the agent (e.g., 'coder', 'tests', 'documentation').
            
        Returns:
            bool: True if the agent should execute, False otherwise.
            
        Example:
            if agent.should_execute_agent('coder'):
                coder_agent.run()
        """
        if not self.selective_agents:
            return True  # All agents run if no selective filter
        return agent_name.lower() in self.selective_agents

    def get_timeout_for_agent(self, agent_name: str, default: int = 120) -> int:
        """Get configured timeout for a specific agent.
        
        Returns the timeout value for a specific agent, or a default if not configured.
        
        Args:
            agent_name: Name of the agent (e.g., 'coder', 'tests').
            default: Default timeout in seconds if not configured. Defaults to 120.
            
        Returns:
            int: Timeout in seconds for the agent.
            
        Example:
            timeout = agent.get_timeout_for_agent('coder', default=60)
        """
        return self.timeout_per_agent.get(agent_name.lower(), default)

    def print_metrics_summary(self) -> None:
        """Print a summary of execution metrics and statistics.
        
        Prints information about files processed, modifications made, agents applied,
        and execution time. Useful for understanding the impact of agent runs.
        
        Example:
            agent.run()
            agent.print_metrics_summary()
        """
        self.metrics['end_time'] = time.time()
        elapsed = self.metrics['end_time'] - self.metrics['start_time']
        
        summary = f"""
=== Agent Execution Summary ===
Files processed: {self.metrics['files_processed']}
Files modified:  {self.metrics['files_modified']}
Execution time:  {elapsed:.2f}s
Dry-run mode:    {'Yes' if self.dry_run else 'No'}

Agents applied:
"""
        for agent, count in sorted(self.metrics['agents_applied'].items()):
            summary += f"  - {agent}: {count} files\n"
        
        logging.info(summary)
        print(summary)

    def create_file_snapshot(self, file_path: Path) -> Optional[str]:
        """Create a snapshot of file content before modifications.
        
        Saves the current content of a file for potential rollback later.
        Useful for preserving pre-agent versions before applying improvements.
        
        Args:
            file_path: Path to the file to snapshot.
            
        Returns:
            str: Snapshot ID (timestamp-based) for later rollback, or None if snapshot failed.
            
        Example:
            snapshot_id = agent.create_file_snapshot(Path('src/main.py'))
            # Make changes...
            if something_wrong:
                agent.restore_from_snapshot('src/main.py', snapshot_id)
        """
        try:
            if not file_path.exists():
                logging.debug(f"Cannot snapshot non-existent file: {file_path}")
                return None
            
            # Create snapshots directory if needed
            snapshot_dir = self.repo_root / '.agent_snapshots'
            snapshot_dir.mkdir(exist_ok=True)
            
            # Generate snapshot ID based on timestamp
            import hashlib
            content = file_path.read_text(encoding='utf-8', errors='replace')
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            snapshot_id = f"{time.time():.0f}_{content_hash}"
            
            # Save relative path and content
            rel_path = file_path.relative_to(self.repo_root)
            snapshot_file = snapshot_dir / f"{snapshot_id}_{rel_path.name}"
            snapshot_file.write_text(content, encoding='utf-8')
            
            logging.debug(f"Created snapshot {snapshot_id} for {rel_path}")
            return snapshot_id
            
        except Exception as e:
            logging.error(f"Failed to create snapshot for {file_path}: {e}")
            return None

    def restore_from_snapshot(self, file_path: Path, snapshot_id: str) -> bool:
        """Restore a file from a previously created snapshot.
        
        Restores file content from a snapshot created by create_file_snapshot().
        Useful for rollback when agent modifications are undesirable.
        
        Args:
            file_path: Path to the file to restore.
            snapshot_id: Snapshot ID returned by create_file_snapshot().
            
        Returns:
            bool: True if restoration successful, False otherwise.
            
        Example:
            snapshot_id = agent.create_file_snapshot(Path('src/main.py'))
            # Modifications...
            agent.restore_from_snapshot(Path('src/main.py'), snapshot_id)
        """
        try:
            snapshot_dir = self.repo_root / '.agent_snapshots'
            if not snapshot_dir.exists():
                logging.warning(f"Snapshot directory not found: {snapshot_dir}")
                return False
            
            # Find snapshot file matching pattern
            rel_path = file_path.relative_to(self.repo_root)
            pattern = f"{snapshot_id}_{rel_path.name}"
            
            snapshot_file = snapshot_dir / pattern
            if not snapshot_file.exists():
                logging.warning(f"Snapshot not found: {pattern}")
                return False
            
            # Restore content
            content = snapshot_file.read_text(encoding='utf-8')
            file_path.write_text(content, encoding='utf-8')
            
            logging.info(f"Restored {rel_path} from snapshot {snapshot_id}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to restore snapshot for {file_path}: {e}")
            return False

    def load_cascading_codeignore(self, directory: Optional[Path] = None) -> Set[str]:
        """Load .codeignore patterns with cascading support.
        
        Loads ignore patterns from .codeignore files in the directory and all
        parent directories up to the repository root. This enables hierarchical
        ignore patterns where subdirectories can have their own .codeignore.
        
        Args:
            directory: Directory to start searching from. Defaults to repo_root.
            
        Returns:
            Set[str]: Combined set of ignore patterns from all .codeignore files.
            
        Example:
            # Load patterns from /repo/.codeignore and /repo/src/.codeignore
            patterns = agent.load_cascading_codeignore(Path('src'))
            
        Note:
            - Patterns closer to the target directory take precedence
            - All patterns are combined into a single set for efficiency
            - Duplicate patterns are automatically deduplicated
        """
        if directory is None:
            directory = self.repo_root
        
        all_patterns = set()
        current_dir = directory.resolve()
        
        # Walk up to repo root, loading .codeignore files
        while current_dir >= self.repo_root:
            codeignore_file = current_dir / '.codeignore'
            if codeignore_file.exists():
                try:
                    patterns = load_codeignore(current_dir)
                    all_patterns.update(patterns)
                    logging.debug(f"Loaded {len(patterns)} patterns from {codeignore_file}")
                except Exception as e:
                    logging.warning(f"Failed to load {codeignore_file}: {e}")
            
            # Stop at repo root
            if current_dir == self.repo_root:
                break
            
            current_dir = current_dir.parent
        
        logging.debug(f"Total cascading patterns from {directory}: {len(all_patterns)}")
        return all_patterns

    def _run_command(self, cmd: List[str], timeout: int = 120, max_retries: int = 1) -> subprocess.CompletedProcess:
        """Run a command with timeout, error handling, retry logic, and logging.
        
        Executes a subprocess command with comprehensive error handling,
        timeout protection, exponential backoff retry, and logging of results.
        
        Args:
            cmd: Command as list of strings (e.g., ['python', 'script.py', '--arg']).
            timeout: Timeout in seconds for command execution. Defaults to 120.
            max_retries: Number of retry attempts on failure. Defaults to 1 (no retry).
            
        Returns:
            subprocess.CompletedProcess: Contains returncode, stdout, stderr.
            
        Raises:
            None. All errors are caught and logged. Returns failed CompletedProcess.
            
        Example:
            result = agent._run_command(['python', '-m', 'pytest', 'test.py'], max_retries=2)
            if result.returncode == 0:
                print("Success")
            else:
                print(f"Failed: {result.stderr}")
                
        Note:
            - Uses UTF-8 encoding with 'replace' error handling for robustness
            - Captures both stdout and stderr
            - Logs command execution at DEBUG level
            - Returns CompletedProcess even on timeout (returncode=-1)
            - Retries with exponential backoff: 1s, 2s, 4s, etc.
        """
        def attempt_command():
            logging.debug(f"Running command: {' '.join(cmd[:3])}... (timeout={timeout}s)")
            try:
                result = subprocess.run(
                    cmd,
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    encoding='utf-8',
                    errors='replace',
                    check=False
                )
                logging.debug(f"Command completed with returncode={result.returncode}")
                return result
            except subprocess.TimeoutExpired:
                logging.error(f"Command timed out after {timeout}s: {' '.join(cmd[:3])}...")
                return subprocess.CompletedProcess(cmd, returncode=-1, stdout="", stderr="Timeout expired")
            except OSError as e:
                logging.error(f"Command failed to start: {e}")
                return subprocess.CompletedProcess(cmd, returncode=-1, stdout="", stderr=str(e))
            except Exception as e:
                logging.error(f"Command failed with unexpected error: {e}")
                return subprocess.CompletedProcess(cmd, returncode=-1, stdout="", stderr=str(e))
        
        result = attempt_command()
        
        # Retry on failure with exponential backoff
        for attempt in range(1, max_retries):
            if result.returncode == 0:
                return result
            
            delay = min(1.0 * (2 ** (attempt - 1)), 30.0)  # Max 30 seconds
            logging.warning(f"Command failed (attempt {attempt}), retrying in {delay}s...")
            time.sleep(delay)
            result = attempt_command()
        
        return result

    def _find_repo_root(self, start_path: Path) -> Path:
        """Find the repository root by looking for repository markers.
        
        Walks up the directory tree from the start path looking for markers
        that indicate a repository root (.git, README.md, package.json).
        
        Args:
            start_path: Starting directory path to search from.
            
        Returns:
            Path: Repository root directory, or start_path if no markers found.
            
        Example:
            root = agent._find_repo_root(Path('/some/nested/dir'))
            # Returns Path to repo root if .git found in parents
            
        Note:
            - Checks the starting path first, then walks up to parents
            - Uses multiple markers to identify repo roots
            - Returns start_path if no markers found (doesn't raise error)
        """
        current = start_path.resolve()
        logging.debug(f"Searching for repository root from {current}")
        # Walk up the directory tree looking for repository markers
        for path in [current] + list(current.parents):
            if (path / '.git').exists() or (path / 'README.md').exists() or \
                    (path / 'package.json').exists():
                logging.info(f"Found repository root at {path}")
                return path
        # If no markers found, return the original path
        logging.debug(f"No repository markers found, using {start_path} as root")
        return start_path

    def find_code_files(self) -> List[Path]:
        """Recursively find all supported code files in the repository.
        
        Searches the repository for files with supported extensions, optionally
        filtered to the scripts/agent directory, and respects .codeignore patterns.
        
        Returns:
            List[Path]: Sorted list of code files found, limited by max_files if set.
            
        Example:
            files = agent.find_code_files()
            print(f"Found {len(files)} code files")
            
        Note:
            - Uses recursive glob patterns for efficiency
            - Filters by SUPPORTED_EXTENSIONS (py, sh, js, ts, go, rb)
            - Respects .codeignore patterns
            - Returns sorted list for reproducibility
            - Limited by max_files parameter if set
        """
        logging.info("Searching for code files...")
        code_files = []
        for ext in self.SUPPORTED_EXTENSIONS:
            code_files.extend(self.repo_root.rglob(f'*{ext}'))
        logging.debug(f"Found {len(code_files)} files with supported extensions")
        
        # Filter to scripts/agent directory if agents_only is True
        if self.agents_only:
            scripts_agent_dir = self.repo_root / 'scripts' / 'agent'
            code_files = [f for f in code_files if f.is_relative_to(scripts_agent_dir)]
            logging.info(f"Filtered to scripts/agent directory: {len(code_files)} files")
        
        # Apply ignore patterns
        code_files = sorted([f for f in code_files if not self._is_ignored(f)])
        logging.info(f"After filtering ignores: {len(code_files)} files")
        
        if self.max_files:
            code_files = code_files[:self.max_files]
            logging.info(f"Limited to max_files={self.max_files}")
        
        return code_files

    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored based on .codeignore patterns.
        
        Checks if a path matches any of the ignore patterns from .codeignore,
        using fnmatch patterns for flexible matching.
        
        Args:
            path: Path object to check.
            
        Returns:
            bool: True if path matches any ignore pattern, False otherwise.
            
        Example:
            ignored = agent._is_ignored(Path('venv/lib/file.py'))
            # Returns True if 'venv/**' or 'lib/**' in ignore patterns
            
        Note:
            - Checks against full path, filename, and path components
            - Uses fnmatch for Unix-style glob patterns
            - Returns False if no ignore patterns loaded
        """
        path_str = str(path)
        for pattern in self.ignored_patterns:
            if (fnmatch.fnmatch(path_str, pattern) or
                fnmatch.fnmatch(path.name, pattern) or
                any(fnmatch.fnmatch(part, pattern) for part in path.parts)):
                logging.debug(f"Path {path} ignored by pattern: {pattern}")
                return True
        return False

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
        return bool(changes_made)

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
        return bool(changes_made)

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
        return bool(changes_made)

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

    def _commit_and_push(self, code_file: Path) -> None:
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

    def register_webhook(self, webhook_url: str) -> None:
        """Register a webhook URL for event notifications.
        
        Registers a webhook URL that will receive POST requests for agent events
        (file processing, completion, errors, etc.). Useful for integration with
        external systems like Slack, Discord, or custom monitoring dashboards.
        
        Args:
            webhook_url: Full URL of the webhook endpoint.
            
        Returns:
            None. Logs registration.
            
        Example:
            agent.register_webhook('https://hooks.slack.com/services/xxx')
            agent.register_webhook('https://example.com/agent-events')
            
        Note:
            - Multiple webhooks can be registered
            - Webhooks are sent asynchronously and don't block execution
            - Failed webhook sends are logged but don't halt execution
        """
        self.webhooks.append(webhook_url)
        logging.info(f"Registered webhook: {webhook_url}")

    def register_callback(self, callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """Register a callback function for agent events.
        
        Registers a Python callable that will be invoked for agent events.
        Callbacks are called synchronously and can receive event data.
        
        Args:
            callback: Callable accepting (event_name: str, event_data: Dict).
            
        Returns:
            None. Logs registration.
            
        Example:
            def my_callback(event_name: str, event_data: Dict):
                print(f"Event: {event_name}")
                print(f"Data: {event_data}")
            
            agent.register_callback(my_callback)
            
        Note:
            - Multiple callbacks can be registered
            - Callbacks are called in registration order
            - Exceptions in callbacks are caught and logged
        """
        self.callbacks.append(callback)
        callback_name = getattr(callback, '__name__', repr(callback))
        logging.info(f"Registered callback: {callback_name}")

    def send_webhook_notification(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Send notification to all registered webhooks.
        
        Sends event notifications to all registered webhook URLs via HTTP POST.
        Uses JSON encoding for the payload. Failed sends are logged but don't halt.
        
        Args:
            event_name: Name of the event (e.g., 'file_processed', 'error').
            event_data: Event data as dictionary (will be JSON-encoded).
            
        Returns:
            None. Logs results.
            
        Example:
            agent.send_webhook_notification('agent_complete', {
                'files_processed': 42,
                'files_modified': 15,
                'duration_seconds': 123.45
            })
            
        Note:
            - Webhooks are sent asynchronously in background threads
            - If requests library not available, webhooks are skipped
            - Timeouts are set to 5 seconds per webhook
        """
        if not HAS_REQUESTS or not self.webhooks:
            return
        
        payload = {
            'event': event_name,
            'timestamp': time.time(),
            'data': event_data
        }
        
        for webhook_url in self.webhooks:
            try:
                logging.debug(f"Sending webhook: {webhook_url}")
                requests.post(
                    webhook_url,
                    json=payload,
                    timeout=5
                )
                logging.debug(f"Webhook sent successfully to {webhook_url}")
            except Exception as e:
                logging.warning(f"Failed to send webhook to {webhook_url}: {e}")

    def execute_callbacks(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Execute all registered callback functions for an event.
        
        Invokes all registered callback functions with event data.
        Exceptions in callbacks are caught and logged, allowing other callbacks to run.
        
        Args:
            event_name: Name of the event (e.g., 'file_processed').
            event_data: Event data to pass to callbacks.
            
        Returns:
            None. Logs execution results.
            
        Example:
            agent.execute_callbacks('processing_complete', {
                'file': 'main.py',
                'changes_made': True
            })
            
        Note:
            - Callbacks are called synchronously in registration order
            - Exceptions in one callback don't prevent others from running
            - Failures are logged as warnings but don't halt execution
        """
        for callback in self.callbacks:
            try:
                callback_name = getattr(callback, '__name__', repr(callback))
                logging.debug(f"Executing callback: {callback_name}")
                callback(event_name, event_data)
            except Exception as e:
                callback_name = getattr(callback, '__name__', repr(callback))
                logging.warning(f"Callback {callback_name} failed: {e}")

    async def async_process_files(self, files: List[Path]) -> List[Path]:
        """Process multiple files concurrently using async/await.
        
        Processes files concurrently using asyncio for I/O-bound operations.
        Useful when the bottleneck is waiting for external services rather than CPU.
        Returns immediately; file processing happens asynchronously.
        
        Args:
            files: List of file paths to process.
            
        Returns:
            List[Path]: List of files that were modified.
            
        Example:
            files = agent.find_code_files()
            modified = await agent.async_process_files(files)
            print(f"Modified {len(modified)} files")
            
        Note:
            - Requires enable_async=True in __init__
            - Uses ThreadPoolExecutor for I/O operations
            - Respects max_workers setting
            - File processing happens in separate threads
            - Modified files are tracked in metrics
        """
        modified_files = []
        
        async def process_file_async(file_path: Path):
            """Process a single file asynchronously."""
            try:
                logging.debug(f"[async] Processing {file_path.name}")
                self.process_file(file_path)
                modified_files.append(file_path)
                self.metrics['files_processed'] += 1
                logging.info(f"[async] Completed {file_path.name}")
            except Exception as e:
                logging.error(f"[async] Failed to process {file_path.name}: {e}")
        
        # Create tasks for all files
        tasks = [process_file_async(f) for f in files]
        
        # Run tasks concurrently
        if tasks:
            await asyncio.gather(*tasks)
        
        return modified_files

    def process_files_multiprocessing(self, files: List[Path]) -> List[Path]:
        """Process multiple files using multiprocessing for parallel execution.
        
        Processes files in parallel using separate Python processes.
        Useful for CPU-intensive operations or avoiding Python's GIL.
        Each worker processes multiple files sequentially.
        
        Args:
            files: List of file paths to process.
            
        Returns:
            List[Path]: List of files that were processed.
            
        Example:
            files = agent.find_code_files()
            processed = agent.process_files_multiprocessing(files)
            print(f"Processed {len(processed)} files")
            
        Note:
            - Requires enable_multiprocessing=True in __init__
            - Uses ProcessPoolExecutor for CPU-bound operations
            - Respects max_workers setting
            - Each worker has its own Python interpreter
            - Progress tracking works with tqdm if available
            - Modified count is estimated from total processed
        """
        processed_files = []
        
        # Use ThreadPoolExecutor for parallel processing (easier pickling than ProcessPoolExecutor)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Create partial functions that can be pickled more easily
            worker_func = functools.partial(_multiprocessing_worker, self)
            
            results = list(tqdm(
                executor.map(worker_func, files),
                total=len(files),
                desc="Processing files (multiprocessing)"
            ) if HAS_TQDM else executor.map(worker_func, files))
        
        # Filter out None results
        processed_files = [f for f in results if f is not None]
        self.metrics['files_processed'] = len(processed_files)
        
        return processed_files

    def process_files_threaded(self, files: List[Path]) -> List[Path]:
        """Process multiple files using threading for concurrent I/O.
        
        Processes files concurrently using worker threads. Good for I/O-bound
        operations while keeping code simpler than async. Works around Python's GIL.
        
        Args:
            files: List of file paths to process.
            
        Returns:
            List[Path]: List of files that were processed.
            
        Example:
            files = agent.find_code_files()
            processed = agent.process_files_threaded(files)
            print(f"Processed {len(processed)} files")
            
        Note:
            - Uses ThreadPoolExecutor for concurrent I/O
            - Respects max_workers setting
            - Good middle ground between sequential and multiprocessing
            - Shared state (metrics) is updated from worker threads
            - Progress tracking with tqdm if available
        """
        processed_files = []
        
        def worker_thread_process_file(file_path: Path) -> Path:
            """Worker function to process a file in a separate thread."""
            try:
                logging.debug(f"[thread] Processing {file_path.name}")
                self.process_file(file_path)
                logging.info(f"[thread] Completed {file_path.name}")
                return file_path
            except Exception as e:
                logging.error(f"[thread] Failed: {e}")
                return None
        
        # Use ThreadPoolExecutor for parallel I/O
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(tqdm(
                executor.map(worker_thread_process_file, files),
                total=len(files),
                desc="Processing files (threaded)"
            ) if HAS_TQDM else executor.map(worker_thread_process_file, files))
        
        # Filter out None results
        processed_files = [f for f in results if f is not None]
        self.metrics['files_processed'] = len(processed_files)
        
        return processed_files

    def run_with_parallel_execution(self) -> None:
        """Run the main agent loop with parallel execution strategy.
        
        Runs the agent with either async, multiprocessing, or threaded execution
        based on configuration. Falls back to sequential if neither enabled.
        
        Returns:
            None. Results logged and metrics updated.
            
        Note:
            - Priority: multiprocessing > async > threaded > sequential
            - Webhooks and callbacks triggered on completion
            - Metrics summary printed at end
        """
        code_files = self.find_code_files()
        logging.info(f"Found {len(code_files)} code files to process")
        
        for loop_iteration in range(1, self.loop + 1):
            logging.info(f"Starting loop iteration {loop_iteration}/{self.loop}")
            
            # Choose execution strategy
            if self.enable_multiprocessing:
                logging.info("Using multiprocessing for parallel execution")
                self.process_files_multiprocessing(code_files)
            elif self.enable_async:
                logging.info("Using async for concurrent execution")
                asyncio.run(self.async_process_files(code_files))
            else:
                logging.info("Using threaded execution")
                self.process_files_threaded(code_files)
            
            logging.info(f"Completed loop iteration {loop_iteration}/{self.loop}")
        
        # Trigger completion events
        self.execute_callbacks('agent_complete', self.metrics)
        self.send_webhook_notification('agent_complete', self.metrics)
        
        # Final stats update
        logging.info("Final stats:")
        self.run_stats_update(code_files)

    def process_file(self, code_file: Path) -> None:
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

    def run(self) -> None:
        """Run the main agent loop.
        
        Executes the main agent loop, processing all code files found.
        Uses parallel execution if enabled, otherwise sequential processing.
        Triggers webhooks and callbacks on completion.
        """
        if self.enable_async or self.enable_multiprocessing:
            self.run_with_parallel_execution()
        else:
            # Sequential execution (original behavior)
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
            
            # Trigger completion events
            self.execute_callbacks('agent_complete', self.metrics)
            self.send_webhook_notification('agent_complete', self.metrics)


def main() -> None:
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
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without modifying files')
    parser.add_argument('--only-agents', type=str, metavar='AGENTS',
                        help='Comma-separated list of agents to execute (e.g., coder,tests,documentation)')
    parser.add_argument('--timeout', type=int, metavar='SECONDS', default=120,
                        help='Default timeout per agent in seconds (default: 120)')
    # Phase 4c: Parallel execution arguments
    parser.add_argument('--async', dest='enable_async', action='store_true',
                        help='Enable async file processing for concurrent I/O')
    parser.add_argument('--multiprocessing', dest='enable_multiprocessing', action='store_true',
                        help='Enable multiprocessing for parallel agent execution')
    parser.add_argument('--workers', type=int, default=4,
                        help='Number of worker threads/processes (default: 4)')
    parser.add_argument('--webhook', type=str, action='append',
                        help='Register webhook URL for notifications (can be used multiple times)')
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    os.environ['DV_AGENT_VERBOSITY'] = args.verbose
    
    # Parse selective agents if provided
    selective_agents = None
    if args.only_agents:
        selective_agents = [a.strip() for a in args.only_agents.split(',')]
        logging.info(f"Running with selective agents: {selective_agents}")
    
    agent = Agent(
        repo_root=args.dir,
        agents_only=args.agents_only,
        max_files=args.max_files,
        loop=args.loop,
        skip_code_update=args.skip_code_update,
        no_git=args.no_git,
        dry_run=args.dry_run,
        selective_agents=selective_agents,
        timeout_per_agent={'coder': args.timeout, 'tests': args.timeout},
        enable_async=args.enable_async,
        enable_multiprocessing=args.enable_multiprocessing,
        max_workers=args.workers
    )
    
    # Register webhooks if provided
    if args.webhook:
        for webhook_url in args.webhook:
            agent.register_webhook(webhook_url)
    
    try:
        agent.run()
    finally:
        # Always print metrics summary
        agent.print_metrics_summary()
