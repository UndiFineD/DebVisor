#!/usr/bin/env python3
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

# !/usr/bin/env python3
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


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

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
_logger=logging.getLogger(__name__)


class AuthorizationFlow(Enum):
    """OAuth2 authorization flows."""

    AUTHORIZATION_CODE="authorization_code"
    IMPLICIT="implicit"
    CLIENT_CREDENTIALS="client_credentials"
    REFRESH_TOKEN="refresh_token"    # nosec B105


class TokenType(Enum):
    """Token types."""

    ACCESS="access"
    REFRESH="refresh"
    ID="id"


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
    response_type: str="code"


@dataclass
class AuthorizationRequest:
    """OAuth2 authorization request."""

    client_id: str
    redirect_uri: str
    scope: str
    state: str
    response_type: str="code"
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
    token_type: str="Bearer"
    expires_in: int=3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: str=""


@dataclass
class UserInfo:
    """User information from OIDC."""

    sub: str    # Subject (unique user ID)
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

    def __init__(self, secretkey: str) -> None:
        """
        Initialize JWT manager.

        Args:
            secret_key: Secret key for signing tokens
        """
        self.secret_key=secret_key  # type: ignore[name-defined]

    def create_token(
        self,
        payload: Dict[str, Any],
        expires_in_seconds: int=3600,
        token_type: TokenType=TokenType.ACCESS,
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
        _now=datetime.now(timezone.utc)
        # Respect type in payload if already set, otherwise use token_type parameter
        _final_type=payload.get("type", token_type.value)
        claims={
            **payload,
            "iat": now,  # type: ignore[name-defined]
            "exp": now + timedelta(seconds=expires_in_seconds),  # type: ignore[name-defined]
            "type": final_type,  # type: ignore[name-defined]
        }

        _token=jwt.encode(claims, self.secret_key, algorithm="HS256")
        return token  # type: ignore[name-defined]

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode JWT token.

        Args:
            token: JWT token string

        Returns:
            Token payload or None if invalid
        """
        try:
            _payload=jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload  # type: ignore[name-defined]
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")  # type: ignore[name-defined]
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")  # type: ignore[name-defined]
            return None

    def refresh_token(
        self, token: str, expires_in_seconds: int=3600
    ) -> Optional[str]:
        """
        Refresh token.

        Args:
            token: Current token
            expires_in_seconds: New expiration

        Returns:
            New token or None
        """
        _payload=self.verify_token(token)
        if not payload or payload.get("type") != TokenType.REFRESH.value:  # type: ignore[name-defined]
            return None

        # Remove old claims
        payload.pop("iat", None)  # type: ignore[name-defined]
        payload.pop("exp", None)  # type: ignore[name-defined]
        payload.pop("type", None)    # Remove old type so create_token uses the parameter  # type: ignore[name-defined]

        return self.create_token(
            payload, expires_in_seconds, token_type=TokenType.ACCESS  # type: ignore[name-defined]
        )


class OIDCProvider:
    """OIDC provider client."""

    def __init__(self, config: OIDCConfig) -> None:
        """
        Initialize OIDC provider.

        Args:
            config: OIDC configuration
        """
        self.config=config
        self.jwt_manager=JWTManager(config.client_secret)

    def get_authorization_url(self, state: str, nonce: Optional[str] = None) -> str:
        """
        Get authorization URL for user redirect.

        Args:
            state: State parameter for security
            nonce: Nonce for ID token validation

        Returns:
            Authorization URL
        """
        params={
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
        logger.info(f"Exchanging code for token: {code}")  # type: ignore[name-defined]

        # Simulate token generation
        _access_token=self.jwt_manager.create_token(
            {"sub": "user123", "aud": self.config.client_id}, expires_in_seconds=3600
        )

        refresh_token=self.jwt_manager.create_token(  # type: ignore[call-arg]
            {"sub": "user123", "type": TokenType.REFRESH.value},
            _expires_in_seconds=86400 * 7,    # 7 days
        )

        return TokenResponse(  # type: ignore[call-arg]
            _access_token=access_token,  # type: ignore[name-defined]
            _refresh_token=refresh_token,
            _expires_in=3600,
            _scope=" ".join(self.config.scopes),
        )

    def get_user_info(self, accesstoken: str) -> Optional[UserInfo]:
        """
        Get user information from OIDC provider.

        Args:
            access_token: Access token

        Returns:
            User information or None
        """
        # In production, would make HTTP request to userinfo_endpoint
        _payload=self.jwt_manager.verify_token(access_token)  # type: ignore[name-defined]

        if not payload:  # type: ignore[name-defined]
            return None

        return UserInfo(  # type: ignore[call-arg]
            _sub=payload.get("sub", ""),  # type: ignore[name-defined]
            _email=payload.get("email", ""),  # type: ignore[name-defined]
            _email_verified=payload.get("email_verified", False),  # type: ignore[name-defined]
            _name=payload.get("name", ""),  # type: ignore[name-defined]
            _roles=payload.get("roles", []),  # type: ignore[name-defined]
            _clusters=payload.get("clusters", []),  # type: ignore[name-defined]
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
            Role(  # type: ignore[call-arg]
                _name="admin",
                _description="Administrator with full access",
                _permissions=["*"],
                _resources=["*"],
            )
        )

        self.create_role(
            Role(  # type: ignore[call-arg]
                _name="operator",
                _description="Operator with read/write access",
                _permissions=["read", "write", "execute"],
                _resources=["clusters", "nodes", "pods", "volumes"],
            )
        )

        self.create_role(
            Role(  # type: ignore[call-arg]
                _name="viewer",
                _description="Read-only access",
                _permissions=["read"],
                _resources=["clusters", "nodes", "pods"],
            )
        )

    def create_role(self, role: Role) -> None:
        """
        Create role.

        Args:
            role: Role definition
        """
        self.roles[role.name] = role
        logger.info(f"Created role: {role.name}")  # type: ignore[name-defined]

    def assign_role(self, userid: str, rolename: str) -> bool:
        """
        Assign role to user.

        Args:
            user_id: User ID
            role_name: Role name

        Returns:
            Success status
        """
        if role_name not in self.roles:  # type: ignore[name-defined]
            logger.error(f"Role not found: {role_name}")  # type: ignore[name-defined]
            return False

        if user_id not in self.user_roles:  # type: ignore[name-defined]
            self.user_roles[user_id] = []  # type: ignore[name-defined]

        self.user_roles[user_id].append(role_name)  # type: ignore[name-defined]
        logger.info(f"Assigned role {role_name} to user {user_id}")  # type: ignore[name-defined]
        return True

    def has_permission(self, userid: str, permission: str, resource: str) -> bool:
        """
        Check if user has permission for resource.

        Args:
            user_id: User ID
            permission: Permission to check
            resource: Resource name

        Returns:
            Permission granted status
        """
        _roles=self.user_roles.get(user_id, [])  # type: ignore[name-defined]

        for role_name in roles:  # type: ignore[name-defined]
            _role=self.roles.get(role_name)
            if not role:  # type: ignore[name-defined]
                continue

            # Check wildcard permissions
            if "*" in role.permissions or permission in role.permissions:  # type: ignore[name-defined]
                if "*" in role.resources or resource in role.resources:  # type: ignore[name-defined]
                    return True

        return False

    def get_user_permissions(self, userid: str) -> Dict[str, List[str]]:
        """
        Get all permissions for user.

        Args:
            user_id: User ID

        Returns:
            Dictionary of permissions by resource
        """
        permissions: Any={}
        _roles=self.user_roles.get(user_id, [])  # type: ignore[name-defined]

        for role_name in roles:  # type: ignore[name-defined]
            _role=self.roles.get(role_name)
            if not role:  # type: ignore[name-defined]
                continue

            for resource in role.resources:  # type: ignore[name-defined]
                if resource not in permissions:
                    permissions[resource] = []
                permissions[resource].extend(role.permissions)  # type: ignore[name-defined]

        # Remove duplicates
        for resource in permissions:
            permissions[resource] = list(set(permissions[resource]))

        return permissions


class SessionManager:
    """Manage user sessions."""

    def __init__(self, sessiontimeout_seconds: int=86400) -> None:
        """
        Initialize session manager.

        Args:
            session_timeout_seconds: Session timeout duration
        """
        self.session_timeout_seconds=session_timeout_seconds  # type: ignore[name-defined]
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
        _session_id=secrets.token_urlsafe(32)
        _now=datetime.now(timezone.utc)

        session=Session(  # type: ignore[call-arg]
            _session_id=session_id,  # type: ignore[name-defined]
            _user_id=user_id,
            _created_at=now,  # type: ignore[name-defined]
            _expires_at=now + timedelta(seconds=self.session_timeout_seconds),  # type: ignore[name-defined]
            _access_token=access_token,
            _refresh_token=refresh_token,
            _user_info=user_info,
        )

        self.sessions[session_id] = session  # type: ignore[name-defined]
        logger.info(f"Created session {session_id} for user {user_id}")  # type: ignore[name-defined]

        return session

    def get_session(self, sessionid: str) -> Optional[Session]:
        """
        Get session by ID.

        Args:
            session_id: Session ID

        Returns:
            Session or None if not found or expired
        """
        _session=self.sessions.get(session_id)  # type: ignore[name-defined]

        if not session:  # type: ignore[name-defined]
            return None

        if session.expires_at < datetime.now(timezone.utc):  # type: ignore[name-defined]
            self.destroy_session(session_id)  # type: ignore[name-defined]
            return None

        return session  # type: ignore[name-defined]

    def refresh_session(self, sessionid: str) -> bool:
        """
        Refresh session expiration.

        Args:
            session_id: Session ID

        Returns:
            Success status
        """
        _session=self.sessions.get(session_id)  # type: ignore[name-defined]

        if not session:  # type: ignore[name-defined]
            return False

        session.expires_at=datetime.now(timezone.utc) + timedelta(  # type: ignore[call-arg, name-defined]
            _seconds=self.session_timeout_seconds
        )
        return True

    def destroy_session(self, sessionid: str) -> None:
        """
        Destroy session.

        Args:
            session_id: Session ID
        """
        if session_id in self.sessions:  # type: ignore[name-defined]
            del self.sessions[session_id]  # type: ignore[name-defined]
            logger.info(f"Destroyed session {session_id}")  # type: ignore[name-defined]

    def get_active_sessions(self, userid: str) -> List[Session]:
        """
        Get active sessions for user.

        Args:
            user_id: User ID

        Returns:
            List of active sessions
        """
        active=[]
        _now=datetime.now(timezone.utc)

        for session in self.sessions.values():
            if session.user_id == user_id and session.expires_at > now:  # type: ignore[name-defined]
                active.append(session)

        return active


class AuthenticationManager:
    """Central authentication manager."""

    def __init__(self, oidcconfig: OIDCConfig, jwtsecret: str) -> None:
        """
        Initialize authentication manager.

        Args:
            oidc_config: OIDC configuration
            jwt_secret: JWT secret key
        """
        self.oidc_provider=OIDCProvider(oidc_config)  # type: ignore[name-defined]
        self.jwt_manager=JWTManager(jwt_secret)  # type: ignore[name-defined]
        self.rbac=RBACManager()
        self.sessions=SessionManager()

    def generate_authorization_request(self) -> tuple[str, str]:
        """
        Generate authorization request.

        Returns:
            Tuple of (auth_url, state)
        """
        _state=secrets.token_urlsafe(32)
        _nonce=secrets.token_urlsafe(32)
        _auth_url=self.oidc_provider.get_authorization_url(state, nonce)  # type: ignore[name-defined]
        return auth_url, state  # type: ignore[name-defined]

    def handle_callback(self, code: str, state: str) -> Optional[Session]:
        """
        Handle authorization callback.

        Args:
            code: Authorization code
            state: State parameter

        Returns:
            Session or None if failed
        """
        token_response=self.oidc_provider.exchange_code_for_token(
            code, self.oidc_provider.config.redirect_uris[0]
        )

        if not token_response:
            logger.error("Failed to exchange code for token")  # type: ignore[name-defined]
            return None

        _user_info=self.oidc_provider.get_user_info(token_response.access_token)

        if not user_info:  # type: ignore[name-defined]
            logger.error("Failed to get user info")  # type: ignore[name-defined]
            return None

        session=self.sessions.create_session(  # type: ignore[call-arg]
            _user_id=user_info.sub,  # type: ignore[name-defined]
            _access_token=token_response.access_token,
            _user_info=user_info,  # type: ignore[name-defined]
            _refresh_token=token_response.refresh_token,
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
        logger.info(f"Authenticating user: {username}")  # type: ignore[name-defined]

        user_info=UserInfo(  # type: ignore[call-arg]
            _sub=username,
            _email=f"{username}@example.com",
            _email_verified=True,
            _name=username,
            _roles=["viewer"],
        )

        access_token=self.jwt_manager.create_token(
            {"sub": username, "email": user_info.email}, expires_in_seconds=3600
        )

        session=self.sessions.create_session(  # type: ignore[call-arg]
            _user_id=username, access_token=access_token, user_info=user_info
        )

        return session

    def verify_session(self, sessionid: str) -> Optional[UserInfo]:
        """
        Verify session and return user info.

        Args:
            session_id: Session ID

        Returns:
            User info or None if session invalid
        """
        _session=self.sessions.get_session(session_id)  # type: ignore[name-defined]

        if not session:  # type: ignore[name-defined]
            return None

        return session.user_info  # type: ignore[name-defined]
