"""
Comprehensive audit logging for DebVisor Web Panel.

Tracks all administrative actions, access patterns, and security events.
"""

import json
import logging
from typing import Any, Dict, Optional
from datetime import datetime, timezone
from enum import Enum
from functools import wraps
from flask import request, g
from flask_login import current_user

logger = logging.getLogger(__name__)


class AuditEventType(Enum):
    """Types of audit events."""
    # Authentication events
    LOGIN_SUCCESS = 'auth.login.success'
    LOGIN_FAILURE = 'auth.login.failure'
    LOGOUT = 'auth.logout'
    TOKEN_GENERATED = 'auth.token.generated'
    SESSION_CREATED = 'auth.session.created'
    SESSION_EXPIRED = 'auth.session.expired'
    
    # User management events
    USER_CREATED = 'user.created'
    USER_UPDATED = 'user.updated'
    USER_DELETED = 'user.deleted'
    USER_DISABLED = 'user.disabled'
    ROLE_CHANGED = 'user.role_changed'
    
    # Node management events
    NODE_REGISTERED = 'node.registered'
    NODE_UPDATED = 'node.updated'
    NODE_DELETED = 'node.deleted'
    NODE_HEARTBEAT = 'node.heartbeat'
    NODE_METRICS_ACCESSED = 'node.metrics_accessed'
    
    # Snapshot events
    SNAPSHOT_CREATED = 'snapshot.created'
    SNAPSHOT_DELETED = 'snapshot.deleted'
    SNAPSHOT_RESTORED = 'snapshot.restored'
    SNAPSHOT_ACCESSED = 'snapshot.accessed'
    
    # Permission events
    PERMISSION_DENIED = 'security.permission_denied'
    UNAUTHORIZED_ACCESS = 'security.unauthorized_access'
    
    # System events
    CONFIG_CHANGED = 'system.config_changed'
    SYSTEM_STATE_CHANGED = 'system.state_changed'


class AuditLevel(Enum):
    """Audit logging levels."""
    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'


class AuditLogger:
    """Log audit events for compliance and security."""
    
    def __init__(self, app=None):
        self.app = app
        self.handlers = []
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize audit logger with Flask app."""
        self.app = app
        
        # Create audit log handler
        audit_file = app.config.get('AUDIT_LOG_FILE', '/var/log/debvisor/audit.log')
        file_handler = logging.FileHandler(audit_file)
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%SZ'
            )
        )
        
        self.audit_logger = logging.getLogger('debvisor.audit')
        self.audit_logger.addHandler(file_handler)
        self.audit_logger.setLevel(logging.INFO)
    
    def log_event(
        self,
        event_type: AuditEventType,
        level: AuditLevel = AuditLevel.INFO,
        user_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        action: Optional[str] = None,
        status: str = 'success',
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """
        Log an audit event.
        
        Args:
            event_type: Type of event
            level: Logging level
            user_id: ID of user performing action
            resource_type: Type of resource affected
            resource_id: ID of resource affected
            action: Action performed
            status: Status (success, failure)
            details: Additional event details
            ip_address: Client IP address
            user_agent: Client user agent
        """
        if not user_id and current_user.is_authenticated:
            user_id = current_user.id
        
        if not ip_address:
            ip_address = request.remote_addr if request else 'unknown'
        
        if not user_agent:
            user_agent = request.headers.get('User-Agent', 'unknown') if request else 'unknown'
        
        event = {
            'timestamp': datetime.now(timezone.utc).isoformat() + 'Z',
            'event_type': event_type.value,
            'level': level.value,
            'user_id': user_id,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'action': action,
            'status': status,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'details': details or {}
        }
        
        # Log as JSON for easy parsing
        log_entry = json.dumps(event, default=str)
        log_func = {
            AuditLevel.INFO: self.audit_logger.info,
            AuditLevel.WARNING: self.audit_logger.warning,
            AuditLevel.CRITICAL: self.audit_logger.critical
        }[level]
        
        log_func(log_entry)
        
        # Also store in database if configured
        if self.app.config.get('STORE_AUDIT_IN_DB'):
            self._store_event_in_db(event)
    
    def _store_event_in_db(self, event: Dict[str, Any]):
        """Store audit event in database."""
        try:
            from opt.web.panel.models import AuditLog, db
            
            audit_log = AuditLog(
                user_id=event.get('user_id'),
                event_type=event['event_type'],
                resource_type=event.get('resource_type'),
                resource_id=event.get('resource_id'),
                action=event.get('action'),
                status=event['status'],
                ip_address=event['ip_address'],
                user_agent=event['user_agent'],
                details=json.dumps(event.get('details', {}))
            )
            db.session.add(audit_log)
            db.session.commit()
        except Exception as e:
            logger.error(f"Failed to store audit event in database: {str(e)}")


def audit_event(
    event_type: AuditEventType,
    level: AuditLevel = AuditLevel.INFO,
    resource_type: Optional[str] = None,
    extract_id: Optional[str] = None
):
    """
    Decorator to automatically log audit events for route handlers.
    
    Args:
        event_type: Type of audit event
        level: Logging level
        resource_type: Type of resource being modified
        extract_id: Parameter name to extract resource ID from kwargs
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from opt.web.panel.app import audit_logger
            
            resource_id = kwargs.get(extract_id) if extract_id else None
            
            try:
                result = func(*args, **kwargs)
                
                audit_logger.log_event(
                    event_type=event_type,
                    level=level,
                    resource_type=resource_type,
                    resource_id=resource_id,
                    action=func.__name__,
                    status='success'
                )
                
                return result
            
            except Exception as e:
                audit_logger.log_event(
                    event_type=event_type,
                    level=AuditLevel.WARNING,
                    resource_type=resource_type,
                    resource_id=resource_id,
                    action=func.__name__,
                    status='failure',
                    details={'error': str(e)}
                )
                raise
        
        return wrapper
    return decorator


def log_authentication_event(
    user_id: str,
    success: bool,
    ip_address: str,
    user_agent: str,
    reason: Optional[str] = None
):
    """Log authentication event."""
    from opt.web.panel.app import audit_logger
    
    event_type = AuditEventType.LOGIN_SUCCESS if success else AuditEventType.LOGIN_FAILURE
    level = AuditLevel.INFO if success else AuditLevel.WARNING
    
    audit_logger.log_event(
        event_type=event_type,
        level=level,
        user_id=user_id,
        action='login',
        status='success' if success else 'failure',
        ip_address=ip_address,
        user_agent=user_agent,
        details={'reason': reason} if reason else None
    )


def log_permission_denied(
    resource_type: str,
    resource_id: Optional[str],
    action: str,
    reason: str
):
    """Log permission denied event."""
    from opt.web.panel.app import audit_logger
    
    audit_logger.log_event(
        event_type=AuditEventType.PERMISSION_DENIED,
        level=AuditLevel.WARNING,
        resource_type=resource_type,
        resource_id=resource_id,
        action=action,
        status='denied',
        details={'reason': reason}
    )


# Example route decorators using audit logging
def setup_audit_routes(app):
    """Setup example routes with audit logging."""
    from flask import jsonify
    
    @app.route('/nodes/<node_id>', methods=['DELETE'])
    @audit_event(
        AuditEventType.NODE_DELETED,
        level=AuditLevel.CRITICAL,
        resource_type='node',
        extract_id='node_id'
    )
    def delete_node(node_id):
        """Delete node with audit logging."""
        # Implementation
        return jsonify({'success': True})
    
    @app.route('/users', methods=['POST'])
    @audit_event(
        AuditEventType.USER_CREATED,
        level=AuditLevel.CRITICAL,
        resource_type='user'
    )
    def create_user():
        """Create user with audit logging."""
        # Implementation
        return jsonify({'user_id': '123'}), 201


# Audit log retrieval
class AuditLogQuery:
    """Query audit logs."""
    
    @staticmethod
    def get_events(
        event_type: Optional[AuditEventType] = None,
        user_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ):
        """Query audit log events."""
        from opt.web.panel.models import AuditLog
        
        query = AuditLog.query
        
        if event_type:
            query = query.filter_by(event_type=event_type.value)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        
        if start_time:
            query = query.filter(AuditLog.created_at >= start_time)
        
        if end_time:
            query = query.filter(AuditLog.created_at <= end_time)
        
        return query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_user_activity(user_id: str, days: int = 30):
        """Get user activity for specified period."""
        from opt.web.panel.models import AuditLog
        from datetime import timedelta, timezone
        
        start_time = datetime.now(timezone.utc) - timedelta(days=days)
        
        return AuditLog.query.filter_by(
            user_id=user_id
        ).filter(
            AuditLog.created_at >= start_time
        ).order_by(
            AuditLog.created_at.desc()
        ).all()
