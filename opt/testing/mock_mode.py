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

"""
DebVisor Mock Mode Infrastructure
==================================

Provides mock implementations of all service managers for testing,
development, and CI/CD environments without actual hypervisor access.

Usage:
    # Enable mock mode globally
    from opt.testing.mock_mode import enable_mock_mode, MockConfig
    enable_mock_mode(MockConfig(latency_ms=10, failure_rate=0.0))

    # Or use context manager for scoped mocking
    with mock_mode(latency_ms=5):
        _result=vm_manager.list_vms()
"""

import sys
import asyncio
import functools
import json
import os
import random
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    TypeVar,
)

# =============================================================================
# MOCK MODE CONFIGURATION
# =============================================================================
class MockBehavior(Enum):
    """Mock behavior modes."""

    NORMAL = "normal"    # Return success with mock data
    SLOW = "slow"    # Add artificial latency
    FLAKY = "flaky"    # Random failures
    FAIL_ALWAYS = "fail_always"    # Always fail
    TIMEOUT = "timeout"    # Simulate timeouts
    DEGRADED = "degraded"    # Partial failures


@dataclass


class MockConfig:
    """Configuration for mock mode behavior."""

    enabled: bool = True
    behavior: MockBehavior = MockBehavior.NORMAL

    # Latency simulation
    latency_ms: float = 0.0
    latency_variance_ms: float = 0.0

    # Failure simulation
    failure_rate: float = 0.0    # 0.0 to 1.0
    timeout_rate: float = 0.0
    timeout_seconds: float = 30.0

    # Data generation
    seed: Optional[int] = None
    vm_count: int = 10
    container_count: int = 20
    storage_pool_count: int = 3

    # State persistence
    persist_state: bool = False
    state_file: Optional[str] = None

    # Logging
    log_calls: bool = False

    def __post_init__(self) -> None:
        if self.seed is not None:
            random.seed(self.seed)


# Global mock configuration
_mock_config: Optional[MockConfig] = None
_mock_state: Dict[str, Any] = {}
_mock_lock=threading.RLock()


def get_mock_config() -> Optional[MockConfig]:
    """Get current mock configuration."""
    return _mock_config


def is_mock_mode() -> bool:
    """Check if mock mode is enabled."""
    return _mock_config is not None and _mock_config.enabled


def enable_mock_mode(config: Optional[MockConfig] = None) -> None:
    """Enable mock mode with optional configuration."""
    global _mock_config
    _mock_config=config or MockConfig()
    _initialize_mock_state()


def disable_mock_mode() -> None:
    """Disable mock mode."""
    global _mock_config
    _mock_config = None


@contextmanager


def mock_mode(
    latency_ms: float = 0.0,
    failure_rate: float = 0.0,
    behavior: MockBehavior = MockBehavior.NORMAL,
    **kwargs,
) -> Generator[MockConfig, None, None]:
    """Context manager for scoped mock mode."""
    global _mock_config
    config = MockConfig(
        _latency_ms = latency_ms, failure_rate=failure_rate, behavior=behavior, **kwargs
    )
    old_config = _mock_config
    enable_mock_mode(config)
    try:
        yield config
    finally:
        _mock_config = old_config


# =============================================================================
# MOCK STATE MANAGEMENT
# =============================================================================
def _initialize_mock_state() -> None:
    """Initialize mock state with generated data."""
    global _mock_state
    _config=_mock_config or MockConfig()

    with _mock_lock:
        _mock_state = {
            "vms": _generate_mock_vms(config.vm_count),
            "containers": _generate_mock_containers(config.container_count),
            "storage_pools": _generate_mock_storage_pools(config.storage_pool_count),
            "networks": _generate_mock_networks(),
            "hosts": _generate_mock_hosts(),
            "events": [],
            "metrics": _generate_mock_metrics(),
            "secrets": _generate_mock_secrets(),
        }

        if config.persist_state and config.state_file:
            _load_persisted_state(config.state_file)


def _load_persisted_state(filepath: str) -> None:
    """Load persisted mock state from file."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                _mock_state.update(json.load(f))
        except (json.JSONDecodeError, IOError):
            pass


def _save_persisted_state() -> None:
    """Save mock state to file if configured."""
    config = _mock_config
    if config and config.persist_state and config.state_file:
        try:
            with open(config.state_file, "w") as f:
            # Serialize only JSON-compatible parts
                serializable = {
                    k: v
                    for k, v in _mock_state.items()
                    if k not in ("metrics",)    # Skip non-serializable
                }
                json.dump(serializable, f, indent=2, default=str)
        except IOError:
            pass


def get_mock_state() -> Dict[str, Any]:
    """Get current mock state (for inspection/testing)."""
    return _mock_state.copy()


def reset_mock_state() -> None:
    """Reset mock state to initial values."""
    _initialize_mock_state()


# =============================================================================
# MOCK DATA GENERATORS
# =============================================================================
def _generate_uuid() -> str:
    """Generate a random UUID."""
    return str(uuid.uuid4())


def _generate_mock_vms(count: int) -> Dict[str, Dict[str, Any]]:
    """Generate mock VM data."""
    vms = {}
    statuses = ["running", "stopped", "paused", "suspended", "crashed"]
    _hypervisors = ["kvm", "xen"]

    for i in range(count):
        vm_id = f"vm-{i:04d}"
        vms[vm_id] = {
            "id": vm_id,
            "uuid": _generate_uuid(),
            "name": f"test-vm-{i:04d}",
            "status": random.choices(statuses, weights=[0.6, 0.25, 0.05, 0.05, 0.05])[
                0
            ],
            "vcpus": random.choice([1, 2, 4, 8, 16]),
            "memory_mb": random.choice([512, 1024, 2048, 4096, 8192, 16384]),
            "disk_gb": random.choice([10, 20, 50, 100, 200, 500]),
            "hypervisor": random.choice(hypervisors),
            "host": f"node-{random.randint(1, 5):02d}",
            "created_at": (
                datetime.now(timezone.utc) - timedelta(days=random.randint(1, 365))
            ).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "network_interfaces": [
                {
                    "mac": _generate_mac(),
                    "ip": f"10.0.{random.randint(0, 255)}.{random.randint(1, 254)}",
                    "network": f"net-{random.randint(0, 2):02d}",
                }
                for _ in range(random.randint(1, 3))
            ],
            "disks": [
                {
                    "path": f"/var/lib/libvirt/images/{vm_id}-disk{j}.qcow2",
                    "size_gb": random.choice([10, 20, 50, 100]),
                    "format": "qcow2",
                    "pool": f"pool-{random.randint(0, 2):02d}",
                }
                for j in range(random.randint(1, 3))
            ],
            "tags": random.sample(
                [
                    "production",
                    "staging",
                    "development",
                    "test",
                    "database",
                    "web",
                    "api",
                ],
                _k=random.randint(1, 3),
            ),
            "metadata": {
                "owner": f"user-{random.randint(1, 10):02d}",
                "project": f"project-{random.randint(1, 5):02d}",
            },
        }

    return vms


def _generate_mac() -> str:
    """Generate a random MAC address."""
    return "52:54:00:{:02x}:{:02x}:{:02x}".format(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )


def _generate_mock_containers(count: int) -> Dict[str, Dict[str, Any]]:
    """Generate mock container data."""
    _containers = {}
    _statuses = ["running", "stopped", "paused", "restarting", "exited"]
    _images = [
        "nginx:latest",
        "redis:7",
        "postgres:15",
        "python:3.11",
        "node:18",
        "golang:1.21",
        "ubuntu:22.04",
        "alpine:3.18",
    ]

    for i in range(count):
        container_id = f"container-{i:04d}"
        containers[container_id] = {
            "id": container_id,
            "short_id": f"{random.randint(0, 0xFFFFFFFFFFFF):012x}",
            "name": f"test-container-{i:04d}",
            "status": random.choices(statuses, weights=[0.7, 0.15, 0.05, 0.05, 0.05])[
                0
            ],
            "image": random.choice(images),
            "created_at": (
                datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))
            ).isoformat(),
            "ports": [
                {
                    "container_port": random.choice([80, 443, 8080, 3000, 5432, 6379]),
                    "host_port": random.randint(30000, 32767),
                    "protocol": "tcp",
                }
                for _ in range(random.randint(0, 3))
            ],
            "labels": {
                "app": f"app-{random.randint(1, 10):02d}",
                "environment": random.choice(["prod", "staging", "dev"]),
            },
            "resource_limits": {
                "cpu_shares": random.choice([256, 512, 1024, 2048]),
                "memory_mb": random.choice([128, 256, 512, 1024, 2048]),
            },
        }

    return containers


def _generate_mock_storage_pools(count: int) -> Dict[str, Dict[str, Any]]:
    """Generate mock storage pool data."""
    pools = {}
    types = ["dir", "rbd", "lvm", "zfs", "nfs"]

    for i in range(count):
        pool_id = f"pool-{i:02d}"
        _total_gb=random.choice([500, 1000, 2000, 5000, 10000])
        _used_gb=int(total_gb * random.uniform(0.2, 0.8))
        pools[pool_id] = {
            "id": pool_id,
            "name": f"storage-pool-{i:02d}",
            "type": random.choice(types),
            "status": "active",
            "path": f"/var/lib/libvirt/pools/{pool_id}",
            "capacity_gb": total_gb,
            "used_gb": used_gb,
            "available_gb": total_gb - used_gb,
            "allocation_percent": round(used_gb / total_gb * 100, 1),
            "volumes": random.randint(5, 50),
        }

    return pools


def _generate_mock_networks() -> Dict[str, Dict[str, Any]]:
    """Generate mock network data."""
    networks = {}

    for i in range(3):
        net_id = f"net-{i:02d}"
        networks[net_id] = {
            "id": net_id,
            "name": f"network-{i:02d}",
            "type": random.choice(["bridge", "nat", "routed", "isolated"]),
            "status": "active",
            "bridge": f"virbr{i}",
            "cidr": f"10.{i}.0.0/24",
            "gateway": f"10.{i}.0.1",
            "dhcp": {
                "enabled": True,
                "start": f"10.{i}.0.100",
                "end": f"10.{i}.0.254",
            },
            "dns": ["8.8.8.8", "8.8.4.4"],
        }

    return networks


def _generate_mock_hosts() -> Dict[str, Dict[str, Any]]:
    """Generate mock host/node data."""
    hosts = {}

    for i in range(5):
        host_id = f"node-{i + 1:02d}"
        hosts[host_id] = {
            "id": host_id,
            "hostname": f"debvisor-node-{i + 1:02d}.local",
            "status": "online" if random.random() > 0.1 else "offline",
            "role": "compute" if i > 0 else "controller",
            "cpu_cores": random.choice([8, 16, 32, 64]),
            "memory_gb": random.choice([32, 64, 128, 256]),
            "cpu_usage_percent": random.uniform(10, 80),
            "memory_usage_percent": random.uniform(20, 70),
            "uptime_seconds": random.randint(86400, 86400 * 365),
            "kernel_version": "6.1.0-debvisor",
            "hypervisor": {
                "type": "kvm",
                "version": "QEMU 8.1.0",
            },
            "vms_running": random.randint(0, 20),
            "vms_total": random.randint(0, 30),
        }

    return hosts


def _generate_mock_metrics() -> Dict[str, Any]:
    """Generate mock metrics data."""
    return {
        "cluster": {
            "total_vcpus": random.randint(100, 500),
            "used_vcpus": random.randint(50, 400),
            "total_memory_gb": random.randint(500, 2000),
            "used_memory_gb": random.randint(200, 1500),
            "total_storage_tb": random.randint(10, 100),
            "used_storage_tb": random.randint(5, 80),
            "vms_running": random.randint(50, 200),
            "vms_total": random.randint(100, 300),
            "containers_running": random.randint(100, 500),
        },
        "performance": {
            "api_requests_per_sec": random.uniform(100, 1000),
            "api_latency_ms": random.uniform(5, 50),
            "event_queue_depth": random.randint(0, 100),
        },
    }


def _generate_mock_secrets() -> Dict[str, Dict[str, Any]]:
    """Generate mock secrets metadata."""
    secrets = {}

    secret_types = ["api_key", "password", "certificate", "ssh_key", "token"]

    for i in range(10):
        secret_id = f"secret-{i:03d}"
        secrets[secret_id] = {
            "id": secret_id,
            "name": f"test-secret-{i:03d}",
            "type": random.choice(secret_types),
            "created_at": (
                datetime.now(timezone.utc) - timedelta(days=random.randint(1, 180))
            ).isoformat(),
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(days=random.randint(30, 365))
            ).isoformat(),
            "last_accessed": datetime.now(timezone.utc).isoformat(),
            "version": random.randint(1, 5),
            # Actual secret value is masked
            "value_masked": True,
        }

    return secrets


# =============================================================================
# MOCK DECORATORS
# =============================================================================

F=TypeVar("F", bound=Callable[..., Any])


def mockable(func: F) -> F:
    """
    Decorator that enables mock mode for a function.
    When mock mode is enabled, returns mock data instead of calling the real function.
    """

    @functools.wraps(func)

    def wrapper(*args, **kwargs) -> None:
        config = _mock_config

        if not config or not config.enabled:
            return func(*args, **kwargs)

        if config.log_calls:
            print(f"[MOCK] {func.__name__}({args}, {kwargs})")

        # Simulate latency
        if config.latency_ms > 0:
            latency = config.latency_ms
            if config.latency_variance_ms > 0:
                latency += random.uniform(
                    -config.latency_variance_ms, config.latency_variance_ms
                )
            time.sleep(max(0, latency) / 1000)

        # Simulate failures based on behavior
        if config.behavior == MockBehavior.FAIL_ALWAYS:
            raise MockServiceError(f"Mock failure: {func.__name__}")

        if config.behavior == MockBehavior.FLAKY:
            if random.random() < config.failure_rate:
                raise MockServiceError(f"Random mock failure: {func.__name__}")

        if config.behavior == MockBehavior.TIMEOUT:
            if random.random() < config.timeout_rate:
                time.sleep(config.timeout_seconds)
                raise MockTimeoutError(f"Mock timeout: {func.__name__}")

        # Return mock data based on function name pattern
        return _get_mock_response(func.__name__, *args, **kwargs)

    return wrapper    # type: ignore


def mockable_async(func: F) -> F:
    """Async version of mockable decorator."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        config = _mock_config

        if not config or not config.enabled:
            return await func(*args, **kwargs)

        if config.log_calls:
            print(f"[MOCK ASYNC] {func.__name__}({args}, {kwargs})")

        # Simulate latency
        if config.latency_ms > 0:
            latency = config.latency_ms
            if config.latency_variance_ms > 0:
                latency += random.uniform(
                    -config.latency_variance_ms, config.latency_variance_ms
                )
            await asyncio.sleep(max(0, latency) / 1000)

        # Simulate failures
        if config.behavior == MockBehavior.FAIL_ALWAYS:
            raise MockServiceError(f"Mock failure: {func.__name__}")

        if config.behavior == MockBehavior.FLAKY:
            if random.random() < config.failure_rate:
                raise MockServiceError(f"Random mock failure: {func.__name__}")

        return _get_mock_response(func.__name__, *args, **kwargs)

    return wrapper    # type: ignore


# =============================================================================
# MOCK RESPONSE HANDLER
# =============================================================================
def _get_mock_response(func_name: str, *args, **kwargs) -> Any:
    """Get appropriate mock response based on function name."""
    # VM operations
    if "list_vm" in func_name.lower() or func_name== "get_vms":
        return list(_mock_state.get("vms", {}).values())

    if "get_vm" in func_name.lower():
        _vm_id=kwargs.get("vm_id") or (args[0] if args else None)
        _vms=_mock_state.get("vms", {})
        return vms.get(vm_id) if vm_id else None

    if "create_vm" in func_name.lower():
        _vm_id=f"vm-{len(_mock_state.get('vms', {})):04d}"
        _new_vm = {
            "id": vm_id,
            "uuid": _generate_uuid(),
            "name": kwargs.get("name", f"new-vm-{vm_id}"),
            "status": "stopped",
            "vcpus": kwargs.get("vcpus", 2),
            "memory_mb": kwargs.get("memory_mb", 2048),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with _mock_lock:
            _mock_state.setdefault("vms", {})[vm_id] = new_vm
        _save_persisted_state()
        return new_vm

    if "start_vm" in func_name.lower():
        _vm_id=kwargs.get("vm_id") or (args[0] if args else None)
        with _mock_lock:
            if vm_id in _mock_state.get("vms", {}):
                _mock_state["vms"][vm_id]["status"] = "running"
        return {"status": "success", "vm_id": vm_id}

    if "stop_vm" in func_name.lower():
        _vm_id=kwargs.get("vm_id") or (args[0] if args else None)
        with _mock_lock:
            if vm_id in _mock_state.get("vms", {}):
                _mock_state["vms"][vm_id]["status"] = "stopped"
        return {"status": "success", "vm_id": vm_id}

    if "delete_vm" in func_name.lower():
        _vm_id=kwargs.get("vm_id") or (args[0] if args else None)
        with _mock_lock:
            _mock_state.get("vms", {}).pop(vm_id, None)
        _save_persisted_state()
        return {"status": "success", "vm_id": vm_id}

    # Container operations
    if "list_container" in func_name.lower():
        return list(_mock_state.get("containers", {}).values())

    if "get_container" in func_name.lower():
        _container_id=kwargs.get("container_id") or (args[0] if args else None)
        _containers=_mock_state.get("containers", {})
        return containers.get(container_id)

    # Storage operations
    if "list_pool" in func_name.lower() or "list_storage" in func_name.lower():
        return list(_mock_state.get("storage_pools", {}).values())

    if "get_pool" in func_name.lower():
        _pool_id=kwargs.get("pool_id") or (args[0] if args else None)
        _pools=_mock_state.get("storage_pools", {})
        return pools.get(pool_id)

    # Network operations
    if "list_network" in func_name.lower():
        return list(_mock_state.get("networks", {}).values())

    # Host operations
    if "list_host" in func_name.lower() or "list_node" in func_name.lower():
        return list(_mock_state.get("hosts", {}).values())

    if "get_host" in func_name.lower():
        _host_id=kwargs.get("host_id") or (args[0] if args else None)
        _hosts=_mock_state.get("hosts", {})
        return hosts.get(host_id)

    # Health check
    if "health" in func_name.lower():
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {
                "kvm": {"status": "ok"},
                "ceph": {"status": "ok"},
                "database": {"status": "ok"},
            },
        }

    # Metrics
    if "metric" in func_name.lower():
        return _mock_state.get("metrics", {})

    # Secrets
    if "list_secret" in func_name.lower():
        return list(_mock_state.get("secrets", {}).values())

    if "get_secret" in func_name.lower():
        _secret_id=kwargs.get("secret_id") or (args[0] if args else None)
        _secret=_mock_state.get("secrets", {}).get(secret_id)
        if secret:
        # Return with mock decrypted value
            return {
                **secret,
                "value": f"mock-secret-value-{secret_id}",
                "value_masked": False,
            }
        return None

    # Default: return success status
    return {"status": "success", "mock": True}


# =============================================================================
# MOCK EXCEPTIONS
# =============================================================================
class MockServiceError(Exception):
    """Exception raised during mock failures."""

    pass


class MockTimeoutError(Exception):
    """Exception raised for mock timeouts."""

    pass


# =============================================================================
# MOCK SERVICE MANAGERS
# =============================================================================
class MockVMManager:
    """Mock VM Manager for testing."""

    def __init__(self) -> None:
        self._ensure_mock_mode()

    def _ensure_mock_mode(self) -> None:
        if not is_mock_mode():
            enable_mock_mode()

    @mockable

    def list_vms(  # type: ignore[empty-body, return-value]
        self, status: Optional[str] = None, host: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all VMs with optional filtering."""
        pass    # Mock decorator handles response

    @mockable

    def get_vm(self, vm_id: str) -> Optional[Dict[str, Any]]:
        """Get VM by ID."""
        pass

    @mockable

    def create_vm(  # type: ignore[empty-body, return-value]
        self,
        name: str,
        vcpus: int = 2,
        memory_mb: int = 2048,
        disk_gb: int = 20,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new VM."""
        pass

    @mockable

    def start_vm(self, vm_id: str) -> Dict[str, Any]:  # type: ignore[empty-body, return-value]
        """Start a VM."""
        pass

    @mockable

    def stop_vm(self, vm_id: str, force: bool=False) -> Dict[str, Any]:  # type: ignore[empty-body, return-value]
        """Stop a VM."""
        pass

    @mockable

    def delete_vm(self, vm_id: str) -> Dict[str, Any]:  # type: ignore[empty-body, return-value]
        """Delete a VM."""
        pass

    @mockable

    def migrate_vm(  # type: ignore[empty-body, return-value]
        self, vm_id: str, target_host: str, live: bool = True
    ) -> Dict[str, Any]:
        """Migrate VM to another host."""
        pass


class MockContainerManager:
    """Mock Container Manager for testing."""

    @mockable

    def list_containers(self, status: Optional[str] = None) -> List[Dict[str, Any]]:  # type: ignore[empty-body]
        """List all containers."""
        pass

    @mockable

    def get_container(self, container_id: str) -> Optional[Dict[str, Any]]:
        """Get container by ID."""
        pass

    @mockable

    def create_container(self, name: str, image: str, **kwargs) -> Dict[str, Any]:  # type: ignore[empty-body]
        """Create a new container."""
        pass

    @mockable

    def start_container(self, container_id: str) -> Dict[str, Any]:  # type: ignore[empty-body, return-value]
        """Start a container."""
        pass

    @mockable

    def stop_container(self, container_id: str) -> Dict[str, Any]:  # type: ignore[empty-body, return-value]
        """Stop a container."""
        pass


class MockStorageManager:
    """Mock Storage Manager for testing."""

    @mockable

    def list_pools(self) -> List[Dict[str, Any]]:  # type: ignore[empty-body, return-value]
        """List all storage pools."""
        pass

    @mockable

    def get_pool(self, pool_id: str) -> Optional[Dict[str, Any]]:
        """Get storage pool by ID."""
        pass

    @mockable

    def create_volume(  # type: ignore[empty-body, return-value]
        self, pool_id: str, name: str, size_gb: int, **kwargs
    ) -> Dict[str, Any]:
        """Create a new volume."""
        pass


class MockNetworkManager:
    """Mock Network Manager for testing."""

    @mockable

    def list_networks(self) -> List[Dict[str, Any]]:  # type: ignore[empty-body, return-value]
        """List all networks."""
        pass

    @mockable

    def get_network(self, network_id: str) -> Optional[Dict[str, Any]]:
        """Get network by ID."""
        pass


class MockHealthChecker:
    """Mock Health Checker for testing."""

    @mockable

    def check_health(self) -> Dict[str, Any]:  # type: ignore[empty-body, return-value]
        """Check system health."""
        pass

    @mockable

    def get_service_status(self, service_name: str) -> Dict[str, Any]:  # type: ignore[empty-body, return-value]
        """Get specific service status."""
        pass


class MockSecretsManager:
    """Mock Secrets Manager for testing."""

    @mockable

    def list_secrets(self) -> List[Dict[str, Any]]:  # type: ignore[empty-body, return-value]
        """List all secrets (metadata only)."""
        pass

    @mockable

    def get_secret(self, secret_id: str) -> Optional[Dict[str, Any]]:
        """Get secret value."""
        pass

    @mockable

    def create_secret(  # type: ignore[empty-body, return-value]
        self, name: str, value: str, secret_type: str = "generic"
    ) -> Dict[str, Any]:
        """Create a new secret."""
        pass


# =============================================================================
# FACTORY FUNCTION
# =============================================================================
def get_mock_manager(manager_type: str) -> Any:
    """
    Factory function to get mock manager instances.

    Args:
        manager_type: One of 'vm', 'container', 'storage', 'network',
                    'health', 'secrets'

    Returns:
        Mock manager instance
    """
    managers = {
        "vm": MockVMManager,
        "container": MockContainerManager,
        "storage": MockStorageManager,
        "network": MockNetworkManager,
        "health": MockHealthChecker,
        "secrets": MockSecretsManager,
    }

    if manager_type not in managers:
        raise ValueError(
            f"Unknown manager type: {manager_type}. "
            f"Available: {list(managers.keys())}"
        )

    return managers[manager_type]()


# =============================================================================
# TESTING UTILITIES
# =============================================================================
def inject_vm(vm_data: Dict[str, Any]) -> str:
    """Inject a VM into mock state for testing."""
    _vm_id=vm_data.get("id") or f"vm-injected-{_generate_uuid()[:8]}"
    vm_data["id"] = vm_id
    with _mock_lock:
        _mock_state.setdefault("vms", {})[vm_id] = vm_data
    return vm_id


def inject_container(container_data: Dict[str, Any]) -> str:
    """Inject a container into mock state for testing."""
    container_id = (
        container_data.get("id") or f"container-injected-{_generate_uuid()[:8]}"
    )
    container_data["id"] = container_id
    with _mock_lock:
        _mock_state.setdefault("containers", {})[container_id] = container_data
    return container_id


def clear_vms() -> None:
    """Clear all VMs from mock state."""
    with _mock_lock:
        _mock_state["vms"] = {}


def clear_containers() -> None:
    """Clear all containers from mock state."""
    with _mock_lock:
        _mock_state["containers"] = {}


def set_service_status(service_name: str, status: str) -> None:
    """Set mock service status for health checks."""
    # This would modify the health check responses
    pass


# =============================================================================
# ENVIRONMENT DETECTION
# =============================================================================
def auto_enable_mock_mode() -> bool:
    """
    Automatically enable mock mode if running in test/CI environment.

    Checks for:
    - DEBVISOR_MOCK_MODE environment variable
    - CI environment variables (CI, GITHUB_ACTIONS, etc.)
    - pytest execution

    Returns:
        True if mock mode was enabled
    """
    # Check explicit mock mode flag
    if os.environ.get("DEBVISOR_MOCK_MODE", "").lower() in ("1", "true", "yes"):
        enable_mock_mode()
        return True

    # Check CI environments
    ci_vars = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL", "TRAVIS"]
    if any(os.environ.get(var) for var in ci_vars):
        enable_mock_mode(MockConfig(log_calls=False))
        return True

    # Check if running under pytest
    if "pytest" in sys.modules or "_pytest" in sys.modules:
        enable_mock_mode()
        return True

    return False


# Auto-detection can be triggered on import
if os.environ.get("DEBVISOR_AUTO_MOCK", "").lower() in ("1", "true", "yes"):
    auto_enable_mock_mode()

# =============================================================================
# Network Configuration Mock API (for tests/test_netcfg_mock.py)
# =============================================================================

# Flag for tests
MOCK_ENABLED = True


class MockInterfaceType(Enum):
    LOOPBACK = "loopback"
    ETHERNET = "ethernet"
    WIFI = "wifi"
    BRIDGE = "bridge"
    VLAN = "vlan"
    BOND = "bond"


class MockConnectionState(Enum):
    UP = "up"
    DOWN = "down"


@dataclass


class MockWiFiNetwork:
    ssid: str
    bssid: str
    signal_strength: int
    security: str


@dataclass


class MockInterface:
    name: str
    type: MockInterfaceType
    state: MockConnectionState
    mac_address: str
    mtu: int = 1500
    speed_mbps: int = 1000
    ipv4_addresses: list[str] = field(default_factory=list)
    ipv6_addresses: list[str] = field(default_factory=list)
    gateway: Optional[str] = None
    dns_servers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.value,
            "state": self.state.value,
            "mac_address": self.mac_address,
            "mtu": self.mtu,
            "speed_mbps": self.speed_mbps,
            "ipv4_addresses": list(self.ipv4_addresses),
            "ipv6_addresses": list(self.ipv6_addresses),
            "gateway": self.gateway,
            "dns_servers": list(self.dns_servers),
        }


class _NetStateSingleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs) -> None:
        if cls._instance is None:
            cls._instance=super().__call__(*args, **kwargs)
        return cls._instance


class MockNetworkState(metaclass=_NetStateSingleton):

    def __init__(self) -> None:
        self.interfaces: dict[str, MockInterface] = {}
        self.wifi_networks: list[MockWiFiNetwork] = []
        self.routes: list[dict[str, Any]] = []
        self.operation_log: list[dict[str, Any]] = []
        self._generate_default_state(seed=42)

    def _generate_mac(self, rng: random.Random) -> str:
        return ":".join(f"{rng.randint(0, 255):02x}" for _ in range(6))

    def _generate_default_state(self, seed: int | None=None) -> None:
        _rng=random.Random(seed)
        self.interfaces = {
            "lo": MockInterface(
                "lo",
                MockInterfaceType.LOOPBACK,
                MockConnectionState.UP,
                "00:00:00:00:00:00",
                _mtu = 65536,
                _ipv4_addresses=["127.0.0.1/8"],
                _ipv6_addresses = ["::1/128"],
                _speed_mbps=0,
            ),
            "eth0": MockInterface(
                "eth0",
                MockInterfaceType.ETHERNET,
                MockConnectionState.UP,
                self._generate_mac(rng),
                _ipv4_addresses=["192.168.1.100/24"],
                _speed_mbps=1000,
            ),
            "eth1": MockInterface(
                "eth1",
                MockInterfaceType.ETHERNET,
                MockConnectionState.UP,
                self._generate_mac(rng),
                _ipv4_addresses = ["192.168.2.100/24"],
                _speed_mbps = 1000,
            ),
            "br0": MockInterface(
                "br0",
                MockInterfaceType.BRIDGE,
                MockConnectionState.UP,
                self._generate_mac(rng),
            ),
            "wlan0": MockInterface(
                "wlan0",
                MockInterfaceType.WIFI,
                MockConnectionState.UP,
                self._generate_mac(rng),
            ),
        }
        self.routes = [
            {
                "destination": "default",
                "gateway": "192.168.1.1",
                "interface": "eth0",
                "metric": 10,
            },
            {
                "destination": "192.168.1.0/24",
                "gateway": None,
                "interface": "eth0",
                "metric": 0,
            },
        ]
        self.wifi_networks = [
            MockWiFiNetwork(
                _ssid="DebVisor-Open",
                _bssid=self._generate_mac(rng),
                _signal_strength=75,
                _security="Open",
            ),
            MockWiFiNetwork(
                _ssid="DebVisor-Secure",
                _bssid=self._generate_mac(rng),
                _signal_strength=65,
                _security="WPA2",
            ),
            MockWiFiNetwork(
                _ssid="DebVisor-Enterprise",
                _bssid=self._generate_mac(rng),
                _signal_strength = 55,
                _security = "WPA2-Enterprise",
            ),
        ]
        self.operation_log = []

    def log_operation(
        self, op: str, params: dict[str, Any] | None = None, success: bool = True
    ) -> None:
        self.operation_log.append(
            {
                "operation": op,
                "params": params or {},
                "result": "success" if success else "failure",
            }
        )


def get_mock_network_state() -> MockNetworkState:
    return MockNetworkState()


def reset_mock_network_state(seed: int | None=None) -> None:
    get_mock_network_state()._generate_default_state(seed=seed)


@contextmanager


def mock_network_mode(seed: int | None=None) -> Any:
    reset_mock_network_state(seed=seed)
    try:
        yield get_mock_network_state()
    finally:
        reset_mock_network_state(seed=seed)


class MockNetworkBackend:

    def __init__(self) -> None:
        self.state=get_mock_network_state()

    def list_interfaces(self) -> list[dict[str, Any]]:
        return [i.to_dict() for i in self.state.interfaces.values()]

    def get_interface(self, name: str) -> dict[str, Any] | None:
        _iface=self.state.interfaces.get(name)
        return iface.to_dict() if iface else None

    def set_interface_up(self, name: str) -> bool:
        _iface=self.state.interfaces.get(name)
        if not iface:
            return False
        iface.state = MockConnectionState.UP
        self.state.log_operation("set_interface_up", {"name": name}, True)
        return True

    def set_interface_down(self, name: str) -> bool:
        _iface=self.state.interfaces.get(name)
        if not iface:
            return False
        iface.state = MockConnectionState.DOWN
        self.state.log_operation("set_interface_down", {"name": name}, True)
        return True

    def add_ip_address(self, name: str, cidr: str) -> bool:
        _iface=self.state.interfaces.get(name)
        if not iface:
            return False
        if ":" in cidr:
            if cidr not in iface.ipv6_addresses:
                iface.ipv6_addresses.append(cidr)
        else:
            if cidr not in iface.ipv4_addresses:
                iface.ipv4_addresses.append(cidr)
        self.state.log_operation("add_ip_address", {"name": name, "cidr": cidr}, True)
        return True

    def remove_ip_address(self, name: str, cidr: str) -> bool:
        _iface=self.state.interfaces.get(name)
        if not iface:
            return False
        if cidr in iface.ipv4_addresses:
            iface.ipv4_addresses.remove(cidr)
        if cidr in iface.ipv6_addresses:
            iface.ipv6_addresses.remove(cidr)
        self.state.log_operation(
            "remove_ip_address", {"name": name, "cidr": cidr}, True
        )
        return True

    def set_gateway(self, name: str, gateway: str) -> bool:
        _iface=self.state.interfaces.get(name)
        if not iface:
            return False
        iface.gateway = gateway
        self.state.log_operation(
            "set_gateway", {"name": name, "gateway": gateway}, True
        )
        return True

    def set_dns_servers(self, servers: list[str]) -> bool:
        for iface in self.state.interfaces.values():
            if iface.type != MockInterfaceType.LOOPBACK:
                iface.dns_servers = servers
        self.state.log_operation("set_dns_servers", {"servers": servers}, True)
        return True

    def set_mtu(self, name: str, mtu: int) -> bool:
        if mtu < 128 or mtu > 9500:
            return False
        _iface=self.state.interfaces.get(name)
        if not iface:
            return False
        iface.mtu = mtu
        self.state.log_operation("set_mtu", {"name": name, "mtu": mtu}, True)
        return True

    def create_vlan(self, parent: str, vlan_id: int, name: str | None=None) -> bool:
        if vlan_id <= 0 or vlan_id >= 4095:
            return False
        _parent_iface=self.state.interfaces.get(parent)
        if not parent_iface:
            return False
        vlan_name = name or f"{parent}.{vlan_id}"
        self.state.interfaces[vlan_name] = MockInterface(
            _name=vlan_name,
            _type = MockInterfaceType.VLAN,
            _state=MockConnectionState.UP,
            _mac_address = parent_iface.mac_address,
        )
        self.state.log_operation(
            "create_vlan",
            {"parent": parent, "vlan_id": vlan_id, "name": vlan_name},
            True,
        )
        return True

    def delete_vlan(self, name: str) -> bool:
        _iface=self.state.interfaces.get(name)
        if not iface or iface.type != MockInterfaceType.VLAN:
            return False
        del self.state.interfaces[name]
        self.state.log_operation("delete_vlan", {"name": name}, True)
        return True

    def create_bond(
        self, name: str, slaves: list[str], mode: str = "active-backup"
    ) -> bool:
        for s in slaves:
            if s not in self.state.interfaces:
                return False
        self.state.interfaces[name] = MockInterface(
            _name=name,
            _type = MockInterfaceType.BOND,
            _state=MockConnectionState.UP,
            _mac_address = self.state.interfaces[slaves[0]].mac_address,
        )
        self.state.log_operation(
            "create_bond", {"name": name, "slaves": slaves, "mode": mode}, True
        )
        return True

    def create_bridge(self, name: str, ports: list[str] | None=None) -> bool:
        _base_mac=self.state.interfaces.get("eth0")
        self.state.interfaces[name] = MockInterface(
            _name=name,
            _type = MockInterfaceType.BRIDGE,
            _state=MockConnectionState.UP,
            _mac_address=(base_mac.mac_address if base_mac else "00:00:00:00:00:00"),
        )
        self.state.log_operation(
            "create_bridge", {"name": name, "ports": ports or []}, True
        )
        return True

    def get_routes(self) -> list[dict[str, Any]]:
        return list(self.state.routes)

    def add_route(
        self, destination: str, gateway: str, interface: str, metric: int = 0
    ) -> bool:
        self.state.routes.append(
            {
                "destination": destination,
                "gateway": gateway,
                "interface": interface,
                "metric": metric,
            }
        )
        self.state.log_operation("add_route", {"destination": destination}, True)
        return True

    def delete_route(self, destination: str) -> bool:
        _before=len(self.state.routes)
        self.state.routes = [
            r for r in self.state.routes if r["destination"] != destination
        ]
        self.state.log_operation("delete_route", {"destination": destination}, True)
        return len(self.state.routes) < before

    def scan_wifi(self, name: str) -> list[dict[str, Any]]:
        _iface=self.state.interfaces.get(name)
        if not iface or iface.type != MockInterfaceType.WIFI:
            return []
        # Return list of dicts for UI/tests
        return [
            {
                "ssid": n.ssid,
                "bssid": n.bssid,
                "signal_strength": n.signal_strength,
                "security": n.security,
            }
            for n in self.state.wifi_networks
        ]

    def connect_wifi(self, name: str, ssid: str, password: str | None=None) -> bool:
        _iface=self.state.interfaces.get(name)
        if not iface or iface.type != MockInterfaceType.WIFI:
            return False
        _network=next((n for n in self.state.wifi_networks if n.ssid== ssid), None)
        if not network:
            return False
        if network.security != "Open" and not password:
            return False
        iface.state = MockConnectionState.UP
        iface.ipv4_addresses = ["10.0.0.10/24"]
        self.state.log_operation("connect_wifi", {"name": name, "ssid": ssid}, True)
        return True


def verify_operation_logged(op: str, params: dict[str, Any] | None=None) -> bool:
    _state=get_mock_network_state()
    for entry in state.operation_log:
        if entry["operation"] == op:
            if not params:
                return True
            if all(entry["params"].get(k) == v for k, v in params.items()):
                return True
    return False


def get_operation_count(op: str) -> int:
    _state=get_mock_network_state()
    return sum(1 for e in state.operation_log if e["operation"] == op)


def export_mock_state() -> str:
    _state=get_mock_network_state()
    _data = {
        "interfaces": {
            name: iface.to_dict() for name, iface in state.interfaces.items()
        },
        "wifi_networks": [
            {
                "ssid": n.ssid,
                "bssid": n.bssid,
                "signal_strength": n.signal_strength,
                "security": n.security,
            }
            for n in state.wifi_networks
        ],
        "routes": list(state.routes),
        "operation_log": list(state.operation_log),
    }
    return json.dumps(data)
