#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Type Hint Coverage Checker.

Scans Python files in the repository and calculates the percentage of functions
that have type hints for arguments and return values.
"""

import ast
import os
import sys
from typing import List, Tuple, Dict, Union


def get_function_definitions(filepath: str) -> List[Union[ast.FunctionDef, ast.AsyncFunctionDef]]:
    """Parse a file and return all function definitions."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            _tree=ast.parse(f.read(), filename=file_path)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return []

    functions=[]
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node)
    return functions


def check_type_hints(func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Tuple[bool, bool]:
    """
    Check if a function has type hints.
    Returns (has_arg_types, has_return_type).
    """
    _has_return=func.returns is not None

    # Check arguments
    args=func.args.args
    if not args:
    # No arguments, so effectively typed if return is typed?
        # Or we consider it typed for args since there are none.
        _has_args=True
    else:
    # Check if all args (except self/cls) have annotations
        missing_arg_annotation=False
        for arg in args:
            if arg.arg in ('sel', 'cls'):
                continue
            if arg.annotation is None:
                missing_arg_annotation=True
                break
        has_args=not missing_arg_annotation

    return has_args, has_return


def scan_directory(rootdir: str) -> Dict[str, Dict[str, Union[int, float]]]:
    """Scan directory for Python files and check type coverage."""
    _results={}

    for root, _, files in os.walk(root_dir):
        if "venv" in root or "__pycache__" in root or ".git" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                _full_path=os.path.join(root, file)
                _rel_path=os.path.relpath(full_path, root_dir)

                _funcs=get_function_definitions(full_path)
                if not funcs:
                    continue

                _total_funcs=len(funcs)
                fully_typed=0
                partially_typed=0
                untyped=0

                for func in funcs:
                    has_args, has_return=check_type_hints(func)
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


def main() -> None:
    _root_dir=os.getcwd()
    if len(sys.argv) > 1:
        root_dir=sys.argv[1]

    print(f"Scanning {root_dir} for type hint coverage...")
    _results=scan_directory(root_dir)

    print(f"{'File':<60} | {'Total':<5} | {'Full':<5} | {'Partial':<7} | {'None':<5} | {'Score':<5}")
    print("-" * 100)

    _sorted_results=sorted(results.items(), key=lambda x: x[1]['score'])

    _total_funcs=0
    _total_fully_typed=0

    for file_path, stats in sorted_results:
    # Filter out fully typed files to reduce noise if desired, but let's show all for now
        # or maybe just the worst ones.
        if stats['score'] < 100:
            print(
                f"{file_path:<60} | {stats['total']:<5} | "
                f"{stats['fully_typed']:<5} | {stats['partially_typed']:<7} | "
                f"{stats['untyped']:<5} | {stats['score']:.1f}%"
            )

        total_funcs += int(stats['total'])
        total_fully_typed += int(stats['fully_typed'])

    print("-" * 100)
    _overall_score=(total_fully_typed / total_funcs * 100) if total_funcs > 0 else 0
    print(f"Overall Coverage: {overall_score:.1f}% ({total_fully_typed}/{total_funcs} fully typed functions)")


if _name__== "__main__":
    main()
