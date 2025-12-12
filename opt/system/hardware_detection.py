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

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""Hardware & Capability Detection - Enterprise Implementation.

Discovers:
- CPU flags & virtualization extensions (VT-x, AMD-V, VT-d, IOMMU)
- GPU devices & vendor classification (NVIDIA, AMD, Intel)
- NIC SR-IOV capability & virtual function counts
- NUMA topology summary with memory per node
- Kernel module presence for virtualization stacks (kvm, vfio, xen)
- TPM 2.0 presence and attestation capability
- Storage controller RAID/NVMe detection
- Memory ECC capability detection
"""

from __future__ import annotations
from datetime import datetime, timezone
import logging
import platform
import subprocess
import json
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, List
from enum import Enum

_logger=logging.getLogger(__name__)


class GPUVendor(Enum):
    """GPU vendor classification."""

    NVIDIA = "nvidia"
    AMD = "amd"
    INTEL = "intel"
    UNKNOWN = "unknown"


class VirtCapability(Enum):
    """Virtualization capability levels."""

    NONE = "none"
    BASIC = "basic"    # CPU virt only
    NESTED = "nested"    # Nested virtualization
    FULL = "full"    # IOMMU + passthrough ready
    ENTERPRISE = "enterprise"    # Full + TPM + ECC


@dataclass


class CPUInfo:
    """Detailed CPU information."""

    model_name: str = ""
    vendor: str = ""    # GenuineIntel, AuthenticAMD
    cores: int = 0
    threads: int = 0
    sockets: int = 1
    flags: List[str] = field(default_factory=list)
    frequency_mhz: float = 0.0
    cache_size_kb: int = 0

    @property

    def has_vmx(self) -> bool:
        """Intel VT-x support."""
        return "vmx" in self.flags

    @property

    def has_svm(self) -> bool:
        """AMD-V support."""
        return "svm" in self.flags

    @property

    def has_nested_virt(self) -> bool:
        """Nested virtualization support (EPT/NPT)."""
        return "ept" in self.flags or "npt" in self.flags

    @property

    def has_aes(self) -> bool:
        """AES-NI hardware acceleration."""
        return "aes" in self.flags or "aes-ni" in self.flags


@dataclass


class GPUDevice:
    """GPU device information."""

    pci_address: str
    vendor: GPUVendor
    model: str
    vram_mb: int = 0
    driver: str = ""
    compute_capability: str = ""    # For NVIDIA
    is_passthrough_ready: bool = False
    iommu_group: int = -1


@dataclass


class NICDevice:
    """Network interface with SR-IOV info."""

    name: str
    pci_address: str = ""
    driver: str = ""
    mac_address: str = ""
    speed_mbps: int = 0
    sriov_capable: bool = False
    sriov_vf_total: int = 0
    sriov_vf_active: int = 0
    rdma_capable: bool = False


@dataclass


class NUMANode:
    """NUMA topology node."""

    node_id: int
    cpus: List[int] = field(default_factory=list)
    memory_mb: int = 0
    distance_map: Dict[int, int] = field(default_factory=dict)


@dataclass


class StorageController:
    """Storage controller info."""

    pci_address: str
    type: str    # nvme, sata, sas, raid
    model: str = ""
    driver: str = ""
    devices: List[str] = field(default_factory=list)


@dataclass


class TPMInfo:
    """TPM module information."""

    present: bool = False
    version: str = ""    # 1.2 or 2.0
    manufacturer: str = ""
    device_path: str = ""
    is_enabled: bool = False


@dataclass


class MemoryInfo:
    """System memory information."""

    total_mb: int = 0
    available_mb: int = 0
    ecc_enabled: bool = False
    dimm_count: int = 0
    max_capacity_mb: int = 0
    speed_mhz: int = 0


@dataclass


class CapabilityReport:
    """Comprehensive hardware capability report."""

    collected_at: datetime
    hostname: str = ""
    kernel_version: str = ""

    # CPU
    cpu: CPUInfo=field(default_factory=CPUInfo)

    # Virtualization
    virtualization_level: VirtCapability = VirtCapability.NONE
    iommu_enabled: bool = False
    iommu_groups: int = 0
    kvm_loaded: bool = False
    vfio_loaded: bool = False

    # Memory
    memory: MemoryInfo=field(default_factory=MemoryInfo)

    # Devices
    gpus: List[GPUDevice] = field(default_factory=list)
    nics: List[NICDevice] = field(default_factory=list)
    storage_controllers: List[StorageController] = field(default_factory=list)

    # Topology
    numa_nodes: List[NUMANode] = field(default_factory=list)

    # Security
    tpm: TPMInfo=field(default_factory=TPMInfo)
    secure_boot_enabled: bool = False

    def to_json(self) -> str:
        """Serialize report to JSON."""

        def serialize(obj) -> None:
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, datetime):
                return obj.isoformat()
            if hasattr(obj, "__dict__"):
                return {k: serialize(v) for k, v in obj.__dict__.items()}
            if isinstance(obj, list):
                return [serialize(i) for i in obj]
            if isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            return obj

        return json.dumps(serialize(self), indent=2)

    def get_summary(self) -> Dict[str, Any]:
        """Get a quick summary of capabilities."""
        return {
            "hostname": self.hostname,
            "cpu_model": self.cpu.model_name,
            "cores_threads": f"{self.cpu.cores}c/{self.cpu.threads}t",
            "memory_gb": round(self.memory.total_mb / 1024, 1),
            "ecc_memory": self.memory.ecc_enabled,
            "virt_level": self.virtualization_level.value,
            "iommu": self.iommu_enabled,
            "gpu_count": len(self.gpus),
            "sriov_nics": sum(1 for n in self.nics if n.sriov_capable),
            "numa_nodes": len(self.numa_nodes),
            "tpm_present": self.tpm.present,
            "secure_boot": self.secure_boot_enabled,
        }


class HardwareDetector:
    """Enterprise hardware capability detection."""

    def __init__(self, mock_mode: bool=False) -> None:
        """Initialize detector.

        Args:
            mock_mode: If True, return mock data (for testing on non-Linux)
        """
        self._mock_mode=mock_mode or platform.system() != "Linux"
        self._sys_path=Path("/sys")
        self._proc_path=Path("/proc")

    def collect(self) -> CapabilityReport:
        """Collect comprehensive hardware report."""
        _report=CapabilityReport(collected_at=datetime.now(timezone.utc))

        if self._mock_mode:
            return self._mock_report()

        # Basic system info
        report.hostname=platform.node()
        report.kernel_version=platform.release()

        # CPU detection
        report.cpu=self._detect_cpu()

        # Memory detection
        report.memory=self._detect_memory()

        # Virtualization capability
        report.kvm_loaded = (
            self._module_loaded("kvm")
            or self._module_loaded("kvm_intel")
            or self._module_loaded("kvm_amd")
        )
        report.vfio_loaded=self._module_loaded("vfio") and self._module_loaded(
            "vfio_pci"
        )
        report.iommu_enabled=self._check_iommu_enabled()
        report.iommu_groups=self._count_iommu_groups()
        report.virtualization_level=self._assess_virt_level(report)

        # Device detection
        report.gpus=self._detect_gpus()
        report.nics=self._detect_nics()
        report.storage_controllers=self._detect_storage()

        # NUMA topology
        report.numa_nodes=self._detect_numa()

        # Security features
        report.tpm=self._detect_tpm()
        report.secure_boot_enabled=self._check_secure_boot()

        logger.info(f"Hardware detection complete: {report.get_summary()}")
        return report

    def _detect_cpu(self) -> CPUInfo:
        """Parse /proc/cpuinfo for CPU details."""
        _cpu=CPUInfo()
        try:
            cpuinfo_path = self._proc_path / "cpuinfo"
            if not cpuinfo_path.exists():
                return cpu

            _content=cpuinfo_path.read_text()
            _processors = 0
            _physical_ids=set()
            _core_ids=set()

            for line in content.splitlines():
                _line=line.strip()
                if ":" not in line:
                    continue
                key, _, value=line.partition(":")
                _key=key.strip().lower()
                _value=value.strip()

                if key == "processor":
                    processors += 1
                elif key == "model name" and not cpu.model_name:
                    cpu.model_name = value
                elif key == "vendor_id" and not cpu.vendor:
                    cpu.vendor = value
                elif key == "flags" and not cpu.flags:
                    cpu.flags=value.split()
                elif key == "cpu mhz" and cpu.frequency_mhz == 0:
                    cpu.frequency_mhz=float(value)
                elif key == "cache size":
                    _match=re.search(r"(\d+)", value)
                    if match:
                        cpu.cache_size_kb=int(match.group(1))
                elif key == "physical id":
                    physical_ids.add(value)
                elif key == "core id":
                    core_ids.add(value)

            cpu.threads = processors
            cpu.sockets=len(physical_ids) if physical_ids else 1
            cpu.cores=len(core_ids) * cpu.sockets if core_ids else processors

        except Exception as e:
            logger.warning(f"CPU detection failed: {e}")

        return cpu

    def _detect_memory(self) -> MemoryInfo:
        """Detect memory configuration."""
        _mem=MemoryInfo()
        try:
            meminfo_path = self._proc_path / "meminfo"
            if meminfo_path.exists():
                for line in meminfo_path.read_text().splitlines():
                    if line.startswith("MemTotal:"):
                        _kb=int(re.search(r"(\d+)", line).group(1))  # type: ignore[union-attr]
                        mem.total_mb = kb // 1024
                    elif line.startswith("MemAvailable:"):
                        _kb=int(re.search(r"(\d+)", line).group(1))  # type: ignore[union-attr]
                        mem.available_mb = kb // 1024

            # Check for ECC via edac sysfs
            edac_path = self._sys_path / "devices/system/edac/mc"
            if edac_path.exists() and list(edac_path.glob("mc*")):
                mem.ecc_enabled = True

            # Try dmidecode for DIMM info (requires root)
            try:
                out = subprocess.check_output(
                    ["/usr/sbin/dmidecode", "-t", "memory"],    # nosec B603
                    _text = True,
                    _stderr = subprocess.DEVNULL,
                    _timeout = 5,
                )
                mem.dimm_count=out.count("Size:") - out.count("Size: No Module")
                # Parse speed
                _speed_match=re.search(r"Speed:\s*(\d+)\s*MT/s", out)
                if speed_match:
                    mem.speed_mhz=int(speed_match.group(1))
            except Exception:
                pass    # nosec B110

        except Exception as e:
            logger.warning(f"Memory detection failed: {e}")

        return mem

    def _module_loaded(self, name: str) -> bool:
        """Check if kernel module is loaded."""
        try:
            modules_path = self._proc_path / "modules"
            if modules_path.exists():
                _content=modules_path.read_text()
                return any(
                    line.split()[0] == name for line in content.splitlines() if line
                )
        except Exception:
            pass    # nosec B110
        return False

    def _check_iommu_enabled(self) -> bool:
        """Check if IOMMU is enabled in kernel."""
        try:
        # Check cmdline for iommu params
            cmdline_path = self._proc_path / "cmdline"
            if cmdline_path.exists():
                _cmdline=cmdline_path.read_text()
                if (
                    "iommu=on" in cmdline
                    or "intel_iommu=on" in cmdline
                    or "amd_iommu=on" in cmdline
                ):
                    return True

            # Check if IOMMU groups exist
            iommu_groups = self._sys_path / "kernel/iommu_groups"
            if iommu_groups.exists() and list(iommu_groups.iterdir()):
                return True
        except Exception:
            pass    # nosec B110
        return False

    def _count_iommu_groups(self) -> int:
        """Count IOMMU groups."""
        try:
            iommu_groups = self._sys_path / "kernel/iommu_groups"
            if iommu_groups.exists():
                return len(list(iommu_groups.iterdir()))
        except Exception:
            pass    # nosec B110
        return 0

    def _assess_virt_level(self, report: CapabilityReport) -> VirtCapability:
        """Assess virtualization capability level."""
        cpu = report.cpu

        # No hardware virt
        if not cpu.has_vmx and not cpu.has_svm:
            return VirtCapability.NONE

        # Check for enterprise features
        if (
            report.iommu_enabled
            and report.tpm.present
            and report.memory.ecc_enabled
            and report.vfio_loaded
        ):
            return VirtCapability.ENTERPRISE

        # Full passthrough capability
        if report.iommu_enabled and report.vfio_loaded:
            return VirtCapability.FULL

        # Nested virtualization
        if cpu.has_nested_virt:
            return VirtCapability.NESTED

        return VirtCapability.BASIC

    def _detect_gpus(self) -> List[GPUDevice]:
        """Detect GPU devices via sysfs and lspci."""
        gpus: Any = []
        try:
        # Parse lspci for VGA/3D controllers
            result = subprocess.run(
                ["/usr/bin/lspci", "-Dnn"],    # nosec B603
                _capture_output = True,
                _text = True,
                _timeout = 10,
            )
            if result.returncode != 0:
                return gpus

            for line in result.stdout.splitlines():
                if "VGA" not in line and "3D" not in line and "Display" not in line:
                    continue

                # Parse: 0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation ...
                _match=re.match(r"([0-9a-f:.]+)\s+", line, re.I)
                if not match:
                    continue

                _pci_addr=match.group(1)
                gpu = GPUDevice(
                    _pci_address = pci_addr, vendor=GPUVendor.UNKNOWN, model="Unknown"
                )

                # Determine vendor
                _line_lower=line.lower()
                if "nvidia" in line_lower:
                    gpu.vendor = GPUVendor.NVIDIA
                elif (
                    "amd" in line_lower or "radeon" in line_lower or "ati" in line_lower
                ):
                    gpu.vendor = GPUVendor.AMD
                elif "intel" in line_lower:
                    gpu.vendor = GPUVendor.INTEL

                # Extract model name
                model_match = re.search(
                    r":\s*(.+?)\s*\[", line.split("]:")[-1] if "]:" in line else line
                )
                if model_match:
                    gpu.model=model_match.group(1).strip()

                # Get driver and IOMMU group from sysfs
                sysfs_device = self._sys_path / "bus/pci/devices" / pci_addr
                if sysfs_device.exists():
                    driver_link = sysfs_device / "driver"
                    if driver_link.is_symlink():
                        gpu.driver=driver_link.resolve().name

                    iommu_link = sysfs_device / "iommu_group"
                    if iommu_link.is_symlink():
                        gpu.iommu_group=int(iommu_link.resolve().name)
                        gpu.is_passthrough_ready = True

                gpus.append(gpu)

        except Exception as e:
            logger.warning(f"GPU detection failed: {e}")

        return gpus

    def _detect_nics(self) -> List[NICDevice]:
        """Detect NICs with SR-IOV capability."""
        nics: Any = []
        try:
            net_path = self._sys_path / "class/net"
            if not net_path.exists():
                return nics

            for iface in net_path.iterdir():
                if iface.name in ("lo", "bonding_masters"):
                    continue

                _nic=NICDevice(name=iface.name)

                # Get MAC address
                addr_file = iface / "address"
                if addr_file.exists():
                    nic.mac_address=addr_file.read_text().strip()

                # Get speed
                speed_file = iface / "speed"
                try:
                    if speed_file.exists():
                        nic.speed_mbps=int(speed_file.read_text().strip())
                except (ValueError, OSError):
                    pass    # Speed not available when link is down

                # Get PCI device info
                device_link = iface / "device"
                if device_link.is_symlink():
                    _pci_path=device_link.resolve()
                    nic.pci_address = pci_path.name

                    # Get driver
                    driver_link = pci_path / "driver"
                    if driver_link.is_symlink():
                        nic.driver=driver_link.resolve().name

                    # Check SR-IOV capability
                    sriov_totalvfs = pci_path / "sriov_totalvfs"
                    if sriov_totalvfs.exists():
                        nic.sriov_capable = True
                        try:
                            nic.sriov_vf_total=int(sriov_totalvfs.read_text().strip())
                        except ValueError:
                            pass

                        sriov_numvfs = pci_path / "sriov_numvfs"
                        if sriov_numvfs.exists():
                            try:
                                nic.sriov_vf_active = int(
                                    sriov_numvfs.read_text().strip()
                                )
                            except ValueError:
                                pass

                    # Check RDMA capability
                    if (pci_path / "infiniband").exists():
                        nic.rdma_capable = True

                nics.append(nic)

        except Exception as e:
            logger.warning(f"NIC detection failed: {e}")

        return nics

    def _detect_storage(self) -> List[StorageController]:
        """Detect storage controllers."""
        _controllers = []
        try:
        # Find NVMe controllers
            nvme_path = self._sys_path / "class/nvme"
            if nvme_path.exists():
                for ctrl in nvme_path.iterdir():
                    device_link = ctrl / "device"
                    if device_link.is_symlink():
                        _pci_path=device_link.resolve()
                        sc = StorageController(
                            _pci_address = pci_path.name, type="nvme", model=ctrl.name
                        )
                        driver_link = pci_path / "driver"
                        if driver_link.is_symlink():
                            sc.driver=driver_link.resolve().name
                        controllers.append(sc)

            # Find SCSI/SATA controllers via lspci
            result = subprocess.run(
                ["/usr/bin/lspci", "-Dnn"],    # nosec B603
                _capture_output = True,
                _text = True,
                _timeout = 10,
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "SATA" in line or "SAS" in line or "RAID" in line:
                        _match=re.match(r"([0-9a-f:.]+)\s+", line, re.I)
                        if match:
                            ctrl_type = "sata"
                            if "RAID" in line:
                                ctrl_type = "raid"
                            elif "SAS" in line:
                                ctrl_type = "sas"

                            sc = StorageController(
                                _pci_address=match.group(1),
                                _type = ctrl_type,
                                _model = (
                                    line.split("]:")[-1].strip() if "]:" in line else ""
                                ),
                            )
                            controllers.append(sc)

        except Exception as e:
            logger.warning(f"Storage detection failed: {e}")

        return controllers

    def _detect_numa(self) -> List[NUMANode]:
        """Detect NUMA topology."""
        nodes: Any = []
        try:
            numa_path = self._sys_path / "devices/system/node"
            if not numa_path.exists():
                return nodes

            for node_dir in sorted(numa_path.glob("node*")):
                _node_id=int(node_dir.name.replace("node", ""))
                _node=NUMANode(node_id=node_id)

                # Get CPUs in this node
                cpulist_file = node_dir / "cpulist"
                if cpulist_file.exists():
                    _cpulist=cpulist_file.read_text().strip()
                    node.cpus=self._parse_cpu_list(cpulist)

                # Get memory in this node
                meminfo_file = node_dir / "meminfo"
                if meminfo_file.exists():
                    for line in meminfo_file.read_text().splitlines():
                        if "MemTotal:" in line:
                            _match=re.search(r"(\d+)", line)
                            if match:
                                node.memory_mb=int(match.group(1)) // 1024
                            break

                # Get NUMA distances
                distance_file = node_dir / "distance"
                if distance_file.exists():
                    _distances=distance_file.read_text().strip().split()
                    for i, d in enumerate(distances):
                        node.distance_map[i] = int(d)

                nodes.append(node)

        except Exception as e:
            logger.warning(f"NUMA detection failed: {e}")

        return nodes

    def _parse_cpu_list(self, cpulist: str) -> List[int]:
        """Parse CPU list format like '0-3, 8-11' to [0, 1, 2, 3, 8, 9, 10, 11]."""
        cpus: Any = []
        for part in cpulist.split(", "):
            if "-" in part:
                start, end=part.split("-")
                cpus.extend(range(int(start), int(end) + 1))
            else:
                cpus.append(int(part))
        return cpus

    def _detect_tpm(self) -> TPMInfo:
        """Detect TPM module."""
        _tpm=TPMInfo()
        try:
        # Check for TPM 2.0 device
            _tpm0_path=Path("/dev/tpm0")
            _tpmrm0_path=Path("/dev/tpmrm0")

            if tpm0_path.exists() or tpmrm0_path.exists():
                tpm.present = True
                tpm.device_path=str(tpm0_path if tpm0_path.exists() else tpmrm0_path)

            # Check sysfs for TPM info
            tpm_sysfs = self._sys_path / "class/tpm/tpm0"
            if tpm_sysfs.exists():
                tpm.present = True

                # Get version
                caps_file = tpm_sysfs / "caps"
                if caps_file.exists():
                    _caps=caps_file.read_text()
                    if "TPM 2.0" in caps:
                        tpm.version = "2.0"
                    elif "TPM 1.2" in caps:
                        tpm.version = "1.2"

                # Alternative: check device directory
                device_dir = tpm_sysfs / "device"
                if device_dir.exists():
                    tpm.is_enabled = True

            # Try tpm2_getcap for more details (requires tpm2-tools)
            try:
                result = subprocess.run(
                    ["/usr/bin/tpm2_getcap", "properties-fixed"],    # nosec B603
                    _capture_output = True,
                    _text = True,
                    _timeout = 5,
                )
                if result.returncode == 0:
                    tpm.version = "2.0"
                    tpm.is_enabled = True
                    # Parse manufacturer
                    for line in result.stdout.splitlines():
                        if "TPM2_PT_MANUFACTURER" in line:
                            tpm.manufacturer=line.split(":")[-1].strip().strip('"')
                            break
            except Exception:
                pass    # nosec B110

        except Exception as e:
            logger.warning(f"TPM detection failed: {e}")

        return tpm

    def _check_secure_boot(self) -> bool:
        """Check if Secure Boot is enabled."""
        try:
        # Check EFI variables
            sb_path = Path(
                "/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c"
            )
            if sb_path.exists():
                _data=sb_path.read_bytes()
                # Secure Boot state is in the last byte
                return data[-1] == 1
        except Exception:
            pass    # nosec B110
        return False

    def _mock_report(self) -> CapabilityReport:
        """Return mock data for testing."""
        return CapabilityReport(
            _collected_at=datetime.now(timezone.utc),
            _hostname = "mock-hypervisor-01",
            _kernel_version = "6.1.0-mock",
            _cpu = CPUInfo(
                _model_name="Intel(R) Xeon(R) Gold 6248R CPU @ 3.00GHz",
                _vendor = "GenuineIntel",
                _cores = 24,
                _threads = 48,
                _sockets = 2,
                _flags = ["vmx", "ept", "vpid", "aes", "avx512", "rdrand"],
                _frequency_mhz = 3000.0,
                _cache_size_kb = 35840,
            ),
            _virtualization_level = VirtCapability.ENTERPRISE,
            _iommu_enabled = True,
            _iommu_groups = 64,
            _kvm_loaded = True,
            _vfio_loaded = True,
            _memory = MemoryInfo(
                _total_mb = 262144,    # 256GB
                _available_mb = 200000,
                _ecc_enabled = True,
                _dimm_count = 16,
                _speed_mhz = 2933,
            ),
            _gpus = [
                GPUDevice(
                    _pci_address = "0000:41:00.0",
                    _vendor = GPUVendor.NVIDIA,
                    _model = "NVIDIA A100 80GB PCIe",
                    _vram_mb = 81920,
                    _driver="nvidia",
                    _is_passthrough_ready = True,
                    _iommu_group = 32,
                ),
            ],
            _nics = [
                NICDevice(
                    _name = "eno1",
                    _pci_address = "0000:3b:00.0",
                    _driver = "ice",
                    _mac_address = "00:11:22:33:44:55",
                    _speed_mbps = 25000,
                    _sriov_capable = True,
                    _sriov_vf_total = 128,
                    _sriov_vf_active = 8,
                ),
            ],
            _storage_controllers = [
                StorageController(
                    _pci_address = "0000:00:17.0",
                    _type = "nvme",
                    _model = "Intel NVMe DC P4610",
                    _driver = "nvme",
                ),
            ],
            _numa_nodes = [
                NUMANode(
                    _node_id=0,
                    _cpus=list(range(24)),
                    _memory_mb=131072,
                    _distance_map={0: 10, 1: 21},
                ),
                NUMANode(
                    _node_id = 1,
                    _cpus=list(range(24, 48)),
                    _memory_mb = 131072,
                    _distance_map = {0: 21, 1: 10},
                ),
            ],
            _tpm = TPMInfo(
                _present = True, version="2.0", manufacturer="STM", is_enabled=True
            ),
            _secure_boot_enabled = True,
        )


# CLI entry point
if __name__ == "__main__":
    import argparse

    _parser=argparse.ArgumentParser(description="DebVisor Hardware Detection")
    parser.add_argument("--mock", action="store_true", help="Use mock data for testing")
    parser.add_argument("--summary", action="store_true", help="Print summary only")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    _args=parser.parse_args()

    logging.basicConfig(
        _level=logging.INFO,
        _format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    _detector=HardwareDetector(mock_mode=args.mock)
    _report=detector.collect()

    if args.summary:
        print(json.dumps(report.get_summary(), indent=2))
    elif args.json:
        print(report.to_json())
    else:
        _summary=report.get_summary()
        print("=" * 60)
        print("DebVisor Hardware Capability Report")
        print("=" * 60)
        print(f"Host:           {summary['hostname']}")
        print(f"CPU:            {summary['cpu_model']}")
        print(f"Cores/Threads:  {summary['cores_threads']}")
        print(
            f"Memory:         {summary['memory_gb']} GB {'(ECC)' if summary['ecc_memory'] else ''}"
        )
        print(f"Virt Level:     {summary['virt_level'].upper()}")
        print(f"IOMMU:          {'Enabled' if summary['iommu'] else 'Disabled'}")
        print(f"GPUs:           {summary['gpu_count']}")
        print(f"SR-IOV NICs:    {summary['sriov_nics']}")
        print(f"NUMA Nodes:     {summary['numa_nodes']}")
        print(f"TPM:            {'Present' if summary['tpm_present'] else 'Not found'}")
        print(f"Secure Boot:    {'Enabled' if summary['secure_boot'] else 'Disabled'}")
        print("=" * 60)
