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


"""
Xen Hypervisor Integration for DebVisor.

Provides multi-hypervisor support by extending the management plane
to work with Xen alongside KVM.

Features:
- Xen host capability detection
- VM lifecycle management (create, start, stop, migrate)
- Resource allocation and monitoring
- Live migration support
- Unified scheduling primitives
- Cross-hypervisor compatibility matrix
- Security isolation profiles

Author: DebVisor Team
Date: December 11, 2025
"""

import asyncio
import json
import logging
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


# =============================================================================
# Enums & Constants
# =============================================================================


class HypervisorType(Enum):
    """Supported hypervisor types."""
    KVM = "kvm"
    XEN = "xen"
    UNKNOWN = "unknown"


class VMState(Enum):
    """Virtual machine states."""
    RUNNING = "running"
    PAUSED = "paused"
    SHUTDOWN = "shutdown"
    CRASHED = "crashed"
    DYING = "dying"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class XenVMType(Enum):
    """Xen VM types."""
    PV = "pv"  # Paravirtualized
    HVM = "hvm"  # Hardware Virtual Machine
    PVH = "pvh"  # Paravirtualized Hardware


class MigrationCompatibility(Enum):
    """Migration compatibility between hypervisors."""
    COMPATIBLE = "compatible"
    REQUIRES_CONVERSION = "requires_conversion"
    INCOMPATIBLE = "incompatible"


# =============================================================================
# Data Models
# =============================================================================


@dataclass
class HypervisorCapabilities:
    """Hypervisor capabilities and features."""
    hypervisor_type: HypervisorType
    version: str
    host_cpus: int
    total_memory_mb: int
    free_memory_mb: int
    features: List[str] = field(default_factory=list)
    supported_vm_types: List[str] = field(default_factory=list)
    max_vcpus_per_vm: int = 0
    live_migration_supported: bool = False
    nested_virtualization: bool = False
    iommu_enabled: bool = False


@dataclass
class XenVM:
    """Xen virtual machine representation."""
    vm_id: str  # Domain ID
    name: str
    uuid: str
    vm_type: XenVMType
    state: VMState
    vcpus: int
    memory_mb: int
    max_memory_mb: int
    cpu_time_ns: int = 0
    uptime_seconds: int = 0
    autostart: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MigrationPlan:
    """Plan for VM migration between hypervisors."""
    source_hypervisor: HypervisorType
    target_hypervisor: HypervisorType
    vm_id: str
    compatibility: MigrationCompatibility
    conversion_steps: List[str] = field(default_factory=list)
    estimated_downtime_seconds: int = 0
    risks: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)


# =============================================================================
# Xen Host Manager
# =============================================================================


class XenHostManager:
    """
    Manages Xen hypervisor hosts and capabilities.
    """

    def __init__(self):
        self.xen_available = False
        self.capabilities: Optional[HypervisorCapabilities] = None
        self._check_xen_availability()

    def _check_xen_availability(self) -> None:
        """Check if Xen is available on the system."""
        try:
            # Check for xl command
            result = subprocess.run(
                ["xl", "info"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                self.xen_available = True
                logger.info("Xen hypervisor detected")
            else:
                logger.debug("Xen hypervisor not available")
        except FileNotFoundError:
            logger.debug("xl command not found - Xen not installed")
        except Exception as e:
            logger.debug(f"Error checking Xen availability: {e}")

    async def detect_capabilities(self) -> Optional[HypervisorCapabilities]:
        """Detect Xen hypervisor capabilities."""
        if not self.xen_available:
            logger.warning("Xen not available on this system")
            return None

        try:
            # Get Xen info
            result = subprocess.run(
                ["xl", "info"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                logger.error("Failed to get Xen info")
                return None

            # Parse xl info output
            info = self._parse_xl_info(result.stdout)

            capabilities = HypervisorCapabilities(
                hypervisor_type=HypervisorType.XEN,
                version=info.get("xen_version", "unknown"),
                host_cpus=int(info.get("nr_cpus", 0)),
                total_memory_mb=int(info.get("total_memory", 0)),
                free_memory_mb=int(info.get("free_memory", 0)),
                features=self._parse_xen_features(info),
                supported_vm_types=["pv", "hvm", "pvh"],
                max_vcpus_per_vm=int(info.get("max_cpu_id", 0)) + 1,
                live_migration_supported=True,
                nested_virtualization=self._check_nested_virt(info),
                iommu_enabled=self._check_iommu(info),
            )

            self.capabilities = capabilities
            logger.info(
                f"Detected Xen {capabilities.version} with "
                f"{capabilities.host_cpus} CPUs, "
                f"{capabilities.total_memory_mb}MB RAM"
            )

            return capabilities

        except Exception as e:
            logger.error(f"Error detecting Xen capabilities: {e}")
            return None

    def _parse_xl_info(self, output: str) -> Dict[str, str]:
        """Parse xl info output."""
        info = {}

        for line in output.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                info[key.strip().lower().replace(" ", "_")] = value.strip()

        return info

    def _parse_xen_features(self, info: Dict[str, str]) -> List[str]:
        """Parse Xen features from info."""
        features = []

        # Check for common features
        if "hvm" in info.get("xen_caps", "").lower():
            features.append("hvm")
        if "pv" in info.get("xen_caps", "").lower():
            features.append("pv")
        if "shadow" in info.get("xen_caps", "").lower():
            features.append("shadow_paging")

        return features

    def _check_nested_virt(self, info: Dict[str, str]) -> bool:
        """Check if nested virtualization is enabled."""
        # Check virt_caps or similar
        virt_caps = info.get("virt_caps", "")
        return "hvm_directio" in virt_caps or "nested" in virt_caps

    def _check_iommu(self, info: Dict[str, str]) -> bool:
        """Check if IOMMU is enabled."""
        return "iommu" in info.get("xen_caps", "").lower()


# =============================================================================
# Xen VM Manager
# =============================================================================


class XenVMManager:
    """
    Manages Xen virtual machines.
    """

    def __init__(self, host_manager: XenHostManager):
        self.host = host_manager

    async def list_vms(self) -> List[XenVM]:
        """List all Xen VMs."""
        if not self.host.xen_available:
            return []

        try:
            result = subprocess.run(
                ["xl", "list"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                logger.error("Failed to list Xen VMs")
                return []

            return self._parse_xl_list(result.stdout)

        except Exception as e:
            logger.error(f"Error listing Xen VMs: {e}")
            return []

    def _parse_xl_list(self, output: str) -> List[XenVM]:
        """Parse xl list output."""
        vms = []
        lines = output.strip().split("\n")

        # Skip header line
        if len(lines) < 2:
            return vms

        for line in lines[1:]:
            parts = line.split()
            if len(parts) < 6:
                continue

            try:
                vm = XenVM(
                    vm_id=parts[1],
                    name=parts[0],
                    uuid="",  # Need to get from xl domid
                    vm_type=XenVMType.HVM,  # Default, need to query
                    state=self._parse_state(parts[4]),
                    vcpus=int(parts[3]),
                    memory_mb=int(parts[2]),
                    max_memory_mb=int(parts[2]),
                    cpu_time_ns=int(float(parts[5]) * 1e9) if len(parts) > 5 else 0,
                )
                vms.append(vm)
            except (ValueError, IndexError) as e:
                logger.warning(f"Error parsing VM line: {line} - {e}")

        return vms

    def _parse_state(self, state_str: str) -> VMState:
        """Parse VM state string."""
        state_map = {
            "r": VMState.RUNNING,
            "b": VMState.BLOCKED,
            "p": VMState.PAUSED,
            "s": VMState.SHUTDOWN,
            "c": VMState.CRASHED,
            "d": VMState.DYING,
        }

        # State string can be like "r-----" or "-b----"
        for char, state in state_map.items():
            if char in state_str.lower():
                return state

        return VMState.UNKNOWN

    async def create_vm(
        self,
        name: str,
        vcpus: int,
        memory_mb: int,
        vm_type: XenVMType = XenVMType.HVM,
        disk_path: Optional[str] = None,
        network_config: Optional[Dict[str, Any]] = None,
        vnc_config: Optional[Dict[str, Any]] = None
    ) -> Optional[XenVM]:
        """Create a new Xen VM.

        Args:
            name: VM name
            vcpus: Number of virtual CPUs
            memory_mb: Memory in MB
            vm_type: Xen VM type (HVM, PV, or PVH)
            disk_path: Path to disk image
            network_config: Network configuration dict
            vnc_config: VNC configuration dict with optional keys:
                - bind_address: VNC listen address (default: 127.0.0.1)
                - password_file: Path to VNC password file
                - auth_enabled: Enable VNC authentication (default: False)

        Returns:
            XenVM instance or None on failure
        """
        if not self.host.xen_available:
            logger.error("Xen not available")
            return None

        # Sanitize VM name to prevent path traversal
        sanitized_name = re.sub(r'[^A-Za-z0-9_.-]', '', name)
        if not sanitized_name:
            logger.error(f"Invalid VM name after sanitization: {name}")
            return None

        # Use sanitized name for VM operations
        config_content = self._generate_vm_config(
            sanitized_name, vcpus, memory_mb, vm_type, disk_path, network_config, vnc_config
        )

        temp_config_fd = None
        temp_config_path = None

        try:
            # Create secure temporary file with restrictive permissions (0600)
            temp_config_fd, temp_config_path = tempfile.mkstemp(
                suffix=".cfg",
                prefix="xen-config-",
                text=True
            )

            # Set restrictive permissions (owner read/write only)
            os.chmod(temp_config_path, 0o600)

            # Write config to temporary file
            with os.fdopen(temp_config_fd, 'w') as f:
                f.write(config_content)
                temp_config_fd = None  # Mark as closed

            # Create VM using temporary config
            result = subprocess.run(
                ["xl", "create", temp_config_path],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                logger.error(f"Failed to create VM: {result.stderr}")
                return None

            logger.info(f"Created Xen VM: {sanitized_name}")

            # Get VM info
            vms = await self.list_vms()
            for vm in vms:
                if vm.name == sanitized_name:
                    return vm

            return None

        except Exception as e:
            logger.error(f"Error creating Xen VM: {e}")
            return None

        finally:
            # Always cleanup: close fd if still open and remove temp file
            if temp_config_fd is not None:
                try:
                    os.close(temp_config_fd)
                except Exception:
                    pass

            if temp_config_path and os.path.exists(temp_config_path):
                try:
                    os.unlink(temp_config_path)
                    logger.debug(f"Cleaned up temporary config file: {temp_config_path}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup temp config: {e}")

    def _generate_vm_config(
        self,
        name: str,
        vcpus: int,
        memory_mb: int,
        vm_type: XenVMType,
        disk_path: Optional[str],
        network_config: Optional[Dict[str, Any]],
        vnc_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate Xen VM configuration.

        Args:
            vnc_config: Optional VNC configuration with bind_address, password_file, auth_enabled
        """
        config = f"""# Xen VM Configuration for {name}
name = "{name}"
type = "{vm_type.value}"
vcpus = {vcpus}
memory = {memory_mb}
maxmem = {memory_mb}

# Boot
on_poweroff = "destroy"
on_reboot = "restart"
on_crash = "restart"
"""

        # Add disk configuration
        if disk_path:
            config += f'\ndisk = [ "file:{disk_path},xvda,w" ]'

        # Add network configuration
        if network_config:
            bridge = network_config.get("bridge", "xenbr0")
            config += f'\nvif = [ "bridge={bridge}" ]'
        else:
            config += '\nvif = [ "bridge=xenbr0" ]'

        # HVM-specific settings
        if vm_type == XenVMType.HVM:
            # VNC configuration with secure defaults
            vnc_bind = "127.0.0.1"  # Default: localhost only
            vnc_auth = ""

            if vnc_config:
                # Validate and extract bind address
                bind_address = vnc_config.get("bind_address", "127.0.0.1")
                # Basic validation: ensure it's a valid-looking IP or hostname
                if bind_address and all(c.isalnum() or c in ".-:" for c in bind_address):
                    vnc_bind = bind_address
                else:
                    logger.warning(f"Invalid VNC bind address, using default: 127.0.0.1")

                # Add VNC authentication if enabled
                if vnc_config.get("auth_enabled"):
                    password_file = vnc_config.get("password_file", "")
                    if password_file and all(c.isalnum() or c in "/_.-" for c in password_file):
                        vnc_auth = f'\nvncpasswd = "{password_file}"'
                    else:
                        logger.warning("VNC auth enabled but no valid password_file provided")

            config += f"""

# HVM settings
builder = "hvm"
boot = "c"
vnc = 1
vnclisten = "{vnc_bind}"{vnc_auth}
"""

        return config

    async def start_vm(self, vm_id: str) -> bool:
        """Start a Xen VM."""
        try:
            result = subprocess.run(
                ["xl", "unpause", vm_id],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                logger.info(f"Started Xen VM: {vm_id}")
                return True
            else:
                logger.error(f"Failed to start VM {vm_id}: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error starting VM {vm_id}: {e}")
            return False

    async def stop_vm(self, vm_id: str, force: bool = False) -> bool:
        """Stop a Xen VM."""
        try:
            command = ["xl", "destroy" if force else "shutdown", vm_id]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                logger.info(f"Stopped Xen VM: {vm_id}")
                return True
            else:
                logger.error(f"Failed to stop VM {vm_id}: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error stopping VM {vm_id}: {e}")
            return False

    async def migrate_vm(
        self,
        vm_id: str,
        target_host: str,
        live: bool = True
    ) -> bool:
        """Migrate a Xen VM to another host."""
        try:
            command = ["xl", "migrate"]
            if live:
                command.append("--live")
            command.extend([vm_id, target_host])

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes for migration
            )

            if result.returncode == 0:
                logger.info(f"Migrated VM {vm_id} to {target_host}")
                return True
            else:
                logger.error(f"Failed to migrate VM {vm_id}: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error migrating VM {vm_id}: {e}")
            return False


# =============================================================================
# Multi-Hypervisor Scheduler
# =============================================================================


class MultiHypervisorScheduler:
    """
    Unified scheduler for KVM and Xen hypervisors.
    """

    def __init__(self):
        self.xen_manager = XenVMManager(XenHostManager())
        self.hypervisors: Dict[str, HypervisorCapabilities] = {}

    async def discover_hypervisors(self) -> Dict[str, HypervisorCapabilities]:
        """Discover available hypervisors on the system."""
        discovered = {}

        # Check Xen
        xen_caps = await self.xen_manager.host.detect_capabilities()
        if xen_caps:
            discovered["xen"] = xen_caps

        # Check KVM (simplified - would use libvirt in production)
        if Path("/dev/kvm").exists():
            # Mock KVM capabilities
            discovered["kvm"] = HypervisorCapabilities(
                hypervisor_type=HypervisorType.KVM,
                version="QEMU 8.0",
                host_cpus=8,
                total_memory_mb=32768,
                free_memory_mb=16384,
                features=["kvm", "nested", "iommu"],
                supported_vm_types=["qemu", "kvm"],
                max_vcpus_per_vm=288,
                live_migration_supported=True,
                nested_virtualization=True,
                iommu_enabled=True,
            )

        self.hypervisors = discovered
        return discovered

    def select_hypervisor(
        self,
        vm_requirements: Dict[str, Any]
    ) -> Optional[HypervisorType]:
        """Select best hypervisor for VM requirements."""
        if not self.hypervisors:
            return None

        # Simple selection logic
        required_vcpus = vm_requirements.get("vcpus", 1)
        required_memory = vm_requirements.get("memory_mb", 1024)
        vm_type = vm_requirements.get("type", "kvm")

        # Check each hypervisor
        for hv_type, caps in self.hypervisors.items():
            # Check capacity
            if caps.free_memory_mb < required_memory:
                continue

            if required_vcpus > caps.max_vcpus_per_vm:
                continue

            # Prefer native VM type
            if vm_type.lower() in [vt.lower() for vt in caps.supported_vm_types]:
                return caps.hypervisor_type

        # Return first available
        if self.hypervisors:
            return list(self.hypervisors.values())[0].hypervisor_type

        return None

    def assess_migration_compatibility(
        self,
        source: HypervisorType,
        target: HypervisorType,
        vm_id: str
    ) -> MigrationPlan:
        """Assess migration compatibility between hypervisors."""
        plan = MigrationPlan(
            source_hypervisor=source,
            target_hypervisor=target,
            vm_id=vm_id,
            compatibility=MigrationCompatibility.INCOMPATIBLE,
        )

        # Same hypervisor - fully compatible
        if source == target:
            plan.compatibility = MigrationCompatibility.COMPATIBLE
            plan.estimated_downtime_seconds = 2
            plan.conversion_steps = ["Live migration via native protocol"]
            return plan

        # KVM to Xen or vice versa
        if (source == HypervisorType.KVM and target == HypervisorType.XEN) or \
           (source == HypervisorType.XEN and target == HypervisorType.KVM):
            plan.compatibility = MigrationCompatibility.REQUIRES_CONVERSION
            plan.estimated_downtime_seconds = 300  # 5 minutes
            plan.conversion_steps = [
                "Stop source VM",
                "Export disk image",
                "Convert disk format (qcow2 <-> raw)",
                "Generate target hypervisor config",
                "Import and start on target",
            ]
            plan.risks = [
                "Requires VM downtime",
                "Disk format conversion may fail",
                "Driver compatibility issues possible",
            ]
            plan.prerequisites = [
                "Sufficient storage on target",
                "Compatible CPU architecture",
                "Network connectivity",
            ]
            return plan

        return plan


# =============================================================================
# Example Usage
# =============================================================================


async def main():
    """Example usage of Xen integration."""
    print("=== Xen Hypervisor Integration ===\n")

    # Initialize managers
    xen_host = XenHostManager()

    if not xen_host.xen_available:
        print("⚠️  Xen hypervisor not available on this system")
        print("   To use Xen features, install: xen-hypervisor xen-utils")
        return

    # Detect capabilities
    print("Detecting Xen capabilities...")
    caps = await xen_host.detect_capabilities()

    if caps:
        print(f"\n✓ Xen {caps.version} detected")
        print(f"  CPUs: {caps.host_cpus}")
        print(f"  Memory: {caps.total_memory_mb} MB (Free: {caps.free_memory_mb} MB)")
        print(f"  Features: {', '.join(caps.features)}")
        print(f"  Supported VM types: {', '.join(caps.supported_vm_types)}")
        print(f"  Live migration: {'Yes' if caps.live_migration_supported else 'No'}")
        print(f"  IOMMU: {'Enabled' if caps.iommu_enabled else 'Disabled'}")

    # List VMs
    vm_manager = XenVMManager(xen_host)
    print("\n\nListing Xen VMs...")
    vms = await vm_manager.list_vms()

    if vms:
        print(f"\nFound {len(vms)} VMs:")
        for vm in vms:
            print(f"  {vm.name} ({vm.vm_id})")
            print(f"    State: {vm.state.value}")
            print(f"    vCPUs: {vm.vcpus}, Memory: {vm.memory_mb} MB")
    else:
        print("\nNo VMs found")

    # Multi-hypervisor scheduler
    print("\n\nTesting multi-hypervisor scheduler...")
    scheduler = MultiHypervisorScheduler()
    discovered = await scheduler.discover_hypervisors()

    print(f"\nDiscovered {len(discovered)} hypervisor(s):")
    for name, hv_caps in discovered.items():
        print(f"  {name.upper()}: {hv_caps.hypervisor_type.value}")

    # Test migration compatibility
    if len(discovered) >= 2:
        source = list(discovered.values())[0].hypervisor_type
        target = list(discovered.values())[1].hypervisor_type

        print(f"\n\nMigration compatibility: {source.value} → {target.value}")
        plan = scheduler.assess_migration_compatibility(source, target, "test-vm")
        print(f"  Compatibility: {plan.compatibility.value}")
        print(f"  Estimated downtime: {plan.estimated_downtime_seconds}s")
        if plan.conversion_steps:
            print(f"  Steps:")
            for step in plan.conversion_steps:
                print(f"    - {step}")


if __name__ == "__main__":
    asyncio.run(main())
