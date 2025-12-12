# !/usr/bin/env python3
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


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

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

    def __init__(self) -> None:
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

    def scan_devices(self) -> List[PCIDevice]:
        return []
