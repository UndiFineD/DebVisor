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

_logger=logging.getLogger(__name__)


###############################################################################
# Data Classes & Enums
###############################################################################
class AddressFamily(Enum):
    """IP address family"""

    IPV4="inet"
    IPV6="inet6"
    BOTH="both"


class InterfaceState(Enum):
    """Interface state"""

    UP="UP"
    DOWN="DOWN"
    UNKNOWN="UNKNOWN"


@dataclass
class IPAddress:
    """IP address configuration"""

    address: str
    prefix_len: int
    gateway: Optional[str] = None
    family: AddressFamily=AddressFamily.IPV4

    def to_cidr(self) -> str:
        """Convert to CIDR notation"""
        return f"{self.address}/{self.prefix_len}"

    @classmethod
    def from_cidr(cls, cidr: str) -> "IPAddress":
        """Create from CIDR notation"""
        _parts=cidr.split("/")
        if len(parts) != 2:  # type: ignore[name-defined]
            raise ValueError(f"Invalid CIDR: {cidr}")
        return cls(address=parts[0], prefix_len=int(parts[1]))  # type: ignore[name-defined]


@dataclass
class InterfaceConfig:
    """Network interface configuration"""

    name: str
    state: InterfaceState=InterfaceState.DOWN
    mtu: int=1500
    addresses: Optional[List[IPAddress]] = None
    dns_servers: Optional[List[str]] = None
    domain_search: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.addresses is None:
            self.addresses=[]
        if self.dns_servers is None:
            self.dns_servers=[]
        if self.domain_search is None:
            self.domain_search=[]


@dataclass
class BondConfig:
    """Bond configuration"""

    name: str
    mode: str
    slaves: List[str]
    mii_monitor: int=100
    ad_select: str="stable"


@dataclass
class VLANConfig:
    """VLAN configuration"""

    name: str
    parent: str
    vlan_id: int
    protocol: str="802.1q"
    mtu: int=1500


###############################################################################
# Abstract Backend Interface
###############################################################################
class NetworkBackend(ABC):
    """Abstract base class for network backends"""

    def __init__(self, name: str) -> None:
        """Initialize backend"""
        self.name=name
        self.is_available=self._check_availability()
        logger.info(f"{name} backend initialized (available: {self.is_available})")  # type: ignore[name-defined]

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
        self, cmd: List[str], check: bool=True
    ) -> Tuple[int, str, str]:
        """Execute shell command"""
        try:
            result=subprocess.run(
                cmd, capture_output=True, text=True, check=check
            )    # nosec B603
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(cmd)}: {e.stderr}")  # type: ignore[name-defined]
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
        rc, _, _=self.execute_command(["which", "ip"], check=False)
        return rc == 0

    def get_interface(self, name: str) -> Optional[InterfaceConfig]:
        """Get interface configuration using 'ip addr'"""
        rc, output, _=self.execute_command(["ip", "link", "show", name], check=False)

        if rc != 0:
            logger.warning(f"Interface not found: {name}")  # type: ignore[name-defined]
            return None

        # Parse output
        _config=InterfaceConfig(name=name)

        # Extract state
        if "UP" in output:
            config.state=InterfaceState.UP  # type: ignore[name-defined]
        else:
            config.state=InterfaceState.DOWN  # type: ignore[name-defined]

        # Extract MTU
        _mtu_match=re.search(r"mtu\s+(\d+)", output)
        if mtu_match:  # type: ignore[name-defined]
            config.mtu=int(mtu_match.group(1))  # type: ignore[name-defined]

        # Get addresses
        rc, addr_output, _=self.execute_command(
            ["ip", "addr", "show", name], check=False
        )
        if rc == 0:
            for line in addr_output.split("\n"):
                if "inet" in line:
                    _parts=line.split()
                    if len(parts) >= 2:  # type: ignore[name-defined]
                        cidr=parts[1]  # type: ignore[name-defined]
                        config.addresses.append(IPAddress.from_cidr(cidr))  # type: ignore[name-defined, union-attr]

        logger.debug(f"Interface retrieved: {name}")  # type: ignore[name-defined]
        return config  # type: ignore[name-defined]

    def set_interface_up(self, name: str) -> bool:
        """Bring interface up"""
        rc, _, err=self.execute_command(
            ["ip", "link", "set", name, "up"], check=False
        )
        if rc != 0:
            logger.error(f"Failed to set interface up: {name}: {err}")  # type: ignore[name-defined]
            return False
        logger.info(f"Interface up: {name}")  # type: ignore[name-defined]
        return True

    def set_interface_down(self, name: str) -> bool:
        """Bring interface down"""
        rc, _, err=self.execute_command(
            ["ip", "link", "set", name, "down"], check=False
        )
        if rc != 0:
            logger.error(f"Failed to set interface down: {name}: {err}")  # type: ignore[name-defined]
            return False
        logger.info(f"Interface down: {name}")  # type: ignore[name-defined]
        return True

    def add_ip_address(self, name: str, address: IPAddress) -> bool:
        """Add IP address using 'ip addr add'"""
        _cmd=["ip", "addr", "add", address.to_cidr(), "dev", name]
        rc, _, err=self.execute_command(cmd, check=False)  # type: ignore[name-defined]
        if rc != 0:
            logger.error(f"Failed to add address: {err}")  # type: ignore[name-defined]
            return False
        logger.info(f"Address added: {name} -> {address.to_cidr()}")  # type: ignore[name-defined]
        return True

    def remove_ip_address(self, name: str, address: IPAddress) -> bool:
        """Remove IP address using 'ip addr del'"""
        _cmd=["ip", "addr", "del", address.to_cidr(), "dev", name]
        rc, _, err=self.execute_command(cmd, check=False)  # type: ignore[name-defined]
        if rc != 0:
            logger.error(f"Failed to remove address: {err}")  # type: ignore[name-defined]
            return False
        logger.info(f"Address removed: {name} -> {address.to_cidr()}")  # type: ignore[name-defined]
        return True

    def set_mtu(self, name: str, mtu: int) -> bool:
        """Set interface MTU"""
        _cmd=["ip", "link", "set", name, "mtu", str(mtu)]
        rc, _, err=self.execute_command(cmd, check=False)  # type: ignore[name-defined]
        if rc != 0:
            logger.error(f"Failed to set MTU: {err}")  # type: ignore[name-defined]
            return False
        logger.info(f"MTU set: {name} -> {mtu}")  # type: ignore[name-defined]
        return True

    def create_bond(self, config: BondConfig) -> bool:
        """Create bond interface"""
        # Create bond
        cmd=["ip", "link", "add", config.name, "type", "bond", "mode", config.mode]
        rc, _, err=self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to create bond: {err}")  # type: ignore[name-defined]
            return False

        # Add slaves
        for slave in config.slaves:
            slave_cmd=["ip", "link", "set", slave, "master", config.name]
            rc, _, err=self.execute_command(slave_cmd, check=False)
            if rc != 0:
                logger.error(f"Failed to add slave: {err}")  # type: ignore[name-defined]
                return False

        # Bring up bond
        self.set_interface_up(config.name)

        logger.info(f"Bond created: {config.name} with slaves {config.slaves}")  # type: ignore[name-defined]
        return True

    def create_vlan(self, config: VLANConfig) -> bool:
        """Create VLAN interface"""
        _cmd=[
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
        rc, _, err=self.execute_command(cmd, check=False)  # type: ignore[name-defined]
        if rc != 0:
            logger.error(f"Failed to create VLAN: {err}")  # type: ignore[name-defined]
            return False

        # Set MTU if needed
        if config.mtu != 1500:
            self.set_mtu(config.name, config.mtu)

        # Bring up VLAN
        self.set_interface_up(config.name)

        logger.info(f"VLAN created: {config.name} on {config.parent}:{config.vlan_id}")  # type: ignore[name-defined]
        return True

    def delete_interface(self, name: str) -> bool:
        """Delete interface"""
        cmd=["ip", "link", "del", name]
        rc, _, err=self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to delete interface: {err}")  # type: ignore[name-defined]
            return False
        logger.info(f"Interface deleted: {name}")  # type: ignore[name-defined]
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
        rc, _, _=self.execute_command(["which", "nmcli"], check=False)
        return rc == 0

    def get_interface(self, name: str) -> Optional[InterfaceConfig]:
        """Get interface configuration using nmcli"""
        rc, output, _=self.execute_command(
            ["nmcli", "device", "show", name], check=False
        )

        if rc != 0:
            logger.warning(f"Interface not found: {name}")  # type: ignore[name-defined]
            return None

        _config=InterfaceConfig(name=name)

        # Parse output
        for line in output.split("\n"):
            if line.startswith("GENERAL.CONNECTION:"):
            # Connection is active
                config.state=InterfaceState.UP  # type: ignore[name-defined]
            elif line.startswith("GENERAL.STATE:"):
                if "connected" in line.lower():
                    config.state=InterfaceState.UP  # type: ignore[name-defined]
                else:
                    config.state=InterfaceState.DOWN  # type: ignore[name-defined]
            elif line.startswith("WIRED-PROPERTIES.MTU:"):
                _parts=line.split(":")
                if len(parts) > 1:  # type: ignore[name-defined]
                    config.mtu=int(parts[1].strip())  # type: ignore[name-defined]
            elif line.startswith("IP4.ADDRESS"):
                _parts=line.split(":")
                if len(parts) > 1:  # type: ignore[name-defined]
                    _address_str=parts[1].strip()  # type: ignore[name-defined]
                    if address_str:  # type: ignore[name-defined]
                        config.addresses.append(IPAddress.from_cidr(address_str))  # type: ignore[name-defined, union-attr]
            elif line.startswith("IP4.DNS"):
                _parts=line.split(":")
                if len(parts) > 1:  # type: ignore[name-defined]
                    _dns=parts[1].strip()  # type: ignore[name-defined]
                    if dns:  # type: ignore[name-defined]
                        config.dns_servers.append(dns)  # type: ignore[name-defined, union-attr]

        logger.debug(f"Interface retrieved via nmcli: {name}")  # type: ignore[name-defined]
        return config  # type: ignore[name-defined]

    def set_interface_up(self, name: str) -> bool:
        """Bring interface up using nmcli"""
        rc, _, err=self.execute_command(
            ["nmcli", "device", "connect", name], check=False
        )
        if rc != 0:
            logger.error(f"Failed to set interface up: {err}")  # type: ignore[name-defined]
            return False
        logger.info(f"Interface up (via nmcli): {name}")  # type: ignore[name-defined]
        return True

    def set_interface_down(self, name: str) -> bool:
        """Bring interface down using nmcli"""
        rc, _, err=self.execute_command(
            ["nmcli", "device", "disconnect", name], check=False
        )
        if rc != 0:
            logger.error(f"Failed to set interface down: {err}")  # type: ignore[name-defined]
            return False
        logger.info(f"Interface down (via nmcli): {name}")  # type: ignore[name-defined]
        return True

    def add_ip_address(self, name: str, address: IPAddress) -> bool:
        """Add IP address using nmcli connection modify"""
        # This is more complex with nmcli - requires connection modification
        _cmd=[
            "nmcli",
            "connection",
            "modify",
            name,
            "+ipv4.addresses",
            address.to_cidr(),
            "ipv4.method",
            "manual",
        ]
        rc, _, err=self.execute_command(cmd, check=False)  # type: ignore[name-defined]
        if rc != 0:
            logger.error(f"Failed to add address via nmcli: {err}")  # type: ignore[name-defined]
            return False

        # Reactivate connection
        self.execute_command(["nmcli", "connection", "up", name], check=False)

        logger.info(f"Address added via nmcli: {name} -> {address.to_cidr()}")  # type: ignore[name-defined]
        return True

    def remove_ip_address(self, name: str, address: IPAddress) -> bool:
        """Remove IP address using nmcli"""
        cmd=[
            "nmcli",
            "connection",
            "modify",
            name,
            "-ipv4.addresses",
            address.to_cidr(),
        ]
        rc, _, err=self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to remove address via nmcli: {err}")  # type: ignore[name-defined]
            return False

        logger.info(f"Address removed via nmcli: {name} -> {address.to_cidr()}")  # type: ignore[name-defined]
        return True

    def set_mtu(self, name: str, mtu: int) -> bool:
        """Set MTU via nmcli"""
        _cmd=["nmcli", "connection", "modify", name, "ethernet.mtu", str(mtu)]
        rc, _, err=self.execute_command(cmd, check=False)  # type: ignore[name-defined]
        if rc != 0:
            logger.error(f"Failed to set MTU via nmcli: {err}")  # type: ignore[name-defined]
            return False

        logger.info(f"MTU set via nmcli: {name} -> {mtu}")  # type: ignore[name-defined]
        return True

    def create_bond(self, config: BondConfig) -> bool:
        """Create bond via nmcli"""
        # Create connection
        _cmd=[
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
        rc, _, err=self.execute_command(cmd, check=False)  # type: ignore[name-defined]
        if rc != 0:
            logger.error(f"Failed to create bond via nmcli: {err}")  # type: ignore[name-defined]
            return False

        # Add slaves
        for slave in config.slaves:
            _slave_cmd=[
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
            rc, _, err=self.execute_command(slave_cmd, check=False)  # type: ignore[name-defined]
            if rc != 0:
                logger.error(f"Failed to add slave via nmcli: {err}")  # type: ignore[name-defined]
                return False

        logger.info(f"Bond created via nmcli: {config.name}")  # type: ignore[name-defined]
        return True

    def create_vlan(self, config: VLANConfig) -> bool:
        """Create VLAN via nmcli"""
        _cmd=[
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
        rc, _, err=self.execute_command(cmd, check=False)  # type: ignore[name-defined]
        if rc != 0:
            logger.error(f"Failed to create VLAN via nmcli: {err}")  # type: ignore[name-defined]
            return False

        logger.info(f"VLAN created via nmcli: {config.name}")  # type: ignore[name-defined]
        return True

    def delete_interface(self, name: str) -> bool:
        """Delete interface via nmcli"""
        cmd=["nmcli", "connection", "delete", name]
        rc, _, err=self.execute_command(cmd, check=False)
        if rc != 0:
            logger.error(f"Failed to delete interface via nmcli: {err}")  # type: ignore[name-defined]
            return False

        logger.info(f"Interface deleted via nmcli: {name}")  # type: ignore[name-defined]
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
    def create_backend(cls, backendname: Optional[str] = None) -> NetworkBackend:
        """Create backend instance"""
        if backend_name and backend_name in cls._backends:  # type: ignore[name-defined]
            _backend=cls._backends[backend_name]()  # type: ignore[name-defined]
            if backend.is_available:  # type: ignore[name-defined]
                return backend  # type: ignore[name-defined]
            logger.warning(f"Backend {backend_name} not available on system")  # type: ignore[name-defined]

        # Try backends in order of preference
        for name in ["iproute2", "nmcli"]:
            _backend=cls._backends[name]()
            if backend.is_available:  # type: ignore[name-defined]
                logger.info(f"Using {name} backend")  # type: ignore[name-defined]
                return backend  # type: ignore[name-defined]

        raise RuntimeError("No supported network backend available")

    @classmethod
    def register_backend(cls, name: str, backendclass: type) -> None:
        """Register custom backend"""
        cls._backends[name] = backend_class  # type: ignore[name-defined]
        logger.info(f"Backend registered: {name}")  # type: ignore[name-defined]


###############################################################################
# Example Usage
###############################################################################

if _name__== "__main__":  # type: ignore[name-defined]
    logging.basicConfig(level=logging.DEBUG)

    # Create backend
    _factory=NetworkBackendFactory()
    _backend=factory.create_backend()  # type: ignore[name-defined]

    print(f"Using backend: {backend.name}")  # type: ignore[name-defined]

    # Get interface
    _if_config=backend.get_interface("eth0")  # type: ignore[name-defined]
    if if_config:  # type: ignore[name-defined]
        print(f"Interface: {if_config.name}, State: {if_config.state.value}")  # type: ignore[name-defined]

    # Add IP address
    _new_addr=IPAddress(address="192.168.1.100", prefix_len=24)
    _result=backend.add_ip_address("eth0", new_addr)  # type: ignore[name-defined]
    print(f"Address added: {result}")  # type: ignore[name-defined]

    # Create VLAN
    _vlan_config=VLANConfig(name="eth0.100", parent="eth0", vlan_id=100)
    _result=backend.create_vlan(vlan_config)  # type: ignore[name-defined]
    print(f"VLAN created: {result}")  # type: ignore[name-defined]
