#!/usr/bin/env python3
"""
Critic + Coding Expert Workflow Driver
1. Critic agent detects issues and writes .md reports
2. Coding expert agent reads reports and proposes fixes
"""

import sys
import subprocess
from pathlib import Path


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
2. Implement the proposed fixes in the source files
3. Once fixed, mark issues as implemented by adding the code to the
   "Fixed Issues" section in the corresponding .md file
4. Re-run this workflow to detect any new issues
""")


if __name__ == '__main__':
    main()
