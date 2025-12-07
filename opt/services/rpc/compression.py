"""
Request/Response compression for gRPC RPC service.

Supports GZIP and Brotli compression with automatic negotiation
based on content type and size. Includes metrics tracking.

Features:
- GZIP compression (fast, widely supported)
- Brotli compression (better ratio, slower)
- Configurable compression threshold
- Content-type based algorithm selection
- Compression metrics tracking
- Transparent compression/decompression
"""

import gzip
import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple

try:
    import brotli
    BROTLI_AVAILABLE = True
except ImportError:
    BROTLI_AVAILABLE = False

logger = logging.getLogger(__name__)


class CompressionAlgorithm(Enum):
    """Supported compression algorithms."""

    NONE = "none"
    GZIP = "gzip"
    BROTLI = "brotli"


@dataclass
class CompressionConfig:
    """Compression configuration."""

    enabled: bool = True
    min_payload_bytes: int = 1024  # Don't compress payloads smaller than 1KB
    preferred_algorithm: CompressionAlgorithm = CompressionAlgorithm.GZIP
    allow_brotli: bool = True
    gzip_level: int = 6  # 1-9, higher = better compression, slower
    brotli_quality: int = 4  # 0-11, higher = better compression, slower


class CompressionMetrics:
    """Track compression metrics."""

    def __init__(self):
        self.total_requests = 0
        self.compressed_requests = 0
        self.gzip_requests = 0
        self.brotli_requests = 0
        self.total_bytes_original = 0
        self.total_bytes_compressed = 0
        self.compression_time_ms = 0.0
        self.decompression_time_ms = 0.0
        self.errors = 0

    def record_compression(
        self,
        algorithm: CompressionAlgorithm,
        original_size: int,
        compressed_size: int,
        duration_ms: float,
    ) -> None:
        """Record compression operation."""
        self.total_requests += 1
        if compressed_size < original_size:
            self.compressed_requests += 1
            if algorithm == CompressionAlgorithm.GZIP:
                self.gzip_requests += 1
            elif algorithm == CompressionAlgorithm.BROTLI:
                self.brotli_requests += 1

            self.total_bytes_original += original_size
            self.total_bytes_compressed += compressed_size
            self.compression_time_ms += duration_ms

    def record_decompression(self, duration_ms: float) -> None:
        """Record decompression operation."""
        self.decompression_time_ms += duration_ms

    def record_error(self) -> None:
        """Record compression error."""
        self.errors += 1

    def get_metrics(self) -> Dict:
        """Get metrics summary."""
        if self.total_requests == 0:
            return {
                "total_requests": 0,
                "compressed_requests": 0,
                "average_compression_ratio": 0.0,
                "average_compression_time_ms": 0.0,
            }

        compression_ratio = (
            self.total_bytes_compressed / self.total_bytes_original
            if self.total_bytes_original > 0
            else 1.0
        )

        avg_compression_time = (
            self.compression_time_ms / self.compressed_requests
            if self.compressed_requests > 0
            else 0.0
        )

        return {
            "total_requests": self.total_requests,
            "compressed_requests": self.compressed_requests,
            "gzip_requests": self.gzip_requests,
            "brotli_requests": self.brotli_requests,
            "compression_ratio": round(compression_ratio, 3),
            "bytes_saved": self.total_bytes_original - self.total_bytes_compressed,
            "average_compression_time_ms": round(avg_compression_time, 2),
            "average_decompression_time_ms": round(
                self.decompression_time_ms / self.total_requests, 2
            ) if self.total_requests > 0 else 0.0,
            "errors": self.errors,
        }


class CompressionManager:
    """Manages compression and decompression operations."""

    def __init__(self, config: Optional[CompressionConfig] = None):
        """
        Initialize compression manager.

        Args:
            config: CompressionConfig instance (uses defaults if None)
        """
        self.config = config or CompressionConfig()
        self.metrics = CompressionMetrics()

        # Validate Brotli availability
        if self.config.allow_brotli and not BROTLI_AVAILABLE:
            logger.warning("Brotli not available. Install with: pip install brotli")
            self.config.allow_brotli = False

    def select_algorithm(
        self,
        payload_size: int,
        client_supported: Optional[list] = None,
        content_type: Optional[str] = None,
    ) -> CompressionAlgorithm:
        """
        Select compression algorithm based on payload and client capabilities.

        Args:
            payload_size: Size of payload in bytes
            client_supported: List of algorithms client supports
            content_type: Content type of payload

        Returns:
            Selected CompressionAlgorithm
        """
        # Don't compress small payloads
        if payload_size < self.config.min_payload_bytes:
            return CompressionAlgorithm.NONE

        # Disable compression if not enabled
        if not self.config.enabled:
            return CompressionAlgorithm.NONE

        # Check client capabilities
        supported = client_supported or [
            CompressionAlgorithm.GZIP,
            CompressionAlgorithm.BROTLI if self.config.allow_brotli else None,
        ]
        supported = [a for a in supported if a is not None]

        if not supported:
            return CompressionAlgorithm.NONE

        # Content-type based selection
        # Use Brotli for text-heavy content, GZIP for binary
        if content_type:
            if "text" in content_type or "json" in content_type:
                if (
                    CompressionAlgorithm.BROTLI in supported
                    and self.config.allow_brotli
                ):
                    return CompressionAlgorithm.BROTLI

        # Use preferred algorithm if available
        if self.config.preferred_algorithm in supported:
            return self.config.preferred_algorithm

        # Fallback to GZIP
        if CompressionAlgorithm.GZIP in supported:
            return CompressionAlgorithm.GZIP

        return CompressionAlgorithm.NONE

    def compress(
        self,
        data: bytes,
        algorithm: Optional[CompressionAlgorithm] = None,
        content_type: Optional[str] = None,
    ) -> Tuple[bytes, CompressionAlgorithm]:
        """
        Compress data using specified or auto-selected algorithm.

        Args:
            data: Bytes to compress
            algorithm: Compression algorithm (auto-selects if None)
            content_type: Content type hint for algorithm selection

        Returns:
            Tuple of (compressed_data, algorithm_used)

        Raises:
            ValueError: If compression fails
        """
        try:
            # Auto-select algorithm if not specified
            if algorithm is None:
                algorithm = self.select_algorithm(
                    len(data), content_type=content_type
                )

            if algorithm == CompressionAlgorithm.NONE:
                return data, algorithm

            start_time = time.time()

            if algorithm == CompressionAlgorithm.GZIP:
                compressed = gzip.compress(data, compresslevel=self.config.gzip_level)
            elif algorithm == CompressionAlgorithm.BROTLI:
                if not BROTLI_AVAILABLE:
                    raise ValueError("Brotli not available")
                compressed = brotli.compress(
                    data, quality=self.config.brotli_quality
                )
            else:
                raise ValueError(f"Unknown compression algorithm: {algorithm}")

            duration_ms = (time.time() - start_time) * 1000

            # Only use compression if it actually reduces size
            if len(compressed) < len(data):
                self.metrics.record_compression(
                    algorithm, len(data), len(compressed), duration_ms
                )
                logger.debug(
                    f"Compressed {len(data)} bytes to {len(compressed)} bytes "
                    f"({(len(compressed) / len(data) * 100):.1f}%) using {algorithm.value}"
                )
                return compressed, algorithm
            else:
                logger.debug(
                    f"Compression increased size ({len(data)} -> {len(compressed)} bytes), "
                    f"sending uncompressed"
                )
                self.metrics.total_requests += 1
                return data, CompressionAlgorithm.NONE

        except Exception as e:
            self.metrics.record_error()
            logger.error(f"Compression error: {e}")
            # Return uncompressed data on error
            return data, CompressionAlgorithm.NONE

    def decompress(
        self, data: bytes, algorithm: CompressionAlgorithm
    ) -> bytes:
        """
        Decompress data using specified algorithm.

        Args:
            data: Compressed bytes
            algorithm: Compression algorithm used

        Returns:
            Decompressed bytes

        Raises:
            ValueError: If decompression fails
        """
        if algorithm == CompressionAlgorithm.NONE:
            return data

        try:
            start_time = time.time()

            if algorithm == CompressionAlgorithm.GZIP:
                decompressed = gzip.decompress(data)
            elif algorithm == CompressionAlgorithm.BROTLI:
                if not BROTLI_AVAILABLE:
                    raise ValueError("Brotli not available")
                decompressed = brotli.decompress(data)
            else:
                raise ValueError(f"Unknown compression algorithm: {algorithm}")

            duration_ms = (time.time() - start_time) * 1000
            self.metrics.record_decompression(duration_ms)

            logger.debug(
                f"Decompressed {len(data)} bytes to {len(decompressed)} bytes "
                f"using {algorithm.value}"
            )
            return decompressed

        except Exception as e:
            self.metrics.record_error()
            logger.error(f"Decompression error: {e}")
            raise ValueError(f"Failed to decompress data: {e}")

    def get_metrics(self) -> Dict:
        """Get compression metrics."""
        return self.metrics.get_metrics()
