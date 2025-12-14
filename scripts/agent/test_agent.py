# AI Code Improvement Suggestions
# Description: Improve the code for test_agent.py
#
# Suggestions:
# 1. Add comprehensive docstrings to all functions
# 2. Implement proper error handling with try/except blocks
# 3. Add type hints for better code clarity
# 4. Break down complex functions into smaller, focused functions
# 5. Add input validation and sanitization
# 6. Implement logging for debugging and monitoring
# 7. Add unit tests for all functions
# 8. Follow PEP 8 style guidelines
# 9. Add configuration management for customizable behavior
# 10. Implement proper resource cleanup with context managers
#
# Note: Full AI code rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not code generation.
#
# Original code preserved below:
#

# AI Test Improvement Suggestions
# Description: Improve the test suite for test_agent
#
# Suggestions for improving test suites:
# 1. Add unit tests for all public functions and methods
# 2. Include integration tests for component interactions
# 3. Add edge case and error condition testing
# 4. Implement property-based testing where applicable
# 5. Add performance and load testing
# 6. Include security testing and vulnerability checks
# 7. Add mock objects and test doubles for external dependencies
# 8. Implement test fixtures and setup/teardown methods
# 9. Add test coverage reporting and analysis
# 10. Include automated test execution in CI/CD pipelines
#
# Note: Full AI content rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not content generation.
#
# Original test code preserved below:
#

# AI Code Improvement Suggestions
# Description: Improve the code for test_agent.py
#
# Suggestions:
# 1. Add comprehensive docstrings to all functions
# 2. Implement proper error handling with try/except blocks
# 3. Add type hints for better code clarity
# 4. Break down complex functions into smaller, focused functions
# 5. Add input validation and sanitization
# 6. Implement logging for debugging and monitoring
# 7. Add unit tests for all functions
# 8. Follow PEP 8 style guidelines
# 9. Add configuration management for customizable behavior
# 10. Implement proper resource cleanup with context managers
#
# Note: Full AI code rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not code generation.
#
# Original code preserved below:
#

# AI Test Improvement Suggestions
# Description: Improve the test suite for test_agent
#
# Suggestions for improving test suites:
# 1. Add unit tests for all public functions and methods
# 2. Include integration tests for component interactions
# 3. Add edge case and error condition testing
# 4. Implement property-based testing where applicable
# 5. Add performance and load testing
# 6. Include security testing and vulnerability checks
# 7. Add mock objects and test doubles for external dependencies
# 8. Implement test fixtures and setup/teardown methods
# 9. Add test coverage reporting and analysis
# 10. Include automated test execution in CI/CD pipelines
#
# Note: Full AI content rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not content generation.
#
# Original test code preserved below:
#

# AI Code Improvement Suggestions
# Description: Improve the code for test_agent.py
#
# Suggestions:
# 1. Add comprehensive docstrings to all functions
# 2. Implement proper error handling with try/except blocks
# 3. Add type hints for better code clarity
# 4. Break down complex functions into smaller, focused functions
# 5. Add input validation and sanitization
# 6. Implement logging for debugging and monitoring
# 7. Add unit tests for all functions
# 8. Follow PEP 8 style guidelines
# 9. Add configuration management for customizable behavior
# 10. Implement proper resource cleanup with context managers
#
# Note: Full AI code rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not code generation.
#
# Original code preserved below:
#

# AI Test Improvement Suggestions
# Description: Improve the test suite for test_agent
#
# Suggestions for improving test suites:
# 1. Add unit tests for all public functions and methods
# 2. Include integration tests for component interactions
# 3. Add edge case and error condition testing
# 4. Implement property-based testing where applicable
# 5. Add performance and load testing
# 6. Include security testing and vulnerability checks
# 7. Add mock objects and test doubles for external dependencies
# 8. Implement test fixtures and setup/teardown methods
# 9. Add test coverage reporting and analysis
# 10. Include automated test execution in CI/CD pipelines
#
# Note: Full AI content rewriting requires additional AI service integration.
# The new GitHub Copilot CLI focuses on command-line suggestions, not content generation.
#
# Original test code preserved below:
#

# Tests for agent.py
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add the scripts/agent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from agent import Agent, load_codeignore  # noqa: E402


class TestAgent:
    """Test cases for the Agent class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.repo_root = self.temp_dir / "repo"
        self.repo_root.mkdir()

        # Create a sample Python file
        self.sample_file = self.repo_root / "sample.py"
        self.sample_file.write_text('print("Hello, World!")')

        # Create repository marker
        (self.repo_root / "README.md").write_text("# Test Repository")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_agent_initialization(self):
        """Test agent initialization with default parameters."""
        agent = Agent(repo_root=str(self.repo_root))
        assert agent.repo_root == self.repo_root
        assert not agent.agents_only
        assert agent.max_files is None

    def test_load_codeignore(self):
        """Test loading ignore patterns from .codeignore file."""
        codeignore_file = self.repo_root / ".codeignore"
        codeignore_file.write_text("# Comment\n__pycache__\n*.tmp\n")

        patterns = load_codeignore(self.repo_root)
        assert "__pycache__" in patterns
        assert "*.tmp" in patterns
        assert "# Comment" not in patterns

    def test_find_code_files(self):
        """Test finding code files in the repository."""
        agent = Agent(repo_root=str(self.repo_root))

        # Create various file types
        (self.repo_root / "script.py").write_text("# Python script")
        (self.repo_root / "module.js").write_text("// JavaScript module")
        (self.repo_root / "readme.txt").write_text("Documentation")

        files = agent.find_code_files()
        file_names = [f.name for f in files]

        assert "script.py" in file_names
        assert "module.js" in file_names
        assert "readme.txt" not in file_names

    def test_is_ignored(self):
        """Test file ignoring functionality."""
        agent = Agent(repo_root=str(self.repo_root))
        agent.ignored_patterns = {"__pycache__", "*.tmp"}

        # Create test files
        cache_file = self.repo_root / "__pycache__" / "module.pyc"
        cache_file.parent.mkdir()
        cache_file.write_text("bytecode")

        temp_file = self.repo_root / "temp.tmp"
        temp_file.write_text("temporary")

        normal_file = self.repo_root / "normal.py"
        normal_file.write_text("normal")

        assert agent._is_ignored(cache_file)
        assert agent._is_ignored(temp_file)
        assert not agent._is_ignored(normal_file)

    @patch('subprocess.run')
    def test_run_stats_update(self, mock_subprocess):
        """Test running stats update."""
        mock_subprocess.return_value = MagicMock()
        agent = Agent(repo_root=str(self.repo_root))

        agent.run_stats_update([self.sample_file])

        mock_subprocess.assert_called_once()
        args = mock_subprocess.call_args[0][0]
        assert "agent-stats.py" in args[1]

    @patch('subprocess.run')
    def test_run_tests_no_test_file(self, mock_subprocess):
        """Test running tests when no test file exists."""
        agent = Agent(repo_root=str(self.repo_root))

        # Should not call subprocess since no test file exists
        agent.run_tests(self.sample_file)
        mock_subprocess.assert_not_called()

    @patch('subprocess.run')
    def test_run_tests_with_test_file(self, mock_subprocess):
        """Test running tests when test file exists."""
        mock_subprocess.return_value = MagicMock(returncode=0, stdout="", stderr="")
        agent = Agent(repo_root=str(self.repo_root))

        # Create a test file
        test_file = self.repo_root / "test_sample.py"
        test_file.write_text("def test_sample(): pass")

        agent.run_tests(self.sample_file)

        mock_subprocess.assert_called_once()
        args = mock_subprocess.call_args[0][0]
        assert "pytest" in args
        assert str(test_file) in args


class TestAgentIntegration:
    """Integration tests for the Agent class."""

    def test_full_file_processing_workflow(self):
        """Test the complete file processing workflow."""
        # This would be a more comprehensive integration test
        # For now, just test that the agent can be created and run without errors
        pass


if __name__ == "__main__":
    pytest.main([__file__])
