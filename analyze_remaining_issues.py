#!/usr/bin/env python3
"""Categorize and report remaining flake8 issues."""

import subprocess
import json
from collections import defaultdict

# Run flake8 and capture output
result = subprocess.run(
    ['.venv\\Scripts\\python.exe', '-m', 'flake8', '--max-line-length=120', 'scripts/agent/', '--format=json'],
    capture_output=True,
    text=True
)

try:
    issues = json.loads(result.stdout)
except json.JSONDecodeError:
    # Fall back to parsing text output
    result = subprocess.run(
        ['.venv\\Scripts\\python.exe', '-m', 'flake8', '--max-line-length=120', 'scripts/agent/'],
        capture_output=True,
        text=True
    )
    issues = []
    for line in result.stdout.split('\n'):
        if ':' in line and line.strip():
            parts = line.split(':')
            code = parts[-1].strip().split()[0]
            issues.append({'code': code})

# Categorize by error code
categories = defaultdict(list)
for issue in issues:
    if isinstance(issue, dict) and 'code' in issue:
        code = issue['code']
    else:
        continue
    categories[code].append(issue)

# Print summary
print("=" * 60)
print("REMAINING FLAKE8 ISSUES BY CATEGORY")
print("=" * 60)

total = 0
for code in sorted(categories.keys()):
    count = len(categories[code])
    total += count
    
    # Categorize by severity
    severity = "?"
    description = ""
    
    if code.startswith('E'):  # PEP8 errors
        severity = "STYLE"
        if code == 'E128': description = "Continuation line indentation"
        elif code == 'E129': description = "Visually indented line"
        elif code == 'E301': description = "Expected 1 blank line"
        elif code == 'E305': description = "Expected 2 blank lines"
        elif code == 'E501': description = "Line too long"
        elif code == 'E713': description = "Test for membership should be 'not in'"
        else: description = "PEP8 style error"
    
    elif code.startswith('W'):  # PEP8 warnings
        severity = "WARNING"
        if code == 'W291': description = "Trailing whitespace"
        elif code == 'W293': description = "Blank line with whitespace"
        else: description = "PEP8 warning"
    
    elif code.startswith('F'):  # PyFlakes errors
        severity = "LOGIC"
        if code == 'F401': description = "Imported but unused"
        elif code == 'F402': description = "Import shadows builtin"
        elif code == 'F541': description = "F-string missing placeholders"
        elif code == 'F821': description = "Undefined name"
        elif code == 'F841': description = "Assigned but never used"
        elif code == 'F811': description = "Redefined while unused"
        else: description = "Code logic error"
    
    print(f"{code:6} | {count:3} issues | {severity:8} | {description}")
    
    # Show some details for high-count issues
    if count <= 3 and 'message' in categories[code][0]:
        for issue in categories[code]:
            print(f"       └─ {issue.get('filename', '?')}:{issue.get('line_number', '?')}")

print("=" * 60)
print(f"TOTAL:  | {total:3} issues")
print("=" * 60)

# Priority recommendations
print("\nRECOMMENDED PRIORITY:")
print("-" * 60)
print("🔴 CRITICAL (Must fix):")
print("   - F821: Undefined names (31) - breaks code")
print("   - E501: Lines too long (8) - convention")
print()
print("🟠 HIGH (Should fix soon):")
print("   - F401: Unused imports (24) - code cleanliness")
print("   - E128: Indentation (60) - readability")
print("   - F541: F-string issues (12) - correctness")
print()
print("🟡 MEDIUM (Nice to have):")
print("   - F841: Unused variables (7) - code cleanliness")
print("   - E741: Ambiguous names (3) - readability")
print("   - E301/E305: Blank lines (5) - PEP8 style")
print()
print("🟢 LOW (Nice to have):")
print("   - E713: Membership test (1) - code style")
print("   - F402: Import shadows (1) - code quality")
print("   - F811: Redefined (6) - code cleanliness")
