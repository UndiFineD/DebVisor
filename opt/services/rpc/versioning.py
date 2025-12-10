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
API versioning support for gRPC RPC service.

Handles API version negotiation, routing to appropriate handlers,
and migration support between versions.

Features:
- Version detection and negotiation
- Version-specific request routing
- Backward compatibility layers
- Deprecation tracking
- Migration helpers for clients
"""

import logging
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class APIVersion(Enum):
    """Supported API versions."""

    V1_0 = "1.0"
    V2_0 = "2.0"
    V3_0 = "3.0"


@dataclass
class VersionInfo:
    """Information about an API version."""

    version: APIVersion
    released: datetime
    deprecated: Optional[datetime] = None
    removed: Optional[datetime] = None
    description: str = ""
    breaking_changes: Optional[List[str]] = None
    new_features: Optional[List[str]] = None
    migration_guide: str = ""

    def __post_init__(self) -> None:
        if self.breaking_changes is None:
            self.breaking_changes = []
        if self.new_features is None:
            self.new_features = []

    def is_deprecated(self) -> bool:
        """Check if version is deprecated."""
        if self.deprecated is None:
            return False
        return datetime.now(timezone.utc) >= self.deprecated

    def is_removed(self) -> bool:
        """Check if version is removed."""
        if self.removed is None:
            return False
        return datetime.now(timezone.utc) >= self.removed

    def get_status(self) -> str:
        """Get version status."""
        if self.is_removed():
            return "REMOVED"
        elif self.is_deprecated():
            return "DEPRECATED"
        else:
            return "ACTIVE"


class VersionNegotiator:
    """Handles version negotiation between client and server."""

    def __init__(self) -> None:
        """Initialize version negotiator."""
        # Register all supported versions
        self.versions: Dict[APIVersion, VersionInfo] = {
            APIVersion.V1_0: VersionInfo(
                version=APIVersion.V1_0,
                released=datetime(2024, 1, 1),
                description="Initial API with basic cluster operations",
                new_features=[
                    "Basic node management",
                    "Storage operations",
                    "Cluster health checks",
                ],
            ),
            APIVersion.V2_0: VersionInfo(
                version=APIVersion.V2_0,
                released=datetime(2024, 6, 1),
                deprecated=datetime(2026, 1, 1),
                description="Enhanced API with advanced operations",
                breaking_changes=[
                    "health_check endpoint returns structured data",
                    "storage_list now requires pool_id parameter",
                ],
                new_features=[
                    "Connection pooling support",
                    "Compression support (GZIP, Brotli)",
                    "Batch operations",
                    "Advanced filtering",
                ],
                migration_guide="See MIGRATION_V1_TO_V2.md",
            ),
            APIVersion.V3_0: VersionInfo(
                version=APIVersion.V3_0,
                released=datetime(2025, 11, 27),
                description="Next-gen API with streaming and advanced features",
                breaking_changes=[
                    "All request/response messages are protobuf3",
                    "Error responses use standard gRPC codes",
                ],
                new_features=[
                    "Server-side streaming for large result sets",
                    "Client-side streaming for bulk operations",
                    "Bidirectional streaming for real-time monitoring",
                    "Native gRPC metadata for auth/tracing",
                    "Extended retention policies (keep_daily_days)",
                ],
                migration_guide="See MIGRATION_V2_TO_V3.md",
            ),
        }

        # Track version adoption
        self.adoption_metrics: Dict[APIVersion, int] = {
            v: 0 for v in self.versions.keys()
        }

    def get_supported_versions(self) -> List[str]:
        """Get list of currently supported API versions."""
        return [v.version.value for v in self.versions.values() if not v.is_removed()]

    def get_version_info(self, version: APIVersion) -> Optional[VersionInfo]:
        """Get detailed information about a version."""
        return self.versions.get(version)

    def negotiate_version(
        self, client_versions: List[str], server_version: Optional[str] = None
    ) -> str:
        """
        Negotiate API version between client and server.

        Implements standard version negotiation:
        1. Find the highest client version supported by server
        2. Fall back to server's latest if no match
        3. Return negotiated version

        Args:
            client_versions: List of versions client supports (highest priority first)
            server_version: Preferred server version (defaults to latest)

        Returns:
            Negotiated API version string

        Raises:
            ValueError: If no compatible version found
        """
        supported = self.get_supported_versions()

        # Try to find highest client version that server supports
        for client_v in client_versions:
            if client_v in supported:
                self.adoption_metrics[APIVersion(client_v)] += 1
                logger.info(f"Version negotiated: client={client_v}")
                return client_v

        # Fallback to server's preferred version
        if server_version and server_version in supported:
            self.adoption_metrics[APIVersion(server_version)] += 1
            logger.warning(
                f"No client version compatible, using server default: {server_version}"
            )
            return server_version

        # Use server's latest version
        latest = APIVersion.V3_0    # or determine dynamically
        if latest.value in supported:
            self.adoption_metrics[latest] += 1
            logger.warning(f"No compatible version found, using latest: {latest.value}")
            return latest.value

        raise ValueError(
            f"No compatible API version found. Client: {client_versions}, Server: {supported}"
        )

    def validate_version(self, version_str: str) -> bool:
        """Validate that version string is supported."""
        try:
            version = APIVersion(version_str)
            version_info = self.versions.get(version)
            return version_info is not None and not version_info.is_removed()
        except ValueError:
            return False

    def get_adoption_metrics(self) -> Dict[str, int]:
        """Get version adoption metrics."""
        return {
            v.version.value: self.adoption_metrics[v.version] for v in self.versions.values()
        }

    def get_deprecation_warnings(self, version_str: str) -> List[str]:
        """Get deprecation warnings for a version."""
        warnings = []

        try:
            version = APIVersion(version_str)
            version_info = self.versions.get(version)

            if version_info is None:
                warnings.append(f"Version {version_str} not found")
                return warnings

            if version_info.is_removed():
                warnings.append(
                    f"Version {version_str} has been removed. Please upgrade."
                )
            elif version_info.is_deprecated():
                next_version = self._get_next_version(version)
                warnings.append(
                    f"Version {version_str} is deprecated. Please upgrade to {next_version.value}"
                )
                warnings.append(f"Migration guide: {version_info.migration_guide}")

        except ValueError:
            warnings.append(f"Unknown version: {version_str}")

        return warnings

    def _get_next_version(self, version: APIVersion) -> APIVersion:
        """Get next version after specified version."""
        version_order = [APIVersion.V1_0, APIVersion.V2_0, APIVersion.V3_0]
        idx = version_order.index(version)
        if idx < len(version_order) - 1:
            return version_order[idx + 1]
        return version


class VersionedRequestRouter:
    """Routes requests to appropriate version-specific handlers."""

    def __init__(self, negotiator: VersionNegotiator):
        """
        Initialize request router.

        Args:
            negotiator: VersionNegotiator instance
        """
        self.negotiator = negotiator
        self.handlers: Dict[APIVersion, Dict[str, Callable[..., Any]]] = {
            v: {} for v in APIVersion
        }

    def register_handler(
        self, version: APIVersion, operation: str, handler: Callable[..., Any]
    ) -> None:
        """
        Register a handler for a specific version and operation.

        Args:
            version: API version
            operation: Operation name (e.g., "list_nodes", "create_storage")
            handler: Callable to handle the operation
        """
        if version not in self.handlers:
            self.handlers[version] = {}

        self.handlers[version][operation] = handler
        logger.debug(f"Registered handler: {version.value}/{operation}")

    def route(self, version_str: str, operation: str, *args: Any, **kwargs: Any) -> Any:
        """
        Route request to appropriate handler.

        Args:
            version_str: API version string
            operation: Operation name
            *args: Arguments to pass to handler
            **kwargs: Keyword arguments to pass to handler

        Returns:
            Result from handler

        Raises:
            ValueError: If version not supported
            KeyError: If operation not found for version
        """
        try:
            version = APIVersion(version_str)
        except ValueError:
            raise ValueError(f"Unknown API version: {version_str}")

        if version not in self.handlers:
            raise ValueError(f"No handlers for version: {version_str}")

        if operation not in self.handlers[version]:
            raise KeyError(
                f"Operation '{operation}' not found for version {version_str}"
            )

        handler = self.handlers[version][operation]
        logger.debug(f"Routing {version_str}/{operation} to handler")

        return handler(*args, **kwargs)

    def get_compatibility_matrix(self) -> Dict[str, List[str]]:
        """Get operation compatibility across versions."""
        matrix = {}
        for version, operations in self.handlers.items():
            matrix[version.value] = list(operations.keys())
        return matrix


class BackwardCompatibilityLayer:
    """Provides backward compatibility for older API versions."""

    @staticmethod
    def convert_v1_response_to_v2(v1_response: Dict[str, Any]) -> Dict[str, Any]:
        """Convert V1 response to V2 format."""
        # Example transformation logic
        if "nodes" in v1_response:
            v1_response["nodes_list"] = v1_response.pop("nodes")
        if "status" in v1_response:
            v1_response["status_code"] = {
                "healthy": 200,
                "degraded": 202,
                "unhealthy": 500,
            }.get(v1_response["status"], 500)
        return v1_response

    @staticmethod
    def convert_v2_request_to_v1(v2_request: Dict[str, Any]) -> Dict[str, Any]:
        """Convert V2 request to V1 format for legacy backend."""
        # Example transformation logic
        if "pool_id" in v2_request:
            # V1 doesn't support pool filtering, remove it
            v2_request.pop("pool_id", None)
        return v2_request
