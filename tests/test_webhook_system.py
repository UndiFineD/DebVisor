#!/usr/bin/env python3
"""
Unit tests for webhook system.

Tests for:
  - Webhook registration and lifecycle
  - Event filtering and routing
  - Delivery management and retries
  - Event storage and replay
  - Webhook signatures
"""

import unittest
from datetime import datetime, timedelta, timezone


from webhook_system import (
    WebhookManager, EventStore, WebhookSigner, WebhookFilter,
    Event, EventType, WebhookStatus, DeliveryStatus
)


class TestWebhookSigner(unittest.TestCase):
    """Tests for webhook signing."""

    def test_sign_payload(self):
        """Test signing payload."""
        payload = '{"event": "test"}'
        secret = "test_secret"

        signature = WebhookSigner.sign(payload, secret)

        self.assertTrue(signature.startswith("sha256="))

    def test_verify_valid_signature(self):
        """Test verifying valid signature."""
        payload = '{"event": "test"}'
        secret = "test_secret"

        signature = WebhookSigner.sign(payload, secret)
        valid = WebhookSigner.verify(payload, secret, signature)

        self.assertTrue(valid)

    def test_verify_invalid_signature(self):
        """Test rejecting invalid signature."""
        payload = '{"event": "test"}'
        secret = "test_secret"

        valid = WebhookSigner.verify(payload, secret, "sha256=invalid")

        self.assertFalse(valid)

    def test_verify_different_secret(self):
        """Test signature with different secret."""
        payload = '{"event": "test"}'
        signature = WebhookSigner.sign(payload, "secret1")

        valid = WebhookSigner.verify(payload, "secret2", signature)

        self.assertFalse(valid)


class TestWebhookFilter(unittest.TestCase):
    """Tests for webhook filtering."""

    def test_filter_by_event_type(self):
        """Test filtering by event type."""
        filter_obj = WebhookFilter(
            event_types=[EventType.OPERATION_COMPLETED]
        )

        event1 = Event(
            id="1", type=EventType.OPERATION_COMPLETED,
            timestamp=datetime.now(timezone.utc), resource_type="op",
            resource_id="op1", data={}
        )

        event2 = Event(
            id="2", type=EventType.OPERATION_FAILED,
            timestamp=datetime.now(timezone.utc), resource_type="op",
            resource_id="op2", data={}
        )

        self.assertTrue(filter_obj.matches(event1))
        self.assertFalse(filter_obj.matches(event2))

    def test_filter_by_resource_type(self):
        """Test filtering by resource type."""
        filter_obj = WebhookFilter(
            resource_types=["cluster", "node"]
        )

        event1 = Event(
            id="1", type=EventType.CLUSTER_CREATED,
            timestamp=datetime.now(timezone.utc), resource_type="cluster",
            resource_id="c1", data={}
        )

        event2 = Event(
            id="2", type=EventType.CONFIG_CHANGED,
            timestamp=datetime.now(timezone.utc), resource_type="config",
            resource_id="cfg1", data={}
        )

        self.assertTrue(filter_obj.matches(event1))
        self.assertFalse(filter_obj.matches(event2))

    def test_empty_filter_matches_all(self):
        """Test empty filter matches all events."""
        filter_obj = WebhookFilter()

        event = Event(
            id="1", type=EventType.CLUSTER_CREATED,
            timestamp=datetime.now(timezone.utc), resource_type="cluster",
            resource_id="c1", data={}
        )

        self.assertTrue(filter_obj.matches(event))


class TestWebhookManager(unittest.TestCase):
    """Tests for webhook manager."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = WebhookManager()

    def test_register_webhook(self):
        """Test webhook registration."""
        filter_obj = WebhookFilter(
            event_types=[EventType.OPERATION_COMPLETED]
        )

        webhook = self.manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        self.assertIsNotNone(webhook)
        self.assertIn(webhook.id, self.manager.webhooks)

    def test_unregister_webhook(self):
        """Test webhook unregistration."""
        filter_obj = WebhookFilter()
        webhook = self.manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        success = self.manager.unregister_webhook(webhook.id)

        self.assertTrue(success)
        self.assertNotIn(webhook.id, self.manager.webhooks)

    def test_update_webhook(self):
        """Test updating webhook."""
        filter_obj = WebhookFilter()
        webhook = self.manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        updated = self.manager.update_webhook(
            webhook.id,
            status=WebhookStatus.INACTIVE
        )

        self.assertEqual(updated.status, WebhookStatus.INACTIVE)

    def test_get_webhook(self):
        """Test getting webhook."""
        filter_obj = WebhookFilter()
        webhook = self.manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        retrieved = self.manager.get_webhook(webhook.id)

        self.assertEqual(retrieved.id, webhook.id)

    def test_list_webhooks(self):
        """Test listing webhooks."""
        filter_obj = WebhookFilter()
        _webhook1 = self.manager.register_webhook(
            "https://example.com/webhook1",
            filter_obj
        )
        _webhook2 = self.manager.register_webhook(
            "https://example.com/webhook2",
            filter_obj
        )

        webhooks = self.manager.list_webhooks()

        self.assertEqual(len(webhooks), 2)

    def test_trigger_event(self):
        """Test triggering event."""
        filter_obj = WebhookFilter(
            event_types=[EventType.OPERATION_COMPLETED]
        )
        _webhook = self.manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        event = Event(
            id="1", type=EventType.OPERATION_COMPLETED,
            timestamp=datetime.now(timezone.utc), resource_type="op",
            resource_id="op1", data={}
        )

        triggered = self.manager.trigger_event(event)

        self.assertEqual(triggered, 1)

    def test_trigger_event_no_match(self):
        """Test event trigger with no matching webhooks."""
        filter_obj = WebhookFilter(
            event_types=[EventType.CLUSTER_CREATED]
        )
        _webhook = self.manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        event = Event(
            id="1", type=EventType.OPERATION_COMPLETED,
            timestamp=datetime.now(timezone.utc), resource_type="op",
            resource_id="op1", data={}
        )

        triggered = self.manager.trigger_event(event)

        self.assertEqual(triggered, 0)

    def test_record_delivery_success(self):
        """Test recording successful delivery."""
        filter_obj = WebhookFilter()
        _webhook = self.manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        event = Event(
            id="1", type=EventType.OPERATION_COMPLETED,
            timestamp=datetime.now(timezone.utc), resource_type="op",
            resource_id="op1", data={}
        )

        self.manager.trigger_event(event)

        deliveries = self.manager.list_deliveries()
        self.assertGreater(len(deliveries), 0)

        delivery = deliveries[0]
        self.manager.record_delivery(delivery, 200, '{"result": "ok"}')

        self.assertEqual(delivery.status, DeliveryStatus.SUCCESS)

    def test_record_delivery_failure_retry(self):
        """Test retry on delivery failure."""
        filter_obj = WebhookFilter()
        _webhook = self.manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        event = Event(
            id="1", type=EventType.OPERATION_COMPLETED,
            timestamp=datetime.now(timezone.utc), resource_type="op",
            resource_id="op1", data={}
        )

        self.manager.trigger_event(event)

        deliveries = self.manager.list_deliveries()
        delivery = deliveries[0]

        self.manager.record_delivery(
            delivery, 500, error="Internal server error")

        self.assertEqual(delivery.status, DeliveryStatus.RETRYING)

    def test_get_pending_retries(self):
        """Test getting pending retries."""
        filter_obj = WebhookFilter()
        _webhook = self.manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        event = Event(
            id="1", type=EventType.OPERATION_COMPLETED,
            timestamp=datetime.now(timezone.utc), resource_type="op",
            resource_id="op1", data={}
        )

        self.manager.trigger_event(event)

        deliveries = self.manager.list_deliveries()
        delivery = deliveries[0]

        self.manager.record_delivery(delivery, 500, error="Error")

        # Manually move next_retry_at to past
        delivery.next_retry_at = datetime.now(
            timezone.utc) - timedelta(seconds=1)
        self.manager.retry_queue.append(delivery)

        pending = self.manager.get_pending_retries()

        self.assertGreater(len(pending), 0)

    def test_replay_event(self):
        """Test event replay."""
        filter_obj = WebhookFilter()
        self.manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        count = self.manager.replay_event("event_123")

        self.assertEqual(count, 1)


class TestEventStore(unittest.TestCase):
    """Tests for event store."""

    def setUp(self):
        """Set up test fixtures."""
        self.store = EventStore()

    def test_store_event(self):
        """Test storing event."""
        event = Event(
            id="1", type=EventType.CLUSTER_CREATED,
            timestamp=datetime.now(timezone.utc), resource_type="cluster",
            resource_id="c1", data={}
        )

        event_id = self.store.store_event(event)

        self.assertEqual(event_id, "1")

    def test_get_event(self):
        """Test retrieving event."""
        event = Event(
            id="1", type=EventType.CLUSTER_CREATED,
            timestamp=datetime.now(timezone.utc), resource_type="cluster",
            resource_id="c1", data={}
        )

        self.store.store_event(event)
        retrieved = self.store.get_event("1")

        self.assertEqual(retrieved.id, "1")

    def test_list_events(self):
        """Test listing events."""
        event1 = Event(
            id="1", type=EventType.CLUSTER_CREATED,
            timestamp=datetime.now(timezone.utc), resource_type="cluster",
            resource_id="c1", data={}
        )
        event2 = Event(
            id="2", type=EventType.NODE_CORDONED,
            timestamp=datetime.now(timezone.utc), resource_type="node",
            resource_id="n1", data={}
        )

        self.store.store_event(event1)
        self.store.store_event(event2)

        events = self.store.list_events()

        self.assertEqual(len(events), 2)

    def test_filter_by_event_type(self):
        """Test filtering events by type."""
        event1 = Event(
            id="1", type=EventType.CLUSTER_CREATED,
            timestamp=datetime.now(timezone.utc), resource_type="cluster",
            resource_id="c1", data={}
        )
        event2 = Event(
            id="2", type=EventType.NODE_CORDONED,
            timestamp=datetime.now(timezone.utc), resource_type="node",
            resource_id="n1", data={}
        )

        self.store.store_event(event1)
        self.store.store_event(event2)

        events = self.store.list_events(event_type=EventType.CLUSTER_CREATED)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].type, EventType.CLUSTER_CREATED)

    def test_cleanup_expired_events(self):
        """Test cleaning up expired events."""
        old_time = datetime.now(timezone.utc) - timedelta(days=31)
        event = Event(
            id="1", type=EventType.CLUSTER_CREATED,
            timestamp=old_time, resource_type="cluster",
            resource_id="c1", data={}
        )

        self.store.store_event(event)
        cleaned = self.store.cleanup_expired_events()

        self.assertEqual(cleaned, 1)
        self.assertIsNone(self.store.get_event("1"))


class TestWebhookIntegration(unittest.TestCase):
    """Integration tests."""

    def test_end_to_end_webhook_flow(self):
        """Test complete webhook flow."""
        manager = WebhookManager()
        store = EventStore()

        # Register webhook
        filter_obj = WebhookFilter(
            event_types=[EventType.OPERATION_COMPLETED]
        )
        _webhook = manager.register_webhook(
            "https://example.com/webhook",
            filter_obj
        )

        # Create and store event
        event = Event(
            id="1", type=EventType.OPERATION_COMPLETED,
            timestamp=datetime.now(timezone.utc), resource_type="deployment",
            resource_id="app-1", data={"status": "success"}
        )

        store.store_event(event)

        # Trigger event
        triggered = manager.trigger_event(event)

        self.assertEqual(triggered, 1)

    def test_multiple_webhooks_same_event(self):
        """Test multiple webhooks receiving same event."""
        manager = WebhookManager()

        filter_obj = WebhookFilter(
            event_types=[EventType.OPERATION_COMPLETED]
        )
        _webhook1 = manager.register_webhook(
            "https://example.com/webhook1",
            filter_obj
        )
        _webhook2 = manager.register_webhook(
            "https://example.com/webhook2",
            filter_obj
        )

        event = Event(
            id="1", type=EventType.OPERATION_COMPLETED,
            timestamp=datetime.now(timezone.utc), resource_type="op",
            resource_id="op1", data={}
        )

        triggered = manager.trigger_event(event)

        self.assertEqual(triggered, 2)


if __name__ == "__main__":
    unittest.main()
