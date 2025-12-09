import subprocess
import json
# import shutil
import re


def main() -> None:
    # Fetch alerts using gh cli
    jq_filter = (
        "map({number, rule: .rule.id, severity: .rule.severity, "
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
        return

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error fetching alerts:")
        print(result.stderr)
        return

    try:
        # Handle paginated output which might result in multiple JSON arrays separated by whitespace
        # We replace ']...[' with ',' to merge them into a single list.
        json_str = re.sub(r'\]\s*\[', ',', result.stdout)
        alerts = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return

    print(f"Found {len(alerts)} alerts.")

    with open("security-scan.md", "w", encoding="utf-8") as f:
        f.write("# Security Scan Report\n\n")
        f.write(f"**Total Alerts:** {len(alerts)}\n\n")
        f.write("Generated via GitHub CLI.\n\n")

        # Group by category
        security_alerts = [a for a in alerts if not (a['rule'].startswith('E') or a['rule'].startswith('W'))]
        style_alerts = [a for a in alerts if (a['rule'].startswith('E') or a['rule'].startswith('W'))]

        f.write("## Security Vulnerabilities (High Priority)\n\n")
        if security_alerts:
            f.write("| ID | Rule | Severity | File | Line | Message |\n")
            f.write("|----|------|----------|------|------|---------|\n")
            for a in security_alerts:
                severity = a.get('severity', 'warning')
                msg = a['message'].replace('|', '\\|').replace('\n', ' ')
                f.write(f"| {a['number']} | {a['rule']} | {severity} | `{a['file']}` | {a['line']} | {msg} |\n")
        else:
            f.write("*No security vulnerabilities found.*\n")

        f.write("\n## Code Quality & Style Issues\n\n")
        if style_alerts:
            f.write("| ID | Rule | File | Line | Message |\n")
            f.write("|----|------|------|------|---------|\n")
            for a in style_alerts:
                msg = a['message'].replace('|', '\\|').replace('\n', ' ')
                f.write(f"| {a['number']} | {a['rule']} | `{a['file']}` | {a['line']} | {msg} |\n")
        else:
            f.write("*No style issues found.*\n")

    print("Report generated: security-scan.md")


if __name__ == "__main__":
    main()
