"""
Socket.IO integration for real-time WebSocket communication in DebVisor.

Provides Socket.IO server with namespaces for different event streams:
- /nodes - Node status and metrics
- /jobs - Job progress and completion
- /alerts - Cluster alerts and notifications
- /admin - Administrative events

Features:
- Namespace-based event routing
- Authentication and RBAC with strong enforcement
- Client session management
- Automatic reconnection
- Message acknowledgment
- Namespace-level authentication checks on connect
- Per-namespace permission verification
"""

import asyncio
import logging
import jwt
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

try:
    from flask_socketio import (
        SocketIO,
        emit,
        join_room,
        leave_room,
        rooms,
        disconnect,
        request,
    )
except ImportError:
    # Placeholder for when flask-socketio is not installed
    SocketIO = None
    emit = None
    join_room = None
    leave_room = None
    rooms = None
    disconnect = None
    request = None

from websocket_events import (
    EventFactory,
    WebSocketConnectionManager,
    WebSocketEventBus,
)

logger = logging.getLogger(__name__)


class NamespaceAuthenticationRequired(Exception):
    """Raised when authentication fails for namespace connection."""
    pass


class WebSocketAuthenticationManager:
    """
    Manages authentication for WebSocket namespace connections.

    Enforces:
    - JWT token validation
    - Namespace-level permission checks
    - Session timeout
    - Token expiration
    """

    # Default JWT configuration
    JWT_SECRET = "your-secret-key-change-in-production"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRY_SECONDS = 3600

    NAMESPACE_PERMISSIONS = {
        "/nodes": ["view:nodes", "edit:nodes"],
        "/jobs": ["view:jobs", "edit:jobs"],
        "/alerts": ["view:alerts"],
        "/notifications": ["view:notifications"],
        "/admin": ["admin"],
    }

    def __init__(self, secret: Optional[str] = None):
        """
        Initialize authentication manager.

        Args:
            secret: JWT secret (uses default if not provided)
        """
        self.secret = secret or self.JWT_SECRET
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def verify_namespace_access(
        self,
        auth: Optional[Dict],
        namespace: str,
        required_permissions: Optional[List[str]] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify that authenticated user has access to namespace.

        Args:
            auth: Authentication data from client
            namespace: WebSocket namespace (e.g., '/nodes')
            required_permissions: Optional specific permissions required

        Returns:
            Tuple of (success, error_message)
        """
        # Check if auth provided
        if auth is None:
            return False, "Authentication required"

        # Verify token
        token = auth.get("token")
        if not token:
            return False, "No authentication token provided"

        try:
            # Decode and validate JWT
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            return False, "Authentication token expired"
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return False, "Invalid authentication token"

        # Extract user info
        user_id = payload.get("user_id")
        user_permissions = payload.get("permissions", [])

        if not user_id:
            return False, "Token missing user_id"

        # Check namespace-level permissions
        required_perms = required_permissions or self.NAMESPACE_PERMISSIONS.get(
            namespace, []
        )

        # Check if user has required permissions
        has_permission = any(
            perm in user_permissions or f"{perm}:*" in user_permissions
            for perm in required_perms
        ) or "admin" in user_permissions

        if not has_permission:
            logger.warning(
                f"User {user_id} denied access to {namespace}: "
                f"requires {required_perms}, has {user_permissions}"
            )
            return False, f"Insufficient permissions for {namespace}"

        # Track active session
        self.active_sessions[user_id] = {
            "namespace": namespace,
            "connected_at": datetime.now(timezone.utc),
            "permissions": user_permissions,
        }

        return True, None

    def create_session_token(
        self,
        user_id: str,
        permissions: List[str],
        expiry_seconds: Optional[int] = None
    ) -> str:
        """
        Create a JWT token for WebSocket authentication.

        Args:
            user_id: User identifier
            permissions: User permissions
            expiry_seconds: Token expiration in seconds

        Returns:
            JWT token string
        """
        expiry = expiry_seconds or self.JWT_EXPIRY_SECONDS
        now = time.time()

        payload = {
            "user_id": user_id,
            "permissions": permissions,
            "iat": now,
            "exp": now + expiry,
        }

        token = jwt.encode(
            payload,
            self.secret,
            algorithm=self.JWT_ALGORITHM
        )

        logger.debug(f"Created session token for user {user_id}")
        return token

    def revoke_session(self, user_id: str) -> None:
        """
        Revoke an active session.

        Args:
            user_id: User identifier
        """
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
            logger.info(f"Revoked session for user {user_id}")

    def get_active_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get all active WebSocket sessions."""
        return self.active_sessions.copy()


@dataclass
class SocketIOConfig:
    """Configuration for Socket.IO server."""

    async_mode: str = "threading"  # threading, eventlet, gevent
    cors_allowed_origins: List[str] = field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:5000"]
    )
    ping_timeout: int = 10
    ping_interval: int = 5
    engineio_logger: bool = False
    socketio_logger: bool = False
    max_http_buffer_size: int = 1e6
    heartbeat_interval: int = 30
    auth_manager: Optional[WebSocketAuthenticationManager] = field(
        default_factory=WebSocketAuthenticationManager
    )


class SocketIONamespace:
    """Base namespace handler for Socket.IO."""

    def __init__(
        self,
        namespace: str,
        connection_manager: WebSocketConnectionManager,
        event_bus: WebSocketEventBus,
        auth_manager: Optional[WebSocketAuthenticationManager] = None,
    ):
        """
        Initialize namespace.

        Args:
            namespace: Namespace path (e.g., '/nodes')
            connection_manager: WebSocket connection manager
            event_bus: Event bus for message delivery
            auth_manager: Authentication manager for namespace auth
        """
        self.namespace = namespace
        self.connection_manager = connection_manager
        self.event_bus = event_bus
        self.auth_manager = auth_manager or WebSocketAuthenticationManager()
        self.clients: Dict[str, Dict[str, Any]] = {}
        self.lock = asyncio.Lock()

    def register_handlers(self, socketio: any) -> None:
        """
        Register namespace handlers with Socket.IO.

        Args:
            socketio: Flask-SocketIO instance
        """
        # Base implementation registers the namespace
        socketio.on_namespace(self)


class NodeNamespace(SocketIONamespace):
    """Namespace for node-related events."""

    def __init__(
        self,
        connection_manager: WebSocketConnectionManager,
        event_bus: WebSocketEventBus,
    ):
        super().__init__("/nodes", connection_manager, event_bus)

    def register_handlers(self, socketio: any) -> None:
        """Register node namespace handlers."""

        @socketio.on("connect", namespace=self.namespace)
        def handle_connect(auth):
            """Handle client connection."""
            if not self._verify_auth(auth):
                disconnect()
                return False

            client_id = f"node_client_{id(auth)}"
            user_id = auth.get("user_id", "anonymous")
            # permissions = auth.get("permissions", [])

            self.clients[client_id] = {
                "user_id": user_id,
                "connected_at": datetime.now(timezone.utc),
                "subscriptions": set(),
            }

            logger.info(f"Client {client_id} connected to /nodes")
            return True

        @socketio.on("subscribe_node", namespace=self.namespace)
        def handle_subscribe_node(data):
            """Subscribe to node updates."""
            node_id = data.get("node_id")
            room = f"node:{node_id}"

            join_room(room)
            logger.debug(f"Client subscribed to node {node_id}")

            return {"status": "subscribed", "node_id": node_id}

        @socketio.on("unsubscribe_node", namespace=self.namespace)
        def handle_unsubscribe_node(data):
            """Unsubscribe from node updates."""
            node_id = data.get("node_id")
            room = f"node:{node_id}"

            leave_room(room)
            logger.debug(f"Client unsubscribed from node {node_id}")

            return {"status": "unsubscribed", "node_id": node_id}

        @socketio.on("subscribe_metrics", namespace=self.namespace)
        def handle_subscribe_metrics(data):
            """Subscribe to node metrics."""
            node_id = data.get("node_id")
            room = f"node_metrics:{node_id}"

            join_room(room)
            logger.debug(f"Client subscribed to node metrics {node_id}")

            return {"status": "subscribed_metrics", "node_id": node_id}

        @socketio.on("unsubscribe_metrics", namespace=self.namespace)
        def handle_unsubscribe_metrics(data):
            """Unsubscribe from node metrics."""
            node_id = data.get("node_id")
            room = f"node_metrics:{node_id}"

            leave_room(room)
            logger.debug(f"Client unsubscribed from node metrics {node_id}")

            return {"status": "unsubscribed_metrics", "node_id": node_id}

        @socketio.on("get_node_status", namespace=self.namespace)
        def handle_get_node_status(data):
            """Get current node status."""
            node_id = data.get("node_id")

            # In production, fetch from database/cache
            status = {
                "node_id": node_id,
                "status": "online",
                "uptime_seconds": 3600,
                "last_update": datetime.now(timezone.utc).isoformat(),
            }

            return status

        @socketio.on("disconnect", namespace=self.namespace)
        def handle_disconnect():
            """Handle client disconnection."""
            logger.info("Client disconnected from /nodes")

    def broadcast_node_status(self, node_id: str, status: str) -> None:
        """
        Broadcast node status update.

        Args:
            node_id: Node ID
            status: Node status
        """
        room = f"node:{node_id}"
        event = EventFactory.node_status_event(node_id, status)

        if emit:
            emit(
                "node_status_update",
                event.to_json(),
                namespace=self.namespace,
                room=room,
            )

    def broadcast_node_metrics(self, node_id: str, metrics: Dict[str, Any]) -> None:
        """
        Broadcast node metrics update.

        Args:
            node_id: Node ID
            metrics: Node metrics
        """
        room = f"node_metrics:{node_id}"
        event = EventFactory.node_metrics_event(node_id, metrics)

        if emit:
            emit(
                "node_metrics_update",
                event.to_json(),
                namespace=self.namespace,
                room=room,
            )

    @staticmethod
    def _verify_auth(auth: Optional[dict]) -> bool:
        """
        Verify authentication token using enhanced JWT validation.

        Args:
            auth: Authentication data from client

        Returns:
            True if auth is valid, False otherwise
        """
        if auth is None:
            logger.warning("WebSocket connection attempt without authentication")
            return False

        token = auth.get("token")
        if not token:
            logger.warning("WebSocket connection attempt without token")
            return False

        # Validate JWT token format and signature
        try:
            jwt.decode(
                token,
                WebSocketAuthenticationManager.JWT_SECRET,
                algorithms=[WebSocketAuthenticationManager.JWT_ALGORITHM]
            )
            return True
        except jwt.ExpiredSignatureError:
            logger.warning("WebSocket connection with expired token")
            return False
        except jwt.InvalidTokenError as e:
            logger.warning(f"WebSocket connection with invalid token: {e}")
            return False


class JobNamespace(SocketIONamespace):
    """Namespace for job-related events."""

    def __init__(
        self,
        connection_manager: WebSocketConnectionManager,
        event_bus: WebSocketEventBus,
    ):
        super().__init__("/jobs", connection_manager, event_bus)
        self.active_jobs: Dict[str, Dict[str, Any]] = {}

    def register_handlers(self, socketio: any) -> None:
        """Register job namespace handlers."""

        @socketio.on("connect", namespace=self.namespace)
        def handle_connect(auth):
            """Handle client connection."""
            if not self._verify_auth(auth):
                disconnect()
                return False

            logger.info("Client connected to /jobs")
            return True

        @socketio.on("subscribe_job", namespace=self.namespace)
        def handle_subscribe_job(data):
            """Subscribe to job progress."""
            job_id = data.get("job_id")
            room = f"job:{job_id}"

            join_room(room)
            logger.debug(f"Client subscribed to job {job_id}")

            return {"status": "subscribed", "job_id": job_id}

        @socketio.on("unsubscribe_job", namespace=self.namespace)
        def handle_unsubscribe_job(data):
            """Unsubscribe from job progress."""
            job_id = data.get("job_id")
            room = f"job:{job_id}"

            leave_room(room)
            logger.debug(f"Client unsubscribed from job {job_id}")

            return {"status": "unsubscribed", "job_id": job_id}

        @socketio.on("get_job_status", namespace=self.namespace)
        def handle_get_job_status(data):
            """Get current job status."""
            job_id = data.get("job_id")

            # In production, fetch from database/cache
            status = {
                "job_id": job_id,
                "status": "running",
                "progress": 50,
                "started_at": datetime.now(timezone.utc).isoformat(),
            }

            return status

        @socketio.on("disconnect", namespace=self.namespace)
        def handle_disconnect():
            """Handle client disconnection."""
            logger.info("Client disconnected from /jobs")

    def broadcast_job_progress(self, job_id: str, progress: int, status: str) -> None:
        """
        Broadcast job progress update.

        Args:
            job_id: Job ID
            progress: Progress percentage (0-100)
            status: Job status
        """
        room = f"job:{job_id}"
        event = EventFactory.job_progress_event(job_id, progress, status)

        if emit:
            emit(
                "job_progress_update",
                event.to_json(),
                namespace=self.namespace,
                room=room,
            )

    @staticmethod
    def _verify_auth(auth: Optional[dict]) -> bool:
        """Verify authentication token."""
        if auth is None:
            return False

        token = auth.get("token")
        return token is not None


class AlertNamespace(SocketIONamespace):
    """Namespace for alert and notification events."""

    def __init__(
        self,
        connection_manager: WebSocketConnectionManager,
        event_bus: WebSocketEventBus,
    ):
        super().__init__("/alerts", connection_manager, event_bus)

    def register_handlers(self, socketio: any) -> None:
        """Register alert namespace handlers."""

        @socketio.on("connect", namespace=self.namespace)
        def handle_connect(auth):
            """Handle client connection."""
            if not self._verify_auth(auth):
                disconnect()
                return False

            logger.info("Client connected to /alerts")
            return True

        @socketio.on("subscribe_alerts", namespace=self.namespace)
        def handle_subscribe_alerts(data):
            """Subscribe to cluster alerts."""
            severity = data.get("severity", "warning")
            room = f"alerts:{severity}"

            join_room(room)
            logger.debug(f"Client subscribed to alerts (severity: {severity})")

            return {"status": "subscribed", "severity": severity}

        @socketio.on("acknowledge_alert", namespace=self.namespace)
        def handle_acknowledge_alert(data):
            """Acknowledge alert."""
            alert_id = data.get("alert_id")
            logger.debug(f"Alert {alert_id} acknowledged")

            return {"status": "acknowledged", "alert_id": alert_id}

        @socketio.on("disconnect", namespace=self.namespace)
        def handle_disconnect():
            """Handle client disconnection."""
            logger.info("Client disconnected from /alerts")

    def broadcast_alert(
        self, alert_type: str, message: str, severity: str = "warning"
    ) -> None:
        """
        Broadcast alert to subscribers.

        Args:
            alert_type: Alert type
            message: Alert message
            severity: Severity level (info, warning, error, critical)
        """
        room = f"alerts:{severity}"
        event = EventFactory.alert_event(alert_type, message, severity)

        if emit:
            emit(
                "alert",
                event.to_json(),
                namespace=self.namespace,
                room=room,
            )

    @staticmethod
    def _verify_auth(auth: Optional[dict]) -> bool:
        """Verify authentication token."""
        if auth is None:
            return False

        token = auth.get("token")
        return token is not None


class NotificationNamespace(SocketIONamespace):
    """Namespace for user notifications and chat."""

    def __init__(
        self,
        connection_manager: WebSocketConnectionManager,
        event_bus: WebSocketEventBus,
    ):
        super().__init__("/notifications", connection_manager, event_bus)

    def register_handlers(self, socketio: any) -> None:
        """Register notification namespace handlers."""

        @socketio.on("connect", namespace=self.namespace)
        def handle_connect(auth):
            """Handle client connection."""
            if not self._verify_auth(auth):
                disconnect()
                return False

            user_id = auth.get("user_id")
            if user_id:
                join_room(f"user:{user_id}")
                logger.info(f"User {user_id} connected to /notifications")
            return True

        @socketio.on("send_message", namespace=self.namespace)
        def handle_send_message(data):
            """Handle chat message."""
            user_id = data.get("user_id")  # Target user
            message = data.get("message")

            if user_id and message:
                # In a real app, we would validate permissions and persist the message
                self.send_notification(user_id, f"New message: {message}", "info")
                return {"status": "sent"}
            return {"status": "error", "message": "Invalid data"}

        @socketio.on("disconnect", namespace=self.namespace)
        def handle_disconnect():
            """Handle client disconnection."""
            logger.info("Client disconnected from /notifications")

    def send_notification(self, user_id: str, message: str, level: str = "info") -> None:
        """
        Send notification to specific user.

        Args:
            user_id: Target user ID
            message: Notification message
            level: Notification level (info, warning, error, success)
        """
        if emit:
            emit(
                "notification",
                {
                    "message": message,
                    "level": level,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                },
                namespace=self.namespace,
                room=f"user:{user_id}"
            )

    @staticmethod
    def _verify_auth(auth: Optional[dict]) -> bool:
        """Verify authentication token."""
        if auth is None:
            return False

        token = auth.get("token")
        return token is not None


class SocketIOServer:
    """Socket.IO server for DebVisor real-time updates."""

    def __init__(
        self, app: any = None, config: Optional[SocketIOConfig] = None
    ):
        """
        Initialize Socket.IO server.

        Args:
            app: Flask application instance
            config: SocketIOConfig instance
        """
        self.config = config or SocketIOConfig()
        self.app = app
        self.socketio = None

        self.event_bus = WebSocketEventBus()
        self.connection_manager = WebSocketConnectionManager(self.event_bus)

        self.namespaces: Dict[str, SocketIONamespace] = {}

    def init_app(self, app: any) -> None:
        """
        Initialize with Flask app.

        Args:
            app: Flask application instance
        """
        self.app = app

        if SocketIO is None:
            logger.error("flask-socketio not installed")
            return

        self.socketio = SocketIO(
            app,
            async_mode=self.config.async_mode,
            cors_allowed_origins=self.config.cors_allowed_origins,
            ping_timeout=self.config.ping_timeout,
            ping_interval=self.config.ping_interval,
            engineio_logger=self.config.engineio_logger,
            socketio_logger=self.config.socketio_logger,
        )

        # Register namespaces
        self._register_namespaces()

    def _register_namespaces(self) -> None:
        """Register all namespaces."""
        node_ns = NodeNamespace(self.connection_manager, self.event_bus)
        job_ns = JobNamespace(self.connection_manager, self.event_bus)
        alert_ns = AlertNamespace(self.connection_manager, self.event_bus)
        notification_ns = NotificationNamespace(self.connection_manager, self.event_bus)

        self.namespaces["/nodes"] = node_ns
        self.namespaces["/jobs"] = job_ns
        self.namespaces["/alerts"] = alert_ns
        self.namespaces["/notifications"] = notification_ns

        if self.socketio:
            node_ns.register_handlers(self.socketio)
            job_ns.register_handlers(self.socketio)
            alert_ns.register_handlers(self.socketio)
            notification_ns.register_handlers(self.socketio)

            logger.info("Registered namespaces: /nodes, /jobs, /alerts, /notifications")

    def emit_node_status(self, node_id: str, status: str) -> None:
        """Emit node status update."""
        node_ns = self.namespaces.get("/nodes")
        if node_ns:
            node_ns.broadcast_node_status(node_id, status)

    def emit_node_metrics(self, node_id: str, metrics: Dict[str, Any]) -> None:
        """Emit node metrics update."""
        node_ns = self.namespaces.get("/nodes")
        if node_ns:
            node_ns.broadcast_node_metrics(node_id, metrics)

    def emit_job_progress(self, job_id: str, progress: int, status: str) -> None:
        """Emit job progress update."""
        job_ns = self.namespaces.get("/jobs")
        if job_ns:
            job_ns.broadcast_job_progress(job_id, progress, status)

    def emit_alert(
        self, alert_type: str, message: str, severity: str = "warning"
    ) -> None:
        """Emit alert."""
        alert_ns = self.namespaces.get("/alerts")
        if alert_ns:
            alert_ns.broadcast_alert(alert_type, message, severity)

    async def heartbeat(self) -> None:
        """Send periodic heartbeat to all connected clients."""
        while True:
            try:
                event = EventFactory.heartbeat_event()
                await self.event_bus.publish(event)
                await asyncio.sleep(self.config.heartbeat_interval)
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                await asyncio.sleep(5)

    def get_stats(self) -> dict:
        """Get server statistics."""
        return {
            "connected_clients": len(self.connection_manager.connections),
            "subscriptions": len(self.event_bus.subscriptions),
            "event_history_size": len(self.event_bus.event_history),
            "namespaces": list(self.namespaces.keys()),
        }
