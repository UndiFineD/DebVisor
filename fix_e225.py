#!/usr/bin/env python3
"""Fix E225 errors - missing whitespace around operators"""
import re
from pathlib import Path
import sys

def fix_e225_in_file(file_path):
    """Fix E225 errors in a single file."""
    path = Path(file_path)
    if not path.exists():
        return False
    
    content = path.read_text(encoding='utf-8')
    original = content
    
    # Patterns to fix: missing spaces around operators
    # But be careful not to break slice notation, type hints, etc.
    
    # Fix: a+b → a + b (but not in strings/comments)
    # Fix: a-b → a - b
    # Fix: a*b → a * b
    # Fix: a/b → a / b
    # Fix: a%b → a % b
    # Fix: a**b → a ** b (but preserve *args and **kwargs)
    
    # Pattern 1: Missing space after binary operators (before them too)
    # Match operators surrounded by alphanumeric/underscore/close bracket but without spaces
    
    # a+b or a +b or a+ b → a + b
    content = re.sub(r'(\w|\]|\))\+(\w)', r'\1 + \2', content)
    
    # a-b (but not hyphen in names or negative numbers)
    # Only fix when clearly a binary operator
    content = re.sub(r'(\w|\]|\))-(?![\w>]|$|$)(\w|\[)', r'\1 - \2', content)
    
    # a*b (but preserve **kwargs and *args)
    # Only fix single * not preceded or followed by another *
    content = re.sub(r'(\w|\]|\))\*(?!\*)(\w|\[)', r'\1 * \2', content)
    
    # a/b
    content = re.sub(r'(\w|\]|\))/(\w|\[)', r'\1 / \2', content)
    
    # a%b
    content = re.sub(r'(\w|\]|\))%(\w)', r'\1 % \2', content)
    
    # a**b (but not **kwargs)
    # Preserve ** when followed by a word at start of context (parameter)
    content = re.sub(r'(\w|\]|\))\*\*(?!\w|})(\w|\()', r'\1 ** \2', content)
    
    # a&b
    content = re.sub(r'(\w|\]|\))&(\w|\()', r'\1 & \2', content)
    
    # a|b
    content = re.sub(r'(\w|\]|\))\|(\w|\()', r'\1 | \2', content)
    
    # a^b
    content = re.sub(r'(\w|\]|\))\^(\w)', r'\1 ^ \2', content)
    
    # a<<b
    content = re.sub(r'(\w|\]|\))<<(\w)', r'\1 << \2', content)
    
    # a>>b
    content = re.sub(r'(\w|\]|\))>>(\w)', r'\1 >> \2', content)
    
    if content != original:
        path.write_text(content, encoding='utf-8')
        return True
    
    return False

def main():
    """Fix E225 errors across all agent scripts."""
    agent_dir = Path('scripts/agent')
    
    if not agent_dir.exists():
        print("Error: scripts/agent directory not found")
        sys.exit(1)
    
    python_files = list(agent_dir.glob('*.py'))
    fixed_count = 0
    
    for py_file in sorted(python_files):
        if fix_e225_in_file(str(py_file)):
            print(f"✓ {py_file.name}")
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count}/{len(python_files)} files with E225 errors")

if __name__ == '__main__':
    main()
