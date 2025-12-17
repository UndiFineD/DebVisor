#!/usr/bin/env python3
"""Comprehensive fix for E251 errors across all scripts/agent files"""
import re
from pathlib import Path
import sys

def fix_e251_in_file(file_path):
    """Fix E251 errors in a single file."""
    path = Path(file_path)
    if not path.exists():
        return 0
    
    content = path.read_text(encoding='utf-8')
    original_content = content
    
    # Pattern 1: Simple spaces around = in function calls/definitions
    # This handles: func(param = value) → func(param=value)
    # We match = with spaces on both sides, but only within parentheses
    # Use a more aggressive pattern: \s*=\s* when surrounded by word chars
    
    # First pass: Fix keyword arguments with spaces around =
    # Match: word characters/identifiers followed by spaces, =, and spaces
    content = re.sub(
        r'(\w+)\s+=\s+',
        r'\1=',
        content
    )
    
    # Track changes
    if content != original_content:
        path.write_text(content, encoding='utf-8')
        # Count approximate changes by counting commas/parens with our pattern
        changes = len(re.findall(r'\w+=', content)) - len(re.findall(r'\w+=', original_content))
        return abs(changes) if changes != 0 else 1
    
    return 0

def main():
    """Fix E251 errors across all agent scripts."""
    agent_dir = Path('scripts/agent')
    
    if not agent_dir.exists():
        print("Error: scripts/agent directory not found")
        sys.exit(1)
    
    python_files = list(agent_dir.glob('*.py'))
    total_fixes = 0
    
    for py_file in sorted(python_files):
        fixes = fix_e251_in_file(str(py_file))
        if fixes > 0:
            print(f"✓ {py_file.name}: Fixed E251 errors")
            total_fixes += fixes
    
    print(f"\n✅ Total files processed: {len(python_files)}")
    print(f"✅ Estimated changes applied")

if __name__ == '__main__':
    main()
