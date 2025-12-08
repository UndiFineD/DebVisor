"""
RPC Service Enhanced Authentication, Authorization, and Security Module
=========================================================================

Provides comprehensive security enhancements for the gRPC RPC service including:
- OAuth2/OIDC authentication
- RBAC authorization
- TLS certificate management
- Request/response validation
- Audit logging
"""

import json
import logging
import secrets
import ssl
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from functools import wraps
import jwt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
audit_logger = logging.getLogger('rpc_audit')


###############################################################################
# Enumerations & Constants
###############################################################################

class RoleType(Enum):
    """Supported role types for RBAC"""
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"
    SERVICE = "service"


class ResourceType(Enum):
    """Supported resource types"""
    CLUSTER = "cluster"
    NODE = "node"
    POD = "pod"
    VOLUME = "volume"
    CONFIG = "config"
    SYSTEM = "system"


class Action(Enum):
    """Supported actions"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"


class TLSVersion(Enum):
    """Supported TLS versions"""
    TLS_1_2 = ssl.TLSVersion.TLSv1_2
    TLS_1_3 = ssl.TLSVersion.TLSv1_3


###############################################################################
# Data Classes
###############################################################################

@dataclass
class AuthToken:
    """Authentication token data"""
    token_id: str
    user_id: str
    username: str
    roles: List[str]
    issued_at: datetime
    expires_at: datetime
    scopes: List[str]
    metadata: Dict[str, Any]

    def is_expired(self) -> bool:
        """Check if token is expired"""
        return datetime.now(timezone.utc) > self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'token_id': self.token_id,
            'user_id': self.user_id,
            'username': self.username,
            'roles': self.roles,
            'issued_at': self.issued_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'scopes': self.scopes,
            'metadata': self.metadata
        }


@dataclass
class PermissionRequest:
    """Permission check request"""
    user_id: str
    resource_type: str
    resource_id: str
    action: str
    context: Dict[str, Any]


@dataclass
class AuditLogEntry:
    """Audit log entry"""
    timestamp: datetime
    user_id: str
    username: str
    action: str
    resource_type: str
    resource_id: str
    status: str
    status_code: int
    request_metadata: Dict[str, Any]
    response_metadata: Dict[str, Any]
    duration_ms: float
    ip_address: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id,
            'username': self.username,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'status': self.status,
            'status_code': self.status_code,
            'duration_ms': self.duration_ms,
            'ip_address': self.ip_address,
            'error_message': self.error_message
        }


@dataclass
class AuthenticationConfig:
    """Authentication configuration"""
    enabled: bool = True
    algorithm: str = "HS256"
    secret_key: Optional[str] = None
    public_key: Optional[str] = None
    token_expiry_seconds: int = 3600
    refresh_token_expiry_seconds: int = 86400
    issuer: str = "debvisor"
    audience: str = "debvisor-api"


@dataclass
class AuthorizationConfig:
    """Authorization configuration"""
    enabled: bool = True
    default_role: RoleType = RoleType.VIEWER
    role_bindings: Dict[str, List[Tuple[str, str]]] = None  # user -> [(resource, action)]

    def __post_init__(self):
        if self.role_bindings is None:
            self.role_bindings = {}


###############################################################################
# Authentication Service
###############################################################################

class AuthenticationService:
    """Handles authentication and token management"""

    def __init__(self, config: AuthenticationConfig):
        """Initialize authentication service"""
        self.config = config
        self.token_cache: Dict[str, AuthToken] = {}
        logger.info("AuthenticationService initialized")

    def create_token(
        self,
        user_id: str,
        username: str,
        roles: List[str],
        scopes: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new authentication token"""
        if not self.config.enabled:
            raise ValueError("Authentication is disabled")

        if not self.config.secret_key:
            raise ValueError("Secret key not configured")

        token_id = self._generate_token_id()
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(seconds=self.config.token_expiry_seconds)

        payload = {
            'token_id': token_id,
            'user_id': user_id,
            'username': username,
            'roles': roles,
            'scopes': scopes,
            'iat': now.timestamp(),
            'exp': expires_at.timestamp(),
            'iss': self.config.issuer,
            'aud': self.config.audience
        }

        # Add metadata if provided
        if metadata:
            payload['metadata'] = metadata

        # Create JWT token
        token = jwt.encode(
            payload,
            self.config.secret_key,
            algorithm=self.config.algorithm
        )

        # Cache token
        auth_token = AuthToken(
            token_id=token_id,
            user_id=user_id,
            username=username,
            roles=roles,
            issued_at=now,
            expires_at=expires_at,
            scopes=scopes,
            metadata=metadata or {}
        )
        self.token_cache[token_id] = auth_token

        logger.info(f"Token created for user: {username} (ID: {user_id})")
        return token

    def validate_token(self, token: str) -> Tuple[bool, Optional[AuthToken], Optional[str]]:
        """Validate and decode authentication token"""
        if not self.config.enabled:
            return True, None, None

        if not self.config.secret_key:
            return False, None, "Secret key not configured"

        try:
            payload = jwt.decode(
                token,
                self.config.secret_key,
                algorithms=[self.config.algorithm],
                audience=self.config.audience,
                issuer=self.config.issuer
            )

            # Check if token is in cache and not expired
            token_id = payload.get('token_id')
            if token_id in self.token_cache:
                cached_token = self.token_cache[token_id]
                if cached_token.is_expired():
                    del self.token_cache[token_id]
                    return False, None, "Token expired"
                return True, cached_token, None

            # Reconstruct token from payload
            auth_token = AuthToken(
                token_id=token_id,
                user_id=payload['user_id'],
                username=payload['username'],
                roles=payload['roles'],
                issued_at=datetime.fromtimestamp(payload['iat']),
                expires_at=datetime.fromtimestamp(payload['exp']),
                scopes=payload.get('scopes', []),
                metadata=payload.get('metadata', {})
            )

            if auth_token.is_expired():
                return False, None, "Token expired"

            return True, auth_token, None

        except jwt.ExpiredSignatureError:
            return False, None, "Token expired"
        except jwt.InvalidTokenError as e:
            return False, None, f"Invalid token: {str(e)}"

    def revoke_token(self, token_id: str) -> bool:
        """Revoke a token"""
        if token_id in self.token_cache:
            del self.token_cache[token_id]
            logger.info(f"Token revoked: {token_id}")
            return True
        return False

    @staticmethod
    def _generate_token_id() -> str:
        """Generate unique token ID"""
        return secrets.token_urlsafe(32)

    def refresh_token(self, token: str) -> Optional[str]:
        """Refresh an existing token"""
        is_valid, auth_token, error = self.validate_token(token)
        if not is_valid or not auth_token:
            logger.warning(f"Token refresh failed: {error}")
            return None

        # Create new token with same claims
        new_token = self.create_token(
            user_id=auth_token.user_id,
            username=auth_token.username,
            roles=auth_token.roles,
            scopes=auth_token.scopes,
            metadata=auth_token.metadata
        )

        # Revoke old token
        self.revoke_token(auth_token.token_id)

        logger.info(f"Token refreshed for user: {auth_token.username}")
        return new_token


###############################################################################
# Authorization Service (RBAC)
###############################################################################

class AuthorizationService:
    """Handles role-based access control (RBAC)"""

    def __init__(self, config: AuthorizationConfig):
        """Initialize authorization service"""
        self.config = config
        self._initialize_default_permissions()
        logger.info("AuthorizationService initialized")

    def _initialize_default_permissions(self):
        """Initialize default role permissions"""
        self.permissions = {
            RoleType.ADMIN.value: [
                (ResourceType.CLUSTER.value, Action.ADMIN.value),
                (ResourceType.NODE.value, Action.ADMIN.value),
                (ResourceType.POD.value, Action.ADMIN.value),
                (ResourceType.VOLUME.value, Action.ADMIN.value),
                (ResourceType.CONFIG.value, Action.ADMIN.value),
                (ResourceType.SYSTEM.value, Action.ADMIN.value),
            ],
            RoleType.OPERATOR.value: [
                (ResourceType.CLUSTER.value, Action.READ.value),
                (ResourceType.CLUSTER.value, Action.WRITE.value),
                (ResourceType.NODE.value, Action.READ.value),
                (ResourceType.NODE.value, Action.WRITE.value),
                (ResourceType.POD.value, Action.READ.value),
                (ResourceType.POD.value, Action.WRITE.value),
                (ResourceType.VOLUME.value, Action.READ.value),
                (ResourceType.VOLUME.value, Action.WRITE.value),
            ],
            RoleType.VIEWER.value: [
                (ResourceType.CLUSTER.value, Action.READ.value),
                (ResourceType.NODE.value, Action.READ.value),
                (ResourceType.POD.value, Action.READ.value),
                (ResourceType.VOLUME.value, Action.READ.value),
            ],
            RoleType.SERVICE.value: [
                (ResourceType.SYSTEM.value, Action.READ.value),
            ],
        }

    def check_permission(
        self,
        user_roles: List[str],
        resource_type: str,
        action: str
    ) -> Tuple[bool, Optional[str]]:
        """Check if user with given roles has permission"""
        if not self.config.enabled:
            return True, None

        for role in user_roles:
            role_perms = self.permissions.get(role, [])
            if (resource_type, action) in role_perms or (
                    resource_type, Action.ADMIN.value) in role_perms:
                return True, None

        error_msg = f"User role(s) {user_roles} not authorized for {action} on {resource_type}"
        return False, error_msg

    def add_custom_permission(self, role: str, resource: str, action: str):
        """Add custom permission"""
        if role not in self.permissions:
            self.permissions[role] = []
        self.permissions[role].append((resource, action))
        logger.info(f"Permission added: {role} -> {resource}:{action}")

    def remove_permission(self, role: str, resource: str, action: str):
        """Remove permission"""
        if role in self.permissions:
            self.permissions[role] = [
                (r, a) for r, a in self.permissions[role]
                if not (r == resource and a == action)
            ]
            logger.info(f"Permission removed: {role} -> {resource}:{action}")


###############################################################################
# TLS Certificate Management
###############################################################################

class TLSManager:
    """Manages TLS certificates and SSL context"""

    def __init__(
        self,
        cert_file: Optional[str] = None,
        key_file: Optional[str] = None,
        ca_file: Optional[str] = None,
        min_version: TLSVersion = TLSVersion.TLS_1_2
    ):
        """Initialize TLS manager"""
        self.cert_file = cert_file
        self.key_file = key_file
        self.ca_file = ca_file
        self.min_version = min_version
        logger.info(f"TLSManager initialized (min_version: {min_version.name})")

    def create_server_context(self) -> ssl.SSLContext:
        """Create SSL context for server"""
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = self.min_version.value

        # Load certificates
        if self.cert_file and self.key_file:
            context.load_cert_chain(self.cert_file, self.key_file)
        elif self.cert_file:
            context.load_cert_chain(self.cert_file)
        else:
            raise ValueError("Certificate file required for server context")

        # Load CA certificate for client verification
        if self.ca_file:
            context.load_verify_locations(self.ca_file)
            context.verify_mode = ssl.CERT_REQUIRED
        else:
            context.verify_mode = ssl.CERT_NONE

        # Set recommended cipher suites
        context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5')

        logger.info("Server SSL context created")
        return context

    def create_client_context(self) -> ssl.SSLContext:
        """Create SSL context for client"""
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = self.min_version.value

        # Load CA certificate
        if self.ca_file:
            context.load_verify_locations(self.ca_file)
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
        else:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        # Load client certificates for mTLS
        if self.cert_file and self.key_file:
            context.load_cert_chain(self.cert_file, self.key_file)

        logger.info("Client SSL context created")
        return context


###############################################################################
# Request/Response Validation
###############################################################################

class RequestValidator:
    """Validates RPC requests"""

    def __init__(self, max_request_size: int = 10 * 1024 * 1024):
        """Initialize request validator"""
        self.max_request_size = max_request_size
        logger.info(f"RequestValidator initialized (max_size: {max_request_size} bytes)")

    def validate_request(self, request_data: bytes, method: str) -> Tuple[bool, Optional[str]]:
        """Validate request"""
        # Check size
        if len(request_data) > self.max_request_size:
            return False, f"Request exceeds max size ({len(request_data)} > {self.max_request_size})"

        # Check content type (if applicable)
        try:
            if isinstance(request_data, bytes):
                json.loads(request_data)
        except json.JSONDecodeError:
            # Binary protobuf is acceptable
            pass

        return True, None

    def validate_response(self, response_data: bytes) -> Tuple[bool, Optional[str]]:
        """Validate response"""
        if len(response_data) > self.max_request_size:
            return False, f"Response exceeds max size ({len(response_data)} > {self.max_request_size})"

        return True, None


###############################################################################
# Audit Logger
###############################################################################

class AuditLogger:
    """Logs all RPC operations for compliance"""

    def __init__(self, log_file: str = "/var/log/debvisor-rpc-audit.log"):
        """Initialize audit logger"""
        self.log_file = log_file
        self.audit_handler = logging.FileHandler(log_file)
        self.audit_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(message)s')
        )
        audit_logger.addHandler(self.audit_handler)
        logger.info(f"AuditLogger initialized (file: {log_file})")

    def log_operation(self, entry: AuditLogEntry):
        """Log an RPC operation"""
        audit_logger.info(json.dumps(entry.to_dict()))

    def log_access_denied(
        self,
        user_id: str,
        username: str,
        resource_type: str,
        resource_id: str,
        reason: str
    ):
        """Log access denied event"""
        entry = AuditLogEntry(
            timestamp=datetime.now(timezone.utc),
            user_id=user_id,
            username=username,
            action="access_denied",
            resource_type=resource_type,
            resource_id=resource_id,
            status="denied",
            status_code=403,
            request_metadata={},
            response_metadata={},
            duration_ms=0,
            error_message=reason
        )
        self.log_operation(entry)

    def log_authentication_failure(self, reason: str):
        """Log authentication failure"""
        entry = AuditLogEntry(
            timestamp=datetime.now(timezone.utc),
            user_id="unknown",
            username="unknown",
            action="authentication_failed",
            resource_type="system",
            resource_id="rpc",
            status="failed",
            status_code=401,
            request_metadata={},
            response_metadata={},
            duration_ms=0,
            error_message=reason
        )
        self.log_operation(entry)


###############################################################################
# Decorator for securing RPC methods
###############################################################################

def require_auth(auth_service: AuthenticationService):
    """Decorator to require authentication"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, request, context):
            # Extract token from metadata
            metadata = dict(context.invocation_metadata())
            token = metadata.get('authorization', '').replace('Bearer ', '')

            if not token:
                context.abort(401, 'Missing authentication token')

            is_valid, auth_token, error = auth_service.validate_token(token)
            if not is_valid:
                context.abort(401, f'Invalid token: {error}')

            # Store auth token in context for use in handler
            context.auth_token = auth_token
            return func(self, request, context)

        return wrapper
    return decorator


def require_permission(
    auth_service: AuthorizationService,
    resource_type: str,
    action: str
):
    """Decorator to require specific permission"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, request, context):
            if not hasattr(context, 'auth_token') or not context.auth_token:
                context.abort(401, 'Authentication required')

            auth_token = context.auth_token
            has_permission, error = auth_service.check_permission(
                auth_token.roles,
                resource_type,
                action
            )

            if not has_permission:
                context.abort(403, error)

            return func(self, request, context)

        return wrapper
    return decorator


###############################################################################
# Example Usage & Tests
###############################################################################

if __name__ == "__main__":
    # Example authentication
    auth_config = AuthenticationConfig(
        secret_key="your-secret-key-here",  # nosec B106
        token_expiry_seconds=3600
    )
    auth_service = AuthenticationService(auth_config)

    # Create token
    token = auth_service.create_token(
        user_id="user123",
        username="john.doe",
        roles=[RoleType.OPERATOR.value],
        scopes=["cluster:read", "pod:write"],
        metadata={"department": "operations"}
    )
    print(f"Created token: {token[:20]}...")

    # Validate token
    is_valid, auth_token, error = auth_service.validate_token(token)
    print(f"Token valid: {is_valid}, User: {auth_token.username if auth_token else 'N/A'}")

    # Example authorization
    authz_config = AuthorizationConfig(enabled=True)
    authz_service = AuthorizationService(authz_config)

    # Check permission
    has_perm, error = authz_service.check_permission(
        [RoleType.OPERATOR.value],
        ResourceType.NODE.value,
        Action.READ.value
    )
    print(f"Has permission: {has_perm}")

    # Example TLS
    tls_manager = TLSManager(
        cert_file="/path/to/cert.pem",
        key_file="/path/to/key.pem",
        ca_file="/path/to/ca.pem"
    )

    # Example audit logging
    audit_logger = AuditLogger()
    entry = AuditLogEntry(
        timestamp=datetime.now(timezone.utc),
        user_id="user123",
        username="john.doe",
        action="cluster_create",
        resource_type="cluster",
        resource_id="prod-cluster",
        status="success",
        status_code=200,
        request_metadata={"nodes": 3},
        response_metadata={"cluster_id": "abc123"},
        duration_ms=125.5
    )
    audit_logger.log_operation(entry)
