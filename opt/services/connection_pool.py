#!/usr/bin/env python3
"""
Enterprise Connection Pool Manager for DebVisor.

Provides advanced connection pooling with health checks, circuit breakers,
connection draining, and metrics for Redis, PostgreSQL, and other backends.

Features:
- Health-aware connection pooling
- Circuit breaker integration
- Connection validation and recycling
- Metrics and monitoring
- Graceful shutdown with drain support
- Connection warming

Author: DebVisor Team
Date: November 28, 2025
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar, AsyncIterator

logger = logging.getLogger(__name__)

# Type variable for pooled connections
T = TypeVar("T")


# =============================================================================
# Enums & Constants
# =============================================================================


class PoolState(Enum):
    """Connection pool state."""

    INITIALIZING = "initializing"
    ACTIVE = "active"
    DRAINING = "draining"
    CLOSED = "closed"


class ConnectionState(Enum):
    """Individual connection state."""

    IDLE = "idle"
    IN_USE = "in_use"
    VALIDATING = "validating"
    RECYCLING = "recycling"
    CLOSED = "closed"


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class PoolConfig:
    """Connection pool configuration."""

    # Pool sizing
    min_connections: int = 5
    max_connections: int = 20

    # Connection lifecycle
    max_connection_age_seconds: float = 3600.0  # 1 hour
    idle_timeout_seconds: float = 300.0  # 5 minutes
    connection_timeout_seconds: float = 10.0

    # Health checking
    health_check_interval_seconds: float = 30.0
    validation_query_timeout_seconds: float = 5.0
    validation_on_borrow: bool = True
    validation_on_return: bool = False

    # Circuit breaker
    circuit_breaker_enabled: bool = True
    failure_threshold: int = 5
    recovery_timeout_seconds: float = 30.0

    # Warmup
    warmup_on_init: bool = True
    warmup_batch_size: int = 5


@dataclass
class ConnectionMetrics:
    """Metrics for a single connection."""

    connection_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_used_at: Optional[datetime] = None
    last_validated_at: Optional[datetime] = None
    times_borrowed: int = 0
    times_validated: int = 0
    validation_failures: int = 0
    total_time_in_use_ms: float = 0.0

    @property
    def age_seconds(self) -> float:
        """Get connection age in seconds."""
        return (datetime.now(timezone.utc) - self.created_at).total_seconds()

    @property
    def idle_seconds(self) -> float:
        """Get time since last use in seconds."""
        if self.last_used_at:
            return (datetime.now(timezone.utc) - self.last_used_at).total_seconds()
        return self.age_seconds


@dataclass
class PoolMetrics:
    """Aggregate pool metrics."""

    total_connections: int = 0
    active_connections: int = 0
    idle_connections: int = 0
    waiting_requests: int = 0

    # Counters
    connections_created: int = 0
    connections_closed: int = 0
    connections_recycled: int = 0
    borrow_count: int = 0
    return_count: int = 0

    # Health
    health_checks_passed: int = 0
    health_checks_failed: int = 0

    # Timing
    avg_borrow_time_ms: float = 0.0
    avg_connection_age_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_connections": self.total_connections,
            "active_connections": self.active_connections,
            "idle_connections": self.idle_connections,
            "waiting_requests": self.waiting_requests,
            "connections_created": self.connections_created,
            "connections_closed": self.connections_closed,
            "connections_recycled": self.connections_recycled,
            "borrow_count": self.borrow_count,
            "return_count": self.return_count,
            "health_checks_passed": self.health_checks_passed,
            "health_checks_failed": self.health_checks_failed,
            "avg_borrow_time_ms": self.avg_borrow_time_ms,
            "avg_connection_age_seconds": self.avg_connection_age_seconds,
        }


@dataclass
class PooledConnection(Generic[T]):
    """Wrapper for a pooled connection."""

    connection: T
    connection_id: str
    state: ConnectionState = ConnectionState.IDLE
    metrics: ConnectionMetrics = field(
        default_factory=lambda: ConnectionMetrics(connection_id="")
    )

    def __post_init__(self) -> None:
        self.metrics.connection_id = self.connection_id

    def mark_borrowed(self) -> None:
        """Mark connection as borrowed."""
        self.state = ConnectionState.IN_USE
        self.metrics.times_borrowed += 1
        self._borrow_time = time.time()

    def mark_returned(self) -> None:
        """Mark connection as returned."""
        self.state = ConnectionState.IDLE
        self.metrics.last_used_at = datetime.now(timezone.utc)
        if hasattr(self, "_borrow_time"):
            duration = (time.time() - self._borrow_time) * 1000
            self.metrics.total_time_in_use_ms += duration


# =============================================================================
# Connection Factory Interface
# =============================================================================


class ConnectionFactory(ABC, Generic[T]):
    """Abstract factory for creating connections."""

    @abstractmethod
    async def create(self) -> T:
        """Create a new connection."""
        pass

    @abstractmethod
    async def validate(self, connection: T) -> bool:
        """Validate a connection is healthy."""
        pass

    @abstractmethod
    async def close(self, connection: T) -> None:
        """Close a connection."""
        pass


# =============================================================================
# Redis Connection Factory
# =============================================================================


class RedisConnectionFactory(ConnectionFactory[Any]):
    """Factory for Redis connections."""

    def __init__(
        self, url: str = "redis://localhost:6379/0", decode_responses: bool = True
    ):
        self.url = url
        self.decode_responses = decode_responses

    async def create(self) -> Any:
        """Create Redis connection."""
        import redis.asyncio as aioredis

        client = await aioredis.from_url(
            self.url, decode_responses=self.decode_responses
        )
        return client

    async def validate(self, connection: Any) -> bool:
        """Validate Redis connection with PING."""
        try:
            result = await asyncio.wait_for(connection.ping(), timeout=5.0)
            return result is True or result == b"PONG"
        except Exception as e:
            logger.warning(f"Redis validation failed: {e}")
            return False

    async def close(self, connection: Any) -> None:
        """Close Redis connection."""
        try:
            await connection.close()
        except Exception as e:
            logger.warning(f"Error closing Redis connection: {e}")


# =============================================================================
# Connection Pool
# =============================================================================


class ConnectionPool(Generic[T]):
    """
    Enterprise connection pool with health checks.

    Features:
    - Async/await support
    - Health checking and validation
    - Connection recycling
    - Metrics collection
    - Circuit breaker integration
    - Graceful shutdown
    """

    def __init__(
        self,
        factory: ConnectionFactory[T],
        config: Optional[PoolConfig] = None,
        name: str = "pool",
    ):
        """
        Initialize connection pool.

        Args:
            factory: Connection factory
            config: Pool configuration
            name: Pool name for logging
        """
        self.factory = factory
        self.config = config or PoolConfig()
        self.name = name

        # State
        self.state = PoolState.INITIALIZING
        self._lock = asyncio.Lock()
        self._connections: List[PooledConnection[T]] = []
        self._waiters: asyncio.Queue[PooledConnection[T]] = asyncio.Queue()

        # Metrics
        self.metrics = PoolMetrics()

        # Background tasks
        self._health_check_task: Optional[asyncio.Task[None]] = None
        self._cleanup_task: Optional[asyncio.Task[None]] = None

        # Circuit breaker state
        self._consecutive_failures = 0
        self._circuit_open_until: Optional[datetime] = None

        logger.info(f"Connection pool '{name}' created with config: {config}")

    # =========================================================================
    # Lifecycle
    # =========================================================================

    async def initialize(self) -> None:
        """Initialize the pool and warm up connections."""
        async with self._lock:
            if self.state != PoolState.INITIALIZING:
                return

            logger.info(f"Initializing pool '{self.name}'...")

            # Warm up connections
            if self.config.warmup_on_init:
                await self._warmup()

            # Start background tasks
            self._health_check_task = asyncio.create_task(self._health_check_loop())
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())

            self.state = PoolState.ACTIVE
            logger.info(
                f"Pool '{self.name}' initialized with {len(self._connections)} connections"
            )

    async def shutdown(self, grace_period_seconds: float = 30.0) -> None:
        """
        Gracefully shutdown the pool.

        Args:
            grace_period_seconds: Time to wait for connections to drain
        """
        async with self._lock:
            if self.state == PoolState.CLOSED:
                return

            logger.info(f"Shutting down pool '{self.name}'...")
            self.state = PoolState.DRAINING

        # Cancel background tasks
        if self._health_check_task:
            self._health_check_task.cancel()
        if self._cleanup_task:
            self._cleanup_task.cancel()

        # Wait for active connections to return
        start = time.time()
        while time.time() - start < grace_period_seconds:
            async with self._lock:
                active = sum(
                    1 for c in self._connections if c.state == ConnectionState.IN_USE
                )
                if active == 0:
                    break
            await asyncio.sleep(0.1)

        # Close all connections
        async with self._lock:
            for conn in self._connections:
                try:
                    await self.factory.close(conn.connection)
                    conn.state = ConnectionState.CLOSED
                except Exception as e:
                    logger.warning(f"Error closing connection: {e}")

            self._connections.clear()
            self.state = PoolState.CLOSED

        logger.info(f"Pool '{self.name}' shutdown complete")

    async def _warmup(self) -> None:
        """Warm up the pool with initial connections."""
        target = self.config.min_connections
        batch_size = self.config.warmup_batch_size

        logger.debug(f"Warming up {target} connections...")

        for i in range(0, target, batch_size):
            tasks = []
            for j in range(min(batch_size, target - i)):
                tasks.append(self._create_connection())

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    logger.warning(f"Warmup connection failed: {result}")

    # =========================================================================
    # Connection Management
    # =========================================================================

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[T]:
        """
        Acquire a connection from the pool.

        Yields:
            Connection instance
        """
        connection = await self._borrow()
        try:
            yield connection.connection
        finally:
            await self._return(connection)

    async def _borrow(self) -> PooledConnection[T]:
        """Borrow a connection from the pool."""
        start = time.time()

        # Check circuit breaker
        if self._is_circuit_open():
            raise ConnectionError(f"Pool '{self.name}' circuit breaker is open")

        async with self._lock:
            # Try to find an idle connection
            for conn in self._connections:
                if conn.state == ConnectionState.IDLE:
                    # Validate if required
                    if self.config.validation_on_borrow:
                        if not await self._validate_connection(conn):
                            await self._recycle_connection(conn)
                            continue

                    conn.mark_borrowed()
                    self.metrics.borrow_count += 1
                    self._update_borrow_timing(start)
                    return conn

            # Create new connection if room
            if len(self._connections) < self.config.max_connections:
                conn = await self._create_connection()
                conn.mark_borrowed()
                self.metrics.borrow_count += 1
                self._update_borrow_timing(start)
                return conn

        # Wait for a connection
        timeout = self.config.connection_timeout_seconds
        try:
            conn = await asyncio.wait_for(self._wait_for_connection(), timeout=timeout)
            conn.mark_borrowed()
            self.metrics.borrow_count += 1
            self._update_borrow_timing(start)
            return conn
        except asyncio.TimeoutError:
            raise TimeoutError(
                f"Timeout waiting for connection from pool '{self.name}'"
            )

    async def _return(self, connection: PooledConnection[T]) -> None:
        """Return a connection to the pool."""
        connection.mark_returned()

        # Validate if required
        if self.config.validation_on_return:
            if not await self._validate_connection(connection):
                await self._recycle_connection(connection)
                return

        # Check if connection should be recycled due to age
        if connection.metrics.age_seconds > self.config.max_connection_age_seconds:
            await self._recycle_connection(connection)
            return

        self.metrics.return_count += 1

        # Notify waiters
        if not self._waiters.empty():
            try:
                self._waiters.put_nowait(connection)
            except asyncio.QueueFull:
                pass

    async def _create_connection(self) -> PooledConnection[T]:
        """Create a new pooled connection."""
        import uuid

        try:
            raw_connection = await asyncio.wait_for(
                self.factory.create(), timeout=self.config.connection_timeout_seconds
            )

            connection = PooledConnection(
                connection=raw_connection, connection_id=str(uuid.uuid4())[:8]
            )

            async with self._lock:
                self._connections.append(connection)

            self.metrics.connections_created += 1
            self._reset_circuit_breaker()

            logger.debug(f"Created connection {connection.connection_id}")
            return connection

        except Exception as e:
            self._record_failure()
            raise ConnectionError(f"Failed to create connection: {e}")

    async def _validate_connection(self, connection: PooledConnection[T]) -> bool:
        """Validate a connection is healthy."""
        connection.state = ConnectionState.VALIDATING
        connection.metrics.times_validated += 1

        try:
            valid = await asyncio.wait_for(
                self.factory.validate(connection.connection),
                timeout=self.config.validation_query_timeout_seconds,
            )

            if valid:
                connection.metrics.last_validated_at = datetime.now(timezone.utc)
                self.metrics.health_checks_passed += 1
                connection.state = ConnectionState.IDLE
                return True
            else:
                connection.metrics.validation_failures += 1
                self.metrics.health_checks_failed += 1
                return False

        except Exception as e:
            logger.warning(f"Connection validation error: {e}")
            connection.metrics.validation_failures += 1
            self.metrics.health_checks_failed += 1
            return False

    async def _recycle_connection(self, connection: PooledConnection[T]) -> None:
        """Recycle a connection by closing and removing it."""
        connection.state = ConnectionState.RECYCLING

        try:
            await self.factory.close(connection.connection)
        except Exception as e:
            logger.warning(f"Error closing connection: {e}")

        async with self._lock:
            if connection in self._connections:
                self._connections.remove(connection)

        self.metrics.connections_recycled += 1
        self.metrics.connections_closed += 1

        logger.debug(f"Recycled connection {connection.connection_id}")

    async def _wait_for_connection(self) -> PooledConnection[T]:
        """Wait for an available connection."""
        self.metrics.waiting_requests += 1
        try:
            return await self._waiters.get()
        finally:
            self.metrics.waiting_requests -= 1

    # =========================================================================
    # Background Tasks
    # =========================================================================

    async def _health_check_loop(self) -> None:
        """Background health check loop."""
        while self.state == PoolState.ACTIVE:
            try:
                await asyncio.sleep(self.config.health_check_interval_seconds)

                async with self._lock:
                    for conn in self._connections:
                        if conn.state == ConnectionState.IDLE:
                            if not await self._validate_connection(conn):
                                await self._recycle_connection(conn)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check error: {e}")

    async def _cleanup_loop(self) -> None:
        """Background cleanup loop for idle connections."""
        while self.state == PoolState.ACTIVE:
            try:
                await asyncio.sleep(60.0)  # Check every minute

                async with self._lock:
                    # Remove idle connections above minimum
                    idle_to_remove: List[PooledConnection[T]] = []

                    for conn in self._connections:
                        if conn.state == ConnectionState.IDLE:
                            if (
                                conn.metrics.idle_seconds
                                > self.config.idle_timeout_seconds
                            ):
                                if (
                                    len(self._connections) - len(idle_to_remove)
                                    > self.config.min_connections
                                ):
                                    idle_to_remove.append(conn)

                    for conn in idle_to_remove:
                        await self._recycle_connection(conn)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Cleanup error: {e}")

    # =========================================================================
    # Circuit Breaker
    # =========================================================================

    def _is_circuit_open(self) -> bool:
        """Check if circuit breaker is open."""
        if not self.config.circuit_breaker_enabled:
            return False

        if self._circuit_open_until:
            if datetime.now(timezone.utc) < self._circuit_open_until:
                return True
            else:
                # Reset for half-open test
                self._circuit_open_until = None

        return False

    def _record_failure(self) -> None:
        """Record a connection failure."""
        self._consecutive_failures += 1

        if self._consecutive_failures >= self.config.failure_threshold:
            self._circuit_open_until = datetime.now(timezone.utc) + timedelta(
                seconds=self.config.recovery_timeout_seconds
            )
            logger.warning(
                f"Pool '{self.name}' circuit breaker opened "
                f"after {self._consecutive_failures} failures"
            )

    def _reset_circuit_breaker(self) -> None:
        """Reset circuit breaker on success."""
        if self._consecutive_failures > 0:
            logger.info(f"Pool '{self.name}' circuit breaker reset")
        self._consecutive_failures = 0
        self._circuit_open_until = None

    # =========================================================================
    # Metrics
    # =========================================================================

    def _update_borrow_timing(self, start: float) -> None:
        """Update average borrow timing."""
        duration = (time.time() - start) * 1000
        count = self.metrics.borrow_count
        if count == 1:
            self.metrics.avg_borrow_time_ms = duration
        else:
            self.metrics.avg_borrow_time_ms = (
                self.metrics.avg_borrow_time_ms * (count - 1) + duration
            ) / count

    def get_metrics(self) -> PoolMetrics:
        """Get current pool metrics."""
        self.metrics.total_connections = len(self._connections)
        self.metrics.active_connections = sum(
            1 for c in self._connections if c.state == ConnectionState.IN_USE
        )
        self.metrics.idle_connections = sum(
            1 for c in self._connections if c.state == ConnectionState.IDLE
        )

        # Calculate average age
        if self._connections:
            total_age = sum(c.metrics.age_seconds for c in self._connections)
            self.metrics.avg_connection_age_seconds = total_age / len(self._connections)

        return self.metrics

    def get_status(self) -> Dict[str, Any]:
        """Get pool status."""
        return {
            "name": self.name,
            "state": self.state.value,
            "circuit_breaker_open": self._is_circuit_open(),
            "metrics": self.get_metrics().to_dict(),
        }


# =============================================================================
# Global Pool Manager
# =============================================================================


class PoolManager:
    """Manages multiple connection pools."""

    _instance: Optional["PoolManager"] = None
    _pools: Dict[str, ConnectionPool[Any]] = {}

    def __new__(cls) -> "PoolManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_pool(cls, name: str) -> Optional[ConnectionPool[Any]]:
        """Get a pool by name."""
        return cls._pools.get(name)

    @classmethod
    def register_pool(cls, name: str, pool: ConnectionPool[Any]) -> None:
        """Register a pool."""
        cls._pools[name] = pool
        logger.info(f"Registered pool '{name}'")

    @classmethod
    async def shutdown_all(cls, grace_period: float = 30.0) -> None:
        """Shutdown all pools."""
        for name, pool in cls._pools.items():
            logger.info(f"Shutting down pool '{name}'...")
            await pool.shutdown(grace_period)
        cls._pools.clear()

    @classmethod
    def get_all_status(cls) -> Dict[str, Any]:
        """Get status of all pools."""
        return {name: pool.get_status() for name, pool in cls._pools.items()}


# =============================================================================
# Convenience Functions
# =============================================================================


async def create_redis_pool(
    url: str = "redis://localhost:6379/0",
    name: str = "redis",
    config: Optional[PoolConfig] = None,
) -> ConnectionPool[Any]:
    """
    Create and initialize a Redis connection pool.

    Args:
        url: Redis URL
        name: Pool name
        config: Pool configuration

    Returns:
        Initialized ConnectionPool
    """
    factory = RedisConnectionFactory(url=url)
    pool = ConnectionPool(factory, config or PoolConfig(), name=name)
    await pool.initialize()
    PoolManager.register_pool(name, pool)
    return pool


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # import asyncio  # Already imported at top level

    logging.basicConfig(level=logging.DEBUG)

    async def main() -> None:
        # Create pool
        pool = await create_redis_pool(
            url="redis://localhost:6379/0",
            name="test-redis",
            config=PoolConfig(
                min_connections=2,
                max_connections=10,
                health_check_interval_seconds=10.0,
            ),
        )

        # Use pool
        async with pool.acquire() as conn:
            await conn.set("test_key", "test_value")
            value = await conn.get("test_key")
            print(f"Got value: {value}")

        # Get status
        print(f"Pool status: {pool.get_status()}")

        # Shutdown
        await PoolManager.shutdown_all()

    asyncio.run(main())
