#!/usr/bin/env python3
"""
OIDC/OAuth2 Authentication Support for DebVisor.

Provides industry-standard authentication with OpenID Connect and OAuth2.

Features:
  - OIDC provider integration
  - OAuth2 authorization flows
  - JWT token management
  - Role-based access control (RBAC)
  - Session management
"""

import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import jwt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthorizationFlow(Enum):
    """OAuth2 authorization flows."""

    AUTHORIZATION_CODE = "authorization_code"
    IMPLICIT = "implicit"
    CLIENT_CREDENTIALS = "client_credentials"
    REFRESH_TOKEN = "refresh_token"  # nosec B105


class TokenType(Enum):
    """Token types."""

    ACCESS = "access"
    REFRESH = "refresh"
    ID = "id"


@dataclass
class OIDCConfig:
    """OIDC provider configuration."""

    provider_name: str
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    jwks_uri: str
    client_id: str
    client_secret: str
    redirect_uris: List[str]
    scopes: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    response_type: str = "code"


@dataclass
class AuthorizationRequest:
    """OAuth2 authorization request."""

    client_id: str
    redirect_uri: str
    scope: str
    state: str
    response_type: str = "code"
    nonce: Optional[str] = None
    prompt: Optional[str] = None
    max_age: Optional[int] = None


@dataclass
class TokenRequest:
    """OAuth2 token request."""

    grant_type: str
    code: Optional[str] = None
    refresh_token: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class TokenResponse:
    """OAuth2 token response."""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: str = ""


@dataclass
class UserInfo:
    """User information from OIDC."""

    sub: str  # Subject (unique user ID)
    email: str
    email_verified: bool
    name: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    clusters: List[str] = field(default_factory=list)


@dataclass
class Role:
    """RBAC role definition."""

    name: str
    description: str
    permissions: List[str]
    resources: List[str] = field(default_factory=list)


@dataclass
class Session:
    """User session."""

    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    access_token: str
    refresh_token: Optional[str] = None
    user_info: Optional[UserInfo] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class JWTManager:
    """JWT token generation and validation."""

    def __init__(self, secret_key: str):
        """
        Initialize JWT manager.

        Args:
            secret_key: Secret key for signing tokens
        """
        self.secret_key = secret_key

    def create_token(
        self,
        payload: Dict[str, Any],
        expires_in_seconds: int = 3600,
        token_type: TokenType = TokenType.ACCESS,
    ) -> str:
        """
        Create JWT token.

        Args:
            payload: Token payload
            expires_in_seconds: Token expiration
            token_type: Token type

        Returns:
            JWT token string
        """
        now = datetime.now(timezone.utc)
        # Respect type in payload if already set, otherwise use token_type parameter
        final_type = payload.get("type", token_type.value)
        claims = {
            **payload,
            "iat": now,
            "exp": now + timedelta(seconds=expires_in_seconds),
            "type": final_type,
        }

        token = jwt.encode(claims, self.secret_key, algorithm="HS256")
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode JWT token.

        Args:
            token: JWT token string

        Returns:
            Token payload or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None

    def refresh_token(
        self, token: str, expires_in_seconds: int = 3600
    ) -> Optional[str]:
        """
        Refresh token.

        Args:
            token: Current token
            expires_in_seconds: New expiration

        Returns:
            New token or None
        """
        payload = self.verify_token(token)
        if not payload or payload.get("type") != TokenType.REFRESH.value:
            return None

        # Remove old claims
        payload.pop("iat", None)
        payload.pop("exp", None)
        payload.pop("type", None)  # Remove old type so create_token uses the parameter

        return self.create_token(
            payload, expires_in_seconds, token_type=TokenType.ACCESS
        )


class OIDCProvider:
    """OIDC provider client."""

    def __init__(self, config: OIDCConfig):
        """
        Initialize OIDC provider.

        Args:
            config: OIDC configuration
        """
        self.config = config
        self.jwt_manager = JWTManager(config.client_secret)

    def get_authorization_url(self, state: str, nonce: Optional[str] = None) -> str:
        """
        Get authorization URL for user redirect.

        Args:
            state: State parameter for security
            nonce: Nonce for ID token validation

        Returns:
            Authorization URL
        """
        params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uris[0],
            "response_type": self.config.response_type,
            "scope": " ".join(self.config.scopes),
            "state": state,
        }

        if nonce:
            params["nonce"] = nonce

        return f"{self.config.authorization_endpoint}?{urlencode(params)}"

    def exchange_code_for_token(
        self, code: str, redirect_uri: str
    ) -> Optional[TokenResponse]:
        """
        Exchange authorization code for tokens.

        Args:
            code: Authorization code
            redirect_uri: Redirect URI

        Returns:
            Token response or None
        """
        # In production, would make HTTP request to token_endpoint
        logger.info(f"Exchanging code for token: {code}")

        # Simulate token generation
        access_token = self.jwt_manager.create_token(
            {"sub": "user123", "aud": self.config.client_id}, expires_in_seconds=3600
        )

        refresh_token = self.jwt_manager.create_token(
            {"sub": "user123", "type": TokenType.REFRESH.value},
            expires_in_seconds=86400 * 7,  # 7 days
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=3600,
            scope=" ".join(self.config.scopes),
        )

    def get_user_info(self, access_token: str) -> Optional[UserInfo]:
        """
        Get user information from OIDC provider.

        Args:
            access_token: Access token

        Returns:
            User information or None
        """
        # In production, would make HTTP request to userinfo_endpoint
        payload = self.jwt_manager.verify_token(access_token)

        if not payload:
            return None

        return UserInfo(
            sub=payload.get("sub", ""),
            email=payload.get("email", ""),
            email_verified=payload.get("email_verified", False),
            name=payload.get("name", ""),
            roles=payload.get("roles", []),
            clusters=payload.get("clusters", []),
        )


class RBACManager:
    """Role-Based Access Control manager."""

    def __init__(self) -> None:
        """Initialize RBAC manager."""
        self.roles: Dict[str, Role] = {}
        self.user_roles: Dict[str, List[str]] = {}
        self._setup_default_roles()

    def _setup_default_roles(self) -> None:
        """Set up default roles."""
        self.create_role(
            Role(
                name="admin",
                description="Administrator with full access",
                permissions=["*"],
                resources=["*"],
            )
        )

        self.create_role(
            Role(
                name="operator",
                description="Operator with read/write access",
                permissions=["read", "write", "execute"],
                resources=["clusters", "nodes", "pods", "volumes"],
            )
        )

        self.create_role(
            Role(
                name="viewer",
                description="Read-only access",
                permissions=["read"],
                resources=["clusters", "nodes", "pods"],
            )
        )

    def create_role(self, role: Role) -> None:
        """
        Create role.

        Args:
            role: Role definition
        """
        self.roles[role.name] = role
        logger.info(f"Created role: {role.name}")

    def assign_role(self, user_id: str, role_name: str) -> bool:
        """
        Assign role to user.

        Args:
            user_id: User ID
            role_name: Role name

        Returns:
            Success status
        """
        if role_name not in self.roles:
            logger.error(f"Role not found: {role_name}")
            return False

        if user_id not in self.user_roles:
            self.user_roles[user_id] = []

        self.user_roles[user_id].append(role_name)
        logger.info(f"Assigned role {role_name} to user {user_id}")
        return True

    def has_permission(self, user_id: str, permission: str, resource: str) -> bool:
        """
        Check if user has permission for resource.

        Args:
            user_id: User ID
            permission: Permission to check
            resource: Resource name

        Returns:
            Permission granted status
        """
        roles = self.user_roles.get(user_id, [])

        for role_name in roles:
            role = self.roles.get(role_name)
            if not role:
                continue

            # Check wildcard permissions
            if "*" in role.permissions or permission in role.permissions:
                if "*" in role.resources or resource in role.resources:
                    return True

        return False

    def get_user_permissions(self, user_id: str) -> Dict[str, List[str]]:
        """
        Get all permissions for user.

        Args:
            user_id: User ID

        Returns:
            Dictionary of permissions by resource
        """
        permissions: Any = {}
        roles = self.user_roles.get(user_id, [])

        for role_name in roles:
            role = self.roles.get(role_name)
            if not role:
                continue

            for resource in role.resources:
                if resource not in permissions:
                    permissions[resource] = []
                permissions[resource].extend(role.permissions)

        # Remove duplicates
        for resource in permissions:
            permissions[resource] = list(set(permissions[resource]))

        return permissions


class SessionManager:
    """Manage user sessions."""

    def __init__(self, session_timeout_seconds: int = 86400):
        """
        Initialize session manager.

        Args:
            session_timeout_seconds: Session timeout duration
        """
        self.session_timeout_seconds = session_timeout_seconds
        self.sessions: Dict[str, Session] = {}

    def create_session(
        self,
        user_id: str,
        access_token: str,
        user_info: Optional[UserInfo] = None,
        refresh_token: Optional[str] = None,
    ) -> Session:
        """
        Create user session.

        Args:
            user_id: User ID
            access_token: Access token
            user_info: User information
            refresh_token: Refresh token

        Returns:
            Created session
        """
        session_id = secrets.token_urlsafe(32)
        now = datetime.now(timezone.utc)

        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            expires_at=now + timedelta(seconds=self.session_timeout_seconds),
            access_token=access_token,
            refresh_token=refresh_token,
            user_info=user_info,
        )

        self.sessions[session_id] = session
        logger.info(f"Created session {session_id} for user {user_id}")

        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Get session by ID.

        Args:
            session_id: Session ID

        Returns:
            Session or None if not found or expired
        """
        session = self.sessions.get(session_id)

        if not session:
            return None

        if session.expires_at < datetime.now(timezone.utc):
            self.destroy_session(session_id)
            return None

        return session

    def refresh_session(self, session_id: str) -> bool:
        """
        Refresh session expiration.

        Args:
            session_id: Session ID

        Returns:
            Success status
        """
        session = self.sessions.get(session_id)

        if not session:
            return False

        session.expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=self.session_timeout_seconds
        )
        return True

    def destroy_session(self, session_id: str) -> None:
        """
        Destroy session.

        Args:
            session_id: Session ID
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Destroyed session {session_id}")

    def get_active_sessions(self, user_id: str) -> List[Session]:
        """
        Get active sessions for user.

        Args:
            user_id: User ID

        Returns:
            List of active sessions
        """
        active = []
        now = datetime.now(timezone.utc)

        for session in self.sessions.values():
            if session.user_id == user_id and session.expires_at > now:
                active.append(session)

        return active


class AuthenticationManager:
    """Central authentication manager."""

    def __init__(self, oidc_config: OIDCConfig, jwt_secret: str):
        """
        Initialize authentication manager.

        Args:
            oidc_config: OIDC configuration
            jwt_secret: JWT secret key
        """
        self.oidc_provider = OIDCProvider(oidc_config)
        self.jwt_manager = JWTManager(jwt_secret)
        self.rbac = RBACManager()
        self.sessions = SessionManager()

    def generate_authorization_request(self) -> tuple[str, str]:
        """
        Generate authorization request.

        Returns:
            Tuple of (auth_url, state)
        """
        state = secrets.token_urlsafe(32)
        nonce = secrets.token_urlsafe(32)
        auth_url = self.oidc_provider.get_authorization_url(state, nonce)
        return auth_url, state

    def handle_callback(self, code: str, state: str) -> Optional[Session]:
        """
        Handle authorization callback.

        Args:
            code: Authorization code
            state: State parameter

        Returns:
            Session or None if failed
        """
        token_response = self.oidc_provider.exchange_code_for_token(
            code, self.oidc_provider.config.redirect_uris[0]
        )

        if not token_response:
            logger.error("Failed to exchange code for token")
            return None

        user_info = self.oidc_provider.get_user_info(token_response.access_token)

        if not user_info:
            logger.error("Failed to get user info")
            return None

        session = self.sessions.create_session(
            user_id=user_info.sub,
            access_token=token_response.access_token,
            user_info=user_info,
            refresh_token=token_response.refresh_token,
        )

        return session

    def authenticate_user(self, username: str, password: str) -> Optional[Session]:
        """
        Authenticate user with credentials.

        Args:
            username: Username
            password: Password

        Returns:
            Session or None if authentication failed
        """
        # In production, would validate against directory service
        logger.info(f"Authenticating user: {username}")

        user_info = UserInfo(
            sub=username,
            email=f"{username}@example.com",
            email_verified=True,
            name=username,
            roles=["viewer"],
        )

        access_token = self.jwt_manager.create_token(
            {"sub": username, "email": user_info.email}, expires_in_seconds=3600
        )

        session = self.sessions.create_session(
            user_id=username, access_token=access_token, user_info=user_info
        )

        return session

    def verify_session(self, session_id: str) -> Optional[UserInfo]:
        """
        Verify session and return user info.

        Args:
            session_id: Session ID

        Returns:
            User info or None if session invalid
        """
        session = self.sessions.get_session(session_id)

        if not session:
            return None

        return session.user_info
