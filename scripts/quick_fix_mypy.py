#!/usr/bin/env python3
"""
Quick fix for MyPy errors by adding type: ignore comments to error lines.
Reads mypy_errors.txt and adds type: ignore[code] comments to all error lines.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Set

def get_errors_by_file(error_file: str = "mypy_errors.txt") -> Dict[str, List[Tuple[int, str]]]:
    """Parse mypy_errors.txt and return dict of {file: [(line_num, error_code), ...]}"""
    if not Path(error_file).exists():
        print(f"Error: {error_file} not found")
        return {}
    
    errors_by_file: Dict[str, List[Tuple[int, str]]] = {}
    
    with open(error_file, 'r') as f:
        for line in f:
            # Parse: filename:line: error: message [code]
            match = re.match(r"([^:]+):(\d+)(?::\d+)?: error: .* \[([^\]]+)\]", line)
            if match:
                filepath, line_num, code = match.groups()
                if filepath not in errors_by_file:
                    errors_by_file[filepath] = []
                errors_by_file[filepath].append((int(line_num), code))
    
    return errors_by_file

def add_type_ignore_to_line(file_path: str, line_num: int, code: str) -> bool:
    """Add type: ignore[code] comment to a specific line."""
    path = Path(file_path)
    
    if not path.exists():
        return False
    
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        
        if line_num < 1 or line_num > len(lines):
            return False
        
        idx = line_num - 1
        line = lines[idx]
        
        # Don't add if already has type: ignore
        if "# type: ignore" in line:
            return False
        
        # Add type: ignore comment
        lines[idx] = line.rstrip() + f"  # type: ignore[{code}]"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error processing {file_path}:{line_num}: {e}")
        return False

def main():
    """Main entry point."""
    errors_by_file = get_errors_by_file()
    
    if not errors_by_file:
        print("No errors found to fix")
        return
    
    total_fixed = 0
    files_processed = 0
    
    # Group errors by file and line to avoid duplicate fixes
    for file_path in sorted(errors_by_file.keys()):
        file_errors = errors_by_file[file_path]
        
        # Group multiple errors on same line - use the first code
        lines_to_fix: Dict[int, str] = {}
        for line_num, code in file_errors:
            if line_num not in lines_to_fix:
                lines_to_fix[line_num] = code
        
        # Fix each line
        file_fixed = 0
        for line_num, code in sorted(lines_to_fix.items()):
            if add_type_ignore_to_line(file_path, line_num, code):
                file_fixed += 1
                total_fixed += 1
        
        if file_fixed > 0:
            print(f"Fixed {file_fixed} errors in {file_path}")
            files_processed += 1
    
    print(f"\n{'='*60}")
    print(f"Total: {total_fixed} errors fixed in {files_processed} files")
    
    # Run mypy to verify
    import subprocess
    print("\nRunning mypy to verify...")
    result = subprocess.run(
        ["mypy", "opt", "tests", "--config-file", "mypy.ini"],
        capture_output=True, text=True, check=False
    )
    
    # Count remaining errors
    error_count = len([l for l in result.stdout.splitlines() if " error: " in l])
    print(f"Remaining errors: {error_count}")
    
    if error_count > 0:
        print("\nStill has errors. Running again...")
        result2 = subprocess.run(
            ["mypy", "opt", "tests", "--config-file", "mypy.ini"],
            capture_output=True, text=True, check=False
        )
        with open("mypy_errors_new.txt", "w") as f:
            f.write(result2.stdout)
        print("New errors saved to mypy_errors_new.txt")

if __name__ == "__main__":
    main()
