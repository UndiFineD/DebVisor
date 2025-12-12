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


"""Xen Hypervisor Driver - Enterprise Implementation.

Provides unified hypervisor abstraction layer for Xen:
- Host capability detection (xl info, physinfo)
- VM lifecycle management (create/destroy/migrate/pause/resume)
- Storage/network configuration translation
- PV vs HVM mode selection
- Resource scheduling and pinning
- Live migration coordination
- Security isolation profiles
- Integration with unified DebVisor VM model
"""

from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from enum import Enum
from abc import ABC, abstractmethod
import logging
import subprocess
import re
import os
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Enums and Constants
# -----------------------------------------------------------------------------


class XenVMType(Enum):
    PV = "pv"    # Paravirtualized (Linux guests)
    HVM = "hvm"    # Hardware Virtual Machine (Windows/full virt)
    PVH = "pvh"    # PV in HVM container (modern hybrid)
    PVSHIM = "pvshim"    # PV shim for HVM guests


class VMState(Enum):
    RUNNING = "running"
    PAUSED = "paused"
    BLOCKED = "blocked"
    SHUTDOWN = "shutdown"
    CRASHED = "crashed"
    DYING = "dying"
    UNKNOWN = "unknown"


class MigrationMode(Enum):
    LIVE = "live"    # Live migration (minimal downtime)
    OFFLINE = "offline"    # Cold migration (VM stopped)
    POSTCOPY = "postcopy"    # Post-copy migration


class SchedulerType(Enum):
    CREDIT = "credit"
    CREDIT2 = "credit2"
    RTDS = "rtds"    # Real-time scheduler
    ARINC653 = "arinc653"
    NULL = "null"


@dataclass
class XenHostInfo:
    """Xen hypervisor host information."""

    xen_version: str
    xen_major: int
    xen_minor: int
    xen_extra: str
    capabilities: List[str]
    total_memory_mb: int
    free_memory_mb: int
    total_cpus: int
    online_cpus: int
    cpu_mhz: int
    hw_caps: List[str]
    scheduler: SchedulerType
    virt_caps: List[str]    # hvm, hap, shadow, etc.
    numa_nodes: int
    host_name: str
    xen_commandline: str


@dataclass
class XenVMConfig:
    """Xen VM configuration (maps to xl.cfg format)."""

    name: str
    uuid: Optional[str] = None
    vm_type: XenVMType = XenVMType.HVM
    vcpus: int = 1
    maxvcpus: Optional[int] = None
    memory_mb: int = 1024
    maxmem_mb: Optional[int] = None

    # Boot configuration
    kernel: Optional[str] = None    # For PV
    ramdisk: Optional[str] = None
    cmdline: Optional[str] = None
    bootloader: Optional[str] = None
    boot_device: str = "c"    # For HVM: c=disk, d=cdrom, n=network

    # Disks
    disks: List[Dict[str, Any]] = field(default_factory=list)
    # Format: [{"vdev": "xvda", "target": "/dev/zvol/...", "format": "raw", "mode": "rw"}]

    # Network
    vifs: List[Dict[str, Any]] = field(default_factory=list)
    # Format: [{"bridge": "xenbr0", "mac": "...", "model": "rtl8139", "rate": "10MB/s"}]

    # HVM-specific
    firmware: str = "uefi"    # bios, uefi, seabios, ovmf
    viridian: bool = False    # Hyper-V enlightenments
    usb: bool = False
    usbdevice: Optional[str] = None
    serial: str = "pty"
    vnc: bool = True
    vnclisten: str = "0.0.0.0"    # nosec B104
    vncpasswd: Optional[str] = None
    spice: bool = False

    # Resource control
    cpu_weight: int = 256
    cpu_cap: int = 0    # 0 = no cap, 100 = 1 physical CPU
    cpus: Optional[str] = None    # CPU pinning: "0-3", "0, 2, 4"
    numa_placement: Optional[str] = None

    # Security
    seclabel: Optional[str] = None    # XSM/Flask label
    device_model_stubdomain: bool = False

    # Misc
    on_crash: str = "restart"
    on_reboot: str = "restart"
    on_watchdog: str = "destroy"
    timer_mode: str = "delay_for_missed_ticks"

    # Passthrough
    pci: List[str] = field(default_factory=list)    # ["0000:01:00.0"]

    # Extra options
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class XenVM:
    """Running Xen VM (domU) information."""

    domid: int
    name: str
    uuid: str
    state: VMState
    vcpus: int
    memory_mb: int
    cpu_time_ns: int
    uptime_seconds: float
    vm_type: XenVMType
    ssidref: int = 0    # Security ID

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domid": self.domid,
            "name": self.name,
            "uuid": self.uuid,
            "state": self.state.value,
            "vcpus": self.vcpus,
            "memory_mb": self.memory_mb,
            "cpu_time_ns": self.cpu_time_ns,
            "uptime_seconds": self.uptime_seconds,
            "vm_type": self.vm_type.value,
        }


@dataclass
class MigrationStatus:
    """Live migration status."""

    vm_name: str
    source_host: str
    dest_host: str
    state: str    # started, transferring, finishing, completed, failed
    progress_percent: float
    transferred_mb: int
    remaining_mb: int
    downtime_ms: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


# -----------------------------------------------------------------------------
# Xen Command Executor
# -----------------------------------------------------------------------------


class XenCommandExecutor:
    """Execute xl/xm commands with error handling."""

    def __init__(self, tool: str = "xl"):
        self.tool = tool    # xl (modern) or xm (legacy)
        self.timeout = 60

    def run(
        self, args: List[str], timeout: Optional[int] = None, check: bool = True
    ) -> Tuple[int, str, str]:
        """Run xl command and return (returncode, stdout, stderr)."""
        cmd = [self.tool] + args
        actual_timeout = timeout or self.timeout

        try:
            result = subprocess.run(
                cmd,    # nosec B603
                capture_output=True,
                text=True,
                timeout=actual_timeout,
            )

            if check and result.returncode != 0:
                logger.warning(
                    f"Command failed: {' '.join(cmd)}\nstderr: {result.stderr}"
                )

            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {' '.join(cmd)}")
            return -1, "", "Command timed out"
        except FileNotFoundError:
            logger.error(f"Xen tool not found: {self.tool}")
            return -1, "", f"{self.tool} not found"

    def run_json(self, args: List[str]) -> Optional[Any]:
        """Run command expecting JSON output."""
        # xl doesn't natively output JSON, so we parse text output
        code, stdout, stderr = self.run(args, check=False)
        if code != 0:
            return None
        return stdout


# -----------------------------------------------------------------------------
# Config Generator
# -----------------------------------------------------------------------------


class XenConfigGenerator:
    """Generate xl.cfg format configuration files."""

    @staticmethod
    def generate(config: XenVMConfig) -> str:
        """Generate xl.cfg content."""
        lines = []

        # Basic settings
        lines.append(f'name = "{config.name}"')
        if config.uuid:
            lines.append(f'uuid = "{config.uuid}"')
        lines.append(f'type = "{config.vm_type.value}"')
        lines.append(f"vcpus = {config.vcpus}")
        if config.maxvcpus:
            lines.append(f"maxvcpus = {config.maxvcpus}")
        lines.append(f"memory = {config.memory_mb}")
        if config.maxmem_mb:
            lines.append(f"maxmem = {config.maxmem_mb}")

        # Boot configuration
        if config.vm_type == XenVMType.PV:
            if config.kernel:
                lines.append(f'kernel = "{config.kernel}"')
            if config.ramdisk:
                lines.append(f'ramdisk = "{config.ramdisk}"')
            if config.cmdline:
                lines.append(f'extra = "{config.cmdline}"')
            if config.bootloader:
                lines.append(f'bootloader = "{config.bootloader}"')
        else:    # HVM
            lines.append(f'boot = "{config.boot_device}"')
            if config.firmware == "uefi":
                lines.append('bios = "ovmf"')
            else:
                lines.append(f'bios = "{config.firmware}"')

        # Disks
        if config.disks:
            disk_strs = []
            for disk in config.disks:
                target = disk.get("target", "")
                vdev = disk.get("vdev", "xvda")
                fmt = disk.get("format", "raw")
                mode = disk.get("mode", "rw")

                if config.vm_type in [XenVMType.HVM, XenVMType.PVH]:
                # HVM format: phy:/dev/...,hda,w
                    disk_strs.append(f'"{fmt}:{target}, {vdev}, {mode}"')
                else:
                # PV format: phy:/dev/...,xvda,w
                    disk_strs.append(f'"phy:{target}, {vdev}, {mode}"')

            lines.append(f'disk = [{", ".join(disk_strs)}]')

        # Network interfaces
        if config.vifs:
            vif_strs = []
            for vif in config.vifs:
                parts = []
                if vif.get("mac"):
                    parts.append(f'mac={vif["mac"]}')
                if vif.get("bridge"):
                    parts.append(f'bridge={vif["bridge"]}')
                if vif.get("model") and config.vm_type != XenVMType.PV:
                    parts.append(f'model={vif["model"]}')
                if vif.get("rate"):
                    parts.append(f'rate={vif["rate"]}')
                vif_strs.append(f'"{", ".join(parts)}"')

            lines.append(f'vif = [{", ".join(vif_strs)}]')

        # HVM-specific
        if config.vm_type != XenVMType.PV:
            if config.viridian:
                lines.append("viridian = 1")
            if config.usb:
                lines.append("usb = 1")
                if config.usbdevice:
                    lines.append(f'usbdevice = "{config.usbdevice}"')
            lines.append(f'serial = "{config.serial}"')
            if config.vnc:
                lines.append("vnc = 1")
                lines.append(f'vnclisten = "{config.vnclisten}"')
                if config.vncpasswd:
                    lines.append(f'vncpasswd = "{config.vncpasswd}"')
            if config.spice:
                lines.append("spice = 1")

        # Resource control
        if config.cpu_weight != 256:
            lines.append(f"cpu_weight = {config.cpu_weight}")
        if config.cpu_cap > 0:
            lines.append(f"cap = {config.cpu_cap}")
        if config.cpus:
            lines.append(f'cpus = "{config.cpus}"')
        if config.numa_placement:
            lines.append(f"numa = {config.numa_placement}")

        # Security
        if config.seclabel:
            lines.append(f'seclabel = "{config.seclabel}"')
        if config.device_model_stubdomain:
            lines.append("device_model_stubdomain_override = 1")

        # Lifecycle
        lines.append(f'on_crash = "{config.on_crash}"')
        lines.append(f'on_reboot = "{config.on_reboot}"')
        lines.append(f'on_watchdog = "{config.on_watchdog}"')

        # PCI passthrough
        if config.pci:
            pci_strs = [f'"{p}"' for p in config.pci]
            lines.append(f'pci = [{", ".join(pci_strs)}]')

        # Timer mode
        if config.vm_type != XenVMType.PV:
            lines.append(f'timer_mode = "{config.timer_mode}"')

        # Extra options
        for key, value in config.extra.items():
            if isinstance(value, str):
                lines.append(f'{key} = "{value}"')
            elif isinstance(value, bool):
                lines.append(f"{key} = {1 if value else 0}")
            else:
                lines.append(f"{key} = {value}")

        return "\n".join(lines)


# -----------------------------------------------------------------------------
# Xen Driver
# -----------------------------------------------------------------------------


class XenDriver:
    """Enterprise Xen hypervisor driver."""

    def __init__(self, config_dir: str = "/etc/xen"):
        self.config_dir = Path(config_dir)
        self.executor = XenCommandExecutor()
        self.config_generator = XenConfigGenerator()
        self._available: Optional[bool] = None
        self._host_info: Optional[XenHostInfo] = None
        self._callbacks: List[Callable[[str, XenVM], None]] = []

    @property
    def available(self) -> bool:
        """Check if Xen tools are available."""
        if self._available is None:
            code, _, _ = self.executor.run(["info"], check=False)
            self._available = code == 0
        return self._available

    def register_callback(self, callback: Callable[[str, XenVM], None]) -> None:
        """Register VM state change callback."""
        self._callbacks.append(callback)

    def _notify(self, event: str, vm: XenVM) -> None:
        for cb in self._callbacks:
            try:
                cb(event, vm)
            except Exception as e:
                logger.warning(f"Callback error: {e}")

    def get_host_info(self, refresh: bool = False) -> Optional[XenHostInfo]:
        """Get Xen host information."""
        if not self.available:
            return None

        if self._host_info and not refresh:
            return self._host_info

        code, stdout, _ = self.executor.run(["info"])
        if code != 0:
            return None

        info = self._parse_xl_info(stdout)

        # Also get physical info
        code, phys_out, _ = self.executor.run(["info", "-n"])
        if code == 0:
            info.update(self._parse_xl_info(phys_out))

        try:
            self._host_info = XenHostInfo(
                xen_version=info.get("xen_version", "unknown"),
                xen_major=int(info.get("xen_major", 0)),
                xen_minor=int(info.get("xen_minor", 0)),
                xen_extra=info.get("xen_extra", ""),
                capabilities=info.get("xen_caps", "").split(),
                total_memory_mb=int(info.get("total_memory", 0)),
                free_memory_mb=int(info.get("free_memory", 0)),
                total_cpus=int(info.get("nr_cpus", 0)),
                online_cpus=int(info.get("online_cpus", info.get("nr_cpus", 0))),
                cpu_mhz=int(info.get("cpu_mhz", 0)),
                hw_caps=info.get("hw_caps", "").split(),
                scheduler=SchedulerType(info.get("sched_id", "credit")),
                virt_caps=info.get("virt_caps", "").split(),
                numa_nodes=int(info.get("nr_nodes", 1)),
                host_name=info.get("host", ""),
                xen_commandline=info.get("xen_commandline", ""),
            )
        except (ValueError, KeyError) as e:
            logger.warning(f"Error parsing xl info: {e}")
            return None

        return self._host_info

    def _parse_xl_info(self, output: str) -> Dict[str, str]:
        """Parse xl info key:value output."""
        result = {}
        for line in output.strip().split("\n"):
            if ":" in line:
                key, _, value = line.partition(":")
                result[key.strip()] = value.strip()
        return result

    def list_vms(self, include_dom0: bool = False) -> List[XenVM]:
        """List all running VMs."""
        if not self.available:
            return []

        code, stdout, _ = self.executor.run(["list"])
        if code != 0:
            return []

        vms = []
        lines = stdout.strip().split("\n")[1:]    # Skip header

        for line in lines:
            parts = line.split()
            if len(parts) < 6:
                continue

            name = parts[0]
            domid = int(parts[1])

            if domid == 0 and not include_dom0:
                continue

            mem = int(parts[2])
            vcpus = int(parts[3])
            state_str = parts[4]
            cpu_time = float(parts[5]) if len(parts) > 5 else 0.0

            # Parse state
            state = VMState.UNKNOWN
            if "r" in state_str:
                state = VMState.RUNNING
            elif "b" in state_str:
                state = VMState.BLOCKED
            elif "p" in state_str:
                state = VMState.PAUSED
            elif "s" in state_str:
                state = VMState.SHUTDOWN
            elif "c" in state_str:
                state = VMState.CRASHED
            elif "d" in state_str:
                state = VMState.DYING

            # Get additional info
            vm_info = self._get_vm_info(domid)

            vm = XenVM(
                domid=domid,
                name=name,
                uuid=vm_info.get("uuid", ""),
                state=state,
                vcpus=vcpus,
                memory_mb=mem,
                cpu_time_ns=int(cpu_time * 1e9),
                uptime_seconds=vm_info.get("uptime", 0.0),
                vm_type=XenVMType(vm_info.get("type", "hvm")),
            )
            vms.append(vm)

        return vms

    def _get_vm_info(self, domid: int) -> Dict[str, Any]:
        """Get detailed VM info."""
        info = {"type": "hvm", "uuid": "", "uptime": 0.0}

        # Get UUID and type from xl list -l (long format)
        code, stdout, _ = self.executor.run(["list", "-l", str(domid)], check=False)
        if code == 0:
        # Parse SXPR or JSON output
            if "uuid" in stdout:
                match = re.search(r'uuid\s*[:=]\s*"?([a-f0-9-]+)"?', stdout, re.I)
                if match:
                    info["uuid"] = match.group(1)
            if "type" in stdout.lower():
                if "pv" in stdout.lower():
                    info["type"] = "pv"
                elif "pvh" in stdout.lower():
                    info["type"] = "pvh"

        # Get uptime
        code, stdout, _ = self.executor.run(["uptime", str(domid)], check=False)
        if code == 0:
        # Parse uptime output
            match = re.search(r"(\d+)\s*s", stdout)
            if match:
                info["uptime"] = float(match.group(1))

        return info

    def get_vm(self, name_or_id: str) -> Optional[XenVM]:
        """Get VM by name or domid."""
        vms = self.list_vms()
        for vm in vms:
            if vm.name == name_or_id or str(vm.domid) == name_or_id:
                return vm
        return None

    def create_vm(self, config: XenVMConfig) -> Tuple[bool, str]:
        """Create and start a VM from config."""
        if not self.available:
            return False, "Xen not available"

        # Generate config file
        cfg_content = self.config_generator.generate(config)

        # Write to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cfg", delete=False) as f:
            f.write(cfg_content)
            cfg_path = f.name

        try:
            code, stdout, stderr = self.executor.run(["create", cfg_path])
            if code == 0:
                logger.info(f"Created VM {config.name}")
                vm = self.get_vm(config.name)
                if vm:
                    self._notify("created", vm)
                return True, f"VM {config.name} created"
            else:
                return False, stderr
        finally:
            os.unlink(cfg_path)

    def destroy_vm(self, name_or_id: str) -> Tuple[bool, str]:
        """Forcefully destroy a VM."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        code, stdout, stderr = self.executor.run(["destroy", str(vm.domid)])
        if code == 0:
            self._notify("destroyed", vm)
            return True, f"VM {vm.name} destroyed"
        return False, stderr

    def shutdown_vm(
        self, name_or_id: str, wait: bool = True, timeout: int = 120
    ) -> Tuple[bool, str]:
        """Gracefully shutdown a VM."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        args = ["shutdown"]
        if wait:
            args.extend(["-w", "-t", str(timeout)])
        args.append(str(vm.domid))

        code, stdout, stderr = self.executor.run(args, timeout=timeout + 10)
        if code == 0:
            self._notify("shutdown", vm)
            return True, f"VM {vm.name} shutdown"
        return False, stderr

    def reboot_vm(self, name_or_id: str) -> Tuple[bool, str]:
        """Reboot a VM."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        code, stdout, stderr = self.executor.run(["reboot", str(vm.domid)])
        if code == 0:
            self._notify("rebooted", vm)
            return True, f"VM {vm.name} rebooted"
        return False, stderr

    def pause_vm(self, name_or_id: str) -> Tuple[bool, str]:
        """Pause a VM."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        code, stdout, stderr = self.executor.run(["pause", str(vm.domid)])
        if code == 0:
            vm.state = VMState.PAUSED
            self._notify("paused", vm)
            return True, f"VM {vm.name} paused"
        return False, stderr

    def unpause_vm(self, name_or_id: str) -> Tuple[bool, str]:
        """Unpause/resume a VM."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        code, stdout, stderr = self.executor.run(["unpause", str(vm.domid)])
        if code == 0:
            vm.state = VMState.RUNNING
            self._notify("resumed", vm)
            return True, f"VM {vm.name} resumed"
        return False, stderr

    def migrate_vm(
        self,
        name_or_id: str,
        dest_host: str,
        mode: MigrationMode = MigrationMode.LIVE,
        ssl: bool = True,
    ) -> Tuple[bool, str]:
        """Migrate VM to another host."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        args = ["migrate"]
        if mode == MigrationMode.LIVE:
            args.append("-l")
        if ssl:
            args.append("-s")
        args.extend([str(vm.domid), dest_host])

        # Migration can take a while
        code, stdout, stderr = self.executor.run(args, timeout=3600)
        if code == 0:
            self._notify("migrated", vm)
            return True, f"VM {vm.name} migrated to {dest_host}"
        return False, stderr

    def save_vm(self, name_or_id: str, save_path: str) -> Tuple[bool, str]:
        """Save VM state to file (hibernate)."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        code, stdout, stderr = self.executor.run(["save", str(vm.domid), save_path])
        if code == 0:
            self._notify("saved", vm)
            return True, f"VM {vm.name} saved to {save_path}"
        return False, stderr

    def restore_vm(self, save_path: str, paused: bool = False) -> Tuple[bool, str]:
        """Restore VM from saved state."""
        args = ["restore"]
        if paused:
            args.append("-p")
        args.append(save_path)

        code, stdout, stderr = self.executor.run(args)
        if code == 0:
            return True, "VM restored"
        return False, stderr

    def console_vm(self, name_or_id: str) -> Tuple[bool, str]:
        """Get console device path for VM."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        # Return the TTY path
        tty_path = f"/dev/pts/{vm.domid}"    # Simplified
        return True, tty_path

    def set_vcpus(self, name_or_id: str, vcpu_count: int) -> Tuple[bool, str]:
        """Hot-plug/unplug vCPUs."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        code, stdout, stderr = self.executor.run(
            ["vcpu-set", str(vm.domid), str(vcpu_count)]
        )
        if code == 0:
            return True, f"vCPUs set to {vcpu_count}"
        return False, stderr

    def set_memory(self, name_or_id: str, memory_mb: int) -> Tuple[bool, str]:
        """Hot-plug/unplug memory (balloon)."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        code, stdout, stderr = self.executor.run(
            ["mem-set", str(vm.domid), str(memory_mb)]
        )
        if code == 0:
            return True, f"Memory set to {memory_mb}MB"
        return False, stderr

    def attach_disk(
        self, name_or_id: str, disk_spec: str, vdev: str
    ) -> Tuple[bool, str]:
        """Hot-attach a disk to VM."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        code, stdout, stderr = self.executor.run(
            ["block-attach", str(vm.domid), disk_spec, vdev]
        )
        if code == 0:
            return True, f"Disk attached as {vdev}"
        return False, stderr

    def detach_disk(self, name_or_id: str, vdev: str) -> Tuple[bool, str]:
        """Hot-detach a disk from VM."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        code, stdout, stderr = self.executor.run(["block-detach", str(vm.domid), vdev])
        if code == 0:
            return True, f"Disk {vdev} detached"
        return False, stderr

    def get_vm_metrics(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        """Get VM performance metrics."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return None

        metrics = {
            "domid": vm.domid,
            "name": vm.name,
            "cpu_time_ns": vm.cpu_time_ns,
            "vcpus": vm.vcpus,
            "memory_mb": vm.memory_mb,
            "state": vm.state.value,
        }

        # Get detailed CPU stats
        code, stdout, _ = self.executor.run(["vcpu-list", str(vm.domid)], check=False)
        if code == 0:
            vcpu_stats = []
            for line in stdout.strip().split("\n")[1:]:
                parts = line.split()
                if len(parts) >= 5:
                    vcpu_stats.append(
                        {
                            "vcpu": int(parts[1]),
                            "cpu": int(parts[2]) if parts[2] != "-" else -1,
                            "state": parts[3],
                            "time": float(parts[4]) if len(parts) > 4 else 0.0,
                        }
                    )
            metrics["vcpu_stats"] = vcpu_stats

        return metrics

    def get_scheduler_params(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        """Get scheduler parameters for VM."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return None

        code, stdout, _ = self.executor.run(
            ["sched-credit", "-d", str(vm.domid)], check=False
        )

        if code == 0:
        # Parse weight and cap
            params = {}
            for line in stdout.strip().split("\n"):
                if "weight" in line.lower():
                    match = re.search(r"weight\s*[:=]\s*(\d+)", line, re.I)
                    if match:
                        params["weight"] = int(match.group(1))
                if "cap" in line.lower():
                    match = re.search(r"cap\s*[:=]\s*(\d+)", line, re.I)
                    if match:
                        params["cap"] = int(match.group(1))
            return params
        return None

    def set_scheduler_params(
        self, name_or_id: str, weight: Optional[int] = None, cap: Optional[int] = None
    ) -> Tuple[bool, str]:
        """Set scheduler parameters for VM."""
        vm = self.get_vm(name_or_id)
        if not vm:
            return False, f"VM {name_or_id} not found"

        args = ["sched-credit", "-d", str(vm.domid)]
        if weight is not None:
            args.extend(["-w", str(weight)])
        if cap is not None:
            args.extend(["-c", str(cap)])

        code, stdout, stderr = self.executor.run(args)
        if code == 0:
            return True, "Scheduler params updated"
        return False, stderr


# -----------------------------------------------------------------------------
# Hypervisor Abstraction Layer
# -----------------------------------------------------------------------------


class HypervisorDriver(ABC):
    """Abstract hypervisor driver interface for multi-hypervisor support."""

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def get_host_info(self) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def list_vms(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def create_vm(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def destroy_vm(self, vm_id: str) -> Tuple[bool, str]:
        pass


class XenHypervisorDriver(HypervisorDriver):
    """Xen implementation of hypervisor abstraction."""

    def __init__(self) -> None:
        self.driver = XenDriver()

    def get_name(self) -> str:
        return "xen"

    def is_available(self) -> bool:
        return self.driver.available

    def get_host_info(self) -> Optional[Dict[str, Any]]:
        info = self.driver.get_host_info()
        if not info:
            return None
        return {
            "hypervisor": "xen",
            "version": info.xen_version,
            "total_memory_mb": info.total_memory_mb,
            "free_memory_mb": info.free_memory_mb,
            "total_cpus": info.total_cpus,
            "online_cpus": info.online_cpus,
            "capabilities": info.capabilities,
        }

    def list_vms(self) -> List[Dict[str, Any]]:
        return [vm.to_dict() for vm in self.driver.list_vms()]

    def create_vm(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        xen_config = XenVMConfig(
            name=config["name"],
            uuid=config.get("uuid"),
            vm_type=XenVMType(config.get("type", "hvm")),
            vcpus=config.get("vcpus", 1),
            memory_mb=config.get("memory_mb", 1024),
            disks=config.get("disks", []),
            vifs=config.get("vifs", []),
        )
        return self.driver.create_vm(xen_config)

    def destroy_vm(self, vm_id: str) -> Tuple[bool, str]:
        return self.driver.destroy_vm(vm_id)


# -----------------------------------------------------------------------------
# Example / CLI
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    driver = XenDriver()

    print("Xen Driver Status")
    print("=" * 40)

    if driver.available:
        print("Xen tools: Available")

        info = driver.get_host_info()
        if info:
            print("\nHost Information:")
            print(f"  Xen Version: {info.xen_version}")
            print(f"  Total Memory: {info.total_memory_mb} MB")
            print(f"  Free Memory: {info.free_memory_mb} MB")
            print(f"  CPUs: {info.online_cpus}/{info.total_cpus}")
            print(f"  Scheduler: {info.scheduler.value}")
            print(f"  Capabilities: {', '.join(info.virt_caps)}")

        vms = driver.list_vms()
        if vms:
            print(f"\nRunning VMs ({len(vms)}):")
            for vm in vms:
                print(
                    f"  - {vm.name} (domid={vm.domid}, state={vm.state.value}, "
                    f"vcpus={vm.vcpus}, mem={vm.memory_mb}MB)"
                )
        else:
            print("\nNo VMs running (excluding dom0)")

        # Demo: Generate a sample config
        print("\nSample HVM Config:")
        sample_config = XenVMConfig(
            name="test-hvm",
            vm_type=XenVMType.HVM,
            vcpus=2,
            memory_mb=2048,
            disks=[
                {
                    "target": "/dev/zvol/pool/test",
                    "vdev": "xvda",
                    "format": "phy",
                    "mode": "rw",
                }
            ],
            vifs=[{"bridge": "xenbr0"}],
            vnc=True,
        )
        print(XenConfigGenerator.generate(sample_config))
    else:
        print("Xen tools (xl): Not found")
        print("\nThis driver requires Xen hypervisor with xl toolstack.")
        print("Install with: apt install xen-tools xen-hypervisor-*")
