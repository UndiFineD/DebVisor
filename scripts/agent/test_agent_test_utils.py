"""Tests for agent_test_utils.py."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest
from agent_test_utils import agent_dir_on_path, load_agent_module, AGENT_DIR


def test_agent_dir_on_path_modifies_sys_path() -> None:
    """Test that agent_dir_on_path adds AGENT_DIR to sys.path."""
    original_path = list(sys.path)
    with agent_dir_on_path():
        assert str(AGENT_DIR) in sys.path
        assert sys.path[0] == str(AGENT_DIR)
    
    # Should be restored
    assert sys.path == original_path


def test_load_agent_module_loads_valid_module() -> None:
    """Test loading a valid agent module."""
    # We can load this test file itself or another known file
    # But load_agent_module expects files in AGENT_DIR.
    # Let's try loading 'agent_test_utils.py' itself since it's in AGENT_DIR
    with agent_dir_on_path():
        mod = load_agent_module("agent_test_utils.py")
        assert mod.__name__ == "_dv_legacy_agent_test_utils"
        assert hasattr(mod, "agent_dir_on_path")


def test_load_agent_module_raises_on_missing_file() -> None:
    """Test that loading a missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_agent_module("non_existent_file.py")

