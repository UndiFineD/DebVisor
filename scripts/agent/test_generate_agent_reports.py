"""Tests for generate_agent_reports.py."""

from __future__ import annotations
import ast
from pathlib import Path
from typing import Any
import pytest
from agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture
def report_module() -> Any:
    with agent_dir_on_path():
        return load_agent_module("generate_agent_reports.py")


def test_sha256_text(report_module: Any) -> None:
    """Test SHA256 calculation."""
    text = "hello world"
    # echo -n "hello world" | sha256sum
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert report_module._sha256_text(text) == expected


def test_detect_cli_entry(report_module: Any) -> None:
    """Test CLI entry point detection."""
    source_with_main = 'if __name__ == "__main__":\n    main()'
    source_without_main = 'def foo(): pass'
    
    assert report_module._detect_cli_entry(source_with_main) is True
    assert report_module._detect_cli_entry(source_without_main) is False


def test_find_top_level_defs(report_module: Any) -> None:
    """Test finding top-level functions and classes."""
    source = """
def func1(): pass
class Class1: pass
async def func2(): pass
"""
    tree = ast.parse(source)
    funcs, classes = report_module._find_top_level_defs(tree)
    
    assert "func1" in funcs
    assert "async func2" in funcs
    assert "Class1" in classes


def test_is_pytest_test_file(report_module: Any) -> None:
    """Test pytest file detection."""
    assert report_module._is_pytest_test_file(Path("test_foo.py")) is True
    assert report_module._is_pytest_test_file(Path("foo_test.py")) is False
    assert report_module._is_pytest_test_file(Path("test_foo.txt")) is False

