#!/usr/bin/env python3
"""
Unit tests for OIDC/OAuth2 authentication.

Tests for:
  - JWT token management
  - OIDC provider flows
  - Role-based access control
  - Session management
  - Authentication workflows
"""

import unittest
from datetime import datetime, timedelta, timezone


from oidc_oauth2 import (
    OIDCConfig,
    JWTManager,
    OIDCProvider,
    RBACManager,
    SessionManager,
    AuthenticationManager,
    Role,
    UserInfo,
    TokenType,
)


class TestJWTManager(unittest.TestCase):
    """Tests for JWT token management."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.jwt_manager = JWTManager("test_secret_key")

    def test_create_token(self) -> None:
        """Test token creation."""
        payload = {"sub": "user123", "email": "user@example.com"}
        token = self.jwt_manager.create_token(payload)

        self.assertIsNotNone(token)
        self.assertTrue(isinstance(token, str))

    def test_verify_token(self) -> None:
        """Test token verification."""
        payload = {"sub": "user123", "email": "user@example.com"}
        token = self.jwt_manager.create_token(payload)
        verified = self.jwt_manager.verify_token(token)

        self.assertIsNotNone(verified)
        self.assertEqual(verified["sub"], "user123")

    def test_verify_invalid_token(self) -> None:
        """Test invalid token verification."""
        verified = self.jwt_manager.verify_token("invalid.token.here")

        self.assertIsNone(verified)

    def test_token_expiration(self) -> None:
        """Test token expiration."""
        payload = {"sub": "user123"}
        token = self.jwt_manager.create_token(payload, expires_in_seconds=1)

        # Immediately should be valid
        verified = self.jwt_manager.verify_token(token)
        self.assertIsNotNone(verified)

    def test_refresh_token(self) -> None:
        """Test token refresh."""
        payload = {"sub": "user123", "type": TokenType.REFRESH.value}
        token = self.jwt_manager.create_token(payload, expires_in_seconds=3600)

        new_token = self.jwt_manager.refresh_token(token)

        self.assertIsNotNone(new_token)
        self.assertNotEqual(token, new_token)

    def test_token_type_in_payload(self) -> None:
        """Test token type is included in payload."""
        payload = {"sub": "user123"}
        token = self.jwt_manager.create_token(payload, token_type=TokenType.ACCESS)
        verified = self.jwt_manager.verify_token(token)

        self.assertEqual(verified["type"], TokenType.ACCESS.value)


class TestRBACManager(unittest.TestCase):
    """Tests for role-based access control."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.rbac = RBACManager()

    def test_default_roles_created(self) -> None:
        """Test default roles are created."""
        self.assertIn("admin", self.rbac.roles)
        self.assertIn("operator", self.rbac.roles)
        self.assertIn("viewer", self.rbac.roles)

    def test_create_custom_role(self) -> None:
        """Test creating custom role."""
        role = Role(
            name="developer",
            description="Developer role",
            permissions=["read", "write"],
            resources=["pods", "logs"],
        )
        self.rbac.create_role(role)

        self.assertIn("developer", self.rbac.roles)

    def test_assign_role_to_user(self) -> None:
        """Test assigning role to user."""
        success = self.rbac.assign_role("user1", "admin")

        self.assertTrue(success)
        self.assertIn("admin", self.rbac.user_roles["user1"])

    def test_assign_invalid_role(self) -> None:
        """Test assigning invalid role."""
        success = self.rbac.assign_role("user1", "invalid_role")

        self.assertFalse(success)

    def test_check_permission(self) -> None:
        """Test permission checking."""
        self.rbac.assign_role("user1", "admin")

        has_perm = self.rbac.has_permission("user1", "write", "clusters")

        self.assertTrue(has_perm)

    def test_check_permission_denied(self) -> None:
        """Test permission denied."""
        self.rbac.assign_role("user1", "viewer")

        has_perm = self.rbac.has_permission("user1", "write", "clusters")

        self.assertFalse(has_perm)

    def test_get_user_permissions(self) -> None:
        """Test getting user permissions."""
        self.rbac.assign_role("user1", "operator")

        permissions = self.rbac.get_user_permissions("user1")

        self.assertIn("clusters", permissions)
        self.assertIn("read", permissions["clusters"])

    def test_multiple_roles_per_user(self) -> None:
        """Test user with multiple roles."""
        self.rbac.assign_role("user1", "viewer")
        self.rbac.assign_role("user1", "operator")

        permissions = self.rbac.get_user_permissions("user1")

        self.assertGreater(len(permissions), 0)


class TestSessionManager(unittest.TestCase):
    """Tests for session management."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.session_mgr = SessionManager(session_timeout_seconds=3600)

    def test_create_session(self) -> None:
        """Test session creation."""
        user_info = UserInfo(
            sub="user123",
            email="user@example.com",
            email_verified=True,
            name="Test User",
        )

        session = self.session_mgr.create_session(
            "user123", "access_token_123", user_info=user_info
        )

        self.assertIsNotNone(session)
        self.assertEqual(session.user_id, "user123")

    def test_get_session(self) -> None:
        """Test getting session."""
        session = self.session_mgr.create_session("user123", "token123")
        retrieved = self.session_mgr.get_session(session.session_id)

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.user_id, "user123")

    def test_get_nonexistent_session(self) -> None:
        """Test getting nonexistent session."""
        retrieved = self.session_mgr.get_session("nonexistent")

        self.assertIsNone(retrieved)

    def test_session_expiration(self) -> None:
        """Test session expiration."""
        self.session_mgr.session_timeout_seconds = 1
        session = self.session_mgr.create_session("user123", "token123")
        session.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)

        retrieved = self.session_mgr.get_session(session.session_id)

        self.assertIsNone(retrieved)

    def test_refresh_session(self) -> None:
        """Test refreshing session."""
        session = self.session_mgr.create_session("user123", "token123")
        old_expiry = session.expires_at

        success = self.session_mgr.refresh_session(session.session_id)

        self.assertTrue(success)
        updated = self.session_mgr.get_session(session.session_id)
        self.assertGreater(updated.expires_at, old_expiry)

    def test_destroy_session(self) -> None:
        """Test destroying session."""
        session = self.session_mgr.create_session("user123", "token123")
        self.session_mgr.destroy_session(session.session_id)

        retrieved = self.session_mgr.get_session(session.session_id)

        self.assertIsNone(retrieved)

    def test_get_active_sessions(self) -> None:
        """Test getting active sessions."""
        self.session_mgr.create_session("user123", "token1")
        self.session_mgr.create_session("user123", "token2")
        self.session_mgr.create_session("user456", "token3")

        sessions = self.session_mgr.get_active_sessions("user123")

        self.assertEqual(len(sessions), 2)


class TestOIDCProvider(unittest.TestCase):
    """Tests for OIDC provider."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.config = OIDCConfig(
            provider_name="TestProvider",
            issuer="https://example.com",
            authorization_endpoint="https://example.com/authorize",
            token_endpoint="https://example.com/token",
            userinfo_endpoint="https://example.com/userinfo",
            jwks_uri="https://example.com/.well-known/jwks.json",
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uris=["https://app.example.com/callback"],
        )
        self.provider = OIDCProvider(self.config)

    def test_get_authorization_url(self) -> None:
        """Test authorization URL generation."""
        url = self.provider.get_authorization_url("state123")

        self.assertIn("https://example.com/authorize", url)
        self.assertIn("client_id=test_client_id", url)
        self.assertIn("state=state123", url)

    def test_authorization_url_with_nonce(self) -> None:
        """Test authorization URL with nonce."""
        url = self.provider.get_authorization_url("state123", "nonce456")

        self.assertIn("nonce=nonce456", url)

    def test_exchange_code_for_token(self) -> None:
        """Test code exchange."""
        token_response = self.provider.exchange_code_for_token(
            "auth_code_123", "https://app.example.com/callback"
        )

        self.assertIsNotNone(token_response)
        self.assertIsNotNone(token_response.access_token)
        self.assertIsNotNone(token_response.refresh_token)

    def test_get_user_info(self) -> None:
        """Test getting user information."""
        # Create valid token
        payload = {"sub": "user123", "email": "user@example.com"}
        token = self.provider.jwt_manager.create_token(payload)

        user_info = self.provider.get_user_info(token)

        self.assertIsNotNone(user_info)
        self.assertEqual(user_info.sub, "user123")


class TestAuthenticationManager(unittest.TestCase):
    """Tests for authentication manager."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.config = OIDCConfig(
            provider_name="TestProvider",
            issuer="https://example.com",
            authorization_endpoint="https://example.com/authorize",
            token_endpoint="https://example.com/token",
            userinfo_endpoint="https://example.com/userinfo",
            jwks_uri="https://example.com/.well-known/jwks.json",
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uris=["https://app.example.com/callback"],
        )
        self.auth_mgr = AuthenticationManager(self.config, "jwt_secret")

    def test_generate_authorization_request(self) -> None:
        """Test authorization request generation."""
        url, state = self.auth_mgr.generate_authorization_request()

        self.assertIsNotNone(url)
        self.assertIsNotNone(state)
        self.assertIn("state=", url)

    def test_authenticate_user(self) -> None:
        """Test user authentication."""
        session = self.auth_mgr.authenticate_user("testuser", "password123")

        self.assertIsNotNone(session)
        self.assertEqual(session.user_id, "testuser")

    def test_verify_session(self) -> None:
        """Test session verification."""
        session = self.auth_mgr.authenticate_user("testuser", "password123")
        user_info = self.auth_mgr.verify_session(session.session_id)

        self.assertIsNotNone(user_info)
        self.assertEqual(user_info.sub, "testuser")

    def test_verify_invalid_session(self) -> None:
        """Test invalid session verification."""
        user_info = self.auth_mgr.verify_session("invalid_session")

        self.assertIsNone(user_info)

    def test_rbac_integration(self) -> None:
        """Test RBAC with authentication."""
        _session = self.auth_mgr.authenticate_user("testuser", "password123")
        self.auth_mgr.rbac.assign_role("testuser", "viewer")

        has_perm = self.auth_mgr.rbac.has_permission("testuser", "read", "pods")

        self.assertTrue(has_perm)


class TestOIDCWorkflow(unittest.TestCase):
    """Integration tests for OIDC workflows."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.config = OIDCConfig(
            provider_name="TestProvider",
            issuer="https://example.com",
            authorization_endpoint="https://example.com/authorize",
            token_endpoint="https://example.com/token",
            userinfo_endpoint="https://example.com/userinfo",
            jwks_uri="https://example.com/.well-known/jwks.json",
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uris=["https://app.example.com/callback"],
        )
        self.auth_mgr = AuthenticationManager(self.config, "jwt_secret")

    def test_complete_auth_flow(self) -> None:
        """Test complete authentication flow."""
        # Step 1: Generate authorization request
        url, state = self.auth_mgr.generate_authorization_request()
        self.assertIsNotNone(url)

        # Step 2: Authenticate user
        session = self.auth_mgr.authenticate_user("user1", "password")
        self.assertIsNotNone(session)

        # Step 3: Verify session
        user_info = self.auth_mgr.verify_session(session.session_id)
        self.assertIsNotNone(user_info)

    def test_authorization_with_rbac(self) -> None:
        """Test authorization with role-based access."""
        # Create session
        _session = self.auth_mgr.authenticate_user("operator_user", "password")

        # Assign operator role
        self.auth_mgr.rbac.assign_role("operator_user", "operator")

        # Check permissions
        can_read = self.auth_mgr.rbac.has_permission("operator_user", "read", "pods")
        can_write = self.auth_mgr.rbac.has_permission("operator_user", "write", "pods")
        can_delete = self.auth_mgr.rbac.has_permission(
            "operator_user", "delete", "pods"
        )

        self.assertTrue(can_read)
        self.assertTrue(can_write)
        self.assertFalse(can_delete)


if __name__ == "__main__":
    unittest.main()
