#!/usr/bin/env python3
"""
Critic + Coding Expert Workflow Driver
1. Critic agent detects issues and writes .md reports
2. Coding expert agent reads reports and proposes fixes
3. Both agents are aware of markdown linting standards
"""

import sys
import subprocess
from pathlib import Path


MARKDOWN_LINTING_STANDARDS = """
## Markdown Linting Standards for Generated Reports

When generating .md report files, ensure compliance with these markdown rules:

**MD034: no-bare-urls**
- Issue: Bare URLs used in markdown
- Example of violation: `Visit http://example.com for details`
- Fix: Wrap in markdown link format: `Visit [http://example.com](http://example.com) for details`

**MD047: single-trailing-newline**
- Issue: File doesn't end with exactly one newline character
- Fix: Ensure all generated .md files end with a single newline (\\n)
- How: Use file I/O to append newline if not present

**MD022: blanks-around-headings**
- Issue: Headings not surrounded by blank lines
- Example of violation: Line before heading without blank line
- Fix: Add blank lines before and after each heading

**MD038: no-space-in-code**
- Issue: Spaces inside code span delimiters
- Example of violation: ` code ` (with spaces inside backticks)
- Fix: Remove spaces: `code` (no spaces)
"""


def run_agent(script_name: str, script_path: Path):
    """Run an agent script and report results."""
    print(f"\n{'='*70}")
    print(f"Running: {script_name}")
    print(f"{'='*70}\n")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent.parent,
            check=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return False


def main():
    """Run the full critic + expert workflow."""
    repo_root = Path(__file__).parent.parent

    print("=" * 70)
    print("CRITIC + CODING EXPERT WORKFLOW")
    print("=" * 70)
    print(MARKDOWN_LINTING_STANDARDS)
    print("=" * 70)

    # Step 1: Run Critic Agent
    critic_success = run_agent(
        "Critic Agent",
        repo_root / "scripts" / "critic_agent.py"
    )

    if not critic_success:
        print("[Workflow] Critic agent encountered errors (non-fatal).")

    # Step 2: Run Coding Expert Agent
    expert_success = run_agent(
        "Coding Expert Agent",
        repo_root / "scripts" / "coding_expert_agent.py"
    )

    if not expert_success:
        print("[Workflow] Coding Expert agent encountered errors (non-fatal).")

    print("\n" + "=" * 70)
    print("WORKFLOW COMPLETE")
    print("=" * 70)
    print("""
Next steps:
1. Review all .md files generated alongside code files
2. Ensure all generated .md files comply with markdown linting rules:
   - MD034: Wrap bare URLs in markdown links
   - MD047: Add trailing newline at end of file
   - MD022: Add blank lines around headings
   - MD038: Remove spaces in code spans
3. Implement the proposed fixes in the source files
4. Once fixed, mark issues as implemented by adding the code to the
   "Fixed Issues" section in the corresponding .md file
5. Re-run this workflow to detect any new issues

Note: Use Get-Content/Set-Content for proper line ending handling on Windows
""")


if __name__ == '__main__':
    main()
