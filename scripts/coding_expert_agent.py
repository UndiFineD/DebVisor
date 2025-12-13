#!/usr/bin/env python3
"""
Coding Expert Agent: Reads issue reports from .md files and proposes fixes.
Uses GitHub Copilot CLI to autonomously generate patch proposals via GitHub Copilot.

Copilot Integration Setup:
1. Install GitHub CLI: https://cli.github.com/
2. Authenticate with GitHub: gh auth login
3. Install Copilot extension: gh extension install github/gh-copilot
4. Run the agent: python scripts/coding_expert_agent.py --agents-only

Note: Requires GitHub Copilot subscription.
"""

import re
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass
import argparse
import os
import subprocess

def runSubagent(description: str, prompt: str) -> str:
    """
    Run a subagent using GitHub Copilot CLI to interact with GitHub Copilot.

    Args:
        description: Description of the task
        prompt: The prompt to send to Copilot

    Returns:
        Copilot's response as a string

    Raises:
        Exception: If GitHub CLI is not available or Copilot integration fails
    """
    try:
        # Check if gh command is available
        subprocess.run(['gh', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise Exception("GitHub CLI not available. Install from: https://cli.github.com/")

    try:
        # Check if copilot extension is installed
        result = subprocess.run(['gh', 'extension', 'list'], capture_output=True, text=True)
        if 'gh-copilot' not in result.stdout:
            raise Exception("GitHub Copilot extension not installed. Run: gh extension install github/gh-copilot")
    except subprocess.CalledProcessError:
        raise Exception("Failed to check GitHub CLI extensions. Ensure gh is properly installed.")

    try:
        # Run gh copilot suggest with the prompt
        result = subprocess.run(
            ['gh', 'copilot', 'suggest', prompt],
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )

        if result.returncode != 0:
            raise Exception(f"GitHub Copilot CLI failed: {result.stderr}")

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        raise Exception("GitHub Copilot request timed out")
    except Exception as e:
        raise Exception(f"Failed to run Copilot subagent: {str(e)}")


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

    def __init__(self, repo_root: str = '.', agents_only: bool = False, auto_apply: bool = False):
        self.repo_root = Path(repo_root)
        self.agents_only = agents_only
        self.auto_apply = auto_apply

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
                implemented=False  # Will be determined below
            )

            # Check if this specific issue is marked as implemented
            # Look for checkmark near the issue code in the content
            issue_code = match.group(4)
            # Check if there's a checkmark within a few lines of this issue's table row
            start_pos = match.start()
            end_pos = match.end()
            context_start = max(0, start_pos - 200)  # Look 200 chars before
            context_end = min(len(content), end_pos + 200)  # Look 200 chars after
            context = content[context_start:context_end]
            issue.implemented = f'✅ {issue_code}' in context or f'✅ `{issue_code}`' in context

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
        """Generate a fix proposal for an issue using Copilot."""
        start_line, context = self.get_source_context(source_path, issue.line)

        # Create detailed prompt for Copilot
        copilot_prompt = f"""
You are an expert software engineer. Analyze this code issue and provide a specific, actionable fix.

**Issue Details:**
- File: {source_path.name}
- Line: {issue.line}
- Tool: {issue.tool}
- Code: {issue.code}
- Severity: {issue.severity.upper()}
- Message: {issue.message}

**Code Context (around line {issue.line}):**
```
{context}
```

**Task:**
1. Analyze the issue and understand what needs to be fixed
2. Provide the specific code change needed
3. Explain why this fix is correct
4. Ensure the fix follows Python best practices and coding standards

**Response Format:**
- **Root Cause:** Brief explanation of why this issue occurred
- **Fix:** The exact code change needed (show before/after if helpful)
- **Explanation:** Why this fix resolves the issue
- **Verification:** How to verify the fix works

Be specific and provide actionable code changes.
"""

        try:
            # Use runSubagent to get Copilot's analysis and fix suggestions
            copilot_response = runSubagent(
                description="Code fix analysis",
                prompt=copilot_prompt
            )

            # If auto-apply is enabled, try to apply the fix
            applied = False
            if self.auto_apply:
                applied = self.apply_fix(source_path, issue, copilot_response)
                if applied:
                    print(f"  -> Auto-applied fix for {issue.code}")

            proposal = f"""
### Issue at Line {issue.line}

**Tool:** {issue.tool} | **Code:** `{issue.code}` | **Severity:** {issue.severity.upper()}

**Message:** {issue.message}

**Code Context:**
```
{context}
```

**Copilot Analysis & Fix Proposal:**

{copilot_response}

{'**✅ AUTO-APPLIED**' if applied else '**⚠️ MANUAL REVIEW NEEDED**'}

---
*Generated by GitHub Copilot via runSubagent*
"""
        except Exception as e:
            # Fallback to generic proposal if Copilot fails
            proposal = f"""
### Issue at Line {issue.line}

**Tool:** {issue.tool} | **Code:** `{issue.code}` | **Severity:** {issue.severity.upper()}

**Message:** {issue.message}

**Context:**
```
{context}
```

**Proposal:** (Copilot unavailable - {str(e)})
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---
"""

        return proposal

    def apply_fix(self, source_path: Path, issue: Issue, copilot_response: str) -> bool:
        """Apply a fix suggested by Copilot to the source file."""
        try:
            # Parse the Copilot response to extract code changes
            # Look for code blocks in the response
            import re

            # Find code blocks (```language or ```)
            code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', copilot_response, re.DOTALL)

            if not code_blocks:
                print(f"  -> No code blocks found in Copilot response for {issue.code}")
                return False

            # For now, we'll just log the suggested fix
            # In a full implementation, you would parse the before/after code and apply it
            print(f"  -> Copilot suggested fix for {issue.code}:")
            for i, block in enumerate(code_blocks[:2]):  # Show first 2 code blocks
                print(f"    Code block {i+1}:")
                for line in block.split('\n')[:5]:  # Show first 5 lines
                    print(f"      {line}")
                if len(block.split('\n')) > 5:
                    print("      ...")

            # TODO: Implement automatic application of fixes
            # This would require parsing the before/after code and applying patches

            return False  # For now, don't apply automatically

        except Exception as e:
            print(f"  -> Failed to apply fix for {issue.code}: {e}")
            return False

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

            # Always update the plan.md file to mark fixed issues
            plan_md_path = source_path.with_suffix('.plan.md')
            if plan_md_path.exists():
                try:
                    content = plan_md_path.read_text(encoding='utf-8', errors='replace')
                    # Mark implemented issues as [Fixed] in the table rows
                    lines = content.split('\n')
                    updated_lines = []
                    for line in lines:
                        # Check if this is an issue table row (contains | and looks like a data row)
                        if '|' in line and line.count('|') >= 5 and not line.startswith('| ---'):
                            parts = line.split('|')
                            if len(parts) >= 6:
                                # Extract the issue code from the 4th column (Code column)
                                code_part = parts[3].strip()
                                if code_part.startswith('`') and code_part.endswith('`'):
                                    issue_code = code_part[1:-1]  # Remove backticks
                                    # Check if this issue is implemented
                                    if any(issue.code == issue_code and issue.implemented for issue in issues):
                                        # Add [Fixed] to the message part (last column before closing |)
                                        message_part = parts[-2].strip()
                                        if not message_part.startswith('[Fixed]'):
                                            parts[-2] = f' [Fixed] {message_part}'
                                            line = '|'.join(parts)
                        updated_lines.append(line)

                    updated_content = '\n'.join(updated_lines)
                    plan_md_path.write_text(updated_content, encoding='utf-8')
                    print("  -> Updated plan file with fixed issue markers: " +
                          str(plan_md_path.relative_to(self.repo_root)))
                except Exception as e:
                    print(f"  -> Failed to update plan file: {e}")

            if not unimplemented:
                print("  -> All " + str(len(issues)) + " issues already implemented ✅")
                continue

            # Generate detailed proposal report
            proposal_report = self.generate_implementation_report(report_path, source_path, issues)
            report_path.write_text(proposal_report, encoding='utf-8')

            print("  -> Generated proposals for " + str(len(unimplemented)) + " issues")
            print("  -> Report updated: " + str(report_path.relative_to(self.repo_root)))

        print("\n[Coding Expert] Ready for implementation. Review proposals above.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Coding Expert Agent: Reads issue reports from .md files and proposes fixes using Copilot.'
    )
    parser.add_argument(
        '--agents-only', action='store_true',
        help='Focus only on scripts/ directory for agent development/testing'
    )
    parser.add_argument(
        '--auto-apply', action='store_true',
        help='Automatically apply fixes suggested by Copilot (experimental)'
    )
    args = parser.parse_args()

    agent = CodingExpertAgent(agents_only=args.agents_only, auto_apply=args.auto_apply)
    agent.run()
