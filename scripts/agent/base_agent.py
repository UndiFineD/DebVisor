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
Base Agent: Common functionality for all AI-powered agents.

Provides shared functionality for agents that improve code files using AI assistance.
"""

import argparse
import difflib
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
from typing import Optional

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None  # type: ignore[assignment]


def setup_logging(verbosity_arg: int = 0) -> None:
    """Configure logging based on environment variable and argument."""
    env_verbosity = os.environ.get('DV_AGENT_VERBOSITY')
    levels = {
        'quiet': logging.ERROR,
        'minimal': logging.WARNING,
        'normal': logging.INFO,
        'elaborate': logging.DEBUG,
        '0': logging.ERROR,
        '1': logging.WARNING,
        '2': logging.INFO,
        '3': logging.DEBUG,
    }
    # Determine level from environment
    if env_verbosity:
        level = levels.get(env_verbosity.lower(), logging.INFO)
    else:
        level = logging.INFO
    # If argument is provided, it forces DEBUG (elaborate)
    if verbosity_arg > 0:
        level = logging.DEBUG
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


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


# Import markdown fixing functionality (optional).
try:
    from scripts.fix.fix_markdown_lint import fix_markdown_content  # type: ignore
except ImportError:
    try:
        import importlib.util
        fix_dir = Path(__file__).parent.parent / 'fix'
        spec = importlib.util.spec_from_file_location("fix_markdown_lint", str(fix_dir / "fix_markdown_lint.py"))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules["fix_markdown_lint"] = module
            spec.loader.exec_module(module)
            fix_markdown_content = module.fix_markdown_content
        else:
            raise ImportError
    except Exception:  # pragma: no cover
        def fix_markdown_content(text: str) -> str:
            return text


class BaseAgent:
    """Base class for all AI-powered agents."""

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.previous_content = ""
        self.current_content = ""

    def read_previous_content(self) -> str:
        """Read the existing file content."""
        if self.file_path.exists():
            self.previous_content = self.file_path.read_text(encoding='utf-8')
        else:
            self.previous_content = self._get_default_content()
        return self.previous_content

    def _get_default_content(self) -> str:
        """Return default content for new files. Override in subclasses."""
        return "# Default content\n\n# Add content here\n"

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the content. Override in subclasses."""
        description = f"Improve the {self.__class__.__name__.replace('Agent', '').lower()} for {self.file_path.stem}"
        try:
            improvement = self.run_subagent(description, prompt, self.previous_content)
            self.current_content = improvement
            return self.current_content
        except Exception as e:
            logging.warning(f"Failed to improve content: {e}")
            self.current_content = self.previous_content
            return self.current_content

    def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        """
        Run a subagent using one of several AI backends.

        Supported backends (selected by `DV_AGENT_BACKEND`):
            - auto (default): try local `copilot` CLI, then GitHub Models (if configured)
                then `gh copilot` for command-like prompts
            - copilot: force local `copilot` CLI
            - gh: force `gh copilot` (CLI extension)
            - github-models: force GitHub Models OpenAI-compatible API

        Notes:
            - "github-models" is an API-backed LLM route (Copilot-adjacent), not Copilot Chat.
            - When explicit backends are misconfigured/unavailable, an exception may be raised.

        Args:
            description: Description of the task
            prompt: The prompt to send to Copilot
            original_content: Original content (for context)

        Returns:
            AI response as a string, or fallback suggestions
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
                # Non-interactive mode requires --allow-all-tools, but we explicitly deny
                # the dangerous ones for safety in automated runs.
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
            # The `gh copilot` extension is primarily for suggesting/explaining terminal
            # commands. Avoid using it for general prose/code rewrite prompts.
            if not allow_non_command_prompt and not _looks_like_command(prompt):
                return None
            # Warn if prompt is too long for gh copilot
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
            return self.llm_chat_via_github_models(
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
        # auto (default): prefer local Copilot CLI, then GitHub Models if configured.
        result = _try_copilot_cli()
        if result is not None:
            return result
        try:
            result = _try_github_models()
            if result is not None:
                return result
        except Exception:
            # Keep auto mode resilient.
            pass
        result = _try_gh_copilot(allow_non_command_prompt=False)
        if result is not None:
            return result
        # In environments without any configured backend, do not overwrite files with placeholders.
        return original_content or self._get_fallback_response()

    @staticmethod
    def get_backend_status() -> dict:
        """Return a diagnostic snapshot of backend availability/config.

        Never includes secret values (token contents), only set/unset.
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

    @staticmethod
    def describe_backends() -> str:
        """Human-readable backend diagnostics for debugging."""
        status = BaseAgent.get_backend_status()
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

    def llm_chat_via_github_models(
        self,
        *,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout_s: int = 60,
    ) -> str:
        """Call a GitHub Models OpenAI-compatible chat endpoint.

        This is intentionally small and dependency-light (uses `requests`).
        It is designed for programmatic access (route #2) and is safe to mock in tests.

        Required:
            - `token` argument OR `GITHUB_TOKEN` env var
            - `base_url` argument OR `GITHUB_MODELS_BASE_URL` env var
        """
        if requests is None:  # pragma: no cover
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

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot CLI is unavailable. Override in subclasses."""
        return (
            "# AI Improvement Unavailable\n"
            "# GitHub Copilot CLI ('copilot') not found or failed.\n"
            "# Install Copilot CLI: https://github.com/github/copilot-cli\n"
            "# Windows: winget install GitHub.Copilot\n"
            "# npm: npm install -g @github/copilot\n"
        )

    def update_file(self) -> None:
        """Write the improved content back to the file."""
        content_to_write = self.current_content
        # Only run the markdown fixer on markdown-like files. Applying markdown
        # normalization to source code can corrupt it.
        suffix = self.file_path.suffix.lower()
        is_markdown = suffix in {'.md', '.markdown'} or self.file_path.name.lower().endswith('.plan.md')
        if is_markdown:
            content_to_write = fix_markdown_content(content_to_write)
        self.file_path.write_text(content_to_write, encoding='utf-8')

    def get_diff(self) -> str:
        """Get the diff between previous and current content."""
        diff = difflib.unified_diff(
            self.previous_content.splitlines(keepends=True),
            self.current_content.splitlines(keepends=True),
            fromfile='previous',
            tofile='current'
        )
        return ''.join(diff)


from typing import Optional, Type, Callable, Any

# ... (imports)

def create_main_function(agent_class: Type[BaseAgent], description: str, context_help: str) -> Callable[[], None]:
    """Create a main function for an agent class."""
    def main() -> None:
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            '--describe-backends',
            action='store_true',
            help='Print which AI backends are available/configured and exit',
        )
        parser.add_argument(
            '--backend',
            choices=['auto', 'copilot', 'gh', 'github-models'],
            default=None,
            help='Select backend (overrides DV_AGENT_BACKEND for this run only)',
        )
        parser.add_argument(
            '--verbose',
            '-v',
            action='count',
            default=0,
            help='Increase verbosity (can be used multiple times, e.g. -vv)',
        )
        parser.add_argument('--context', required=True, help=context_help)
        parser.add_argument('--prompt', required=True, help='Prompt for improving the content')
        args = parser.parse_args()
        setup_logging(args.verbose)
        if args.backend:
            os.environ['DV_AGENT_BACKEND'] = args.backend
        if args.describe_backends:
            print(agent_class.describe_backends())
            return
        agent = agent_class(args.context)
        agent.read_previous_content()
        agent.improve_content(args.prompt)
        agent.update_file()
        diff = agent.get_diff()
        if diff:
            logging.info(f"{agent_class.__name__.replace('Agent', '').lower()} updated:")
            logging.info(diff)
        else:
            logging.info(f"No changes made to {agent_class.__name__.replace('Agent', '').lower()}.")
    return main
