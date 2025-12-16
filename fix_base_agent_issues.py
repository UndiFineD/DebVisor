#!/usr/bin/env python3
"""Fix remaining issues in base_agent.py: F401, E302, and W293."""

import re

file_path = r"c:\Users\kdejo\DEV\DebVisor\scripts\agent\base_agent.py"

# Read file with proper encoding
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='latin-1') as f:
        lines = f.readlines()

# Fix 1: Remove unused subprocess import (line 27)
for i, line in enumerate(lines):
    if i == 26 and 'import subprocess' in line:  # Line 27 is index 26
        lines[i] = ''
        print(f"Removed unused subprocess import at line {i+1}")
        break

# Fix 2: Add blank line before create_main_function (line 2077)
# The function definition should be at a certain line
for i in range(len(lines)):
    if 'def create_main_function' in lines[i]:
        # Check if there's only one blank line before it
        blank_count = 0
        check_idx = i - 1
        while check_idx >= 0 and lines[check_idx].strip() == '':
            blank_count += 1
            check_idx -= 1
        
        if blank_count == 1:
            # Insert additional blank line
            lines.insert(i, '\n')
            print(f"Added blank line before create_main_function at line {i+1}")
        break

# Fix 3: Fix all W293 issues (blank lines with whitespace)
w293_count = 0
for i, line in enumerate(lines):
    if line.strip() == '' and len(line) > 1:  # Blank line with whitespace
        lines[i] = '\n'
        w293_count += 1

print(f"Fixed {w293_count} W293 (blank line whitespace) issues")

# Write file
try:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Successfully wrote fixed file to {file_path}")
except Exception as e:
    print(f"Error writing file: {e}")
    with open(file_path, 'w', encoding='latin-1') as f:
        f.writelines(lines)
    print(f"Successfully wrote fixed file (latin-1) to {file_path}")

print(f"\nSummary:")
print(f"- Removed 1 unused subprocess import (F401)")
print(f"- Added 1 blank line (E302)")
print(f"- Fixed {w293_count} blank line whitespace issues (W293)")
