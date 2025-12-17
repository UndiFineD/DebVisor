#!/usr/bin/env python3
"""Fix E225 errors - missing whitespace around assignment operators"""
import re
from pathlib import Path

def fix_e225_assignments(file_path):
    """Fix E225 errors for assignment operators."""
    path = Path(file_path)
    content = path.read_text(encoding='utf-8')
    original = content
    
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Skip comments and empty lines
        if line.strip().startswith('#') or not line.strip():
            result.append(line)
            continue
        
        # Check if line has an assignment (but be careful about colons/type hints)
        # Fix: X="value" → X = "value"
        # Fix: X=123 → X = 123
        # Fix: X=[...] → X = [...]
        # But keep: x: str = "value" as is (has proper spacing)
        
        # Pattern: word/identifier/closing bracket followed immediately by = without spaces
        # But NOT if preceded by !=, ==, <=, >=, etc.
        line = re.sub(r'(?<![!<>=])(\w|\]|\))=(?![=])', r'\1 = ', line)
        
        result.append(line)
    
    new_content = '\n'.join(result)
    
    if new_content != original:
        path.write_text(new_content, encoding='utf-8')
        return True
    return False

# Process all Python files
from pathlib import Path

agent_dir = Path('scripts/agent')
python_files = list(agent_dir.glob('*.py'))

fixed = 0
for py_file in sorted(python_files):
    if fix_e225_assignments(str(py_file)):
        print(f"✓ {py_file.name}")
        fixed += 1

print(f"\n✅ Fixed {fixed}/{len(python_files)} files")
