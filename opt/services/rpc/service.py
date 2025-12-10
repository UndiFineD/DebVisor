"""
RPC Service integration layer combining pooling, compression, and versioning.

This module provides the main RPC service class that integrates all
Phase 4 features and provides a clean API for service handlers.

Features:
- Automatic connection pooling
- Transparent compression
- API version negotiation
- Metrics collection and reporting
- Context management for lifecycle
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable
from types import TracebackType

from opt.services.rpc.pool import ConnectionPool, PoolConfig
from opt.services.rpc.compression import CompressionManager, CompressionConfig
from opt.services.rpc.versioning import (
    VersionNegotiator,
    VersionedRequestRouter,
    APIVersion,
)

logger = logging.getLogger(__name__)


@dataclass
class RPCServiceConfig:
    """Configuration for RPC service."""

    target: str = "localhost:50051"
    pool_config: Optional[PoolConfig] = None
    compression_config: Optional[CompressionConfig] = None

    def __post_init__(self) -> None:
        if self.pool_config is None:
            self.pool_config = PoolConfig()
        if self.compression_config is None:
            self.compression_config = CompressionConfig()


class RPCService:
    """
    Main RPC service class integrating pooling, compression, and versioning.

    Usage:
        service = RPCService(RPCServiceConfig(target="localhost:50051"))
        await service.initialize()

        # Make RPC call with automatic pooling and compression
        async with service.call("2.0", "list_nodes") as response:
            # Use response
            pass

        await service.shutdown()
    """

    def __init__(self, config: RPCServiceConfig):
        """
        Initialize RPC service.

        Args:
            config: RPCServiceConfig instance
        """
        self.config = config
        self.connection_pool = ConnectionPool(config.target, config.pool_config)
        self.compression_manager = CompressionManager(config.compression_config)
        self.version_negotiator = VersionNegotiator()
        self.request_router = VersionedRequestRouter(self.version_negotiator)
        self._initialized = False
        self.call_metrics = {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "total_latency_ms": 0.0,
        }

    async def initialize(self) -> None:
        """Initialize service components."""
        try:
            logger.info("Initializing RPC service...")

            # Initialize connection pool
            await self.connection_pool.initialize()

            # Register default handlers (empty for now, will be populated by subclasses)
            self._register_default_handlers()

            self._initialized = True
            logger.info("RPC service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize RPC service: {e}")
            raise

    def _register_default_handlers(self) -> None:
        """Register default request handlers for all versions."""
        # This method can be overridden by subclasses to register specific handlers
        pass

    async def call(
        self,
        version: str,
        operation: str,
        request_data: Optional[bytes] = None,
        client_supported_compression: Optional[List[str]] = None,
    ) -> bytes:
        """
        Make an RPC call with automatic pooling and compression.

        Args:
            version: API version (e.g., "1.0", "2.0")
            operation: Operation name
            request_data: Request data bytes
            client_supported_compression: List of compression algorithms client supports

        Returns:
            Response bytes (automatically decompressed if compressed)

        Raises:
            ValueError: If version not supported
            TimeoutError: If connection unavailable
            Exception: If RPC call fails
        """
        if not self._initialized:
            raise RuntimeError("Service not initialized. Call initialize() first.")

        import time

        start_time = time.time()

        try:
            # Validate version
            if not self.version_negotiator.validate_version(version):
                raise ValueError(f"Unsupported API version: {version}")

            # Log deprecation warnings if any
            warnings = self.version_negotiator.get_deprecation_warnings(version)
            if warnings:
                logger.warning(f"Version warnings: {warnings}")

Acquire connection from pool
            async with self.connection_pool.acquire() as pooled_conn:
                # Compress request if appropriate
                compressed_request = request_data
                request_algo = None

                if request_data:
                    compressed_request, request_algo = (
                        self.compression_manager.compress(
                            request_data
                        )
                    )

                # Make actual RPC call
                # (This is a placeholder; actual implementation depends on service definition)
                response = await self._execute_rpc_call(
                    pooled_conn.channel,
                    operation,
                    compressed_request,
                    version,
                )

                # Decompress response if compressed
                if response and request_algo:
                    response = self.compression_manager.decompress(
                        response, request_algo
                    )

                # Record metrics
                latency_ms = (time.time() - start_time) * 1000
                self._record_call_metric(success=True, latency_ms=latency_ms)

                return response

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self._record_call_metric(success=False, latency_ms=latency_ms)
            logger.error(f"RPC call failed: {operation} (version {version}): {e}")
            raise

    async def _execute_rpc_call(
        self, channel: Any, operation: str, request: Optional[bytes], version: str
    ) -> bytes:
        """
        Execute the actual RPC call.

        This is a placeholder that should be implemented based on
        the specific gRPC service definition.

        Args:
            channel: gRPC channel
            operation: Operation name
            request: Request bytes
            version: API version

        Returns:
            Response bytes
        """
        # Placeholder implementation
        # In real code, this would call the appropriate gRPC stub method
        logger.debug(f"Executing RPC: {operation} (v{version})")

        # Simulate RPC call
        await asyncio.sleep(0.01)

        return b'{"status": "ok"}'

    def register_handler(self, version: str, operation: str, handler: Callable[..., Any]) -> None:
        """
        Register a request handler for a specific version and operation.

        Args:
            version: API version
            operation: Operation name
            handler: Callable handler function
        """
        try:
            api_version = APIVersion(version)
            self.request_router.register_handler(api_version, operation, handler)
        except ValueError:
            raise ValueError(f"Invalid API version: {version}")

    def _record_call_metric(self, success: bool, latency_ms: float) -> None:
        """Record metrics for an RPC call."""
        self.call_metrics["total_calls"] += 1
        self.call_metrics["total_latency_ms"] += latency_ms

        if success:
            self.call_metrics["successful_calls"] += 1
        else:
            self.call_metrics["failed_calls"] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive service metrics."""
        avg_latency = (
            self.call_metrics["total_latency_ms"] / self.call_metrics["total_calls"]
            if self.call_metrics["total_calls"] > 0
            else 0
        )

        success_rate = (
            self.call_metrics["successful_calls"] / self.call_metrics["total_calls"]
            if self.call_metrics["total_calls"] > 0
            else 0
        )

        return {
            "service": {
                "total_calls": self.call_metrics["total_calls"],
                "successful_calls": self.call_metrics["successful_calls"],
                "failed_calls": self.call_metrics["failed_calls"],
                "success_rate": success_rate,
                "average_latency_ms": round(avg_latency, 2),
            },
            "pool": self.connection_pool.get_metrics(),
            "compression": self.compression_manager.get_metrics(),
            "versioning": self.version_negotiator.get_adoption_metrics(),
        }

    async def shutdown(self) -> None:
        """Shutdown service and cleanup resources."""
        try:
            logger.info("Shutting down RPC service...")

            # Close connection pool
            await self.connection_pool.close()

            self._initialized = False
            logger.info("RPC service shutdown complete")

        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            raise

    async def __aenter__(self) -> "RPCService":
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
        await self.shutdown()


class HealthCheckService:
    """Health check endpoint for the RPC service."""

    def __init__(self, rpc_service: RPCService):
        """
        Initialize health check service.

        Args:
            rpc_service: RPCService instance to monitor
        """
        self.rpc_service = rpc_service

    async def check(self) -> Dict[str, Any]:
        """
        Check service health.

        Returns:
            Health status dictionary
        """
        try:
            # Check if service is initialized
            if not self.rpc_service._initialized:
                return {"status": "NOT_READY", "reason": "Service not initialized"}

            # Check pool status
            pool_metrics = self.rpc_service.connection_pool.get_metrics()
            if pool_metrics["available"] == 0 and pool_metrics["in_use"] == 0:
                return {
                    "status": "UNHEALTHY",
                    "reason": "No connections available",
                }

            # Check success rate
            call_metrics = self.rpc_service.call_metrics
            if call_metrics["total_calls"] > 0:
                success_rate = (
                    call_metrics["successful_calls"] / call_metrics["total_calls"]
                )
                if success_rate < 0.8:    # Less than 80% success rate
                    return {
                        "status": "DEGRADED",
                        "reason": f"Low success rate: {success_rate:.1%}",
                    }

            return {
                "status": "SERVING",
                "version": self.rpc_service.version_negotiator.get_supported_versions(),
                "metrics": self.rpc_service.get_metrics(),
            }

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "UNHEALTHY", "reason": str(e)}
