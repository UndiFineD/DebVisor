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
Planning Agent: Validates and enforces code file structure.

Checks that each code file has:
1. LICENSE_HEADER (as comments)
2. Description section (docstring)
3. Changelog section (docstring)
4. Suggested Fixes section (docstring)
5. Improvements section (docstring)
6. Then the actual code

Generates .plan.md reports for each file with structure issues and fix proposals.
Reports include Copilot enhancement prompts for AI-assisted improvements.

## Description
This module provides a Planning Agent that validates and enforces proper code file structure
across a codebase. It ensures all code files follow a consistent format with license headers,
comprehensive docstrings, and proper organization. Generated planning reports include
prompts for GitHub Copilot to provide enhanced analysis and recommendations.

## Changelog
- 1.0.0: Initial implementation with basic structure validation
- 1.1.0: Enhanced docstring parsing for Python files
- 1.2.0: Added support for multiple programming languages
- 1.3.0: Added Copilot enhancement prompts to generated reports

## Suggested Fixes
- Improve error messages for better user guidance
- Add configuration file support for custom validation rules
- Implement auto-fix capabilities for common issues

## Improvements
- Performance optimization for large codebases
- Better integration with CI/CD pipelines
- Enhanced reporting with actionable recommendations
- AI-assisted report enhancement via Copilot prompts
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any, Set
from datetime import datetime
import argparse


def load_codeignore(root: Path) -> Set[str]:
    """Load ignore patterns from .codeignore file."""
    codeignore_path = root / ".codeignore"
    if codeignore_path.exists():
        try:
            content = codeignore_path.read_text(encoding='utf-8')
            return {line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')}
        except Exception as e:
            print(f"Warning: Could not read .codeignore file: {e}")
    return set()


# License header as comments (language-dependent)
LICENSE_HEADER = [
    "Copyright (c) 2025 DebVisor contributors",
    'Licensed under the Apache License, Version 2.0 (the "License");',
    "you may not use this file except in compliance with the License.",
    "You may obtain a copy of the License at",
    "    http://www.apache.org/licenses/LICENSE-2.0",
    "Unless required by applicable law or agreed to in writing, software",
    'distributed under the License is distributed on an "AS IS" BASIS,',
    "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.",
    "See the License for the specific language governing permissions and",
    "limitations under the License.",
]

REQUIRED_SECTIONS = [
    "Description",
    "Changelog",
    "Suggested Fixes",
    "Improvements"
]

MARKDOWN_LINTING_RULES = {
    'MD034': {
        'name': 'no-bare-urls',
        'description': 'Bare URL used',
        'fix': 'Wrap URLs in markdown link format: [URL](URL)'
    },
    'MD047': {
        'name': 'single-trailing-newline',
        'description': 'Files should end with a single newline character',
        'fix': 'Add a single newline (\\n) at the end of the file'
    },
    'MD022': {
        'name': 'blanks-around-headings',
        'description': 'Headings should be surrounded by blank lines',
        'fix': 'Add blank lines before and after headings'
    },
    'MD038': {
        'name': 'no-space-in-code',
        'description': 'Spaces inside code span delimiters',
        'fix': 'Remove spaces: change ` code ` to `code`'
    }
}


class PlanningAgent:
    """Validates code file structure and generates planning reports."""

    SUPPORTED_EXTENSIONS = {'.py', '.sh', '.js', '.ts', '.go', '.rb'}

    def __init__(self, repo_root: str = '.', agents_only: bool = False):
        self.repo_root = Path(repo_root)
        self.agents_only = agents_only
        self.issues: Dict[str, List[Dict[str, Any]]] = {}
        self.ignored_patterns = load_codeignore(self.repo_root)

    def find_code_files(self) -> List[Path]:
        """Recursively find all supported code files."""
        code_files = []
        for ext in self.SUPPORTED_EXTENSIONS:
            code_files.extend(self.repo_root.rglob(f'*{ext}'))

        # Filter to scripts directory if agents_only is True
        if self.agents_only:
            scripts_dir = self.repo_root / 'scripts'
            code_files = [f for f in code_files if f.is_relative_to(scripts_dir)]

        return sorted([f for f in code_files if not self._is_ignored(f)])

    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored."""
        return any(part in self.ignored_patterns for part in path.parts)

    def validate_file_structure(self, file_path: Path) -> Dict[str, Any]:
        """Validate a code file's structure."""
        result = {
            'file': str(file_path.relative_to(self.repo_root)),
            'issues': [],
            'status': 'valid'
        }

        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Check for license header
            header_issues = self._check_license_header(file_path, lines)
            if header_issues:
                result['issues'].extend(header_issues)

            # Check for required sections
            section_issues = self._check_required_sections(file_path, lines)
            if section_issues:
                result['issues'].extend(section_issues)

            # Check file organization
            org_issues = self._check_organization(file_path, lines)
            if org_issues:
                result['issues'].extend(org_issues)

            if result['issues']:
                result['status'] = 'invalid'

        except Exception as e:
            result['issues'].append({
                'type': 'error',
                'message': f"Failed to read file: {str(e)}"
            })
            result['status'] = 'error'

        return result

    def _check_license_header(self, file_path: Path, lines: List[str]) -> List[Dict[str, str]]:
        """Check if file starts with license header."""
        issues = []
        ext = file_path.suffix.lower()

        if ext == '.py':
            comment_char = '#'
        elif ext in {'.sh', '.rb'}:
            comment_char = '#'
        elif ext in {'.js', '.ts', '.go'}:
            comment_char = '//'
        else:
            return []

        # Get expected header lines
        expected_header = [f"{comment_char} {line}" for line in LICENSE_HEADER]

        # For Python files, skip shebang line
        start_line = 0
        if ext == '.py' and lines and lines[0].startswith('#!'):
            start_line = 1

        # Check header lines starting from start_line
        for i, expected in enumerate(expected_header):
            line_idx = start_line + i
            if line_idx >= len(lines):
                issues.append({
                    'type': 'missing_header_line',
                    'line': line_idx + 1,
                    'message': f"Missing license header line: {expected}"
                })
            elif lines[line_idx].strip() != expected.strip():
                issues.append({
                    'type': 'incorrect_header',
                    'line': line_idx + 1,
                    'message': (
                        f"Header line incorrect: got '{lines[line_idx]}', "
                        f"expected '{expected}'"
                    )
                })

        return issues

    def _extract_docstring(self, lines: List[str]) -> str:
        """Extract the module docstring from Python file lines."""
        # Find the first docstring after license header (assume header is ~10 lines)
        start_idx = 0
        for i, line in enumerate(lines):
            if i > 10:  # After license header
                if '"""' in line or "'''" in line:
                    start_idx = i
                    break

        if start_idx == 0:
            return ""

        # Find the quote type
        start_line = lines[start_idx]
        if '"""' in start_line:
            quote = '"""'
        elif "'''" in start_line:
            quote = "'''"
        else:
            return ""

        # Find the end
        docstring_lines = []
        for i in range(start_idx, len(lines)):
            docstring_lines.append(lines[i])
            if i > start_idx and quote in lines[i]:
                break

        return '\n'.join(docstring_lines)

    def _check_required_sections(self, file_path: Path, lines: List[str]) -> List[Dict[str, str]]:
        """Check for required documentation sections."""
        issues = []
        ext = file_path.suffix.lower()

        if ext == '.py':
            # For Python files, check sections within the docstring
            docstring = self._extract_docstring(lines)
            if not docstring:
                issues.append({
                    'type': 'missing_docstring',
                    'message': "Missing module docstring after license header."
                })
                return issues

            # Check each section exists in docstring
            for section in REQUIRED_SECTIONS:
                if f"## {section}" not in docstring:
                    issues.append({
                        'type': 'missing_section',
                        'message': (
                            f"Missing '## {section}' section in docstring. "
                            "Should be in module docstring after license header."
                        )
                    })

            # Check section order if all exist
            if not issues:
                positions = {}
                for section in REQUIRED_SECTIONS:
                    pos = docstring.find(f"## {section}")
                    if pos != -1:
                        positions[section] = pos

                if len(positions) == len(REQUIRED_SECTIONS):
                    sorted_sections = sorted(positions.items(), key=lambda x: x[1])
                    expected_order = REQUIRED_SECTIONS
                    actual_order = [sec for sec, _ in sorted_sections]
                    if actual_order != expected_order:
                        sections_str = ', '.join(expected_order)
                        issues.append({
                            'type': 'section_order',
                            'message': f"Sections out of order in docstring. Expected: {sections_str}"
                        })
        else:
            # For other languages, check sections anywhere (fallback)
            content = '\n'.join(lines)
            for section in REQUIRED_SECTIONS:
                if section not in content:
                    issues.append({
                        'type': 'missing_section',
                        'message': (
                            f"Missing '{section}' section. "
                            "Should be documented in the file."
                        )
                    })

        return issues

    def _check_organization(self, file_path: Path, lines: List[str]) -> List[Dict[str, str]]:
        """Check overall file organization."""
        issues = []
        ext = file_path.suffix.lower()

        # Python-specific checks
        if ext == '.py':
            # Check for shebang at top
            if not lines or not lines[0].startswith('#!'):
                issues.append({
                    'type': 'missing_shebang',
                    'line': 1,
                    'message': "Python files should start with shebang: #!/usr/bin/env python3"
                })

        return issues

    def generate_plan_report(self, file_path: Path, validation: Dict[str, Any]) -> str:
        """Generate a .plan.md report for a file."""
        relative_path = file_path.relative_to(self.repo_root)

        lines = [
            f"# Planning Report: {relative_path}",
            f"Generated: {datetime.now().isoformat()}",
            f"Status: {validation['status'].upper()}",
            "",
            "## File Structure Validation",
            "",
        ]

        if validation['status'] == 'valid':
            lines.append("✅ **File structure is valid**")
        else:
            lines.extend([
                "### Issues Found",
                "",
                "| Type | Line | Message |",
                "|------|------|---------|",
            ])

            for issue in validation['issues']:
                issue_type = issue.get('type', 'unknown')
                line_num = issue.get('line', '-')
                message = issue.get('message', '')
                lines.append(f"| {issue_type} | {line_num} | {message} |")

        lines.extend([
            "",
            "## Markdown Linting Awareness",
            "",
            "⚠️ **Generated .md files should comply with these rules:**",
            "",
        ])

        for code, rule_info in sorted(MARKDOWN_LINTING_RULES.items()):
            lines.extend([
                f"### {code}: {rule_info['name']}",
                f"- **Issue**: {rule_info['description']}",
                f"- **Fix**: {rule_info['fix']}",
                ""
            ])

        lines.extend([
            "## Required Structure",
            "",
            "Each code file should have the following structure:",
            "",
            "```",
            "#!/usr/bin/env python3  (shebang for .py files)",
            "# [LICENSE_HEADER - 10 lines of Apache 2.0 license as comments]",
            "",
            '"""',
            "Module description and purpose.",
            "",
            "## Description",
            "Detailed description of what this file does.",
            "",
            "## Changelog",
            "- Version X.X.X: Description of changes",
            "- Version X.X.Y: Description of changes",
            "",
            "## Suggested Fixes",
            "- Improvement 1",
            "- Improvement 2",
            "",
            "## Improvements",
            "- Enhancement 1",
            "- Enhancement 2",
            '"""',
            "",
            "# =====================================================",
            "# [Actual code starts here]",
            "# =====================================================",
            "```",
            "",
            "## Copilot Improvement Queries",
            "",
            "Use these prompts with GitHub Copilot to enhance the docstring sections:",
            "",
            "### 1. Improve Description Section",
            "```",
            "Review this Python module's current description and suggest improvements:",
            "",
            f"File: {relative_path}",
            "Current Description:",
            "[Insert current ## Description content here]",
            "",
            "Please provide:",
            "1. A more comprehensive and clear description",
            "2. Better organization of information",
            "3. More specific technical details",
            "4. Clear explanation of the module's purpose and scope",
            "```",
            "",
            "### 2. Improve Changelog Section",
            "```",
            "Analyze this Python module's changelog and suggest enhancements:",
            "",
            f"File: {relative_path}",
            "Current Changelog:",
            "[Insert current ## Changelog content here]",
            "",
            "Please provide:",
            "1. More detailed version entries",
            "2. Better categorization of changes (features, fixes, breaking changes)",
            "3. Consistent formatting and style",
            "4. Addition of missing version entries if applicable",
            "```",
            "",
            "### 3. Improve Suggested Fixes Section",
            "```",
            "Review this Python module's suggested fixes and provide better recommendations:",
            "",
            f"File: {relative_path}",
            "Current Suggested Fixes:",
            "[Insert current ## Suggested Fixes content here]",
            "",
            "Please provide:",
            "1. More specific and actionable fix suggestions",
            "2. Prioritized list of improvements",
            "3. Technical details for implementation",
            "4. Potential impact assessment for each fix",
            "```",
            "",
            "### 4. Improve Improvements Section",
            "```",
            "Enhance this Python module's improvements section with better future plans:",
            "",
            f"File: {relative_path}",
            "Current Improvements:",
            "[Insert current ## Improvements content here]",
            "",
            "Please provide:",
            "1. More ambitious and innovative improvement ideas",
            "2. Roadmap-style organization",
            "3. Technical feasibility assessment",
            "4. Potential benefits and impact of each improvement",
            "```",
            "",
        ])

        if validation['issues']:
            lines.extend([
                "## Fix Proposals",
                "",
                "### To Fix This File:",
                "",
                "1. Add shebang at line 1: `#!/usr/bin/env python3`",
                "2. Add license header (lines 2-11)",
                "3. Add module docstring with required sections:",
                "   - Description",
                "   - Changelog",
                "   - Suggested Fixes",
                "   - Improvements",
                "4. Separate docstring from code with blank line and comment divider",
                "5. Ensure generated .md reports comply with markdown linting rules:",
                "   - **MD034**: Wrap bare URLs in links: `[URL](URL)`",
                "   - **MD047**: Add trailing newline at end of file",
                "   - **MD022**: Add blank lines around headings",
                "   - **MD038**: Remove spaces in code spans: `` `code` `` not `` ` code ` ``",
                "",
                "### Example Template:",
                "",
                "```python",
                "#!/usr/bin/env python3",
                "# Copyright (c) 2025 DebVisor contributors",
                '# Licensed under the Apache License, Version 2.0 (the "License");',
                "# you may not use this file except in compliance with the License.",
                "# You may obtain a copy of the License at",
                "#     [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)",
                "# Unless required by applicable law or agreed to in writing, software",
                '# distributed under the License is distributed on an "AS IS" BASIS,',
                "# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.",
                "# See the License for the specific language governing permissions and",
                "# limitations under the License.",
                "",
                '"""',
                "Brief description of module.",
                "",
                "## Description",
                "Longer description of what this module does.",
                "",
                "## Changelog",
                "- 1.0.0: Initial version",
                "",
                "## Suggested Fixes",
                "- None currently identified",
                "",
                "## Improvements",
                "- Future enhancements",
                '"""',
                "",
                "# =====================================================",
                "# Implementation",
                "# =====================================================",
                "",
                "# Your code here...",
                "```",
                "",
            ])

        lines.extend([
            "## Implementation Status",
            "Mark items as complete with ✅ emoji:",
            ""
        ])

        return "\n".join(lines)

    def run(self, output_dir: str = None):
        """Run planning agent on all code files."""
        code_files = self.find_code_files()
        print(f"[Planning] Found {len(code_files)} code files to analyze...")

        validated = 0
        with_issues = 0
        wrote_markdown = False

        for file_path in code_files:
            print(f"[Planning] Validating {file_path.relative_to(self.repo_root)}...")
            validation = self.validate_file_structure(file_path)

            if validation['status'] != 'valid':
                with_issues += 1
                plan_report = self.generate_plan_report(file_path, validation)
                plan_path = file_path.with_suffix(file_path.suffix + '.plan.md')
                plan_path.write_text(plan_report, encoding='utf-8')
                issues_count = len(validation['issues'])
                relative_path = plan_path.relative_to(self.repo_root)
                print(f"  -> {issues_count} issues found, wrote to {relative_path}")
                wrote_markdown = True
            else:
                validated += 1
                print("  -> Structure is valid")

        print("[Planning] Analysis complete!")
        print(f"[Planning] Summary: {validated} valid, {with_issues} with issues")

        if wrote_markdown:
            fixer_path = self.repo_root / 'fix_all_markdown.py'
            if fixer_path.exists():
                print("[Planning] Running fix_all_markdown.py to normalize reports...")
                try:
                    cmd = [sys.executable, str(fixer_path), "--quiet", "--max-line-length", "120"]
                    subprocess.run(cmd, check=False, cwd=self.repo_root)
                except Exception as exc:
                    print(f"[Planning] Skipped markdown fixer: {exc}")
            else:
                print("[Planning] fix_all_markdown.py not found; skipping markdown normalization")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Planning Agent: Validates code file structure')
    parser.add_argument('--agents-only', action='store_true',
                        help='Only process files in the scripts/ directory')
    args = parser.parse_args()

    agent = PlanningAgent(agents_only=args.agents_only)
    agent.run()
