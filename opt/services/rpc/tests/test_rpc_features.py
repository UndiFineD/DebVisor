"""
Unit tests for RPC service connection pool, compression, and versioning.

Tests cover:
- Connection pool creation, acquisition, release
- Connection health checks and TTL
- Compression with GZIP and Brotli
- API version negotiation and compatibility
"""

from typing import AsyncGenerator
import pytest
# from unittest.mock import AsyncMock, Mock, patch
from opt.services.rpc.pool import ConnectionPool, PoolConfig, PooledConnection
from opt.services.rpc.compression import (
    CompressionManager,
    CompressionConfig,
    CompressionAlgorithm,
)
from opt.services.rpc.versioning import (
    VersionNegotiator,
    VersionedRequestRouter,
    APIVersion,
    BackwardCompatibilityLayer,
)


# ============================================================================
# Connection Pool Tests
# ============================================================================


class TestConnectionPool:
    """Test suite for connection pool."""

    @pytest.fixture
    def pool_config(self) -> PoolConfig:
        """Create pool configuration."""
        return PoolConfig(
            max_connections=10,
            min_connections=2,
            connection_ttl_seconds=300,
            health_check_interval_seconds=30,
        )

    @pytest.fixture
    async def pool(self, pool_config: PoolConfig) -> AsyncGenerator[ConnectionPool, None]:
        """Create initialized pool."""
        pool = ConnectionPool("localhost:50051", pool_config)
        await pool.initialize()
        yield pool
        await pool.close()

    @pytest.mark.asyncio
    async def test_pool_initialization(self, pool_config: PoolConfig) -> None:
        """Test pool initializes with minimum connections."""
        pool = ConnectionPool("localhost:50051", pool_config)
        assert pool._initialized is False

        await pool.initialize()
        assert pool._initialized is True
        assert len(pool.available_connections) >= pool_config.min_connections    # type: ignore

    @pytest.mark.asyncio
    async def test_pool_acquire_release(self, pool: ConnectionPool) -> None:
        """Test acquiring and releasing connections."""
        initial_available = len(pool.available_connections)

        async with pool.acquire() as conn:
            assert conn is not None
            assert len(pool.available_connections) < initial_available
            assert conn in pool.in_use_connections

        # After release, connection should be back in available pool
        assert len(pool.available_connections) == initial_available

    @pytest.mark.asyncio
    async def test_pool_max_connections_limit(self, pool: ConnectionPool) -> None:
        """Test pool respects max connections limit."""
        pool.config.max_connections = 3

        connections = []
        for _ in range(3):
            ctx = pool.acquire()
            conn = await ctx.__aenter__()
            connections.append(ctx)
            assert conn is not None

        # Fourth acquire should timeout
        with pytest.raises(TimeoutError):
            async with pool.acquire(timeout=0.1):
                pass

    @pytest.mark.asyncio
    async def test_pool_connection_reuse(self, pool: ConnectionPool) -> None:
        """Test connections are reused from available pool."""
        # First acquire
        async with pool.acquire() as conn1:
            conn1_id = id(conn1)

        # Second acquire should reuse same connection
        async with pool.acquire() as conn2:
            conn2_id = id(conn2)

        # Same connection object should be reused
        assert conn1_id == conn2_id

    @pytest.mark.asyncio
    async def test_pool_metrics(self, pool: ConnectionPool) -> None:
        """Test pool metrics tracking."""
        async with pool.acquire():
            pass

        metrics = pool.get_metrics()
        assert metrics["reused"] > 0
        assert metrics["available"] >= 0
        assert metrics["in_use"] == 0

    @pytest.mark.asyncio
    async def test_pool_close(self, pool: ConnectionPool) -> None:
        """Test closing pool."""
        await pool.close()

        with pytest.raises(RuntimeError):
            async with pool.acquire():
                pass


class TestPooledConnection:
    """Test suite for pooled connection."""

    @pytest.mark.asyncio
    async def test_connection_stale_detection(self) -> None:
        """Test stale connection detection based on TTL."""
        mock_channel = AsyncMock()  # type: ignore[name-defined]
        pool = Mock(spec=ConnectionPool)  # type: ignore[name-defined]
        pool.config.connection_ttl_seconds = 1

        conn = PooledConnection(mock_channel, pool)
        assert not conn.is_stale()

        # Simulate age
        conn.created_at -= 2    # 2 seconds ago
        assert conn.is_stale()

    @pytest.mark.asyncio
    async def test_connection_health_check(self) -> None:
        """Test connection health check."""
        mock_channel = AsyncMock()  # type: ignore[name-defined]
        pool = Mock(spec=ConnectionPool)  # type: ignore[name-defined]

        conn = PooledConnection(mock_channel, pool)

        # Mock health check response
        mock_response = Mock()  # type: ignore[name-defined]
        mock_response.status = 1    # SERVING

        with patch("grpc.health.v1.health_pb2_grpc.HealthStub") as mock_health:  # type: ignore[name-defined]
            mock_health.return_value.Check.return_value = mock_response
            result = await conn.health_check()
            assert result is True
            assert conn.healthy is True


# ============================================================================
# Compression Tests
# ============================================================================


class TestCompression:
    """Test suite for compression."""

    @pytest.fixture
    def compression_config(self) -> CompressionConfig:
        """Create compression configuration."""
        return CompressionConfig(
            enabled=True,
            min_payload_bytes=100,
            gzip_level=6,
        )

    @pytest.fixture
    def manager(self, compression_config: CompressionConfig) -> CompressionManager:
        """Create compression manager."""
        return CompressionManager(compression_config)

    def test_compression_algorithm_selection(self, manager: CompressionManager) -> None:
        """Test algorithm selection based on payload size."""
        small_payload_size = 50    # Below threshold

        # Small payload should not compress
        algo = manager.select_algorithm(small_payload_size)
        assert algo == CompressionAlgorithm.NONE

        # Large payload should compress
        large_payload_size = 5000
        algo = manager.select_algorithm(large_payload_size)
        assert algo in [CompressionAlgorithm.GZIP, CompressionAlgorithm.BROTLI]

    def test_gzip_compression(self, manager: CompressionManager) -> None:
        """Test GZIP compression."""
        data = b"Hello World! " * 100    # ~1300 bytes

        compressed, algo = manager.compress(data, CompressionAlgorithm.GZIP)

        assert algo == CompressionAlgorithm.GZIP
        assert len(compressed) < len(data)
        assert compressed.startswith(b"\x1f\x8b")    # GZIP magic number

    def test_gzip_decompression(self, manager: CompressionManager) -> None:
        """Test GZIP decompression."""
        original_data = b"Test data for compression" * 50

        compressed, algo = manager.compress(original_data, CompressionAlgorithm.GZIP)
        decompressed = manager.decompress(compressed, algo)

        assert decompressed == original_data

    def test_compression_no_benefit(self, manager: CompressionManager) -> None:
        """Test that compression is skipped if it doesn't reduce size."""
        # Random data compresses poorly
        data = bytes(range(256)) * 5    # Only 1280 bytes, not very compressible

        compressed, algo = manager.compress(data, CompressionAlgorithm.GZIP)

        # If compression increases size, should return NONE
        if len(compressed) >= len(data):
            assert algo == CompressionAlgorithm.NONE

    def test_compression_metrics(self, manager: CompressionManager) -> None:
        """Test compression metrics tracking."""
        data = b"Compressible data " * 100

        manager.compress(data, CompressionAlgorithm.GZIP)
        manager.compress(data, CompressionAlgorithm.GZIP)

        metrics = manager.get_metrics()
        assert metrics["total_requests"] > 0
        assert metrics["compressed_requests"] > 0
        assert 0 < metrics["compression_ratio"] < 1

    def test_compression_error_handling(self, manager: CompressionManager) -> None:
        """Test error handling in compression."""
        # Try to decompress invalid data
        invalid_data = b"not compressed data"

        with pytest.raises(ValueError):
            manager.decompress(invalid_data, CompressionAlgorithm.GZIP)

        # Metrics should record error
        metrics = manager.get_metrics()
        assert metrics["errors"] > 0


# ============================================================================
# Versioning Tests
# ============================================================================


class TestVersioning:
    """Test suite for API versioning."""

    @pytest.fixture
    def negotiator(self) -> VersionNegotiator:
        """Create version negotiator."""
        return VersionNegotiator()

    def test_supported_versions(self, negotiator: VersionNegotiator) -> None:
        """Test listing supported versions."""
        supported = negotiator.get_supported_versions()
        assert "1.0" in supported
        assert "2.0" in supported

    def test_version_negotiation_client_preference(self, negotiator: VersionNegotiator) -> None:
        """Test version negotiation respects client preference."""
        client_versions = ["2.0", "1.0"]
        negotiated = negotiator.negotiate_version(client_versions)

        assert negotiated == "2.0"    # Highest client version

    def test_version_negotiation_fallback(self, negotiator: VersionNegotiator) -> None:
        """Test version negotiation fallback to server version."""
        client_versions = ["99.0", "100.0"]    # Unsupported versions

        with pytest.raises(ValueError):
            negotiator.negotiate_version(client_versions)

    def test_version_validation(self, negotiator: VersionNegotiator) -> None:
        """Test version validation."""
        assert negotiator.validate_version("1.0") is True
        assert negotiator.validate_version("2.0") is True
        assert negotiator.validate_version("99.0") is False

    def test_deprecation_warnings(self, negotiator: VersionNegotiator) -> None:
        """Test deprecation warnings."""
        negotiator.get_deprecation_warnings("1.0")
        # V1.0 is active, so no deprecation warning

        # V2.0 will be deprecated
        negotiator.get_deprecation_warnings("2.0")
        # Check if deprecated flag is set and warning generated

    def test_version_adoption_metrics(self, negotiator: VersionNegotiator) -> None:
        """Test version adoption tracking."""
        negotiator.negotiate_version(["1.0"])
        negotiator.negotiate_version(["2.0"])
        negotiator.negotiate_version(["2.0"])

        metrics = negotiator.get_adoption_metrics()
        assert metrics["1.0"] == 1
        assert metrics["2.0"] == 2


class TestVersionedRouter:
    """Test suite for versioned request routing."""

    @pytest.fixture
    def router(self) -> VersionedRequestRouter:
        """Create versioned request router."""
        negotiator = VersionNegotiator()
        return VersionedRequestRouter(negotiator)

    def test_handler_registration(self, router: VersionedRequestRouter) -> None:
        """Test registering version-specific handlers."""
        mock_handler = Mock(return_value="result")  # type: ignore[name-defined]

        router.register_handler(APIVersion.V1_0, "list_nodes", mock_handler)

        assert "list_nodes" in router.handlers[APIVersion.V1_0]

    def test_request_routing(self, router: VersionedRequestRouter) -> None:
        """Test routing requests to appropriate handlers."""
        mock_handler_v1 = Mock(return_value="v1_result")  # type: ignore[name-defined]
        mock_handler_v2 = Mock(return_value="v2_result")  # type: ignore[name-defined]

        router.register_handler(APIVersion.V1_0, "list_nodes", mock_handler_v1)
        router.register_handler(APIVersion.V2_0, "list_nodes", mock_handler_v2)

        result = router.route("1.0", "list_nodes", arg1="value1")
        assert result == "v1_result"
        mock_handler_v1.assert_called_once_with(arg1="value1")

        result = router.route("2.0", "list_nodes", arg1="value2")
        assert result == "v2_result"
        mock_handler_v2.assert_called_once_with(arg1="value2")

    def test_operation_not_found(self, router: VersionedRequestRouter) -> None:
        """Test error when operation not found."""
        router.register_handler(APIVersion.V1_0, "list_nodes", Mock())  # type: ignore[name-defined]

        with pytest.raises(KeyError):
            router.route("1.0", "nonexistent_operation")

    def test_compatibility_matrix(self, router: VersionedRequestRouter) -> None:
        """Test compatibility matrix generation."""
        router.register_handler(APIVersion.V1_0, "list_nodes", Mock())  # type: ignore[name-defined]
        router.register_handler(APIVersion.V1_0, "get_node", Mock())  # type: ignore[name-defined]
        router.register_handler(APIVersion.V2_0, "list_nodes", Mock())  # type: ignore[name-defined]

        matrix = router.get_compatibility_matrix()
        assert "list_nodes" in matrix["1.0"]
        assert "get_node" in matrix["1.0"]
        assert "list_nodes" in matrix["2.0"]


class TestBackwardCompatibility:
    """Test suite for backward compatibility layer."""

    def test_v1_to_v2_response_conversion(self) -> None:
        """Test converting V1 response to V2 format."""
        v1_response = {
            "nodes": [{"id": 1}, {"id": 2}],
            "status": "healthy",
        }

        v2_response = BackwardCompatibilityLayer.convert_v1_response_to_v2(v1_response)

        assert "nodes_list" in v2_response
        assert "status_code" in v2_response
        assert v2_response["status_code"] == 200

    def test_v2_to_v1_request_conversion(self) -> None:
        """Test converting V2 request to V1 format."""
        v2_request = {
            "pool_id": "pool-1",
            "filter": "healthy",
        }

        v1_request = BackwardCompatibilityLayer.convert_v2_request_to_v1(v2_request)

        assert "pool_id" not in v1_request
        assert "filter" in v1_request


# ============================================================================
# Integration Tests
# ============================================================================


class TestRPCIntegration:
    """Integration tests for RPC components."""

    @pytest.mark.asyncio
    async def test_pool_with_compression(self) -> None:
        """Test connection pool with compression."""
        pool_config = PoolConfig(min_connections=1)
        pool = ConnectionPool("localhost:50051", pool_config)

        compression_manager = CompressionManager()

        # Initialize pool
        await pool.initialize()

        # Test acquiring connection and compressing data
        async with pool.acquire() as conn:
            assert conn is not None

            # Test compression
            data = b"Test data " * 100
            compressed, algo = compression_manager.compress(data)
            decompressed = compression_manager.decompress(compressed, algo)

            assert decompressed == data

        await pool.close()

    @pytest.mark.asyncio
    async def test_versioning_with_pool_and_compression(self) -> None:
        """Test all components together."""
        # Initialize components
        pool = ConnectionPool("localhost:50051")
        compression_manager = CompressionManager()
        negotiator = VersionNegotiator()

        await pool.initialize()

        # Negotiate version
        negotiated_version = negotiator.negotiate_version(["2.0", "1.0"])
        assert negotiated_version in ["1.0", "2.0"]

        # Acquire connection
        async with pool.acquire() as conn:
            assert conn is not None

            # Compress data
            data = b"Integration test data " * 50
            compressed, algo = compression_manager.compress(data)
            assert len(compressed) < len(data)

        await pool.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
