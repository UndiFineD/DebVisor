#!/usr/bin/env python3
"""Fix E251/E252 issues in function signatures"""
import re
from pathlib import Path

path = Path('opt/services/backup/backup_intelligence.py')
content = path.read_text(encoding='utf-8')

# E251: unexpected spaces around keyword / parameter equals
# Fix: "param = value" in function definitions should be "param=value"
# But we also need to fix "param=value" to "param = value" in assignments

lines = content.split('\n')
for i, line in enumerate(lines):
    # In function definitions, default parameters should not have spaces: def foo(x=1, y=2)
    if 'def ' in line and '(' in line:
        # This is a function definition - fix param = value to param=value
        before_paren = line[:line.find('(')]
        # Get the parameter list
        start = line.find('(')
        end = line.find(')')
        if start >= 0 and end > start:
            params = line[start+1:end]
            # Fix param = value to param=value in parameters
            params = re.sub(r'(\w+)\s*=\s*([^\,\)]*)', r'\1=\2', params)
            line = before_paren + '(' + params + ')' + line[end+1:]

lines = '\n'.join(lines)
path.write_text(lines, encoding='utf-8')
print("✓ Fixed E251/E252 parameter spacing in function definitions")
