#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
    parser = argparse.ArgumentParser(
        description="Audit GitHub Actions workflows for pinned versions and deprecated actions"
    )
    parser.add_argument(
        "--workflows",
        type=str,
        default=str(Path(__file__).parent.parent / ".github" / "workflows"),
        help="Path to workflows directory (defaults to repo .github/workflows)",
    )
    parser.add_argument(
        "--json",
        type=str,
        default=None,
        help="Optional path to write JSON report (deprecated; prefer --output)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to write report when using --format",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "sarif"],
        default=None,
        help="Output format when writing report",
    )
    parser.add_argument(
        "--fail-on-high",
        action="store_true",
        help="Return non-zero exit code when HIGH severity issues are found",
    )
    parser.add_argument(
        "--require-sha",
        action="store_true",
        help="Require actions to be pinned to commit SHA; non-SHA pins flagged as HIGH",
    )
    parser.add_argument(
        "--flag-wildcards",
        action="store_true",
        help="Flag wildcard path triggers as LOW severity recommendations",
    )
    parser.add_argument(
        "--flag-permissions",
        action="store_true",
        help="Flag broad or write permissions in workflow permissions blocks",
    )

    args = parser.parse_args(argv)

    workflows_dir = Path(args.workflows)
    if not workflows_dir.exists():
        print(f"❌ Workflows directory not found: {workflows_dir}", file=sys.stderr)
        sys.exit(1)

    auditor = ActionAuditor(
        workflows_dir,
        require_sha=args.require_sha,
        flag_wildcards=args.flag_wildcards,
        flag_permissions=args.flag_permissions,
    )
    issues, stats = auditor.audit_all_workflows()
    auditor.print_report()

    # Write output if requested
    output_path: Optional[str] = args.output or args.json
    if output_path and (args.format == "json" or args.json):
        payload = {"stats": stats, "issues": issues}
        try:
            Path(output_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(f"📝 JSON report written to: {output_path}")
        except Exception as e:
            print(f"⚠️ Failed to write JSON report: {e}", file=sys.stderr)
    elif output_path and args.format == "sarif":
        # Minimal SARIF v2.1.0 output
        level_map = {"HIGH": "error", "MEDIUM": "warning", "LOW": "note"}
        results = []
        for i in issues:
            results.append(
                {
                    "ruleId": "actions-audit",
                    "level": level_map.get(i.get("severity", "LOW"), "note"),
                    "message": {"text": f"{i.get('issue')} - {i.get('recommendation')}"},
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": f".github/workflows/{i.get('file')}"}
                            }
                        }
                    ],
                }
            )
        sarif = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "DebVisor Actions Auditor",
                            "informationUri": "https://github.com/UndiFineD/DebVisor",
                            "rules": [{"id": "actions-audit", "name": "GitHub Actions security audit"}],
                        }
                    },
                    "results": results,
                }
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(sarif, indent=2), encoding="utf-8")
            print(f"📝 SARIF report written to: {output_path}")
        except Exception as e:
            print(f"⚠️ Failed to write SARIF report: {e}", file=sys.stderr)

    # Exit with error code if requested and high-severity issues found
    if args.fail_on_high:
        high_severity_count = sum(1 for i in issues if i["severity"] == "HIGH")
        if high_severity_count > 0:
            sys.exit(1)

    sys.exit(0)
                    }
                )

            # Optional: flag wildcard paths that may trigger broadly
            if self.flag_wildcards:
                for m in re.finditer(r"paths:\s*(?:\n|\r\n)(?:\s*-\s*.+\*.+\n)+", content, re.IGNORECASE):
                    self.issues.append(
                        {
                            "file": workflow_file.name,
                            "action": "workflow",
                            "severity": "LOW",
                            "issue": "Workflow triggers include wildcard paths",
                            "recommendation": "Constrain paths to reduce unintended triggers",
                        }
                    )

            # Optional: flag broad or write permissions
            if self.flag_permissions:
                # Detect explicit write-all or dangerous writes
                perms_block = re.search(r"permissions:\s*(?:\n|\r\n)([\s\S]*?)(?:\n\S|$)", content, re.IGNORECASE)
                if perms_block:
                    block = perms_block.group(1)
                    if re.search(r"write-all", block, re.IGNORECASE):
                        self.issues.append(
                            {
                                "file": workflow_file.name,
                                "action": "workflow",
                                "severity": "MEDIUM",
                                "issue": "Workflow sets permissions: write-all",
                                "recommendation": "Minimize permissions; specify only required scopes",
                            }
                        )
                    if re.search(r"contents:\s*write", block, re.IGNORECASE):
                        self.issues.append(
                            {
                                "file": workflow_file.name,
                                "action": "workflow",
                                "severity": "MEDIUM",
                                "issue": "Workflow grants contents: write",
                                "recommendation": "Reduce to read or set at job level with least privilege",
                            }
                        )
                else:
                    # No explicit permissions block -> recommend defining minimal permissions
                    self.issues.append(
                        {
                            "file": workflow_file.name,
                            "action": "workflow",
                            "severity": "LOW",
                            "issue": "No explicit permissions block at workflow top-level",
                            "recommendation": "Define minimal top-level permissions to avoid defaults",
                        }
                    )

            # Additional checks for actions/checkout safeguards
            if re.search(r"uses:\s*actions/checkout@", content):
                # Detect persist-credentials: true
                if re.search(r"persist-credentials:\s*true", content, re.IGNORECASE):
                    self.issues.append(
                        {
                            "file": workflow_file.name,
                            "action": "actions/checkout",
                            "severity": "LOW",
                            "issue": "Checkout uses persist-credentials: true",
                            "recommendation": "Set persist-credentials: false for forks or PRs",
                        }
                    )
                # Recommend fetch-depth: 0 for full history when needed
                if not re.search(r"fetch-depth:\s*0", content, re.IGNORECASE):
                    self.issues.append(
                        {
                            "file": workflow_file.name,
                            "action": "actions/checkout",
                            "severity": "LOW",
                            "issue": "Checkout missing fetch-depth: 0",
                            "recommendation": "Add fetch-depth: 0 when full history is required",
                        }
                    )

            # Check actions/cache version pinning
            for m in re.finditer(r"uses:\s*actions/cache@([^\s]+)", content):
                cache_ver = m.group(1)
                is_sha = bool(re.fullmatch(r"[a-f0-9]{40}", cache_ver))
                if not is_sha:
                    self.issues.append(
                        {
                            "file": workflow_file.name,
                            "action": "actions/cache",
                            "version": cache_ver,
                            "severity": "MEDIUM",
                            "issue": "Cache action not pinned to commit SHA",
                            "recommendation": "Pin actions/cache to commit SHA to avoid mutable tags",
                        }
                    )

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

        print("📊 Statistics:")
        print(f"  Total actions found: {self.stats['total_actions']}")
        print(f"  ✅ Properly pinned: {self.stats['pinned']}")
        print(f"  ⚠️ Unpinned/mutable: {self.stats['unpinned']}")
        print(f"  ❗ Deprecated versions: {self.stats['deprecated']}\n")

        if not self.issues:
            print("✅ No issues found! All actions are properly pinned.\n")
            return

        # Group issues by severity
        high = [i for i in self.issues if i["severity"] == "HIGH"]
        medium = [i for i in self.issues if i["severity"] == "MEDIUM"]

        if high:
            print(f"❗ HIGH Severity Issues ({len(high)}):")
            print("-" * 80)
            for issue in high:
                print(f"  File: {issue['file']}")
                print(f"  Action: {issue['action']}")
                print(f"  Issue: {issue['issue']}")
                print(f"  💡 {issue['recommendation']}\n")

        if medium:
            print(f"⚠️ MEDIUM Severity Issues ({len(medium)}):")
            print("-" * 80)
            for issue in medium:
                print(f"  File: {issue['file']}")
                print(f"  Action: {issue['action']}")
                if "version" in issue:
                    print(f"  Version: {issue['version']}")
                print(f"  Issue: {issue['issue']}")
                print(f"  💡 {issue['recommendation']}\n")

        print("=" * 80)
        print(f"Total issues: {len(self.issues)}")
        print("=" * 80 + "\n")


def main(argv: Optional[List[str]] = None) -> None:
    """Main entry point with CLI options."""
    parser = argparse.ArgumentParser(
        description="Audit GitHub Actions workflows for pinned versions and deprecated actions"
    )
    parser.add_argument(
        "--workflows",
        type=str,
        default=str(Path(__file__).parent.parent / ".github" / "workflows"),
        help="Path to workflows directory (defaults to repo .github/workflows)",
    )
    parser.add_argument(
        "--json",
        type=str,
        default=None,
        help="Optional path to write JSON report (deprecated; prefer --output)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to write report when using --format",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "sarif"],
        default=None,
        help="Output format when writing report",
    )
    parser.add_argument(
        "--fail-on-high",
        action="store_true",
        help="Return non-zero exit code when HIGH severity issues are found",
    )
    parser.add_argument(
        "--require-sha",
        action="store_true",
        help="Require actions to be pinned to commit SHA; non-SHA pins flagged as HIGH",
    )
    parser.add_argument(
        "--flag-wildcards",
        action="store_true",
        help="Flag wildcard path triggers as LOW severity recommendations",
    )
    parser.add_argument(
        "--flag-permissions",
        action="store_true",
        help="Flag broad or write permissions in workflow permissions blocks",
    )

    args = parser.parse_args(argv)

    workflows_dir = Path(args.workflows)
    if not workflows_dir.exists():
        print(f"❌ Workflows directory not found: {workflows_dir}", file=sys.stderr)
        sys.exit(1)

    auditor = ActionAuditor(
        workflows_dir,
        require_sha=args.require_sha,
        flag_wildcards=args.flag_wildcards,
        flag_permissions=args.flag_permissions,
    )
    issues, stats = auditor.audit_all_workflows()
    auditor.print_report()

    # Write output if requested
    output_path: Optional[str] = args.output or args.json
    if output_path and (args.format == "json" or args.json):
        payload = {"stats": stats, "issues": issues}
        try:
            Path(output_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(f"📝 JSON report written to: {output_path}")
        except Exception as e:
            print(f"⚠️ Failed to write JSON report: {e}", file=sys.stderr)
    elif output_path and args.format == "sarif":
        # Minimal SARIF v2.1.0 output
        level_map = {"HIGH": "error", "MEDIUM": "warning", "LOW": "note"}
        results = []
        for i in issues:
            results.append(
                {
                    "ruleId": "actions-audit",
                    "level": level_map.get(i.get("severity", "LOW"), "note"),
                    "message": {"text": f"{i.get('issue')} - {i.get('recommendation')}"},
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": f".github/workflows/{i.get('file')}"}
                            }
                        }
                    ],
                }
            )
        sarif = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "DebVisor Actions Auditor",
                            "informationUri": "https://github.com/UndiFineD/DebVisor",
                            "rules": [{"id": "actions-audit", "name": "GitHub Actions security audit"}],
                        }
                    },
                    "results": results,
                }
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(sarif, indent=2), encoding="utf-8")
            print(f"📝 SARIF report written to: {output_path}")
        except Exception as e:
            print(f"⚠️ Failed to write SARIF report: {e}", file=sys.stderr)

    # Exit with error code if requested and high-severity issues found
    if args.fail_on_high:
        high_severity_count = sum(1 for i in issues if i["severity"] == "HIGH")
        if high_severity_count > 0:
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
