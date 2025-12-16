#!/usr/bin/env python3
"""
Fix W293 (blank line whitespace) issues in generate_agent_reports.py
"""

filepath = r"c:\Users\kdejo\DEV\DebVisor\scripts\agent\generate_agent_reports.py"

# Read file
with open(filepath, 'r', encoding = 'utf-8') as f:
    content = f.read()

# Get all lines (preserving line endings)
lines = content.splitlines(keepends = True)

w293_fixed = 0
updated_lines = []

# Process each line
for i, line in enumerate(lines, 1):
    # Check if line is blank (only whitespace)
    if line.rstrip('\n\r') == '':
        # Line is blank - remove any trailing whitespace before newline
        if line != '\n':
            updated_lines.append('\n')
            w293_fixed += 1
        else:
            updated_lines.append(line)
    else:
        updated_lines.append(line)

# Write file
with open(filepath, 'w', encoding = 'utf-8') as f:
    f.writelines(updated_lines)

print(f"Fixed {w293_fixed} W293 (blank line whitespace) issues")
print(f"Successfully wrote fixed file to {filepath}")
