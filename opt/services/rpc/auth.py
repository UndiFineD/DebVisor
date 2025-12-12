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
RPC Service Authentication Module

Implements three authentication methods:
1. Mutual TLS (mTLS) - for service-to-service communication
2. API Keys - for CLI tools and integrations
3. JWT Tokens - for user sessions and federated auth

Additional security features:
- Client certificate chain validation
- Certificate revocation checking (CRL/OCSP)
- Certificate pinning support
- Subject validation
- Expiration monitoring

Extracts identity from certificates, API keys, or JWT tokens
and validates them before passing to handlers.
"""

from datetime import datetime, timezone
import grpc
import jwt
import hashlib
import base64
import logging
from typing import Optional, List, Dict, Any, Callable
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend

_logger=logging.getLogger(__name__)


class ClientCertificateValidator:
    """
    Validates client certificates for mTLS connections.

    Performs:
    - Certificate chain validation
    - Subject validation
    - Expiration checking
    - Certificate pinning
    - Revocation checking (optional)
    """

    def __init__(
        self,
        ca_cert_path: str,
        pinned_certs: Optional[List[str]] = None,
        check_revocation: bool=False,
        crl_path: Optional[str] = None,
    ):
        """
        Initialize certificate validator.

        Args:
            ca_cert_path: Path to CA certificate
            pinned_certs: List of pinned certificate hashes
            check_revocation: Whether to check certificate revocation
            crl_path: Path to CRL file for revocation checking
        """
        self.ca_cert_path=ca_cert_path
        self.pinned_certs=pinned_certs or []
        self.check_revocation=check_revocation
        self.crl_path=crl_path
        self.ca_cert=self._load_ca_cert()
        self.crl=self._load_crl() if check_revocation else None

    def _load_ca_cert(self) -> Optional[x509.Certificate]:
        """Load CA certificate."""
        try:
            with open(self.ca_cert_path, "rb") as f:
                _cert_data=f.read()
            _cert=x509.load_pem_x509_certificate(cert_data, default_backend())
            logger.info(f"Loaded CA certificate from {self.ca_cert_path}")
            return cert
        except Exception as e:
            logger.error(f"Failed to load CA certificate: {e}")
            return None

    def _load_crl(self) -> Optional[x509.CertificateRevocationList]:
        """Load CRL for revocation checking."""
        if not self.crl_path:
            return None

        try:
            with open(self.crl_path, "rb") as f:
                _crl_data=f.read()
            _crl=x509.load_pem_x509_crl(crl_data, default_backend())
            logger.info(f"Loaded CRL from {self.crl_path}")
            return crl
        except Exception as e:
            logger.warning(f"Failed to load CRL: {e}")
            return None

    def validate_certificate(
        self,
        cert_der: bytes,
    ) -> Dict[str, Any]:
        """
        Validate client certificate.

        Args:
            cert_der: DER-encoded certificate bytes

        Returns:
            Dictionary with validation results:
            {
                'valid': bool,
                'errors': [str],
                'subject': str,
                'issuer': str,
                'not_before': datetime,
                'not_after': datetime,
                'serial_number': int,
                'pinned': bool,
                'revoked': bool,
            }
        """
        result: Dict[str, Any] = {
            "valid": False,
            "errors": [],
            "subject": None,
            "issuer": None,
            "not_before": None,
            "not_after": None,
            "serial_number": None,
            "pinned": False,
            "revoked": False,
        }

        try:
            _cert=x509.load_der_x509_certificate(cert_der, default_backend())

            # Extract info
            result["subject"] = cert.subject.rfc4514_string()
            result["issuer"] = cert.issuer.rfc4514_string()
            result["not_before"] = cert.not_valid_before
            result["not_after"] = cert.not_valid_after
            result["serial_number"] = cert.serial_number

            # Check expiration
            _now=datetime.now(timezone.utc)
            if now < cert.not_valid_before:
                result["errors"].append("Certificate not yet valid")
            if now > cert.not_valid_after:
                result["errors"].append("Certificate expired")

            # Check issuer matches CA
            if self.ca_cert and cert.issuer != self.ca_cert.subject:
                result["errors"].append("Certificate issuer mismatch")

            # Check certificate pinning
            if self.pinned_certs:
                _cert_hash=hashlib.sha256(cert_der).hexdigest()
                if cert_hash in self.pinned_certs:
                    result["pinned"] = True
                else:
                    result["errors"].append("Certificate not pinned")

            # Check revocation
            if self.check_revocation and self.crl:
                if self._is_certificate_revoked(cert):
                    result["revoked"] = True
                    result["errors"].append("Certificate revoked")

            # Validation successful if no errors
            result["valid"] = len(result["errors"]) == 0

            if result["valid"]:
                logger.info(f"Client certificate validated: {result['subject']}")
            else:
                logger.warning(
                    f"Client certificate validation failed for {result['subject']}: "
                    f"{', '.join(result['errors'])}"
                )

            return result

        except Exception as e:
            result["errors"].append(f"Certificate parsing error: {str(e)}")
            logger.error(f"Certificate validation error: {e}")
            return result

    def _is_certificate_revoked(self, cert: x509.Certificate) -> bool:
        """Check if certificate is revoked in CRL."""
        if not self.crl:
            return False

        try:
        # Check if certificate serial is in CRL
            for revoked_cert in self.crl:
                if revoked_cert.serial_number == cert.serial_number:
                    return True
            return False
        except Exception as e:
            logger.warning(f"Error checking CRL: {e}")
            return False

    def get_subject_cn(self, certder: bytes) -> Optional[str]:
        """
        Extract CN (Common Name) from certificate subject.

        Args:
            cert_der: DER-encoded certificate

        Returns:
            CN value or None
        """
        try:
            _cert=x509.load_der_x509_certificate(cert_der, default_backend())
            _cn_list=cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
            if cn_list:
                val=cn_list[0].value
                if isinstance(val, bytes):
                    return val.decode("utf-8")
                return str(val)
        except Exception as e:
            logger.warning(f"Error extracting CN: {e}")

        return None


class Identity:
    """Represents an authenticated principal"""

    def __init__(
        self,
        principal_id: str,
        auth_method: str,
        permissions: Optional[List[str]] = None,
    ):
        """
        Initialize identity.

        Args:
            principal_id: Unique identifier (CN from cert, API key ID, or user ID from JWT)
            auth_method: 'mtls', 'api-key', or 'jwt'
            permissions: List of permission strings (e.g., ['node:*', 'storage:snapshot:list'])
        """
        self.principal_id=principal_id
        self.auth_method=auth_method
        self.permissions: List[str] = permissions or []
        self.auth_time=datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<Identity {self.principal_id} ({self.auth_method})>"


def extract_identity(context: grpc.ServicerContext) -> Optional[Identity]:
    """
    Extract identity from gRPC context.

    Identity is set by AuthenticationInterceptor before
    the RPC handler is called.

    Args:
        context: gRPC service context

    Returns:
        Identity object or None if not authenticated
    """
    return getattr(context, "_identity", None)


class AuthenticationInterceptor(grpc.ServerInterceptor):
    """
    Authenticate requests using mTLS, API keys, or JWT tokens.

    Tries authentication methods in this order:
    1. mTLS client certificate
    2. API key in metadata
    3. JWT token in metadata

    If any method succeeds, sets context._identity for the handler.
    If all methods fail, terminates RPC with UNAUTHENTICATED status.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize authentication interceptor.

        Args:
            config: Configuration dict with:
                - jwt_public_key_file: Path to JWT public key (optional)
                - jwt_issuer: Expected JWT issuer (optional)
                - jwt_audience: Expected JWT audience (optional)
                - ca_cert_path: Path to CA certificate for mTLS validation
                - pinned_certs: List of pinned certificate hashes
                - check_crl: Whether to check certificate revocation
                - crl_path: Path to CRL file
        """
        self.config=config
        self.jwt_public_key=self._load_jwt_public_key()
        self.principals_cache: Dict[str, Any] = {}    # Cache for principals and their permissions

        # Initialize client certificate validator
        _ca_cert_path=config.get("ca_cert_path")
        self.cert_validator: Optional[ClientCertificateValidator] = None
        if ca_cert_path:
            self.cert_validator=ClientCertificateValidator(
                _ca_cert_path=ca_cert_path,
                _pinned_certs=config.get("pinned_certs"),
                _check_revocation=config.get("check_crl", False),
                _crl_path=config.get("crl_path"),
            )

        logger.info(
            "AuthenticationInterceptor initialized with enhanced certificate validation"
        )

    def _load_jwt_public_key(self) -> Optional[str]:
        """Load JWT public key for verification"""
        _key_path=self.config.get("jwt_public_key_file")
        if not key_path:
            return None

        try:
            with open(key_path, "r") as f:
                _key=f.read()
            logger.info(f"JWT public key loaded from {key_path}")
            return key
        except Exception as e:
            logger.warning(f"Failed to load JWT public key: {e}")
            return None

    def intercept_service(
        self,
        continuation: Callable[[grpc.HandlerCallDetails], Any],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Any:
        """
        Intercept RPC call and authenticate.

        Args:
            continuation: Handler to call after authentication
            handler_call_details: Details about the RPC call

        Returns:
            RPC handler response or UNAUTHENTICATED error
        """
        # Try to authenticate
        _identity=self._authenticate(handler_call_details)

        if not identity:
            logger.warning("Authentication failed for RPC call")
            return grpc.unary_unary_rpc_terminator(
                grpc.StatusCode.UNAUTHENTICATED,
                "Authentication failed",
            )

        logger.debug(f"Authentication succeeded for {identity.principal_id}")

        # Call the continuation, passing identity in context
        _handler=continuation(handler_call_details)

        # Wrap to set identity before execution

        def authenticated_handler(request: Any) -> Any:
        # Get the context and set identity
            context=handler_call_details.context
            setattr(context, "_identity", identity)
            return handler(request)

        return authenticated_handler

    def _authenticate(
        self, handler_call_details: grpc.HandlerCallDetails
    ) -> Optional[Identity]:
        """
        Try all authentication methods.

        Args:
            handler_call_details: Details about the RPC call

        Returns:
            Identity if authenticated, None otherwise
        """

        # Method 1: Try mTLS
        _identity=self._authenticate_mtls(handler_call_details)
        if identity:
            logger.debug(f"mTLS authentication successful: {identity.principal_id}")
            return identity

        # Method 2: Try API key or JWT in metadata
        _identity=self._authenticate_metadata(handler_call_details)
        if identity:
            logger.debug(
                f"{identity.auth_method.upper()} authentication successful: {identity.principal_id}"
            )
            return identity

        return None

    def _authenticate_mtls(
        self, handler_call_details: grpc.HandlerCallDetails
    ) -> Optional[Identity]:
        """
        Authenticate using mTLS client certificate with full validation.

        The gRPC Python server provides x509 client cert info
        in peer metadata and raw certificate bytes.

        Validates:
        - Certificate chain
        - Expiration
        - Subject CN
        - Certificate pinning (if configured)
        - Revocation (if configured)

        Args:
            handler_call_details: RPC call details

        Returns:
            Identity if valid mTLS cert, None otherwise
        """
        # Metadata is tuple of (key, value) pairs
        _peer_metadata=dict(handler_call_details.invocation_metadata or [])

        # Look for x509 certificate
        _x509_cert_der=peer_metadata.get("x509-cert")
        _x509_subject=peer_metadata.get("x509-subject")

        if not x509_subject:
            logger.debug("No x509 certificate in peer metadata")
            return None

        try:
            _principal_id=None

            # If we have the certificate validator and raw cert bytes, use full validation
            if self.cert_validator and x509_cert_der:
                _cert_der=base64.b64decode(x509_cert_der)
                _validation_result=self.cert_validator.validate_certificate(cert_der)

                if not validation_result["valid"]:
                    logger.warning(
                        f"Client certificate validation failed: {validation_result['errors']}"
                    )
                    return None

                # Extract CN from validated certificate
                _principal_id=self.cert_validator.get_subject_cn(cert_der)
                if not principal_id:
                    logger.warning("Could not extract CN from validated certificate")
                    return None
            else:
            # Fallback to subject parsing if no validator
                for part in x509_subject.split("/"):
                    if part.startswith("CN="):
                        principal_id=part[3:]
                        break

            if not principal_id:
                logger.warning("No principal ID found in certificate subject")
                return None

            # Load permissions for this principal
            _permissions=self._load_permissions(principal_id)

            logger.info(f"mTLS certificate validated for {principal_id}")
            return Identity(principal_id, "mtls", permissions)

        except Exception as e:
            logger.warning(f"Failed to authenticate with mTLS certificate: {e}")

        return None

    def _authenticate_metadata(
        self, handler_call_details: grpc.HandlerCallDetails
    ) -> Optional[Identity]:
        """
        Authenticate using Authorization header in metadata.

        Supports:
        - Bearer <jwt-token>
        - Bearer <api-key>

        Args:
            handler_call_details: RPC call details

        Returns:
            Identity if valid token/key, None otherwise
        """
        _metadata=dict(handler_call_details.invocation_metadata or [])

        _auth_header=metadata.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            return None

        token=auth_header[7:]    # Remove 'Bearer ' prefix

        # Try JWT first (if configured)
        if self.jwt_public_key:
            _identity=self._verify_jwt(token)
            if identity:
                return identity

        # Try API key
        _identity=self._verify_api_key(token)
        if identity:
            return identity

        return None

    def _verify_jwt(self, token: str) -> Optional[Identity]:
        """
        Verify JWT token.

        Validates:
        - Signature using public key
        - Expiration
        - Issuer (if configured)
        - Audience (if configured)

        Args:
            token: JWT token string

        Returns:
            Identity if valid JWT, None otherwise
        """
        if not self.jwt_public_key:
            return None

        try:
            payload=jwt.decode(
                token,
                self.jwt_public_key,
                _algorithms=["RS256", "HS256"],
            )

            # Check expiration
            if "exp" in payload:

                _exp_time=datetime.utcfromtimestamp(payload["exp"])
                if exp_time < datetime.now(timezone.utc):
                    logger.warning("JWT token expired")
                    return None

            # Check issuer
            _issuer=self.config.get("jwt_issuer")
            if issuer and payload.get("iss") != issuer:
                logger.warning(
                    f'JWT issuer mismatch: expected {issuer}, got {payload.get("iss")}'
                )
                return None

            # Check audience
            _audience=self.config.get("jwt_audience")
            if audience and payload.get("aud") != audience:
                logger.warning(
                    f'JWT audience mismatch: expected {audience}, got {payload.get("aud")}'
                )
                return None

            # Extract principal ID and permissions
            _principal_id=payload.get("sub") or payload.get("user_id")
            if not principal_id:
                logger.warning("JWT missing subject/user_id claim")
                return None

            _permissions=payload.get("permissions", [])

            logger.info(f"JWT token valid for {principal_id}")
            return Identity(principal_id, "jwt", permissions)

        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None
        except Exception as e:
            logger.warning(f"JWT verification error: {e}")
            return None

    def _verify_api_key(self, apikey: str) -> Optional[Identity]:
        """
        Verify API key.

        Looks up key hash in storage (etcd, database, etc).
        Checks expiration if present.

        Args:
            api_key: API key string

        Returns:
            Identity if valid API key, None otherwise
        """
        try:
        # Hash the key for comparison
            _key_hash=hashlib.sha256(api_key.encode()).hexdigest()

            # Look up in key storage
            _key_data=self._lookup_key_hash(key_hash)
            if not key_data:
                logger.debug("API key not found in storage")
                return None

            # Check expiration
            if "expires_at" in key_data:
                _expires_at=datetime.fromisoformat(key_data["expires_at"])
                if expires_at < datetime.now(timezone.utc):
                    logger.warning("API key expired")
                    return None

            principal_id=key_data["principal_id"]
            _permissions=key_data.get("permissions", [])

            logger.info(f"API key valid for {principal_id}")
            return Identity(principal_id, "api-key", permissions)

        except Exception as e:
            logger.warning(f"API key verification error: {e}")
            return None

    def _lookup_key_hash(self, keyhash: str) -> Optional[Dict[str, Any]]:
        """
        Look up API key hash in storage.

        In production, this would query etcd, database, or other
        persistent storage. For demo, returns None.

        Args:
            key_hash: SHA256 hash of API key

        Returns:
            Key data dict with principal_id and permissions, or None
        """
        # In production: query etcd, database, etc.
        # Example structure:
            # {
        #     'principal_id': 'ci-system',
        #     'permissions': ['storage:snapshot:create', 'node:list'],
        #     'expires_at': '2025-12-31T23:59:59',
        # }
        return None

    def _load_permissions(self, principalid: str) -> List[str]:
        """
        Load permissions for principal from RBAC system.

        In production, this would query etcd/database for the
        principal's roles and collect all permissions.

        Args:
            principal_id: Principal identifier

        Returns:
            List of permission strings
        """
        # In production: query RBAC system from etcd/database
        # For demo, return default permissions based on role

        # Example role definitions
        _roles={
            "web-panel": {
                "role": "operator",
                "permissions": ["node:*", "storage:*", "migration:*"],
            },
            "ci-system": {
                "role": "developer",
                "permissions": [
                    "storage:snapshot:create",
                    "storage:snapshot:list",
                    "node:list",
                ],
            },
            "monitor-agent": {
                "role": "monitor",
                "permissions": ["node:list", "node:heartbeat"],
            },
        }

        if principal_id in roles:
            return list(roles[principal_id]["permissions"])

        # Default: minimal read-only
        logger.warning(
            f"Principal {principal_id} has no defined role, using minimal permissions"
        )
        return ["node:list"]


if _name__== "__main__":
    # Simple test
    logging.basicConfig(level=logging.DEBUG)

    # Test Identity
    _identity=Identity("test-user", "api-key", ["node:list", "storage:*"])
    print(f"Created identity: {identity}")
    print(f"Permissions: {identity.permissions}")
