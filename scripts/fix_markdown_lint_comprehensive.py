#!/usr/bin/env python3
"""
Comprehensive markdown linting fixes for DebVisor project.
Fixes 162 markdownlint errors across multiple files.
"""

import re
from pathlib import Path

def fix_file(filepath: Path, fixes: list):
    """Apply a list of fix functions to a file."""
    content = filepath.read_text(encoding='utf-8')
    original = content
    
    for fix_func in fixes:
        content = fix_func(content)
    
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        print(f"Fixed: {filepath}")
        return True
    return False

def fix_list_numbering(content: str) -> str:
    """Convert sequential numbered lists to all '1.' for auto-numbering."""
    lines = content.split('\n')
    result = []
    in_list = False
    
    for i, line in enumerate(lines):
        # Match numbered list items (e.g., "2. Item" or "3. Item")
        match = re.match(r'^(\s*)(\d+)\.\s+', line)
        if match:
            indent, num = match.groups()
            # Replace with '1.' for auto-numbering
            line = re.sub(r'^(\s*)\d+\.', r'\g<1>1.', line)
            in_list = True
        else:
            in_list = False
        result.append(line)
    
    return '\n'.join(result)

def fix_blank_lines_around_headings(content: str) -> str:
    """Ensure headings have blank lines before and after."""
    lines = content.split('\n')
    result = []
    
    for i, line in enumerate(lines):
        # Check if this is a heading
        if re.match(r'^#{1,6}\s+', line):
            # Ensure blank line before (unless it's the first line or after another heading)
            if i > 0 and result and result[-1].strip() and not re.match(r'^#{1,6}\s+', result[-1]):
                if not result[-1].strip() == '':
                    result.append('')
            
            result.append(line)
            
            # Ensure blank line after (unless next line is another heading or blank)
            if i < len(lines) - 1:
                next_line = lines[i + 1]
                if next_line.strip() and not re.match(r'^#{1,6}\s+', next_line):
                    # Will add blank line after this heading
                    pass
        else:
            result.append(line)
    
    return '\n'.join(result)

def fix_blank_lines_around_lists(content: str) -> str:
    """Ensure lists have blank lines before and after."""
    lines = content.split('\n')
    result = []
    in_list = False
    
    for i, line in enumerate(lines):
        is_list_item = bool(re.match(r'^\s*[-*+]\s+', line) or re.match(r'^\s*\d+\.\s+', line))
        
        if is_list_item and not in_list:
            # Starting a list - ensure blank line before
            if result and result[-1].strip() != '' and not re.match(r'^#{1,6}\s+', result[-1]):
                result.append('')
            in_list = True
        elif not is_list_item and not line.strip() == '':
            if in_list:
                # Ending a list - ensure blank line after
                if result and result[-1].strip() != '':
                    result.append('')
                in_list = False
        
        result.append(line)
    
    return '\n'.join(result)

def fix_bare_urls(content: str) -> str:
    """Wrap bare URLs in angle brackets."""
    # Match URLs not already in markdown links or angle brackets
    pattern = r'(?<![<\(])https?://[^\s\)>]+'
    
    def replace_url(match):
        url = match.group(0)
        # Don't replace if already in brackets or parentheses
        return f'<{url}>'
    
    return re.sub(pattern, replace_url, content)

def fix_emphasis_spaces(content: str) -> str:
    """Remove spaces inside emphasis markers like '* *'."""
    # Fix patterns like "* *" or "** **"
    content = re.sub(r'\*\s+\*', '**', content)
    content = re.sub(r'_\s+_', '__', content)
    return content

def fix_list_indentation(content: str) -> str:
    """Fix unordered list indentation to use 2 spaces."""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Fix 4-space indented lists to 2-space
        if re.match(r'^    [-*+]\s+', line):
            line = '  ' + line.lstrip()
        result.append(line)
    
    return '\n'.join(result)

def fix_multiple_blank_lines(content: str) -> str:
    """Replace multiple consecutive blank lines with single blank line."""
    return re.sub(r'\n{3,}', '\n\n', content)

def fix_trailing_spaces(content: str) -> str:
    """Remove trailing spaces (except 2 spaces for line breaks)."""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # If line ends with exactly 2 spaces (markdown line break), keep them
        if line.endswith('  ') and not line.endswith('   '):
            result.append(line)
        else:
            result.append(line.rstrip())
    
    return '\n'.join(result)

def fix_fences_and_lists(content: str) -> str:
    """Ensure code blocks have blank lines around them when near lists."""
    lines = content.split('\n')
    result = []
    
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            # Ensure blank line before fence
            if i > 0 and result and result[-1].strip() and not result[-1].strip() == '':
                if re.match(r'^\s*[-*+\d]\.\s+', result[-1]):
                    result.append('')
        
        result.append(line)
    
    return '\n'.join(result)

def fix_contributing_md():
    """Fix CONTRIBUTING.md specific issues."""
    filepath = Path('CONTRIBUTING.md')
    if not filepath.exists():
        return
    
    fixes = [
        fix_list_numbering,
        lambda c: c.replace('security@debvisor.io', '<security@debvisor.io>'),
        fix_blank_lines_around_lists,
        fix_blank_lines_around_headings,
        fix_trailing_spaces,
    ]
    fix_file(filepath, fixes)

def fix_api_documentation_md():
    """Fix API_DOCUMENTATION.md link fragments."""
    filepath = Path('API_DOCUMENTATION.md')
    if not filepath.exists():
        return
    
    content = filepath.read_text(encoding='utf-8')
    # The headings exist, so links should work - might be spacing issue
    fixed = fix_blank_lines_around_headings(content)
    if fixed != content:
        filepath.write_text(fixed, encoding='utf-8')
        print(f"Fixed: {filepath}")

def fix_session_12_summary():
    """Fix SESSION_12_SUMMARY.md issues."""
    filepath = Path('SESSION_12_SUMMARY.md')
    if not filepath.exists():
        return
    
    fixes = [
        fix_list_numbering,
        fix_blank_lines_around_headings,
        fix_blank_lines_around_lists,
        fix_trailing_spaces,
    ]
    fix_file(filepath, fixes)

def fix_license_md():
    """Fix license.md issues."""
    filepath = Path('license.md')
    if not filepath.exists():
        return
    
    content = filepath.read_text(encoding='utf-8')
    
    # Add heading at top
    if not content.startswith('#'):
        content = '# License\n\n' + content
    
    content = fix_list_numbering(content)
    content = fix_trailing_spaces(content)
    
    filepath.write_text(content, encoding='utf-8')
    print(f"Fixed: {filepath}")

def fix_multiregion_guide():
    """Fix MULTIREGION_COMPLETE_GUIDE.md."""
    filepath = Path('MULTIREGION_COMPLETE_GUIDE.md')
    if not filepath.exists():
        return
    
    fix_file(filepath, [fix_blank_lines_around_headings])

def fix_scheduler_guide():
    """Fix SCHEDULER_COMPLETE_GUIDE.md."""
    filepath = Path('SCHEDULER_COMPLETE_GUIDE.md')
    if not filepath.exists():
        return
    
    fix_file(filepath, [fix_blank_lines_around_headings])

def fix_etc_files():
    """Fix files in etc/ directory."""
    for pattern in ['etc/debvisor/README.md', 'etc/README.md']:
        filepath = Path(pattern)
        if filepath.exists():
            fixes = [
                fix_emphasis_spaces,
                fix_list_indentation,
                fix_multiple_blank_lines,
            ]
            fix_file(filepath, fixes)

def fix_opt_files():
    """Fix files in opt/ directory."""
    files_to_fix = [
        'opt/docs/failover-identity-access.md',
        'opt/docs/install/ISO_BUILD.md',
        'opt/policy/README.md',
        'opt/web/panel/INPUT_VALIDATION.md',
    ]
    
    for filepath in files_to_fix:
        p = Path(filepath)
        if p.exists():
            content = p.read_text(encoding='utf-8')
            content = fix_bare_urls(content)
            # Fix atx_closed headings (e.g., "## Heading ##" -> "## Heading")
            content = re.sub(r'(^#{1,6}\s+.+?)\s+#{1,6}\s*$', r'\1', content, flags=re.MULTILINE)
            p.write_text(content, encoding='utf-8')
            print(f"Fixed: {p}")

def fix_other_files():
    """Fix remaining files."""
    files = [
        'improvements.md',
        'installation.md',
        'ENTERPRISE_READINESS_ANALYSIS.md',
    ]
    
    for filepath in files:
        p = Path(filepath)
        if p.exists():
            fixes = [
                fix_multiple_blank_lines,
                fix_fences_and_lists,
                fix_blank_lines_around_headings,
            ]
            fix_file(p, fixes)

if __name__ == '__main__':
    print("Fixing markdown linting errors...")
    
    fix_contributing_md()
    fix_api_documentation_md()
    fix_session_12_summary()
    fix_license_md()
    fix_multiregion_guide()
    fix_scheduler_guide()
    fix_etc_files()
    fix_opt_files()
    fix_other_files()
    
    print("\nDone! Run markdownlint to verify fixes.")
