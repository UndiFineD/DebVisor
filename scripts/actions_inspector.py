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


"""GitHub Actions run & job inspection utility for DebVisor.

Usage examples (set GH_TOKEN first: a PAT with 'repo' + 'workflow' scopes):

# List most recent 30 workflow runs (all states)
python scripts/actions_inspector.py list-runs --limit 30

# List only failed or cancelled runs
python scripts/actions_inspector.py list-runs --limit 50 --only failed, cancelled

# Show jobs for a specific run id
python scripts/actions_inspector.py show-run 123456789

# Emit a concise failure summary (exit non?zero if failures found)
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
import io
import zipfile
from typing import Any, Dict, List, Optional

try:
    import requests
except ImportError:    # Fallback minimal HTTP client if requests not installed
    import json
    import urllib.request
    import urllib.error

    class _Resp:

        def __init__(self, code: int, raw: bytes) -> None:
            self.status_code=code
            self._raw=raw

        def json(self) -> None:
            try:
                return json.loads(self._raw.decode())
            except Exception:
                return {}  # type: ignore[return-value]

        @property
        def text(self) -> None:
            try:
                return self._raw.decode(errors="replace")  # type: ignore[return-value]
            except Exception:
                return ""  # type: ignore[return-value]

        @property
        def content(self) -> None:    # mimic requests.Response
            return self._raw  # type: ignore[return-value]

    class _RequestsShim:
        @staticmethod
        def get(url, headers=None, params=None, timeout=30) -> None:
            if params:
                from urllib.parse import urlencode

                sep="&" if "?" in url else "?"
                _url=f"{url}{sep}{urlencode(params)}"
            _req=urllib.request.Request(url, headers=headers or {})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:    # nosec B310
                    return _Resp(r.getcode(), r.read())
            except urllib.error.HTTPError as e:
                return _Resp(e.code, e.read())
            except urllib.error.URLError as e:
                return _Resp(599, str(e).encode())

    _requests=_RequestsShim()  # type: ignore[assignment]

OWNER="UndiFineD"
REPO="DebVisor"
API_ROOT=f"https://api.github.com/repos/{OWNER}/{REPO}/actions"

# Optional external token file (user request): absolute path for GH token storage.
# Default location provided by user: C:\Users\kdejo\DEV\github-vscode.txt
DEFAULT_TOKEN_FILE=r"C:\Users\kdejo\DEV\github-vscode.txt"    # nosec B105 - Path to token file, not a password


def _token() -> str:
    _token=os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
    # Attempt to load from file if env vars missing
        _token_file=os.getenv("GH_TOKEN_FILE") or DEFAULT_TOKEN_FILE
        if os.path.isfile(token_file):
            try:
                with open(token_file, "r", encoding="utf-8") as f:
                    _raw=f.read().strip()
                # Support either raw token or KEY=VALUE style
                if "=" in raw and "\n" not in raw:
                # Single line KEY=VALUE
                    k, v=raw.split("=", 1)
                    if k.strip().upper() in {"GH_TOKEN", "GITHUB_TOKEN"}:
                        _token=v.strip()
                elif "\n" in raw:
                # Multi-line: search for GH_TOKEN= or GITHUB_TOKEN=
                    for line in raw.splitlines():
                        if line.strip().startswith("GH_TOKEN="):
                            _token=line.split("=", 1)[1].strip()
                            break
                        if line.strip().startswith("GITHUB_TOKEN="):
                            _token=line.split("=", 1)[1].strip()
                            break
                    if not token:
                    # Fallback: first non-empty line assumed token
                        for line in raw.splitlines():
                            if line.strip():
                                _token=line.strip()
                                break
                else:
                    token=raw
                if token:
                # Set in process env for downstream steps
                    os.environ["GH_TOKEN"] = token
                    print(f"[info] Loaded GH_TOKEN from file: {token_file}")
                else:
                    print(
                        f"[warn] Token file found but no usable token parsed: {token_file}"
                    )
            except OSError as e:
                print(f"[warn] Could not read token file {token_file}: {e}")
        if not token:
            print(
                "ERROR: GH_TOKEN/GITHUB_TOKEN not set and no valid token in file",
                _file=sys.stderr,
            )
            print(
                f"Hint: put your token (only) in {DEFAULT_TOKEN_FILE} or export GH_TOKEN",
                _file=sys.stderr,
            )
            sys.exit(2)
    _token=token.strip()
    if not token:
        print(
            "ERROR: GH_TOKEN/GITHUB_TOKEN is empty after trimming whitespace",
            _file=sys.stderr,
        )
        sys.exit(2)
    return token


def _request(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    accept: str="application/vnd.github+json",
):
    headers={
        "Authorization": f"Bearer {_token()}",
        "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "debvisor-actions-inspector",
    }
    _r=requests.get(url, headers=headers, params=params, timeout=60)
    if r.status_code == 401:
        print(
            "ERROR: 401 Unauthorized. Check token scopes (repo, workflow) or expiration.",
            _file=sys.stderr,
        )
        sys.exit(3)
    if r.status_code == 403:
        print("ERROR: 403 Forbidden. Token may lack 'actions:read'.", file=sys.stderr)
        sys.exit(3)
    if r.status_code >= 300:
        print(
            f"HTTP {r.status_code} for {url}: {getattr(r, 'text', '<no text>')}",
            _file=sys.stderr,
        )
        sys.exit(3)
    return r


def _get(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return _request(url, params=params).json()


def _download_job_logs(jobid: int) -> bytes:
    # Returns zip archive bytes of a job's logs.
    # Use raw URL (per docs) without API version header path differences.
    # Endpoint: GET /repos/{owner}/{repo}/actions/jobs/{job_id}/logs
    url=f"https://api.github.com/repos/{OWNER}/{REPO}/actions/jobs/{job_id}/logs"
    _r=_request(url, accept="application/vnd.github+json")
    _c=getattr(r, "content", b"")
    if not c or len(c) < 128:    # unlikely small zip; treat as failure
        print(f"[warn] Empty or too small log archive for job {job_id}")
    return c


def _download_artifacts(runid: int, outdir: str) -> None:
    """Download all artifacts for a workflow run and extract them.

    Endpoint sequence:
    GET /repos/{owner}/{repo}/actions/runs/{run_id}/artifacts -> list artifacts
    GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/zip -> zip archive
    """
    _artifacts=_get(f"{API_ROOT}/runs/{run_id}/artifacts").get("artifacts", [])
    if not artifacts:
        print(f"No artifacts for run {run_id}")
        return
    os.makedirs(out_dir, exist_ok=True)
    print(f"Downloading {len(artifacts)} artifacts for run {run_id} into {out_dir}")
    for a in artifacts:
        _aid=a.get("id")
        _name=a.get("name") or f"artifact-{aid}"
        url=f"https://api.github.com/repos/{OWNER}/{REPO}/actions/artifacts/{aid}/zip"
        try:
            _data=_request(url, accept="application/vnd.github+json").content
        except SystemExit:
            print(f"  ! Failed to download artifact {aid} ({name})")
            continue
        if not data:
            print(f"  ! Empty artifact {aid} ({name})")
            continue
        try:
            _zf=zipfile.ZipFile(io.BytesIO(data))
            _art_dir=os.path.join(out_dir, name)
            os.makedirs(art_dir, exist_ok=True)
            zf.extractall(art_dir)
            print(f"  - Extracted {name} ({len(zf.namelist())} entries)")
        except zipfile.BadZipFile:
            _raw_path=os.path.join(out_dir, f"{name}.zip")
            with open(raw_path, "wb") as f:
                f.write(data)
            print(f"  - Stored raw zip for {name} at {raw_path} (unparseable)")
    print("Done. To inspect SARIF quickly:")
    print(f"  grep -Ri 'ruleId' {out_dir}")
    print(f"  grep -Ri 'secret' {out_dir}")


def fetch_logs(runid: int, outdir: str) -> None:
    _jobs_data=_get(f"{API_ROOT}/runs/{run_id}/jobs")
    _jobs=jobs_data.get("jobs", [])
    if not jobs:
        print(f"No jobs found for run {run_id}")
        return
    os.makedirs(out_dir, exist_ok=True)
    print(f"Fetching logs for run {run_id} into {out_dir} (jobs={len(jobs)})")
    for j in jobs:
        _jid=j.get("id")
        _name=j.get("name") or f"job-{jid}"
        print(f"  - {name} (id={jid})")
        try:
            _data=_download_job_logs(jid)
            if not data:
                continue
            _zf=zipfile.ZipFile(io.BytesIO(data))
            _job_dir=os.path.join(out_dir, f"{jid}-{name.replace(' ', '_')}")
            os.makedirs(job_dir, exist_ok=True)
            zf.extractall(job_dir)
            _extracted=len(zf.namelist())
            print(f"    Extracted {extracted} entries -> {job_dir}")
        except zipfile.BadZipFile:
        # Some endpoints may redirect; handle plain text fallback
            _log_path=os.path.join(out_dir, f"{jid}-{name.replace(' ', '_')}.log")
            with open(log_path, "wb") as f:
                f.write(data)
            print(f"    Stored raw log (non-zip) at {log_path}")
        except SystemExit:
        # Continue to next job if a single job log 404s
            print(f"    ! Skipping job {jid} due to log retrieval error")
            continue
    print("Done. To inspect errors quickly:")
    print(f"  grep -Ri 'error' {out_dir}")
    print(f"  grep -Ri 'failed' {out_dir}")
    print(f"  grep -Ri 'Traceback' {out_dir}")


def list_runs(limit: int, only: List[str]) -> None:
    _per_page=min(limit, 100)
    runs: List[Dict[str, Any]] = []
    page=1
    while len(runs) < limit:
        _data=_get(f"{API_ROOT}/runs", params={"per_page": per_page, "page": page})
        _batch=data.get("workflow_runs", [])
        if not batch:
            break
        runs.extend(batch)
        page += 1
    runs=runs[:limit]
    if only:
        _only_set={o.strip().lower() for o in only}
        runs=[
            r
            for r in runs
            if (r.get("conclusion") or r.get("status")).lower() in only_set  # type: ignore[union-attr]
        ]
    print(f"Showing {len(runs)} runs (requested {limit})")
    for r in runs:
        _rid=r.get("id")
        _num=r.get("run_number")
        _name=r.get("name")
        _status=r.get("status")
        _conclusion=r.get("conclusion") or "-"
        _event=r.get("event")
        _created=r.get("created_at")
        _url=r.get("html_url")
        print(
            f"    #{num} id={rid} {name} event={event} status={status} "
            f"conclusion={conclusion} created={created}"
        )
    print(f"  {url}")


def show_run(runid: int) -> None:
    _jobs_data=_get(f"{API_ROOT}/runs/{run_id}/jobs")
    _jobs=jobs_data.get("jobs", [])
    if not jobs:
        print(f"No jobs for run {run_id}")
        return
    print(f"Run {run_id} jobs ({len(jobs)}):")
    for j in jobs:
        _jid=j.get("id")
        _name=j.get("name")
        _status=j.get("status")
        _conclusion=j.get("conclusion")
        _started=j.get("started_at")
        _completed=j.get("completed_at")
        _html_url=j.get("html_url")
        print(
            f"- {name} id={jid} status={status} conclusion={conclusion} "
            f"started={started} completed={completed}"
        )
        print(f"  {html_url}")
        # Steps summary (only failed or timed out ones for brevity)
        for s in j.get("steps", []):
            _sc=s.get("conclusion")
            if sc and sc not in ("success", "skipped"):
                print(f"    * Step '{s.get('name')}' conclusion={sc}")


def summarize_failures(limit: int) -> None:
    _per_page=min(limit, 100)
    _data=_get(f"{API_ROOT}/runs", params={"per_page": per_page})
    _runs=data.get("workflow_runs", [])[:limit]
    failed: List[Dict[str, Any]] = [
        r
        for r in runs
        if (r.get("conclusion") or "").lower() in {"failure", "cancelled", "timed_out"}
    ]
    if not failed:
        print("No failed/cancelled/timed_out runs in recent set.")
        return
    print(f"Found {len(failed)} problematic runs (out of {len(runs)} scanned):")
    for r in failed:
        print(
            f"-    #{r.get('run_number')} {r.get('name')} conclusion={r.get('conclusion')} "
            f"url={r.get('html_url')}"
        )
    # Optional deeper look at first failure
    first=failed[0]
    print("\nDetail of first failed run steps:")
    _jobs_data=_get(f"{API_ROOT}/runs/{first['id']}/jobs")
    for j in jobs_data.get("jobs", []):
        if j.get("conclusion") != "success":
            print(
                f" Job: {j.get('name')} conclusion={j.get('conclusion')} "
                f"url={j.get('html_url')}"
            )
            for s in j.get("steps", []):
                _sc=s.get("conclusion")
                if sc and sc != "success":
                    print(
                        f"    - Step: {s.get('name')} status={s.get('status')} "
                        f"conclusion={sc}"
                    )
    # Exit non-zero for pipeline use
    sys.exit(1)


def parse_args(argv: List[str]) -> argparse.Namespace:
    p=argparse.ArgumentParser(
        _prog="actions_inspector",
        _formatter_class=argparse.RawDescriptionHelpFormatter,
        _description=textwrap.dedent(
            """Inspect GitHub Actions runs & jobs for this repository.
                        Commands:
                            list-runs                   List workflow runs
                            show-run <id>               Show jobs & failed steps for run id
                            summarize-failures          Summarize and exit non-zero on failures
                            fetch-logs <run_id>         Download & extract job logs for run
                            download-artifacts <run_id> Download & extract artifacts for run
                        """
        ),
    )
    p.add_argument(
        "--debug",
        _action="store_true",
        _help="Enable verbose debug and token verification checks",
    )
    _sub=p.add_subparsers(dest="command", required=True)

    _pr=sub.add_parser("list-runs")
    pr.add_argument("--limit", type=int, default=30, help="Max runs to list (<=300)")
    pr.add_argument(
        "--only",
        _type=str,
        _default="",
        _help="Comma list of conclusions to include (e.g. failed, cancelled)",
    )

    _sr=sub.add_parser("show-run")
    sr.add_argument("run_id", type=int, help="Run ID to inspect")

    _sf=sub.add_parser("summarize-failures")
    sf.add_argument("--limit", type=int, default=50, help="Max runs to scan")

    _fl=sub.add_parser("fetch-logs")
    fl.add_argument("run_id", type=int, help="Run ID to download logs for")
    fl.add_argument(
        "--out-dir",
        _type=str,
        _default="logs/actions",
        _help="Directory to store extracted logs",
    )

    _da=sub.add_parser("download-artifacts")
    da.add_argument("run_id", type=int, help="Run ID to download artifacts for")
    da.add_argument(
        "--out-dir",
        _type=str,
        _default="artifacts/actions",
        _help="Directory to store extracted artifacts",
    )

    return p.parse_args(argv)


def main(argv: List[str]) -> None:
    _args=parse_args(argv)
    if args.debug:
    # Basic token diagnostics before executing command
        _tok=os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or ""
        print(
            f"[debug] token length={len(tok)} startswith={tok[:4]!r} endswith={tok[-4:]!r} "
            f"spaces?={tok != tok.strip()}"
        )
        # Try user endpoint to confirm scopes
        try:
            _udata=_get("https://api.github.com/user")
            print(
                f"[debug] authenticated as: {udata.get('login')} (id={udata.get('id')})"
            )
        except SystemExit:
            print("[debug] token failed user endpoint check")
            raise
        # Try minimal runs endpoint
        try:
            _test_runs=_get(f"{API_ROOT}/runs", params={"per_page": 1})
            print(f"[debug] can access actions runs: keys={list(test_runs.keys())[:5]}")
        except SystemExit:
            print("[debug] token failed actions runs endpoint check")
            raise
    if args.command == "list-runs":
        only_list=(
            [o for o in args.only.split(", ") if o.strip()]
            if getattr(args, "only", "")
            else []
        )
        list_runs(min(getattr(args, "limit", 30), 300), only_list)
    elif args.command == "show-run":
        show_run(args.run_id)
    elif args.command == "summarize-failures":
        summarize_failures(getattr(args, "limit", 50))
    elif args.command == "fetch-logs":
        fetch_logs(args.run_id, getattr(args, "out_dir", "logs/actions"))
    elif args.command == "download-artifacts":
        _download_artifacts(args.run_id, getattr(args, "out_dir", "artifacts/actions"))
    else:
        print("Unknown command", file=sys.stderr)
        sys.exit(2)


if _name__== "__main__":    # pragma: no cover
    main(sys.argv[1:])
