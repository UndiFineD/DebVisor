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
Unified Workflow Driver.

Orchestrates all three quality agents in sequence:
1. Planning Agent: Validates file structure
2. Critic Agent: Detects code issues
3. Coding Expert Agent: Proposes fixes

Usage:
    python3 scripts/unified_workflow.py
"""

import subprocess
import sys
from pathlib import Path


def run_agent(agent_script: str, description: str, timeout_seconds: int) -> bool:
    """Run an agent script and return success status."""
    print(f"\n{'=' * 70}")
    print(f"[WORKFLOW] Starting: {description}")
    print(f"{'=' * 70}\n")

    try:
        result = subprocess.run(
            [sys.executable, agent_script],
            cwd=Path(__file__).parent.parent,
            timeout=timeout_seconds
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        minutes = max(1, int(round(timeout_seconds / 60)))
        print(f"[ERROR] {description} timed out after {minutes} minutes")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to run {description}: {str(e)}")
        return False


def main():
    """Execute the unified workflow."""
    print("\n" + "=" * 70)
    print("DEBVISOR UNIFIED QUALITY WORKFLOW")
    print("=" * 70)

    scripts_dir = Path(__file__).parent
    agents = [
        ("planning_agent.py", "Planning Agent (File Structure Validation)", 600),
        ("critic_agent.py", "Critic Agent (Code Quality Analysis)", 3600),
        ("coding_expert_agent.py", "Coding Expert Agent (Fix Proposals)", 1800),
    ]

    results = {}

    for agent_script, description, timeout_seconds in agents:
        agent_path = scripts_dir / agent_script
        if not agent_path.exists():
            print(f"\n[SKIP] {description} - script not found at {agent_path}")
            results[description] = False
            continue

        success = run_agent(str(agent_path), description, timeout_seconds)
        results[description] = success

    # Print final summary
    print("\n" + "=" * 70)
    print("WORKFLOW SUMMARY")
    print("=" * 70)

    for agent_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} {agent_name}")

    all_passed = all(results.values())

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL AGENTS COMPLETED SUCCESSFULLY")
        print("\nNext Steps:")
        print("1. Review generated .plan.md reports (file structure issues)")
        print("2. Review generated .md reports (code quality issues)")
        print("3. Review fix proposals and implementation status")
        print("4. Implement fixes in source files")
        print("5. Mark fixed issues with ✅ emoji in reports")
        print("6. Re-run this workflow to detect new issues")
    else:
        print("❌ SOME AGENTS FAILED")
        print("\nCheck error messages above and fix issues before re-running.")

    print("=" * 70 + "\n")

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
