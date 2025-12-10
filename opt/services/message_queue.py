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

"""
Async Message Queue Service

Provides an abstraction for asynchronous message queuing, supporting both
in-memory (for development/testing) and Redis (for production) backends.

Author: DebVisor Development Team
Date: November 28, 2025
Version: 1.0.0
"""

import asyncio
import redis
import json
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable, Awaitable

logger = logging.getLogger("DebVisor.MessageQueue")

try:

    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False


class MessageQueue(ABC):
    """Abstract base class for message queues."""

    @abstractmethod
    async def publish(self, topic: str, message: Dict[str, Any]) -> str:
        """Publish a message to a topic.

        Args:
            topic: Topic name
            message: Message payload

        Returns:
            Message ID
        """
        pass

    @abstractmethod
    async def subscribe(
        self, topic: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]
    ) -> None:
        """Subscribe to a topic.

        Args:
            topic: Topic name
            callback: Async callback function to handle messages
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the connection."""
        pass


class InMemoryMessageQueue(MessageQueue):
    """
    In-memory message queue for development and testing.

    Provides a simple pub/sub implementation using Python data structures.
    Not suitable for production use - use RedisMessageQueue instead.

    Attributes:
        subscribers: Dict mapping topic names to callback lists
        running: Boolean indicating if queue is active
    """

    def __init__(self) -> None:
        """Initialize the in-memory message queue."""
        self.subscribers: Dict[str, list[Callable[[Dict[str, Any]], Awaitable[None]]]] = {}
        self.running = True

    async def publish(self, topic: str, message: Dict[str, Any]) -> str:
        """
        Publish a message to a topic.

        Args:
            topic: Topic name to publish to
            message: Message payload dictionary

        Returns:
            Generated message ID
        """
        msg_id = str(uuid.uuid4())
        message["_id"] = msg_id

        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                # Fire and forget in background task to simulate async decoupling
                asyncio.create_task(self._handle_message(callback, message))

        return msg_id

    async def _handle_message(
        self,
        callback: Callable[[Dict[str, Any]], Awaitable[None]],
        message: Dict[str, Any],
    ) -> None:
        """
        Handle message delivery to callback.

        Args:
            callback: Async callback function to invoke
            message: Message payload to deliver
        """
        try:
            await callback(message)
        except Exception as e:
            logger.error(f"Error processing message in memory queue: {e}")

    async def subscribe(
        self, topic: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]
    ) -> None:
        """
        Subscribe to a topic with a callback.

        Args:
            topic: Topic name to subscribe to
            callback: Async callback function to handle messages
        """
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        logger.info(f"Subscribed to in-memory topic: {topic}")

    async def close(self) -> None:
        """Close the message queue and clear subscribers."""
        self.running = False
        self.subscribers.clear()


class RedisMessageQueue(MessageQueue):
    """
    Redis-backed message queue for production.

    Provides a scalable pub/sub implementation using Redis.
    Requires the redis.asyncio package.

    Attributes:
        redis: Redis async client instance
        pubsub: Redis PubSub instance
        handlers: Dict mapping topic names to handler lists
        listen_task: Background task for listening to messages
    """

    def __init__(self, url: str = "redis://localhost:6379/0") -> None:
        """
        Initialize Redis message queue.

        Args:
            url: Redis connection URL

        Raises:
            ImportError: If redis package is not installed
        """
        if not HAS_REDIS:
            raise ImportError("redis package is required for RedisMessageQueue")
        self.redis = redis.from_url(url, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.handlers: Dict[str, list[Callable[[Dict[str, Any]], Awaitable[None]]]] = {}
        self.listen_task: Optional[asyncio.Task[None]] = None

    async def publish(self, topic: str, message: Dict[str, Any]) -> str:
        """
        Publish a message to a Redis topic.

        Args:
            topic: Topic name to publish to
            message: Message payload dictionary

        Returns:
            Generated message ID
        """
        msg_id = str(uuid.uuid4())
        message["_id"] = msg_id
        await self.redis.publish(topic, json.dumps(message))
        return msg_id

    async def subscribe(
        self, topic: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]
    ) -> None:
        """
        Subscribe to a Redis topic.

        Args:
            topic: Topic name to subscribe to
            callback: Async callback function to handle messages
        """
        if topic not in self.handlers:
            self.handlers[topic] = []
            await self.pubsub.subscribe(topic)

        self.handlers[topic].append(callback)

        if not self.listen_task:
            self.listen_task = asyncio.create_task(self._listen())

        logger.info(f"Subscribed to Redis topic: {topic}")

    async def _listen(self) -> None:
        """
        Listen loop for Redis PubSub.

        Continuously listens for messages and dispatches them to handlers.
        Runs until cancelled or an error occurs.
        """
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    topic = message["channel"]
                    data = message["data"]
                    try:
                        payload = json.loads(data)
                        if topic in self.handlers:
                            for handler in self.handlers[topic]:
                                asyncio.create_task(
                                    self._handle_message(handler, payload)
                                )
                    except json.JSONDecodeError:
                        logger.error(f"Failed to decode message on topic {topic}")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Redis listener error: {e}")

    async def _handle_message(
        self,
        callback: Callable[[Dict[str, Any]], Awaitable[None]],
        message: Dict[str, Any],
    ) -> None:
        """
        Handle message delivery to callback.

        Args:
            callback: Async callback function to invoke
            message: Message payload to deliver
        """
        try:
            await callback(message)
        except Exception as e:
            logger.error(f"Error processing message from Redis: {e}")

    async def close(self) -> None:
        """Close Redis connection and stop listener."""
        if self.listen_task:
            self.listen_task.cancel()
            try:
                await self.listen_task
            except asyncio.CancelledError:
                pass

        # mypy thinks this is unreachable for some reason
        await self.pubsub.close()
        await self.redis.close()    # type: ignore[unreachable]


_queue_instance: Optional[MessageQueue] = None


def get_message_queue(
    backend: str = "memory", redis_url: Optional[str] = None
) -> MessageQueue:
    """Get or create the global message queue instance.

    Args:
        backend: 'memory' or 'redis'
        redis_url: Redis connection URL (if backend='redis')

    Returns:
        MessageQueue instance
    """
    global _queue_instance

    if _queue_instance is None:
        if backend == "redis" and HAS_REDIS:
            try:
                _queue_instance = RedisMessageQueue(
                    url=redis_url or "redis://localhost:6379/0"
                )
                logger.info("Initialized Redis message queue")
            except Exception as e:
                logger.warning(
                    f"Failed to init Redis queue, falling back to memory: {e}"
                )
                _queue_instance = InMemoryMessageQueue()
        else:
            _queue_instance = InMemoryMessageQueue()
            logger.info("Initialized in-memory message queue")

    return _queue_instance
