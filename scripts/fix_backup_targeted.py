#!/usr/bin/env python3
"""Targeted fixes for remaining issues"""

import re

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    lines = f.readlines()

# Fix 1: Change function parameter from hoursahead to hours_ahead (line 336)
for i, line in enumerate(lines):
    if 'def predict_changes(self, vmid: str, hoursahead: int)' in line:
        lines[i] = line.replace('hoursahead: int', 'hours_ahead: int')
        # Also fix vmid -> vm_id
        lines[i] = lines[i].replace('vmid: str', 'vm_id: str')

# Fix 2: Handle indentation issues - add pass before comments after else/except/finally
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.lstrip()
    
    # Check for else:/except:/finally: followed by comment on next line
    if re.match(r'^(else|except|finally|try):\s*$', stripped):
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line.strip().startswith('#'):
                # Get indentation from current line
                indent_level = len(line) - len(stripped)
                # Add pass with proper indentation
                pass_indent = ' ' * (indent_level + 4)
                lines.insert(i + 1, pass_indent + 'pass\n')
                i += 1  # Skip the newly inserted line
    i += 1

# Fix 3: Fix E251/E252 - parameter spacing issues in function calls
# These are typically in default_factory=dict, etc.
patterns = [
    (r'default_factory\s*=\s*dict', 'default_factory=dict'),
    (r'default_factory\s*=\s*list', 'default_factory=list'),
    (r'default_factory\s*=\s*', 'default_factory='),
]

content = ''.join(lines)
for pattern, replacement in patterns:
    content = re.sub(pattern, replacement, content)

lines = content.split('\n')
lines = [line + '\n' if line and not line.endswith('\n') else line for line in lines]

# Fix 4: sandbox_id and policy_id - these need to be extracted from method parameters
# Looking at context, we need to define these variables properly
# For now, let's check what methods these are in

# Fix 5: E251/E252 spacing in specific locations - need to look at actual lines
# Let's read the file back to identify specific issues

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.writelines(lines)

print("Targeted fixes completed")
