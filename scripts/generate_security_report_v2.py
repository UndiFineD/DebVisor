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

import subprocess
import json
import shutil
import re
import sys


def main() -> int:
    # Fetch alerts using gh cli
    jq_filter = (
        "map({number, rule: .rule.id, severity: .rule.severity, "
        "state: .state, tool: .tool.name, "
        "message: .most_recent_instance.message.text, "
        "file: .most_recent_instance.location.path, "
        "line: .most_recent_instance.location.start_line})"
    )

    cmd = [
        "gh", "api", "repos/UndiFineD/DebVisor/code-scanning/alerts",
        "--paginate",
        "--jq", jq_filter
    ]

    print("Fetching alerts...")

    gh_path = shutil.which("gh")
    if not gh_path:
        print("Error: 'gh' executable not found in PATH.")
        return 1

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error fetching alerts:")
        print(result.stderr)
        return 1

    try:
        # Handle paginated output which might result in multiple JSON arrays separated by whitespace
        # We replace ']...[' with ',' to merge them into a single list.
        json_str = re.sub(r'\]\s*\[', ', ', result.stdout)
        alerts = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return 1

    print(f"Found {len(alerts)} alerts.")

    # Filter by state
    open_alerts = [a for a in alerts if a.get('state') == 'open']
    dismissed_alerts = [a for a in alerts if a.get('state') in ('dismissed', 'fixed')]

    with open("security-scan.md", "w", encoding="utf-8") as f:
        f.write("# Security Scan Report\n\n")
        f.write(f"**Total Alerts:** {len(alerts)}\n")
        f.write(f"**Open:** {len(open_alerts)} | **Dismissed/Fixed:** {len(dismissed_alerts)}\n\n")
        f.write("Generated via GitHub CLI.\n\n")

        # Group open alerts by severity
        critical = [a for a in open_alerts if a.get('severity') == 'critical']
        high = [a for a in open_alerts if a.get('severity') == 'high']
        medium = [a for a in open_alerts if a.get('severity') == 'medium']
        low = [a for a in open_alerts if a.get('severity') == 'low']
        other = [a for a in open_alerts if a.get('severity') not in ('critical', 'high', 'medium', 'low')]

        def write_severity_section(title: str, items: list, emoji: str = "") -> None:
            """Write a section for a specific severity level."""
            f.write(f"## {emoji} {title} ({len(items)})\n\n")
            if items:
                f.write("| ID | Rule | Tool | File | Line | Message |\n")
                f.write("|----|------|------|------|------|---------|\n")
                for a in items:
                    tool = a.get('tool', 'Unknown')
                    msg = a['message'].replace('|', '\\|').replace('\n', ' ')
                    f.write(f"| {a['number']} | {a['rule']} | {tool} | `{a['file']}` | {a['line']} | {msg} |\n")
            else:
                f.write("*No alerts found.*\n")
            f.write("\n")

        write_severity_section("Critical Severity", critical, "🔴")
        write_severity_section("High Severity", high, "🟠")
        write_severity_section("Medium Severity", medium, "🟡")
        write_severity_section("Low Severity", low, "🟢")
        if other:
            write_severity_section("Other", other, "⚪")

    print("Report generated: security-scan.md")
    # Also emit a JSON summary for CI comment composition
    severity_buckets = {
        "critical": len(critical),
        "high": len(high),
        "medium": len(medium),
        "low": len(low),
        "other": len(other),
    }
    summary = {
        "total_alerts": len(alerts),
        "open_alerts": len(open_alerts),
        "dismissed_or_fixed": len(dismissed_alerts),
        "by_severity": severity_buckets,
    }
    try:
        with open("security-scan-summary.json", "w", encoding="utf-8") as jf:
            json.dump(summary, jf, indent=2)
        print("Summary generated: security-scan-summary.json")
    except Exception as e:
        print(f"Warning: failed to write summary JSON: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
