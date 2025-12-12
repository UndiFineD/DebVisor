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


"""Snapshot Model - Storage Snapshot Tracking

Stores snapshot information with relationships to nodes and source VMs.
Tracks snapshot state, size, and lifecycle.
"""

from typing import Any, Optional, List, Dict
from datetime import datetime, timezone
from opt.web.panel.extensions import db


class Snapshot(db.Model):
    """Storage snapshot information model."""

    __tablename__ = "snapshot"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Snapshot identification
    snapshot_id = db.Column(
        db.String(36), unique=True, nullable=False, index=True
    )    # UUID from RPC
    name = db.Column(db.String(255), nullable=False, index=True)

    # Relationships
    node_id = db.Column(
        db.Integer, db.ForeignKey("node.id"), nullable=False, index=True
    )

    # Source information
    source_vm = db.Column(db.String(255), nullable=True, index=True)    # Source VM identifier
    source_volume = db.Column(db.String(255), nullable=True)    # Source volume/disk

    # Snapshot details
    description = db.Column(db.Text, nullable=True)
    size_gb = db.Column(db.Float)

    # Status tracking
    # pending, success, failed, deleting
    status = db.Column(db.String(20), default="pending", index=True)
    progress_percent = db.Column(db.Integer, default=0)

    # Metadata
    retention_days = db.Column(db.Integer)    # Days to retain
    is_encrypted = db.Column(db.Boolean, default=True)
    checksum = db.Column(db.String(64), nullable=True)    # SHA256 of snapshot

    # Timing
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    expires_at = db.Column(db.DateTime, nullable=True, index=True)

    def __repr__(self) -> str:
        """String representation of Snapshot."""
        return f"<Snapshot {self.name} on {self.node.hostname} - {self.status}>"

    def is_complete(self) -> bool:
        """Check if snapshot is complete.

        Returns:
            True if status is 'success' and progress is 100%
        """
        return bool(self.status == "success" and self.progress_percent == 100)

    def is_expired(self) -> bool:
        """Check if snapshot is past expiration time.

        Returns:
            True if expires_at is in past
        """
        if not self.expires_at:
            return False
        return bool(datetime.now(timezone.utc) > self.expires_at)

    def update_progress(self, percent: int, status: Optional[str] = None) -> None:
        """Update snapshot progress.

        Args:
            percent: Progress percentage (0-100)
            status: Optional status update
        """
        self.progress_percent = min(100, max(0, percent))
        if status:
            self.status = status
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()

    def mark_complete(self, checksum: Optional[str] = None) -> None:
        """Mark snapshot as complete.

        Args:
            checksum: Optional SHA256 checksum
        """
        self.status = "success"
        self.progress_percent = 100
        self.checksum = checksum
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()

    def mark_failed(self, error_message: Optional[str] = None) -> None:
        """Mark snapshot as failed.

        Args:
            error_message: Optional error details (stored in description)
        """
        self.status = "failed"
        if error_message:
            self.description = f"Error: {error_message}"
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()

    def to_dict(self, include_node: bool = False) -> Dict[str, Any]:
        """Convert snapshot to dictionary for JSON responses.

        Args:
            include_node: Whether to include node information

        Returns:
            Dictionary representation of snapshot
        """
        data = {
            "id": self.id,
            "snapshot_id": self.snapshot_id,
            "name": self.name,
            "node_id": self.node_id,
            "source_vm": self.source_vm,
            "source_volume": self.source_volume,
            "size_gb": self.size_gb,
            "status": self.status,
            "progress_percent": self.progress_percent,
            "is_complete": self.is_complete(),
            "is_expired": self.is_expired(),
            "is_encrypted": self.is_encrypted,
            "retention_days": self.retention_days,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }
        if include_node:
            data["node"] = self.node.to_dict()
        return data

    @staticmethod
    def get_by_snapshot_id(snapshot_id: str) -> Optional['Snapshot']:
        """Get snapshot by snapshot_id (UUID from RPC).

        Args:
            snapshot_id: Snapshot UUID to search for

        Returns:
            Snapshot instance or None
        """
        return Snapshot.query.filter_by(snapshot_id=snapshot_id).first()    # type: ignore

    @staticmethod
    def get_node_snapshots(node_id: int, status: Optional[str] = None) -> List['Snapshot']:
        """Get all snapshots for a node.

        Args:
            node_id: Node ID to filter by
            status: Optional status filter

        Returns:
            List of Snapshot instances
        """
        query = Snapshot.query.filter_by(node_id=node_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Snapshot.created_at.desc()).all()    # type: ignore

    @staticmethod
    def get_expired_snapshots() -> List['Snapshot']:
        """Get all snapshots past their retention date.

        Returns:
            List of expired Snapshot instances
        """
        now = datetime.now(timezone.utc)
        return Snapshot.query.filter(Snapshot.expires_at < now).all()    # type: ignore

    @staticmethod
    def get_pending_snapshots() -> List['Snapshot']:
        """Get all snapshots in progress.

        Returns:
            List of pending Snapshot instances
        """
        return Snapshot.query.filter_by(status="pending").all()    # type: ignore
