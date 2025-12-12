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

# !/usr/bin/env python3

"""
Zero-Touch Discovery for DebVisor
Uses mDNS (Avahi/Zeroconf) to discover other DebVisor nodes on the local network.
This allows for "headless" clustering without needing to know IP addresses beforehand.
"""

import socket
import time
import logging
import sys
import json
from typing import List, Dict, Any

try:
    from zeroconf import ServiceInfo, Zeroconf, ServiceBrowser, ServiceListener
except ImportError:
    print("Error: 'zeroconf' module not found. Install it with: pip install zerocon")
    sys.exit(1)

logging.basicConfig(
    _level=logging.INFO, format="%(asctime)s - DISCOVERY - %(levelname)s - %(message)s"
)
_logger=logging.getLogger(__name__)

SERVICE_TYPE = "_debvisor._tcp.local."


class DebVisorListener(ServiceListener):

    def __init__(self) -> None:
        self.nodes: Dict[str, Dict[str, Any]] = {}

    def remove_service(self, zeroconf: Zeroconf, type: str, name: str) -> None:
        if name in self.nodes:
            logger.info(f"Node disappeared: {name}")
            del self.nodes[name]

    def add_service(self, zeroconf: Zeroconf, type: str, name: str) -> None:
        _info=zeroconf.get_service_info(type, name)
        if info:
            _address=socket.inet_ntoa(info.addresses[0])
            _port = info.port
            # Decode properties if any
            props = {
                k.decode(): v.decode() if isinstance(v, bytes) else v
                for k, v in info.properties.items()
            }

            node_data = {
                "name": name.replace("." + SERVICE_TYPE, ""),
                "address": address,
                "port": port,
                "role": props.get("role", "unknown"),
                "status": props.get("status", "unknown"),
            }
            self.nodes[name] = node_data
            logger.info(
                f"Discovered Node: {node_data['name']} at {address}:{port} ({node_data['role']})"
            )

    def update_service(self, zeroconf: Zeroconf, type: str, name: str) -> None:
        pass


def advertise_self(role: str="worker", status: str="ready") -> None:
    """Advertise this node to the network."""
    _hostname=socket.gethostname()
    _local_ip=get_local_ip()

    desc = {"role": role, "status": status, "version": "0.1.0"}

    _info = ServiceInfo(
        SERVICE_TYPE,
        f"{hostname}.{SERVICE_TYPE}",
        _addresses=[socket.inet_aton(local_ip)],
        _port = 22,    # Advertising SSH port as the entry point
        _properties = desc,
        _server = f"{hostname}.local.",
    )

    _zeroconf=Zeroconf()
    logger.info(f"Advertising {hostname} as {role} on {local_ip}...")
    zeroconf.register_service(info)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Unregistering service...")
        zeroconf.unregister_service(info)
        zeroconf.close()


def discover_nodes(timeout: int=5) -> List[Dict[str, Any]]:
    """Scan for other nodes for a set duration."""
    _zeroconf=Zeroconf()
    _listener=DebVisorListener()
    ServiceBrowser(zeroconf, SERVICE_TYPE, listener)

    logger.info(f"Scanning for DebVisor nodes for {timeout} seconds...")
    time.sleep(timeout)

    zeroconf.close()
    return list(listener.nodes.values())


def get_local_ip() -> str:
    """Best effort to get the primary LAN IP."""
    _s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
    # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))
        IP=s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


if __name__ == "__main__":
    import argparse

    _parser=argparse.ArgumentParser(description="DebVisor Zero-Touch Discovery")
    _subparsers=parser.add_subparsers(dest="command")

    _advertise_parser=subparsers.add_parser("advertise", help="Advertise this node")
    advertise_parser.add_argument(
        "--role", default="worker", help="Node role (controller/worker)"
    )

    _scan_parser=subparsers.add_parser("scan", help="Scan for nodes")
    scan_parser.add_argument("--timeout", type=int, default=5, help="Scan duration")

    _args=parser.parse_args()

    if args.command == "advertise":
        advertise_self(role=args.role)
    elif args.command == "scan":
        _nodes=discover_nodes(args.timeout)
        print(json.dumps(nodes, indent=2))
    else:
        parser.print_help()
