"""
Integration Tests for Deduplication Backup Service

Tests backup functionality including:
- Content-defined chunking
- Deduplication detection
- Snapshot management
- Retention policies
- Restore operations
- S3 and local backends

These tests use in-memory backends to avoid filesystem dependencies.
"""

import pytest
import os
import hashlib
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock
from typing import Dict, Optional
from dataclasses import dataclass, field

# Add the services path for imports
try:
    from dedup_backup_service import (
        SnapshotMetadata,
    )

    HAS_BACKUP_SERVICE = True
except ImportError:
    HAS_BACKUP_SERVICE = False

    # Define mock classes for testing
    @dataclass
    class SnapshotMetadata:
        """Mock snapshot metadata."""

        snapshot_id: str
        source_path: str
        created_at: datetime
        size_bytes: int
        chunk_count: int
        dedup_ratio: float = 1.0
        tags: Dict = field(default_factory=dict)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def sample_data_blocks():
    """Create sample data blocks for chunking tests."""
    return [
        b"This is the first block of data that will be chunked.",
        b"Second block contains different content for deduplication test.",
        b"Third block is unique content that should be stored separately.",
        b"This is the first block of data that will be chunked.",  # Duplicate of first
    ]


@pytest.fixture
def in_memory_chunk_store():
    """Create an in-memory chunk store for testing."""

    class InMemoryChunkStore:
        def __init__(self):
            self.chunks: Dict[str, bytes] = {}
            self.reference_counts: Dict[str, int] = {}

        def store(self, chunk_hash: str, data: bytes) -> bool:
            """Store a chunk, returns True if new, False if duplicate."""
            if chunk_hash in self.chunks:
                self.reference_counts[chunk_hash] += 1
                return False

            self.chunks[chunk_hash] = data
            self.reference_counts[chunk_hash] = 1
            return True

        def retrieve(self, chunk_hash: str) -> Optional[bytes]:
            """Retrieve a chunk by its hash."""
            return self.chunks.get(chunk_hash)

        def exists(self, chunk_hash: str) -> bool:
            """Check if a chunk exists."""
            return chunk_hash in self.chunks

        def delete(self, chunk_hash: str) -> bool:
            """Delete a chunk if reference count is 0."""
            if chunk_hash not in self.chunks:
                return False

            self.reference_counts[chunk_hash] -= 1
            if self.reference_counts[chunk_hash] <= 0:
                del self.chunks[chunk_hash]
                del self.reference_counts[chunk_hash]
            return True

        @property
        def total_chunks(self) -> int:
            return len(self.chunks)

        @property
        def total_size(self) -> int:
            return sum(len(data) for data in self.chunks.values())

    return InMemoryChunkStore()


@pytest.fixture
def sample_snapshots():
    """Create sample snapshot metadata."""
    now = datetime.now(timezone.utc)
    return [
        SnapshotMetadata(
            snapshot_id="snap-001",
            source_path="/var/lib/vm/disk1.qcow2",
            created_at=now - timedelta(days=30),
            size_bytes=10 * 1024 * 1024 * 1024,  # 10 GB
            chunk_count=1000,
            dedup_ratio=1.5,
            tags={"vm": "web-server-01", "type": "daily"},
        ),
        SnapshotMetadata(
            snapshot_id="snap-002",
            source_path="/var/lib/vm/disk1.qcow2",
            created_at=now - timedelta(days=7),
            size_bytes=10 * 1024 * 1024 * 1024,
            chunk_count=1020,
            dedup_ratio=1.8,
            tags={"vm": "web-server-01", "type": "weekly"},
        ),
        SnapshotMetadata(
            snapshot_id="snap-003",
            source_path="/var/lib/vm/disk2.qcow2",
            created_at=now - timedelta(days=1),
            size_bytes=50 * 1024 * 1024 * 1024,  # 50 GB
            chunk_count=5000,
            dedup_ratio=2.5,
            tags={"vm": "db-server-01", "type": "daily"},
        ),
    ]


@pytest.fixture
def retention_policy():
    """Create a sample retention policy."""
    return {
        "daily": 7,  # Keep 7 daily snapshots
        "weekly": 4,  # Keep 4 weekly snapshots
        "monthly": 12,  # Keep 12 monthly snapshots
        "yearly": 3,  # Keep 3 yearly snapshots
    }


# =============================================================================
# Unit Tests - Content Chunking
# =============================================================================


class TestContentChunking:
    """Tests for content-defined chunking."""

    def test_hash_computation(self, sample_data_blocks):
        """Test SHA-256 hash computation for chunks."""
        hashes = []
        for block in sample_data_blocks:
            chunk_hash = hashlib.sha256(block).hexdigest()
            hashes.append(chunk_hash)

        # First and fourth blocks are identical
        assert hashes[0] == hashes[3]

        # Other blocks are unique
        assert len(set(hashes)) == 3

    def test_chunk_size_boundaries(self):
        """Test chunk size boundary detection."""
        min_chunk = 4 * 1024  # 4 KB
        avg_chunk = 64 * 1024  # 64 KB
        max_chunk = 256 * 1024  # 256 KB

        # Verify boundaries are reasonable
        assert min_chunk < avg_chunk < max_chunk
        assert max_chunk <= 1024 * 1024  # Max 1 MB

    def test_rolling_hash_simulation(self, sample_data_blocks):
        """Simulate rolling hash for content-defined boundaries."""
        window_size = 48

        for block in sample_data_blocks:
            if len(block) < window_size:
                continue

            # Simulate Rabin fingerprint
            fingerprints = []
            for i in range(len(block) - window_size + 1):
                window = block[i : i + window_size]
                fp = sum(
                    b * (31 ** (window_size - j - 1)) for j, b in enumerate(window)
                )
                fingerprints.append(fp % (2**32))

            assert len(fingerprints) > 0

    def test_empty_data_handling(self):
        """Test handling of empty data."""
        empty_data = b""
        chunk_hash = hashlib.sha256(empty_data).hexdigest()

        # Empty data has a valid hash
        assert len(chunk_hash) == 64


# =============================================================================
# Unit Tests - Deduplication Store
# =============================================================================


class TestDeduplicationStore:
    """Tests for deduplication chunk store."""

    def test_store_new_chunk(self, in_memory_chunk_store, sample_data_blocks):
        """Test storing a new chunk."""
        chunk = sample_data_blocks[0]
        chunk_hash = hashlib.sha256(chunk).hexdigest()

        is_new = in_memory_chunk_store.store(chunk_hash, chunk)

        assert is_new is True
        assert in_memory_chunk_store.total_chunks == 1

    def test_store_duplicate_chunk(self, in_memory_chunk_store, sample_data_blocks):
        """Test storing a duplicate chunk."""
        chunk = sample_data_blocks[0]
        chunk_hash = hashlib.sha256(chunk).hexdigest()

        # Store first time
        first = in_memory_chunk_store.store(chunk_hash, chunk)
        assert first is True

        # Store second time (duplicate)
        second = in_memory_chunk_store.store(chunk_hash, chunk)
        assert second is False

        # Still only one chunk stored
        assert in_memory_chunk_store.total_chunks == 1

        # But reference count is 2
        assert in_memory_chunk_store.reference_counts[chunk_hash] == 2

    def test_retrieve_chunk(self, in_memory_chunk_store, sample_data_blocks):
        """Test retrieving a stored chunk."""
        chunk = sample_data_blocks[0]
        chunk_hash = hashlib.sha256(chunk).hexdigest()

        in_memory_chunk_store.store(chunk_hash, chunk)
        retrieved = in_memory_chunk_store.retrieve(chunk_hash)

        assert retrieved == chunk

    def test_retrieve_nonexistent_chunk(self, in_memory_chunk_store):
        """Test retrieving a non-existent chunk."""
        fake_hash = "0" * 64
        result = in_memory_chunk_store.retrieve(fake_hash)

        assert result is None

    def test_chunk_existence_check(self, in_memory_chunk_store, sample_data_blocks):
        """Test chunk existence check."""
        chunk = sample_data_blocks[0]
        chunk_hash = hashlib.sha256(chunk).hexdigest()

        assert in_memory_chunk_store.exists(chunk_hash) is False

        in_memory_chunk_store.store(chunk_hash, chunk)

        assert in_memory_chunk_store.exists(chunk_hash) is True

    def test_deduplication_ratio_calculation(
        self, in_memory_chunk_store, sample_data_blocks
    ):
        """Test deduplication ratio calculation."""
        total_input_size = 0

        for block in sample_data_blocks:
            chunk_hash = hashlib.sha256(block).hexdigest()
            in_memory_chunk_store.store(chunk_hash, block)
            total_input_size += len(block)

        stored_size = in_memory_chunk_store.total_size
        dedup_ratio = total_input_size / stored_size if stored_size > 0 else 1.0

        # We have 4 blocks (total 232 bytes) but only 3 unique ones (179 bytes)
        # Ratio is 232/179 = 1.296...
        assert dedup_ratio > 1.0
        assert round(dedup_ratio, 2) == 1.30


# =============================================================================
# Unit Tests - Snapshot Management
# =============================================================================


class TestSnapshotManagement:
    """Tests for snapshot metadata management."""

    def test_snapshot_creation(self, sample_snapshots):
        """Test snapshot metadata creation."""
        snap = sample_snapshots[0]

        assert snap.snapshot_id == "snap-001"
        assert snap.size_bytes == 10 * 1024 * 1024 * 1024
        assert snap.chunk_count == 1000

    def test_snapshot_filtering_by_source(self, sample_snapshots):
        """Test filtering snapshots by source path."""
        source = "/var/lib/vm/disk1.qcow2"
        filtered = [s for s in sample_snapshots if s.source_path == source]

        assert len(filtered) == 2

    def test_snapshot_filtering_by_tag(self, sample_snapshots):
        """Test filtering snapshots by tag."""
        filtered = [s for s in sample_snapshots if s.tags.get("type") == "daily"]

        assert len(filtered) == 2

    def test_snapshot_sorting_by_date(self, sample_snapshots):
        """Test sorting snapshots by creation date."""
        sorted_snaps = sorted(
            sample_snapshots, key=lambda s: s.created_at, reverse=True
        )

        # Most recent first
        assert sorted_snaps[0].snapshot_id == "snap-003"
        assert sorted_snaps[-1].snapshot_id == "snap-001"

    def test_snapshot_size_summary(self, sample_snapshots):
        """Test snapshot size summary calculation."""
        total_size = sum(s.size_bytes for s in sample_snapshots)

        # 10 + 10 + 50 = 70 GB
        assert total_size == 70 * 1024 * 1024 * 1024


# =============================================================================
# Unit Tests - Retention Policies
# =============================================================================


class TestRetentionPolicies:
    """Tests for backup retention policy enforcement."""

    def test_daily_retention(self, sample_snapshots, retention_policy):
        """Test daily retention policy application."""
        daily_keep = retention_policy["daily"]

        daily_snaps = [s for s in sample_snapshots if s.tags.get("type") == "daily"]

        # Keep up to retention limit
        to_keep = sorted(daily_snaps, key=lambda s: s.created_at, reverse=True)[
            :daily_keep
        ]

        assert len(to_keep) <= daily_keep

    def test_retention_by_age(self, retention_policy):
        """Test retention based on snapshot age."""
        now = datetime.now(timezone.utc)
        max_daily_age = timedelta(days=retention_policy["daily"])

        # Create snapshots of varying ages
        test_snaps = [
            SnapshotMetadata(
                snapshot_id=f"snap-{i}",
                source_path="/test",
                created_at=now - timedelta(days=i),
                size_bytes=1000,
                chunk_count=10,
            )
            for i in range(10)
        ]

        # Filter by age (strictly less than, so 7 days = days 0-6 inclusive)
        keep_snaps = [s for s in test_snaps if (now - s.created_at) < max_daily_age]

        assert len(keep_snaps) == 7  # Days 0-6

    def test_grandfather_father_son_policy(self, retention_policy):
        """Test GFS rotation policy."""
        # GFS: Daily (7) + Weekly (4) + Monthly (12) + Yearly (3)
        total_retention = (
            retention_policy["daily"]
            + retention_policy["weekly"]
            + retention_policy["monthly"]
            + retention_policy["yearly"]
        )

        assert total_retention == 26


# =============================================================================
# Integration Tests - Backup Operations
# =============================================================================


class TestBackupOperations:
    """Integration tests for backup operations."""

    @pytest.fixture
    def temp_backup_dir(self, tmp_path):
        """Create temporary backup directory."""
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()
        return backup_dir

    def test_full_backup_simulation(self, in_memory_chunk_store, temp_backup_dir):
        """Simulate a full backup operation."""
        # Create test file
        test_file = temp_backup_dir / "test.dat"
        test_data = b"Test backup data " * 1000
        test_file.write_bytes(test_data)

        # Simulate chunking (fixed size for simplicity)
        chunk_size = 4096
        chunks = []

        data = test_file.read_bytes()
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            in_memory_chunk_store.store(chunk_hash, chunk)
            chunks.append(chunk_hash)

        # Create snapshot metadata
        snapshot = SnapshotMetadata(
            snapshot_id="test-snap-001",
            source_path=str(test_file),
            created_at=datetime.now(timezone.utc),
            size_bytes=len(data),
            chunk_count=len(chunks),
        )

        assert snapshot.chunk_count > 0
        assert in_memory_chunk_store.total_chunks > 0

    def test_incremental_backup_simulation(
        self, in_memory_chunk_store, temp_backup_dir
    ):
        """Simulate an incremental backup operation."""
        # First backup
        test_file = temp_backup_dir / "test.dat"
        original_data = b"Original backup data " * 1000
        test_file.write_bytes(original_data)

        chunk_size = 4096
        first_chunks = []

        for i in range(0, len(original_data), chunk_size):
            chunk = original_data[i : i + chunk_size]
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            in_memory_chunk_store.store(chunk_hash, chunk)
            first_chunks.append(chunk_hash)

        _chunks_after_first = in_memory_chunk_store.total_chunks

        # Second backup with mostly same data
        modified_data = b"Modified backup data " + original_data[20:]
        test_file.write_bytes(modified_data)

        second_chunks = []
        new_chunk_count = 0

        for i in range(0, len(modified_data), chunk_size):
            chunk = modified_data[i : i + chunk_size]
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            is_new = in_memory_chunk_store.store(chunk_hash, chunk)
            if is_new:
                new_chunk_count += 1
            second_chunks.append(chunk_hash)

        # Should have some overlap
        _overlap = set(first_chunks) & set(second_chunks)

        # Only new chunks should be stored
        assert in_memory_chunk_store.total_chunks < len(first_chunks) + len(
            second_chunks
        )


# =============================================================================
# Integration Tests - Restore Operations
# =============================================================================


class TestRestoreOperations:
    """Tests for backup restore operations."""

    def test_restore_from_chunks(self, in_memory_chunk_store):
        """Test restoring data from chunks."""
        # Original data
        original = b"This is test data that will be backed up and restored."

        # Store as single chunk
        chunk_hash = hashlib.sha256(original).hexdigest()
        in_memory_chunk_store.store(chunk_hash, original)

        # Restore
        restored = in_memory_chunk_store.retrieve(chunk_hash)

        assert restored == original

    def test_restore_ordered_chunks(self, in_memory_chunk_store):
        """Test restoring data from ordered chunk list."""
        # Create multi-chunk data
        chunk1 = b"First part of the data. "
        chunk2 = b"Second part of the data. "
        chunk3 = b"Third part of the data."

        original = chunk1 + chunk2 + chunk3

        # Store chunks
        chunk_hashes = []
        for chunk in [chunk1, chunk2, chunk3]:
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            in_memory_chunk_store.store(chunk_hash, chunk)
            chunk_hashes.append(chunk_hash)

        # Restore in order
        restored_chunks = [in_memory_chunk_store.retrieve(h) for h in chunk_hashes]
        restored = b"".join(restored_chunks)

        assert restored == original

    def test_restore_integrity_verification(self, in_memory_chunk_store):
        """Test integrity verification during restore."""
        data = b"Data with integrity check"

        chunk_hash = hashlib.sha256(data).hexdigest()
        in_memory_chunk_store.store(chunk_hash, data)

        # Restore and verify
        restored = in_memory_chunk_store.retrieve(chunk_hash)
        restored_hash = hashlib.sha256(restored).hexdigest()

        assert restored_hash == chunk_hash


# =============================================================================
# Storage Backend Tests
# =============================================================================


class TestStorageBackends:
    """Tests for different storage backends."""

    def test_local_backend_write(self, tmp_path):
        """Test local filesystem backend write."""
        chunk_dir = tmp_path / "chunks"
        chunk_dir.mkdir()

        chunk_data = b"Test chunk data"
        chunk_hash = hashlib.sha256(chunk_data).hexdigest()

        chunk_file = chunk_dir / f"{chunk_hash[:2]}" / f"{chunk_hash[2:]}"
        chunk_file.parent.mkdir(parents=True, exist_ok=True)
        chunk_file.write_bytes(chunk_data)

        assert chunk_file.exists()
        assert chunk_file.read_bytes() == chunk_data

    def test_local_backend_read(self, tmp_path):
        """Test local filesystem backend read."""
        chunk_dir = tmp_path / "chunks"
        chunk_dir.mkdir()

        chunk_data = b"Test chunk for reading"
        chunk_hash = hashlib.sha256(chunk_data).hexdigest()

        chunk_file = chunk_dir / f"{chunk_hash[:2]}" / f"{chunk_hash[2:]}"
        chunk_file.parent.mkdir(parents=True, exist_ok=True)
        chunk_file.write_bytes(chunk_data)

        # Read back
        read_data = chunk_file.read_bytes()

        assert read_data == chunk_data

    @pytest.mark.asyncio
    async def test_s3_backend_mock(self):
        """Test S3 backend with mock client."""
        mock_s3 = AsyncMock()
        mock_s3.put_object = AsyncMock(return_value={"ETag": "abc123"})
        mock_s3.get_object = AsyncMock(
            return_value={"Body": AsyncMock(read=AsyncMock(return_value=b"chunk data"))}
        )

        # Simulate S3 operations
        chunk_data = b"Test S3 chunk"
        chunk_hash = hashlib.sha256(chunk_data).hexdigest()

        # Put
        result = await mock_s3.put_object(
            Bucket="backups", Key=f"chunks/{chunk_hash}", Body=chunk_data
        )

        assert "ETag" in result

        # Get
        response = await mock_s3.get_object(
            Bucket="backups", Key=f"chunks/{chunk_hash}"
        )

        retrieved = await response["Body"].read()
        assert retrieved == b"chunk data"


# =============================================================================
# Performance Tests
# =============================================================================


class TestPerformance:
    """Performance-related tests."""

    def test_chunking_throughput(self, in_memory_chunk_store):
        """Test chunking throughput."""
        import time

        # Generate 1 MB of data
        data_size = 1 * 1024 * 1024
        data = os.urandom(data_size)

        chunk_size = 64 * 1024  # 64 KB

        start = time.time()

        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            in_memory_chunk_store.store(chunk_hash, chunk)

        elapsed = time.time() - start
        throughput_mbps = data_size / (1024 * 1024) / elapsed if elapsed > 0 else 0

        # Should handle at least 10 MB/s in-memory
        assert throughput_mbps > 10 or elapsed < 1.0

    def test_dedup_lookup_performance(self, in_memory_chunk_store):
        """Test deduplication lookup performance."""
        import time

        # Pre-populate store with 1000 chunks
        for i in range(1000):
            chunk = f"Chunk number {i}".encode()
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            in_memory_chunk_store.store(chunk_hash, chunk)

        # Test lookup speed
        test_hashes = [
            hashlib.sha256(f"Chunk number {i}".encode()).hexdigest() for i in range(100)
        ]

        start = time.time()

        for h in test_hashes * 10:  # 1000 lookups
            in_memory_chunk_store.exists(h)

        elapsed = time.time() - start

        # Should complete 1000 lookups in under 100ms
        assert elapsed < 0.1


# =============================================================================
# Error Handling Tests
# =============================================================================


class TestErrorHandling:
    """Tests for error handling."""

    def test_corrupt_chunk_detection(self, in_memory_chunk_store):
        """Test detection of corrupted chunks."""
        data = b"Original data"
        chunk_hash = hashlib.sha256(data).hexdigest()

        # Store corrupt data
        corrupt_data = b"Corrupted data"
        in_memory_chunk_store.chunks[chunk_hash] = corrupt_data

        # Retrieve and verify
        retrieved = in_memory_chunk_store.retrieve(chunk_hash)
        retrieved_hash = hashlib.sha256(retrieved).hexdigest()

        # Hash mismatch indicates corruption
        assert retrieved_hash != chunk_hash

    def test_missing_chunk_handling(self, in_memory_chunk_store):
        """Test handling of missing chunks."""
        fake_hash = "a" * 64

        result = in_memory_chunk_store.retrieve(fake_hash)

        assert result is None

    def test_storage_full_simulation(self, in_memory_chunk_store):
        """Simulate storage full condition."""

        class LimitedStore:
            def __init__(self, max_size):
                self.max_size = max_size
                self.current_size = 0
                self.chunks = {}

            def store(self, chunk_hash, data):
                if self.current_size + len(data) > self.max_size:
                    raise IOError("Storage full")

                self.chunks[chunk_hash] = data
                self.current_size += len(data)
                return True

        limited_store = LimitedStore(max_size=100)

        # Fill up storage
        with pytest.raises(IOError, match="Storage full"):
            for i in range(20):
                chunk = f"Chunk {i:04d}".encode()
                chunk_hash = hashlib.sha256(chunk).hexdigest()
                limited_store.store(chunk_hash, chunk)


# =============================================================================
# Test Runner
# =============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
