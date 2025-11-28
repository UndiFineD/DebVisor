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
import logging
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar('F', bound=Callable[..., Any])


class VersionStatus(Enum):
    """API version lifecycle status."""
    PREVIEW = "preview"       # Not stable, may change
    CURRENT = "current"       # Recommended version
    SUPPORTED = "supported"   # Still supported but not recommended
    DEPRECATED = "deprecated" # Will be removed
    SUNSET = "sunset"         # No longer available


@dataclass
class APIVersion:
    """
    API version definition.
    
    Attributes:
        major: Major version number
        minor: Minor version number (optional)
        status: Version lifecycle status
        introduced: Date version was introduced
        deprecated: Date version was deprecated (if applicable)
        sunset: Date version will be/was removed
        changelog: Description of changes in this version
    """
    major: int
    minor: int = 0
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
        return (self.major, self.minor) < (other.major, other.minor)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, APIVersion):
            return False
        return self.major == other.major and self.minor == other.minor
    
    def __hash__(self) -> int:
        return hash((self.major, self.minor))


@dataclass
class VersionedEndpoint:
    """Endpoint with version-specific handlers."""
    path: str
    handlers: Dict[str, Callable] = field(default_factory=dict)  # version -> handler
    deprecated_versions: Set[str] = field(default_factory=set)


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
    
    def __init__(self, default_version: Optional[str] = None):
        """
        Initialize version manager.
        
        Args:
            default_version: Default version to use if not specified
        """
        self._versions: Dict[str, APIVersion] = {}
        self._default_version = default_version
        self._endpoints: Dict[str, VersionedEndpoint] = {}
    
    def register_version(self, version: APIVersion) -> None:
        """
        Register an API version.
        
        Args:
            version: API version to register
        """
        self._versions[version.string] = version
        
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
        for v in self._versions.values():
            if v.status == VersionStatus.CURRENT:
                return v
        return None
    
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
            "deprecated_at": version.deprecated.isoformat() if version.deprecated else None,
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
        self,
        requested: Optional[str] = None,
        accept_header: Optional[str] = None
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
                        f"API version {version.string} is deprecated. "
                        f"Please migrate to {self.current_version.string if self.current_version else 'a newer version'}."
                    )
                if not version.is_active:
                    warnings_list.append(f"API version {version.string} is no longer available.")
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
        def wrapper(*args, **kwargs):
            from flask import request, g, make_response
            
            # Get version from route or header
            version_string = kwargs.get("version") or request.headers.get("Accept-Version")
            
            version, warnings_list = self.negotiate_version(
                requested=version_string,
                accept_header=request.headers.get("Accept-Version")
            )
            
            if not version or not version.is_active:
                from flask import jsonify
                return jsonify({
                    "error": "Unsupported API version",
                    "code": "VERSION_NOT_SUPPORTED",
                    "supported_versions": [v.string for v in self.supported_versions],
                    "warnings": warnings_list,
                }), 400
            
            # Store version in request context
            g.api_version = version
            
            # Call the handler
            result = func(*args, **kwargs)
            
            # Ensure we have a response object
            if not hasattr(result, 'headers'):
                result = make_response(result)
            
            # Add version headers
            result.headers["X-API-Version"] = version.string
            
            # Add deprecation headers if applicable
            if version.is_deprecated:
                result.headers["Deprecation"] = "true"
                if version.sunset:
                    result.headers["Sunset"] = version.sunset.strftime("%a, %d %b %Y %H:%M:%S GMT")
                result.headers["X-Deprecation-Notice"] = (
                    f"This API version is deprecated. "
                    f"Please migrate to {self.current_version.string if self.current_version else 'a newer version'}."
                )
            
            # Add warnings header
            for i, warning in enumerate(warnings_list):
                result.headers[f"Warning"] = f'299 - "{warning}"'
            
            return result
        
        return wrapper  # type: ignore
    
    def deprecated(
        self,
        since_version: str,
        use_instead: Optional[str] = None,
        removal_version: Optional[str] = None
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
            def wrapper(*args, **kwargs):
                from flask import make_response
                
                # Log deprecation warning
                logger.warning(
                    f"Deprecated endpoint called: {func.__name__} "
                    f"(deprecated since {since_version})"
                )
                
                result = func(*args, **kwargs)
                
                if not hasattr(result, 'headers'):
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

def create_version_blueprint(manager: APIVersionManager):
    """
    Create Flask blueprint for version discovery endpoints.
    
    Example:
        version_bp = create_version_blueprint(version_mgr)
        app.register_blueprint(version_bp, url_prefix="/api")
    """
    from flask import Blueprint, jsonify
    
    bp = Blueprint("api_versions", __name__)
    
    @bp.route("/versions")
    def list_versions():
        """List all API versions."""
        return jsonify(manager.get_version_info())
    
    @bp.route("/versions/current")
    def current_version():
        """Get current API version."""
        current = manager.current_version
        if not current:
            return jsonify({"error": "No current version defined"}), 500
        return jsonify({
            "version": current.string,
            "status": current.status.value,
        })
    
    @bp.route("/versions/<version_string>")
    def get_version_details(version_string: str):
        """Get details for a specific version."""
        version = manager.get_version(version_string)
        if not version:
            return jsonify({
                "error": f"Unknown version: {version_string}",
                "supported": [v.string for v in manager.supported_versions]
            }), 404
        
        return jsonify({
            "version": version.string,
            "status": version.status.value,
            "introduced": version.introduced.isoformat() if version.introduced else None,
            "deprecated": version.deprecated.isoformat() if version.deprecated else None,
            "sunset": version.sunset.isoformat() if version.sunset else None,
            "is_active": version.is_active,
            "changelog": version.changelog,
        })
    
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
    manager.register_version(APIVersion(
        major=1,
        minor=0,
        status=VersionStatus.SUPPORTED,
        introduced=datetime(2024, 6, 1, tzinfo=timezone.utc),
        deprecated=datetime(2025, 6, 1, tzinfo=timezone.utc),
        sunset=datetime(2026, 1, 1, tzinfo=timezone.utc),
        changelog="Initial API release"
    ))
    
    manager.register_version(APIVersion(
        major=2,
        minor=0,
        status=VersionStatus.CURRENT,
        introduced=datetime(2025, 6, 1, tzinfo=timezone.utc),
        changelog=(
            "- Enhanced authentication with OIDC support\n"
            "- GraphQL endpoint\n"
            "- Improved error responses\n"
            "- New passthrough management endpoints"
        )
    ))
    
    manager.register_version(APIVersion(
        major=3,
        minor=0,
        status=VersionStatus.PREVIEW,
        introduced=datetime(2025, 11, 1, tzinfo=timezone.utc),
        changelog=(
            "- Breaking changes to node management API\n"
            "- New federation endpoints\n"
            "- Async operation support"
        )
    ))
    
    return manager
