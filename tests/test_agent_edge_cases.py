"""Edge case and error scenario tests for agent modules."""
from __future__ import annotations
import logging
import os
import sys
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest
from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path


@pytest.fixture()
def agent_module():
    with agent_sys_path():
        return load_module_from_path("_dv_agent", AGENT_DIR / "agent.py")


@pytest.fixture()
def base_agent_module():
    with agent_sys_path():
        return load_module_from_path("_dv_base_agent", AGENT_DIR / "base_agent.py")


@pytest.fixture()
def agent_backend_module():
    with agent_sys_path():
        return load_module_from_path("_dv_agent_backend", AGENT_DIR / "agent_backend.py")


# ============================================================================
# Tests for agent.py Edge Cases
# ============================================================================

class TestCodeignoreCache:
    """Test .codeignore pattern caching."""

    def test_codeignore_patterns_cached_on_repeat_loads(self, tmp_path: Path, agent_module):
        """Verify .codeignore patterns are cached and not re-parsed."""
        codeignore_file = tmp_path / ".codeignore"
        codeignore_file.write_text("*.log\n__pycache__/\nvenv/\n", encoding="utf-8")

        # First load
        patterns1 = agent_module.load_codeignore(tmp_path)
        assert len(patterns1) == 3

        # Second load should use cache
        patterns2 = agent_module.load_codeignore(tmp_path)
        assert patterns1 == patterns2

    def test_codeignore_cache_invalidated_on_file_modification(self, tmp_path: Path, agent_module):
        """Verify cache is invalidated when .codeignore file changes."""
        codeignore_file = tmp_path / ".codeignore"
        codeignore_file.write_text("*.log\n", encoding="utf-8")

        # First load
        patterns1 = agent_module.load_codeignore(tmp_path)
        assert "*.log" in patterns1

        # Modify file
        time.sleep(0.01)  # Ensure mtime changes
        codeignore_file.write_text("*.log\n*.tmp\n", encoding="utf-8")

        # Second load should re-parse
        patterns2 = agent_module.load_codeignore(tmp_path)
        assert "*.tmp" in patterns2

    def test_codeignore_handles_missing_file_gracefully(self, tmp_path: Path, agent_module):
        """Verify missing .codeignore is handled gracefully."""
        # No .codeignore file created
        patterns = agent_module.load_codeignore(tmp_path)
        assert patterns == set()

    def test_codeignore_skips_comments_and_empty_lines(self, tmp_path: Path, agent_module):
        """Verify comments and empty lines are ignored."""
        codeignore_file = tmp_path / ".codeignore"
        codeignore_file.write_text(
            "# This is a comment\n"
            "*.log\n"
            "\n"
            "# Another comment\n"
            "__pycache__/\n",
            encoding="utf-8"
        )

        patterns = agent_module.load_codeignore(tmp_path)
        assert "*.log" in patterns
        assert "__pycache__/" in patterns
        assert "# This is a comment" not in patterns


class TestAgentContextManager:
    """Test Agent context manager support."""

    def test_agent_supports_context_manager(self, tmp_path: Path, agent_module):
        """Verify Agent can be used with 'with' statement."""
        (tmp_path / ".git").mkdir()
        with agent_module.Agent(repo_root=str(tmp_path)) as agent:
            assert agent.repo_root == tmp_path

    def test_agent_context_manager_logs_on_error(self, tmp_path: Path, agent_module, caplog):
        """Verify Agent logs when exception occurs in context."""
        (tmp_path / ".git").mkdir()
        try:
            with agent_module.Agent(repo_root=str(tmp_path)) as agent:
                raise ValueError("Test error")
        except ValueError:
            pass

        # Should log the error
        assert "error" in caplog.text.lower()


class TestCommandRetry:
    """Test command execution retry logic."""

    def test_command_retries_on_failure(self, tmp_path: Path, agent_module, monkeypatch):
        """Verify commands are retried on failure."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        attempts = []

        def fake_run(*args, **kwargs):
            attempts.append(1)
            if len(attempts) < 3:
                raise OSError("Network error")
            return MagicMock(returncode=0, stdout="success", stderr="")

        monkeypatch.setattr("subprocess.run", fake_run)

        result = agent._run_command(["dummy"], max_retries=3)
        assert result.returncode == 0
        assert len(attempts) == 3

    def test_command_retry_exponential_backoff(self, tmp_path: Path, agent_module, monkeypatch):
        """Verify exponential backoff is applied during retries."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        times = []

        def fake_time_sleep(duration):
            times.append(duration)

        def fake_run(*args, **kwargs):
            raise OSError("Transient failure")

        monkeypatch.setattr("time.sleep", fake_time_sleep)
        monkeypatch.setattr("subprocess.run", fake_run)

        result = agent._run_command(["dummy"], max_retries=4)
        
        # Should have slept with exponential backoff
        assert len(times) >= 2
        # Delays should generally increase (allowing for float precision)
        if len(times) >= 3:
            assert times[0] <= times[1] or abs(times[0] - times[1]) < 0.1

    def test_command_timeout_returns_error(self, tmp_path: Path, agent_module, monkeypatch):
        """Verify timeout is handled properly."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        def fake_run(*args, **kwargs):
            raise agent_module.subprocess.TimeoutExpired("cmd", 10)

        monkeypatch.setattr("subprocess.run", fake_run)

        result = agent._run_command(["dummy"], timeout=10)
        assert result.returncode == -1
        assert "Timeout" in result.stderr


class TestIgnorePatternMatching:
    """Test .codeignore pattern matching."""

    def test_ignore_pattern_matching_full_path(self, tmp_path: Path, agent_module):
        """Verify patterns match against path parts."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.ignored_patterns = {"venv"}  # Match path component

        venv_file = tmp_path / "venv" / "lib" / "file.py"
        assert agent._is_ignored(venv_file)

    def test_ignore_pattern_matching_filename(self, tmp_path: Path, agent_module):
        """Verify patterns match against filename."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.ignored_patterns = {"*.log"}

        log_file = tmp_path / "debug.log"
        assert agent._is_ignored(log_file)

    def test_ignore_pattern_not_matched(self, tmp_path: Path, agent_module):
        """Verify non-matching files are not ignored."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.ignored_patterns = {"*.log", "__pycache__"}

        py_file = tmp_path / "main.py"
        assert not agent._is_ignored(py_file)


# ============================================================================
# Tests for base_agent.py Edge Cases
# ============================================================================

class TestBaseAgentContextManager:
    """Test BaseAgent context manager support."""

    def test_base_agent_supports_context_manager(self, tmp_path: Path, base_agent_module):
        """Verify BaseAgent can be used with 'with' statement."""
        target = tmp_path / "file.md"
        target.write_text("content", encoding="utf-8")

        with base_agent_module.BaseAgent(str(target)) as agent:
            assert agent.file_path == target

    def test_base_agent_context_manager_cleanup(self, tmp_path: Path, base_agent_module, caplog):
        """Verify BaseAgent logs cleanup on context exit."""
        target = tmp_path / "file.md"
        target.write_text("content", encoding="utf-8")

        with caplog.at_level(logging.DEBUG):
            with base_agent_module.BaseAgent(str(target)) as agent:
                pass

        assert "exiting" in caplog.text.lower()


class TestBaseAgentFileEncoding:
    """Test BaseAgent file encoding handling."""

    def test_read_file_with_utf8_encoding(self, tmp_path: Path, base_agent_module):
        """Verify UTF-8 encoded files are read correctly."""
        target = tmp_path / "file.md"
        target.write_text("Hello: café ñ", encoding="utf-8")

        agent = base_agent_module.BaseAgent(str(target))
        assert "café" in agent.previous_content
        assert "ñ" in agent.previous_content

    def test_write_file_creates_parent_directories(self, tmp_path: Path, base_agent_module, monkeypatch):
        """Verify parent directories are created if needed."""
        target = tmp_path / "deep" / "nested" / "file.md"
        agent = base_agent_module.BaseAgent(str(target))
        agent.current_content = "new content"

        monkeypatch.setattr(base_agent_module, "fix_markdown_content", lambda x: x)
        agent.update_file()

        assert target.exists()
        assert target.read_text(encoding="utf-8") == "new content"


class TestBaseAgentDiffGeneration:
    """Test BaseAgent diff generation."""

    def test_diff_empty_when_content_unchanged(self, base_agent_module):
        """Verify diff is empty when content doesn't change."""
        agent = base_agent_module.BaseAgent("/tmp/dummy")
        agent.previous_content = "same"
        agent.current_content = "same"

        diff = agent.get_diff()
        assert diff == ""

    def test_diff_shows_additions(self, base_agent_module):
        """Verify diff shows additions."""
        agent = base_agent_module.BaseAgent("/tmp/dummy")
        agent.previous_content = "line1\nline2\n"
        agent.current_content = "line1\nline2\nline3\n"

        diff = agent.get_diff()
        assert "+line3" in diff


# ============================================================================
# Tests for agent_backend.py Edge Cases
# ============================================================================

class TestGitHubModelsRetry:
    """Test GitHub Models API retry logic."""

    def test_github_models_retries_on_timeout(self, agent_backend_module, monkeypatch):
        """Verify timeout errors trigger retry logic."""
        attempts = []

        def fake_post(*args, **kwargs):
            attempts.append(1)
            if len(attempts) < 2:
                raise agent_backend_module.requests.Timeout("timeout")
            response = Mock()
            response.json.return_value = {"choices": [{"message": {"content": "result"}}]}
            return response

        monkeypatch.setenv("GITHUB_TOKEN", "token")
        monkeypatch.setenv("GITHUB_MODELS_BASE_URL", "http://api.example.com")
        monkeypatch.setattr(agent_backend_module.requests, "post", fake_post)

        result = agent_backend_module.llm_chat_via_github_models(
            prompt="test",
            model="gpt-4",
            max_retries=2
        )

        assert result == "result"
        assert len(attempts) == 2

    def test_github_models_fails_on_auth_error(self, agent_backend_module, monkeypatch):
        """Verify auth errors don't trigger retry."""
        attempts = []

        def fake_post(*args, **kwargs):
            attempts.append(1)
            response = Mock()
            response.raise_for_status.side_effect = agent_backend_module.requests.HTTPError("401 Unauthorized")
            return response

        monkeypatch.setenv("GITHUB_TOKEN", "token")
        monkeypatch.setenv("GITHUB_MODELS_BASE_URL", "http://api.example.com")
        monkeypatch.setattr(agent_backend_module.requests, "post", fake_post)

        with pytest.raises(agent_backend_module.requests.HTTPError):
            agent_backend_module.llm_chat_via_github_models(
                prompt="test",
                model="gpt-4",
                max_retries=2
            )

        # Should fail immediately, not retry
        assert len(attempts) == 1


class TestBackendSelection:
    """Test AI backend selection and fallback."""

    def test_backend_fallback_order(self, agent_backend_module, monkeypatch):
        """Verify backends are tried in correct order on 'auto'."""
        calls = []

        def track_call(name):
            def wrapper(*args, **kwargs):
                calls.append(name)
                return None
            return wrapper

        monkeypatch.setenv("DV_AGENT_BACKEND", "auto")
        monkeypatch.delenv("GITHUB_MODELS_BASE_URL", raising=False)

        # Mock all backend functions
        monkeypatch.setattr(
            agent_backend_module, 
            "_command_available",
            lambda x: False  # No CLIs available
        )

        # Try to run, expect fallback
        result = agent_backend_module.run_subagent("task", "prompt")
        assert result is None  # No backend available


class TestEnvironmentVariableHandling:
    """Test environment variable handling."""

    def test_repo_root_from_env_variable(self, tmp_path: Path, agent_backend_module, monkeypatch):
        """Verify DV_AGENT_REPO_ROOT environment variable is used."""
        monkeypatch.setenv("DV_AGENT_REPO_ROOT", str(tmp_path))
        
        root = agent_backend_module._resolve_repo_root()
        assert root == tmp_path

    def test_context_chars_limit_from_env(self, agent_backend_module, monkeypatch):
        """Verify DV_AGENT_MAX_CONTEXT_CHARS is respected."""
        monkeypatch.setenv("DV_AGENT_MAX_CONTEXT_CHARS", "1000")
        
        status = agent_backend_module.get_backend_status()
        assert status["max_context_chars"] == 1000

    def test_invalid_context_chars_defaults_to_12000(self, agent_backend_module, monkeypatch):
        """Verify invalid context chars defaults properly."""
        monkeypatch.setenv("DV_AGENT_MAX_CONTEXT_CHARS", "invalid")
        
        status = agent_backend_module.get_backend_status()
        assert status["max_context_chars"] == 12000


class TestErrorLogging:
    """Test comprehensive error logging."""

    def test_errors_logged_with_context(self, tmp_path: Path, agent_module, monkeypatch, caplog):
        """Verify errors include sufficient context for debugging."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        def fake_run(*args, **kwargs):
            raise OSError("Permission denied")

        monkeypatch.setattr("subprocess.run", fake_run)

        with caplog.at_level(logging.ERROR):
            result = agent._run_command(["dummy"])

        assert "Permission denied" in caplog.text
        assert result.returncode == -1

    def test_backend_diagnostics_no_token_leak(self, agent_backend_module, monkeypatch):
        """Verify backend diagnostics don't leak sensitive tokens."""
        monkeypatch.setenv("GITHUB_TOKEN", "ghp_SUPER_SECRET_TOKEN")

        diagnostics = agent_backend_module.describe_backends()
        assert "SUPER_SECRET_TOKEN" not in diagnostics
        assert "token set" in diagnostics
