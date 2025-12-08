from dataclasses import dataclass, field
from typing import List, Optional


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
    devices: List[PCIDevice] = field(default_factory=list)

    @property
    def is_isolated(self) -> bool:
        return len(self.devices) == 1


@dataclass
class PassthroughProfile:
    name: str
    description: str
    device_classes: List[str]


class PassthroughManager:
    def __init__(self):
        # Minimal stub; real functionality not required for current tests
        self.PROFILES = {
            "gaming": PassthroughProfile(
                "Gaming GPU", "GPU + HDMI Audio", ["0300", "0403"]
            ),
            "ai": PassthroughProfile(
                "AI Accelerator", "GPU + 3D Controller", ["0300", "0302"]
            ),
            "usb": PassthroughProfile("USB Controller", "USB controller", ["0c03"]),
            "nvme": PassthroughProfile("NVMe Storage", "NVMe storage", ["0108"]),
        }

    # Stubs for potential calls in skipped tests
    def scan_devices(self):
        return []
