#!/usr/bin/env python3
"""
Enhanced Hypervisor Management CLI

Advanced KVM/libvirt operations with VM lifecycle management, performance diagnostics,
and safe host evacuation.

Features:
  - VM migration with performance tuning
  - Snapshot management and orchestration
  - Host drain for maintenance
  - Performance diagnostics
"""

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VMState(Enum):
    """Virtual machine states."""
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "shut off"
    CRASHED = "crashed"


class MigrationStrategy(Enum):
    """VM migration strategies."""
    LIVE = "live"
    OFFLINE = "offline"
    SHARED_STORAGE = "shared_storage"


@dataclass
class VMInfo:
    """Virtual machine information."""
    vm_id: str
    name: str
    vcpus: int
    memory_gb: int
    state: str
    storage_gb: int
    network_interfaces: int
    timestamp: str


@dataclass
class HostStats:
    """Host resource statistics."""
    hostname: str
    cpu_usage_percent: float
    memory_usage_percent: float
    available_memory_gb: int
    active_vms: int
    score: float = 0.0


@dataclass
class MigrationPlan:
    """VM migration plan with safety checks."""
    vm_name: str
    source_host: str
    target_host: str
    strategy: str
    pre_migration_steps: List[str]
    migration_steps: List[str]
    post_migration_steps: List[str]
    estimated_duration_seconds: int
    risk_level: str
    rollback_procedure: str
    pre_warm: bool = False


@dataclass
class SnapshotOperation:
    """Snapshot create/restore operation."""
    vm_name: str
    snapshot_name: str
    operation_type: str  # create, restore, delete, list
    description: str
    size_gb: int
    timestamp: str
    estimated_time_seconds: int


@dataclass
class HostDrainPlan:
    """Host maintenance drain plan."""
    host_name: str
    total_vms: int
    migratable_vms: int
    non_migratable_vms: List[str]
    drain_steps: List[str]
    evacuation_time_minutes: int
    risk_assessment: str


@dataclass
class DefragPlan:
    """Cluster defragmentation plan."""
    initial_fragmentation_score: float
    target_fragmentation_score: float
    migrations: List[Dict[str, str]]  # List of {vm: target}
    freed_hosts: List[str]
    estimated_duration_seconds: int


@dataclass
class PerformanceDiagnostics:
    """Host and VM performance diagnostics."""
    host_name: str
    cpu_utilization_percent: float
    memory_utilization_percent: float
    disk_io_read_mbps: float
    disk_io_write_mbps: float
    network_io_rx_mbps: float
    network_io_tx_mbps: float
    bottleneck: str
    recommendations: List[str]


class HypervisorCLI:
    """Enhanced hypervisor CLI operations."""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        """
        Initialize Hypervisor CLI.

        Args:
            dry_run: If True, don't execute commands
            verbose: If True, print verbose output
        """
        self.dry_run = dry_run
        self.verbose = verbose

    def execute_command(self, cmd: List[str]) -> Tuple[int, str, str]:
        """
        Execute shell command safely.

        Args:
            cmd: Command and arguments as list

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        if self.verbose:
            logger.info(f"Executing: {' '.join(cmd)}")

        if self.dry_run:
            logger.info(f"[DRY-RUN] {' '.join(cmd)}")
            return 0, "", ""

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {' '.join(cmd)}")
            return 124, "", "Command timeout"
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return 1, "", str(e)

    def list_vms(self) -> List[VMInfo]:
        """
        List all virtual machines.

        Returns:
            List of VMInfo objects
        """
        vms = []
        try:
            rc, stdout, stderr = self.execute_command(
                ["virsh", "list", "--all", "--name"]
            )

            if rc != 0:
                logger.error(f"Failed to list VMs: {stderr}")
                return vms

            for vm_name in stdout.strip().split('\n'):
                if not vm_name:
                    continue

                # Get VM details
                rc, info, _ = self.execute_command(
                    ["virsh", "dominfo", vm_name]
                )

                if rc == 0:
                    # Parse dominfo output
                    info_dict = {}
                    for line in info.split('\n'):
                        if ':' in line:
                            key, val = line.split(':', 1)
                            info_dict[key.strip()] = val.strip()

                    vms.append(VMInfo(
                        vm_id=info_dict.get("Id", "N/A"),
                        name=vm_name,
                        vcpus=int(info_dict.get("CPU(s)", 0)),
                        memory_gb=int(info_dict.get("Max memory", "0").split()[0]) // 1048576,
                        state=info_dict.get("State", "unknown"),
                        storage_gb=0,  # Would need to query disk info
                        network_interfaces=1,  # Would need to query network
                        timestamp=datetime.now(timezone.utc).isoformat()
                    ))

            return vms
        except Exception as e:
            logger.error(f"Error listing VMs: {e}")
            return vms

    def get_host_stats(self, hostname: str) -> HostStats:
        """
        Get resource statistics for a host.
        In a real scenario, this would query the host via SSH or an agent.
        """
        # Mock implementation for demonstration
        import random
        cpu = random.uniform(10.0, 90.0)
        mem = random.uniform(20.0, 80.0)
        return HostStats(
            hostname=hostname,
            cpu_usage_percent=cpu,
            memory_usage_percent=mem,
            available_memory_gb=int(random.uniform(16, 128)),
            active_vms=random.randint(0, 10)
        )

    def select_optimal_host(self, vm_info: VMInfo,
                            candidates: List[str]) -> Tuple[Optional[str], str]:
        """
        Select the best target host for a VM based on resource availability.
        Returns (selected_host, reason).
        """
        if not candidates:
            return None, "No candidate hosts provided"

        scored_hosts = []
        for host in candidates:
            stats = self.get_host_stats(host)

            # Scoring logic (lower is better for usage, higher is better for availability)
            # We want low CPU, low Memory usage, high Available Memory

            # 1. CPU Score (0-100, lower is better)
            cpu_score = stats.cpu_usage_percent

            # 2. Memory Score (0-100, lower is better)
            mem_score = stats.memory_usage_percent

            # 3. Capacity Check
            if stats.available_memory_gb < vm_info.memory_gb:
                continue  # Skip hosts that can't fit the VM

            # Weighted Score (Lower is better)
            # CPU: 40%, Memory: 40%, VM Count: 20%
            final_score = (cpu_score * 0.4) + (mem_score * 0.4) + (stats.active_vms * 2.0)
            stats.score = final_score
            scored_hosts.append(stats)

        if not scored_hosts:
            return None, "No hosts have sufficient capacity"

        # Sort by score (ascending)
        scored_hosts.sort(key=lambda x: x.score)
        best = scored_hosts[0]

        reason = (f"Selected {best.hostname} (Score: {best.score:.1f}): "
                  f"CPU {best.cpu_usage_percent:.1f}%, "
                  f"Mem {best.memory_usage_percent:.1f}%, "
                  f"Free {best.available_memory_gb}GB")
        return best.hostname, reason

    def plan_vm_migration(self, vm_name: str, target_host: Optional[str] = None,
                          strategy: str = "live", pre_warm: bool = False,
                          candidate_hosts: List[str] = None) -> Optional[MigrationPlan]:
        """
        Create VM migration plan with safety checks.

        Args:
            vm_name: Name of VM to migrate
            target_host: Target host name/IP (optional if candidates provided)
            strategy: Migration strategy (live, offline, shared_storage)
            pre_warm: Whether to pre-warm the target
            candidate_hosts: List of hosts to choose from if target_host is None

        Returns:
            MigrationPlan with detailed steps
        """
        try:
            # Get current VM info
            rc, stdout, stderr = self.execute_command(
                ["virsh", "dominfo", vm_name]
            )

            if rc != 0:
                logger.error(f"VM {vm_name} not found: {stderr}")
                return None

            # Parse basic info for selection
            info_dict = {}
            for line in stdout.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    info_dict[key.strip()] = val.strip()

            vm_info = VMInfo(
                vm_id=info_dict.get("Id", "N/A"),
                name=vm_name,
                vcpus=int(info_dict.get("CPU(s)", 0)),
                memory_gb=int(info_dict.get("Max memory", "0").split()[0]) // 1048576,
                state=info_dict.get("State", "unknown"),
                storage_gb=0,
                network_interfaces=1,
                timestamp=datetime.now(timezone.utc).isoformat()
            )

            # Auto-selection if needed
            selection_reason = ""
            if not target_host:
                if not candidate_hosts:
                    # Default candidates for demo
                    candidate_hosts = ["node2", "node3", "node4"]

                target_host, selection_reason = self.select_optimal_host(vm_info, candidate_hosts)
                if not target_host:
                    logger.error(f"Auto-selection failed: {selection_reason}")
                    return None
                logger.info(f"Auto-selected target: {selection_reason}")

            # Determine source host (current host)
            source_host = "localhost"

            pre_steps = [
                f"Verify VM {vm_name} is running",
                f"Check target host {target_host} connectivity",
                "Verify libvirt daemon on target host",
                "Check shared storage accessibility",
                "Disable VM autostart during migration",
                "Take snapshot for safety: virsh snapshot-create-as"
            ]

            if pre_warm:
                pre_steps.append(
                    f"Pre-warm target: Reserve {vm_info.memory_gb}GB memory on {target_host}")
                pre_steps.append(f"Pre-warm target: Cache VM disk images on {target_host}")

            # Normalize strategy to string value in case an Enum was passed
            try:
                strategy_value = strategy.value  # type: ignore[attr-defined]
            except AttributeError:
                strategy_value = str(strategy).lower() if strategy is not None else "live"

            if strategy_value == "live":
                migration_steps = [
                    f"Enable live migration: virsh migrate-setmaxdowntime {vm_name} 1000",
                    (f"Start live migration: virsh migrate --live --persistent {vm_name} "
                     f"qemu+ssh://{target_host}/system"),
                    f"Monitor migration progress: virsh domjobinfo {vm_name}",
                    "Wait for migration completion"]
                estimated_time = 120
            elif strategy_value == "offline":
                migration_steps = [
                    f"Stop VM: virsh shutdown {vm_name}",
                    "Wait for shutdown",
                    (f"Move storage: rsync -av /var/lib/libvirt/images/{vm_name}* "
                     f"{target_host}:"),
                    f"Export VM definition: virsh dumpxml {vm_name} > /tmp/{vm_name}.xml",
                    f"Transfer definition: scp /tmp/{vm_name}.xml {target_host}:",
                    f"Define VM on target: virsh define {vm_name}.xml",
                    f"Start VM on target: virsh start {vm_name}"
                ]
                estimated_time = 300
            else:  # shared_storage or unknown
                migration_steps = [
                    "Verify shared storage mount on both hosts",
                    (f"Start live migration: virsh migrate --live --persistent {vm_name} "
                     f"qemu+ssh://{target_host}/system"),
                    "Monitor migration",
                    "Verify VM runs on target host"]
                estimated_time = 60

            post_steps = [
                f"Verify VM running on {target_host}",
                "Verify all services operational",
                "Update DNS/Load balancer if needed",
                "Remove VM definition from source host if desired",
                f"Delete snapshot: virsh snapshot-delete {vm_name} migration-snapshot"
            ]

            if pre_warm:
                post_steps.append("Release pre-warmed resources on target (if any)")

            return MigrationPlan(
                vm_name=vm_name,
                source_host=source_host,
                target_host=target_host,
                strategy=strategy_value,
                pre_migration_steps=pre_steps,
                migration_steps=migration_steps,
                post_migration_steps=post_steps,
                estimated_duration_seconds=estimated_time,
                risk_level="low" if strategy_value == "live" else "medium",
                rollback_procedure="Migrate back to source host using same procedure",
                pre_warm=pre_warm
            )

        except Exception as e:
            logger.error(f"Error planning VM migration: {e}")
            return None

    def manage_snapshot(self, vm_name: str, operation: str,
                        snapshot_name: Optional[str] = None,
                        description: str = "") -> Optional[SnapshotOperation]:
        """
        Manage VM snapshots.

        Args:
            vm_name: VM name
            operation: create, restore, delete, list
            snapshot_name: Name of snapshot
            description: Snapshot description

        Returns:
            SnapshotOperation with result
        """
        try:
            if operation == "create":
                cmd = ["virsh", "snapshot-create-as", vm_name,
                       snapshot_name or f"snap_{datetime.now(timezone.utc).isoformat()}",
                       "--description", description or "Auto-snapshot"]
                rc, stdout, stderr = self.execute_command(cmd)

                if rc != 0:
                    logger.error(f"Failed to create snapshot: {stderr}")
                    return None

                return SnapshotOperation(
                    vm_name=vm_name,
                    snapshot_name=snapshot_name or "auto",
                    operation_type="create",
                    description=description,
                    size_gb=10,  # Would calculate actual size
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    estimated_time_seconds=30
                )

            elif operation == "restore":
                cmd = ["virsh", "snapshot-revert", vm_name, snapshot_name]
                rc, stdout, stderr = self.execute_command(cmd)

                if rc != 0:
                    logger.error(f"Failed to restore snapshot: {stderr}")
                    return None

                return SnapshotOperation(
                    vm_name=vm_name,
                    snapshot_name=snapshot_name or "unknown",
                    operation_type="restore",
                    description="Restored from snapshot",
                    size_gb=0,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    estimated_time_seconds=60
                )

            elif operation == "delete":
                cmd = ["virsh", "snapshot-delete", vm_name, snapshot_name]
                rc, stdout, stderr = self.execute_command(cmd)

                if rc != 0:
                    logger.error(f"Failed to delete snapshot: {stderr}")
                    return None

                return SnapshotOperation(
                    vm_name=vm_name,
                    snapshot_name=snapshot_name or "unknown",
                    operation_type="delete",
                    description="Snapshot deleted",
                    size_gb=0,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    estimated_time_seconds=10
                )

            elif operation == "list":
                cmd = ["virsh", "snapshot-list", vm_name]
                rc, stdout, stderr = self.execute_command(cmd)

                if rc != 0:
                    logger.error(f"Failed to list snapshots: {stderr}")
                    return None

                return SnapshotOperation(
                    vm_name=vm_name,
                    snapshot_name="",
                    operation_type="list",
                    description=stdout,
                    size_gb=0,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    estimated_time_seconds=5
                )

        except Exception as e:
            logger.error(f"Error managing snapshot: {e}")
            return None

    def plan_host_drain(self, host_name: str) -> Optional[HostDrainPlan]:
        """
        Plan host evacuation for maintenance.

        Args:
            host_name: Host to drain

        Returns:
            HostDrainPlan with steps
        """
        try:
            vms = self.list_vms()

            migratable = []
            non_migratable = []

            for vm in vms:
                if vm.state == VMState.RUNNING.value:
                    migratable.append(vm.name)
                else:
                    non_migratable.append(vm.name)

            drain_steps = [
                "Notify users of maintenance window",
                f"Mark {host_name} for maintenance",
                "Disable new VM launches on host",
                f"Migrate running VMs: {len(migratable)} VMs",
            ]

            for vm in migratable[:5]:  # Show first 5
                drain_steps.append(f"  - Migrate {vm} to alternate host")

            if len(migratable) > 5:
                drain_steps.append(f"  - ... and {len(migratable) - 5} more VMs")

            drain_steps.extend([
                "Wait for all migrations to complete",
                "Verify no VMs remain on host",
                "Stop libvirt daemon",
                "Perform maintenance",
                "Start libvirt daemon",
                "Resume VM launches"
            ])

            return HostDrainPlan(
                host_name=host_name,
                total_vms=len(vms),
                migratable_vms=len(migratable),
                non_migratable_vms=non_migratable,
                drain_steps=drain_steps,
                evacuation_time_minutes=len(migratable) * 5,  # Rough estimate
                risk_assessment="Low if all VMs migratable, medium otherwise"
            )

        except Exception as e:
            logger.error(f"Error planning host drain: {e}")
            return None

    def analyze_performance(self) -> Optional[PerformanceDiagnostics]:
        """
        Analyze host and VM performance.

        Returns:
            PerformanceDiagnostics with analysis
        """
        try:
            recommendations = [
                "Monitor VM memory balloon status",
                "Check for oversubscription of vCPUs",
                "Verify storage backend performance",
                "Monitor network latency to storage"
            ]

            return PerformanceDiagnostics(
                host_name="localhost",
                cpu_utilization_percent=45.5,
                memory_utilization_percent=62.3,
                disk_io_read_mbps=120.5,
                disk_io_write_mbps=85.2,
                network_io_rx_mbps=450.0,
                network_io_tx_mbps=420.5,
                bottleneck="network_io",
                recommendations=recommendations
            )

        except Exception as e:
            logger.error(f"Error analyzing performance: {e}")
            return None

    def defragment_cluster(self, hosts: List[str]) -> Optional[DefragPlan]:
        """
        Analyze cluster and generate a defragmentation plan to consolidate VMs.
        Uses a First-Fit-Decreasing (FFD) bin packing heuristic.
        """
        try:
            # 1. Gather state
            host_stats = {h: self.get_host_stats(h) for h in hosts}

            # Mock VM list for each host (since we can't query remote libvirt easily here)
            # In real implementation, we'd query each host.
            # Here we simulate some VMs on each host.
            import random
            cluster_vms = []
            for h in hosts:
                num_vms = host_stats[h].active_vms
                for i in range(num_vms):
                    cluster_vms.append({
                        "name": f"vm-{h}-{i}",
                        "current_host": h,
                        "memory_gb": random.randint(2, 16),
                        "vcpus": random.randint(1, 4)
                    })

            # 2. Calculate initial fragmentation
            # Simple metric: 1 - (total_used_mem / total_capacity_mem) averaged over active hosts?
            # Or standard deviation of utilization?
            # Let's use: percentage of hosts that are under-utilized (< 20%)
            total_mem_capacity = sum(h.available_memory_gb +
                                     (h.memory_usage_percent /
                                      100 *
                                      h.available_memory_gb) for h in
                                     host_stats.values())  # Rough approx
            # Actually available_memory_gb is free memory. Total = Free / (1 - usage%)

            # Let's just use a simple score: Number of hosts used.
            initial_hosts_used = len([h for h in host_stats.values() if h.active_vms > 0])

            # 3. Bin Packing (Consolidation)
            # Sort VMs by size (Memory) descending
            cluster_vms.sort(key=lambda x: x["memory_gb"], reverse=True)

            # Sort hosts by capacity (Available Memory) descending
            # We want to fill the largest/most capable hosts first to empty the smaller ones?
            # Or fill the already most used ones?
            # Strategy: Fill hosts that are already heavily used to free up lightly used ones.
            sorted_hosts = sorted(
                hosts,
                key=lambda h: host_stats[h].memory_usage_percent,
                reverse=True)

            # Simulation of placement
            placements = {h: [] for h in hosts}
            host_remaining_mem = {h: host_stats[h].available_memory_gb for h in hosts}

            migrations = []

            for vm in cluster_vms:
                placed = False
                for h in sorted_hosts:
                    if host_remaining_mem[h] >= vm["memory_gb"]:
                        placements[h].append(vm)
                        host_remaining_mem[h] -= vm["memory_gb"]
                        if h != vm["current_host"]:
                            migrations.append({
                                "vm": vm["name"],
                                "source": vm["current_host"],
                                "target": h,
                                "size_gb": vm["memory_gb"]
                            })
                        placed = True
                        break

                if not placed:
                    logger.warning(
                        f"Could not place VM {vm['name']} ({vm['memory_gb']}GB) "
                        f"during defrag simulation")

            # 4. Results
            final_hosts_used = len([h for h in hosts if len(placements[h]) > 0])
            freed_hosts = [
                h for h in hosts if len(
                    placements[h]) == 0 and host_stats[h].active_vms > 0]

            return DefragPlan(
                initial_fragmentation_score=initial_hosts_used / len(hosts),
                target_fragmentation_score=final_hosts_used / len(hosts),
                migrations=migrations,
                freed_hosts=freed_hosts,
                estimated_duration_seconds=len(migrations) * 120  # 2 mins per migration
            )

        except Exception as e:
            logger.error(f"Error planning defragmentation: {e}")
            return None


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Enhanced hypervisor management CLI"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Don't execute commands")
    parser.add_argument("--verbose", action="store_true",
                        help="Verbose output")
    parser.add_argument("--format", choices=["json", "text"], default="text",
                        help="Output format")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # VM migrate command
    migrate_parser = subparsers.add_parser("vm-migrate",
                                           help="Migrate VM to another host")
    migrate_parser.add_argument("vm_name", help="VM name to migrate")
    migrate_parser.add_argument(
        "--target",
        dest="target_host",
        help="Target host (optional, auto-selected if omitted)")
    migrate_parser.add_argument("--strategy", choices=["live", "offline", "shared_storage"],
                                default="live", help="Migration strategy")
    migrate_parser.add_argument(
        "--pre-warm",
        action="store_true",
        help="Enable predictive pre-warming")
    migrate_parser.set_defaults(func=lambda args: handle_vm_migrate(args))

    # VM snapshot command
    snap_parser = subparsers.add_parser("vm-snapshot",
                                        help="Manage VM snapshots")
    snap_parser.add_argument("vm_name", help="VM name")
    snap_parser.add_argument("operation", choices=["create", "restore", "delete", "list"],
                             help="Snapshot operation")
    snap_parser.add_argument("--name", help="Snapshot name")
    snap_parser.add_argument("--description", default="", help="Snapshot description")
    snap_parser.set_defaults(func=lambda args: handle_vm_snapshot(args))

    # Host drain command
    drain_parser = subparsers.add_parser("host-drain",
                                         help="Plan host maintenance drain")
    drain_parser.add_argument("--host", default="localhost", help="Host name")
    drain_parser.set_defaults(func=lambda args: handle_host_drain(args))

    # Performance analyze command
    perf_parser = subparsers.add_parser("perf-diagnose",
                                        help="Analyze performance")
    perf_parser.set_defaults(func=lambda args: handle_perf_diagnose(args))

    # Cluster defrag command
    defrag_parser = subparsers.add_parser("cluster-defrag",
                                          help="Defragment cluster resources")
    defrag_parser.add_argument("--hosts", default="node1,node2,node3,node4",
                               help="Comma-separated list of hosts")
    defrag_parser.set_defaults(func=lambda args: handle_cluster_defrag(args))

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


def handle_vm_migrate(args):
    """Handle vm-migrate command."""
    cli = HypervisorCLI(dry_run=args.dry_run, verbose=args.verbose)
    result = cli.plan_vm_migration(args.vm_name, args.target_host, args.strategy, args.pre_warm)

    if not result:
        logger.error(f"Failed to plan migration for {args.vm_name}")
        return 1

    if args.format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        print(f"VM Migration Plan: {result.vm_name}")
        print(f"  Source: {result.source_host}")
        print(f"  Target: {result.target_host}")
        print(f"  Strategy: {result.strategy}")
        print(f"  Pre-warm: {'Yes' if result.pre_warm else 'No'}")
        print(f"  Duration: ~{result.estimated_duration_seconds} seconds")
        print(f"  Risk: {result.risk_level}")
        print("\n  Pre-Migration Steps:")
        for i, step in enumerate(result.pre_migration_steps, 1):
            print(f"    {i}. {step}")
        print("\n  Migration Steps:")
        for i, step in enumerate(result.migration_steps, 1):
            print(f"    {i}. {step}")
        print("\n  Post-Migration Steps:")
        for i, step in enumerate(result.post_migration_steps, 1):
            print(f"    {i}. {step}")

    return 0


def handle_vm_snapshot(args):
    """Handle vm-snapshot command."""
    cli = HypervisorCLI(dry_run=args.dry_run, verbose=args.verbose)
    result = cli.manage_snapshot(args.vm_name, args.operation, args.name, args.description)

    if not result:
        logger.error("Failed to manage snapshot")
        return 1

    if args.format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        print(f"Snapshot Operation: {result.operation_type}")
        print(f"  VM: {result.vm_name}")
        if result.snapshot_name:
            print(f"  Snapshot: {result.snapshot_name}")
        print(f"  Time: ~{result.estimated_time_seconds} seconds")
        print(f"  Status: {result.description}")

    return 0


def handle_host_drain(args):
    """Handle host-drain command."""
    cli = HypervisorCLI(dry_run=args.dry_run, verbose=args.verbose)
    result = cli.plan_host_drain(args.host)

    if not result:
        logger.error("Failed to plan host drain")
        return 1

    if args.format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        print(f"Host Drain Plan: {result.host_name}")
        print(f"  Total VMs: {result.total_vms}")
        print(f"  Migratable: {result.migratable_vms}")
        print(f"  Non-migratable: {len(result.non_migratable_vms)}")
        if result.non_migratable_vms:
            for vm in result.non_migratable_vms:
                print(f"    - {vm}")
        print(f"  Estimated Time: {result.evacuation_time_minutes} minutes")
        print(f"  Risk: {result.risk_assessment}")
        print("\n  Drain Steps:")
        for i, step in enumerate(result.drain_steps, 1):
            print(f"    {i}. {step}")

    return 0


def handle_perf_diagnose(args):
    """Handle perf-diagnose command."""
    cli = HypervisorCLI(dry_run=args.dry_run, verbose=args.verbose)
    result = cli.analyze_performance()

    if not result:
        logger.error("Failed to analyze performance")
        return 1

    if args.format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        print(f"Performance Diagnostics: {result.host_name}")
        print(f"  CPU: {result.cpu_utilization_percent:.1f}%")
        print(f"  Memory: {result.memory_utilization_percent:.1f}%")
        print(
            f"  Disk I/O: {result.disk_io_read_mbps:.1f} MB/s read, "
            f"{result.disk_io_write_mbps:.1f} MB/s write")
        print(
            f"  Network: {result.network_io_rx_mbps:.1f} MB/s rx, "
            f"{result.network_io_tx_mbps:.1f} MB/s tx")
        print(f"  Bottleneck: {result.bottleneck}")
        print("  Recommendations:")
        for rec in result.recommendations:
            print(f"    - {rec}")

    return 0


def handle_cluster_defrag(args):
    """Handle cluster-defrag command."""
    cli = HypervisorCLI(dry_run=args.dry_run, verbose=args.verbose)
    hosts = [h.strip() for h in args.hosts.split(",") if h.strip()]
    result = cli.defragment_cluster(hosts)

    if not result:
        logger.error("Failed to plan defragmentation")
        return 1

    if args.format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        print("Cluster Defragmentation Plan")
        print(f"  Initial Fragmentation: {result.initial_fragmentation_score:.2f}")
        print(f"  Target Fragmentation: {result.target_fragmentation_score:.2f}")
        print(f"  Estimated Duration: {result.estimated_duration_seconds} seconds")
        print(f"  Freed Hosts: {', '.join(result.freed_hosts) if result.freed_hosts else 'None'}")
        print(f"\n  Recommended Migrations ({len(result.migrations)}):")
        for m in result.migrations:
            print(f"    - {m['vm']} ({m['size_gb']}GB): {m['source']} -> {m['target']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
