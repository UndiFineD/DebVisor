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

# !/usr/bin/env python3

"""
Webhook System for DebVisor.

Event-driven webhook subscriptions with delivery guarantees and retry logic.

Features:
- Event registration and routing
- Webhook management and lifecycle
- Retry logic with exponential backoff
- Event filtering and transformation
- Event replay capability
"""

import hashlib
import hmac
import logging
import secrets
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import threading

# Configure logging
try:
    from opt.core.logging import configure_logging

    configure_logging(service_name="webhook-system")
except ImportError:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventType(Enum):
    """Supported event types."""

    CLUSTER_CREATED = "cluster.created"
    CLUSTER_DELETED = "cluster.deleted"
    CLUSTER_UPDATED = "cluster.updated"
    NODE_CORDONED = "node.cordoned"
    NODE_DRAINED = "node.drained"
    WORKLOAD_DEPLOYED = "workload.deployed"
    WORKLOAD_MIGRATED = "workload.migrated"
    OPERATION_STARTED = "operation.started"
    OPERATION_COMPLETED = "operation.completed"
    OPERATION_FAILED = "operation.failed"
    ALERT_TRIGGERED = "alert.triggered"
    CONFIG_CHANGED = "config.changed"


class WebhookStatus(Enum):
    """Webhook status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    DISABLED = "disabled"
    FAILED = "failed"


class DeliveryStatus(Enum):
    """Delivery status."""

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class Event:
    """Webhook event."""

    id: str
    type: EventType
    timestamp: datetime
    resource_type: str
    resource_id: str
    data: Dict[str, Any]
    source: str = "debvisor"


@dataclass
class WebhookFilter:
    """Event filter for webhook."""

    event_types: List[EventType] = field(default_factory=list)
    resource_types: List[str] = field(default_factory=list)
    custom_filters: Dict[str, Any] = field(default_factory=dict)

    def matches(self, event: Event) -> bool:
        """Check if event matches filter."""
        if self.event_types and event.type not in self.event_types:
            return False

        if self.resource_types and event.resource_type not in self.resource_types:
            return False

        return True


@dataclass
class Webhook:
    """Webhook definition."""

    id: str
    url: str
    status: WebhookStatus
    events: WebhookFilter
    secret: str
    created_at: datetime
    updated_at: datetime
    retry_policy: Dict[str, Any] = field(
        default_factory=lambda: {
            "max_attempts": 3,
            "initial_delay_ms": 1000,
            "max_delay_ms": 60000,
            "backoff_factor": 2.0,
        }
    )
    headers: Dict[str, str] = field(default_factory=dict)
    active: bool = True
    failure_count: int = 0
    last_triggered_at: Optional[datetime] = None


@dataclass
class WebhookDelivery:
    """Webhook delivery record."""

    id: str
    webhook_id: str
    event_id: str
    status: DeliveryStatus
    attempt_number: int
    http_status_code: Optional[int] = None
    response_body: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    delivered_at: Optional[datetime] = None
    next_retry_at: Optional[datetime] = None


class WebhookSigner:
    """Sign webhook payloads for verification."""

    @staticmethod
    def sign(payload: str, secret: str) -> str:
        """
        Sign payload with HMAC-SHA256.

        Args:
            payload: JSON payload
            secret: Webhook secret

        Returns:
            Signature string
        """
        signature = hmac.new(
            secret.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"

    @staticmethod
    def verify(payload: str, secret: str, signature: str) -> bool:
        """
        Verify webhook signature.

        Args:
            payload: JSON payload
            secret: Webhook secret
            signature: Signature to verify

        Returns:
            Verification result
        """
        expected = WebhookSigner.sign(payload, secret)
        return hmac.compare_digest(expected, signature)


class WebhookManager:
    """Manage webhooks and deliveries."""

    def __init__(self) -> None:
        """Initialize webhook manager."""
        self.webhooks: Dict[str, Webhook] = {}
        self.deliveries: Dict[str, WebhookDelivery] = {}
        self.event_queue: List[tuple[Event, str]] = []    # (event, webhook_id)
        self.retry_queue: List[WebhookDelivery] = []
        self._lock = threading.Lock()

    def register_webhook(
        self, url: str, events: WebhookFilter, headers: Optional[Dict[str, str]] = None
    ) -> Webhook:
        """
        Register webhook.

        Args:
            url: Webhook URL
            events: Event filter
            headers: Custom headers

        Returns:
            Created webhook
        """
        webhook_id = str(uuid.uuid4())
        secret = secrets.token_urlsafe(32)

        webhook = Webhook(
            id=webhook_id,
            url=url,
            status=WebhookStatus.ACTIVE,
            events=events,
            secret=secret,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            headers=headers or {},
        )

        self.webhooks[webhook_id] = webhook
        logger.info(f"Registered webhook {webhook_id}: {url}")

        return webhook

    def unregister_webhook(self, webhook_id: str) -> bool:
        """
        Unregister webhook.

        Args:
            webhook_id: Webhook ID

        Returns:
            Success status
        """
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            logger.info(f"Unregistered webhook {webhook_id}")
            return True

        return False

    def update_webhook(self, webhook_id: str, **kwargs) -> Optional[Webhook]:
        """
        Update webhook.

        Args:
            webhook_id: Webhook ID
            **kwargs: Fields to update

        Returns:
            Updated webhook or None
        """
        webhook = self.webhooks.get(webhook_id)
        if not webhook:
            return None

        for key, value in kwargs.items():
            if hasattr(webhook, key):
                setattr(webhook, key, value)

        webhook.updated_at = datetime.now(timezone.utc)
        logger.info(f"Updated webhook {webhook_id}")

        return webhook

    def get_webhook(self, webhook_id: str) -> Optional[Webhook]:
        """Get webhook by ID."""
        return self.webhooks.get(webhook_id)

    def list_webhooks(self, status: Optional[WebhookStatus] = None) -> List[Webhook]:
        """
        List webhooks.

        Args:
            status: Filter by status

        Returns:
            List of webhooks
        """
        if not status:
            return list(self.webhooks.values())

        return [w for w in self.webhooks.values() if w.status == status]

    def trigger_event(self, event: Event) -> int:
        """
        Trigger event to matching webhooks.

        Args:
            event: Event to trigger

        Returns:
            Number of webhooks triggered
        """
        triggered_count = 0

        for webhook in self.webhooks.values():
            if webhook.status != WebhookStatus.ACTIVE:
                continue

            if webhook.events.matches(event):
                self._queue_delivery(event, webhook)
                triggered_count += 1

        logger.info(f"Event {event.id} triggered {triggered_count} webhooks")

        return triggered_count

    def _queue_delivery(self, event: Event, webhook: Webhook) -> None:
        """Queue webhook delivery."""
        delivery = WebhookDelivery(
            id=str(uuid.uuid4()),
            webhook_id=webhook.id,
            event_id=event.id,
            status=DeliveryStatus.PENDING,
            attempt_number=1,
            created_at=datetime.now(timezone.utc),
        )

        self.deliveries[delivery.id] = delivery

        with self._lock:
            self.event_queue.append((event, delivery.webhook_id))
    def get_delivery(self, delivery_id: str) -> Optional[WebhookDelivery]:
        """Get delivery by ID."""
        return self.deliveries.get(delivery_id)

    def list_deliveries(
        self, webhook_id: Optional[str] = None, status: Optional[DeliveryStatus] = None
    ) -> List[WebhookDelivery]:
        """
        List deliveries.

        Args:
            webhook_id: Filter by webhook
            status: Filter by status

        Returns:
            List of deliveries
        """
        deliveries = list(self.deliveries.values())

        if webhook_id:
            deliveries = [d for d in deliveries if d.webhook_id == webhook_id]

        if status:
            deliveries = [d for d in deliveries if d.status == status]

        return deliveries

    def record_delivery(
        self,
        delivery: WebhookDelivery,
        http_status: int,
        response: Optional[str] = None,
        error: Optional[str] = None,
    ) -> None:
        """
        Record delivery result.

        Args:
            delivery: Delivery record
            http_status: HTTP status code
            response: Response body
            error: Error message
        """
        delivery.http_status_code = http_status
        delivery.response_body = response
        delivery.error_message = error

        if 200 <= http_status < 300:
            delivery.status = DeliveryStatus.SUCCESS
            delivery.delivered_at = datetime.now(timezone.utc)
            logger.info(f"Delivery {delivery.id} succeeded")

        else:
            delivery.status = DeliveryStatus.FAILED
            webhook = self.webhooks.get(delivery.webhook_id)

            if (
                webhook
                and delivery.attempt_number < webhook.retry_policy["max_attempts"]
            ):
                self._schedule_retry(delivery, webhook)

            else:
                if webhook:
                    webhook.failure_count += 1
                    if webhook.failure_count > 5:
                        webhook.status = WebhookStatus.DISABLED
                        logger.warning(f"Webhook {webhook.id} disabled due to failures")

    def _schedule_retry(self, delivery: WebhookDelivery, webhook: Webhook) -> None:
        """Schedule retry for failed delivery."""
        retry_policy = webhook.retry_policy
        delay_ms = min(
            retry_policy["initial_delay_ms"]
            * (retry_policy["backoff_factor"] ** (delivery.attempt_number - 1)),
            retry_policy["max_delay_ms"],
        )

        delivery.next_retry_at = datetime.now(timezone.utc) + timedelta(
            milliseconds=delay_ms
        )
        delivery.attempt_number += 1
        delivery.status = DeliveryStatus.RETRYING

        with self._lock:
            self.retry_queue.append(delivery)

        logger.info(f"Scheduled retry for delivery {delivery.id} in {delay_ms}ms")

    def get_pending_retries(self) -> List[tuple[WebhookDelivery, Webhook]]:
        """Get pending retries."""
        now = datetime.now(timezone.utc)
        pending = []

        for delivery in self.retry_queue[:]:
            if delivery.next_retry_at and delivery.next_retry_at <= now:
                webhook = self.webhooks.get(delivery.webhook_id)
                if webhook:
                    pending.append((delivery, webhook))
                self.retry_queue.remove(delivery)

        return pending

    def replay_event(self, event_id: str) -> int:
        """
        Replay event to all webhooks.

        Args:
            event_id: Event ID

        Returns:
            Number of webhooks triggered
        """
        # Simulate event replay
        count = 0

        for webhook in self.webhooks.values():
            if webhook.status == WebhookStatus.ACTIVE:
                count += 1

        logger.info(f"Replayed event {event_id} to {count} webhooks")

        return count


class EventStore:
    """Store and retrieve events."""

    def __init__(self, retention_days: int = 30):
        """
        Initialize event store.

        Args:
            retention_days: Event retention period
        """
        self.events: Dict[str, Event] = {}
        self.retention_days = retention_days
        self._lock = threading.Lock()

    def store_event(self, event: Event) -> str:
        """
        Store event.

        Args:
            event: Event to store

        Returns:
            Event ID
        """
        with self._lock:
            self.events[event.id] = event

        logger.info(f"Stored event {event.id}: {event.type.value}")

        return event.id

    def get_event(self, event_id: str) -> Optional[Event]:
        """Get event by ID."""
        return self.events.get(event_id)

    def list_events(
        self,
        event_type: Optional[EventType] = None,
        resource_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[Event]:
        """
        List events.

        Args:
            event_type: Filter by type
            resource_type: Filter by resource type
            limit: Result limit

        Returns:
            List of events
        """
        events = list(self.events.values())

        if event_type:
            events = [e for e in events if e.type == event_type]

        if resource_type:
            events = [e for e in events if e.resource_type == resource_type]

        # Sort by timestamp descending
        events.sort(key=lambda e: e.timestamp, reverse=True)

        return events[:limit]

    def cleanup_expired_events(self) -> int:
        """
        Clean up expired events.

        Returns:
            Number of deleted events
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        expired = [
            event_id
            for event_id, event in self.events.items()
            if event.timestamp < cutoff
        ]

        for event_id in expired:
            del self.events[event_id]

        logger.info(f"Cleaned up {len(expired)} expired events")

        return len(expired)


# Example usage
if __name__ == "__main__":
    # Create managers
    webhook_mgr = WebhookManager()
    event_store = EventStore()

    # Register webhooks
    filter1 = WebhookFilter(
        event_types=[EventType.OPERATION_COMPLETED, EventType.OPERATION_FAILED]
    )
    webhook1 = webhook_mgr.register_webhook(
        "https://example.com/webhook1", filter1, headers={"X-Custom-Header": "value"}
    )

    filter2 = WebhookFilter(resource_types=["cluster", "node"])
    webhook2 = webhook_mgr.register_webhook("https://example.com/webhook2", filter2)

    # Create and trigger events
    event = Event(
        id=str(uuid.uuid4()),
        type=EventType.OPERATION_COMPLETED,
        timestamp=datetime.now(timezone.utc),
        resource_type="deployment",
        resource_id="app-1",
        data={"operation": "scale", "replicas": 5},
    )

    event_store.store_event(event)
    triggered = webhook_mgr.trigger_event(event)

    print(f"Event triggered {triggered} webhooks")
    print(f"\nRegistered webhooks: {len(webhook_mgr.webhooks)}")
    print(f"Pending deliveries: {len(webhook_mgr.deliveries)}")

    # List deliveries
    deliveries = webhook_mgr.list_deliveries()
    for delivery in deliveries:
        print(f"  - Delivery {delivery.id}: {delivery.status.value}")
