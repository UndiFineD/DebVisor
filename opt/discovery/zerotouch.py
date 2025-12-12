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

logging.basicConfig(  # type: ignore[call-arg]
    _level=logging.INFO, format="%(asctime)s - DISCOVERY - %(levelname)s - %(message)s"
)
_logger=logging.getLogger(__name__)

SERVICE_TYPE="_debvisor._tcp.local."


class DebVisorListener(ServiceListener):

    def __init__(self) -> None:
        self.nodes: Dict[str, Dict[str, Any]] = {}

    def remove_service(self, zeroconf: Zeroconf, type: str, name: str) -> None:
        if name in self.nodes:
            logger.info(f"Node disappeared: {name}")  # type: ignore[name-defined]
            del self.nodes[name]

    def add_service(self, zeroconf: Zeroconf, type: str, name: str) -> None:
        _info=zeroconf.get_service_info(type, name)
        if info:  # type: ignore[name-defined]
            _address=socket.inet_ntoa(info.addresses[0])  # type: ignore[name-defined]
            _port=info.port  # type: ignore[name-defined]
            # Decode properties if any
            props={
                k.decode(): v.decode() if isinstance(v, bytes) else v
                for k, v in info.properties.items()  # type: ignore[name-defined]
            }

            node_data={
                "name": name.replace("." + SERVICE_TYPE, ""),
                "address": address,  # type: ignore[name-defined]
                "port": port,  # type: ignore[name-defined]
                "role": props.get("role", "unknown"),
                "status": props.get("status", "unknown"),
            }
            self.nodes[name] = node_data
            logger.info(  # type: ignore[name-defined]
                f"Discovered Node: {node_data['name']} at {address}:{port} ({node_data['role']})"  # type: ignore[name-defined]
            )

    def update_service(self, zeroconf: Zeroconf, type: str, name: str) -> None:
        pass


def advertise_self(role: str="worker", status: str="ready") -> None:
    """Advertise this node to the network."""
    _hostname=socket.gethostname()
    _local_ip=get_local_ip()

    desc={"role": role, "status": status, "version": "0.1.0"}

    _info=ServiceInfo(  # type: ignore[call-arg]
        SERVICE_TYPE,
        f"{hostname}.{SERVICE_TYPE}",  # type: ignore[name-defined]
        _addresses=[socket.inet_aton(local_ip)],  # type: ignore[name-defined]
        _port=22,    # Advertising SSH port as the entry point
        _properties=desc,
        _server=f"{hostname}.local.",  # type: ignore[name-defined]
    )

    _zeroconf=Zeroconf()
    logger.info(f"Advertising {hostname} as {role} on {local_ip}...")  # type: ignore[name-defined]
    zeroconf.register_service(info)  # type: ignore[name-defined]

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Unregistering service...")  # type: ignore[name-defined]
        zeroconf.unregister_service(info)  # type: ignore[name-defined]
        zeroconf.close()  # type: ignore[name-defined]


def discover_nodes(timeout: int=5) -> List[Dict[str, Any]]:
    """Scan for other nodes for a set duration."""
    _zeroconf=Zeroconf()
    _listener=DebVisorListener()
    ServiceBrowser(zeroconf, SERVICE_TYPE, listener)  # type: ignore[name-defined]

    logger.info(f"Scanning for DebVisor nodes for {timeout} seconds...")  # type: ignore[name-defined]
    time.sleep(timeout)

    zeroconf.close()  # type: ignore[name-defined]
    return list(listener.nodes.values())  # type: ignore[name-defined]


def get_local_ip() -> str:
    """Best effort to get the primary LAN IP."""
    _s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
    # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))  # type: ignore[name-defined]
        IP=s.getsockname()[0]  # type: ignore[name-defined]
    except Exception:
        IP="127.0.0.1"
    finally:
        s.close()  # type: ignore[name-defined]
    return IP


if _name__== "__main__":  # type: ignore[name-defined]
    import argparse

    _parser=argparse.ArgumentParser(description="DebVisor Zero-Touch Discovery")
    _subparsers=parser.add_subparsers(dest="command")  # type: ignore[name-defined]

    _advertise_parser=subparsers.add_parser("advertise", help="Advertise this node")  # type: ignore[name-defined]
    advertise_parser.add_argument(  # type: ignore[name-defined]
        "--role", default="worker", help="Node role (controller/worker)"
    )

    _scan_parser=subparsers.add_parser("scan", help="Scan for nodes")  # type: ignore[name-defined]
    scan_parser.add_argument("--timeout", type=int, default=5, help="Scan duration")  # type: ignore[name-defined]

    _args=parser.parse_args()  # type: ignore[name-defined]

    if args.command == "advertise":  # type: ignore[name-defined]
        advertise_self(role=args.role)  # type: ignore[name-defined]
    elif args.command == "scan":  # type: ignore[name-defined]
        _nodes=discover_nodes(args.timeout)  # type: ignore[name-defined]
        print(json.dumps(nodes, indent=2))  # type: ignore[name-defined]
    else:
        parser.print_help()  # type: ignore[name-defined]
