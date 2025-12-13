#!/usr/bin/env python3
import re

file_path = 'scripts/critic_workflow.py.plan.md'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix MD022: Add blank lines around headings
lines = content.split('\n')
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if this is a heading (starts with #)
    if line.startswith('#') and not line.startswith('#!/'):
        # Add blank line before if needed
        if fixed_lines and fixed_lines[-1].strip() != '':
            fixed_lines.append('')
        fixed_lines.append(line)
        # Add blank line after if needed
        if i + 1 < len(lines) and lines[i + 1].strip() != '':
            fixed_lines.append('')
    else:
        fixed_lines.append(line)
    i += 1

content = '\n'.join(fixed_lines)

# Fix MD026: Remove trailing punctuation from headings
content = re.sub(r'^(#+\s+[^:\n]+):\s*$', r'\1', content, flags=re.MULTILINE)

# Fix MD034: Wrap bare URLs in markdown links
content = re.sub(r'(?<!\[)https?://([^\s\)]+)(?!\))', r'[\g<0>](\g<0>)', content)

# Fix MD029: Standardize ordered list numbering to use 1.
content = re.sub(r'^(\s*)([2-9]\.)(\s+)', r'\g<1>1.\g<3>', content, flags=re.MULTILINE)

# Fix MD040: Add language identifier to code blocks
content = re.sub(r'^```$', r'```python', content, flags=re.MULTILINE)

# Fix MD032: Add blank lines around lists
lines = content.split('\n')
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if this is a list item (starts with -, *, +, or 1.)
    if re.match(r'^\s*[-*+1]\s', line):
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
