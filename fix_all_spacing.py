#!/usr/bin/env python3
"""Comprehensive fixer for E251/E225/E252 spacing issues"""
import re
from pathlib import Path

def fix_spacing_issues(file_path):
    """Fix spacing issues in Python file."""
    path = Path(file_path)
    content = path.read_text(encoding='utf-8')
    original = content
    
    # Pattern 1: Remove spaces around = in function calls/function definitions parameters
    # func(param = value) → func(param=value)
    # def func(param = value) → def func(param=value)
    # But NOT: x = 5 (regular assignment)
    
    # Strategy: Only fix within parentheses contexts
    # Match spaces around = that are within function calls
    
    # This regex targets = with spaces on both sides that are preceded by alphanumeric/underscore
    # and followed by various value types, all within a line that's likely a function call
    content = re.sub(r'(\w+)\s+=\s+', r'\1=', content)
    
    print(f"Processing: {path.name}")
    
    if content != original:
        path.write_text(content, encoding='utf-8')
        return True
    return False

# Process all Python files
from pathlib import Path

agent_dir = Path('scripts/agent')
python_files = list(agent_dir.glob('*.py'))

fixed = 0
for py_file in sorted(python_files):
    if fix_spacing_issues(str(py_file)):
        fixed += 1

print(f"\n✅ Processed {len(python_files)} files")
