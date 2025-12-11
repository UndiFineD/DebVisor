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

"""Audit GitHub Actions workflow files for pinned action versions and security issues."""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class ActionAuditor:
    """Audit GitHub Actions for version pinning and security best practices."""

    def __init__(self, workflows_dir: Path):
        self.workflows_dir = workflows_dir
        self.issues: List[Dict[str, str]] = []
        self.stats = {"total_actions": 0, "pinned": 0, "unpinned": 0, "deprecated": 0}

    def audit_all_workflows(self) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
        """Audit all workflow files in the directory."""
        workflow_files = list(self.workflows_dir.glob("*.yml")) + list(
            self.workflows_dir.glob("*.yaml")
        )

        for workflow_file in workflow_files:
            self._audit_workflow(workflow_file)

        return self.issues, self.stats

    def _audit_workflow(self, workflow_file: Path) -> None:
        """Audit a single workflow file."""
        try:
            with open(workflow_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Find all 'uses:' statements
            uses_pattern = r"uses:\s+([^\s@]+)(?:@([^\s]+))?"

            for match in re.finditer(uses_pattern, content, re.MULTILINE):
                action_name = match.group(1)
                version = match.group(2)

                self.stats["total_actions"] += 1

                # Skip local actions
                if action_name.startswith("./"):
                    continue

                # Check if version is pinned
                if not version:
                    self.stats["unpinned"] += 1
                    self.issues.append(
                        {
                            "file": workflow_file.name,
                            "action": action_name,
                            "severity": "HIGH",
                            "issue": "No version specified",
                            "recommendation": "Pin to specific version or commit SHA",
                        }
                    )
                elif version in ["main", "master", "develop"]:
                    self.stats["unpinned"] += 1
                    self.issues.append(
                        {
                            "file": workflow_file.name,
                            "action": action_name,
                            "version": version,
                            "severity": "MEDIUM",
                            "issue": f"Using mutable branch reference: {version}",
                            "recommendation": "Pin to commit SHA or semantic version tag",
                        }
                    )
                else:
                    self.stats["pinned"] += 1

                # Check for deprecated actions
                self._check_deprecated_action(workflow_file.name, action_name, version)

        except Exception as e:
            print(f"[warn] Error auditing {workflow_file.name}: {e}", file=sys.stderr)

    def _check_deprecated_action(
        self, filename: str, action: str, version: str
    ) -> None:
        """Check if action uses deprecated version."""
        deprecated_versions = {
            "actions/checkout": ["v1", "v2"],
            "actions/setup-python": ["v1", "v2", "v3"],
            "actions/setup-node": ["v1", "v2"],
            "actions/upload-artifact": ["v1", "v2"],
            "actions/download-artifact": ["v1", "v2"],
            "github/codeql-action/init": ["v1"],
            "github/codeql-action/analyze": ["v1"],
            "codecov/codecov-action": ["v1", "v2"],
        }

        if action in deprecated_versions:
            if version and any(
                version.startswith(v) for v in deprecated_versions[action]
            ):
                self.stats["deprecated"] += 1
                self.issues.append(
                    {
                        "file": filename,
                        "action": action,
                        "version": version,
                        "severity": "MEDIUM",
                        "issue": f"Deprecated version: {version}",
                        "recommendation": "Upgrade to latest version (v4+ recommended)",
                    }
                )

    def print_report(self) -> None:
        """Print audit report to console."""
        print("\n" + "=" * 80)
        print("GitHub Actions Security Audit Report")
        print("=" * 80 + "\n")

        print("[U+1F4CA] Statistics:")
        print(f"  Total actions found: {self.stats['total_actions']}")
        print(f"  ? Properly pinned: {self.stats['pinned']}")
        print(f"  [warn] Unpinned/mutable: {self.stats['unpinned']}")
        print(f"  [U+1F534] Deprecated versions: {self.stats['deprecated']}\n")

        if not self.issues:
            print("? No issues found! All actions are properly pinned.\n")
            return

        # Group issues by severity
        high = [i for i in self.issues if i["severity"] == "HIGH"]
        medium = [i for i in self.issues if i["severity"] == "MEDIUM"]

        if high:
            print(f"[U+1F534] HIGH Severity Issues ({len(high)}):")
            print("-" * 80)
            for issue in high:
                print(f"  File: {issue['file']}")
                print(f"  Action: {issue['action']}")
                print(f"  Issue: {issue['issue']}")
                print(f"  ? {issue['recommendation']}\n")

        if medium:
            print(f"[warn] MEDIUM Severity Issues ({len(medium)}):")
            print("-" * 80)
            for issue in medium:
                print(f"  File: {issue['file']}")
                print(f"  Action: {issue['action']}")
                if "version" in issue:
                    print(f"  Version: {issue['version']}")
                print(f"  Issue: {issue['issue']}")
                print(f"  ? {issue['recommendation']}\n")

        print("=" * 80)
        print(f"Total issues: {len(self.issues)}")
        print("=" * 80 + "\n")


def main() -> None:
    """Main entry point."""
    workflows_dir = Path(__file__).parent.parent / ".github" / "workflows"

    if not workflows_dir.exists():
        print(f"? Workflows directory not found: {workflows_dir}", file=sys.stderr)
        sys.exit(1)

    auditor = ActionAuditor(workflows_dir)
    issues, stats = auditor.audit_all_workflows()
    auditor.print_report()

    # Exit with error code if high-severity issues found
    high_severity_count = sum(1 for i in issues if i["severity"] == "HIGH")
    if high_severity_count > 0:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
