#!/usr/bin/env python3
"""
Auto-fix MyPy errors.
Usage: python scripts/auto_fix_mypy.py <file_path>
"""

import sys
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

def run_mypy(file_path: str) -> List[str]:
    """Run mypy on a file and return lines."""
    cmd = ["mypy", file_path, "--show-column-numbers", "--no-error-summary"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.stdout.splitlines()
    except FileNotFoundError:
        print("Error: mypy not found. Please install it.")
        sys.exit(1)

def fix_missing_return_type(file_path: str, line_num: int) -> bool:
    """Attempt to fix missing return type annotation."""
    path = Path(file_path)
    lines = path.read_text(encoding="utf-8").splitlines()
    
    if line_num > len(lines):
        return False
    
    # Adjust for 0-based index
    idx = line_num - 1
    line = lines[idx]
    
    # Check if it's a function definition
    if "def " not in line:
        # Might be a multiline def, or decorator. 
        # Simple heuristic: look back a few lines
        return False

    # Check if it already has a return annotation
    if "->" in line:
        return False

    # Check if function body has 'return' with value
    # This is hard without parsing. 
    # We will assume if mypy says "missing return type", we can add -> None 
    # IF we verify it doesn't return anything.
    # For now, let's just add `-> None` if it ends with `):` or `)`
    
    # Regex to find end of function signature
    # This is very naive and works for single-line defs
    if line.strip().endswith(":"):
        # def foo(self): -> def foo(self) -> None:
        new_line = line.replace(":", " -> None:")
        lines[idx] = new_line
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Fixed line {line_num}: Added -> None")
        return True
    
    return False

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/auto_fix_mypy.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    print(f"Analyzing {file_path}...")
    
    errors = run_mypy(file_path)
    
    fixed_count = 0
    for error in errors:
        # Parse error: file:line:col: error: message [code]
        match = re.match(r"([^:]+):(\d+):(\d+): error: (.*) \[(.*)\]", error)
        if not match:
            continue
            
        fpath, line, col, msg, code = match.groups()
        
        if fpath != file_path:
            continue
            
        if code == "no-untyped-def" and "return type annotation" in msg:
            if fix_missing_return_type(fpath, int(line)):
                fixed_count += 1
                
    print(f"Applied {fixed_count} fixes.")
    if fixed_count > 0:
        print("Please verify changes.")

if __name__ == "__main__":
    main()
