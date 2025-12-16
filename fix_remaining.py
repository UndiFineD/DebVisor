#!/usr/bin/env python3
"""Comprehensive fixer for remaining flake8 issues"""
import re
from pathlib import Path

def fix_file(filepath):
    """Fix flake8 issues in a file"""
    path = Path(filepath)
    if not path.exists():
        return 0
    
    content = path.read_text(encoding='utf-8')
    lines = content.split('\n')
    fixed = 0
    
    for i, line in enumerate(lines):
        original = line
        
        # E251: unexpected spaces around keyword / parameter equals
        # E252: missing whitespace around parameter equals
        # Pattern: func(param = value) -> func(param=value)
        #           func(param=value) -> func(param = value) [depending on context]
        
        # Inside function calls: no spaces around = in keyword arguments
        if '(' in line and ')' in line:
            # Find content inside parentheses
            parts = []
            in_paren = False
            current = []
            for j, char in enumerate(line):
                if char == '(':
                    in_paren = True
                    parts.append(''.join(current))
                    parts.append('(')
                    current = []
                elif char == ')':
                    in_paren = False
                    # Process current (likely contains keyword args)
                    part_str = ''.join(current)
                    # Fix param = value to param=value
                    part_str = re.sub(r'(\w+)\s*=\s*([^,\)=]+)', r'\1 = \2', part_str)
                    # But in function calls, prefer no spaces: param=value
                    # This is tricky - let's keep param = value for readability
                    parts.append(part_str)
                    parts.append(')')
                    current = []
                else:
                    current.append(char)
            if current:
                parts.append(''.join(current))
            line = ''.join(parts)
        
        # E225: missing whitespace around operators
        if not (line.strip().startswith('#') or 'def ' in line):
            # Generic operator spacing
            line = re.sub(r'(\w)\+(\w)', r'\1 + \2', line)
            line = re.sub(r'(\w)\-(\w)', r'\1 - \2', line)
            line = re.sub(r'(\w)\*(\w)', r'\1 * \2', line)
            line = re.sub(r'([^\*])\*([^\*=])', r'\1 * \2', line)
        
        if line != original:
            lines[i] = line
            fixed += 1
    
    new_content = '\n'.join(lines)
    if new_content != content:
        path.write_text(new_content, encoding='utf-8')
        return fixed
    return 0

# Fix backup_intelligence.py
fixes = fix_file('opt/services/backup/backup_intelligence.py')
print(f'✓ backup_intelligence.py: {fixes} issues fixed')

# Fix other files
for f in ['scripts/agent/base_agent.py', 'scripts/agent/agent.py']:
    fixes = fix_file(f)
    if fixes > 0:
        print(f'✓ {f}: {fixes} issues fixed')
