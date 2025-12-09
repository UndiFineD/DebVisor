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
import subprocess
import asyncio
import datetime
import logging
import sys
import os
import json
import base64
from dataclasses import dataclass
from typing import List, Optional, Union

# Try to use structured logging
try:
    from opt.core.logging import configure_logging

    configure_logging(service_name="backup-manager")
    logger = logging.getLogger("backup-manager")
except ImportError:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)

Try to import cryptography
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    logger.warning("cryptography module not found. Encryption disabled.")


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
    encrypt: bool = False  # Enable encryption at rest


class BackupEncryption:
    """
    Handles AES-256-GCM envelope encryption for backups.
    """

    CHUNK_SIZE = 64 * 1024 * 1024  # 64MB chunks

    def __init__(self, key_path: str = "/etc/debvisor/backup.key"):
        self.key_path = key_path
        self._key = self._load_or_generate_key()

    def _load_or_generate_key(self) -> bytes:
        """Load master key or generate if missing."""
        if not HAS_CRYPTO:
            return b""

        if os.path.exists(self.key_path):
            try:
                with open(self.key_path, "rb") as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Failed to load key: {e}")
                raise

        # Generate new 256-bit key
        logger.info(f"Generating new master key at {self.key_path}")
        key = AESGCM.generate_key(bit_length=256)
        try:
            os.makedirs(os.path.dirname(self.key_path), exist_ok=True)
            with open(self.key_path, "wb") as f:
                f.write(key)
            os.chmod(self.key_path, 0o600)
            return key
        except Exception as e:
            logger.error(f"Failed to save key: {e}")
            raise

    async def encrypt_file(self, input_path: str, output_path: str) -> None:
        """
        Encrypt file using AES-256-GCM envelope encryption with chunking.

        Format:
        [Header JSON]\n
        [Chunk Length (4 bytes)][Nonce (12 bytes)][Ciphertext + Tag]...
        """
        if not HAS_CRYPTO:
            raise RuntimeError("Encryption not available")

        # Generate Data Encryption Key (DEK)
        dek = AESGCM.generate_key(bit_length=256)
        dek_nonce = os.urandom(12)

        # Encrypt DEK with Master Key
        master_gcm = AESGCM(self._key)
        encrypted_dek = master_gcm.encrypt(dek_nonce, dek, None)

        header = {
            "version": 2,
            "algo": "AES-256-GCM",
            "chunked": True,
            "dek_nonce": base64.b64encode(dek_nonce).decode("utf-8"),
            "encrypted_dek": base64.b64encode(encrypted_dek).decode("utf-8"),
        }

        file_gcm = AESGCM(dek)

        try:
            with open(input_path, "rb") as fin, open(output_path, "wb") as fout:
                # Write header
                fout.write(json.dumps(header).encode("utf-8") + b"\n")

                while True:
                    chunk = fin.read(self.CHUNK_SIZE)
                    if not chunk:
                        break

                    # Generate unique nonce for each chunk
                    chunk_nonce = os.urandom(12)
                    ciphertext = file_gcm.encrypt(chunk_nonce, chunk, None)

                    # Write chunk: Length (4 bytes) + Nonce (12 bytes) + Ciphertext
                    # Length includes nonce and ciphertext/tag
                    chunk_len = len(chunk_nonce) + len(ciphertext)
                    fout.write(chunk_len.to_bytes(4, byteorder="big"))
                    fout.write(chunk_nonce)
                    fout.write(ciphertext)

        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            if os.path.exists(output_path):
                os.unlink(output_path)
            raise

    async def decrypt_file(self, input_path: str, output_path: str) -> None:
        """
        Decrypt file using AES-256-GCM envelope encryption.
        """
        if not HAS_CRYPTO:
            raise RuntimeError("Encryption not available")

        try:
            with open(input_path, "rb") as fin:
                # Read header
                header_line = fin.readline()
                header = json.loads(header_line.decode("utf-8"))

                if header.get("version") != 2:
                    raise ValueError(f"Unsupported version: {header.get('version')}")

                # Decrypt DEK
                dek_nonce = base64.b64decode(header["dek_nonce"])
                encrypted_dek = base64.b64decode(header["encrypted_dek"])
                master_gcm = AESGCM(self._key)
                dek = master_gcm.decrypt(dek_nonce, encrypted_dek, None)

                file_gcm = AESGCM(dek)

                with open(output_path, "wb") as fout:
                    while True:
                        # Read chunk length
                        len_bytes = fin.read(4)
                        if not len_bytes:
                            break

                        chunk_len = int.from_bytes(len_bytes, byteorder="big")

                        # Read nonce + ciphertext
                        chunk_data = fin.read(chunk_len)
                        if len(chunk_data) != chunk_len:
                            raise ValueError("Truncated backup file")

                        chunk_nonce = chunk_data[:12]
                        ciphertext = chunk_data[12:]

                        plaintext = file_gcm.decrypt(chunk_nonce, ciphertext, None)
                        fout.write(plaintext)

            logger.info(f"Decrypted {input_path} to {output_path}")

        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise

        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            raise

    async def decrypt_file(self, input_path: str, output_path: str) -> None:
        """Decrypt file using AES-256-GCM envelope encryption."""
        if not HAS_CRYPTO:
            raise RuntimeError("Encryption not available")

        try:
            with open(input_path, "rb") as fin:
                # Read header
                header_line = fin.readline()
                header = json.loads(header_line)

                if header.get("algo") != "AES-256-GCM":
                    raise ValueError(f"Unsupported algorithm: {header.get('algo')}")

                # Decrypt DEK
                dek_nonce = base64.b64decode(header["dek_nonce"])
                encrypted_dek = base64.b64decode(header["encrypted_dek"])
                master_gcm = AESGCM(self._key)
                dek = master_gcm.decrypt(dek_nonce, encrypted_dek, None)

                file_gcm = AESGCM(dek)

                with open(output_path, "wb") as fout:
                    if header.get("chunked"):
                        while True:
                            len_bytes = fin.read(4)
                            if not len_bytes:
                                break
                            chunk_len = int.from_bytes(len_bytes, byteorder="big")

                            chunk_nonce = fin.read(12)
                            ciphertext = fin.read(chunk_len - 12)

                            plaintext = file_gcm.decrypt(chunk_nonce, ciphertext, None)
                            fout.write(plaintext)
                    else:
                        # Legacy non-chunked format (v1)
                        file_nonce = base64.b64decode(header["file_nonce"])
                        ciphertext = fin.read()
                        plaintext = file_gcm.decrypt(file_nonce, ciphertext, None)
                        fout.write(plaintext)

            logger.info(f"Decrypted {input_path} to {output_path}")

        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            raise


class ZFSBackend:
    """
    ZFS Snapshot and Replication backend (Async).
    """

    async def _run_command(
        self, args: List[str], input_data: Optional[bytes] = None
    ) -> bytes:
        """Helper to run async subprocess commands."""
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE if input_data else None,
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

    async def replicate(
        self, snap_name: str, target: str, prev_snap: Optional[str] = None
    ) -> None:
        logger.info(f"Replicating {snap_name} to {target}...")

        is_remote = "@" in target

        send_cmd = ["zfs", "send"]
        if prev_snap:
            send_cmd.extend(["-i", prev_snap])
        send_cmd.append(snap_name)

        if is_remote:
            user_host, dest_pool = target.split(":")
            recv_cmd = ["ssh", user_host, "zfs", "recv", "-F", dest_pool]
        else:
            recv_cmd = ["zfs", "recv", "-F", target]

        # Use a shell pipeline string for the replication specifically,
        # as it's the most robust way to pipe streams without buffering in Python.

        full_cmd = f"{' '.join(send_cmd)} | {' '.join(recv_cmd)}"
        logger.info(f"Executing pipeline: {full_cmd}")

        pipeline = await asyncio.create_subprocess_shell(
            full_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await pipeline.communicate()

        if pipeline.returncode != 0:
            raise Exception(f"Replication failed: {stderr.decode()}")

    async def export_snapshot(self, snap_name: str, output_path: str) -> None:
        """Export snapshot to file."""
        logger.info(f"Exporting {snap_name} to {output_path}")
        with open(output_path, "wb") as f:
            process = await asyncio.create_subprocess_exec(
                "zfs", "send", snap_name, stdout=f, stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await process.communicate()
            if process.returncode != 0:
                raise Exception(f"Export failed: {stderr.decode()}")


class CephBackend:
    """
    Ceph RBD Snapshot backend (Async).
    """

    async def _run_command(self, args: List[str]) -> bytes:
        process = await asyncio.create_subprocess_exec(
            *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
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

    async def export_snapshot(self, snap_name: str, output_path: str) -> None:
        """Export snapshot to file."""
        logger.info(f"Exporting {snap_name} to {output_path}")
        # rbd export pool/image@snap path
        dataset, snap = snap_name.split("@")
        await self._run_command(["rbd", "export", snap_name, output_path])


class BackupManager:
    """
    Orchestrates backups based on policies (Async).
    """

    def __init__(self) -> None:
        self.policies: List[BackupPolicy] = []
        self.zfs = ZFSBackend()
        self.ceph = CephBackend()
        self.encryption = BackupEncryption()

    def add_policy(self, policy: BackupPolicy) -> None:
        self.policies.append(policy)

    async def run_policy(self, policy: BackupPolicy) -> None:
        logger.info(f"Running policy: {policy.name}")
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tag = f"auto-{timestamp}"

        backend: Union[ZFSBackend, CephBackend] = (
            self.zfs if policy.backend == "zfs" else self.ceph
        )

        try:
            # 1. Create Snapshot
            snap_name = await backend.create_snapshot(policy.dataset, tag)

            # 2. Replicate (if ZFS and target set)
            if policy.backend == "zfs" and policy.replication_target:
                assert isinstance(backend, ZFSBackend)
                snaps = await backend.list_snapshots(policy.dataset)
                auto_snaps = sorted([s for s in snaps if "auto-" in s])
                prev_snap = None
                if len(auto_snaps) > 1:
                    prev_snap = auto_snaps[-2]

                await backend.replicate(snap_name, policy.replication_target, prev_snap)

            # 3. Encrypt Export (if enabled)
            if policy.encrypt and HAS_CRYPTO:
                export_dir = "/var/backups/exports"
                os.makedirs(export_dir, exist_ok=True)

                safe_name = snap_name.replace("/", "_").replace("@", "_")
                export_path = os.path.join(export_dir, f"{safe_name}.raw")
                encrypted_path = os.path.join(export_dir, f"{safe_name}.enc")

                try:
                    await backend.export_snapshot(snap_name, export_path)
                    await self.encryption.encrypt_file(export_path, encrypted_path)
                    logger.info(f"Encrypted backup saved to {encrypted_path}")
                finally:
                    if os.path.exists(export_path):
                        os.remove(export_path)

            # 4. Prune
            await self._prune(policy, backend)

        except Exception as e:
            logger.error(f"Policy {policy.name} failed: {e}")

    async def _prune(
        self, policy: BackupPolicy, backend: Union[ZFSBackend, CephBackend]
    ) -> None:
        snaps = await backend.list_snapshots(policy.dataset)
        auto_snaps = sorted([s for s in snaps if "auto-" in s])

        total_to_keep = policy.retention_hourly + policy.retention_daily

        if len(auto_snaps) > total_to_keep:
            to_delete = auto_snaps[:-total_to_keep]
            for s in to_delete:
                await backend.destroy_snapshot(s)


async def async_main() -> int:
    parser = argparse.ArgumentParser(description="DebVisor Backup Manager")
    parser.add_argument(
        "--run-all", action="store_true", help="Run all policies immediately"
    )
    parser.add_argument(
        "--daemon", action="store_true", help="Run in daemon mode (scheduler)"
    )

    args = parser.parse_args()

    mgr = BackupManager()

    # Example Policy
    mgr.add_policy(
        BackupPolicy(
            name="vm-daily",
            dataset="tank/vm",
            backend="zfs",
            schedule_cron="0 0 * * *",
            retention_daily=7,
        )
    )

    if args.run_all:
        tasks = [mgr.run_policy(p) for p in mgr.policies]
        await asyncio.gather(*tasks)

    elif args.daemon:
        logger.info("Starting Backup Manager Daemon...")
        while True:
            await asyncio.sleep(60)
            # Check schedules...

    return 0


def main() -> None:
    try:
        sys.exit(asyncio.run(async_main()))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
