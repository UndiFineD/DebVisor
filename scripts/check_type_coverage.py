#!/usr/bin/env python3
"""
Type Hint Coverage Checker.

Scans Python files in the repository and calculates the percentage of functions
that have type hints for arguments and return values.
"""

import ast
import os
import sys
from typing import List, Tuple, Dict

def get_function_definitions(file_path: str) -> List[ast.FunctionDef]:
    """Parse a file and return all function definitions."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return []

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node)
    return functions

def check_type_hints(func: ast.FunctionDef) -> Tuple[bool, bool]:
    """
    Check if a function has type hints.
    Returns (has_arg_types, has_return_type).
    """
    has_return = func.returns is not None
    
    # Check arguments
    args = func.args.args
    if not args:
        # No arguments, so effectively typed if return is typed? 
        # Or we consider it typed for args since there are none.
        has_args = True
    else:
        # Check if all args (except self/cls) have annotations
        missing_arg_annotation = False
        for arg in args:
            if arg.arg in ('self', 'cls'):
                continue
            if arg.annotation is None:
                missing_arg_annotation = True
                break
        has_args = not missing_arg_annotation

    return has_args, has_return

def scan_directory(root_dir: str) -> Dict[str, Dict[str, int]]:
    """Scan directory for Python files and check type coverage."""
    results = {}

    for root, _, files in os.walk(root_dir):
        if "venv" in root or "__pycache__" in root or ".git" in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                
                funcs = get_function_definitions(full_path)
                if not funcs:
                    continue
                    
                total_funcs = len(funcs)
                fully_typed = 0
                partially_typed = 0
                untyped = 0
                
                for func in funcs:
                    has_args, has_return = check_type_hints(func)
                    if has_args and has_return:
                        fully_typed += 1
                    elif has_args or has_return:
                        partially_typed += 1
                    else:
                        untyped += 1
                
                results[rel_path] = {
                    "total": total_funcs,
                    "fully_typed": fully_typed,
                    "partially_typed": partially_typed,
                    "untyped": untyped,
                    "score": (fully_typed + 0.5 * partially_typed) / total_funcs * 100 if total_funcs > 0 else 100
                }
                
    return results

def main():
    root_dir = os.getcwd()
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
        
    print(f"Scanning {root_dir} for type hint coverage...")
    results = scan_directory(root_dir)
    
    print(f"{'File':<60} | {'Total':<5} | {'Full':<5} | {'Partial':<7} | {'None':<5} | {'Score':<5}")
    print("-" * 100)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['score'])
    
    total_funcs = 0
    total_fully_typed = 0
    
    for file_path, stats in sorted_results:
        # Filter out fully typed files to reduce noise if desired, but let's show all for now
        # or maybe just the worst ones.
        if stats['score'] < 100:
            print(f"{file_path:<60} | {stats['total']:<5} | {stats['fully_typed']:<5} | {stats['partially_typed']:<7} | {stats['untyped']:<5} | {stats['score']:.1f}%")
        
        total_funcs += stats['total']
        total_fully_typed += stats['fully_typed']

    print("-" * 100)
    overall_score = (total_fully_typed / total_funcs * 100) if total_funcs > 0 else 0
    print(f"Overall Coverage: {overall_score:.1f}% ({total_fully_typed}/{total_funcs} fully typed functions)")

if __name__ == "__main__":
    main()
