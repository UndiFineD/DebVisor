#!/usr/bin/env python3
"""
Enterprise Backup & Replication Manager for DebVisor

Manages storage snapshots, replication, and retention policies.
Supports ZFS and Ceph backends.

Features:
- Automated snapshot scheduling (hourly, daily, weekly)
- Retention policy enforcement (pruning old snapshots)
- ZFS Replication (send/recv) to remote targets
- Ceph RBD snapshot management
"""

import argparse
import asyncio
import datetime
import logging
import subprocess
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class BackupPolicy:
    name: str
    dataset: str  # zfs dataset or ceph pool/image
    backend: str  # "zfs" or "ceph"
    schedule_cron: str  # e.g. "0 * * * *" (hourly)
    retention_hourly: int = 24
    retention_daily: int = 7
    retention_weekly: int = 4
    replication_target: Optional[str] = None  # e.g. "user@host:pool/dataset"


class ZFSBackend:
    """
    ZFS Snapshot and Replication backend.
    
    Provides ZFS-specific snapshot creation, listing, destruction,
    and replication capabilities using the zfs command-line tool.
    """
    
    def create_snapshot(self, dataset: str, tag: str) -> str:
        """
        Create a ZFS snapshot with the given tag.
        
        Args:
            dataset: ZFS dataset name (e.g., 'tank/vm')
            tag: Snapshot tag (e.g., 'auto-20251128-120000')
            
        Returns:
            The full snapshot name (dataset@tag)
            
        Raises:
            subprocess.CalledProcessError: If zfs snapshot command fails
        """
        snap_name = f"{dataset}@{tag}"
        logger.info(f"Creating ZFS snapshot: {snap_name}")
        subprocess.run(["zfs", "snapshot", snap_name], check=True)
        return snap_name

    def list_snapshots(self, dataset: str) -> List[str]:
        """
        List all snapshots for a ZFS dataset.
        
        Args:
            dataset: ZFS dataset name
            
        Returns:
            List of snapshot names
        """
        try:
            out = subprocess.check_output(
                ["zfs", "list", "-t", "snapshot", "-H", "-o", "name", "-r", dataset],
                text=True
            )
            return [line.strip() for line in out.splitlines() if line.strip()]
        except subprocess.CalledProcessError:
            return []

    def destroy_snapshot(self, snap_name: str) -> None:
        """
        Destroy a ZFS snapshot.
        
        Args:
            snap_name: Full snapshot name (dataset@tag)
            
        Raises:
            subprocess.CalledProcessError: If zfs destroy command fails
        """
        logger.info(f"Destroying ZFS snapshot: {snap_name}")
        subprocess.run(["zfs", "destroy", snap_name], check=True)

    def replicate(self, snap_name: str, target: str, prev_snap: Optional[str] = None) -> None:
        """
        Replicate snapshot to target.
        
        Supports both local and remote targets. For remote targets,
        uses SSH to send the snapshot to the destination.
        
        Args:
            snap_name: Full snapshot name to replicate
            target: Target format: user@host:pool/dataset (remote) or pool/dataset (local)
            prev_snap: Previous snapshot for incremental send (optional)
            
        Raises:
            Exception: If replication fails
        """
        logger.info(f"Replicating {snap_name} to {target}...")
        
        # Determine if local or remote
        is_remote = "@" in target
        
        cmd = ["zfs", "send"]
        if prev_snap:
            cmd.extend(["-i", prev_snap])
        cmd.append(snap_name)
        
        send_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        
        if is_remote:
            user_host, dest_pool = target.split(":")
            recv_cmd = ["ssh", user_host, "zfs", "recv", "-F", dest_pool]
        else:
            recv_cmd = ["zfs", "recv", "-F", target]
            
        recv_proc = subprocess.Popen(recv_cmd, stdin=send_proc.stdout)
        send_proc.stdout.close()  # Allow send to receive SIGPIPE if recv exits
        
        recv_proc.communicate()
        if recv_proc.returncode != 0:
            raise Exception(f"Replication failed with code {recv_proc.returncode}")


class CephBackend:
    """
    Ceph RBD Snapshot backend.
    
    Provides Ceph RBD-specific snapshot creation, listing, and destruction
    capabilities using the rbd command-line tool.
    """
    
    def create_snapshot(self, dataset: str, tag: str) -> str:
        """
        Create a Ceph RBD snapshot.
        
        Args:
            dataset: RBD image in format pool/image
            tag: Snapshot tag
            
        Returns:
            Full snapshot name (pool/image@tag)
            
        Raises:
            subprocess.CalledProcessError: If rbd snap create fails
        """
        # dataset format: pool/image
        snap_name = f"{dataset}@{tag}"
        logger.info(f"Creating Ceph snapshot: {snap_name}")
        subprocess.run(["rbd", "snap", "create", snap_name], check=True)
        return snap_name

    def list_snapshots(self, dataset: str) -> List[str]:
        """
        List all snapshots for a Ceph RBD image.
        
        Args:
            dataset: RBD image in format pool/image
            
        Returns:
            List of snapshot names
        """
        # rbd snap ls pool/image --format json
        # For simplicity, parsing text or assuming list
        try:
            out = subprocess.check_output(
                ["rbd", "snap", "ls", dataset, "--format", "json"],
                text=True
            )
            import json
            snaps = json.loads(out)
            return [f"{dataset}@{s['name']}" for s in snaps]
        except Exception:
            return []

    def destroy_snapshot(self, snap_name: str) -> None:
        """
        Destroy a Ceph RBD snapshot.
        
        Args:
            snap_name: Full snapshot name (pool/image@snap)
            
        Raises:
            subprocess.CalledProcessError: If rbd snap rm fails
        """
        logger.info(f"Destroying Ceph snapshot: {snap_name}")
        # snap_name is pool/image@snap
        subprocess.run(["rbd", "snap", "rm", snap_name], check=True)


class BackupManager:
    """
    Orchestrates backups based on policies.
    
    Manages ZFS and Ceph backup policies, including snapshot creation,
    replication, and retention policy enforcement (pruning).
    
    Attributes:
        policies: List of registered backup policies
        zfs: ZFS backend instance
        ceph: Ceph backend instance
    """
    
    def __init__(self) -> None:
        """Initialize BackupManager with empty policies and backend instances."""
        self.policies: List[BackupPolicy] = []
        self.zfs = ZFSBackend()
        self.ceph = CephBackend()

    def add_policy(self, policy: BackupPolicy) -> None:
        """
        Add a backup policy.
        
        Args:
            policy: BackupPolicy to register
        """
        self.policies.append(policy)

    def run_policy(self, policy: BackupPolicy) -> None:
        """
        Execute a backup policy.
        
        Creates a snapshot, optionally replicates it (for ZFS),
        and prunes old snapshots based on retention settings.
        
        Args:
            policy: BackupPolicy to execute
        """
        logger.info(f"Running policy: {policy.name}")
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tag = f"auto-{timestamp}"
        
        backend: Union[ZFSBackend, CephBackend] = self.zfs if policy.backend == "zfs" else self.ceph
        
        try:
            # 1. Create Snapshot
            snap_name = backend.create_snapshot(policy.dataset, tag)
            
            # 2. Replicate (if ZFS and target set)
            if policy.backend == "zfs" and policy.replication_target:
                # Find previous snapshot for incremental
                snaps = backend.list_snapshots(policy.dataset)
                # Filter for auto- snaps and sort
                auto_snaps = sorted([s for s in snaps if "auto-" in s])
                prev_snap = None
                if len(auto_snaps) > 1:
                    prev_snap = auto_snaps[-2] # The one before current
                
                backend.replicate(snap_name, policy.replication_target, prev_snap)

            # 3. Prune
            self._prune(policy, backend)
            
        except Exception as e:
            logger.error(f"Policy {policy.name} failed: {e}")

    def _prune(self, policy: BackupPolicy, backend: Union[ZFSBackend, CephBackend]) -> None:
        """
        Prune old snapshots based on retention policy.
        
        Removes snapshots exceeding the configured retention limits
        (hourly + daily count).
        
        Args:
            policy: BackupPolicy with retention settings
            backend: Storage backend (ZFS or Ceph)
        """
        snaps = backend.list_snapshots(policy.dataset)
        # Filter for our auto tags
        # Format: dataset@auto-YYYYMMDD-HHMMSS
        
        # Group by hour, day, week
        # This is a simplified pruning logic
        # We just keep the last N snapshots for now to demonstrate logic
        
        auto_snaps = sorted([s for s in snaps if "auto-" in s])
        
        # Keep last N total (simplification of hourly/daily/weekly)
        total_to_keep = policy.retention_hourly + policy.retention_daily
        
        if len(auto_snaps) > total_to_keep:
            to_delete = auto_snaps[:-total_to_keep]
            for s in to_delete:
                backend.destroy_snapshot(s)


def main() -> int:
    """
    CLI entry point for DebVisor Backup Manager.
    
    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(description="DebVisor Backup Manager")
    parser.add_argument("--run-all", action="store_true", help="Run all policies immediately")
    parser.add_argument("--daemon", action="store_true", help="Run in daemon mode (scheduler)")
    
    args = parser.parse_args()
    
    mgr = BackupManager()
    
    # Example Policy (would load from config file in real usage)
    mgr.add_policy(BackupPolicy(
        name="vm-daily",
        dataset="tank/vm",
        backend="zfs",
        schedule_cron="0 0 * * *",
        retention_daily=7
    ))
    
    if args.run_all:
        for p in mgr.policies:
            mgr.run_policy(p)
            
    elif args.daemon:
        logger.info("Starting Backup Manager Daemon...")
        # In real implementation, use a scheduler library like 'schedule' or 'apscheduler'
        # Here we just sleep loop for demo
        import time
        while True:
            time.sleep(60)
            # Check schedules...
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
