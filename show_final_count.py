#!/usr/bin/env python3
"""Show final flake8 issue count"""

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-m", "flake8", "--max-line-length=120", "scripts/agent/"],
    capture_output=True,
    text=True
)

lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
issue_count = len([l for l in lines if l])

print(f"Final Flake8 Issues in scripts/agent/: {issue_count}\n")

# Count by error type
error_types = {}
for line in lines:
    if ':' in line:
        parts = line.split(':')
        if len(parts) >= 4:
            error_code = parts[3].strip().split()[0]
            error_types[error_code] = error_types.get(error_code, 0) + 1

if error_types:
    print("Issues by type:")
    for code in sorted(error_types.keys()):
        print(f"  {code}: {error_types[code]}")
