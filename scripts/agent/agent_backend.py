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
Agent Backend: Handles communication with AI backends.
"""

import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]


def _resolve_repo_root() -> Path:
    env_root = os.environ.get("DV_AGENT_REPO_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / ".git").exists():
            return parent
    return Path.cwd()


def _command_available(command: str) -> bool:
    try:
        subprocess.run(
            [command, '--version'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=5,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


def llm_chat_via_github_models(
    prompt: str,
    model: str,
    system_prompt: str = "You are a helpful assistant.",
    base_url: Optional[str] = None,
    token: Optional[str] = None,
    timeout_s: int = 60,
) -> str:
    """Call a GitHub Models OpenAI-compatible chat endpoint."""
    if requests is None:
        raise RuntimeError("Missing dependency: install 'requests' to use GitHub Models backend")
    resolved_token = token or os.environ.get("GITHUB_TOKEN")
    if not resolved_token:
        raise RuntimeError("Missing token: set GITHUB_TOKEN env var or pass token=")
    resolved_base_url = (base_url or os.environ.get("GITHUB_MODELS_BASE_URL") or "").strip()
    if not resolved_base_url:
        raise RuntimeError(
            "Missing base URL: set GITHUB_MODELS_BASE_URL env var or pass base_url="
        )
    url = resolved_base_url.rstrip("/") + "/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }
    headers = {
        "Authorization": f"Bearer {resolved_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        timeout=timeout_s,
    )
    response.raise_for_status()
    data = response.json()
    try:
        return (data["choices"][0]["message"]["content"] or "").strip()
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Unexpected response shape from LLM endpoint: {data!r}") from e


def run_subagent(description: str, prompt: str, original_content: str = "") -> Optional[str]:
    """
    Run a subagent using one of several AI backends.
    """

    def _build_full_prompt() -> str:
        try:
            max_context_chars = int(os.environ.get("DV_AGENT_MAX_CONTEXT_CHARS", "12000"))
        except ValueError:
            max_context_chars = 12_000
        trimmed_original = (original_content or "")[:max_context_chars]
        return (
            f"Task: {description}\n\n"
            f"Prompt:\n{prompt}\n\n"
            "Context (existing file content):\n"
            f"{trimmed_original}"
        ).strip()

    def _try_copilot_cli() -> Optional[str]:
        if not _command_available('copilot'):
            return None
        full_prompt = _build_full_prompt()
        repo_root = _resolve_repo_root()
        try:
            result = subprocess.run(
                [
                    'copilot',
                    '--prompt',
                    full_prompt,
                    '--no-color',
                    '--log-level',
                    'error',
                    '--add-dir',
                    str(repo_root),
                    '--allow-all-tools',
                    '--disable-parallel-tools-execution',
                    '--deny-tool',
                    'write',
                    '--deny-tool',
                    'shell',
                    '--silent',
                    '--stream',
                    'off',
                ],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=180,
                cwd=str(repo_root),
                check=False
            )
            stdout = (result.stdout or "").strip()
            if result.returncode == 0 and stdout:
                return stdout
            if result.returncode != 0:
                logging.debug(f"Copilot CLI failed (code {result.returncode}): {result.stderr}")
        except subprocess.TimeoutExpired:
            logging.warning("Copilot CLI timed out")
            return None
        except Exception as e:
            logging.warning(f"Copilot CLI error: {e}")
            return None
        return None

    def _looks_like_command(text: str) -> bool:
        t = (text or "").strip()
        if not t:
            return False
        if "\n" in t:
            return False
        if any(op in t for op in ("|", "&&", ";")):
            return True
        starters = (
            "git ",
            "gh ",
            "docker ",
            "kubectl ",
            "pip ",
            "python ",
            "npm ",
            "node ",
            "pwsh ",
            "powershell ",
            "Get-",
            "Set-",
            "New-",
        )
        return t.startswith(starters)

    def _try_gh_copilot(*, allow_non_command_prompt: bool) -> Optional[str]:
        if not _command_available('gh'):
            return None
        if not allow_non_command_prompt and not _looks_like_command(prompt):
            return None
        max_len = 2000
        prompt_to_use = prompt
        if len(prompt) > max_len:
            logging.warning(f"Prompt truncated from {len(prompt)} to {max_len} chars for gh copilot")
            prompt_to_use = prompt[:max_len]

        try:
            result = subprocess.run(
                ['gh', 'copilot', 'explain', prompt_to_use],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,
                cwd=str(_resolve_repo_root()),
                check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                return f"# GitHub Copilot (gh) Explanation:\n{result.stdout.strip()}"
            if result.returncode != 0:
                logging.debug(f"gh copilot failed (code {result.returncode}): {result.stderr}")
        except subprocess.TimeoutExpired:
            logging.warning("gh copilot timed out")
            return None
        except Exception as e:
            logging.warning(f"gh copilot error: {e}")
            return None
        return None

    def _try_github_models() -> Optional[str]:
        model = (
            os.environ.get("DV_AGENT_MODEL")
            or os.environ.get("GITHUB_MODELS_MODEL")
            or ""
        ).strip()
        system_prompt = os.environ.get(
            "DV_AGENT_SYSTEM_PROMPT",
            "You are a helpful assistant. Follow the user instructions exactly.",
        )
        base_url = os.environ.get("GITHUB_MODELS_BASE_URL")
        token = os.environ.get("GITHUB_TOKEN")
        if not model:
            return None
        if not base_url or not base_url.strip():
            return None
        if not token:
            return None
        full_prompt = _build_full_prompt()
        return llm_chat_via_github_models(
            prompt=full_prompt,
            model=model,
            system_prompt=system_prompt,
            base_url=base_url,
            token=token,
        )

    backend = os.environ.get("DV_AGENT_BACKEND", "auto").strip().lower()
    if backend in {"copilot", "local", "copilot-cli"}:
        result = _try_copilot_cli()
        if result is None:
            raise RuntimeError("Requested DV_AGENT_BACKEND=copilot but local 'copilot' CLI is unavailable")
        return result
    if backend in {"gh", "gh-copilot"}:
        result = _try_gh_copilot(allow_non_command_prompt=True)
        if result is None:
            raise RuntimeError("Requested DV_AGENT_BACKEND=gh but 'gh copilot' is unavailable")
        return result
    if backend in {"github-models", "github_models", "models"}:
        result = _try_github_models()
        if result is None:
            raise RuntimeError(
                "Requested DV_AGENT_BACKEND=github-models but it is not configured; "
                "set GITHUB_MODELS_BASE_URL, GITHUB_TOKEN, and DV_AGENT_MODEL (or GITHUB_MODELS_MODEL)"
            )
        return result
    
    # auto (default)
    result = _try_copilot_cli()
    if result is not None:
        return result
    try:
        result = _try_github_models()
        if result is not None:
            return result
    except Exception:
        pass
    result = _try_gh_copilot(allow_non_command_prompt=False)
    if result is not None:
        return result
    
    return None


def get_backend_status() -> dict:
    """Return a diagnostic snapshot of backend availability/config."""
    backend = os.environ.get("DV_AGENT_BACKEND", "auto").strip().lower()
    repo_root = str(_resolve_repo_root())
    try:
        max_context_chars = int(os.environ.get("DV_AGENT_MAX_CONTEXT_CHARS", "12000"))
    except ValueError:
        max_context_chars = 12_000
    models_base_url = (os.environ.get("GITHUB_MODELS_BASE_URL") or "").strip()
    models_model = (
        os.environ.get("DV_AGENT_MODEL")
        or os.environ.get("GITHUB_MODELS_MODEL")
        or ""
    ).strip()
    token_set = bool(os.environ.get("GITHUB_TOKEN"))
    return {
        "selected_backend": backend,
        "repo_root": repo_root,
        "max_context_chars": max_context_chars,
        "commands": {
            "copilot": _command_available("copilot"),
            "gh": _command_available("gh"),
        },
        "github_models": {
            "requests_installed": requests is not None,
            "base_url_set": bool(models_base_url),
            "model_set": bool(models_model),
            "token_set": token_set,
            "configured": bool(models_base_url and models_model and token_set and requests is not None),
        },
    }


def describe_backends() -> str:
    """Human-readable backend diagnostics for debugging."""
    status = get_backend_status()
    cmd = status["commands"]
    models = status["github_models"]

    def yn(value: bool) -> str:
        return "yes" if value else "no"
    return "\n".join(
        [
            "Backend diagnostics:",
            f"- selected: {status['selected_backend']}",
            f"- repo_root: {status['repo_root']}",
            f"- max_context_chars: {status['max_context_chars']}",
            f"- local copilot CLI available: {yn(bool(cmd.get('copilot')))}",
            f"- gh CLI available: {yn(bool(cmd.get('gh')))}",
            "- github-models configured:",
            f"  - requests installed: {yn(bool(models.get('requests_installed')))}",
            f"  - base_url set: {yn(bool(models.get('base_url_set')))}",
            f"  - model set: {yn(bool(models.get('model_set')))}",
            f"  - token set: {yn(bool(models.get('token_set')))}",
        ]
    )
