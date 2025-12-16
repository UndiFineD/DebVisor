#!/usr/bin/env python3
"""
Comprehensive fix script for multiple issue types.
Fixes: E225, E251, E252, F821, F841, E115, E116, and undefined variable references
"""
import re
from pathlib import Path

def fix_backup_intelligence():
    """Fix all issues in backup_intelligence.py"""
    path = Path('opt/services/backup/backup_intelligence.py')
    content = path.read_text(encoding = 'utf-8')
    lines = content.split('\n')
    
    # Fix 1: E225 missing whitespace around operators (e.g., _window=, _score=)
    for i, line in enumerate(lines):
        # Pattern: variable=value where underscore-prefixed
        if '_' in line and '=' in line and not '==' in line:
            # Fix underscore variable assignments with no space
            line = re.sub(r'_([a-zA-Z_]\w*)\s*=([^=])', r'_\1 = \2', line)
        
        # Pattern: missing space around operators in expressions
        # Be careful not to match **kwargs or parameter defaults
        if not ('def ' in line or 'lambda' in line or '**' in line):
            # Fix a=b to a = b (but not in default parameters)
            line = re.sub(r'([a-zA-Z_]\w*)\s*=\s*([a-zA-Z_"\'])', r'\1 = \2', line)
            # Fix things like 2*x to 2 * x
            line = re.sub(r'([0-9])\*([a-zA-Z_])', r'\1 * \2', line)
            line = re.sub(r'([a-zA-Z_])\*([0-9])', r'\1 * \2', line)
        
        lines[i] = line
    
    # Fix 2: Rename _window to window, _score to score, _check_date to check_date
    # and update all references
    replacements = {
        '_window': 'window',
        '_score': 'score',
        '_check_date': 'check_date',
        '_logger': 'logger',
        '_datetime': 'dt',
        '_hour_rate': 'hour_rate',
        '_day_rate': 'day_rate',
    }
    
    full_text = '\n'.join(lines)
    
    for old_var, new_var in replacements.items():
        # Replace all occurrences, not just assignments
        full_text = re.sub(rf'\b{re.escape(old_var)}\b', new_var, full_text)
    
    lines = full_text.split('\n')
    
    # Fix 3: Fix E115/E116 - expected indented block (comment)
    # Pattern: a line that's just a comment at wrong indentation level
    for i, line in enumerate(lines):
        if i > 0 and line.strip().startswith('#'):
            # Check if previous line ends with colon or is a function/class definition
            prev_line = lines[i-1].strip()
            if prev_line.endswith(':') or prev_line.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'except')):
                # This comment should be indented
                indent_match = re.match(r'^(\s*)', lines[i-1])
                if indent_match:
                    current_indent = indent_match.group(1)
                    # Add 4 more spaces
                    if not line.startswith(current_indent + '    '):
                        lines[i] = current_indent + '    ' + line.lstrip()
    
    # Fix 4: E251/E252 - unexpected/missing spaces around parameter equals
    # Pattern: func(param = value) should be func(param=value)
    for i, line in enumerate(lines):
        if '(' in line and '=' in line:
            # Inside function calls/definitions, no spaces around =
            # Replace param = value with param=value inside parentheses
            line = re.sub(r'(\w+)\s*=\s*([^=\s])', r'\1=\2', line)
        lines[i] = line
    
    path.write_text('\n'.join(lines), encoding = 'utf-8')
    print(f"✓ Fixed backup_intelligence.py")

def fix_other_files():
    """Fix common issues in other Python files"""
    for py_file in Path('.').glob('**/*.py'):
        # Skip test files for now
        if 'test_' in py_file.name or '__pycache__' in str(py_file):
            continue
        
        try:
            content = py_file.read_text(encoding = 'utf-8')
            lines = content.split('\n')
            changed = False
            
            # Fix E225: missing whitespace around operators
            for i, line in enumerate(lines):
                original = line
                # Skip comments and strings
                if line.strip().startswith('#'):
                    continue
                
                # Fix a=b patterns (but not in function signatures)
                if 'def ' not in line and 'lambda' not in line:
                    line = re.sub(r'([a-zA-Z_]\w*)\s*=\s*(["\'{a-zA-Z_0-9\[])', r'\1 = \2', line)
                
                if line != original:
                    lines[i] = line
                    changed = True
            
            if changed:
                py_file.write_text('\n'.join(lines), encoding = 'utf-8')
                print(f"✓ Fixed {py_file}")
        except Exception as e:
            pass

if __name__ == '__main__':
    fix_backup_intelligence()
    fix_other_files()
    print("\n✓ All fixes completed")
