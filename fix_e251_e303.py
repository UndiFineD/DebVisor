#!/usr/bin/env python3
"""Fix E251 (parameter spacing) and E303 (excessive blank lines) in scripts/agent"""
import re
from pathlib import Path

def fix_e251_parameter_spacing(lines):
    """Fix E251: remove unexpected spaces around = in function parameters"""
    fixed = 0
    for i, line in enumerate(lines):
        original = line
        
        # Find function definitions and calls with parameters
        if '(' in line and ')' in line:
            # Process content inside parentheses
            start = line.find('(')
            end = line.rfind(')')
            
            if start >= 0 and end > start:
                before = line[:start+1]
                params = line[start+1:end]
                after = line[end:]
                
                # Fix param = value to param=value in parameters
                # But preserve spacing in non-parameter contexts
                if 'def ' in line or 'class ' in line:
                    # In definitions, remove spaces around =
                    fixed_params = re.sub(r'(\w+)\s*=\s*([^\s=,\)])', r'\1=\2', params)
                else:
                    # In calls, keep some readability but fix obvious spacing issues
                    fixed_params = re.sub(r'\s+=\s+', '=', params)
                
                if fixed_params != params:
                    lines[i] = before + fixed_params + after
                    fixed += 1
        
        # Also fix simple assignments (not in function calls)
        elif '=' in line and 'def ' not in line and 'lambda' not in line and '(' not in line:
            # Only process actual statements with =, not in function defs
            pass
    
    return lines, fixed

def fix_e303_excessive_blank_lines(lines):
    """Fix E303: remove excessive blank lines (more than 2 in a row)"""
    fixed = 0
    i = 0
    while i < len(lines):
        print(".")
        # Count consecutive blank lines
        blank_count = 0
        start = i
        while i < len(lines) and lines[i].strip() == '':
            blank_count += 1
            i += 1
        
        # If more than 2 consecutive blank lines, reduce to 2
        if blank_count > 2:
            # Remove excess blank lines
            lines_to_remove = blank_count - 2
            for _ in range(lines_to_remove):
                lines.pop(start)
            fixed += 1
        else:
            i = start + blank_count
    
    return lines, fixed

def fix_file(filepath):
    """Fix both E251 and E303 in a file"""
    path = Path(filepath)
    if not path.exists():
        return 0, 0
    
    try:
        content = path.read_text(encoding='utf-8')
        lines = content.split('\n')
        original_lines = lines[:]
        
        # Fix E251 (parameter spacing)
        lines, e251_fixed = fix_e251_parameter_spacing(lines)
        
        # Fix E303 (excessive blank lines)
        lines, e303_fixed = fix_e303_excessive_blank_lines(lines)
        
        # Write back if changes made
        if lines != original_lines:
            path.write_text('\n'.join(lines), encoding='utf-8')
        
        return e251_fixed, e303_fixed
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0, 0

# Find all Python files in scripts/agent
agent_dir = Path('scripts/agent')
total_e251 = 0
total_e303 = 0

for py_file in sorted(agent_dir.glob('*.py')):
    if py_file.name.startswith('test_'):
        continue
    e251, e303 = fix_file(py_file)
    if e251 > 0 or e303 > 0:
        print(f"✓ {py_file.name:40} | E251: {e251:3} | E303: {e303:2}")
        total_e251 += e251
        total_e303 += e303

print("\n")
print("-" * 70)
print(f"Total fixed: E251: {total_e251:4} | E303: {total_e303:3}")
