#!/usr/bin/env python3
"""
Coding Expert Agent: Reads issue reports from .md files and proposes fixes.
Uses runSubagent to autonomously generate patch proposals.
"""

import re
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass
import argparse


@dataclass
class Issue:
    """Represents a single code issue."""
    line: int
    col: int
    tool: str
    code: str
    severity: str
    message: str
    implemented: bool = False


class CodingExpertAgent:
    """Proposes and implements fixes for code issues."""

    def __init__(self, repo_root: str = '.', agents_only: bool = False):
        self.repo_root = Path(repo_root)
        self.agents_only = agents_only

    def parse_issue_report(self, md_path: Path) -> Tuple[Path, List[Issue], str]:
        """Parse markdown issue report and extract issues."""
        content = md_path.read_text(encoding='utf-8', errors='replace')

        # Extract source file path from header
        header_match = re.search(r'^# Code Issues Report: (.+)$', content, re.MULTILINE)
        source_path = self.repo_root / (header_match.group(1) if header_match else 'unknown')

        issues = []
        # Parse table rows
        table_pattern = r'\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*`([^`]+)`\s*\|\s*(\w+)\s*\|\s*(.+?)\s*\|'

        for match in re.finditer(table_pattern, content):
            issue = Issue(
                line=int(match.group(1)),
                col=int(match.group(2)),
                tool=match.group(3),
                code=match.group(4),
                severity=match.group(5).lower(),
                message=match.group(6).replace('\\|', '|'),
                implemented='✅' in content and str(match.group(4)) in content
            )
            issues.append(issue)

        return source_path, issues, content

    def find_issue_reports(self) -> List[Path]:
        """Find all .md issue report files."""
        reports = []
        patterns = ['**/*.py.md', '**/*.sh.md', '**/*.js.md', '**/*.go.md', '**/*.html.md', '**/*.css.md']
        
        if self.agents_only:
            # Focus only on scripts/ directory for agent development/testing
            scripts_dir = self.repo_root / 'scripts'
            for pattern in patterns:
                reports.extend(scripts_dir.glob(pattern))
        else:
            for pattern in patterns:
                reports.extend(self.repo_root.glob(pattern))
        
        return sorted(reports)

    def get_source_context(self, source_path: Path, line: int, context_lines: int = 3) -> Tuple[int, str]:
        """Get source code context around the issue."""
        if not source_path.exists():
            return 0, ""

        try:
            lines = source_path.read_text(encoding='utf-8', errors='replace').splitlines()
            start = max(0, line - 1 - context_lines)
            end = min(len(lines), line + context_lines)

            context_lines_list = lines[start:end]
            return start + 1, "\n".join(context_lines_list)
        except Exception:
            return 0, ""

    def generate_fix_proposal(self, source_path: Path, issue: Issue) -> str:
        """Generate a fix proposal for an issue."""
        start_line, context = self.get_source_context(source_path, issue.line)

        proposal = f"""
### Issue at Line {issue.line}

**Tool:** {issue.tool} | **Code:** `{issue.code}` | **Severity:** {issue.severity.upper()}

**Message:** {issue.message}

**Context:**
```
{context}
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---
"""
        return proposal

    def generate_implementation_report(self, md_path: Path, source_path: Path, issues: List[Issue]) -> str:
        """Generate implementation report with fix proposals."""
        base_content = md_path.read_text(encoding='utf-8', errors='replace')

        report = base_content + "\n\n## Fix Proposals\n\n"

        unimplemented = [i for i in issues if not i.implemented]

        if not unimplemented:
            report += "✅ All issues have been implemented!\n"
            return report

        report += "**" + str(len(unimplemented)) + " issues to fix:**\n\n"

        for issue in unimplemented:
            proposal = self.generate_fix_proposal(source_path, issue)
            report += proposal

        report += """
## Implementation Progress

To mark an issue as fixed, add the issue code to the line below with a ✅ emoji:

**Fixed Issues:** (none yet)

---
*Updated: (auto-populated by coding expert)*
"""
        return report

    def mark_issue_implemented(self, md_path: Path, code: str):
        """Mark an issue as implemented in the report."""
        content = md_path.read_text(encoding='utf-8', errors='replace')

        # Add to Fixed Issues section
        if '**Fixed Issues:**' in content:
            content = content.replace(
                '**Fixed Issues:** (none yet)',
                '**Fixed Issues:** ✅ `' + code + '`'
            )
        else:
            content += '\n✅ **Fixed:** `' + code + '`\n'

        md_path.write_text(content, encoding='utf-8')

    def run(self):
        """Run coding expert agent."""
        reports = self.find_issue_reports()

        if not reports:
            print("[Coding Expert] No issue reports found.")
            return

        print("[Coding Expert] Found " + str(len(reports)) + " issue reports.")

        for report_path in reports:
            print("\n[Coding Expert] Processing " + str(report_path.relative_to(self.repo_root)) + "...")

            source_path, issues, original_content = self.parse_issue_report(report_path)

            if not source_path.exists():
                print("  -> Source file not found: " + str(source_path))
                continue

            unimplemented = [i for i in issues if not i.implemented]

            if not unimplemented:
                print("  -> All " + str(len(issues)) + " issues already implemented ✅")
                # Mark all issues as [Fixed] in the corresponding .plan.md file if it exists
                plan_md_path = source_path.with_suffix('.plan.md')
                if plan_md_path.exists():
                    try:
                        content = plan_md_path.read_text(encoding='utf-8', errors='replace')
                        # Mark issues as [Fixed] in the table rows
                        lines = content.split('\n')
                        updated_lines = []
                        for line in lines:
                            # Check if this is an issue table row (contains | type | line | message |)
                            if '|' in line and 'incorrect_header' in line or 'missing_section' in line:
                                # Add [Fixed] to the message part
                                parts = line.split('|')
                                if len(parts) >= 4:
                                    # The message is in the last part before the closing |
                                    message_part = parts[-2].strip()
                                    if not message_part.startswith('[Fixed]'):
                                        parts[-2] = f' [Fixed] {message_part}'
                                        line = '|'.join(parts)
                            updated_lines.append(line)

                        updated_content = '\n'.join(updated_lines)
                        plan_md_path.write_text(updated_content, encoding='utf-8')
                        print("  -> Marked all issues as [Fixed] in plan file: " +
                              str(plan_md_path.relative_to(self.repo_root)))
                    except Exception as e:
                        print(f"  -> Failed to update plan file: {e}")
                continue

            # Generate detailed proposal report
            proposal_report = self.generate_implementation_report(report_path, source_path, issues)
            report_path.write_text(proposal_report, encoding='utf-8')

            print("  -> Generated proposals for " + str(len(unimplemented)) + " issues")
            print("  -> Report updated: " + str(report_path.relative_to(self.repo_root)))

        print("\n[Coding Expert] Ready for implementation. Review proposals above.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Coding Expert Agent: Reads issue reports from .md files and proposes fixes.')
    parser.add_argument('--agents-only', action='store_true', help='Focus only on scripts/ directory for agent development/testing')
    args = parser.parse_args()
    
    agent = CodingExpertAgent(agents_only=args.agents_only)
    agent.run()
