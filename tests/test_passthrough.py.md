# Code Issues Report: tests\test_passthrough.py

Generated: 2025-12-13T15:24:41.176542
Source: tests\test_passthrough.py

## Issues Summary

Total: 42 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 179 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 182 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 183 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 184 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 189 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 192 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 195 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 199 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 200 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 201 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 211 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 220 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 232 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 233 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 238 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 243 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 244 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 249 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 261 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 267 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 283 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 297 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 318 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 331 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 341 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 376 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 383 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 391 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 395 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 415 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 416 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 434 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 445 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 449 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 450 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 451 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 459 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 460 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 461 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 462 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 466 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 467 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status

Items marked below as fixed:

## Fix Proposals

### 42 issues to fix

### Issue at Line 179

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

    def test_mock_devices_structure(self, mock_pci_devices):
        """Verify mock device data structure."""
        assert len(mock_pci_devices) == 4

        gpu = mock_pci_devices[0]
        assert gpu.address == "0000:01:00.0"
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 182

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        assert len(mock_pci_devices) == 4

        gpu = mock_pci_devices[0]
        assert gpu.address == "0000:01:00.0"
        assert gpu.vendor_id == "10de"
        assert gpu.device_class == "0300"

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 183

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        gpu = mock_pci_devices[0]
        assert gpu.address == "0000:01:00.0"
        assert gpu.vendor_id == "10de"
        assert gpu.device_class == "0300"

    def test_iommu_group_isolation(self, mock_iommu_groups):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 184

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        gpu = mock_pci_devices[0]
        assert gpu.address == "0000:01:00.0"
        assert gpu.vendor_id == "10de"
        assert gpu.device_class == "0300"

    def test_iommu_group_isolation(self, mock_iommu_groups):
        """Test IOMMU group isolation detection."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 189

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def test_iommu_group_isolation(self, mock_iommu_groups):
        """Test IOMMU group isolation detection."""
        # Group 1 has 2 devices (not isolated)
        assert not mock_iommu_groups[1].is_isolated

        # Group 2 has 1 device (isolated)
        assert mock_iommu_groups[2].is_isolated
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 192

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        assert not mock_iommu_groups[1].is_isolated

        # Group 2 has 1 device (isolated)
        assert mock_iommu_groups[2].is_isolated

        # Group 3 has 1 device (isolated)
        assert mock_iommu_groups[3].is_isolated
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 195

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        assert mock_iommu_groups[2].is_isolated

        # Group 3 has 1 device (isolated)
        assert mock_iommu_groups[3].is_isolated

    def test_device_count_per_group(self, mock_iommu_groups):
        """Verify correct device count per IOMMU group."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 199

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

    def test_device_count_per_group(self, mock_iommu_groups):
        """Verify correct device count per IOMMU group."""
        assert len(mock_iommu_groups[1].devices) == 2    # GPU + Audio
        assert len(mock_iommu_groups[2].devices) == 1    # USB
        assert len(mock_iommu_groups[3].devices) == 1    # NVMe

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 200

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def test_device_count_per_group(self, mock_iommu_groups):
        """Verify correct device count per IOMMU group."""
        assert len(mock_iommu_groups[1].devices) == 2    # GPU + Audio
        assert len(mock_iommu_groups[2].devices) == 1    # USB
        assert len(mock_iommu_groups[3].devices) == 1    # NVMe

    @pytest.mark.skipif(not HAS_PASSTHROUGH, reason="PassthroughManager not available")
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 201

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        """Verify correct device count per IOMMU group."""
        assert len(mock_iommu_groups[1].devices) == 2    # GPU + Audio
        assert len(mock_iommu_groups[2].devices) == 1    # USB
        assert len(mock_iommu_groups[3].devices) == 1    # NVMe

    @pytest.mark.skipif(not HAS_PASSTHROUGH, reason="PassthroughManager not available")

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 211

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            with patch("glob.glob", return_value=[]):
                devices = passthrough_manager.scan_devices()
                # On non-Linux or mock, returns empty or mock data
                assert isinstance(devices, list)

    @pytest.mark.skipif(not HAS_PASSTHROUGH, reason="PassthroughManager not available")

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 220

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        with patch("os.path.exists", return_value=False):
            devices = passthrough_manager.scan_devices()
            # Should return mock devices
            assert isinstance(devices, list)

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 232

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def test_gaming_profile_classes(self) -> None:
        """Verify gaming profile device classes."""
        gaming_classes = ["0300", "0403"]    # VGA + Audio
        assert "0300" in gaming_classes
        assert "0403" in gaming_classes

    def test_ai_profile_classes(self) -> None:
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 233

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        """Verify gaming profile device classes."""
        gaming_classes = ["0300", "0403"]    # VGA + Audio
        assert "0300" in gaming_classes
        assert "0403" in gaming_classes

    def test_ai_profile_classes(self) -> None:
        """Verify AI/ML profile device classes."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 238

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def test_ai_profile_classes(self) -> None:
        """Verify AI/ML profile device classes."""
        ai_classes = ["0300", "0302"]    # VGA + 3D Controller
        assert "0300" in ai_classes

    def test_filter_devices_by_class(self, mock_pci_devices):
        """Test filtering devices by class code."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 243

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def test_filter_devices_by_class(self, mock_pci_devices):
        """Test filtering devices by class code."""
        vga_devices = [d for d in mock_pci_devices if d.device_class == "0300"]
        assert len(vga_devices) == 1
        assert vga_devices[0].device_name == "NVIDIA GeForce RTX 3070"

    def test_filter_devices_by_vendor(self, mock_pci_devices):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 244

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        """Test filtering devices by class code."""
        vga_devices = [d for d in mock_pci_devices if d.device_class == "0300"]
        assert len(vga_devices) == 1
        assert vga_devices[0].device_name == "NVIDIA GeForce RTX 3070"

    def test_filter_devices_by_vendor(self, mock_pci_devices):
        """Test filtering devices by vendor ID."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 249

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def test_filter_devices_by_vendor(self, mock_pci_devices):
        """Test filtering devices by vendor ID."""
        nvidia_devices = [d for d in mock_pci_devices if d.vendor_id == "10de"]
        assert len(nvidia_devices) == 2    # GPU + Audio

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 261

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def test_device_driver_detection(self, mock_pci_devices):
        """Verify current driver detection."""
        gpu = mock_pci_devices[0]
        assert gpu.driver_in_use == "nvidia"

    def test_vfio_bound_check(self, mock_pci_devices):
        """Test VFIO bound status detection."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 267

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        """Test VFIO bound status detection."""
        for device in mock_pci_devices:
            is_vfio_bound = device.driver_in_use == "vfio-pci"
            assert not is_vfio_bound    # None of our mocks are VFIO bound

    @pytest.mark.skipif(not HAS_PASSTHROUGH, reason="PassthroughManager not available")

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 283

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            # passthrough_manager.bind_to_vfio(device.address)
            result = {"success": True, "message": "Simulated bind"}

            assert result["success"] is True

    @pytest.mark.skipif(not HAS_PASSTHROUGH, reason="PassthroughManager not available")

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 297

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            # Simulate unbind operation
            result = {"success": True, "message": "Simulated unbind"}

            assert result["success"] is True

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 318

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        valid_pattern = r"^[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-9]$"

        for addr in invalid_addresses:
            assert not re.match(valid_pattern, addr, re.IGNORECASE)

    def test_valid_pci_address_format(self) -> None:
        """Test validation of correct PCI address format."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 331

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        valid_pattern = r"^[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-9]$"

        for addr in valid_addresses:
            assert re.match(valid_pattern, addr, re.IGNORECASE)

    def test_device_not_found(self, passthrough_manager, mock_pci_devices):
        """Test handling of non-existent device."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 341

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            (d for d in mock_pci_devices if d.address == non_existent_address), None
        )

        assert device is None

    def test_permission_denied_simulation(self) -> None:
        """Test handling of permission denied errors."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 376

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def test_list_devices_endpoint(self, client):
        """Test /passthrough/api/devices endpoint."""
        response = client.get("/passthrough/api/devices")
        assert response.status_code in [200, 500]    # 500 if manager unavailable

    @pytest.mark.skip(reason="Requires full Flask app setup")

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 383

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
    def test_list_gpus_endpoint(self, client):
        """Test /passthrough/api/gpus endpoint."""
        response = client.get("/passthrough/api/gpus")
        assert response.status_code in [200, 500]

    @pytest.mark.skip(reason="Requires full Flask app setup")

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 391

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        """Test input validation for device binding."""
        # Missing address
        response = client.post("/passthrough/api/bind", json={})
        assert response.status_code == 400

        # Invalid address format
        response = client.post("/passthrough/api/bind", json={"address": "invalid"})
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 395

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        # Invalid address format
        response = client.post("/passthrough/api/bind", json={"address": "invalid"})
        assert response.status_code == 400

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 415

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        filtered = [d for d in large_device_list if d.device_class == "0300"]
        elapsed = time.time() - start

        assert elapsed < 0.1    # Should complete in under 100ms
        assert len(filtered) == 25

    def test_iommu_group_building_performance(self, mock_pci_devices):
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 416

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        elapsed = time.time() - start

        assert elapsed < 0.1    # Should complete in under 100ms
        assert len(filtered) == 25

    def test_iommu_group_building_performance(self, mock_pci_devices):
        """Test IOMMU group building is efficient."""
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 434

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            groups[group_id].append(device)
        elapsed = time.time() - start

        assert elapsed < 0.1    # Should complete in under 100ms

# =============================================================================
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 445

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

    def test_mock_devices_available(self, mock_pci_devices):
        """Verify mock devices are properly configured."""
        assert len(mock_pci_devices) > 0

        # Check device types present
        classes = {d.device_class for d in mock_pci_devices}
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 449

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        # Check device types present
        classes = {d.device_class for d in mock_pci_devices}
        assert "0300" in classes    # VGA
        assert "0c03" in classes    # USB
        assert "0108" in classes    # NVMe

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 450

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        # Check device types present
        classes = {d.device_class for d in mock_pci_devices}
        assert "0300" in classes    # VGA
        assert "0c03" in classes    # USB
        assert "0108" in classes    # NVMe

    def test_mock_mode_returns_valid_structure(
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 451

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        classes = {d.device_class for d in mock_pci_devices}
        assert "0300" in classes    # VGA
        assert "0c03" in classes    # USB
        assert "0108" in classes    # NVMe

    def test_mock_mode_returns_valid_structure(
        self, mock_pci_devices, mock_iommu_groups
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 459

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        """Test mock mode returns valid data structure."""
        # Verify devices have all required fields
        for device in mock_pci_devices:
            assert device.address
            assert device.vendor_id
            assert device.product_id
            assert device.iommu_group >= 0
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 460

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        # Verify devices have all required fields
        for device in mock_pci_devices:
            assert device.address
            assert device.vendor_id
            assert device.product_id
            assert device.iommu_group >= 0

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 461

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        for device in mock_pci_devices:
            assert device.address
            assert device.vendor_id
            assert device.product_id
            assert device.iommu_group >= 0

        # Verify groups have valid structure
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 462

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
            assert device.address
            assert device.vendor_id
            assert device.product_id
            assert device.iommu_group >= 0

        # Verify groups have valid structure
        for group_id, group in mock_iommu_groups.items():
```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 466

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python

        # Verify groups have valid structure
        for group_id, group in mock_iommu_groups.items():
            assert group.id == group_id
            assert len(group.devices) > 0

```python

### Proposal

- Review the issue message above

- Consider the context code

- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)

- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 467

**Tool:**bandit |**Code:**`B101` |**Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

### Context

```python
        # Verify groups have valid structure
        for group_id, group in mock_iommu_groups.items():
            assert group.id == group_id
            assert len(group.devices) > 0

# =============================================================================
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
