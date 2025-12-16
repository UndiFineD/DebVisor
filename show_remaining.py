#!/usr/bin/env python3
"""Show remaining flake8 issues by file"""

import subprocess
from pathlib import Path

result = subprocess.run(
    ['.venv/Scripts/python.exe', '-m', 'flake8', 'scripts/agent/', '--max-line-length=120'],
    capture_output=True,
    text=True
)

files = {}
for line in result.stdout.split('\n'):
    if line.strip():
        filename = line.split(':')[0]
        files[filename] = files.get(filename, 0) + 1

print("\nRemaining Flake8 Issues by File (Top 20):\n")
for filename, count in sorted(files.items(), key=lambda x: -x[1])[:20]:
    name = Path(filename).name
    print(f"{name:50} {count:3} issues")

print(f"\nTotal: {sum(files.values())} issues in {len(files)} files")
