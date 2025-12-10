"""
WebSocket real-time notifications for DebVisor Web Panel.

Provides real-time updates for:
- Node status changes
- Cluster alerts
- Job progress
- Storage metrics
- Error notifications

Features:
- Event-based message delivery
- Permission-based filtering
- Client subscription management
- Automatic reconnection support
- Message queuing
"""

import asyncio
from datetime import datetime
import json
import logging
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Supported event types."""

    NODE_STATUS = "node_status"
    NODE_METRICS = "node_metrics"
    NODE_HEALTH = "node_health"
    CLUSTER_ALERT = "cluster_alert"
    JOB_PROGRESS = "job_progress"
    JOB_COMPLETE = "job_complete"
    STORAGE_METRIC = "storage_metric"
    ERROR = "error"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"


@dataclass
class WebSocketEvent:
    """WebSocket event message."""

    event_type: str
    timestamp: str
    data: Dict[str, Any]
    source: str = "system"
    severity: str = "info"    # info, warning, error, critical

    def to_json(self) -> str:
        """Convert event to JSON."""
        return json.dumps(asdict(self))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebSocketEvent":
        """Create event from dictionary."""
        return cls(
            event_type=data.get("event_type", "unknown"),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            data=data.get("data", {}),
            source=data.get("source", "system"),
            severity=data.get("severity", "info"),
        )


@dataclass
class ClientSubscription:
    """Client subscription to events."""

    client_id: str
    event_types: Set[str]
    user_id: str
    permissions: Set[str]    # RBAC permissions
    subscribed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.subscribed_at is None:
            self.subscribed_at = datetime.now(timezone.utc)

    def is_allowed(self, event: WebSocketEvent) -> bool:
        """Check if client is allowed to receive event."""
        # Check event type subscription
        if event.event_type not in self.event_types:
            return False

        # Check permissions (RBAC)
        # For now, simple permission check
        required_permission = f"view:{event.event_type}"
        if (
            required_permission not in self.permissions
            and "view:*" not in self.permissions
        ):
            return False

        return True


class WebSocketEventBus:
    """
    Manages WebSocket event distribution.

    Handles client subscriptions, event filtering, and message delivery.
    """

    def __init__(self) -> None:
        """Initialize event bus."""
        self.subscriptions: Dict[str, ClientSubscription] = {}
        self.event_handlers: Dict[str, List[Callable[..., Any]]] = {}
        self.message_queues: Dict[str, asyncio.Queue[WebSocketEvent]] = {}
        self.lock = asyncio.Lock()
        self.event_history: List[WebSocketEvent] = []
        self.max_history_size = 1000

    async def subscribe(
        self,
        client_id: str,
        event_types: List[str],
        user_id: str,
        permissions: List[str],
    ) -> ClientSubscription:
        """
        Subscribe client to events.

        Args:
            client_id: Unique client identifier
            event_types: List of event types to subscribe to
            user_id: User ID (for RBAC)
            permissions: User permissions

        Returns:
            ClientSubscription instance
        """
        async with self.lock:
            subscription = ClientSubscription(
                client_id=client_id,
                event_types=set(event_types),
                user_id=user_id,
                permissions=set(permissions),
            )

            self.subscriptions[client_id] = subscription

            # Create message queue for client
            if client_id not in self.message_queues:
                self.message_queues[client_id] = asyncio.Queue()

            logger.info(
                f"Client {client_id} subscribed to {event_types} "
                f"with permissions {permissions}"
            )
            return subscription

    async def unsubscribe(self, client_id: str) -> None:
        """
        Unsubscribe client from events.

        Args:
            client_id: Client identifier
        """
        async with self.lock:
            if client_id in self.subscriptions:
                del self.subscriptions[client_id]

            if client_id in self.message_queues:
                del self.message_queues[client_id]

            logger.info(f"Client {client_id} unsubscribed")

    async def publish(self, event: WebSocketEvent) -> None:
        """
        Publish event to subscribed clients.

        Args:
            event: WebSocketEvent to publish
        """
        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history_size:
            self.event_history.pop(0)

        # Distribute to subscribed clients
        async with self.lock:
            for client_id, subscription in self.subscriptions.items():
                if subscription.is_allowed(event):
                    queue = self.message_queues.get(client_id)
                    if queue:
                        try:
                            queue.put_nowait(event)
                        except asyncio.QueueFull:
                            logger.warning(
                                f"Message queue full for client {client_id}, "
                                "dropping message"
                            )

        logger.debug(
            f"Published event {event.event_type} to {len(self.subscriptions)} clients"
        )

    async def get_message(
        self, client_id: str, timeout: Optional[float] = 30.0
    ) -> Optional[WebSocketEvent]:
        """
        Get next message for client.

        Args:
            client_id: Client identifier
            timeout: Timeout in seconds (None = wait indefinitely)

        Returns:
            WebSocketEvent or None if timeout

        Raises:
            KeyError: If client not subscribed
        """
        queue = self.message_queues.get(client_id)
        if queue is None:
            raise KeyError(f"Client {client_id} not subscribed")

        try:
            if timeout:
                event = await asyncio.wait_for(queue.get(), timeout=timeout)
            else:
                event = await queue.get()
            return event
        except asyncio.TimeoutError:
            return None

    async def register_handler(self, event_type: str, handler: Callable[..., Any]) -> None:
        """
        Register handler for event type.

        Args:
            event_type: Event type
            handler: Callable to handle event
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []

        self.event_handlers[event_type].append(handler)
        logger.debug(f"Registered handler for event type {event_type}")

    async def get_client_count(self) -> int:
        """Get number of connected clients."""
        async with self.lock:
            return len(self.subscriptions)

    async def get_subscribed_clients(self, event_type: str) -> List[ClientSubscription]:
        """
        Get clients subscribed to event type.

        Args:
            event_type: Event type

        Returns:
            List of subscribed clients
        """
        async with self.lock:
            return [
                sub
                for sub in self.subscriptions.values()
                if event_type in sub.event_types
            ]


class EventFactory:
    """Factory for creating WebSocket events."""

    @staticmethod
    def node_status_event(
        node_id: str, status: str, details: Optional[Dict[str, Any]] = None
    ) -> WebSocketEvent:
        """Create node status event."""
        return WebSocketEvent(
            event_type=EventType.NODE_STATUS.value,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={
                "node_id": node_id,
                "status": status,
                "details": details or {},
            },
            severity="info",
        )

    @staticmethod
    def node_metrics_event(node_id: str, metrics: Dict[str, Any]) -> WebSocketEvent:
        """Create node metrics event."""
        return WebSocketEvent(
            event_type=EventType.NODE_METRICS.value,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={
                "node_id": node_id,
                "metrics": metrics,
            },
            severity="info",
        )

    @staticmethod
    def alert_event(
        alert_type: str, message: str, severity: str = "warning"
    ) -> WebSocketEvent:
        """Create alert event."""
        return WebSocketEvent(
            event_type=EventType.CLUSTER_ALERT.value,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={
                "alert_type": alert_type,
                "message": message,
            },
            severity=severity,
        )

    @staticmethod
    def job_progress_event(job_id: str, progress: int, status: str) -> WebSocketEvent:
        """Create job progress event."""
        return WebSocketEvent(
            event_type=EventType.JOB_PROGRESS.value,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={
                "job_id": job_id,
                "progress": progress,    # 0-100
                "status": status,
            },
        )

    @staticmethod
    def storage_metric_event(
        pool_id: str, used: int, total: int, usage_percent: float
    ) -> WebSocketEvent:
        """Create storage metric event."""
        return WebSocketEvent(
            event_type=EventType.STORAGE_METRIC.value,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={
                "pool_id": pool_id,
                "used_bytes": used,
                "total_bytes": total,
                "usage_percent": usage_percent,
            },
        )

    @staticmethod
    def error_event(message: str, error_code: Optional[str] = None) -> WebSocketEvent:
        """Create error event."""
        return WebSocketEvent(
            event_type=EventType.ERROR.value,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={
                "message": message,
                "error_code": error_code,
            },
            severity="error",
        )

    @staticmethod
    def heartbeat_event() -> WebSocketEvent:
        """Create heartbeat event (keep-alive)."""
        return WebSocketEvent(
            event_type=EventType.HEARTBEAT.value,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"status": "ok"},
        )


class WebSocketConnectionManager:
    """Manages WebSocket connections and lifecycle."""

    def __init__(self, event_bus: Optional[WebSocketEventBus] = None) -> None:
        """
        Initialize connection manager.

        Args:
            event_bus: WebSocketEventBus instance
        """
        self.event_bus = event_bus or WebSocketEventBus()
        self.connections: Dict[str, Any] = {}
        self.lock = asyncio.Lock()

    async def connect(
        self,
        client_id: str,
        websocket: Any,
        event_types: List[str],
        user_id: str,
        permissions: List[str],
    ) -> None:
        """
        Register a new WebSocket connection.

        Args:
            client_id: Unique client ID
            websocket: WebSocket connection object
            event_types: Event types to subscribe to
            user_id: User ID
            permissions: User permissions
        """
        async with self.lock:
            self.connections[client_id] = websocket

        await self.event_bus.subscribe(client_id, event_types, user_id, permissions)

        logger.info(f"Client {client_id} connected")

    async def disconnect(self, client_id: str) -> None:
        """
        Close a WebSocket connection.

        Args:
            client_id: Client ID
        """
        async with self.lock:
            if client_id in self.connections:
                del self.connections[client_id]

        await self.event_bus.unsubscribe(client_id)
        logger.info(f"Client {client_id} disconnected")

    async def send_to_client(self, client_id: str, event: WebSocketEvent) -> bool:
        """
        Send event to specific client.

        Args:
            client_id: Client ID
            event: Event to send

        Returns:
            True if sent successfully, False if client not connected
        """
        async with self.lock:
            websocket = self.connections.get(client_id)

        if websocket is None:
            return False

        try:
            await websocket.send(event.to_json())
            return True
        except Exception as e:
            logger.error(f"Error sending to client {client_id}: {e}")
            return False

    async def broadcast_event(self, event: WebSocketEvent) -> None:
        """
        Broadcast event to all subscribed clients.

        Args:
            event: Event to broadcast
        """
        await self.event_bus.publish(event)

    async def get_connection_count(self) -> int:
        """Get number of connected clients."""
        async with self.lock:
            return len(self.connections)
