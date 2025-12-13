# Planning Report: scripts\fix_enum_spacing.py

Generated: 2025-12-13T15:10:42.957394
Status: INVALID

## File Structure Validation

### Issues Found

| Type | Line | Message |
|------|------|---------|
| incorrect_header | 1 | Header line incorrect: got '#!/usr/bin/env python3', expected '# Copyright (c) 2025 DebVisor contributors' |
| incorrect_header | 2 | Header line incorrect: got '"""Fix spacing in Enum assignments"""', expected '# Licensed under the Apache License, Version 2.0 (the "License");' |
| incorrect_header | 3 | Header line incorrect: got '', expected '# you may not use this file except in compliance with the License.' |
| incorrect_header | 4 | Header line incorrect: got 'import re', expected '# You may obtain a copy of the License at' |
| incorrect_header | 5 | Header line incorrect: got '', expected '#     [http://www.apache.org/licenses/LICENSE-2.0'](http://www.apache.org/licenses/LICENSE-2.0') |
| incorrect_header | 6 | Header line incorrect: got 'with open('opt/services/backup/backup_intelligence.py', 'r') as f:', expected '# Unless required by applicable law or agreed to in writing, software' |
| incorrect_header | 7 | Header line incorrect: got '    content = f.read()', expected '# distributed under the License is distributed on an "AS IS" BASIS,' |
| incorrect_header | 8 | Header line incorrect: got '', expected '# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.' |
| incorrect_header | 9 | Header line incorrect: got '# Fix Enum assignments - they need spaces around =', expected '# See the License for the specific language governing permissions and' |
| incorrect_header | 10 | Header line incorrect: got 'enum_fixes = [', expected '# limitations under the License.' |
| missing_section | - | Missing 'Description' section. Should be in docstring after license header. |
| missing_section | - | Missing 'Changelog' section. Should be in docstring after license header. |
| missing_section | - | Missing 'Suggested Fixes' section. Should be in docstring after license header. |
| missing_section | - | Missing 'Improvements' section. Should be in docstring after license header. |

## Markdown Linting Awareness

⚠️ **Generated .md files should comply with these rules:**

### MD022: blanks-around-headings

- **Issue**: Headings should be surrounded by blank lines

- **Fix**: Add blank lines before and after headings

### MD034: no-bare-urls

- **Issue**: Bare URL used

- **Fix**: Wrap URLs in markdown link format: [URL](URL)

### MD038: no-space-in-code

- **Issue**: Spaces inside code span delimiters

- **Fix**: Remove spaces: change ` code ` to `code`

### MD047: single-trailing-newline

- **Issue**: Files should end with a single newline character

- **Fix**: Add a single newline (\n) at the end of the file

## Required Structure

Each code file should have the following structure:

```python
#!/usr/bin/env python3  (shebang for .py files)
# [LICENSE_HEADER - 10 lines of Apache 2.0 license as comments]

"""
Module description and purpose.

## Description
Detailed description of what this file does.

## Changelog
- Version X.X.X: Description of changes
- Version X.X.Y: Description of changes

## Suggested Fixes
- Improvement 1
- Improvement 2

## Improvements
- Enhancement 1
- Enhancement 2
"""

# =====================================================
# [Actual code starts here]
# =====================================================
```python

## Fix Proposals

### To Fix This File

1. Add shebang at line 1: `#!/usr/bin/env python3`

2. Add license header (lines 2-11)

3. Add module docstring with required sections:

   - Description

   - Changelog

   - Suggested Fixes

   - Improvements

4. Separate docstring from code with blank line and comment divider

5. Ensure generated .md reports comply with markdown linting rules:

   - **MD034**: Wrap bare URLs in links: `[URL](URL)`

   - **MD047**: Add trailing newline at end of file

   - **MD022**: Add blank lines around headings

   - **MD038**: Remove spaces in code spans: `` `code` `` not `` ` code ` ``

### Example Template

```python
#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     [http://www.apache.org/licenses/LICENSE-2.0]([http://www.apache.org/licenses/LICENSE-2.](http://www.apache.org/licenses/LICENSE-2.)0)
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Brief description of module.

## Description
Longer description of what this module does.

## Changelog
- 1.0.0: Initial version

## Suggested Fixes
- None currently identified

## Improvements
- Future enhancements
"""

# =====================================================
# Implementation
# =====================================================

# Your code here...
```python

## Implementation Status

Mark items as complete with ✅ emoji:
