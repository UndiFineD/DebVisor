#!/usr/bin/env python3
"""Fix E251 errors in agent_backend.py"""
import re
from pathlib import Path

path = Path('scripts/agent/agent_backend.py')
content = path.read_text(encoding='utf-8')

# Fix E251: Remove spaces around = in keyword arguments (inside parentheses)
lines = content.split('\n')
fixed = 0

for i, line in enumerate(lines):
    original = line
    
    # Find content inside parentheses and fix keyword arguments
    # Pattern: parameter = value inside function calls/definitions
    # Replace: param = value with param=value
    
    # Simple approach: replace " = " with "=" when it's surrounded by word chars and in parens
    # Look for patterns like: word = word or word = number etc inside parens
    
    # Use regex to match: identifier followed by spaces and = and spaces, then value
    # But only within parentheses
    
    if '(' in line and ')' in line:
        # Split by parentheses and process the content
        parts = []
        paren_depth = 0
        current = []
        
        for j, char in enumerate(line):
            if char == '(':
                if current:
                    parts.append(('normal', ''.join(current)))
                    current = []
                paren_depth += 1
                parts.append(('paren_open', '('))
            elif char == ')':
                if current:
                    parts.append(('normal', ''.join(current)))
                    current = []
                paren_depth -= 1
                parts.append(('paren_close', ')'))
            else:
                current.append(char)
        
        if current:
            parts.append(('normal', ''.join(current)))
        
        # Process parts
        result = []
        in_parens = 0
        
        for part_type, part_text in parts:
            if part_type == 'paren_open':
                in_parens += 1
                result.append(part_text)
            elif part_type == 'paren_close':
                in_parens -= 1
                result.append(part_text)
            elif in_parens > 0 and part_type == 'normal':
                # Remove spaces around = in keyword arguments
                # Pattern: word = value -> word=value
                fixed_part = re.sub(r'(\w)\s*=\s*([^=])', r'\1=\2', part_text)
                result.append(fixed_part)
            else:
                result.append(part_text)
        
        line = ''.join(result)
    
    if line != original:
        lines[i] = line
        fixed += 1

new_content = '\n'.join(lines)
path.write_text(new_content, encoding='utf-8')

print(f"✓ Fixed {fixed} lines in agent_backend.py")
