import os
import re
from pathlib import Path
from datetime import datetime

def process_file(improvements_path):
    print(f"Processing {improvements_path}")
    try:
        content = improvements_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {improvements_path}: {e}")
        return

    lines = content.splitlines()
    fixed_lines = []
    remaining_lines = []
    
    # Simple state machine to handle list items that might span multiple lines?
    # For now, assuming one line per item as per previous context.
    
    for line in lines:
        if '[Fixed]' in line or '[False Positive]' in line:
            # Clean up the line
            clean_line = line.replace('[Fixed]', '').replace('[False Positive]', '').strip()
            # Remove leading markdown list markers
            clean_line = re.sub(r'^[-*]\s+', '', clean_line)
            # Add status
            status = "Fixed" if '[Fixed]' in line else "False Positive"
            fixed_lines.append(f"{clean_line} ({status})")
        else:
            remaining_lines.append(line)
            
    # Move to changes.md
    if fixed_lines:
        changes_path = improvements_path.with_name(improvements_path.name.replace('.improvements.md', '.changes.md'))
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        new_changes = f"\n## [{date_str}]\n"
        for item in fixed_lines:
            new_changes += f"- {item}\n"
            
        if changes_path.exists():
            changes_content = changes_path.read_text(encoding='utf-8')
            # Append to end
            changes_path.write_text(changes_content + new_changes, encoding='utf-8')
        else:
            changes_path.write_text(f"# Changes\n{new_changes}", encoding='utf-8')
            
        # Update improvements.md
        # Remove empty sections if they become empty?
        # For now just write back remaining lines.
        # We might want to clean up multiple newlines.
        new_content = '\n'.join(remaining_lines)
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)
        improvements_path.write_text(new_content, encoding='utf-8')
        print(f"Moved {len(fixed_lines)} items to {changes_path.name}")

    # Suggest new improvements
    # Infer source file
    # pattern: name.improvements.md -> name.py
    source_name = improvements_path.name.replace('.improvements.md', '.py')
    source_path = improvements_path.with_name(source_name)
    
    if not source_path.exists():
        # Try without the 'test_' prefix if it's a test file? No, usually 1:1
        # Maybe it's a .sh file?
        source_name_sh = improvements_path.name.replace('.improvements.md', '.sh')
        source_path_sh = improvements_path.with_name(source_name_sh)
        if source_path_sh.exists():
            source_path = source_path_sh
        else:
            # print(f"Source file {source_path} not found.")
            return

    try:
        source_content = source_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading source {source_path}: {e}")
        return

    suggestions = []
    
    # Basic Analysis
    lines_count = len(source_content.splitlines())
    
    if lines_count > 300:
        suggestions.append("- Refactor: File is large (>300 lines), consider splitting.")
        
    if 'TODO' in source_content or 'FIXME' in source_content:
        suggestions.append("- Address TODO/FIXME comments.")
        
    if 'except Exception:' in source_content or 'except:' in source_content:
        suggestions.append("- Improve exception handling: Avoid broad `except` clauses.")
        
    if 'print(' in source_content and 'logging' not in source_content and not source_name.startswith('test_'):
        suggestions.append("- Replace `print` statements with `logging`.")
        
    if 'def ' in source_content and '"""' not in source_content:
         suggestions.append("- Add docstrings to functions.")

    if 'type: ignore' in source_content:
        suggestions.append("- Review `type: ignore` comments and try to fix types.")

    # Advanced Checks
    if 'subprocess.run' in source_content and 'check=' not in source_content:
        suggestions.append("- Security: Use `check=True` or `check=False` explicitly in `subprocess.run`.")

    if 'def ' in source_content and '->' not in source_content:
        suggestions.append("- Type Hints: Add return type annotations to functions.")

    if re.search(r'def\s+\w+\s*\(.*=\s*\[\].*\):', source_content):
        suggestions.append("- Bug Risk: Avoid mutable default arguments (e.g., `list=[]`).")

    if re.search(r'def\s+\w+\s*\(.*=\s*\{.*\}.*\):', source_content):
        suggestions.append("- Bug Risk: Avoid mutable default arguments (e.g., `dict={}`).")

    # Check for existing suggestions to avoid duplicates
    current_improvements = improvements_path.read_text(encoding='utf-8')
    new_suggestions = []
    for suggestion in suggestions:
        # Simple check if suggestion is already present
        # Normalize a bit
        check_str = suggestion.strip('- ').split(':')[0] # Check the main part
        if check_str not in current_improvements:
            new_suggestions.append(suggestion)
            
    if new_suggestions:
        with open(improvements_path, 'a', encoding='utf-8') as f:
            # Ensure we have a newline before appending
            if not current_improvements.endswith('\n'):
                f.write('\n')
            # f.write("\n## New Suggestions\n") # Maybe don't add header every time
            for item in new_suggestions:
                f.write(f"{item}\n")
        print(f"Added {len(new_suggestions)} new suggestions to {improvements_path.name}")

def main():
    root = Path('.')
    # Use rglob to find all files recursively
    for path in root.rglob('*.improvements.md'):
        process_file(path)

if __name__ == '__main__':
    main()
