"""Node Model - Infrastructure Node Tracking

Stores cluster node information synchronized from RPC service.
Tracks node status, capabilities, and metadata.
"""

from typing import Any, Optional, List, Dict
from datetime import datetime
from opt.web.panel.extensions import db


class Node(db.Model):
    """Cluster node information model."""

    __tablename__ = "node"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Node identification
    node_id = db.Column(
        db.String(36), unique=True, nullable=False, index=True
    )    # UUID from RPC
    hostname = db.Column(db.String(253), nullable=False, index=True)    # FQDN
    ip_address = db.Column(db.String(45), nullable=False, index=True)    # IPv4 or IPv6
    mac_address = db.Column(db.String(17), nullable=True, index=True)

    # Node capabilities
    cpu_cores = db.Column(db.Integer)
    memory_gb = db.Column(db.Integer)
    storage_gb = db.Column(db.Integer)

    # Status tracking
    status = db.Column(
        db.String(20), default="unknown", index=True
    )    # online, offline, error
    last_heartbeat = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Metadata
    region = db.Column(db.String(100), nullable=True, index=True)
    rack = db.Column(db.String(100), nullable=True)
    labels = db.Column(db.Text, nullable=True)    # JSON-encoded labels

    # Tracking
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    snapshots = db.relationship(
        "Snapshot", backref="node", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of Node."""
        return f"<Node {self.hostname} ({self.status})>"

    def is_healthy(self) -> bool:
        """Check if node is considered healthy.

        Returns:
            True if last heartbeat within 5 minutes
        """
        if not self.last_heartbeat:
            return False
        elapsed = datetime.now(timezone.utc) - self.last_heartbeat
        return bool(elapsed.total_seconds() < 300)    # 5 minutes

    def update_heartbeat(self) -> None:
        """Update last heartbeat timestamp to current time."""
        self.last_heartbeat = datetime.now(timezone.utc)
        self.status = "online"
        db.session.commit()

    def to_dict(self, include_snapshots: bool = False) -> Dict[str, Any]:
        """Convert node to dictionary for JSON responses.

        Args:
            include_snapshots: Whether to include snapshot list

        Returns:
            Dictionary representation of node
        """
        data = {
            "id": self.id,
            "node_id": self.node_id,
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "mac_address": self.mac_address,
            "cpu_cores": self.cpu_cores,
            "memory_gb": self.memory_gb,
            "storage_gb": self.storage_gb,
            "status": self.status,
            "is_healthy": self.is_healthy(),
            "last_heartbeat": (
                self.last_heartbeat.isoformat() if self.last_heartbeat else None
            ),
            "region": self.region,
            "rack": self.rack,
            "created_at": self.created_at.isoformat(),
        }
        if include_snapshots:
            data["snapshots"] = [s.to_dict() for s in self.snapshots]
        return data

    @staticmethod
    def get_by_hostname(hostname: str) -> Optional['Node']:
        """Get node by hostname.

        Args:
            hostname: Hostname to search for

        Returns:
            Node instance or None
        """
        return Node.query.filter_by(hostname=hostname).first()    # type: ignore

    @staticmethod
    def get_by_node_id(node_id: str) -> Optional['Node']:
        """Get node by node_id (UUID from RPC).

        Args:
            node_id: Node UUID to search for

        Returns:
            Node instance or None
        """
        return Node.query.filter_by(node_id=node_id).first()    # type: ignore

    @staticmethod
    def get_healthy_nodes() -> List['Node']:
        """Get all nodes with active heartbeats.

        Returns:
            List of healthy Node instances
        """
        nodes = Node.query.filter_by(status="online").all()
        return [n for n in nodes if n.is_healthy()]

    @staticmethod
    def get_offline_nodes() -> List['Node']:
        """Get all nodes that are offline.

        Returns:
            List of offline Node instances
        """
        return Node.query.filter_by(status="offline").all()    # type: ignore
