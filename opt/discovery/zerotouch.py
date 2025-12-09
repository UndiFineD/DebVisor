#!/usr/bin/env python3
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
from typing import List, Dict, Any, Optional

try:
    from zeroconf import ServiceInfo, Zeroconf, ServiceBrowser
except ImportError:
    print("Error: 'zeroconf' module not found. Install it with: pip install zeroconf")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - DISCOVERY - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SERVICE_TYPE = "_debvisor._tcp.local."


class DebVisorListener:
    def __init__(self) -> None:
        self.nodes: Dict[str, Dict[str, Any]] = {}

    def remove_service(self, zeroconf: Zeroconf, type: str, name: str) -> None:
        if name in self.nodes:
            logger.info(f"Node disappeared: {name}")
            del self.nodes[name]

    def add_service(self, zeroconf: Zeroconf, type: str, name: str) -> None:
        info = zeroconf.get_service_info(type, name)
        if info:
            address = socket.inet_ntoa(info.addresses[0])
            port = info.port
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


def advertise_self(role: str = "worker", status: str = "ready") -> None:
    """Advertise this node to the network."""
    hostname = socket.gethostname()
    local_ip = get_local_ip()

    desc = {"role": role, "status": status, "version": "0.1.0"}

    info = ServiceInfo(
        SERVICE_TYPE,
        f"{hostname}.{SERVICE_TYPE}",
        addresses=[socket.inet_aton(local_ip)],
        port=22,  # Advertising SSH port as the entry point
        properties=desc,
        server=f"{hostname}.local.",
    )

    zeroconf = Zeroconf()
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


def discover_nodes(timeout: int = 5) -> List[Dict[str, Any]]:
    """Scan for other nodes for a set duration."""
    zeroconf = Zeroconf()
    listener = DebVisorListener()
    ServiceBrowser(zeroconf, SERVICE_TYPE, listener)

    logger.info(f"Scanning for DebVisor nodes for {timeout} seconds...")
    time.sleep(timeout)

    zeroconf.close()
    return list(listener.nodes.values())


def get_local_ip() -> None:
    """Best effort to get the primary LAN IP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DebVisor Zero-Touch Discovery")
    subparsers = parser.add_subparsers(dest="command")

    advertise_parser = subparsers.add_parser("advertise", help="Advertise this node")
    advertise_parser.add_argument(
        "--role", default="worker", help="Node role (controller/worker)"
    )

    scan_parser = subparsers.add_parser("scan", help="Scan for nodes")
    scan_parser.add_argument("--timeout", type=int, default=5, help="Scan duration")

    args = parser.parse_args()

    if args.command == "advertise":
        advertise_self(role=args.role)
    elif args.command == "scan":
        nodes = discover_nodes(args.timeout)
        print(json.dumps(nodes, indent=2))
    else:
        parser.print_help()
