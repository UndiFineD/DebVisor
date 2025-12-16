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

This module provides the infrastructure for communicating with various AI backends:
- GitHub Copilot CLI (local command-line tool)
- GitHub Copilot via gh CLI
- GitHub Models API (OpenAI-compatible endpoint)

Supports automatic backend selection with fallback mechanisms.
Configurable via environment variables for flexibility in CI/CD and development.

Environment Variables:
    DV_AGENT_BACKEND: Selected backend ('auto', 'copilot', 'gh', 'github-models')
    DV_AGENT_REPO_ROOT: Override repository root detection
    DV_AGENT_MAX_CONTEXT_CHARS: Max chars to include as context (default: 12000)
    DV_AGENT_MODEL: Model name for GitHub Models backend
    DV_AGENT_SYSTEM_PROMPT: System prompt for AI backends
    GITHUB_TOKEN: Authentication token for GitHub Models API
    GITHUB_MODELS_BASE_URL: API endpoint URL for GitHub Models
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
    """Resolve the repository root directory.
    
    Uses environment variable or automatic detection via .git marker.
    Falls back to current working directory if no repo found.
    
    Args:
        None.
        
    Returns:
        Path: Repository root directory.
        
    Environment Variables:
        DV_AGENT_REPO_ROOT: If set, use this as repo root (can use ~).
        
    Note:
        - Searches from current file location upward for .git directory
        - Returns CWD if no .git found
        - Path is always resolved to absolute form
    """
    env_root = os.environ.get("DV_AGENT_REPO_ROOT")
    if env_root:
        logging.debug(f"Using DV_AGENT_REPO_ROOT: {env_root}")
        return Path(env_root).expanduser().resolve()
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / ".git").exists():
            logging.debug(f"Found repo root at {parent}")
            return parent
    logging.debug(f"No repo root found, using CWD: {Path.cwd()}")
    return Path.cwd()


def _command_available(command: str) -> bool:
    """Check if a command is available in PATH.
    
    Attempts to run command with --version flag to verify availability.
    
    Args:
        command: Command name to check (e.g., 'copilot', 'gh').
        
    Returns:
        bool: True if command is available and working, False otherwise.
        
    Note:
        - Runs with 5-second timeout
        - Catches all subprocess errors and returns False
        - Non-zero exit codes are treated as unavailable
    """
    try:
        logging.debug(f"Checking if command is available: {command}")
        subprocess.run(
            [command, '--version'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=5,
            check=True,
        )
        logging.debug(f"Command available: {command}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        logging.debug(f"Command not available: {command}")
        return False


def llm_chat_via_github_models(
    prompt: str,
    model: str,
    system_prompt: str = "You are a helpful assistant.",
    base_url: Optional[str] = None,
    token: Optional[str] = None,
    timeout_s: int = 60,
) -> str:
    """Call a GitHub Models OpenAI-compatible chat endpoint.
    
    Makes an HTTP request to a GitHub Models API endpoint with the provided
    prompt and returns the AI's response.
    
    Args:
        prompt: User prompt to send to the model.
        model: Model identifier (e.g., 'gpt-4', 'claude-3-sonnet').
        system_prompt: System message for the model. Defaults to helpful assistant.
        base_url: API endpoint base URL. Can also be set via GITHUB_MODELS_BASE_URL.
        token: GitHub personal access token. Can also be set via GITHUB_TOKEN.
        timeout_s: HTTP request timeout in seconds. Defaults to 60.
        
    Returns:
        str: The AI model's response text.
        
    Raises:
        RuntimeError: If required dependencies or configuration are missing.
        requests.RequestException: If HTTP request fails.
        
    Example:
        response = llm_chat_via_github_models(
            prompt="What is Python?",
            model="gpt-4",
            base_url="https://api.github.com/models",
            token="ghp_..."
        )
        
    Note:
        - Requires 'requests' package to be installed
        - Follows OpenAI API format for compatibility
        - Raises RuntimeError if requests library unavailable
    """
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
    
    logging.debug(f"Making GitHub Models API request to {url} with model {model}")
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        timeout=timeout_s,
    )
    response.raise_for_status()
    data = response.json()
    try:
        result = (data["choices"][0]["message"]["content"] or "").strip()
        logging.debug(f"Received {len(result)} bytes from GitHub Models API")
        return result
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Unexpected response shape from LLM endpoint: {data!r}") from e


def run_subagent(description: str, prompt: str, original_content: str = "") -> Optional[str]:
    """Run a subagent using one of several AI backends.
    
    Attempts to run a task using available AI backends with automatic selection
    and fallback mechanisms. Tries backends in order of preference:
    1. GitHub Copilot CLI (if DV_AGENT_BACKEND=copilot)
    2. GitHub Models API (if configured)
    3. gh copilot (if available)
    4. Falls back gracefully if no backend available
    
    Args:
        description: Human-readable task description (e.g., "Improve code quality").
        prompt: The specific prompt/task to send to the AI backend.
        original_content: Current file content for context (limited by DV_AGENT_MAX_CONTEXT_CHARS).
                         Defaults to empty string.
        
    Returns:
        Optional[str]: The AI backend's response, or None if all backends fail.
        
    Raises:
        RuntimeError: If explicit backend requested but unavailable.
        
    Example:
        result = run_subagent(
            description="Add docstrings to function",
            prompt="Add Google-style docstrings",
            original_content=source_code
        )
        if result:
            print(result)
        else:
            print("No AI backend available")
            
    Environment Variables:
        DV_AGENT_BACKEND: Force specific backend ('copilot', 'gh', 'github-models', or 'auto').
        DV_AGENT_MAX_CONTEXT_CHARS: Maximum context size (default 12000).
        
    Note:
        - Context is trimmed to fit within DV_AGENT_MAX_CONTEXT_CHARS
        - Full prompt includes task description and original file context
        - Logs debug info for troubleshooting
        - Handles timeouts and errors gracefully
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
            logging.debug("Copilot CLI not available")
            return None
        full_prompt = _build_full_prompt()
        repo_root = _resolve_repo_root()
        try:
            logging.debug("Attempting to use Copilot CLI backend")
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
                logging.info("Copilot CLI backend succeeded")
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
            logging.debug("gh CLI not available")
            return None
        if not allow_non_command_prompt and not _looks_like_command(prompt):
            logging.debug("Prompt doesn't look like a command, skipping gh copilot")
            return None
        max_len = 2000
        prompt_to_use = prompt
        if len(prompt) > max_len:
            logging.warning(f"Prompt truncated from {len(prompt)} to {max_len} chars for gh copilot")
            prompt_to_use = prompt[:max_len]

        try:
            logging.debug("Attempting to use gh copilot backend")
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
                logging.info("gh copilot backend succeeded")
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
            logging.debug("No model specified for GitHub Models")
            return None
        if not base_url or not base_url.strip():
            logging.debug("No base URL specified for GitHub Models")
            return None
        if not token:
            logging.debug("No GitHub token specified for GitHub Models")
            return None
        full_prompt = _build_full_prompt()
        try:
            logging.debug("Attempting to use GitHub Models backend")
            return llm_chat_via_github_models(
                prompt=full_prompt,
                model=model,
                system_prompt=system_prompt,
                base_url=base_url,
                token=token,
            )
        except Exception as e:
            logging.warning(f"GitHub Models backend error: {e}")
            return None

    backend = os.environ.get("DV_AGENT_BACKEND", "auto").strip().lower()
    logging.debug(f"Using backend: {backend}")
    
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
    logging.debug("Trying backends in order: copilot, github-models, gh")
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
    
    logging.warning("No AI backend available")
    return None


def get_backend_status() -> dict:
    """Return a diagnostic snapshot of backend availability and configuration.
    
    Checks which AI backends are available and configured on the system.
    Used for diagnostics and debugging backend selection issues.
    
    Returns:
        dict: Status information including:
            - selected_backend: Current backend choice (auto, copilot, gh, etc.)
            - repo_root: Detected repository root directory
            - max_context_chars: Maximum context size to include
            - commands: Dict with availability of 'copilot' and 'gh' CLIs
            - github_models: Dict with GitHub Models configuration status
            
    Example:
        status = get_backend_status()
        if status['github_models']['configured']:
            print("GitHub Models is ready to use")
            
    Note:
        - Doesn't require any external services
        - Safe to call for diagnostics
        - Returns info on all backends regardless of selection
    """
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
    """Return human-readable backend diagnostics for debugging.
    
    Generates a formatted text report of all AI backends and their configuration status.
    Useful for troubleshooting when the agent can't find an available backend.
    
    Returns:
        str: Multi-line formatted text with backend diagnostics.
        
    Example:
        print(BaseAgent.describe_backends())
        # Output:
        # Backend diagnostics:
        # - selected: auto
        # - repo_root: /home/user/project
        # - local copilot CLI available: yes
        # - gh CLI available: yes
        # - github-models configured: yes
        
    Note:
        - Safe to call from user code
        - Doesn't require AI backend to be working
        - Shows configuration issues clearly
    """
    status = get_backend_status()
    cmd = status["commands"]
    models = status["github_models"]

    def yn(value: bool) -> str:
        return "yes" if value else "no"
    
    result = "\n".join(
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
    logging.debug("Backend diagnostics generated")
    return result
