#!/usr/bin/env python3
"""Fix markdown linting issues in RUNNER_SETUP_GUIDE.md"""

import re

# Read the file
with open('docs/RUNNER_SETUP_GUIDE.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Process the file
output = []
i = 0
fence_stack = []  # Track if we're inside a code block

while i < len(lines):
    line = lines[i]

    # Fix ```text to ```
    if line.strip() == '```text':
        output.append('```\n')
        i += 1
        fence_stack.pop() if fence_stack else None
        continue

    # Handle code fences
    if line.strip().startswith('```'):
        # Determine if this is a closing fence
        is_closing = line.strip() == '```' and fence_stack

        # Add blank line before if needed
        if output and output[-1].strip() != '':
            # Check if previous line is not a heading or blank
            if not output[-1].startswith('#'):
                output.append('\n')

        output.append(line)

        # If this is an opening fence (has language or is opening a block)
        if not is_closing:
            fence_stack.append(True)

            # If this is a bare opening fence without language
            if line.strip() == '```' and i < len(lines):
                next_line = lines[i]
                # Check if next line is content (not a fence)
                if next_line.strip() and not next_line.startswith('```'):
                    # Try to detect language from content
                    if any(kw in next_line for kw in ['$', 'powershell', 'Get-', 'Set-', '.ps1', ':\\']):
                        output[-1] = '```powershell\n'
                    elif any(kw in next_line for kw in ['#!/', 'bash', 'mkdir', 'cd ', '.sh']):
                        output[-1] = '```bash\n'
                    elif any(kw in next_line for kw in ['python', 'import ', 'def ', 'class ']):
                        output[-1] = '```python\n'
                    elif any(kw in next_line for kw in ['{', '":', 'json']):
                        output[-1] = '```json\n'
        else:
            # This is a closing fence
            fence_stack.pop()

            # Ensure blank line after closing fence if followed by content
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                # If next line is not blank and not a heading/list, add blank line
                if next_line.strip() and not next_line.startswith('#') and not next_line.startswith('-'):
                    output.append('\n')

        i += 1
        continue

    output.append(line)
    i += 1

# Join and write back
content = ''.join(output)

# Final cleanup: fix multiple blank lines
content = re.sub(r'\n\n\n+', '\n\n', content)

with open('docs/RUNNER_SETUP_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed markdown formatting in RUNNER_SETUP_GUIDE.md")
