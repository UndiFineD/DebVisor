"""GitHub Actions run & job inspection utility for DebVisor.

Usage examples (set GH_TOKEN first: a PAT with 'repo' + 'workflow' scopes):

  # List most recent 30 workflow runs (all states)
  python scripts/actions_inspector.py list-runs --limit 30

  # List only failed or cancelled runs
  python scripts/actions_inspector.py list-runs --limit 50 --only failed,cancelled

  # Show jobs for a specific run id
  python scripts/actions_inspector.py show-run 123456789

  # Emit a concise failure summary (exit non‑zero if failures found)
  python scripts/actions_inspector.py summarize-failures --limit 40

Environment:
  GH_TOKEN  Personal Access Token (preferred) OR GITHUB_TOKEN inside a workflow.

Outputs are plain text; redirect to files or pipe to tools as needed.
"""

from __future__ import annotations

import argparse
import os
import sys
import textwrap
from typing import Any, Dict, List, Optional
import requests

OWNER = "UndiFineD"
REPO = "DebVisor"
API_ROOT = f"https://api.github.com/repos/{OWNER}/{REPO}/actions"


def _token() -> str:
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        print("ERROR: GH_TOKEN or GITHUB_TOKEN not set", file=sys.stderr)
        sys.exit(2)
    return token


def _get(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {_token()}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "debvisor-actions-inspector"
    }
    r = requests.get(url, headers=headers, params=params, timeout=30)
    if r.status_code >= 300:
        print(f"HTTP {r.status_code} for {url}: {r.text}", file=sys.stderr)
        sys.exit(3)
    return r.json()


def list_runs(limit: int, only: List[str]) -> None:
    per_page = min(limit, 100)
    runs: List[Dict[str, Any]] = []
    page = 1
    while len(runs) < limit:
        data = _get(f"{API_ROOT}/runs", params={"per_page": per_page, "page": page})
        batch = data.get("workflow_runs", [])
        if not batch:
            break
        runs.extend(batch)
        page += 1
    runs = runs[:limit]
    if only:
        only_set = {o.strip().lower() for o in only}
        runs = [r for r in runs if (r.get("conclusion") or r.get("status")).lower() in only_set]
    print(f"Showing {len(runs)} runs (requested {limit})")
    for r in runs:
        rid = r.get("id")
        num = r.get("run_number")
        name = r.get("name")
        status = r.get("status")
        conclusion = r.get("conclusion") or "-"
        event = r.get("event")
        created = r.get("created_at")
        url = r.get("html_url")
        print(f"#{num} id={rid} {name} event={event} status={status} conclusion={conclusion} created={created}\n  {url}")


def show_run(run_id: int) -> None:
    jobs_data = _get(f"{API_ROOT}/runs/{run_id}/jobs")
    jobs = jobs_data.get("jobs", [])
    if not jobs:
        print(f"No jobs for run {run_id}")
        return
    print(f"Run {run_id} jobs ({len(jobs)}):")
    for j in jobs:
        jid = j.get("id")
        name = j.get("name")
        status = j.get("status")
        conclusion = j.get("conclusion")
        started = j.get("started_at")
        completed = j.get("completed_at")
        html_url = j.get("html_url")
        print(f"- {name} id={jid} status={status} conclusion={conclusion} started={started} completed={completed}\n  {html_url}")
        # Steps summary (only failed or timed out ones for brevity)
        for s in j.get("steps", []):
            sc = s.get("conclusion")
            if sc and sc not in ("success", "skipped"):
                print(f"    * Step '{s.get('name')}' conclusion={sc}")


def summarize_failures(limit: int) -> None:
    per_page = min(limit, 100)
    data = _get(f"{API_ROOT}/runs", params={"per_page": per_page})
    runs = data.get("workflow_runs", [])[:limit]
    failed: List[Dict[str, Any]] = [
        r for r in runs if (r.get("conclusion") or "").lower() in {"failure", "cancelled", "timed_out"}
    ]
    if not failed:
        print("No failed/cancelled/timed_out runs in recent set.")
        return
    print(f"Found {len(failed)} problematic runs (out of {len(runs)} scanned):")
    for r in failed:
        print(f"- #{r.get('run_number')} {r.get('name')} conclusion={r.get('conclusion')} url={r.get('html_url')}")
    # Optional deeper look at first failure
    first = failed[0]
    print("\nDetail of first failed run steps:")
    jobs_data = _get(f"{API_ROOT}/runs/{first['id']}/jobs")
    for j in jobs_data.get("jobs", []):
        if j.get("conclusion") != "success":
            print(f" Job: {j.get('name')} conclusion={j.get('conclusion')} url={j.get('html_url')}")
            for s in j.get("steps", []):
                sc = s.get("conclusion")
                if sc and sc != "success":
                    print(f"    - Step: {s.get('name')} status={s.get('status')} conclusion={sc}")
    # Exit non-zero for pipeline use
    sys.exit(1)


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="actions_inspector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """Inspect GitHub Actions runs & jobs for this repository.
            Commands:
              list-runs            List workflow runs
              show-run <id>        Show jobs & failed steps for run id
              summarize-failures   Summarize and exit non-zero on failures
            """
        ),
    )
    sub = p.add_subparsers(dest="command", required=True)

    pr = sub.add_parser("list-runs")
    pr.add_argument("--limit", type=int, default=30, help="Max runs to list (<=300)")
    pr.add_argument("--only", type=str, default="", help="Comma list of conclusions to include (e.g. failed,cancelled)")

    sr = sub.add_parser("show-run")
    sr.add_argument("run_id", type=int, help="Run ID to inspect")

    sf = sub.add_parser("summarize-failures")
    sf.add_argument("--limit", type=int, default=50, help="Max runs to scan")

    return p.parse_args(argv)


def main(argv: List[str]) -> None:
    args = parse_args(argv)
    if args.command == "list-runs":
        only_list = [o for o in args.only.split(",") if o.strip()] if args.only else []
        list_runs(min(args.limit, 300), only_list)
    elif args.command == "show-run":
        show_run(args.run_id)
    elif args.command == "summarize-failures":
        summarize_failures(args.limit)
    else:
        print("Unknown command", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
