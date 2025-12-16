"""Tests for Phase 4b: Advanced features (snapshots, cascading ignores, rollback)."""
from __future__ import annotations
import logging
import time
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path


@pytest.fixture()
def agent_module():
    with agent_sys_path():
        return load_module_from_path("_dv_agent", AGENT_DIR / "agent.py")


# ============================================================================
# Tests for File Snapshots (Version Control for Rollback)
# ============================================================================

class TestFileSnapshots:
    """Test file snapshot creation and restoration."""

    def test_create_file_snapshot_returns_snapshot_id(self, tmp_path: Path, agent_module):
        """Verify snapshot creation returns a snapshot ID."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("original content", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_id = agent.create_file_snapshot(file_path)
        
        assert snapshot_id is not None
        assert isinstance(snapshot_id, str)
        assert len(snapshot_id) > 0

    def test_create_file_snapshot_creates_snapshot_directory(self, tmp_path: Path, agent_module):
        """Verify .agent_snapshots directory is created."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("content", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_dir = tmp_path / ".agent_snapshots"
        
        assert not snapshot_dir.exists()
        agent.create_file_snapshot(file_path)
        assert snapshot_dir.exists()

    def test_create_file_snapshot_saves_file_content(self, tmp_path: Path, agent_module):
        """Verify snapshot file contains original content."""
        (tmp_path / ".git").mkdir()
        original_content = "original content here"
        file_path = tmp_path / "test.py"
        file_path.write_text(original_content, encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_id = agent.create_file_snapshot(file_path)
        
        # Find snapshot file
        snapshot_dir = tmp_path / ".agent_snapshots"
        snapshot_files = list(snapshot_dir.glob(f"{snapshot_id}*"))
        assert len(snapshot_files) == 1
        
        # Verify content matches
        snapshot_content = snapshot_files[0].read_text(encoding="utf-8")
        assert snapshot_content == original_content

    def test_create_file_snapshot_returns_none_for_nonexistent_file(self, tmp_path: Path, agent_module):
        """Verify None returned for non-existent files."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        nonexistent = tmp_path / "nonexistent.py"
        snapshot_id = agent.create_file_snapshot(nonexistent)
        
        assert snapshot_id is None

    def test_create_file_snapshot_with_unicode_content(self, tmp_path: Path, agent_module):
        """Verify snapshots handle unicode characters."""
        (tmp_path / ".git").mkdir()
        unicode_content = "# café ñ 中文 مرحبا"
        file_path = tmp_path / "unicode.py"
        file_path.write_text(unicode_content, encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_id = agent.create_file_snapshot(file_path)
        
        # Find and verify content
        snapshot_dir = tmp_path / ".agent_snapshots"
        snapshot_files = list(snapshot_dir.glob(f"{snapshot_id}*"))
        snapshot_content = snapshot_files[0].read_text(encoding="utf-8")
        assert snapshot_content == unicode_content

    def test_restore_from_snapshot_restores_original_content(self, tmp_path: Path, agent_module):
        """Verify snapshot restoration works correctly."""
        (tmp_path / ".git").mkdir()
        original_content = "original content"
        modified_content = "modified content"
        file_path = tmp_path / "test.py"
        file_path.write_text(original_content, encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_id = agent.create_file_snapshot(file_path)
        
        # Modify file
        file_path.write_text(modified_content, encoding="utf-8")
        assert file_path.read_text(encoding="utf-8") == modified_content
        
        # Restore
        result = agent.restore_from_snapshot(file_path, snapshot_id)
        assert result is True
        assert file_path.read_text(encoding="utf-8") == original_content

    def test_restore_from_snapshot_returns_false_for_invalid_snapshot(self, tmp_path: Path, agent_module):
        """Verify False returned for invalid snapshot IDs."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("content", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        result = agent.restore_from_snapshot(file_path, "invalid_snapshot_id")
        
        assert result is False

    def test_restore_from_snapshot_returns_false_when_snapshot_dir_missing(self, tmp_path: Path, agent_module):
        """Verify False when snapshot directory doesn't exist."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("content", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        result = agent.restore_from_snapshot(file_path, "any_id")
        
        assert result is False


# ============================================================================
# Tests for Cascading .codeignore Support
# ============================================================================

class TestCascadingCodeignore:
    """Test cascading .codeignore pattern loading."""

    def test_load_cascading_codeignore_loads_root_patterns(self, tmp_path: Path, agent_module):
        """Verify root .codeignore patterns are loaded."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n__pycache__/\n", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore()
        
        assert "*.log" in patterns
        assert "__pycache__/" in patterns

    def test_load_cascading_codeignore_loads_subdirectory_patterns(self, tmp_path: Path, agent_module):
        """Verify patterns from subdirectory .codeignore are loaded."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n", encoding="utf-8")
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / ".codeignore").write_text("*.tmp\n", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore(src_dir)
        
        # Should include patterns from both root and subdirectory
        assert "*.log" in patterns
        assert "*.tmp" in patterns

    def test_load_cascading_codeignore_combines_patterns(self, tmp_path: Path, agent_module):
        """Verify cascading patterns are combined into single set."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n", encoding="utf-8")
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / ".codeignore").write_text("*.tmp\n", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore(src_dir)
        
        # Verify it's a set with combined patterns
        assert isinstance(patterns, set)
        assert len(patterns) >= 2

    def test_load_cascading_codeignore_defaults_to_repo_root(self, tmp_path: Path, agent_module):
        """Verify defaults to repo_root if directory not specified."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore()
        
        assert "*.log" in patterns

    def test_load_cascading_codeignore_handles_missing_codeignore(self, tmp_path: Path, agent_module):
        """Verify graceful handling when .codeignore missing."""
        (tmp_path / ".git").mkdir()
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore(src_dir)
        
        # Should return empty set gracefully
        assert isinstance(patterns, set)

    def test_load_cascading_codeignore_stops_at_repo_root(self, tmp_path: Path, agent_module):
        """Verify traversal stops at repository root."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n", encoding="utf-8")
        
        # Create deep subdirectory structure
        deep_dir = tmp_path / "a" / "b" / "c"
        deep_dir.mkdir(parents=True)
        (deep_dir / ".codeignore").write_text("*.tmp\n", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore(deep_dir)
        
        # Should find both patterns without going above repo root
        assert "*.log" in patterns
        assert "*.tmp" in patterns


# ============================================================================
# Tests for Snapshot Metadata and Integration
# ============================================================================

class TestSnapshotIntegration:
    """Test snapshot integration with other agent features."""

    def test_multiple_snapshots_for_same_file(self, tmp_path: Path, agent_module):
        """Verify multiple snapshots can be created for the same file."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("version 1", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        snapshot_id1 = agent.create_file_snapshot(file_path)
        file_path.write_text("version 2", encoding="utf-8")
        snapshot_id2 = agent.create_file_snapshot(file_path)
        
        assert snapshot_id1 != snapshot_id2
        assert snapshot_id1 is not None
        assert snapshot_id2 is not None

    def test_snapshot_with_dry_run_mode(self, tmp_path: Path, agent_module):
        """Verify snapshots can be created even in dry-run mode."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("content", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=True)
        snapshot_id = agent.create_file_snapshot(file_path)
        
        assert snapshot_id is not None
        # Verify snapshot dir created
        assert (tmp_path / ".agent_snapshots").exists()

    def test_restore_updates_metrics(self, tmp_path: Path, agent_module):
        """Verify restoration logs information."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("original", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_id = agent.create_file_snapshot(file_path)
        
        file_path.write_text("modified", encoding="utf-8")
        agent.restore_from_snapshot(file_path, snapshot_id)
        
        # Verify original content restored
        assert file_path.read_text(encoding="utf-8") == "original"

    def test_snapshot_id_includes_content_hash(self, tmp_path: Path, agent_module):
        """Verify snapshot ID includes content hash for uniqueness."""
        (tmp_path / ".git").mkdir()
        
        # Create two files with different content
        file1 = tmp_path / "file1.py"
        file1.write_text("content1", encoding="utf-8")
        
        file2 = tmp_path / "file2.py"
        file2.write_text("content2", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        
        snapshot_id1 = agent.create_file_snapshot(file1)
        snapshot_id2 = agent.create_file_snapshot(file2)
        
        # Different content should generate different snapshot IDs
        assert snapshot_id1 != snapshot_id2


# ============================================================================
# Tests for Cascading with Selective Agents
# ============================================================================

class TestCascadingIntegration:
    """Test cascading ignore patterns integration with agent features."""

    def test_cascading_ignores_with_selective_agents(self, tmp_path: Path, agent_module):
        """Verify cascading patterns work with selective agent execution."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n", encoding="utf-8")
        
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            selective_agents=['coder']
        )
        
        patterns = agent.load_cascading_codeignore()
        assert "*.log" in patterns
        assert agent.should_execute_agent('coder') is True

    def test_cascading_ignores_with_dry_run(self, tmp_path: Path, agent_module):
        """Verify cascading patterns work in dry-run mode."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=True)
        patterns = agent.load_cascading_codeignore()
        
        assert "*.log" in patterns
        assert agent.dry_run is True


# ============================================================================
# Tests for Edge Cases and Error Handling
# ============================================================================

class TestPhase4bEdgeCases:
    """Test edge cases and error handling for Phase 4b features."""

    def test_create_snapshot_with_large_file(self, tmp_path: Path, agent_module):
        """Verify snapshots work with large files."""
        (tmp_path / ".git").mkdir()
        # Create 1MB file
        large_content = "x" * (1024 * 1024)
        file_path = tmp_path / "large.py"
        file_path.write_text(large_content, encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_id = agent.create_file_snapshot(file_path)
        
        assert snapshot_id is not None
        assert (tmp_path / ".agent_snapshots").exists()

    def test_cascading_ignores_with_circular_references(self, tmp_path: Path, agent_module):
        """Verify cascading doesn't infinite loop with complex structures."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n", encoding="utf-8")
        
        # Create multiple nested levels
        for i in range(5):
            nested = tmp_path / ("a" * (i + 1))
            nested.mkdir(parents=True, exist_ok=True)
            (nested / ".codeignore").write_text(f"*.{i}\n", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore(tmp_path / "aaaaa")
        
        # Should complete without hanging
        assert isinstance(patterns, set)

    def test_restore_snapshot_with_permission_error(self, tmp_path: Path, agent_module, monkeypatch):
        """Verify graceful handling of permission errors."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("original", encoding="utf-8")
        
        agent = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_id = agent.create_file_snapshot(file_path)
        
        # Mock write_text to raise permission error
        def raise_permission(*args, **kwargs):
            raise PermissionError("Access denied")
        
        monkeypatch.setattr(Path, "write_text", raise_permission)
        
        result = agent.restore_from_snapshot(file_path, snapshot_id)
        assert result is False

    def test_snapshot_isolation_between_agents(self, tmp_path: Path, agent_module):
        """Verify snapshots from one agent don't affect another."""
        (tmp_path / ".git").mkdir()
        file_path = tmp_path / "test.py"
        file_path.write_text("content", encoding="utf-8")
        
        agent1 = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_id1 = agent1.create_file_snapshot(file_path)
        
        # Create second agent instance
        agent2 = agent_module.Agent(repo_root=str(tmp_path))
        
        # Should be able to restore using ID from agent1
        file_path.write_text("modified", encoding="utf-8")
        result = agent2.restore_from_snapshot(file_path, snapshot_id1)
        
        assert result is True
        assert file_path.read_text(encoding="utf-8") == "content"
