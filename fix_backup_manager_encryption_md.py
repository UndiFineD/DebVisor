#!/usr/bin/env python3
import re

file_path = 'tests/test_backup_manager_encryption.py.md'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix MD040: Add language identifier to code blocks
content = re.sub(r'^```$', r'```python', content, flags=re.MULTILINE)

# Fix MD012: Remove multiple consecutive blank lines
content = re.sub(r'\n\n\n+', '\n\n', content)

# Fix MD036: Convert emphasis as heading to proper heading
content = re.sub(r'^\*\*(.+?):?\*\*$', r'### \1', content, flags=re.MULTILINE)

# Now fix MD022, MD031, MD032 with line-by-line processing
lines = content.split('\n')
fixed_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check for code block opening
    if line.startswith('```python'):
        # Add blank line before if needed
        if fixed_lines and fixed_lines[-1].strip() != '':
            fixed_lines.append('')
        fixed_lines.append(line)
        # Process code block content
        i += 1
        while i < len(lines) and not lines[i].startswith('```'):
            fixed_lines.append(lines[i])
            i += 1
        # Add closing fence
        if i < len(lines):
            fixed_lines.append(lines[i])
            # Add blank line after if next line exists and is not blank
            if i + 1 < len(lines) and lines[i + 1].strip() != '':
                fixed_lines.append('')
    
    # Check for heading
    elif line.startswith('#') and not line.startswith('#!/'):
        # Add blank line before if needed
        if fixed_lines and fixed_lines[-1].strip() != '':
            fixed_lines.append('')
        fixed_lines.append(line)
        # Add blank line after if needed
        if i + 1 < len(lines) and lines[i + 1].strip() != '':
            fixed_lines.append('')
    
    # Check for list items
    elif re.match(r'^\s*[-*+]\s', line):
        # Add blank line before if needed
        if fixed_lines and fixed_lines[-1].strip() != '':
            fixed_lines.append('')
        fixed_lines.append(line)
    
    else:
        fixed_lines.append(line)
    
    i += 1

content = '\n'.join(fixed_lines)

# Write back to file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ Fixed all markdown linting errors')
