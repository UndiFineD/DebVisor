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
Stats Agent: Reports statistics on file updates and progress.

Tracks which files have updates needed and how many are done.

# Description
This module provides a Stats Agent that monitors the progress of code improvements
across files, reporting on pending updates and completed work.

# Changelog
- 1.0.0: Initial implementation

# Suggested Fixes
- Improve statistics tracking
- Add more detailed progress reports

# Improvements
- Better integration with other agents
- Enhanced reporting
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List


class StatsAgent:
    """Reports statistics on file update progress."""

    def __init__(self, files: List[str]) -> None:
        self.files = [Path(f) for f in files]
        self.stats = {}
        self._validate_files()

    def _validate_files(self) -> None:
        """Validate input files."""
        if not self.files:
            logging.error("No files provided")
            sys.exit(1)
        
        invalid = [f for f in self.files if not f.exists()]
        if invalid:
            logging.warning(f"Files not found: {', '.join(map(str, invalid))}")
            # Filter out invalid files
            self.files = [f for f in self.files if f.exists()]
            
        if not self.files:
            logging.error("No valid files found after filtering")
            sys.exit(1)

    def calculate_stats(self) -> Dict[str, int]:
        """Calculate statistics for each file."""
        total_files = len(self.files)
        files_with_context = 0
        files_with_changes = 0
        files_with_errors = 0
        files_with_improvements = 0
        files_with_tests = 0

        for file_path in self.files:
            base = file_path.stem
            dir_path = file_path.parent
            if (dir_path / f"{base}.description.md").exists():
                files_with_context += 1
            if (dir_path / f"{base}.changes.md").exists():
                files_with_changes += 1
            if (dir_path / f"{base}.errors.md").exists():
                files_with_errors += 1
            if (dir_path / f"{base}.improvements.md").exists():
                files_with_improvements += 1
            if (dir_path / f"test_{base}.py").exists():
                files_with_tests += 1
        self.stats = {
            'total_files': total_files,
            'files_with_context': files_with_context,
            'files_with_changes': files_with_changes,
            'files_with_errors': files_with_errors,
            'files_with_improvements': files_with_improvements,
            'files_with_tests': files_with_tests,
        }
        return self.stats

    def report_stats(self, output_format: str = 'text') -> None:
        """Print the statistics report."""
        stats = self.calculate_stats()
        total = stats['total_files']

        if output_format == 'json':
            print(json.dumps(stats, indent=2))
        else:
            def fmt(count: int) -> str:
                return f"{count}/{total} ({count/total*100:.1f}%)" if total > 0 else "0/0 (0.0%)"

            print("=== Stats Report ===")
            print(f"Total files: {total}")
            print(f"Files with descriptions: {fmt(stats['files_with_context'])}")
            print(f"Files with changelogs: {fmt(stats['files_with_changes'])}")
            print(f"Files with error reports: {fmt(stats['files_with_errors'])}")
            print(f"Files with improvements: {fmt(stats['files_with_improvements'])}")
            print(f"Files with tests: {fmt(stats['files_with_tests'])}")
            print("====================")


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Stats Agent: Reports file update statistics',
        epilog='Example: python scripts/agent/agent-stats.py --files scripts/agent/*.py'
    )
    parser.add_argument('--files', nargs='+', required=True, help='List of files to analyze')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--verbose', default='normal', help='Verbosity level')
    args = parser.parse_args()
    
    # Setup logging
    levels = {
        'quiet': logging.ERROR,
        'minimal': logging.WARNING,
        'normal': logging.INFO,
        'elaborate': logging.DEBUG,
    }
    level = levels.get(args.verbose.lower(), logging.INFO)
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

    agent = StatsAgent(args.files)
    agent.report_stats(output_format=args.format)


if __name__ == '__main__':
    main()
