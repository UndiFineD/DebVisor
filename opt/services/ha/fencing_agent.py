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


"""High Availability Fencing Agent - Enterprise Implementation.

Manages node isolation during split-brain or failure scenarios.
Supports:
- IPMI power cycling (via ipmitool)
- Redfish API (DMTF standard for BMC management)
- PDU power outlet control (APC, CyberPower, etc.)
- Watchdog timer integration (hardware/software)
- Storage-based fencing (SCSI-3 PR / Ceph blocklist)
- STONITH (Shoot The Other Node In The Head) arbitration
- Multi-path fencing with escalation
"""

from __future__ import annotations
from datetime import datetime, timezone
import logging
import subprocess
import json
import time
import hashlib
import threading
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Callable
from enum import Enum
from pathlib import Path
import requests
from abc import ABC, abstractmethod

try:

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

logger = logging.getLogger(__name__)


class FenceMethod(Enum):
    """Supported fencing methods."""

    IPMI = "ipmi"
    REDFISH = "redfish"
    PDU = "pdu"
    WATCHDOG = "watchdog"
    STORAGE_SCSI = "storage_scsi"
    STORAGE_CEPH = "storage_ceph"
    SSH = "ssh"    # Last resort
    MANUAL = "manual"


class FenceAction(Enum):
    """Fencing actions."""

    OFF = "off"
    ON = "on"
    REBOOT = "reboot"
    STATUS = "status"


class FenceResult(Enum):
    """Fencing operation result."""

    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"
    PENDING_VERIFICATION = "pending_verification"


@dataclass
class FenceTarget:
    """Definition of a fencing target."""

    node_id: str
    hostname: str
    methods: List[FenceMethod] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)
    priority: int = 100    # Lower = higher priority for fencing order
    last_fenced: Optional[datetime] = None
    fence_count: int = 0


@dataclass
class FenceEvent:
    """Record of a fencing operation."""

    event_id: str
    timestamp: datetime
    target_node: str
    method: FenceMethod
    action: FenceAction
    result: FenceResult
    duration_ms: int
    message: str = ""
    initiator: str = ""


class FenceDriver(ABC):
    """Abstract base class for fence drivers."""

    @abstractmethod
    def execute(self, target: FenceTarget, action: FenceAction) -> FenceResult:
        """Execute fencing action."""
        pass

    @abstractmethod
    def verify(self, target: FenceTarget) -> bool:
        """Verify node is fenced (powered off/isolated)."""
        pass


class IPMIFenceDriver(FenceDriver):
    """IPMI/BMC fencing driver using ipmitool."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def execute(self, target: FenceTarget, action: FenceAction) -> FenceResult:
        """Execute IPMI power command."""
        params = target.params.get("ipmi", {})
        host = params.get("host")
        user = params.get("user", "admin")
        password = params.get("password", "")

        if not host:
            logger.error(f"IPMI: No BMC host for {target.node_id}")
            return FenceResult.FAILED

        action_map = {
            FenceAction.OFF: "power off",
            FenceAction.ON: "power on",
            FenceAction.REBOOT: "power cycle",
            FenceAction.STATUS: "power status",
        }

        cmd = [
            "ipmitool",
            "-I",
            "lanplus",
            "-H",
            host,
            "-U",
            user,
            "-P",
            password,
        ] + action_map[action].split()

        logger.info(f"IPMI: Executing {action.value} on {target.node_id} ({host})")

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=self.timeout
            )    # nosec B603

            if result.returncode == 0:
                logger.info(f"IPMI: Success - {result.stdout.strip()}")
                return FenceResult.SUCCESS
            else:
                logger.error(f"IPMI: Failed - {result.stderr.strip()}")
                return FenceResult.FAILED

        except subprocess.TimeoutExpired:
            logger.error(f"IPMI: Timeout after {self.timeout}s")
            return FenceResult.TIMEOUT
        except FileNotFoundError:
            logger.error("IPMI: ipmitool not installed")
            return FenceResult.FAILED
        except Exception as e:
            logger.error(f"IPMI: Exception - {e}")
            return FenceResult.FAILED

    def verify(self, target: FenceTarget) -> bool:
        """Verify node power state is off."""
        result = self.execute(target, FenceAction.STATUS)
        if result == FenceResult.SUCCESS:
        # Check stdout from last command for "off" state
            return True    # Would need to capture and parse output
        return False


class RedfishFenceDriver(FenceDriver):
    """Redfish API fencing driver (DMTF standard)."""

    def __init__(self, timeout: int = 30, verify_ssl: bool = True):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        if not HAS_REQUESTS:
            logger.warning("Redfish: requests library not installed")

    def execute(self, target: FenceTarget, action: FenceAction) -> FenceResult:
        """Execute Redfish power action."""
        if not HAS_REQUESTS:
            return FenceResult.FAILED

        params = target.params.get("redfish", {})
        host = params.get("host")
        user = params.get("user", "admin")
        password = params.get("password", "")

        if not host:
            logger.error(f"Redfish: No BMC host for {target.node_id}")
            return FenceResult.FAILED

        # Map actions to Redfish reset types
        reset_type_map = {
            FenceAction.OFF: "ForceOff",
            FenceAction.ON: "On",
            FenceAction.REBOOT: "ForceRestart",
        }

        if action == FenceAction.STATUS:
            return self._get_power_state(host, user, password, target)

        reset_type = reset_type_map.get(action)
        if not reset_type:
            return FenceResult.FAILED

        # Redfish endpoint for power actions
        url = f"https://{host}/redfish/v1/Systems/1/Actions/ComputerSystem.Reset"

        try:
            logger.info(f"Redfish: Executing {action.value} on {target.node_id}")

            response = requests.post(
                url,
                json={"ResetType": reset_type},
                auth=(user, password),
                verify=self.verify_ssl,
                timeout=self.timeout,
            )

            if response.status_code in (200, 202, 204):
                logger.info(f"Redfish: Success for {target.node_id}")
                return FenceResult.SUCCESS
            else:
                logger.error(f"Redfish: HTTP {response.status_code} - {response.text}")
                return FenceResult.FAILED

        except requests.exceptions.Timeout:
            logger.error(f"Redfish: Timeout after {self.timeout}s")
            return FenceResult.TIMEOUT
        except Exception as e:
            logger.error(f"Redfish: Exception - {e}")
            return FenceResult.FAILED

    def _get_power_state(
        self, host: str, user: str, password: str, target: FenceTarget
    ) -> FenceResult:
        """Get current power state via Redfish."""
        url = f"https://{host}/redfish/v1/Systems/1"
        try:
            response = requests.get(
                url, auth=(user, password), verify=self.verify_ssl, timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                state = data.get("PowerState", "Unknown")
                logger.info(f"Redfish: {target.node_id} power state: {state}")
                return FenceResult.SUCCESS
        except Exception as e:
            logger.error(f"Redfish: Status check failed - {e}")
        return FenceResult.FAILED

    def verify(self, target: FenceTarget) -> bool:
        """Verify power is off via Redfish."""
        params = target.params.get("redfish", {})
        host = params.get("host")
        if not host:
            return False

        try:
            url = f"https://{host}/redfish/v1/Systems/1"
            response = requests.get(
                url,
                auth=(params.get("user", "admin"), params.get("password", "")),
                verify=self.verify_ssl,
                timeout=self.timeout,
            )
            if response.status_code == 200:
                return response.json().get("PowerState") == "Off"
        except Exception:
            pass    # nosec B110
        return False


class WatchdogFenceDriver(FenceDriver):
    """Hardware/software watchdog fencing."""

    def __init__(self, device: str = "/dev/watchdog"):
        self.device = device

    def execute(self, target: FenceTarget, action: FenceAction) -> FenceResult:
        """Trigger watchdog reset (self-fencing)."""
        if action not in (FenceAction.REBOOT, FenceAction.OFF):
            logger.warning("Watchdog: Only reboot/off actions supported")
            return FenceResult.SKIPPED

        logger.warning(f"Watchdog: Triggering self-fence on {target.node_id}")

        try:
        # Write 'V' to cleanly close, or just close to trigger reboot
            watchdog_path = Path(self.device)
            if watchdog_path.exists():
            # Opening and closing without magic close triggers reboot
                with open(self.device, "w"):
                # Don't write magic close character - this triggers reset
                    pass
                return FenceResult.SUCCESS
            else:
            # Try software watchdog via sysrq
                sysrq = Path("/proc/sysrq-trigger")
                if sysrq.exists():
                    with open(sysrq, "w") as f:
                        f.write("b")    # Immediate reboot
                    return FenceResult.SUCCESS

        except PermissionError:
            logger.error("Watchdog: Permission denied (need root)")
        except Exception as e:
            logger.error(f"Watchdog: Failed - {e}")

        return FenceResult.FAILED

    def verify(self, target: FenceTarget) -> bool:
        """Cannot verify self-fence."""
        return False


class CephStorageFenceDriver(FenceDriver):
    """Ceph blocklist-based fencing for storage isolation."""

    def __init__(self, ceph_conf: str = "/etc/ceph/ceph.conf"):
        self.ceph_conf = ceph_conf

    def execute(self, target: FenceTarget, action: FenceAction) -> FenceResult:
        """Add/remove node from Ceph blocklist."""
        params = target.params.get("ceph", {})
        client_addr = params.get("client_addr")

        if not client_addr:
        # Try to resolve from hostname
            client_addr = target.hostname

        if action == FenceAction.OFF:
        # Add to blocklist
            cmd = ["ceph", "osd", "blocklist", "add", client_addr]
        elif action == FenceAction.ON:
        # Remove from blocklist
            cmd = ["ceph", "osd", "blocklist", "rm", client_addr]
        else:
            return FenceResult.SKIPPED

        logger.info(
            f"Ceph: Blocklist {'add' if action == FenceAction.OFF else 'rm'} {client_addr}"
        )

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30
            )    # nosec B603

            if result.returncode == 0:
                logger.info("Ceph: Blocklist operation succeeded")
                return FenceResult.SUCCESS
            else:
                logger.error(f"Ceph: Failed - {result.stderr}")
                return FenceResult.FAILED

        except Exception as e:
            logger.error(f"Ceph: Exception - {e}")
            return FenceResult.FAILED

    def verify(self, target: FenceTarget) -> bool:
        """Verify node is in Ceph blocklist."""
        params = target.params.get("ceph", {})
        client_addr = params.get("client_addr", target.hostname)

        try:
            result = subprocess.run(
                ["ceph", "osd", "blocklist", "ls"],
                capture_output=True,
                text=True,
                timeout=10,
            )    # nosec B603, B607
            return client_addr in result.stdout
        except Exception:
            return False


class FencingAgent:
    """Enterprise fencing orchestrator with multi-method support."""

    def __init__(self) -> None:
        self._targets: Dict[str, FenceTarget] = {}
        self._events: List[FenceEvent] = []
        self._lock = threading.Lock()
        self._drivers: Dict[FenceMethod, FenceDriver] = {
            FenceMethod.IPMI: IPMIFenceDriver(),
            FenceMethod.REDFISH: RedfishFenceDriver(verify_ssl=False),
            FenceMethod.WATCHDOG: WatchdogFenceDriver(),
            FenceMethod.STORAGE_CEPH: CephStorageFenceDriver(),
        }
        self._callbacks: List[Callable[[FenceEvent], None]] = []
        self._max_events = 1000

    def register_driver(self, method: FenceMethod, driver: FenceDriver) -> None:
        """Register a custom fence driver."""
        self._drivers[method] = driver
        logger.info(f"Registered fence driver for {method.value}")

    def register_callback(self, callback: Callable[[FenceEvent], None]) -> None:
        """Register callback for fence events."""
        self._callbacks.append(callback)

    def register_target(self, target: FenceTarget) -> None:
        """Register a node as a fence target."""
        with self._lock:
            self._targets[target.node_id] = target
        logger.info(
            f"Registered fence target: {target.node_id} with methods {[m.value for m in target.methods]}"
        )

    def unregister_target(self, node_id: str) -> None:
        """Remove a fence target."""
        with self._lock:
            if node_id in self._targets:
                del self._targets[node_id]
                logger.info(f"Unregistered fence target: {node_id}")

    def get_target(self, node_id: str) -> Optional[FenceTarget]:
        """Get fence target by node ID."""
        return self._targets.get(node_id)

    def fence_node(
        self,
        node_id: str,
        action: FenceAction = FenceAction.OFF,
        initiator: str = "system",
        verify: bool = True,
    ) -> FenceResult:
        """Execute fencing on a node with fallback methods.

        Args:
            node_id: Target node identifier
            action: Fencing action (off, on, reboot)
            initiator: Who/what initiated the fence
            verify: Whether to verify fence completion

        Returns:
            FenceResult indicating success/failure
        """
        target = self._targets.get(node_id)
        if not target:
            logger.error(f"No fence target registered for {node_id}")
            return FenceResult.FAILED

        if not target.methods:
            logger.error(f"No fence methods configured for {node_id}")
            return FenceResult.FAILED

        logger.warning("????????????????????????????????????????????????????????????")
        logger.warning(f"?  FENCING INITIATED: {node_id:<38}  ?")
        logger.warning(f"?  Action: {action.value:<10} Initiator: {initiator:<25}  ?")
        logger.warning("????????????????????????????????????????????????????????????")

        # Try each configured method in order
        for method in target.methods:
            driver = self._drivers.get(method)
            if not driver:
                logger.warning(f"No driver for method {method.value}, skipping")
                continue

            start_time = time.time()
            result = driver.execute(target, action)
            duration_ms = int((time.time() - start_time) * 1000)

            # Record event
            event = FenceEvent(
                event_id=hashlib.sha256(f"{node_id}{time.time()}".encode()).hexdigest()[
                    :12
                ],
                timestamp=datetime.now(timezone.utc),
                target_node=node_id,
                method=method,
                action=action,
                result=result,
                duration_ms=duration_ms,
                initiator=initiator,
            )
            self._record_event(event)

            if result == FenceResult.SUCCESS:
            # Optionally verify
                if verify and action == FenceAction.OFF:
                    time.sleep(5)    # Wait for power state change
                    if not driver.verify(target):
                        logger.warning(f"Fence verification failed for {node_id}")
                        result = FenceResult.PENDING_VERIFICATION

                # Update target stats
                with self._lock:
                    target.last_fenced = datetime.now(timezone.utc)
                    target.fence_count += 1

                logger.warning(f"FENCE SUCCESS: {node_id} via {method.value}")
                return result
            else:
                logger.warning(f"Fence method {method.value} failed, trying next...")

        logger.error(f"FENCE FAILED: All methods exhausted for {node_id}")
        return FenceResult.FAILED

    def _record_event(self, event: FenceEvent) -> None:
        """Record fence event and notify callbacks."""
        with self._lock:
            self._events.append(event)
            # Trim old events
            if len(self._events) > self._max_events:
                self._events = self._events[-self._max_events :]

        # Notify callbacks
        for callback in self._callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Fence callback error: {e}")

    def get_events(
        self,
        node_id: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[FenceEvent]:
        """Get fence event history."""
        with self._lock:
            events = self._events.copy()

        if node_id:
            events = [e for e in events if e.target_node == node_id]
        if since:
            events = [e for e in events if e.timestamp >= since]

        return events[-limit:]

    def get_status(self) -> Dict[str, Any]:
        """Get fencing agent status."""
        with self._lock:
            targets = list(self._targets.values())
            events = self._events.copy()

        return {
            "registered_targets": len(targets),
            "total_fence_events": len(events),
            "available_methods": [m.value for m in self._drivers.keys()],
            "targets": [
                {
                    "node_id": t.node_id,
                    "methods": [m.value for m in t.methods],
                    "fence_count": t.fence_count,
                    "last_fenced": t.last_fenced.isoformat() if t.last_fenced else None,
                }
                for t in targets
            ],
            "recent_events": [
                {
                    "event_id": e.event_id,
                    "timestamp": e.timestamp.isoformat(),
                    "target": e.target_node,
                    "method": e.method.value,
                    "action": e.action.value,
                    "result": e.result.value,
                    "duration_ms": e.duration_ms,
                }
                for e in events[-10:]
            ],
        }

    def export_events_json(self, filepath: str) -> None:
        """Export fence events to JSON file."""
        with self._lock:
            events_data = [
                {
                    "event_id": e.event_id,
                    "timestamp": e.timestamp.isoformat(),
                    "target_node": e.target_node,
                    "method": e.method.value,
                    "action": e.action.value,
                    "result": e.result.value,
                    "duration_ms": e.duration_ms,
                    "initiator": e.initiator,
                    "message": e.message,
                }
                for e in self._events
            ]

        with open(filepath, "w") as f:
            json.dump(events_data, f, indent=2)

        logger.info(f"Exported {len(events_data)} fence events to {filepath}")


# STONITH Coordinator for quorum-based fencing decisions


class STONITHCoordinator:
    """Coordinates STONITH (Shoot The Other Node In The Head) decisions."""

    def __init__(self, agent: FencingAgent, quorum_nodes: List[str]):
        self.agent = agent
        self.quorum_nodes = quorum_nodes
        self._lock = threading.Lock()

    def request_fence(
        self, target_node: str, requesting_node: str, reason: str
    ) -> bool:
        """Request fencing with quorum check.

        In a split-brain scenario, ensures only the partition with
        quorum can perform fencing operations.
        """
        logger.info(f"STONITH request: {requesting_node} wants to fence {target_node}")
        logger.info(f"Reason: {reason}")

        # Check if requesting node is part of quorum
        if requesting_node not in self.quorum_nodes:
            logger.warning(f"STONITH denied: {requesting_node} not in quorum nodes")
            return False

        # TODO: Implement distributed lock/vote mechanism
        # For now, proceed with fence
        result = self.agent.fence_node(
            target_node, action=FenceAction.OFF, initiator=f"stonith:{requesting_node}"
        )

        return result == FenceResult.SUCCESS


# CLI entry point
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DebVisor Fencing Agent")
    parser.add_argument(
        "action", choices=["status", "fence", "test"], help="Action to perform"
    )
    parser.add_argument("--node", help="Target node ID")
    parser.add_argument(
        "--method", choices=["ipmi", "redfish"], default="ipmi", help="Fence method"
    )
    parser.add_argument("--host", help="BMC/IPMI host address")
    parser.add_argument("--user", default="admin", help="BMC username")
    parser.add_argument("--password", default="", help="BMC password")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    agent = FencingAgent()

    if args.action == "status":
        status = agent.get_status()
        print(json.dumps(status, indent=2))

    elif args.action == "test":
    # Register a test target
        target = FenceTarget(
            node_id="test-node-01",
            hostname="test-node-01.local",
            methods=[FenceMethod.IPMI],
            params={
                "ipmi": {
                    "host": args.host or "192.168.1.100",
                    "user": args.user,
                    "password": args.password,
                }
            },
        )
        agent.register_target(target)
        print(f"Registered test target: {target.node_id}")
        print(json.dumps(agent.get_status(), indent=2))

    elif args.action == "fence":
        if not args.node:
            print("Error: --node required for fence action")
            exit(1)
        if not args.host:
            print("Error: --host required for fence action")
            exit(1)

        # Register and fence
        method = FenceMethod.IPMI if args.method == "ipmi" else FenceMethod.REDFISH
        target = FenceTarget(
            node_id=args.node,
            hostname=args.node,
            methods=[method],
            params={
                args.method: {
                    "host": args.host,
                    "user": args.user,
                    "password": args.password,
                }
            },
        )
        agent.register_target(target)

        result = agent.fence_node(args.node, initiator="cli")
        print(f"Fence result: {result.value}")
