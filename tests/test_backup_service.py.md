# Code Issues Report: tests\test_backup_service.py

Generated: 2025-12-13T15:23:23.725169
Source: tests\test_backup_service.py

## Issues Summary

Total: 44 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 173 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 176 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 185 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 186 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 205 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 213 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 229 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 230 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 239 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 243 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 246 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 249 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 259 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 266 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 273 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 277 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 295 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 296 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 309 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 310 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 311 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 318 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 324 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 333 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 334 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 341 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 361 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 383 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 395 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 438 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 439 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 480 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 503 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 525 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 538 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 559 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 560 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 577 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 597 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 605 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 635 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 660 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 683 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 691 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 44 issues to fix

### Issue at Line 173

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
            hashes.append(chunk_hash)

        # First and fourth blocks are identical
        assert hashes[0] == hashes[3]

        # Other blocks are unique
        assert len(set(hashes)) == 3
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 176

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        assert hashes[0] == hashes[3]

        # Other blocks are unique
        assert len(set(hashes)) == 3

    def test_chunk_size_boundaries(self) -> None:
        """Test chunk size boundary detection."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 185

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        max_chunk = 256 * 1024    # 256 KB

        # Verify boundaries are reasonable
        assert min_chunk < avg_chunk < max_chunk
        assert max_chunk <= 1024 * 1024    # Max 1 MB

    def test_rolling_hash_simulation(self, sample_data_blocks):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 186

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        # Verify boundaries are reasonable
        assert min_chunk < avg_chunk < max_chunk
        assert max_chunk <= 1024 * 1024    # Max 1 MB

    def test_rolling_hash_simulation(self, sample_data_blocks):
        """Simulate rolling hash for content-defined boundaries."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 205

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
                )
                fingerprints.append(fp % (2**32))

            assert len(fingerprints) > 0

    def test_empty_data_handling(self) -> None:
        """Test handling of empty data."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 213

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        chunk_hash = hashlib.sha256(empty_data).hexdigest()

        # Empty data has a valid hash
        assert len(chunk_hash) == 64

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 229

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        is_new = in_memory_chunk_store.store(chunk_hash, chunk)

        assert is_new is True
        assert in_memory_chunk_store.total_chunks == 1

    def test_store_duplicate_chunk(self, in_memory_chunk_store, sample_data_blocks):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 230

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        is_new = in_memory_chunk_store.store(chunk_hash, chunk)

        assert is_new is True
        assert in_memory_chunk_store.total_chunks == 1

    def test_store_duplicate_chunk(self, in_memory_chunk_store, sample_data_blocks):
        """Test storing a duplicate chunk."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 239

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        # Store first time
        first = in_memory_chunk_store.store(chunk_hash, chunk)
        assert first is True

        # Store second time (duplicate)
        second = in_memory_chunk_store.store(chunk_hash, chunk)
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 243

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        # Store second time (duplicate)
        second = in_memory_chunk_store.store(chunk_hash, chunk)
        assert second is False

        # Still only one chunk stored
        assert in_memory_chunk_store.total_chunks == 1
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 246

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        assert second is False

        # Still only one chunk stored
        assert in_memory_chunk_store.total_chunks == 1

        # But reference count is 2
        assert in_memory_chunk_store.reference_counts[chunk_hash] == 2
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 249

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        assert in_memory_chunk_store.total_chunks == 1

        # But reference count is 2
        assert in_memory_chunk_store.reference_counts[chunk_hash] == 2

    def test_retrieve_chunk(self, in_memory_chunk_store, sample_data_blocks):
        """Test retrieving a stored chunk."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 259

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        in_memory_chunk_store.store(chunk_hash, chunk)
        retrieved = in_memory_chunk_store.retrieve(chunk_hash)

        assert retrieved == chunk

    def test_retrieve_nonexistent_chunk(self, in_memory_chunk_store):
        """Test retrieving a non-existent chunk."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 266

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        fake_hash = "0" * 64
        result = in_memory_chunk_store.retrieve(fake_hash)

        assert result is None

    def test_chunk_existence_check(self, in_memory_chunk_store, sample_data_blocks):
        """Test chunk existence check."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 273

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        chunk = sample_data_blocks[0]
        chunk_hash = hashlib.sha256(chunk).hexdigest()

        assert in_memory_chunk_store.exists(chunk_hash) is False

        in_memory_chunk_store.store(chunk_hash, chunk)

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 277

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        in_memory_chunk_store.store(chunk_hash, chunk)

        assert in_memory_chunk_store.exists(chunk_hash) is True

    def test_deduplication_ratio_calculation(
        self, in_memory_chunk_store, sample_data_blocks
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 295

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        # We have 4 blocks (total 232 bytes) but only 3 unique ones (179 bytes)
        # Ratio is 232/179 = 1.296...
        assert dedup_ratio > 1.0
        assert round(dedup_ratio, 2) == 1.30

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 296

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        # We have 4 blocks (total 232 bytes) but only 3 unique ones (179 bytes)
        # Ratio is 232/179 = 1.296...
        assert dedup_ratio > 1.0
        assert round(dedup_ratio, 2) == 1.30

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 309

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        """Test snapshot metadata creation."""
        snap = sample_snapshots[0]

        assert snap.snapshot_id == "snap-001"
        assert snap.size_bytes == 10 *1024*1024* 1024
        assert snap.chunk_count == 1000

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 310

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        snap = sample_snapshots[0]

        assert snap.snapshot_id == "snap-001"
        assert snap.size_bytes == 10 *1024*1024* 1024
        assert snap.chunk_count == 1000

    def test_snapshot_filtering_by_source(self, sample_snapshots):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 311

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        assert snap.snapshot_id == "snap-001"
        assert snap.size_bytes == 10 *1024*1024* 1024
        assert snap.chunk_count == 1000

    def test_snapshot_filtering_by_source(self, sample_snapshots):
        """Test filtering snapshots by source path."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 318

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        source = "/var/lib/vm/disk1.qcow2"
        filtered = [s for s in sample_snapshots if s.source_path == source]

        assert len(filtered) == 2

    def test_snapshot_filtering_by_tag(self, sample_snapshots):
        """Test filtering snapshots by tag."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 324

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        """Test filtering snapshots by tag."""
        filtered = [s for s in sample_snapshots if s.tags.get("type") == "daily"]

        assert len(filtered) == 2

    def test_snapshot_sorting_by_date(self, sample_snapshots):
        """Test sorting snapshots by creation date."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 333

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        )

        # Most recent first
        assert sorted_snaps[0].snapshot_id == "snap-003"
        assert sorted_snaps[-1].snapshot_id == "snap-001"

    def test_snapshot_size_summary(self, sample_snapshots):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 334

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        # Most recent first
        assert sorted_snaps[0].snapshot_id == "snap-003"
        assert sorted_snaps[-1].snapshot_id == "snap-001"

    def test_snapshot_size_summary(self, sample_snapshots):
        """Test snapshot size summary calculation."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 341

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        total_size = sum(s.size_bytes for s in sample_snapshots)

        # 10 + 10 + 50 = 70 GB
        assert total_size == 70 *1024*1024* 1024

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 361

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
            :daily_keep
        ]

        assert len(to_keep) <= daily_keep

    def test_retention_by_age(self, retention_policy):
        """Test retention based on snapshot age."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 383

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        # Filter by age (strictly less than, so 7 days = days 0-6 inclusive)
        keep_snaps = [s for s in test_snaps if (now - s.created_at) < max_daily_age]

        assert len(keep_snaps) == 7    # Days 0-6

    def test_grandfather_father_son_policy(self, retention_policy):
        """Test GFS rotation policy."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 395

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
            - retention_policy["yearly"]
        )

        assert total_retention == 26

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 438

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
            chunk_count=len(chunks),
        )

        assert snapshot.chunk_count > 0
        assert in_memory_chunk_store.total_chunks > 0

    def test_incremental_backup_simulation(
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 439

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        )

        assert snapshot.chunk_count > 0
        assert in_memory_chunk_store.total_chunks > 0

    def test_incremental_backup_simulation(
        self, in_memory_chunk_store, temp_backup_dir
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 480

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        _overlap = set(first_chunks) & set(second_chunks)

        # Only new chunks should be stored
        assert in_memory_chunk_store.total_chunks < len(first_chunks) + len(
            second_chunks
        )

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 503

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        # Restore
        restored = in_memory_chunk_store.retrieve(chunk_hash)

        assert restored == original

    def test_restore_ordered_chunks(self, in_memory_chunk_store):
        """Test restoring data from ordered chunk list."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 525

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        restored_chunks = [in_memory_chunk_store.retrieve(h) for h in chunk_hashes]
        restored = b"".join(restored_chunks)

        assert restored == original

    def test_restore_integrity_verification(self, in_memory_chunk_store):
        """Test integrity verification during restore."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 538

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        restored = in_memory_chunk_store.retrieve(chunk_hash)
        restored_hash = hashlib.sha256(restored).hexdigest()

        assert restored_hash == chunk_hash

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 559

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        chunk_file.parent.mkdir(parents=True, exist_ok=True)
        chunk_file.write_bytes(chunk_data)

        assert chunk_file.exists()
        assert chunk_file.read_bytes() == chunk_data

    def test_local_backend_read(self, tmp_path):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 560

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        chunk_file.write_bytes(chunk_data)

        assert chunk_file.exists()
        assert chunk_file.read_bytes() == chunk_data

    def test_local_backend_read(self, tmp_path):
        """Test local filesystem backend read."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 577

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        # Read back
        read_data = chunk_file.read_bytes()

        assert read_data == chunk_data

    @pytest.mark.asyncio
    async def test_s3_backend_mock(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 597

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
            Bucket="backups", Key=f"chunks/{chunk_hash}", Body=chunk_data
        )

        assert "ETag" in result

        # Get
        response = await mock_s3.get_object(
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 605

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        )

        retrieved = await response["Body"].read()
        assert retrieved == b"chunk data"

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 635

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        throughput_mbps = data_size / (1024 * 1024) / elapsed if elapsed > 0 else 0

        # Should handle at least 10 MB/s in-memory
        assert throughput_mbps > 10 or elapsed < 1.0

    def test_dedup_lookup_performance(self, in_memory_chunk_store):
        """Test deduplication lookup performance."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 660

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        elapsed = time.time() - start

        # Should complete 1000 lookups in under 100ms
        assert elapsed < 0.1

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 683

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python
        retrieved_hash = hashlib.sha256(retrieved).hexdigest()

        # Hash mismatch indicates corruption
        assert retrieved_hash != chunk_hash

    def test_missing_chunk_handling(self, in_memory_chunk_store):
        """Test handling of missing chunks."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 691

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised
byte code.

### Context

```python

        result = in_memory_chunk_store.retrieve(fake_hash)

        assert result is None

    def test_storage_full_simulation(self, in_memory_chunk_store):
        """Simulate storage full condition."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

## Implementation Progress

To mark an issue as fixed, add the issue code to the line below with a ✅ emoji:

**Fixed Issues:** (none yet)

---
*Updated: (auto-populated by coding expert)*
