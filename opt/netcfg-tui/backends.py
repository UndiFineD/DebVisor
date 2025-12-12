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


"""
Enhanced Network Configuration Backend Support
==============================================

Provides multiple backend implementations for network configuration:
- iproute2 backend (Linux standard)
- NetworkManager (nmcli) backend
- Pluggable architecture for custom backends
"""

import re
import subprocess
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


###############################################################################
# Data Classes & Enums
###############################################################################


class AddressFamily(Enum):
    """IP address family"""

    IPV4 = "inet"
    IPV6 = "inet6"
    BOTH = "both"


class InterfaceState(Enum):
    """Interface state"""

    UP = "UP"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"


@dataclass
class IPAddress:
    """IP address configuration"""

    address: str
    prefix_len: int
    gateway: Optional[str] = None
    family: AddressFamily = AddressFamily.IPV4

    def to_cidr(self) -> str:
        """Convert to CIDR notation"""
        return f"{self.address}/{self.prefix_len}"

    @classmethod
    def from_cidr(cls, cidr: str) -> "IPAddress":
        """Create from CIDR notation"""
        parts = cidr.split("/")
        if len(parts) != 2:
            raise ValueError(f"Invalid CIDR: {cidr}")
        return cls(address=parts[0], prefix_len=int(parts[1]))


@dataclass
class InterfaceConfig:
    """Network interface configuration"""

    name: str
    state: InterfaceState = InterfaceState.DOWN
    mtu: int = 1500
    addresses: Optional[List[IPAddress]] = None
    dns_servers: Optional[List[str]] = None
    domain_search: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.addresses is None:
            self.addresses = []
        if self.dns_servers is None:
            self.dns_servers = []
        if self.domain_search is None:
            self.domain_search = []


@dataclass
class BondConfig:
    """Bond configuration"""

    name: str
    mode: str
    slaves: List[str]
    mii_monitor: int = 100
    ad_select: str = "stable"


@dataclass
class VLANConfig:
    """VLAN configuration"""

    name: str
    parent: str
    vlan_id: int
    protocol: str = "802.1q"
    mtu: int = 1500


###############################################################################
# Abstract Backend Interface
###############################################################################


class NetworkBackend(ABC):
    """Abstract base class for network backends"""

    def __init__(self, name: str):
        """Initialize backend"""
        self.name = name
        self.is_available = self._check_availability()
        logger.info(f"{name} backend initialized (available: {self.is_available})")

    @abstractmethod
    def _check_availability(self) -> bool:
        """Check if backend is available on system"""
        pass

    @abstractmethod
    def get_interface(self, name: str) -> Optional[InterfaceConfig]:
        """Get interface configuration"""
        pass

    @abstractmethod
    def set_interface_up(self, name: str) -> bool:
        """Bring interface up"""
        pass

    @abstractmethod
    def set_interface_down(self, name: str) -> bool:
        """Bring interface down"""
        pass

    @abstractmethod
    def add_ip_address(self, name: str, address: IPAddress) -> bool:
        """Add IP address to interface"""
        pass

    @abstractmethod
    def remove_ip_address(self, name: str, address: IPAddress) -> bool:
        """Remove IP address from interface"""
        pass

    @abstractmethod
    def set_mtu(self, name: str, mtu: int) -> bool:
        """Set interface MTU"""
        pass

    @abstractmethod
    def create_bond(self, config: BondConfig) -> bool:
        """Create bond interface"""
        pass

    @abstractmethod
    def create_vlan(self, config: VLANConfig) -> bool:
        """Create VLAN interface"""
        pass

    @abstractmethod
    def delete_interface(self, name: str) -> bool:
        """Delete interface"""
        pass

    def execute_command(
        self, cmd: List[str], check: bool = True
    ) -> Tuple[int, str, str]:
        """Execute shell command"""
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=check
            )    # nosec B603
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(cmd)}: {e.stderr}")
            return e.returncode, e.stdout, e.stderr


###############################################################################
# iproute2 Backend Implementation
###############################################################################


class Iproute2Backend(NetworkBackend):
    """iproute2 (ip command) network backend"""

    def __init__(self) -> None:
        """Initialize iproute2 backend"""
        super().__init__("iproute2")

    def _check_availability(self) -> bool:
        """Check if iproute2 is available"""
        rc, _, _ = self.execute_command(["which", "ip"], check=False)
        return rc == 0

    def get_interface(self, name: str) -> Optional[InterfaceConfig]:
        """Get interface configuration using 'ip addr'"""
        rc, output, _ = self.execute_command(["ip", "link", "show", name], check=False)

        if rc != 0:
            logger.warning(f"Interface not found: {name}")
            return None

        # Parse output
        config = InterfaceConfig(name=name)

        # Extract state
        if "UP" in output:
            config.state = InterfaceState.UP
        else:
            config.state = InterfaceState.DOWN

        # Extract MTU
        mtu_match = re.search(r"mtu\s+(\d+)", output)
        if mtu_match:
            config.mtu = int(mtu_match.group(1))

        # Get addresses
        rc, addr_output, _ = self.execute_command(
            ["ip", "addr", "show", name], check=False
        )
        if rc == 0:
            for line in addr_output.split("\n"):
                if "inet" in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        cidr = parts[1]
                        config.addresses.append(IPAddress.from_cidr(cidr))  # type: ignore[union-attr]

        logger.debug(f"Interface retrieved: {name}")
        return config

    def set_interface_up(self, name: str) -> bool:
        """Bring interface up"""
        rc, _, err = self.execute_command(
            ["ip", "link", "set", name, "up"], check=False
        )
        if rc != 0:
            logger.error(f"Failed to set interface up: {name}: {err}")
            return False
        logger.info(f"Interface up: {name}")
        return True

    def set_interface_down(self, name: str) -> bool:
        """Bring interface down"""
        rc, _, err = self.execute_command(
            ["ip", "link", "set", name, "down"], check=False
        )
        if rc != 0:
            logger.error(f"Failed to set interface down: {name}: {err}")
            return False
        logger.info(f"Interface down: {name}")
        return True

    def add_ip_address(self, name: str, address: IPAddress) -> bool:
        """Add IP address using 'ip addr add'"""
        cmd = ["ip", "addr", "add", address.to_cidr(), "dev", name]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to add address: {err}")
            return False
        logger.info(f"Address added: {name} -> {address.to_cidr()}")
        return True

    def remove_ip_address(self, name: str, address: IPAddress) -> bool:
        """Remove IP address using 'ip addr del'"""
        cmd = ["ip", "addr", "del", address.to_cidr(), "dev", name]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to remove address: {err}")
            return False
        logger.info(f"Address removed: {name} -> {address.to_cidr()}")
        return True

    def set_mtu(self, name: str, mtu: int) -> bool:
        """Set interface MTU"""
        cmd = ["ip", "link", "set", name, "mtu", str(mtu)]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to set MTU: {err}")
            return False
        logger.info(f"MTU set: {name} -> {mtu}")
        return True

    def create_bond(self, config: BondConfig) -> bool:
        """Create bond interface"""
        # Create bond
        cmd = ["ip", "link", "add", config.name, "type", "bond", "mode", config.mode]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to create bond: {err}")
            return False

        # Add slaves
        for slave in config.slaves:
            slave_cmd = ["ip", "link", "set", slave, "master", config.name]
            rc, _, err = self.execute_command(slave_cmd, check=False)
            if rc != 0:
                logger.error(f"Failed to add slave: {err}")
                return False

        # Bring up bond
        self.set_interface_up(config.name)

        logger.info(f"Bond created: {config.name} with slaves {config.slaves}")
        return True

    def create_vlan(self, config: VLANConfig) -> bool:
        """Create VLAN interface"""
        cmd = [
            "ip",
            "link",
            "add",
            "link",
            config.parent,
            "name",
            config.name,
            "type",
            "vlan",
            "id",
            str(config.vlan_id),
        ]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to create VLAN: {err}")
            return False

        # Set MTU if needed
        if config.mtu != 1500:
            self.set_mtu(config.name, config.mtu)

        # Bring up VLAN
        self.set_interface_up(config.name)

        logger.info(f"VLAN created: {config.name} on {config.parent}:{config.vlan_id}")
        return True

    def delete_interface(self, name: str) -> bool:
        """Delete interface"""
        cmd = ["ip", "link", "del", name]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to delete interface: {err}")
            return False
        logger.info(f"Interface deleted: {name}")
        return True


###############################################################################
# NetworkManager (nmcli) Backend Implementation
###############################################################################


class NetworkManagerBackend(NetworkBackend):
    """NetworkManager (nmcli) backend"""

    def __init__(self) -> None:
        """Initialize NetworkManager backend"""
        super().__init__("NetworkManager")

    def _check_availability(self) -> bool:
        """Check if NetworkManager and nmcli are available"""
        rc, _, _ = self.execute_command(["which", "nmcli"], check=False)
        return rc == 0

    def get_interface(self, name: str) -> Optional[InterfaceConfig]:
        """Get interface configuration using nmcli"""
        rc, output, _ = self.execute_command(
            ["nmcli", "device", "show", name], check=False
        )

        if rc != 0:
            logger.warning(f"Interface not found: {name}")
            return None

        config = InterfaceConfig(name=name)

        # Parse output
        for line in output.split("\n"):
            if line.startswith("GENERAL.CONNECTION:"):
            # Connection is active
                config.state = InterfaceState.UP
            elif line.startswith("GENERAL.STATE:"):
                if "connected" in line.lower():
                    config.state = InterfaceState.UP
                else:
                    config.state = InterfaceState.DOWN
            elif line.startswith("WIRED-PROPERTIES.MTU:"):
                parts = line.split(":")
                if len(parts) > 1:
                    config.mtu = int(parts[1].strip())
            elif line.startswith("IP4.ADDRESS"):
                parts = line.split(":")
                if len(parts) > 1:
                    address_str = parts[1].strip()
                    if address_str:
                        config.addresses.append(IPAddress.from_cidr(address_str))  # type: ignore[union-attr]
            elif line.startswith("IP4.DNS"):
                parts = line.split(":")
                if len(parts) > 1:
                    dns = parts[1].strip()
                    if dns:
                        config.dns_servers.append(dns)  # type: ignore[union-attr]

        logger.debug(f"Interface retrieved via nmcli: {name}")
        return config

    def set_interface_up(self, name: str) -> bool:
        """Bring interface up using nmcli"""
        rc, _, err = self.execute_command(
            ["nmcli", "device", "connect", name], check=False
        )
        if rc != 0:
            logger.error(f"Failed to set interface up: {err}")
            return False
        logger.info(f"Interface up (via nmcli): {name}")
        return True

    def set_interface_down(self, name: str) -> bool:
        """Bring interface down using nmcli"""
        rc, _, err = self.execute_command(
            ["nmcli", "device", "disconnect", name], check=False
        )
        if rc != 0:
            logger.error(f"Failed to set interface down: {err}")
            return False
        logger.info(f"Interface down (via nmcli): {name}")
        return True

    def add_ip_address(self, name: str, address: IPAddress) -> bool:
        """Add IP address using nmcli connection modify"""
        # This is more complex with nmcli - requires connection modification
        cmd = [
            "nmcli",
            "connection",
            "modify",
            name,
            "+ipv4.addresses",
            address.to_cidr(),
            "ipv4.method",
            "manual",
        ]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to add address via nmcli: {err}")
            return False

        # Reactivate connection
        self.execute_command(["nmcli", "connection", "up", name], check=False)

        logger.info(f"Address added via nmcli: {name} -> {address.to_cidr()}")
        return True

    def remove_ip_address(self, name: str, address: IPAddress) -> bool:
        """Remove IP address using nmcli"""
        cmd = [
            "nmcli",
            "connection",
            "modify",
            name,
            "-ipv4.addresses",
            address.to_cidr(),
        ]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to remove address via nmcli: {err}")
            return False

        logger.info(f"Address removed via nmcli: {name} -> {address.to_cidr()}")
        return True

    def set_mtu(self, name: str, mtu: int) -> bool:
        """Set MTU via nmcli"""
        cmd = ["nmcli", "connection", "modify", name, "ethernet.mtu", str(mtu)]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to set MTU via nmcli: {err}")
            return False

        logger.info(f"MTU set via nmcli: {name} -> {mtu}")
        return True

    def create_bond(self, config: BondConfig) -> bool:
        """Create bond via nmcli"""
        # Create connection
        cmd = [
            "nmcli",
            "connection",
            "add",
            "type",
            "bond",
            "ifname",
            config.name,
            "con-name",
            config.name,
            "bond.options",
            f"mode={config.mode}",
        ]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to create bond via nmcli: {err}")
            return False

        # Add slaves
        for slave in config.slaves:
            slave_cmd = [
                "nmcli",
                "connection",
                "add",
                "type",
                "ethernet",
                "ifname",
                slave,
                "master",
                config.name,
                "slave-type",
                "bond",
            ]
            rc, _, err = self.execute_command(slave_cmd, check=False)
            if rc != 0:
                logger.error(f"Failed to add slave via nmcli: {err}")
                return False

        logger.info(f"Bond created via nmcli: {config.name}")
        return True

    def create_vlan(self, config: VLANConfig) -> bool:
        """Create VLAN via nmcli"""
        cmd = [
            "nmcli",
            "connection",
            "add",
            "type",
            "vlan",
            "ifname",
            config.name,
            "con-name",
            config.name,
            "dev",
            config.parent,
            "id",
            str(config.vlan_id),
        ]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to create VLAN via nmcli: {err}")
            return False

        logger.info(f"VLAN created via nmcli: {config.name}")
        return True

    def delete_interface(self, name: str) -> bool:
        """Delete interface via nmcli"""
        cmd = ["nmcli", "connection", "delete", name]
        rc, _, err = self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to delete interface via nmcli: {err}")
            return False

        logger.info(f"Interface deleted via nmcli: {name}")
        return True


###############################################################################
# Backend Factory
###############################################################################


class NetworkBackendFactory:
    """Factory for creating network backends"""

    _backends: Dict[str, type] = {
        "iproute2": Iproute2Backend,
        "nmcli": NetworkManagerBackend,
    }

    @classmethod
    def create_backend(cls, backend_name: Optional[str] = None) -> NetworkBackend:
        """Create backend instance"""
        if backend_name and backend_name in cls._backends:
            backend = cls._backends[backend_name]()
            if backend.is_available:
                return backend
            logger.warning(f"Backend {backend_name} not available on system")

        # Try backends in order of preference
        for name in ["iproute2", "nmcli"]:
            backend = cls._backends[name]()
            if backend.is_available:
                logger.info(f"Using {name} backend")
                return backend

        raise RuntimeError("No supported network backend available")

    @classmethod
    def register_backend(cls, name: str, backend_class: type) -> None:
        """Register custom backend"""
        cls._backends[name] = backend_class
        logger.info(f"Backend registered: {name}")


###############################################################################
# Example Usage
###############################################################################

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Create backend
    factory = NetworkBackendFactory()
    backend = factory.create_backend()

    print(f"Using backend: {backend.name}")

    # Get interface
    if_config = backend.get_interface("eth0")
    if if_config:
        print(f"Interface: {if_config.name}, State: {if_config.state.value}")

    # Add IP address
    new_addr = IPAddress(address="192.168.1.100", prefix_len=24)
    result = backend.add_ip_address("eth0", new_addr)
    print(f"Address added: {result}")

    # Create VLAN
    vlan_config = VLANConfig(name="eth0.100", parent="eth0", vlan_id=100)
    result = backend.create_vlan(vlan_config)
    print(f"VLAN created: {result}")
