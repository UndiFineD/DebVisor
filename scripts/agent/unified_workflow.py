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
    python3 scripts/unified_workflow.py [--agents-only]
"""

import subprocess
import sys
from pathlib import Path
import argparse


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


def run_git_command(command: list, description: str) -> bool:
    """Run a git command and return success status."""
    try:
        result = subprocess.run(
            command,
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"[GIT] ✅ {description}")
            return True
        else:
            print(f"[GIT] ❌ {description} failed: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[GIT] ❌ {description} timed out")
        return False
    except Exception as e:
        print(f"[GIT] ❌ {description} error: {str(e)}")
        return False


def run_git_workflow():
    """Execute git add, commit, and push workflow."""
    print(f"\n{'=' * 70}")
    print("[GIT] Starting automated git workflow")
    print(f"{'=' * 70}\n")

    # Check if there are any changes to commit
    try:
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        if not status_result.stdout.strip():
            print("[GIT] No changes to commit")
            return True
    except Exception as e:
        print(f"[GIT] Could not check git status: {str(e)}")
        return False

    # Git add all changes
    if not run_git_command(["git", "add", "-A"], "Staged all changes"):
        return False

    # Git commit with automated message
    commit_message = "Automated code quality workflow updates"
    if not run_git_command(["git", "commit", "-m", commit_message], f"Committed changes: '{commit_message}'"):
        return False

    # Git push
    if not run_git_command(["git", "push"], "Pushed changes to remote"):
        return False

    print("[GIT] ✅ Git workflow completed successfully")
    return True


def run_agent(agent_script: str, description: str, timeout_seconds: int, extra_args: list = None) -> bool:
    """Run an agent script and return success status."""
    print(f"\n{'=' * 70}")
    print(f"[WORKFLOW] Starting: {description}")
    print(f"{'=' * 70}\n")

    cmd = [sys.executable, agent_script]
    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(
            cmd,
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
    parser = argparse.ArgumentParser(description='DebVisor Unified Quality Workflow')
    parser.add_argument('--agents-only', action='store_true',
                        help='Only process files in the scripts/ directory (agents focus on themselves)')
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("DEBVISOR UNIFIED QUALITY WORKFLOW")
    if args.agents_only:
        print("MODE: AGENTS-ONLY (processing scripts/ directory only)")
    print("=" * 70)

    scripts_dir = Path(__file__).parent
    agents = [
        ("planning_agent.py", "Planning Agent (File Structure Validation)", 600),
        ("critic_agent.py", "Critic Agent (Code Quality Analysis)", 3600),
        ("coding_expert_agent.py", "Coding Expert Agent (Fix Proposals)", 1800),
    ]

    # Prepare extra arguments for agents
    extra_args = []
    if args.agents_only:
        extra_args = ["--agents-only"]

    results = {}

    for agent_script, description, timeout_seconds in agents:
        agent_path = scripts_dir / agent_script
        if not agent_path.exists():
            print(f"\n[SKIP] {description} - script not found at {agent_path}")
            results[description] = False
            continue

        success = run_agent(str(agent_path), description, timeout_seconds, extra_args)
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

    # Run automated git workflow regardless of agent success/failure
    print(f"\n{'=' * 70}")
    print("[GIT] Running automated git workflow (regardless of agent status)")
    print(f"{'=' * 70}\n")

    git_success = run_git_workflow()

    if git_success:
        print("✅ Changes have been automatically committed and pushed")
    else:
        print("⚠️  Git operations completed with issues - check above for details")

    print("=" * 70 + "\n")

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
