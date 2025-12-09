#!/usr/bin/env python3
"""
API Versioning Support for DebVisor.

Implements enterprise-grade API versioning with:
- URL-based versioning (e.g., /api/v1/nodes, /api/v2/nodes)
- Header-based versioning (Accept-Version header)
- Deprecation warnings and sunset headers
- Version negotiation
- Backward compatibility helpers

Author: DebVisor Team
Date: November 28, 2025
"""

import functools
from unittest.mock import patch
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class VersionStatus(Enum):
    """API version lifecycle status."""

    PREVIEW = "preview"  # Not stable, may change
    EXPERIMENTAL = "preview"  # Alias for PREVIEW
    CURRENT = "current"  # Recommended version
    STABLE = "current"  # Alias for CURRENT
    SUPPORTED = "supported"  # Still supported but not recommended
    DEPRECATED = "deprecated"  # Will be removed
    SUNSET = "sunset"  # No longer available


@dataclass
class APIVersion:
    """
    API version definition.

    Attributes:
        major: Major version number
        minor: Minor version number (optional)
        patch: Patch version number (optional)
        status: Version lifecycle status
        introduced: Date version was introduced
        deprecated: Date version was deprecated (if applicable)
        sunset: Date version will be/was removed
        changelog: Description of changes in this version
    """

    major: int
    minor: int = 0
    patch: int = 0
    status: VersionStatus = VersionStatus.CURRENT
    introduced: Optional[datetime] = None
    deprecated: Optional[datetime] = None
    sunset: Optional[datetime] = None
    changelog: str = ""

    @property
    def string(self) -> str:
        """Version as string (e.g., 'v1', 'v2.1')."""
        if self.minor == 0:
            return f"v{self.major}"
        return f"v{self.major}.{self.minor}"

    @property
    def short_string(self) -> str:
        """Version as short string (e.g., '2.1')."""
        if self.minor == 0:
            return f"{self.major}"
        return f"{self.major}.{self.minor}"

    def __str__(self) -> str:
        """String representation (e.g., '2.1.0')."""
        return f"{self.major}.{self.minor}.{self.patch}"

    @classmethod
    def from_string(cls, version_str: str) -> "APIVersion":
        """
        Parse version from string.

        Supports:
        - "2.1.3" -> major=2, minor=1, patch=3
        - "2.1" -> major=2, minor=1, patch=0
        - "3" -> major=3, minor=0, patch=0
        """
        parts = version_str.strip().lstrip("v").split(".")
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        return cls(major=major, minor=minor, patch=patch)

    @property
    def is_active(self) -> bool:
        """Check if version is still usable."""
        if self.status == VersionStatus.SUNSET:
            return False
        if self.sunset and datetime.now(timezone.utc) >= self.sunset:
            return False
        return True

    @property
    def is_deprecated(self) -> bool:
        """Check if version is deprecated."""
        return self.status in (VersionStatus.DEPRECATED, VersionStatus.SUNSET)

    def __lt__(self, other: "APIVersion") -> bool:
        return (self.major, self.minor, self.patch) < (
            other.major,
            other.minor,
            other.patch,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, APIVersion):
            return False
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.patch))


@dataclass
class VersionedEndpoint:
    """Endpoint with version-specific handlers."""

    path: str
    versions: Dict[str, Dict[str, Any]] = field(
        default_factory=dict
    )  # version -> {handler, ...}
    methods: List[str] = field(default_factory=lambda: ["GET"])
    deprecated_versions: Set[str] = field(default_factory=set)

    # Backward compatibility alias
    @property
    def handlers(self) -> Dict[str, Callable[..., Any]]:
        """Get handlers dict for compatibility."""
        return {
            v: info["handler"] for v, info in self.versions.items() if "handler" in info
        }

    def get_handler(self, version: str) -> Optional[Callable[..., Any]]:
        """Get handler for specific version."""
        version_info = self.versions.get(version)
        if version_info and "handler" in version_info:
            return version_info["handler"]  # type: ignore
        return None


class APIVersionManager:
    """
    Manages API versions for the application.

    Example:
        version_mgr = APIVersionManager()

        # Define versions
        version_mgr.register_version(APIVersion(
            major=1,
            status=VersionStatus.SUPPORTED,
            introduced=datetime(2024, 1, 1, tzinfo=timezone.utc)
        ))
        version_mgr.register_version(APIVersion(
            major=2,
            status=VersionStatus.CURRENT,
            introduced=datetime(2025, 6, 1, tzinfo=timezone.utc)
        ))

        # Use with Flask
        @app.route("/api/<version>/nodes")
        @version_mgr.versioned
        def get_nodes(version):
            return jsonify(nodes)
    """

    def __init__(self, default_version: Optional[str] = None, app: Any = None) -> None:
        """
        Initialize version manager.

        Args:
            default_version: Default version to use if not specified
            app: Flask app instance (optional)
        """
        self._versions: Dict[str, APIVersion] = {}
        self._default_version = default_version
        self._endpoints: Dict[str, VersionedEndpoint] = {}
        self.app = app
        self.config: Dict[str, Any] = {
            "version_source": "header",  # header, url, query, accept
        }
        self._version_changes: Dict[str, List[Dict[str, Any]]] = {}

    @property
    def versions(self) -> Dict[str, Dict[str, Any]]:
        """Get versions dict for external access."""
        return {
            v.string: {
                "version": v,
                "status": v.status,
                "sunset_date": v.sunset,
            }
            for v in self._versions.values()
        }

    def register_version(
        self,
        version: APIVersion,
        sunset_date: Optional[datetime] = None,
        changes: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        Register an API version.

        Args:
            version: API version to register
            sunset_date: Optional sunset date (overrides version.sunset)
            changes: Optional list of changes for this version
        """
        if sunset_date:
            version.sunset = sunset_date

        self._versions[version.string] = version

        # Store changes if provided
        if changes:
            self._version_changes[version.string] = changes

        # Update default if this is the current version
        if version.status == VersionStatus.CURRENT:
            self._default_version = version.string

        logger.info(
            f"Registered API version: {version.string} ({version.status.value})"
        )

    def get_version(self, version_string: str) -> Optional[APIVersion]:
        """Get version by string."""
        return self._versions.get(version_string)

    @property
    def current_version(self) -> Optional[APIVersion]:
        """Get the current (recommended) version."""
        current_versions = [
            v for v in self._versions.values() if v.status == VersionStatus.CURRENT
        ]
        if current_versions:
            # Return the highest version number if multiple CURRENT versions
            return max(current_versions)
        return None

    def get_current_version(self) -> Optional[APIVersion]:
        """Get the current (recommended) version (method form)."""
        return self.current_version

    def list_versions(self, active_only: bool = False) -> List[APIVersion]:
        """List all or active versions."""
        if active_only:
            return [v for v in self._versions.values() if v.is_active]
        return list(self._versions.values())

    def get_requested_version(self) -> Optional[APIVersion]:
        """
        Extract requested version from Flask request context.

        Checks based on config['version_source']:
        - 'header': API-Version header
        - 'url': /v1/ in path
        - 'query': ?version=1.0
        - 'accept': Accept header
        """
        try:
            from flask import request

            source = self.config.get("version_source", "header")

            if source == "header":
                version_str = request.headers.get("API-Version")
                if version_str:
                    return self.parse_version(version_str)

            elif source == "url":
Extract from path like /v2/users
                import re

                match = re.search(r"/v(\d+(?:\.\d+)?)", request.path)
                if match:
                    return self.parse_version(f"v{match.group(1)}")

            elif source == "query":
                version_str = request.args.get("version")
                if version_str:
                    return self.parse_version(version_str)

            elif source == "accept":
                accept = request.headers.get("Accept", "")
                # Parse custom media types like application/vnd.debvisor.v2+json

                match = re.search(r"\.v(\d+(?:\.\d+)?)", accept)
                if match:
                    return self.parse_version(f"v{match.group(1)}")

            # Fall back to current version
            return self.current_version

        except (ImportError, RuntimeError):
            # Not in Flask context
            return self.current_version

    def get_migration_path(
        self, from_version: APIVersion, to_version: APIVersion
    ) -> List[APIVersion]:
        """
        Get migration path between versions.

        Returns list of versions to migrate through.
        """
        all_versions = sorted(self._versions.values())

        try:
            from_idx = all_versions.index(from_version)
            to_idx = all_versions.index(to_version)

            if from_idx < to_idx:
                return all_versions[from_idx : to_idx + 1]
            else:
                return all_versions[to_idx : from_idx + 1][::-1]
        except ValueError:
            return [from_version, to_version]

    def get_breaking_changes(
        self, from_version: APIVersion, to_version: APIVersion
    ) -> List[Dict[str, Any]]:
        """
        Get breaking changes between versions.
        """
        if not hasattr(self, "_version_changes"):
            return []

        changes = self._version_changes.get(to_version.string, [])
        return [c for c in changes if c.get("type") == "breaking"]

    def get_response_headers(self) -> Dict[str, str]:
        """
        Get version-related response headers for current request.
        """
        try:
            from flask import g

            headers = {}

            if hasattr(g, "api_version"):
                headers["X-API-Version"] = g.api_version.string

                if g.api_version.is_deprecated:
                    headers["Deprecation"] = "true"
                    if g.api_version.sunset:
                        headers["Sunset"] = g.api_version.sunset.strftime(
                            "%a, %d %b %Y %H:%M:%S GMT"
                        )

            return headers

        except (ImportError, RuntimeError, AttributeError):
            return {}

    @property
    def supported_versions(self) -> List[APIVersion]:
        """Get all supported versions."""
        return [v for v in self._versions.values() if v.is_active]

    def is_supported(self, version_string: str) -> bool:
        """Check if a version is supported."""
        version = self._versions.get(version_string)
        return version is not None and version.is_active

    def get_deprecation_info(self, version_string: str) -> Optional[Dict[str, Any]]:
        """Get deprecation information for a version."""
        version = self._versions.get(version_string)
        if not version or not version.is_deprecated:
            return None

        return {
            "version": version.string,
            "status": version.status.value,
            "deprecated_at": (
                version.deprecated.isoformat() if version.deprecated else None
            ),
            "sunset_at": version.sunset.isoformat() if version.sunset else None,
            "migration_guide": f"/docs/migration/{version.string}",
        }

    def parse_version(self, version_string: str) -> Optional[APIVersion]:
        """
        Parse version string and return matching version.

        Supports:
        - Exact match: "v1", "v2.1"
        - Major only: "1" -> "v1"
        - With prefix: "version-1" -> "v1"
        """
        # Clean up version string
        cleaned = version_string.lower().strip()
        cleaned = cleaned.replace("version-", "").replace("version", "")

        if not cleaned.startswith("v"):
            cleaned = f"v{cleaned}"

        return self._versions.get(cleaned)

    def negotiate_version(
        self, requested: Optional[str] = None, accept_header: Optional[str] = None
    ) -> Tuple[Optional[APIVersion], List[str]]:
        """
        Negotiate API version from request.

        Args:
            requested: Explicitly requested version (from URL or query)
            accept_header: Accept-Version header value

        Returns:
            Tuple of (negotiated_version, warnings)
        """
        warnings_list: List[str] = []

        # Try explicit version first
        if requested:
            version = self.parse_version(requested)
            if version:
                if version.is_deprecated:
                    warnings_list.append(
                        f"API version {version.string} is deprecated. Please migrate to "
                        f"{self.current_version.string if self.current_version else 'a newer version'}."
                    )
                if not version.is_active:
                    warnings_list.append(
                        f"API version {version.string} is no longer available."
                    )
                    return None, warnings_list
                return version, warnings_list
            else:
                warnings_list.append(f"Unknown API version: {requested}")

        # Try Accept-Version header
        if accept_header:
            version = self.parse_version(accept_header)
            if version and version.is_active:
                if version.is_deprecated:
                    warnings_list.append(f"API version {version.string} is deprecated.")
                return version, warnings_list

        # Fall back to default
        if self._default_version:
            return self._versions.get(self._default_version), warnings_list

        # Use current version
        return self.current_version, warnings_list

    def versioned(self, func: F) -> F:
        """
        Decorator to add version handling to endpoint.

        Extracts version from route parameter and adds deprecation headers.

        Example:
            @app.route("/api/<version>/nodes")
            @version_mgr.versioned
            def get_nodes(version):
                return jsonify(nodes)
        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            from flask import request, g, make_response

Get version from route or header
            version_string = kwargs.get("version") or request.headers.get(
                "Accept-Version"
            )

            version, warnings_list = self.negotiate_version(
                requested=version_string,
                accept_header=request.headers.get("Accept-Version"),
            )

            if not version or not version.is_active:
                from flask import jsonify

                return (
                    jsonify(
                        {
                            "error": "Unsupported API version",
                            "code": "VERSION_NOT_SUPPORTED",
                            "supported_versions": [
                                v.string for v in self.supported_versions
                            ],
                            "warnings": warnings_list,
                        }
                    ),
                    400,
                )

            # Store version in request context
            g.api_version = version

            # Call the handler
            result = func(*args, **kwargs)

            # Ensure we have a response object
            if not hasattr(result, "headers"):
                result = make_response(result)

            # Add version headers
            result.headers["X-API-Version"] = version.string

            # Add deprecation headers if applicable
            if version.is_deprecated:
                result.headers["Deprecation"] = "true"
                if version.sunset:
                    result.headers["Sunset"] = version.sunset.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                result.headers["X-Deprecation-Notice"] = (
                    "This API version is deprecated. Please migrate to "
                    f"{self.current_version.string if self.current_version else 'a newer version'}."
                )

            # Add warnings header
            for i, warning in enumerate(warnings_list):
                result.headers["Warning"] = f'299 - "{warning}"'

            return result

        return wrapper  # type: ignore

    def deprecated(
        self,
        since_version: str,
        use_instead: Optional[str] = None,
        removal_version: Optional[str] = None,
    ) -> Callable[[F], F]:
        """
        Mark an endpoint as deprecated.

        Example:
            @app.route("/api/v1/old-endpoint")
            @version_mgr.deprecated(
                since_version="v2",
                use_instead="/api/v2/new-endpoint",
                removal_version="v3"
            )
            def old_endpoint():
                return jsonify(data)
        """

        def decorator(func: F) -> F:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                from flask import make_response

                # Log deprecation warning
                logger.warning(
                    f"Deprecated endpoint called: {func.__name__} "
                    f"(deprecated since {since_version})"
                )

                result = func(*args, **kwargs)

                if not hasattr(result, "headers"):
                    result = make_response(result)

                # Add deprecation headers
                result.headers["Deprecation"] = "true"
                result.headers["X-Deprecated-Since"] = since_version

                if use_instead:
                    result.headers["Link"] = f'<{use_instead}>; rel="successor-version"'

                if removal_version:
                    result.headers["X-Removal-Version"] = removal_version

                return result

            return wrapper  # type: ignore

        return decorator

    def get_version_info(self) -> Dict[str, Any]:
        """Get information about all API versions."""
        return {
            "versions": [
                {
                    "version": v.string,
                    "status": v.status.value,
                    "introduced": v.introduced.isoformat() if v.introduced else None,
                    "deprecated": v.deprecated.isoformat() if v.deprecated else None,
                    "sunset": v.sunset.isoformat() if v.sunset else None,
                    "is_active": v.is_active,
                    "changelog": v.changelog,
                }
                for v in sorted(self._versions.values(), reverse=True)
            ],
            "current": self.current_version.string if self.current_version else None,
            "default": self._default_version,
        }


# =============================================================================
# Flask Blueprint for Version Discovery
# =============================================================================


def create_version_blueprint(manager: APIVersionManager) -> Any:
    """
    Create Flask blueprint for version discovery endpoints.

    Example:
        version_bp = create_version_blueprint(version_mgr)
        app.register_blueprint(version_bp, url_prefix="/api")
    """
    from flask import Blueprint, jsonify

    bp = Blueprint("api_versions", __name__)

    @bp.route("/versions")
    def list_versions() -> Any:
        """List all API versions."""
        return jsonify(manager.get_version_info())

    @bp.route("/versions/current")
    def current_version() -> Any:
        """Get current API version."""
        current = manager.current_version
        if not current:
            return jsonify({"error": "No current version defined"}), 500
        return jsonify(
            {
                "version": current.string,
                "status": current.status.value,
            }
        )

    @bp.route("/versions/<version_string>")
    def get_version_details(version_string: str) -> Any:
        """Get details for a specific version."""
        version = manager.get_version(version_string)
        if not version:
            return (
                jsonify(
                    {
                        "error": f"Unknown version: {version_string}",
                        "supported": [v.string for v in manager.supported_versions],
                    }
                ),
                404,
            )

        return jsonify(
            {
                "version": version.string,
                "status": version.status.value,
                "introduced": (
                    version.introduced.isoformat() if version.introduced else None
                ),
                "deprecated": (
                    version.deprecated.isoformat() if version.deprecated else None
                ),
                "sunset": version.sunset.isoformat() if version.sunset else None,
                "is_active": version.is_active,
                "changelog": version.changelog,
            }
        )

    return bp


# =============================================================================
# Default Version Manager
# =============================================================================


def get_default_version_manager() -> APIVersionManager:
    """
    Get default API version manager with DebVisor versions.
    """
    manager = APIVersionManager()

    # Register DebVisor API versions
    manager.register_version(
        APIVersion(
            major=1,
            minor=0,
            status=VersionStatus.SUPPORTED,
            introduced=datetime(2024, 6, 1, tzinfo=timezone.utc),
            deprecated=datetime(2025, 6, 1, tzinfo=timezone.utc),
            sunset=datetime(2026, 1, 1, tzinfo=timezone.utc),
            changelog="Initial API release",
        )
    )

    manager.register_version(
        APIVersion(
            major=2,
            minor=0,
            status=VersionStatus.CURRENT,
            introduced=datetime(2025, 6, 1, tzinfo=timezone.utc),
            changelog=(
                "- Enhanced authentication with OIDC support\n"
                "- GraphQL endpoint\n"
                "- Improved error responses\n"
                "- New passthrough management endpoints"
            ),
        )
    )

    manager.register_version(
        APIVersion(
            major=3,
            minor=0,
            status=VersionStatus.PREVIEW,
            introduced=datetime(2025, 11, 1, tzinfo=timezone.utc),
            changelog=(
                "- Breaking changes to node management API\n"
                "- New federation endpoints\n"
                "- Async operation support"
            ),
        )
    )

    return manager


# =============================================================================
# Module-level decorators for backward compatibility
# =============================================================================

# Global manager instance for standalone decorators
_module_manager: Optional[APIVersionManager] = None


def get_module_manager() -> APIVersionManager:
    """Get or create module-level version manager."""
    global _module_manager
    if _module_manager is None:
        _module_manager = get_default_version_manager()
    return _module_manager


def versioned(func: F) -> F:
    """
    Module-level versioned decorator.
    Uses default version manager.

    Example:
        @versioned
        def my_endpoint(version):
            return {"data": "value"}
    """
    return get_module_manager().versioned(func)


def deprecated(
    since_version: str,
    use_instead: Optional[str] = None,
    removal_version: Optional[str] = None,
) -> Callable[[F], F]:
    """
    Module-level deprecated decorator.
    Uses default version manager.

    Example:
        @deprecated(since_version="v2", removal_version="v3")
        def old_endpoint():
            return {"data": "value"}
    """
    return get_module_manager().deprecated(
        since_version=since_version,
        use_instead=use_instead,
        removal_version=removal_version,
    )


def sunset(version_string: str) -> Callable[[F], F]:
    """
    Mark endpoint as sunset (removed in this version).

    Example:
        @sunset("v3")
        def removed_endpoint():
            return {"error": "Endpoint removed"}
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            from flask import jsonify

            return (
                jsonify(
                    {
                        "error": f"This endpoint was removed in API {version_string}",
                        "code": "ENDPOINT_SUNSET",
                        "sunset_version": version_string,
                    }
                ),
                410,
            )  # Gone

        return wrapper  # type: ignore

    return decorator
