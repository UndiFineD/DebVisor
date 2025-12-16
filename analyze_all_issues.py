#!/usr/bin/env python3
"""Analyze flake8 issues and create categorized report"""
import subprocess
import re
from collections import defaultdict

result = subprocess.run(
    ['python', '-m', 'flake8', '--max-line-length=120', 'scripts/agent/'],
    capture_output=True,
    text=True,
    cwd=r'c:\Users\kdejo\DEV\DebVisor'
)

issues = defaultdict(int)
files_affected = defaultdict(list)

for line in result.stderr.split('\n') + result.stdout.split('\n'):
    if not line.strip():
        continue
    match = re.match(r'([^:]+):(\d+):(\d+): ([A-Z]\d+)', line)
    if match:
        filepath, lineno, col, code = match.groups()
        issues[code] += 1
        files_affected[code].append(filepath)

print("=" * 60)
print("FLAKE8 ISSUE BREAKDOWN")
print("=" * 60)

for code in sorted(issues.keys(), key=lambda x: issues[x], reverse=True):
    count = issues[code]
    files = len(set(files_affected[code]))
    print(f"{code:6s} | {count:4d} issues | {files:3d} files")

print("=" * 60)
print(f"Total: {sum(issues.values())} issues")
print("=" * 60)

# Show fix priority
print("\nFIX PRIORITY (easiest to hardest):")
print("=" * 60)
print("🟢 E303/E304: Blank line issues - structural fix")
print("🟡 E501: Line too long - usually just reflow text")  
print("🟡 E302/E305: Blank line requirements - add/remove lines")
print("🟠 F401: Unused imports - needs verification")
print("🔴 F821: Undefined names - code logic issue")
print("🔴 F841: Unused variables - complex detection")
