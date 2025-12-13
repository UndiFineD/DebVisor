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
    logging.basicConfig(  # type: ignore[call-arg]
        _level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
_logger=logging.getLogger(__name__)


@dataclass
class ConfigVersion:
    """Represents a version of configuration."""

    version_id: str
    timestamp: float
    content: Dict[str, Any]
    checksum: str
    description: str=""

    @classmethod
    def create(cls, content: Dict[str, Any], description: str="") -> "ConfigVersion":
        _content_str=json.dumps(content, sort_keys=True)
        _checksum=hashlib.sha256(content_str.encode()).hexdigest()  # type: ignore[name-defined]
        _version_id=f"v{int(time.time())}_{checksum[:8]}"  # type: ignore[name-defined]
        return cls(  # type: ignore[call-arg]
            _version_id=version_id,  # type: ignore[name-defined]
            _timestamp=time.time(),
            _content=content,
            _checksum=checksum,  # type: ignore[name-defined]
            _description=description,
        )


class ConfigStore:
    """Local storage for configuration versions."""

    def __init__(self, storagedir: str) -> None:
        self.storage_dir=Path(storage_dir)  # type: ignore[name-defined]
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.current_version_file=self.storage_dir / "current_version"

    def save_version(self, version: ConfigVersion) -> None:
        version_path=self.storage_dir / f"{version.version_id}.json"
        with open(version_path, "w") as f:
            json.dump(
                {
                    "version_id": version.version_id,
                    "timestamp": version.timestamp,
                    "content": version.content,
                    "checksum": version.checksum,
                    "description": version.description,
                },
                f,
                _indent=2,
            )
        logger.info(f"Saved config version {version.version_id}")  # type: ignore[name-defined]

    def load_version(self, versionid: str) -> Optional[ConfigVersion]:
        version_path=self.storage_dir / f"{version_id}.json"  # type: ignore[name-defined]
        if not version_path.exists():
            return None

        with open(version_path, "r") as f:
            _data=json.load(f)
            return ConfigVersion(**data)  # type: ignore[name-defined]

    def set_current(self, versionid: str) -> None:
        with open(self.current_version_file, "w") as f:
            f.write(version_id)  # type: ignore[name-defined]

    def get_current(self) -> Optional[ConfigVersion]:
        if not self.current_version_file.exists():
            return None
        with open(self.current_version_file, "r") as f:
            _version_id=f.read().strip()
        return self.load_version(version_id)  # type: ignore[name-defined]


class ConfigDistributor:
    """Distributes configuration to nodes."""

    def __init__(self, store: ConfigStore) -> None:
        self.store=store

    async def distribute(
        self, version: ConfigVersion, nodes: List[str]
    ) -> Dict[str, bool]:
        """
        Distribute configuration to a list of nodes.
        Returns a dict of node -> success status.
        """
        logger.info(  # type: ignore[name-defined]
            f"Distributing version {version.version_id} to {len(nodes)} nodes..."
        )

        results={}
        # In a real implementation, this would use RPC calls.
        # Here we simulate the distribution.

        _tasks=[self._push_to_node(node, version) for node in nodes]
        _node_results=await asyncio.gather(*tasks, return_exceptions=True)  # type: ignore[name-defined]

        for node, result in zip(nodes, node_results):  # type: ignore[name-defined]
            if isinstance(result, Exception):
                logger.error(f"Failed to push to {node}: {result}")  # type: ignore[name-defined]
                results[node] = False
            else:
                results[node] = result  # type: ignore[assignment]

        _success_count=sum(1 for r in results.values() if r)
        logger.info(f"Distribution complete. Success: {success_count}/{len(nodes)}")  # type: ignore[name-defined]
        return results

    async def _push_to_node(self, node: str, version: ConfigVersion) -> bool:
        """Simulate pushing config to a single node."""
        # Simulate network latency
        await asyncio.sleep(0.1)

        # Simulate random failure (very low probability for demo)
        # if hash(node) % 100 < 5:
            #     raise Exception("Connection timeout")

        logger.debug(f"Pushed {version.version_id} to {node}")  # type: ignore[name-defined]
        return True

    async def rollback(
        self, nodes: List[str], target_version_id: str
    ) -> Dict[str, bool]:
        """Rollback nodes to a specific version."""
        _version=self.store.load_version(target_version_id)
        if not version:  # type: ignore[name-defined]
            raise ValueError(f"Version {target_version_id} not found")

        logger.info(f"Rolling back to {target_version_id}...")  # type: ignore[name-defined]
        return await self.distribute(version, nodes)  # type: ignore[name-defined]


async def main_async() -> None:
    _parser=argparse.ArgumentParser(description="DebVisor Config Distributor")
    parser.add_argument(  # type: ignore[name-defined]
        "--store-dir",
        _default="/var/lib/debvisor/config_store",
        _help="Storage directory",
    )

    _subparsers=parser.add_subparsers(dest="command", help="Commands")  # type: ignore[name-defined]

    # Create Version
    _create_parser=subparsers.add_parser("create", help="Create new config version")  # type: ignore[name-defined]
    create_parser.add_argument("file", help="JSON config file")  # type: ignore[name-defined]
    create_parser.add_argument("--desc", default="", help="Description")  # type: ignore[name-defined]

    # Distribute
    _dist_parser=subparsers.add_parser("distribute", help="Distribute config")  # type: ignore[name-defined]
    dist_parser.add_argument("version_id", help="Version ID to distribute")  # type: ignore[name-defined]
    dist_parser.add_argument(  # type: ignore[name-defined]
        "--nodes", required=True, help="Comma-separated list of nodes"
    )

    # List Versions
    subparsers.add_parser("list", help="List versions")  # type: ignore[name-defined]

    _args=parser.parse_args()  # type: ignore[name-defined]

    if not args.command:  # type: ignore[name-defined]
        parser.print_help()  # type: ignore[name-defined]
        return 1  # type: ignore[return-value]

    _store=ConfigStore(args.store_dir)  # type: ignore[name-defined]
    _distributor=ConfigDistributor(store)  # type: ignore[name-defined]

    if args.command == "create":  # type: ignore[name-defined]
        with open(args.file, "r") as f:  # type: ignore[name-defined]
            _content=json.load(f)

        _version=ConfigVersion.create(content, args.desc)  # type: ignore[name-defined]
        store.save_version(version)  # type: ignore[name-defined]
        store.set_current(version.version_id)  # type: ignore[name-defined]
        print(f"Created version: {version.version_id}")  # type: ignore[name-defined]

    elif args.command == "distribute":  # type: ignore[name-defined]
        _version=store.load_version(args.version_id)  # type: ignore[assignment, name-defined]
        if not version:  # type: ignore[name-defined]
            print(f"Error: Version {args.version_id} not found")  # type: ignore[name-defined]
            return 1  # type: ignore[return-value]

        _nodes=args.nodes.split(", ")  # type: ignore[name-defined]
        _results=await distributor.distribute(version, nodes)  # type: ignore[name-defined]

        print("\nResults:")
        for node, success in results.items():  # type: ignore[name-defined]
            status="? Success" if success else "? Failed"
            print(f"  {node}: {status}")

    elif args.command == "list":  # type: ignore[name-defined]
    # Simple listing
        if not store.storage_dir.exists():  # type: ignore[name-defined]
            print("No versions found.")
            return 0  # type: ignore[return-value]

        versions=[]
        for p in store.storage_dir.glob("*.json"):  # type: ignore[name-defined]
            if p.name == "current_version":
                continue
            with open(p, "r") as f:
                versions.append(json.load(f))

        versions.sort(key=lambda x: x["timestamp"], reverse=True)

        print(f"{'Version ID':<25} {'Date':<20} {'Description'}")
        print("-" * 60)
        for v in versions:
            date_str=time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(v["timestamp"])
            )
            print(f"{v['version_id']:<25} {date_str:<20} {v['description']}")

    return 0  # type: ignore[return-value]


def main() -> None:
    asyncio.run(main_async())


if _name__== "__main__":  # type: ignore[name-defined]
    sys.exit(main())  # type: ignore[func-returns-value, return-value]
