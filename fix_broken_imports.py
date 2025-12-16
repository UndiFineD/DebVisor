#!/usr/bin/env python3
"""Fix broken imports from the batch fix"""

from pathlib import Path
import re

def fix_broken_imports(file_path: Path):
    """Fix broken import lines"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix "from ... import" with nothing after it
    content = re.sub(r'from\s+\S+\s+import\s*\n', '', content)
    
    # Fix dangling commas at end of import
    content = re.sub(r'from\s+([^\s]+)\s+import\s+,', 'from \\1 import', content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    agent_dir = Path('scripts/agent')
    
    # Files with known syntax errors
    broken_files = [
        'test_agent_test_utils_comprehensive.py',
        'test_agent_tests_comprehensive.py',
        'test_agent_tests_improvements_comprehensive.py',
        'test_base_agent_improvements_comprehensive.py',
        'test_generate_agent_reports_comprehensive.py',
        'test_generate_agent_reports_improvements_comprehensive.py',
    ]
    
    fixed = 0
    for fname in broken_files:
        fpath = agent_dir / fname
        if fpath.exists():
            if fix_broken_imports(fpath):
                print(f"Fixed {fname}")
                fixed += 1
            else:
                print(f"Checked {fname} - no fixes needed")
    
    print(f"\nTotal files checked: {len(broken_files)}")

if __name__ == '__main__':
    main()
