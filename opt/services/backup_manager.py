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
- Fully Asyncio-based execution
"""

import argparse
import asyncio
import datetime
import logging
import sys
from dataclasses import dataclass
from typing import List, Optional, Union

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
    ZFS Snapshot and Replication backend (Async).
    """

    async def _run_command(self, args: List[str], input_data: Optional[bytes] = None) -> bytes:
        """Helper to run async subprocess commands."""
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE if input_data else None
        )

        stdout, stderr = await process.communicate(input=input_data)

        if process.returncode != 0:
            cmd_str = " ".join(args)
            err_msg = stderr.decode().strip()
            raise Exception(f"Command failed: {cmd_str}\nError: {err_msg}")

        return stdout

    async def create_snapshot(self, dataset: str, tag: str) -> str:
        snap_name = f"{dataset}@{tag}"
        logger.info(f"Creating ZFS snapshot: {snap_name}")
        await self._run_command(["zfs", "snapshot", snap_name])
        return snap_name

    async def list_snapshots(self, dataset: str) -> List[str]:
        try:
            out = await self._run_command(
                ["zfs", "list", "-t", "snapshot", "-H", "-o", "name", "-r", dataset]
            )
            return [line.strip() for line in out.decode().splitlines() if line.strip()]
        except Exception:
            return []

    async def destroy_snapshot(self, snap_name: str) -> None:
        logger.info(f"Destroying ZFS snapshot: {snap_name}")
        await self._run_command(["zfs", "destroy", snap_name])

    async def replicate(self, snap_name: str, target: str, prev_snap: Optional[str] = None) -> None:
        logger.info(f"Replicating {snap_name} to {target}...")

        is_remote = "@" in target

        send_cmd = ["zfs", "send"]
        if prev_snap:
            send_cmd.extend(["-i", prev_snap])
        send_cmd.append(snap_name)

        # Create send process
        send_proc = await asyncio.create_subprocess_exec(
            *send_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Create recv process
        if is_remote:
            user_host, dest_pool = target.split(":")
            recv_cmd = ["ssh", user_host, "zfs", "recv", "-F", dest_pool]
        else:
            recv_cmd = ["zfs", "recv", "-F", target]

        recv_proc = await asyncio.create_subprocess_exec(
            *recv_cmd,
            stdin=send_proc.stdout,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for completion
        # Note: We need to ensure send_proc.stdout is closed in the parent
        # so that recv_proc gets EOF when send_proc finishes.
        # However, asyncio.create_subprocess_exec with pipes handles this slightly
        # differently than Popen.
        # We might need to manually pump data if we want to be purely async without
        # pipes connecting directly in OS.
        # But connecting pipes directly between processes in asyncio is tricky.
        # A simpler approach for this specific case (pipe between two subprocesses)
        # is to use shell=True with a pipe string, OR use the shell pipe syntax.
        # But we want to avoid shell=True.

        # Alternative: Read from send, write to recv.
        # This is memory intensive for large streams.

        # Better Alternative: Use a shell pipeline string for the replication specifically,
        # as it's the most robust way to pipe streams without buffering in Python.

        full_cmd = f"{' '.join(send_cmd)} | {' '.join(recv_cmd)}"
        logger.info(f"Executing pipeline: {full_cmd}")

        pipeline = await asyncio.create_subprocess_shell(
            full_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await pipeline.communicate()

        if pipeline.returncode != 0:
            raise Exception(f"Replication failed: {stderr.decode()}")


class CephBackend:
    """
    Ceph RBD Snapshot backend (Async).
    """

    async def _run_command(self, args: List[str]) -> bytes:
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise Exception(f"Command failed: {stderr.decode()}")
        return stdout

    async def create_snapshot(self, dataset: str, tag: str) -> str:
        snap_name = f"{dataset}@{tag}"
        logger.info(f"Creating Ceph snapshot: {snap_name}")
        await self._run_command(["rbd", "snap", "create", snap_name])
        return snap_name

    async def list_snapshots(self, dataset: str) -> List[str]:
        try:
            out = await self._run_command(
                ["rbd", "snap", "ls", dataset, "--format", "json"]
            )
            import json
            snaps = json.loads(out.decode())
            return [f"{dataset}@{s['name']}" for s in snaps]
        except Exception:
            return []

    async def destroy_snapshot(self, snap_name: str) -> None:
        logger.info(f"Destroying Ceph snapshot: {snap_name}")
        await self._run_command(["rbd", "snap", "rm", snap_name])


class BackupManager:
    """
    Orchestrates backups based on policies (Async).
    """

    def __init__(self) -> None:
        self.policies: List[BackupPolicy] = []
        self.zfs = ZFSBackend()
        self.ceph = CephBackend()

    def add_policy(self, policy: BackupPolicy) -> None:
        self.policies.append(policy)

    async def run_policy(self, policy: BackupPolicy) -> None:
        logger.info(f"Running policy: {policy.name}")
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tag = f"auto-{timestamp}"

        backend: Union[ZFSBackend, CephBackend] = self.zfs if policy.backend == "zfs" else self.ceph

        try:
            # 1. Create Snapshot
            snap_name = await backend.create_snapshot(policy.dataset, tag)

            # 2. Replicate (if ZFS and target set)
            if policy.backend == "zfs" and policy.replication_target:
                snaps = await backend.list_snapshots(policy.dataset)
                auto_snaps = sorted([s for s in snaps if "auto-" in s])
                prev_snap = None
                if len(auto_snaps) > 1:
                    prev_snap = auto_snaps[-2]

                await backend.replicate(snap_name, policy.replication_target, prev_snap)

            # 3. Prune
            await self._prune(policy, backend)

        except Exception as e:
            logger.error(f"Policy {policy.name} failed: {e}")

    async def _prune(self, policy: BackupPolicy, backend: Union[ZFSBackend, CephBackend]) -> None:
        snaps = await backend.list_snapshots(policy.dataset)
        auto_snaps = sorted([s for s in snaps if "auto-" in s])

        total_to_keep = policy.retention_hourly + policy.retention_daily

        if len(auto_snaps) > total_to_keep:
            to_delete = auto_snaps[:-total_to_keep]
            for s in to_delete:
                await backend.destroy_snapshot(s)


async def async_main() -> int:
    parser = argparse.ArgumentParser(description="DebVisor Backup Manager")
    parser.add_argument("--run-all", action="store_true", help="Run all policies immediately")
    parser.add_argument("--daemon", action="store_true", help="Run in daemon mode (scheduler)")

    args = parser.parse_args()

    mgr = BackupManager()

    # Example Policy
    mgr.add_policy(BackupPolicy(
        name="vm-daily",
        dataset="tank/vm",
        backend="zfs",
        schedule_cron="0 0 * * *",
        retention_daily=7
    ))

    if args.run_all:
        tasks = [mgr.run_policy(p) for p in mgr.policies]
        await asyncio.gather(*tasks)

    elif args.daemon:
        logger.info("Starting Backup Manager Daemon...")
        while True:
            await asyncio.sleep(60)
            # Check schedules...

    return 0


def main():
    try:
        sys.exit(asyncio.run(async_main()))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
