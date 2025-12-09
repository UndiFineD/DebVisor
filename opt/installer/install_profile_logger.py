#!/usr/bin/env python3
"""
DebVisor Install Profile Summary Logger

Logs installation profile information to /var/log/debvisor/install-profile.log
Captures system configuration, component selections, and deployment parameters
for audit, support, and reproducibility purposes.

Part of DebVisor Enterprise Platform.
"""

import json
import logging
import os
import platform
import socket
import subprocess
# from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
# from typing import Optional, Any
# from enum import Enum


# ==============================================================================
# Configuration
# ==============================================================================

LOG_DIR = Path("/var/log/debvisor")
LOG_FILE = LOG_DIR / "install-profile.log"
PROFILE_DIR = Path("/etc/debvisor/profiles")
STATE_FILE = Path("/var/lib/debvisor/install-state.json")


class InstallPhase(Enum):
    """Installation phases for tracking progress."""

    INIT = "initialization"
    HARDWARE_DETECTION = "hardware_detection"
    STORAGE_SETUP = "storage_setup"
    NETWORK_CONFIG = "network_configuration"
    SECURITY_HARDENING = "security_hardening"
    HYPERVISOR_INSTALL = "hypervisor_installation"
    CONTAINER_SETUP = "container_setup"
    CLUSTER_CONFIG = "cluster_configuration"
    SERVICE_DEPLOY = "service_deployment"
    VALIDATION = "validation"
    COMPLETE = "complete"
    FAILED = "failed"


class ComponentType(Enum):
    """Types of installable components."""

    HYPERVISOR = "hypervisor"
    STORAGE = "storage"
    NETWORK = "network"
    SECURITY = "security"
    MONITORING = "monitoring"
    BACKUP = "backup"
    CONTAINER = "container"
    ADDON = "addon"


# ==============================================================================
# Data Classes
# ==============================================================================


@dataclass
class HardwareProfile:
    """Detected hardware information."""

    cpu_model: str = ""
    cpu_cores: int = 0
    cpu_threads: int = 0
    memory_gb: float = 0.0
    storage_devices: list[Any] = field(default_factory=list[Any])
    network_interfaces: list[Any] = field(default_factory=list[Any])
    gpu_devices: list[Any] = field(default_factory=list[Any])
    virtualization_support: dict[str, Any] = field(default_factory=dict[str, Any])
    iommu_groups: int = 0
    numa_nodes: int = 0
    tpm_version: str = ""


@dataclass
class ComponentSelection:
    """Selected installation components."""

    name: str
    version: str
    component_type: str
    enabled: bool = True
    config: dict[str, Any] = field(default_factory=dict[str, Any])
    dependencies: list[Any] = field(default_factory=list[Any])


@dataclass
class NetworkConfig:
    """Network configuration profile."""

    hostname: str = ""
    domain: str = ""
    management_interface: str = ""
    management_ip: str = ""
    management_gateway: str = ""
    dns_servers: list[Any] = field(default_factory=list[Any])
    ntp_servers: list[Any] = field(default_factory=list[Any])
    vlans: list[Any] = field(default_factory=list[Any])
    bonds: list[Any] = field(default_factory=list[Any])
    bridges: list[Any] = field(default_factory=list[Any])


@dataclass
class StorageConfig:
    """Storage configuration profile."""

    root_device: str = ""
    root_filesystem: str = "ext4"
    boot_mode: str = "uefi"
    zfs_pools: list[Any] = field(default_factory=list[Any])
    ceph_osds: list[Any] = field(default_factory=list[Any])
    lvm_volumes: list[Any] = field(default_factory=list[Any])
    encryption_enabled: bool = False


@dataclass
class ClusterConfig:
    """Cluster configuration for multi-node deployments."""

    cluster_name: str = ""
    cluster_type: str = ""  # standalone, cluster, federation
    node_role: str = ""  # master, worker, hybrid
    master_nodes: list[Any] = field(default_factory=list[Any])
    worker_nodes: list[Any] = field(default_factory=list[Any])
    quorum_type: str = ""
    ha_enabled: bool = False


@dataclass
class InstallProfile:
    """Complete installation profile."""

    profile_id: str = ""
    profile_name: str = ""
    created_at: str = ""
    updated_at: str = ""
    install_phase: str = InstallPhase.INIT.value

    # System info
    debvisor_version: str = ""
    installer_version: str = ""
    install_method: str = ""  # iso, pxe, cloud-init, upgrade

    # Hardware
    hardware: HardwareProfile = field(default_factory=HardwareProfile)

    # Configuration
    network: NetworkConfig = field(default_factory=NetworkConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    cluster: ClusterConfig = field(default_factory=ClusterConfig)

    # Components
    components: list[Any] = field(default_factory=list[Any])

    # Security
    security_profile: str = "baseline"  # minimal, baseline, hardened, paranoid
    certificates_generated: bool = False

    # Validation
    validation_passed: bool = False
    validation_warnings: list[Any] = field(default_factory=list[Any])
    validation_errors: list[Any] = field(default_factory=list[Any])

    # Timing
    start_time: str = ""
    end_time: str = ""
    duration_seconds: float = 0.0

    # Metadata
    operator: str = ""
    notes: str = ""
    tags: list[Any] = field(default_factory=list[Any])


# ==============================================================================
# Profile Logger
# ==============================================================================


class InstallProfileLogger:
    """
    Manages installation profile logging and persistence.

    Provides structured logging of installation progress, configuration
    choices, and system state for audit and support purposes.
    """

    def __init__(self, profile_id: Optional[str] = None):
        """Initialize the profile logger."""
        self.profile_id = profile_id or self._generate_profile_id()
        self.profile = InstallProfile(
            profile_id=self.profile_id,
            created_at=datetime.now(timezone.utc).isoformat() + "Z",
            start_time=datetime.now(timezone.utc).isoformat() + "Z",
        )
        self._setup_logging()
        self._ensure_directories()

    def _generate_profile_id(self) -> str:
        """Generate unique profile ID."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        hostname = socket.gethostname()[:8]
        return f"debvisor-{hostname}-{timestamp}"

    def _setup_logging(self) -> None:
        """Configure logging handlers."""
        self.logger = logging.getLogger(f"debvisor.install.{self.profile_id}")
        self.logger.setLevel(logging.DEBUG)

        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        self.logger.addHandler(console)

        # File handler (if writable)
        try:
            self._ensure_directories()
            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
            )
            self.logger.addHandler(file_handler)
        except PermissionError:
            self.logger.warning(f"Cannot write to {LOG_FILE}, file logging disabled")

    def _ensure_directories(self) -> None:
        """Create required directories."""
        for directory in [LOG_DIR, PROFILE_DIR, STATE_FILE.parent]:
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                pass

    # --------------------------------------------------------------------------
    # Phase Management
    # --------------------------------------------------------------------------

    def set_phase(self, phase: InstallPhase, message: str = "") -> None:
        """Update installation phase."""
        old_phase = self.profile.install_phase
        self.profile.install_phase = phase.value
        self.profile.updated_at = datetime.now(timezone.utc).isoformat() + "Z"

        self.logger.info(f"Phase: {old_phase} -> {phase.value}")
        if message:
            self.logger.info(f"  {message}")

        self._save_state()
        self._log_profile_event(
            "phase_change",
            {"old_phase": old_phase, "new_phase": phase.value, "message": message},
        )

    def complete_installation(self, success: bool = True) -> None:
        """Mark installation as complete."""
        self.profile.end_time = datetime.now(timezone.utc).isoformat() + "Z"

        if self.profile.start_time:
            start = datetime.fromisoformat(self.profile.start_time.rstrip("Z"))
            end = datetime.fromisoformat(self.profile.end_time.rstrip("Z"))
            self.profile.duration_seconds = (end - start).total_seconds()

        if success:
            self.set_phase(InstallPhase.COMPLETE, "Installation completed successfully")
        else:
            self.set_phase(InstallPhase.FAILED, "Installation failed")

        self._save_profile()
        self._log_summary()

    # --------------------------------------------------------------------------
    # Hardware Detection
    # --------------------------------------------------------------------------

    def detect_hardware(self) -> HardwareProfile:
        """Detect and log hardware configuration."""
        self.set_phase(InstallPhase.HARDWARE_DETECTION, "Detecting hardware...")

        hw = HardwareProfile()

        # CPU info
        try:
            hw.cpu_model = self._get_cpu_model()
            hw.cpu_cores = os.cpu_count() or 0
            hw.cpu_threads = self._get_cpu_threads()
        except Exception as e:
            self.logger.warning(f"CPU detection error: {e}")

        # Memory
        try:
            hw.memory_gb = self._get_memory_gb()
        except Exception as e:
            self.logger.warning(f"Memory detection error: {e}")

        # Storage devices
        try:
            hw.storage_devices = self._detect_storage_devices()
        except Exception as e:
            self.logger.warning(f"Storage detection error: {e}")

        # Network interfaces
        try:
            hw.network_interfaces = self._detect_network_interfaces()
        except Exception as e:
            self.logger.warning(f"Network detection error: {e}")

        # GPU devices
        try:
            hw.gpu_devices = self._detect_gpu_devices()
        except Exception as e:
            self.logger.warning(f"GPU detection error: {e}")

        # Virtualization support
        hw.virtualization_support = self._check_virtualization()

        # IOMMU groups
        try:
            iommu_path = Path("/sys/kernel/iommu_groups")
            if iommu_path.exists():
                hw.iommu_groups = len(list(iommu_path.iterdir()))
        except Exception as e:
            self.logger.debug(f"IOMMU detection error: {e}")

        # NUMA nodes
        try:
            numa_path = Path("/sys/devices/system/node")
            if numa_path.exists():
                hw.numa_nodes = len(
                    [d for d in numa_path.iterdir() if d.name.startswith("node")]
                )
        except Exception as e:
            self.logger.debug(f"NUMA detection error: {e}")

        # TPM
        hw.tpm_version = self._detect_tpm()

        self.profile.hardware = hw
        self._log_profile_event("hardware_detected", asdict(hw))

        self.logger.info(
            f"Hardware: {hw.cpu_cores} cores, {hw.memory_gb:.1f}GB RAM, "
            f"{len(hw.storage_devices)} storage, {len(hw.network_interfaces)} NICs"
        )

        return hw

    def _get_cpu_model(self) -> str:
        """Get CPU model name."""
        if platform.system() == "Linux":
            try:
                with open("/proc/cpuinfo") as f:
                    for line in f:
                        if line.startswith("model name"):
                            return line.split(":")[1].strip()
            except Exception as e:
                self.logger.debug(f"CPU model detection error: {e}")
        return platform.processor() or "Unknown"

    def _get_cpu_threads(self) -> int:
        """Get total CPU threads."""
        try:
            if platform.system() == "Linux":
                result = subprocess.run(
                    ["nproc", "--all"], capture_output=True, text=True
                )  # nosec B603, B607 - Trusted system command for hardware detection
                if result.returncode == 0:
                    return int(result.stdout.strip())
        except Exception as e:
            self.logger.debug(f"CPU thread detection error: {e}")
        return os.cpu_count() or 0

    def _get_memory_gb(self) -> float:
        """Get total memory in GB."""
        if platform.system() == "Linux":
            try:
                with open("/proc/meminfo") as f:
                    for line in f:
                        if line.startswith("MemTotal"):
                            kb = int(line.split()[1])
                            return kb / (1024 * 1024)
            except Exception as e:
                self.logger.debug(f"Memory detection error: {e}")
        return 0.0

    def _detect_storage_devices(self) -> list[Any]:
        """Detect storage devices."""
        devices = []
        if platform.system() == "Linux":
            try:
                result = subprocess.run(
                    ["lsblk", "-J", "-d", "-o", "NAME,SIZE,TYPE,MODEL"],
                    capture_output=True,
                    text=True,
                )  # nosec B603, B607 - Trusted system command for hardware detection
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    for dev in data.get("blockdevices", []):
                        if dev.get("type") == "disk":
                            devices.append(
                                {
                                    "name": dev.get("name", ""),
                                    "size": dev.get("size", ""),
                                    "model": (
                                        dev.get("model", "").strip()
                                        if dev.get("model")
                                        else ""
                                    ),
                                }
                            )
            except Exception as e:
                self.logger.debug(f"Storage detection error: {e}")
        return devices

    def _detect_network_interfaces(self) -> list[Any]:
        """Detect network interfaces."""
        interfaces = []
        if platform.system() == "Linux":
            try:
                net_path = Path("/sys/class/net")
                for iface in net_path.iterdir():
                    if iface.name == "lo":
                        continue
                    info = {"name": iface.name}

                    # Get MAC address
                    addr_file = iface / "address"
                    if addr_file.exists():
                        info["mac"] = addr_file.read_text().strip()

                    # Get speed
                    speed_file = iface / "speed"
                    if speed_file.exists():
                        try:
                            info["speed_mbps"] = int(speed_file.read_text().strip())
                        except ValueError:
                            pass

                    # Check if virtual
                    info["virtual"] = (iface / "device").exists() is False

                    interfaces.append(info)
            except Exception as e:
                self.logger.debug(f"Network detection error: {e}")
        return interfaces

    def _detect_gpu_devices(self) -> list[Any]:
        """Detect GPU devices."""
        gpus = []
        if platform.system() == "Linux":
            try:
                result = subprocess.run(
                    ["lspci", "-mm"], capture_output=True, text=True
                )  # nosec B603, B607 - Trusted system command for hardware detection
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        if "VGA" in line or "3D" in line or "Display" in line:
                            parts = line.split('"')
                            if len(parts) >= 6:
                                gpus.append({"vendor": parts[3], "model": parts[5]})
            except Exception as e:
                self.logger.debug(f"GPU detection error: {e}")
        return gpus

    def _check_virtualization(self) -> dict[str, Any]:
        """Check virtualization support."""
        virt = {
            "vmx": False,
            "svm": False,
            "kvm_available": False,
            "nested_supported": False,
        }

        if platform.system() == "Linux":
            try:
                with open("/proc/cpuinfo") as f:
                    cpuinfo = f.read()
                    virt["vmx"] = "vmx" in cpuinfo
                    virt["svm"] = "svm" in cpuinfo

                virt["kvm_available"] = Path("/dev/kvm").exists()

                nested_path = Path("/sys/module/kvm_intel/parameters/nested")
                if not nested_path.exists():
                    nested_path = Path("/sys/module/kvm_amd/parameters/nested")
                if nested_path.exists():
                    virt["nested_supported"] = nested_path.read_text().strip() in (
                        "1",
                        "Y",
                    )
            except Exception as e:
                self.logger.debug(f"Virtualization check error: {e}")

        return virt

    def _detect_tpm(self) -> str:
        """Detect TPM version."""
        if platform.system() == "Linux":
            tpm2_path = Path("/sys/class/tpm/tpm0")
            if tpm2_path.exists():
                try:
                    caps = (tpm2_path / "caps").read_text()
                    if "TPM-2.0" in caps or "2.0" in caps:
                        return "2.0"
                    return "1.2"
                except Exception:
                    return "detected"
        return ""

    # --------------------------------------------------------------------------
    # Configuration Methods
    # --------------------------------------------------------------------------

    def set_network_config(self, config: NetworkConfig) -> None:
        """Set network configuration."""
        self.profile.network = config
        self._log_profile_event("network_configured", asdict(config))
        self.logger.info(
            f"Network: {config.hostname}.{config.domain} on {config.management_interface}"
        )

    def set_storage_config(self, config: StorageConfig) -> None:
        """Set storage configuration."""
        self.profile.storage = config
        self._log_profile_event("storage_configured", asdict(config))
        self.logger.info(
            f"Storage: {config.root_device} ({config.root_filesystem}), "
            f"ZFS pools: {len(config.zfs_pools)}, Ceph OSDs: {len(config.ceph_osds)}"
        )

    def set_cluster_config(self, config: ClusterConfig) -> None:
        """Set cluster configuration."""
        self.profile.cluster = config
        self._log_profile_event("cluster_configured", asdict(config))
        self.logger.info(
            f"Cluster: {config.cluster_name} ({config.cluster_type}), "
            f"Role: {config.node_role}, HA: {config.ha_enabled}"
        )

    def add_component(self, component: ComponentSelection) -> None:
        """Add a selected component."""
        self.profile.components.append(asdict(component))
        self._log_profile_event("component_added", asdict(component))
        self.logger.info(
            f"Component: {component.name} v{component.version} ({component.component_type})"
        )

    def set_security_profile(self, profile: str) -> None:
        """Set security hardening profile."""
        valid = ["minimal", "baseline", "hardened", "paranoid"]
        if profile not in valid:
            self.logger.warning(
                f"Invalid security profile: {profile}, using 'baseline'"
            )
            profile = "baseline"

        self.profile.security_profile = profile
        self._log_profile_event("security_profile_set", {"profile": profile})
        self.logger.info(f"Security profile: {profile}")

    def set_debvisor_version(self, version: str) -> None:
        """Set DebVisor version."""
        self.profile.debvisor_version = version

    def set_install_method(self, method: str) -> None:
        """Set installation method (iso, pxe, cloud-init, upgrade)."""
        self.profile.install_method = method

    def set_operator(self, operator: str) -> None:
        """Set operator/installer name."""
        self.profile.operator = operator

    def add_note(self, note: str) -> None:
        """Add note to profile."""
        if self.profile.notes:
            self.profile.notes += f"\n{note}"
        else:
            self.profile.notes = note

    def add_tag(self, tag: str) -> None:
        """Add tag to profile."""
        if tag not in self.profile.tags:
            self.profile.tags.append(tag)

    # --------------------------------------------------------------------------
    # Validation
    # --------------------------------------------------------------------------

    def add_validation_warning(self, warning: str) -> None:
        """Add validation warning."""
        self.profile.validation_warnings.append(warning)
        self.logger.warning(f"Validation: {warning}")

    def add_validation_error(self, error: str) -> None:
        """Add validation error."""
        self.profile.validation_errors.append(error)
        self.logger.error(f"Validation: {error}")

    def set_validation_result(self, passed: bool) -> None:
        """Set overall validation result."""
        self.profile.validation_passed = passed
        if passed:
            self.logger.info("Validation: PASSED")
        else:
            self.logger.error(
                f"Validation: FAILED ({len(self.profile.validation_errors)} errors)"
            )

    # --------------------------------------------------------------------------
    # Persistence
    # --------------------------------------------------------------------------

    def _save_state(self) -> None:
        """Save current state to state file."""
        try:
            state = {
                "profile_id": self.profile.profile_id,
                "phase": self.profile.install_phase,
                "updated_at": datetime.now(timezone.utc).isoformat() + "Z",
            }
            STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            STATE_FILE.write_text(json.dumps(state, indent=2))
        except PermissionError:
            pass

    def _save_profile(self) -> None:
        """Save complete profile to file."""
        try:
            profile_file = PROFILE_DIR / f"{self.profile_id}.json"
            PROFILE_DIR.mkdir(parents=True, exist_ok=True)
            profile_file.write_text(json.dumps(asdict(self.profile), indent=2))
            self.logger.info(f"Profile saved: {profile_file}")
        except PermissionError:
            self.logger.warning("Cannot save profile - permission denied")

    def _log_profile_event(self, event_type: str, data: dict[str, Any]) -> None:
        """Log profile event in structured format."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            "profile_id": self.profile_id,
            "event": event_type,
            "data": data,
        }
        self.logger.debug(json.dumps(event))

    def _log_summary(self) -> None:
        """Log installation summary."""
        summary = f"""
================================================================================
                        DEBVISOR INSTALLATION SUMMARY
================================================================================
Profile ID:       {self.profile.profile_id}
Profile Name:     {self.profile.profile_name or 'N/A'}
DebVisor Version: {self.profile.debvisor_version or 'N/A'}
Install Method:   {self.profile.install_method or 'N/A'}
Operator:         {self.profile.operator or 'N/A'}

HARDWARE
--------
CPU:              {self.profile.hardware.cpu_model}
Cores/Threads:    {self.profile.hardware.cpu_cores}/{self.profile.hardware.cpu_threads}
Memory:           {self.profile.hardware.memory_gb:.1f} GB
Storage Devices:  {len(self.profile.hardware.storage_devices)}
Network NICs:     {len(self.profile.hardware.network_interfaces)}
GPUs:             {len(self.profile.hardware.gpu_devices)}
IOMMU Groups:     {self.profile.hardware.iommu_groups}
NUMA Nodes:       {self.profile.hardware.numa_nodes}
TPM:              {self.profile.hardware.tpm_version or 'Not detected'}

NETWORK
-------
Hostname:         {self.profile.network.hostname}.{self.profile.network.domain}
Management:       {self.profile.network.management_interface} ({self.profile.network.management_ip})
DNS Servers:      {', '.join(self.profile.network.dns_servers) or 'N/A'}

STORAGE
-------
Root Device:      {self.profile.storage.root_device}
Filesystem:       {self.profile.storage.root_filesystem}
Boot Mode:        {self.profile.storage.boot_mode}
ZFS Pools:        {len(self.profile.storage.zfs_pools)}
Ceph OSDs:        {len(self.profile.storage.ceph_osds)}
Encryption:       {'Enabled' if self.profile.storage.encryption_enabled else 'Disabled'}

CLUSTER
-------
Name:             {self.profile.cluster.cluster_name or 'N/A'}
Type:             {self.profile.cluster.cluster_type or 'standalone'}
Role:             {self.profile.cluster.node_role or 'N/A'}
HA Enabled:       {self.profile.cluster.ha_enabled}

COMPONENTS ({len(self.profile.components)})
----------
"""
        for comp in self.profile.components:
            summary += (
                f"  - {comp['name']} v{comp['version']} ({comp['component_type']})\n"
            )

        summary += f"""
SECURITY
--------
Profile:          {self.profile.security_profile}
Certificates:     {'Generated' if self.profile.certificates_generated else 'Not generated'}

VALIDATION
----------
Result:           {'PASSED' if self.profile.validation_passed else 'FAILED'}
Warnings:         {len(self.profile.validation_warnings)}
Errors:           {len(self.profile.validation_errors)}

TIMING
------
Started:          {self.profile.start_time}
Completed:        {self.profile.end_time}
Duration:         {self.profile.duration_seconds:.1f} seconds

STATUS:           {self.profile.install_phase.upper()}
================================================================================
"""

        # Log to file
        self.logger.info(summary)

        # Also write summary to dedicated file
        try:
            summary_file = LOG_DIR / f"install-summary-{self.profile_id}.txt"
            summary_file.write_text(summary)
        except PermissionError:
            pass

    def export_profile(self, path: Optional[Path] = None) -> str:
        """Export profile as JSON."""
        data = json.dumps(asdict(self.profile), indent=2)
        if path:
            path.write_text(data)
            self.logger.info(f"Profile exported to: {path}")
        return data


# ==============================================================================
# CLI Interface
# ==============================================================================


def main() -> None:
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="DebVisor Install Profile Logger",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # new command
    new_parser = subparsers.add_parser("new", help="Start new installation profile")
    new_parser.add_argument("--name", help="Profile name")
    new_parser.add_argument(
        "--method",
        choices=["iso", "pxe", "cloud-init", "upgrade"],
        default="iso",
        help="Installation method",
    )
    new_parser.add_argument("--operator", help="Operator name")

    # detect command
    subparsers.add_parser("detect", help="Detect and log hardware")

    # status command
    subparsers.add_parser("status", help="Show current installation status")

    # export command
    export_parser = subparsers.add_parser("export", help="Export profile")
    export_parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    if args.command == "new":
        logger = InstallProfileLogger()
        if args.name:
            logger.profile.profile_name = args.name
        logger.set_install_method(args.method)
        if args.operator:
            logger.set_operator(args.operator)
        print(f"Created new profile: {logger.profile_id}")

    elif args.command == "detect":
        logger = InstallProfileLogger()
        hw = logger.detect_hardware()
        print(json.dumps(asdict(hw), indent=2))

    elif args.command == "status":
        if STATE_FILE.exists():
            state = json.loads(STATE_FILE.read_text())
            print(f"Profile:  {state.get('profile_id', 'Unknown')}")
            print(f"Phase:    {state.get('phase', 'Unknown')}")
            print(f"Updated:  {state.get('updated_at', 'Unknown')}")
        else:
            print("No active installation found")

    elif args.command == "export":
        if STATE_FILE.exists():
            state = json.loads(STATE_FILE.read_text())
            profile_file = PROFILE_DIR / f"{state['profile_id']}.json"
            if profile_file.exists():
                data = profile_file.read_text()
                if args.output:
                    Path(args.output).write_text(data)
                    print(f"Exported to: {args.output}")
                else:
                    print(data)
            else:
                print("Profile file not found")
        else:
            print("No active installation found")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
