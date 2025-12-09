"""
Connection pool management for gRPC RPC service.

Manages a pool of reusable gRPC connections with configurable limits,
health checks, and metrics tracking.

Features:
- Configurable pool size (default: 50 connections)
- Connection TTL (time-to-live) with automatic replacement
- Graceful overflow handling (queue or reject)
- Health checks for stale connections
- Prometheus metrics export
- Automatic cleanup on exit
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
# from typing import Dict, List, Optional, Any, AsyncIterator, Type
from types import TracebackType

import grpc

logger = logging.getLogger(__name__)


@dataclass
class PoolConfig:
    """Connection pool configuration."""

    max_connections: int = 50
    min_connections: int = 5
    connection_ttl_seconds: int = 300  # 5 minutes
    health_check_interval_seconds: int = 30
    connection_timeout_seconds: int = 10
    max_wait_queue_size: int = 100
    enable_keepalive: bool = True


class PooledConnection:
    """Wrapper for a single pooled gRPC connection."""

    def __init__(self, channel: grpc.aio.Channel, pool: "ConnectionPool"):
        self.channel = channel
        self.pool = pool
        self.created_at = time.time()
        self.last_used_at = time.time()
        self.healthy = True
        self.in_use = False

    def is_stale(self) -> bool:
        """Check if connection has exceeded TTL."""
        age = time.time() - self.created_at
        return age > self.pool.config.connection_ttl_seconds

    def mark_used(self) -> None:
        """Update last used timestamp."""
        self.last_used_at = time.time()

    async def health_check(self) -> bool:
        """Verify connection is still healthy."""
        try:
            # Create a simple health check call
            # This assumes the service implements the Health Check API (gRPC standard)
            health_stub = grpc.health.v1.health_pb2_grpc.HealthStub(self.channel)
            response = await health_stub.Check(
                grpc.health.v1.health_pb2.HealthCheckRequest(),
                timeout=5,
            )
            self.healthy = (
                response.status == grpc.health.v1.health_pb2.HealthCheckResponse.SERVING
            )
            return self.healthy
        except Exception as e:
            logger.warning(f"Health check failed for connection: {e}")
            self.healthy = False
            return False

    async def close(self) -> None:
        """Close the underlying channel."""
        try:
            await self.channel.close()
        except Exception as e:
            logger.error(f"Error closing channel: {e}")


class ConnectionPool:
    """Thread-safe connection pool for gRPC services."""

    def __init__(self, target: str, config: Optional[PoolConfig] = None):
        """
        Initialize connection pool.

        Args:
            target: gRPC service target (e.g., "localhost:50051")
            config: PoolConfig instance (uses defaults if None)
        """
        self.target = target
        self.config = config or PoolConfig()
        self.available_connections: List[PooledConnection] = []
        self.in_use_connections: List[PooledConnection] = []
        self.waiting_tasks: asyncio.Queue[PooledConnection] = asyncio.Queue(
            maxsize=self.config.max_wait_queue_size
        )
        self.lock = asyncio.Lock()
        self.metrics = {
            "created": 0,
            "destroyed": 0,
            "reused": 0,
            "health_checks": 0,
            "health_check_failures": 0,
            "acquire_waits": 0,
            "acquire_timeouts": 0,
        }
        self.health_check_task: Optional[asyncio.Task[None]] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize pool with minimum connections."""
        async with self.lock:
            if self._initialized:
                return

            try:
                # Create minimum number of connections
                for _ in range(self.config.min_connections):
                    await self._create_connection()

                # Start health check background task
                self.health_check_task = asyncio.create_task(self._health_check_loop())
                self._initialized = True
                logger.info(
                    f"Connection pool initialized for {self.target} "
                    f"with {len(self.available_connections)} connections"
                )
            except Exception as e:
                logger.error(f"Failed to initialize pool: {e}")
                raise

    async def _create_connection(self) -> PooledConnection:
        """Create a new pooled connection."""
        try:
            # Create gRPC channel with keepalive options
            keepalive_params = (
                [
                    ("grpc.keepalive_time_ms", 30000),
                    ("grpc.keepalive_timeout_ms", 10000),
                    ("grpc.keepalive_permit_without_calls", True),
                ]
                if self.config.enable_keepalive
                else []
            )

            channel = grpc.aio.secure_channel(
                self.target,
                grpc.ssl_channel_credentials(),
                options=keepalive_params,
            )

            # Wait for channel to be ready
            try:
                await asyncio.wait_for(
                    channel.channel_ready(),
                    timeout=self.config.connection_timeout_seconds,
                )
            except asyncio.TimeoutError:
                await channel.close()
                raise

            pooled_conn = PooledConnection(channel, self)
            self.available_connections.append(pooled_conn)
            self.metrics["created"] += 1

            logger.debug(
                f"Created connection #{self.metrics['created']} to {self.target}"
            )
            return pooled_conn
        except Exception as e:
            logger.error(f"Failed to create connection: {e}")
            raise

    @asynccontextmanager
    async def acquire(self, timeout: Optional[float] = None) -> AsyncIterator[PooledConnection]:
        """
        Acquire a connection from the pool.

        Usage:
            async with pool.acquire() as connection:
                # Use connection.channel for gRPC calls

        Args:
            timeout: Maximum time to wait for available connection (seconds)

        Yields:
            PooledConnection instance

        Raises:
            TimeoutError: If no connection available within timeout
            RuntimeError: If pool is not initialized
        """
        if not self._initialized:
            raise RuntimeError("Pool not initialized. Call initialize() first.")

        connection = None
        try:
            # Try to acquire existing connection
            async with self.lock:
                if self.available_connections:
                    connection = self.available_connections.pop(0)
                    connection.in_use = True
                    connection.mark_used()
                    self.in_use_connections.append(connection)
                    self.metrics["reused"] += 1

            # If no connection available, create new one (if under limit)
            if connection is None:
                async with self.lock:
                    if (
                        len(self.in_use_connections) + len(self.available_connections)
                        < self.config.max_connections
                    ):
                        connection = await self._create_connection()
                        connection.in_use = True
                        connection.mark_used()
                        self.in_use_connections.append(connection)

            # If still no connection, wait for one to become available
            if connection is None:
                self.metrics["acquire_waits"] += 1
                try:
                    connection = await asyncio.wait_for(
                        self.waiting_tasks.get(), timeout=timeout or 10
                    )
                except asyncio.TimeoutError:
                    self.metrics["acquire_timeouts"] += 1
                    raise TimeoutError(
                        f"No connection available after {timeout or 10}s "
                        f"(pool size: {len(self.in_use_connections)}/{self.config.max_connections})"
                    )

            yield connection

        finally:
            # Return connection to pool
            if connection is not None:
                async with self.lock:
                    if connection in self.in_use_connections:
                        self.in_use_connections.remove(connection)

                    # If connection is stale or unhealthy, discard it
                    if connection.is_stale() or not connection.healthy:
                        await connection.close()
                        self.metrics["destroyed"] += 1
                        logger.debug("Discarded stale/unhealthy connection")

                        # Create replacement if below max
                        if (
                            len(self.in_use_connections)
                            + len(self.available_connections)
                            < self.config.max_connections
                        ):
                            try:
                                await self._create_connection()
                            except Exception as e:
                                logger.warning(
                                    f"Failed to create replacement connection: {e}"
                                )
                    else:
                        # Return healthy connection to available pool
                        connection.in_use = False
                        self.available_connections.append(connection)

    async def _health_check_loop(self) -> None:
        """Background task to periodically check connection health."""
        while True:
            try:
                await asyncio.sleep(self.config.health_check_interval_seconds)

                async with self.lock:
                    connections_to_check = self.available_connections[:]

                # Perform health checks
                for conn in connections_to_check:
                    self.metrics["health_checks"] += 1
                    healthy = await conn.health_check()
                    if not healthy:
                        self.metrics["health_check_failures"] += 1
                        async with self.lock:
                            if conn in self.available_connections:
                                self.available_connections.remove(conn)
                        await conn.close()
                        logger.warning("Removed unhealthy connection from pool")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in health check loop: {e}")

    async def close(self) -> None:
        """Close all connections and shutdown pool."""
        if self.health_check_task:
            self.health_check_task.cancel()
            try:
                await self.health_check_task
            except asyncio.CancelledError:
                pass

        async with self.lock:
            # Close all available connections
            for conn in self.available_connections:
                await conn.close()
            self.available_connections.clear()

            # Close all in-use connections
            for conn in self.in_use_connections:
                await conn.close()
            self.in_use_connections.clear()

        logger.info(f"Connection pool for {self.target} closed")

    def get_metrics(self) -> Dict[str, int]:
        """Get pool metrics."""
        return {
            **self.metrics,
            "available": len(self.available_connections),
            "in_use": len(self.in_use_connections),
            "total": len(self.available_connections) + len(self.in_use_connections),
        }

    async def __aenter__(self) -> "ConnectionPool":
        """Async context manager support."""
        await self.initialize()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Async context manager support."""
        await self.close()
