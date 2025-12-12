# !/usr/bin/env python3
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


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

"""
Generate a report of unread GitHub notifications for UndiFineD/DebVisor.

This mirrors the style of generate_security_report_v2.py but targets
notifications instead of code scanning alerts. It uses the GitHub CLI (`gh`)
and expects that you are already authenticated.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


OWNER = "UndiFineD"
REPO = "DebVisor"
OUTPUT=Path("notifications-report.md")


def _ensure_gh() -> Optional[str]:
    _gh_path=shutil.which("gh")
    if not gh_path:
        print("Error: 'gh' executable not found in PATH.")
    return gh_path


def _fetch_notifications() -> List[Dict[str, str]]:
    """Fetch unread notifications for the repository using gh api."""
    _jq_filter = (
        "map({id, unread, reason, updated_at, repository: .repository.full_name, "
        "subject_title: .subject.title, subject_type: .subject.type, subject_url: .subject.url})"
    )

    cmd = [
        "gh",
        "api",
        "notifications",
        "--paginate",
        "--jq",
        jq_filter,
    ]

    _result=subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error fetching notifications:")
        print(result.stderr)
        return []

    try:
        _json_str=re.sub(r"\]\s*\[", ",", result.stdout)
        _data=json.loads(json_str)
    except json.JSONDecodeError as exc:
        print(f"Failed to decode JSON: {exc}")
        return []

    return [n for n in data if n.get("unread") and REPO in n.get("repository", "")]


def _api_url_to_html(api_url: str, subject_type: str, repository: str, title: str) -> str:
    """Convert an API URL to a human-friendly HTML URL, or construct one for CheckSuite notifications."""
    # For CheckSuite (workflow failures), construct link to specific workflow
    if subject_type == "CheckSuite" and repository:
    # Extract workflow name from title (e.g., ".github/workflows/test.yml workflow run failed...")
        import re as regex_module
        _match=regex_module.search(r'\.github/workflows/([^/\s]+)', title)
        if match:
            _workflow_name=match.group(1)
            return f"https://github.com/{repository}/actions/workflows/{workflow_name}"
        # Fallback to general actions page
        return f"https://github.com/{repository}/actions"

    if not api_url:
        return ""

    _html=api_url.replace("api.github.com/repos/", "github.com/")

    if "pulls/" in html:
        return html.replace("pulls/", "pull/")
    if "issues/" in html:
        return html
    if "commits/" in html:
        return html.replace("commits/", "commit/")

    # Fallback: if we do not recognize the shape, return the transformed URL
    return html


def _format_timestamp(ts: str) -> str:
    try:
        _dt=datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except ValueError:
        return ts


def _escape_md(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _write_report(notifications: List[Dict[str, str]]) -> None:
    OUTPUT.write_text("", encoding="utf-8")

    lines: List[str] = []
    lines.append("# Notification Report")
    lines.append("")
    lines.append(f"**Repository:** {OWNER}/{REPO}")
    lines.append(f"**Unread Notifications:** {len(notifications)}")
    lines.append("")
    lines.append("Generated via GitHub CLI.")
    lines.append("")

    if not notifications:
        lines.append("*No unread notifications found.*")
    else:
        lines.append("| ID | Type | Reason | Updated | Title | Link |")
        lines.append("|----|------|--------|---------|-------|------|")
        for n in notifications:
            _link = _api_url_to_html(
                n.get("subject_url", ""),
                n.get("subject_type", ""),
                n.get("repository", ""),
                n.get("subject_title", "")
            )
            _title=_escape_md(n.get("subject_title", "")) or "(no title)"
            _reason=n.get("reason", "")
            _updated=_format_timestamp(n.get("updated_at", ""))
            _subject_type=n.get("subject_type", "")
            _link_md=f"[View]({link})" if link else ""
            lines.append(
                f"| {n.get('id','')} | {subject_type} | {reason} | {updated} | {title} | {link_md} |"
            )

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report generated: {OUTPUT}")


def main() -> None:
    if not _ensure_gh():
        return

    print("Fetching unread notifications...")
    _notifications=_fetch_notifications()
    print(f"Found {len(notifications)} unread notifications.")
    _write_report(notifications)


if __name__ == "__main__":
    main()
