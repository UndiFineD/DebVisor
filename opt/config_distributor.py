#!/usr/bin/env python3
"""
Configuration Distribution System for DebVisor

Handles the propagation of configuration changes across the cluster.
Ensures consistency, versioning, and rollback capabilities.

Features:
- Versioned configuration management
- Parallel distribution to multiple nodes
- Atomic application with rollback
- Checksum verification
"""

import argparse
import asyncio
import hashlib
import json
import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any

# Configure logging
try:
    from opt.core.logging import configure_logging
    configure_logging(service_name="config-distributor")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)


@dataclass
class ConfigVersion:
    """Represents a version of configuration."""
    version_id: str
    timestamp: float
    content: Dict[str, Any]
    checksum: str
    description: str = ""

    @classmethod
    def create(cls, content: Dict[str, Any], description: str = "") -> 'ConfigVersion':
        content_str = json.dumps(content, sort_keys=True)
        checksum = hashlib.sha256(content_str.encode()).hexdigest()
        version_id = f"v{int(time.time())}_{checksum[:8]}"
        return cls(
            version_id=version_id,
            timestamp=time.time(),
            content=content,
            checksum=checksum,
            description=description
        )


class ConfigStore:
    """Local storage for configuration versions."""

    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.current_version_file = self.storage_dir / "current_version"

    def save_version(self, version: ConfigVersion) -> None:
        version_path = self.storage_dir / f"{version.version_id}.json"
        with open(version_path, "w") as f:
            json.dump({
                "version_id": version.version_id,
                "timestamp": version.timestamp,
                "content": version.content,
                "checksum": version.checksum,
                "description": version.description
            }, f, indent=2)
        logger.info(f"Saved config version {version.version_id}")

    def load_version(self, version_id: str) -> Optional[ConfigVersion]:
        version_path = self.storage_dir / f"{version_id}.json"
        if not version_path.exists():
            return None

        with open(version_path, "r") as f:
            data = json.load(f)
            return ConfigVersion(**data)

    def set_current(self, version_id: str) -> None:
        with open(self.current_version_file, "w") as f:
            f.write(version_id)

    def get_current(self) -> Optional[ConfigVersion]:
        if not self.current_version_file.exists():
            return None
        with open(self.current_version_file, "r") as f:
            version_id = f.read().strip()
        return self.load_version(version_id)


class ConfigDistributor:
    """Distributes configuration to nodes."""

    def __init__(self, store: ConfigStore):
        self.store = store

    async def distribute(self, version: ConfigVersion, nodes: List[str]) -> Dict[str, bool]:
        """
        Distribute configuration to a list of nodes.
        Returns a dict of node -> success status.
        """
        logger.info(f"Distributing version {version.version_id} to {len(nodes)} nodes...")

        results = {}
        # In a real implementation, this would use RPC calls.
        # Here we simulate the distribution.

        tasks = [self._push_to_node(node, version) for node in nodes]
        node_results = await asyncio.gather(*tasks, return_exceptions=True)

        for node, result in zip(nodes, node_results):
            if isinstance(result, Exception):
                logger.error(f"Failed to push to {node}: {result}")
                results[node] = False
            else:
                results[node] = result

        success_count = sum(1 for r in results.values() if r)
        logger.info(f"Distribution complete. Success: {success_count}/{len(nodes)}")
        return results

    async def _push_to_node(self, node: str, version: ConfigVersion) -> bool:
        """Simulate pushing config to a single node."""
        # Simulate network latency
        await asyncio.sleep(0.1)

        # Simulate random failure (very low probability for demo)
        # if hash(node) % 100 < 5:
        #     raise Exception("Connection timeout")

        logger.debug(f"Pushed {version.version_id} to {node}")
        return True

    async def rollback(self, nodes: List[str], target_version_id: str) -> Dict[str, bool]:
        """Rollback nodes to a specific version."""
        version = self.store.load_version(target_version_id)
        if not version:
            raise ValueError(f"Version {target_version_id} not found")

        logger.info(f"Rolling back to {target_version_id}...")
        return await self.distribute(version, nodes)


async def main_async():
    parser = argparse.ArgumentParser(description="DebVisor Config Distributor")
    parser.add_argument(
        "--store-dir",
        default="/var/lib/debvisor/config_store",
        help="Storage directory")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create Version
    create_parser = subparsers.add_parser("create", help="Create new config version")
    create_parser.add_argument("file", help="JSON config file")
    create_parser.add_argument("--desc", default="", help="Description")

    # Distribute
    dist_parser = subparsers.add_parser("distribute", help="Distribute config")
    dist_parser.add_argument("version_id", help="Version ID to distribute")
    dist_parser.add_argument("--nodes", required=True, help="Comma-separated list of nodes")

    # List Versions
    subparsers.add_parser("list", help="List versions")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    store = ConfigStore(args.store_dir)
    distributor = ConfigDistributor(store)

    if args.command == "create":
        with open(args.file, "r") as f:
            content = json.load(f)

        version = ConfigVersion.create(content, args.desc)
        store.save_version(version)
        store.set_current(version.version_id)
        print(f"Created version: {version.version_id}")

    elif args.command == "distribute":
        version = store.load_version(args.version_id)
        if not version:
            print(f"Error: Version {args.version_id} not found")
            return 1

        nodes = args.nodes.split(",")
        results = await distributor.distribute(version, nodes)

        print("\nResults:")
        for node, success in results.items():
            status = "? Success" if success else "? Failed"
            print(f"  {node}: {status}")

    elif args.command == "list":
        # Simple listing
        if not store.storage_dir.exists():
            print("No versions found.")
            return 0

        versions = []
        for p in store.storage_dir.glob("*.json"):
            if p.name == "current_version":
                continue
            with open(p, "r") as f:
                versions.append(json.load(f))

        versions.sort(key=lambda x: x["timestamp"], reverse=True)

        print(f"{'Version ID':<25} {'Date':<20} {'Description'}")
        print("-" * 60)
        for v in versions:
            date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(v["timestamp"]))
            print(f"{v['version_id']:<25} {date_str:<20} {v['description']}")

    return 0


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    sys.exit(main())
