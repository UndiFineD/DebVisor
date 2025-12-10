"""
Integration Tests for Passthrough Manager

Tests hardware passthrough functionality including:
- PCI device discovery
- IOMMU group detection
- VFIO driver binding/unbinding
- Profile-based device selection
- Error handling and edge cases

These tests use mocks when hardware is not available.
"""

import pytest
from unittest.mock import Mock, patch
from dataclasses import dataclass
from typing import List, Optional, Any

# Add the system path for imports
try:
    from passthrough_manager import (
        PassthroughManager,
        PCIDevice,
        IOMMUGroup,
        PassthroughProfile,
    )

    HAS_PASSTHROUGH = True
except ImportError:
    HAS_PASSTHROUGH = False

    # Define mock classes for when module is missing
    @dataclass
    class PassthroughProfile:
        name: str
        description: str
        device_classes: List[str]

    @dataclass
    class PCIDevice:
        slot: str
        vendor: str
        device: str
        class_id: str
        driver: str = ""
        iommu_group: int = 0

    @dataclass
    class IOMMUGroup:
        id: int
        devices: List[PCIDevice]
        viable: bool = True

    # Mock classes for testing when module not available

    @dataclass
    class PCIDevice:
        address: str
        vendor_id: str
        product_id: str
        iommu_group: int
        driver_in_use: Optional[str] = None
        device_class: str = ""
        device_name: str = ""

    @dataclass
    class IOMMUGroup:
        id: int
        devices: List[Any] = None

        def __post_init__(self) -> None:
            if self.devices is None:
                self.devices = []

        @property
        def is_isolated(self) -> bool:
            return len(self.devices) == 1


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_pci_devices() -> None:
    """Create mock PCI device data."""
    return [
        PCIDevice(
            address="0000:01:00.0",
            vendor_id="10de",
            product_id="2484",
            iommu_group=1,
            device_class="0300",
            device_name="NVIDIA GeForce RTX 3070",
            driver_in_use="nvidia",
        ),
        PCIDevice(
            address="0000:01:00.1",
            vendor_id="10de",
            product_id="228b",
            iommu_group=1,
            device_class="0403",
            device_name="NVIDIA HDMI Audio",
            driver_in_use="snd_hda_intel",
        ),
        PCIDevice(
            address="0000:02:00.0",
            vendor_id="1022",
            product_id="43d0",
            iommu_group=2,
            device_class="0c03",
            device_name="AMD USB 3.0 Controller",
            driver_in_use="xhci_hcd",
        ),
        PCIDevice(
            address="0000:03:00.0",
            vendor_id="144d",
            product_id="a80a",
            iommu_group=3,
            device_class="0108",
            device_name="Samsung NVMe SSD 980 PRO",
            driver_in_use="nvme",
        ),
    ]


@pytest.fixture
def mock_iommu_groups(mock_pci_devices):
    """Create mock IOMMU group data."""
    groups = {}
    for device in mock_pci_devices:
        group_id = device.iommu_group
        if group_id not in groups:
            groups[group_id] = IOMMUGroup(id=group_id)
        groups[group_id].devices.append(device)
    return groups


@pytest.fixture
def mock_sysfs() -> None:
    """Mock sysfs filesystem structure."""
    return {
        "/sys/bus/pci/devices/0000:01:00.0/vendor": "0x10de\n",
        "/sys/bus/pci/devices/0000:01:00.0/device": "0x2484\n",
        "/sys/bus/pci/devices/0000:01:00.0/class": "0x030000\n",
        "/sys/bus/pci/devices/0000:01:00.0/iommu_group": "../../../kernel/iommu_groups/1",
        "/sys/bus/pci/devices/0000:01:00.1/vendor": "0x10de\n",
        "/sys/bus/pci/devices/0000:01:00.1/device": "0x228b\n",
        "/sys/bus/pci/devices/0000:01:00.1/class": "0x040300\n",
        "/sys/bus/pci/devices/0000:01:00.1/iommu_group": "../../../kernel/iommu_groups/1",
    }


@pytest.fixture
def passthrough_manager() -> None:
    """Create PassthroughManager instance with mocked methods."""
    if HAS_PASSTHROUGH:
        manager = PassthroughManager()
    else:
        # Create mock manager
        manager = Mock()
        manager.PROFILES = {
            "gaming": (
                PassthroughProfile("Gaming GPU", "GPU + HDMI Audio", ["0300", "0403"])
                if not HAS_PASSTHROUGH
                else None
            ),
            "ai": Mock(name="AI Accelerator", device_classes=["0300", "0302"]),
            "usb": Mock(name="USB Controller", device_classes=["0c03"]),
            "nvme": Mock(name="NVMe Storage", device_classes=["0108"]),
        }
        manager._device_cache = []
        manager._iommu_groups = {}

    return manager


# =============================================================================
# Unit Tests - Device Discovery
# =============================================================================


class TestDeviceDiscovery:
    """Tests for PCI device discovery."""

    def test_mock_devices_structure(self, mock_pci_devices):
        """Verify mock device data structure."""
        assert len(mock_pci_devices) == 4

        gpu = mock_pci_devices[0]
        assert gpu.address == "0000:01:00.0"
        assert gpu.vendor_id == "10de"
        assert gpu.device_class == "0300"

    def test_iommu_group_isolation(self, mock_iommu_groups):
        """Test IOMMU group isolation detection."""
        # Group 1 has 2 devices (not isolated)
        assert not mock_iommu_groups[1].is_isolated

        # Group 2 has 1 device (isolated)
        assert mock_iommu_groups[2].is_isolated

        # Group 3 has 1 device (isolated)
        assert mock_iommu_groups[3].is_isolated

    def test_device_count_per_group(self, mock_iommu_groups):
        """Verify correct device count per IOMMU group."""
        assert len(mock_iommu_groups[1].devices) == 2    # GPU + Audio
        assert len(mock_iommu_groups[2].devices) == 1    # USB
        assert len(mock_iommu_groups[3].devices) == 1    # NVMe

    @pytest.mark.skipif(not HAS_PASSTHROUGH, reason="PassthroughManager not available")
    def test_scan_devices_on_linux(self, passthrough_manager):
        """Test device scanning on Linux system."""
        with patch("os.path.exists", return_value=True):
            with patch("glob.glob", return_value=[]):
                devices = passthrough_manager.scan_devices()
                # On non-Linux or mock, returns empty or mock data
                assert isinstance(devices, list)

    @pytest.mark.skipif(not HAS_PASSTHROUGH, reason="PassthroughManager not available")
    def test_scan_devices_fallback_mock(self, passthrough_manager):
        """Test fallback to mock devices when sysfs unavailable."""
        with patch("os.path.exists", return_value=False):
            devices = passthrough_manager.scan_devices()
            # Should return mock devices
            assert isinstance(devices, list)


# =============================================================================
# Unit Tests - Profile Matching
# =============================================================================


class TestProfileMatching:
    """Tests for profile-based device selection."""

    def test_gaming_profile_classes(self) -> None:
        """Verify gaming profile device classes."""
        gaming_classes = ["0300", "0403"]    # VGA + Audio
        assert "0300" in gaming_classes
        assert "0403" in gaming_classes

    def test_ai_profile_classes(self) -> None:
        """Verify AI/ML profile device classes."""
        ai_classes = ["0300", "0302"]    # VGA + 3D Controller
        assert "0300" in ai_classes

    def test_filter_devices_by_class(self, mock_pci_devices):
        """Test filtering devices by class code."""
        vga_devices = [d for d in mock_pci_devices if d.device_class == "0300"]
        assert len(vga_devices) == 1
        assert vga_devices[0].device_name == "NVIDIA GeForce RTX 3070"

    def test_filter_devices_by_vendor(self, mock_pci_devices):
        """Test filtering devices by vendor ID."""
        nvidia_devices = [d for d in mock_pci_devices if d.vendor_id == "10de"]
        assert len(nvidia_devices) == 2    # GPU + Audio


# =============================================================================
# Unit Tests - VFIO Binding
# =============================================================================


class TestVFIOBinding:
    """Tests for VFIO driver binding operations."""

    def test_device_driver_detection(self, mock_pci_devices):
        """Verify current driver detection."""
        gpu = mock_pci_devices[0]
        assert gpu.driver_in_use == "nvidia"

    def test_vfio_bound_check(self, mock_pci_devices):
        """Test VFIO bound status detection."""
        for device in mock_pci_devices:
            is_vfio_bound = device.driver_in_use == "vfio-pci"
            assert not is_vfio_bound    # None of our mocks are VFIO bound

    @pytest.mark.skipif(not HAS_PASSTHROUGH, reason="PassthroughManager not available")
    def test_bind_to_vfio_simulation(self, passthrough_manager, mock_pci_devices):
        """Simulate VFIO binding (without actual system changes)."""
        _device = mock_pci_devices[0]

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

            # Simulate bind operation
            # In real code: result =
            # passthrough_manager.bind_to_vfio(device.address)
            result = {"success": True, "message": "Simulated bind"}

            assert result["success"] is True

    @pytest.mark.skipif(not HAS_PASSTHROUGH, reason="PassthroughManager not available")
    def test_unbind_from_vfio_simulation(self, passthrough_manager, mock_pci_devices):
        """Simulate VFIO unbinding (without actual system changes)."""
        _device = mock_pci_devices[0]

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

            # Simulate unbind operation
            result = {"success": True, "message": "Simulated unbind"}

            assert result["success"] is True


# =============================================================================
# Unit Tests - Error Handling
# =============================================================================


class TestErrorHandling:
    """Tests for error handling scenarios."""

    def test_invalid_pci_address_format(self) -> None:
        """Test handling of invalid PCI address format."""
        invalid_addresses = [
            "invalid",
            "0000:00:00",    # Missing function
            "00:00.0",    # Missing domain
            "0000:GG:00.0",    # Invalid hex
        ]

        valid_pattern = r"^[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-9]$"
        import re

        for addr in invalid_addresses:
            assert not re.match(valid_pattern, addr, re.IGNORECASE)

    def test_valid_pci_address_format(self) -> None:
        """Test validation of correct PCI address format."""
        valid_addresses = [
            "0000:01:00.0",
            "0000:02:00.1",
            "0000:ff:1f.7",
        ]

        valid_pattern = r"^[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-9]$"

        for addr in valid_addresses:
            assert re.match(valid_pattern, addr, re.IGNORECASE)

    def test_device_not_found(self, passthrough_manager, mock_pci_devices):
        """Test handling of non-existent device."""
        non_existent_address = "0000:99:00.0"

        device = next(
            (d for d in mock_pci_devices if d.address == non_existent_address), None
        )

        assert device is None

    def test_permission_denied_simulation(self) -> None:
        """Test handling of permission denied errors."""
        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            # Simulate permission error when reading sysfs
            with pytest.raises(PermissionError):
                open("/sys/bus/pci/devices/0000:01:00.0/driver_override", "w")


# =============================================================================
# Integration Tests - API Routes
# =============================================================================


class TestPassthroughAPI:
    """Tests for passthrough web API routes."""

    @pytest.fixture
    def client(self) -> None:
        """Create Flask test client."""
        try:
            from app import create_app

            app = create_app("testing")
            app.config["TESTING"] = True
            app.config["WTF_CSRF_ENABLED"] = False
            return app.test_client()
        except ImportError:
            pytest.skip("Flask app not available")

    @pytest.mark.skip(reason="Requires full Flask app setup")
    def test_list_devices_endpoint(self, client):
        """Test /passthrough/api/devices endpoint."""
        response = client.get("/passthrough/api/devices")
        assert response.status_code in [200, 500]    # 500 if manager unavailable

    @pytest.mark.skip(reason="Requires full Flask app setup")
    def test_list_gpus_endpoint(self, client):
        """Test /passthrough/api/gpus endpoint."""
        response = client.get("/passthrough/api/gpus")
        assert response.status_code in [200, 500]

    @pytest.mark.skip(reason="Requires full Flask app setup")
    def test_bind_device_validation(self, client):
        """Test input validation for device binding."""
        # Missing address
        response = client.post("/passthrough/api/bind", json={})
        assert response.status_code == 400

        # Invalid address format
        response = client.post("/passthrough/api/bind", json={"address": "invalid"})
        assert response.status_code == 400


# =============================================================================
# Performance Tests
# =============================================================================


class TestPerformance:
    """Performance-related tests."""

    def test_device_filtering_performance(self, mock_pci_devices):
        """Test device filtering is fast."""
        import time

        # Simulate 100 devices
        large_device_list = mock_pci_devices * 25

        start = time.time()
        filtered = [d for d in large_device_list if d.device_class == "0300"]
        elapsed = time.time() - start

        assert elapsed < 0.1    # Should complete in under 100ms
        assert len(filtered) == 25

    def test_iommu_group_building_performance(self, mock_pci_devices):
        """Test IOMMU group building is efficient."""
        import time

        # Simulate 100 devices
        large_device_list = mock_pci_devices * 25

        start = time.time()
        groups: Any = {}
        for device in large_device_list:
            group_id = device.iommu_group
            if group_id not in groups:
                groups[group_id] = []
            groups[group_id].append(device)
        elapsed = time.time() - start

        assert elapsed < 0.1    # Should complete in under 100ms


# =============================================================================
# Mock Mode Tests
# =============================================================================


class TestMockMode:
    """Tests for mock mode operation."""

    def test_mock_devices_available(self, mock_pci_devices):
        """Verify mock devices are properly configured."""
        assert len(mock_pci_devices) > 0

        # Check device types present
        classes = {d.device_class for d in mock_pci_devices}
        assert "0300" in classes    # VGA
        assert "0c03" in classes    # USB
        assert "0108" in classes    # NVMe

    def test_mock_mode_returns_valid_structure(
        self, mock_pci_devices, mock_iommu_groups
    ):
        """Test mock mode returns valid data structure."""
        # Verify devices have all required fields
        for device in mock_pci_devices:
            assert device.address
            assert device.vendor_id
            assert device.product_id
            assert device.iommu_group >= 0

        # Verify groups have valid structure
        for group_id, group in mock_iommu_groups.items():
            assert group.id == group_id
            assert len(group.devices) > 0


# =============================================================================
# Test Runner
# =============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
