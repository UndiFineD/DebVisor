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

"""Auto-fix common flake8 whitespace issues."""
from pathlib import Path

def fix_trailing_whitespace(content):
    """Fix W293: blank line contains whitespace."""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line and line.strip() == '':
            lines[i] = ''
    return '\n'.join(lines)

def fix_missing_newline_at_end(content):
    """Fix W292: no newline at end of file."""
    if content and not content.endswith('\n'):
        return content + '\n'
    return content

def fix_trailing_blank_lines(content):
    """Fix W391: blank line at end of file."""
    while content.endswith('\n\n'):
        content = content[:-1]
    return content

def process_file(file_path):
    """Process a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, IsADirectoryError):
        return False

    original = content
    content = fix_trailing_whitespace(content)
    content = fix_trailing_blank_lines(content)
    content = fix_missing_newline_at_end(content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        return True
    return False

# Process Python files
for py_file in Path('.').rglob('*.py'):
    if any(skip in py_file.parts for skip in ['.git', '__pycache__', '.venv', 'venv']):
        continue
    if process_file(py_file):
        print(f"Fixed: {py_file}")

print("Whitespace cleanup complete!")
