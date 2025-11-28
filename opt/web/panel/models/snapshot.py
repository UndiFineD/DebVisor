"""Snapshot Model - Storage Snapshot Tracking

Stores snapshot information with relationships to nodes and source VMs.
Tracks snapshot state, size, and lifecycle.
"""

from datetime import datetime, timezone
from app import db


class Snapshot(db.Model):
    """Storage snapshot information model."""
    
    __tablename__ = 'snapshot'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Snapshot identification
    snapshot_id = db.Column(db.String(36), unique=True, nullable=False, index=True)  # UUID from RPC
    name = db.Column(db.String(255), nullable=False, index=True)
    
    # Relationships
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'), nullable=False, index=True)
    
    # Source information
    source_vm = db.Column(db.String(255), nullable=True)  # Source VM identifier
    source_volume = db.Column(db.String(255), nullable=True)  # Source volume/disk
    
    # Snapshot details
    description = db.Column(db.Text, nullable=True)
    size_gb = db.Column(db.Float)
    
    # Status tracking
    status = db.Column(db.String(20), default='pending', index=True)  # pending, success, failed, deleting
    progress_percent = db.Column(db.Integer, default=0)
    
    # Metadata
    retention_days = db.Column(db.Integer)  # Days to retain
    is_encrypted = db.Column(db.Boolean, default=True)
    checksum = db.Column(db.String(64), nullable=True)  # SHA256 of snapshot
    
    # Timing
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime, nullable=True, index=True)
    
    def __repr__(self):
        """String representation of Snapshot."""
        return f'<Snapshot {self.name} on {self.node.hostname} - {self.status}>'
    
    def is_complete(self):
        """Check if snapshot is complete.
        
        Returns:
            True if status is 'success' and progress is 100%
        """
        return self.status == 'success' and self.progress_percent == 100
    
    def is_expired(self):
        """Check if snapshot is past expiration time.
        
        Returns:
            True if expires_at is in past
        """
        if not self.expires_at:
            return False
        return datetime.now(timezone.utc) > self.expires_at
    
    def update_progress(self, percent, status=None):
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
    
    def mark_complete(self, checksum=None):
        """Mark snapshot as complete.
        
        Args:
            checksum: Optional SHA256 checksum
        """
        self.status = 'success'
        self.progress_percent = 100
        self.checksum = checksum
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
    
    def mark_failed(self, error_message=None):
        """Mark snapshot as failed.
        
        Args:
            error_message: Optional error details (stored in description)
        """
        self.status = 'failed'
        if error_message:
            self.description = f"Error: {error_message}"
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
    
    def to_dict(self, include_node=False):
        """Convert snapshot to dictionary for JSON responses.
        
        Args:
            include_node: Whether to include node information
            
        Returns:
            Dictionary representation of snapshot
        """
        data = {
            'id': self.id,
            'snapshot_id': self.snapshot_id,
            'name': self.name,
            'node_id': self.node_id,
            'source_vm': self.source_vm,
            'source_volume': self.source_volume,
            'size_gb': self.size_gb,
            'status': self.status,
            'progress_percent': self.progress_percent,
            'is_complete': self.is_complete(),
            'is_expired': self.is_expired(),
            'is_encrypted': self.is_encrypted,
            'retention_days': self.retention_days,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
        }
        if include_node:
            data['node'] = self.node.to_dict()
        return data
    
    @staticmethod
    def get_by_snapshot_id(snapshot_id):
        """Get snapshot by snapshot_id (UUID from RPC).
        
        Args:
            snapshot_id: Snapshot UUID to search for
            
        Returns:
            Snapshot instance or None
        """
        return Snapshot.query.filter_by(snapshot_id=snapshot_id).first()
    
    @staticmethod
    def get_node_snapshots(node_id, status=None):
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
        return query.order_by(Snapshot.created_at.desc()).all()
    
    @staticmethod
    def get_expired_snapshots():
        """Get all snapshots past their retention date.
        
        Returns:
            List of expired Snapshot instances
        """
        now = datetime.now(timezone.utc)
        return Snapshot.query.filter(Snapshot.expires_at < now).all()
    
    @staticmethod
    def get_pending_snapshots():
        """Get all snapshots in progress.
        
        Returns:
            List of pending Snapshot instances
        """
        return Snapshot.query.filter_by(status='pending').all()
