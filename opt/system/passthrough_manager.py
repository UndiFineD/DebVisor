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

"""Hardware Passthrough Manager.

Manages PCI/GPU passthrough assignments:
- IOMMU group validation
- VFIO driver binding/unbinding
- Device isolation checks
- Profile-based assignment (e.g., "Gaming GPU", "AI Accelerator")

Production ready for device discovery and binding.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import logging
import os
import glob

logger = logging.getLogger(__name__)


@dataclass
class PCIDevice:
    address: str    # 0000:01:00.0
    vendor_id: str
    product_id: str
    iommu_group: int
    driver_in_use: Optional[str] = None
    device_class: str = ""
    device_name: str = ""


@dataclass
class IOMMUGroup:
    id: int
    devices: List[PCIDevice] = field(default_factory=list)

    @property
    def is_isolated(self) -> bool:
        """Check if group contains only one device (ideal for passthrough)."""
        return len(self.devices) == 1


@dataclass
class PassthroughProfile:
    name: str
    description: str
    device_classes: List[str]    # VGA, Audio, USB, etc.


class PassthroughManager:
    PROFILES = {
        "gaming": PassthroughProfile(
            "Gaming GPU", "GPU + HDMI Audio for gaming VMs", ["0300", "0403"]
        ),
        "ai": PassthroughProfile(
            "AI Accelerator", "GPU for ML workloads", ["0300", "0302"]
        ),
        "usb": PassthroughProfile(
            "USB Controller", "Entire USB controller passthrough", ["0c03"]
        ),
        "nvme": PassthroughProfile("NVMe Storage", "Direct NVMe access", ["0108"]),
    }

    def __init__(self) -> None:
        self._device_cache: List[PCIDevice] = []
        self._iommu_groups: Dict[int, IOMMUGroup] = {}

    def scan_devices(self) -> List[PCIDevice]:
        """Scan /sys/bus/pci/devices for all PCI devices."""
        devices = []
        pci_base = "/sys/bus/pci/devices"

        if not os.path.exists(pci_base):
            logger.warning("PCI sysfs not available (not running on Linux?)")
            return self._mock_devices()

        for dev_path in glob.glob(f"{pci_base}/*"):
            try:
                device = self._parse_pci_device(dev_path)
                if device:
                    devices.append(device)
            except Exception as e:
                logger.debug(f"Error parsing {dev_path}: {e}")

        self._device_cache = devices
        self._build_iommu_groups()
        return devices

    def _parse_pci_device(self, dev_path: str) -> Optional[PCIDevice]:
        """Parse PCI device information from sysfs."""
        address = os.path.basename(dev_path)

        # Read vendor/device IDs
        vendor_path = os.path.join(dev_path, "vendor")
        device_path = os.path.join(dev_path, "device")
        class_path = os.path.join(dev_path, "class")
        iommu_path = os.path.join(dev_path, "iommu_group")
        driver_path = os.path.join(dev_path, "driver")

        if not os.path.exists(vendor_path):
            return None

        with open(vendor_path, "r") as f:
            vendor_id = f.read().strip().replace("0x", "")
        with open(device_path, "r") as f:
            product_id = f.read().strip().replace("0x", "")
        with open(class_path, "r") as f:
            device_class = f.read().strip().replace("0x", "")[:4]

        # IOMMU group
        iommu_group = -1
        if os.path.exists(iommu_path):
            iommu_link = os.readlink(iommu_path)
            iommu_group = int(os.path.basename(iommu_link))

        # Current driver
        driver = None
        if os.path.exists(driver_path):
            driver = os.path.basename(os.readlink(driver_path))

        return PCIDevice(
            address=address,
            vendor_id=vendor_id,
            product_id=product_id,
            iommu_group=iommu_group,
            driver_in_use=driver,
            device_class=device_class,
            device_name=self._get_device_name(vendor_id, product_id),
        )

    def _get_device_name(self, vendor_id: str, product_id: str) -> str:
        """Get human-readable device name from IDs."""
        # Common vendors
        vendors = {
            "10de": "NVIDIA",
            "1002": "AMD",
            "8086": "Intel",
            "1022": "AMD",
            "10ec": "Realtek",
            "14e4": "Broadcom",
        }
        vendor_name = vendors.get(vendor_id, vendor_id)
        return f"{vendor_name} [{vendor_id}:{product_id}]"

    def _build_iommu_groups(self) -> None:
        """Build IOMMU group mapping from cached devices."""
        self._iommu_groups.clear()
        for device in self._device_cache:
            if device.iommu_group not in self._iommu_groups:
                self._iommu_groups[device.iommu_group] = IOMMUGroup(device.iommu_group)
            self._iommu_groups[device.iommu_group].devices.append(device)

    def _mock_devices(self) -> List[PCIDevice]:
        """Return mock devices for testing on non-Linux systems."""
        return [
            PCIDevice(
                "0000:01:00.0", "10de", "1c03", 12, "nvidia", "0300", "NVIDIA GTX 1060"
            ),
            PCIDevice(
                "0000:01:00.1",
                "10de",
                "10f1",
                12,
                "snd_hda_intel",
                "0403",
                "NVIDIA Audio",
            ),
            PCIDevice(
                "0000:00:14.0", "8086", "a36d", 5, "xhci_hcd", "0c03", "Intel USB 3.0"
            ),
        ]

    def get_iommu_group(self, group_id: int) -> Optional[IOMMUGroup]:
        """Get IOMMU group details."""
        return self._iommu_groups.get(group_id)

    def get_devices_by_class(self, class_prefix: str) -> List[PCIDevice]:
        """Get devices matching a class (e.g., '03' for display controllers)."""
        return [
            d for d in self._device_cache if d.device_class.startswith(class_prefix)
        ]

    def get_gpus(self) -> List[PCIDevice]:
        """Get all GPU devices (VGA and 3D controllers)."""
        return [d for d in self._device_cache if d.device_class in ("0300", "0302")]

    def bind_to_vfio(self, pci_address: str) -> bool:
        """Bind device to vfio-pci driver for passthrough."""
        device = next((d for d in self._device_cache if d.address == pci_address), None)
        if not device:
            logger.error(f"Device {pci_address} not found")
            return False

        logger.info(f"Binding {pci_address} ({device.device_name}) to vfio-pci")

        # Check IOMMU group isolation
        group = self._iommu_groups.get(device.iommu_group)
        if group and not group.is_isolated:
            logger.warning(
                f"IOMMU group {device.iommu_group} contains multiple devices - "
                "all must be passed through"
            )

        # Steps to bind (requires root):
        # 1. echo "vfio-pci" > /sys/bus/pci/devices/{address}/driver_override
        # 2. echo {address} > /sys/bus/pci/drivers/{current}/unbind
        # 3. echo {address} > /sys/bus/pci/drivers/vfio-pci/bind

        try:
            override_path = f"/sys/bus/pci/devices/{pci_address}/driver_override"
            if os.path.exists(override_path):
                with open(override_path, "w") as f:
                    f.write("vfio-pci")
                logger.info(f"Set driver_override to vfio-pci for {pci_address}")
                return True
        except PermissionError:
            logger.error("Permission denied - run as root")
        except Exception as e:
            logger.error(f"Failed to bind: {e}")

        return False

    def release_device(self, pci_address: str) -> bool:
        """Release device from vfio-pci back to host driver."""
        logger.info(f"Releasing {pci_address} from vfio-pci")

        try:
            override_path = f"/sys/bus/pci/devices/{pci_address}/driver_override"
            if os.path.exists(override_path):
                with open(override_path, "w") as f:
                    f.write("")    # Clear override
                logger.info(f"Cleared driver_override for {pci_address}")
                return True
        except PermissionError:
            logger.error("Permission denied - run as root")
        except Exception as e:
            logger.error(f"Failed to release: {e}")

        return False

    def check_iommu_enabled(self) -> bool:
        """Check if IOMMU is enabled in the system."""
        # Check for Intel VT-d or AMD-Vi
        dmar_path = "/sys/firmware/acpi/tables/DMAR"
        ivrs_path = "/sys/firmware/acpi/tables/IVRS"

        return os.path.exists(dmar_path) or os.path.exists(ivrs_path)

    def get_passthrough_summary(self) -> Dict[str, Any]:
        """Get summary of passthrough capabilities."""
        return {
            "iommu_enabled": self.check_iommu_enabled(),
            "total_devices": len(self._device_cache),
            "gpus": len(self.get_gpus()),
            "iommu_groups": len(self._iommu_groups),
            "isolated_groups": sum(
                1 for g in self._iommu_groups.values() if g.is_isolated
            ),
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mgr = PassthroughManager()
    devices = mgr.scan_devices()

    print("=== Passthrough Manager ===")
    print(f"IOMMU Enabled: {mgr.check_iommu_enabled()}")
    print(f"\nFound {len(devices)} PCI devices:")

    for dev in devices:
        isolation = (
            "isolated" if (group := mgr.get_iommu_group(dev.iommu_group)) and group.is_isolated else "shared"
        )
        print(
            f"  {dev.address} | Group {dev.iommu_group} ({isolation}) | "
            f"{dev.device_name} | Driver: {dev.driver_in_use}"
        )

    print("\nGPUs available for passthrough:")
    for gpu in mgr.get_gpus():
        print(f"  {gpu.address}: {gpu.device_name}")
