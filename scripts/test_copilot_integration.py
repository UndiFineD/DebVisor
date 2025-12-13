#!/usr/bin/env python3
"""
Test script for Copilot integration using GitHub Copilot CLI

This demonstrates how runSubagent works with GitHub Copilot.
"""

import subprocess
from coding_expert_agent import runSubagent as cea_runSubagent
from planning_agent import runSubagent as pa_runSubagent
from unified_workflow import runSubagent as uw_runSubagent


def test_copilot_integration():
    """Test the Copilot integration."""

    # Check if GitHub CLI is available
    try:
        subprocess.run(['gh', '--version'], capture_output=True, check=True)
        print("âœ… GitHub CLI found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("âŒ GitHub CLI not available.")
        print("To install GitHub CLI:")
        print("1. Visit: https://cli.github.com/")
        print("2. Download and install the appropriate version")
        print("3. Run: gh auth login")
        return

    # Check if copilot extension is installed
    try:
        result = subprocess.run(['gh', 'extension', 'list'], capture_output=True, text=True)
        if 'gh-copilot' not in result.stdout:
            print("âŒ GitHub Copilot extension not installed.")
            print("To install Copilot extension:")
            print("1. Run: gh extension install github/gh-copilot")
            print("2. Ensure you have a GitHub Copilot subscription")
            return
        print("âœ… GitHub Copilot extension found")
    except subprocess.CalledProcessError:
        print("âŒ Failed to check GitHub CLI extensions")
        return

    print("âœ… GitHub Copilot CLI setup complete, testing integration...")

    scripts = [
        ('coding_expert_agent', cea_runSubagent),
        ('planning_agent', pa_runSubagent),
        ('unified_workflow', uw_runSubagent)
    ]

    for name, func in scripts:
        try:
            # Test with a simple prompt
            prompt = "Hello! Can you help me with Python code review? Please respond with a brief greeting."
            response = func("Test greeting", prompt)

            print(f"âœ… {name}: Copilot integration successful!")
            print(f"   Response: {response[:200]}...")

        except Exception as e:
            print(f"âŒ {name}: Copilot integration failed: {e}")


if __name__ == "__main__":
    test_copilot_integration()

