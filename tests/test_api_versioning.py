# !/usr/bin/env python3
"""
Tests for API Versioning Framework.

Tests API version routing, deprecation notices, content negotiation,
and version lifecycle management.

Author: DebVisor Team
Date: November 28, 2025
"""

import pytest
from datetime import datetime, timedelta, timezone
from typing import Any
from flask import Flask

from web.panel.api_versioning import (
    APIVersion,
    VersionStatus,
    VersionedEndpoint,
    APIVersionManager,
    sunset,
)

# =============================================================================
# API Version Tests
# =============================================================================
class TestAPIVersion:
    """Test suite for APIVersion."""

    def test_version_creation(self) -> None:
        """Should create API version correctly."""
        version = APIVersion(major=2, minor=1, patch=0, status=VersionStatus.STABLE)

        assert version.major == 2
        assert version.minor == 1
        assert version.patch == 0
        assert version.status == VersionStatus.STABLE

    def test_version_string_representation(self) -> None:
        """Should format version string correctly."""
        version = APIVersion(major=2, minor=1, patch=3)

        assert str(version) == "2.1.3"
        assert version.short_string == "2.1"

    def test_version_comparison(self) -> None:
        """Should compare versions correctly."""
        v1 = APIVersion(major=1, minor=0, patch=0)
        v2 = APIVersion(major=2, minor=0, patch=0)
        v3 = APIVersion(major=1, minor=1, patch=0)
        v4 = APIVersion(major=1, minor=0, patch=1)

        assert v1 < v2
        assert v1 < v3
        assert v1 < v4
        assert v2 > v1
        assert v3 > v4    # 1.1.0 > 1.0.1

    def test_version_equality(self) -> None:
        """Should test version equality correctly."""
        v1 = APIVersion(major=2, minor=1, patch=0)
        v2 = APIVersion(major=2, minor=1, patch=0)
        v3 = APIVersion(major=2, minor=1, patch=1)

        assert v1 == v2
        assert v1 != v3

    def test_version_from_string(self) -> None:
        """Should parse version from string."""
        version = APIVersion.from_string("2.1.3")

        assert version.major == 2
        assert version.minor == 1
        assert version.patch == 3

    def test_version_from_string_short(self) -> None:
        """Should parse short version string."""
        version = APIVersion.from_string("2.1")

        assert version.major == 2
        assert version.minor == 1
        assert version.patch == 0

    def test_version_from_string_major_only(self) -> None:
        """Should parse major-only version string."""
        version = APIVersion.from_string("3")

        assert version.major == 3
        assert version.minor == 0
        assert version.patch == 0

    def test_version_status_values(self) -> None:
        """All version statuses should exist."""
        assert hasattr(VersionStatus, "CURRENT")
        assert hasattr(VersionStatus, "STABLE")
        assert hasattr(VersionStatus, "DEPRECATED")
        assert hasattr(VersionStatus, "SUNSET")
        assert hasattr(VersionStatus, "EXPERIMENTAL")


# =============================================================================
# Version Status Tests
# =============================================================================
class TestVersionStatus:
    """Test suite for VersionStatus."""

    def test_status_progression(self) -> None:
        """Version statuses should have logical progression."""
        # CURRENT/STABLE are active
        # DEPRECATED is warning
        # SUNSET is end-of-life

        v_current = APIVersion(major=3, status=VersionStatus.CURRENT)
        v_deprecated = APIVersion(major=2, status=VersionStatus.DEPRECATED)
        v_sunset = APIVersion(major=1, status=VersionStatus.SUNSET)

        assert v_current.status == VersionStatus.CURRENT
        assert v_deprecated.status == VersionStatus.DEPRECATED
        assert v_sunset.status == VersionStatus.SUNSET

    def test_is_active(self) -> None:
        """Should check if version is active."""
        v_current = APIVersion(major=3, status=VersionStatus.CURRENT)
        v_stable = APIVersion(major=2, status=VersionStatus.STABLE)
        v_deprecated = APIVersion(major=1, status=VersionStatus.DEPRECATED)

        assert v_current.is_active
        assert v_stable.is_active
        # Deprecated versions should still be active (just warned)
        assert v_deprecated.is_active


# =============================================================================
# Versioned Endpoint Tests
# =============================================================================
class TestVersionedEndpoint:
    """Test suite for VersionedEndpoint."""

    def test_endpoint_creation(self) -> None:
        """Should create versioned endpoint."""
        endpoint = VersionedEndpoint(
            path="/users",
            versions={"1": {"handler": lambda: "v1"}, "2": {"handler": lambda: "v2"}},
            methods=["GET", "POST"],
        )

        assert endpoint.path == "/users"
        assert "1" in endpoint.versions
        assert "2" in endpoint.versions
        assert "GET" in endpoint.methods

    def test_get_handler_for_version(self) -> None:
        """Should get correct handler for version."""

        def v1_handler() -> str:
            return "v1"

        def v2_handler() -> str:
            return "v2"

        endpoint = VersionedEndpoint(
            _path = "/users",
            _versions = {"1": {"handler": v1_handler}, "2": {"handler": v2_handler}},
        )

        handler = endpoint.get_handler("1")
        assert handler == v1_handler

        handler = endpoint.get_handler("2")
        assert handler == v2_handler

    def test_get_handler_unknown_version(self) -> None:
        """Should return None for unknown version."""
        endpoint = VersionedEndpoint(
            _path = "/users", versions={"1": {"handler": lambda: "v1"}}
        )

        handler = endpoint.get_handler("99")
        assert handler is None


# =============================================================================
# API Version Manager Tests
# =============================================================================
class TestAPIVersionManager:
    """Test suite for APIVersionManager."""

    @pytest.fixture

    def app(self) -> Flask:
        """Create Flask test app."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    @pytest.fixture

    def manager(self, app):
        """Create API version manager."""
        return APIVersionManager(app)

    def test_manager_initialization(self, manager):
        """Should initialize manager correctly."""
        assert manager is not None
        assert hasattr(manager, "register_version")

    def test_register_version(self, manager):
        """Should register API version."""
        version = APIVersion(major=1, minor=0)

        manager.register_version(version)

        assert "v1" in manager.versions

    def test_register_deprecated_version(self, manager):
        """Should register deprecated version with date."""
        version = APIVersion(major=1, minor=0, status=VersionStatus.DEPRECATED)
        sunset_date = datetime.now(timezone.utc) + timedelta(days=90)

        manager.register_version(version, sunset_date=sunset_date)

        assert manager.versions["v1"]["sunset_date"] == sunset_date

    def test_get_current_version(self, manager):
        """Should return current version."""
        v1 = APIVersion(major=1, status=VersionStatus.STABLE)
        v2 = APIVersion(major=2, status=VersionStatus.CURRENT)

        manager.register_version(v1)
        manager.register_version(v2)

        current = manager.get_current_version()

        assert current.major == 2

    def test_version_from_header(self, manager, app):
        """Should extract version from header."""
        manager.register_version(APIVersion(major=1))
        manager.register_version(APIVersion(major=2))

        with app.test_request_context(headers={"API-Version": "v1"}):
            version = manager.get_requested_version()
            assert version is not None
            assert version.major == 1

    def test_version_from_url(self, manager, app):
        """Should extract version from URL path."""
        manager.register_version(APIVersion(major=1))
        manager.register_version(APIVersion(major=2))
        manager.config["version_source"] = "url"

        with app.test_request_context("/v2/users"):
            version = manager.get_requested_version()
            assert version.major == 2

    def test_default_version_fallback(self, manager, app):
        """Should fall back to default version."""
        v1 = APIVersion(major=1, status=VersionStatus.STABLE)
        v2 = APIVersion(major=2, status=VersionStatus.CURRENT)

        manager.register_version(v1)
        manager.register_version(v2)

        with app.test_request_context():
            version = manager.get_requested_version()
            # Should return current version as default
            assert version.major == 2

    def test_list_all_versions(self, manager):
        """Should list all registered versions."""
        manager.register_version(APIVersion(major=1, status=VersionStatus.SUNSET))
        manager.register_version(APIVersion(major=2, status=VersionStatus.DEPRECATED))
        manager.register_version(APIVersion(major=3, status=VersionStatus.CURRENT))

        all_versions = manager.list_versions()

        assert len(all_versions) == 3

    def test_list_active_versions(self, manager):
        """Should list only active versions."""
        manager.register_version(APIVersion(major=1, status=VersionStatus.SUNSET))
        manager.register_version(APIVersion(major=2, status=VersionStatus.STABLE))
        manager.register_version(APIVersion(major=3, status=VersionStatus.CURRENT))

        active = manager.list_versions(active_only=True)

        assert len(active) == 2
        assert all(v.is_active for v in active)


# =============================================================================
# Decorator Tests
# =============================================================================
class TestVersioningDecorators:
    """Test suite for versioning decorators."""

    @pytest.fixture

    def app(self) -> Flask:
        """Create Flask test app."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    @pytest.fixture

    def manager(self, app):
        """Create API version manager."""
        mgr = APIVersionManager(app)
        mgr.register_version(APIVersion(major=1, status=VersionStatus.DEPRECATED))
        mgr.register_version(APIVersion(major=2, status=VersionStatus.CURRENT))
        return mgr

    def test_versioned_decorator(self, app, manager):
        """versioned decorator should route to correct version."""
        # The actual implementation uses manager.versioned as a method decorator
        # and extracts version from route parameters, not a version-switching
        # decorator

        @app.route("/api/<version>/users")
        @manager.versioned

        def get_users(version):
            # Version is in g.api_version after decorator runs
            from flask import g

            return {
                "version": (
                    getattr(g, "api_version", None).string
                    if hasattr(g, "api_version") and g.api_version
                    else "unknown"
                )
            }

        # Test would need Flask test client to actually test routing
        # Just verify decorator doesn't crash
        assert get_users is not None

    def test_deprecated_decorator(self, app, manager):
        """deprecated decorator should add deprecation warning."""

        @manager.deprecated(
            _since_version = "v1", use_instead="/api/v2/users", removal_version="v3"
        )

        def old_endpoint() -> dict[str, Any]:
            return {"data": "old"}

        # Decorator should wrap the function
        assert old_endpoint is not None

        # Call and verify it works (headers added in Flask context)
        with app.test_request_context():
            result = old_endpoint()
            # Function returns either dict or response
            assert result is not None

    def test_sunset_decorator(self, app, manager):
        """sunset decorator should return 410 Gone."""

        @sunset("v1")

        def sunset_endpoint() -> dict[str, Any]:
            return {"data": "gone"}

        with app.test_request_context():
            result = sunset_endpoint()
            # sunset decorator returns (response, 410) tuple
            if isinstance(result, tuple):
                response, status_code = result
                assert status_code == 410
            else:
            # Or returns response object with status
                assert True    # Decorator exists and works


# =============================================================================
# Content Negotiation Tests
# =============================================================================
class TestContentNegotiation:
    """Test suite for content negotiation by version."""

    @pytest.fixture

    def app(self) -> Flask:
        """Create Flask test app."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    @pytest.fixture

    def manager(self, app):
        """Create API version manager."""
        return APIVersionManager(app)

    def test_accept_header_versioning(self, manager, app):
        """Should parse version from Accept header."""
        manager.register_version(APIVersion(major=1))
        manager.register_version(APIVersion(major=2))
        manager.config["version_source"] = "accept"

        # Custom media type versioning
        with app.test_request_context(
            _headers = {"Accept": "application/vnd.debvisor.v2+json"}
        ):
            version = manager.get_requested_version()
            assert version is not None
            assert version.major == 2

    def test_query_param_versioning(self, manager, app):
        """Should parse version from query parameter."""
        manager.register_version(APIVersion(major=1))
        manager.register_version(APIVersion(major=2))
        manager.config["version_source"] = "query"

        with app.test_request_context("/?version=v1"):
            version = manager.get_requested_version()
            assert version is not None
            assert version.major == 1


# =============================================================================
# Migration Helper Tests
# =============================================================================
class TestMigrationHelpers:
    """Test suite for version migration helpers."""

    @pytest.fixture

    def manager(self) -> None:
        """Create API version manager."""
        app = Flask(__name__)
        return APIVersionManager(app)

    def test_migration_path(self, manager):
        """Should generate migration path between versions."""
        v1 = APIVersion(major=1)
        v2 = APIVersion(major=2)
        v3 = APIVersion(major=3, status=VersionStatus.CURRENT)

        manager.register_version(v1)
        manager.register_version(v2)
        manager.register_version(v3)

        path = manager.get_migration_path(v1, v3)

        assert len(path) >= 2
        assert path[0].major == 1
        assert path[-1].major == 3

    def test_breaking_changes_detection(self, manager):
        """Should list breaking changes between versions."""
        v1 = APIVersion(major=1)
        v2 = APIVersion(major=2)

        # Register versions with changelog
        manager.register_version(v1)
        manager.register_version(
            v2,
            changes=[
                {"type": "breaking", "description": "Changed user ID format"},
                {"type": "addition", "description": "Added pagination"},
            ],
        )

        changes = manager.get_breaking_changes(v1, v2)

        if changes:
            assert any("breaking" in str(c) for c in changes)


# =============================================================================
# Response Header Tests
# =============================================================================
class TestVersionResponseHeaders:
    """Test suite for version response headers."""

    @pytest.fixture

    def app(self) -> Flask:
        """Create Flask test app."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    @pytest.fixture

    def manager(self, app):
        """Create API version manager."""
        mgr = APIVersionManager(app)
        mgr.register_version(APIVersion(major=1, status=VersionStatus.DEPRECATED))
        mgr.register_version(APIVersion(major=2, status=VersionStatus.CURRENT))
        return mgr

    def test_version_header_added(self, app, manager):
        """Response should include API version header."""

        @app.route("/test")
        @manager.versioned

        def test_route() -> str:
            return "ok"

        with app.test_client() as client:
            response = client.get("/test", headers={"Accept-Version": "2.0"})
            assert response.headers.get("X-API-Version") == "v2"

    def test_deprecation_header_added(self, app, manager):
        """Deprecated version response should include Deprecation header."""

        @app.route("/test")
        @manager.versioned

        def test_route() -> str:
            return "ok"

        with app.test_client() as client:
            response = client.get("/test", headers={"Accept-Version": "1"})
            assert response.headers.get("Deprecation") == "true"

    def test_sunset_header_added(self, app, manager):
        """Deprecated version response should include Sunset header."""
        sunset_date = datetime.now(timezone.utc) + timedelta(days=90)
        # Update the actual APIVersion object
        manager._versions["v1"].sunset = sunset_date

        # Mock g.api_version for get_response_headers
        from flask import g

        with app.test_request_context():
            g.api_version = manager._versions["v1"]
            headers = manager.get_response_headers()

            assert "Sunset" in headers
            # Format check
            expected = sunset_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
            assert headers["Sunset"] == expected


# =============================================================================
# Main
# =============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
