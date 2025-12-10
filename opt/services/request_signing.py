#!/usr/bin/env python3

"""
Request Signing and Verification for DebVisor Inter-Service Communication.

Implements HMAC-based request signing for secure service-to-service
communication, preventing request tampering and replay attacks.

Features:
- HMAC-SHA256 request signing
- Timestamp-based replay protection
- Request body integrity verification
- Key rotation support
- Multiple signing algorithms

Author: DebVisor Team
Date: November 28, 2025
"""

from datetime import datetime, timezone
from typing import TypeVar
from typing import Tuple
import base64
import hashlib
import hmac
import json
import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, Optional, TupleVar
from functools import wraps

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class SigningAlgorithm(Enum):
    """Supported signing algorithms."""

    HMAC_SHA256 = "HMAC-SHA256"
    HMAC_SHA384 = "HMAC-SHA384"
    HMAC_SHA512 = "HMAC-SHA512"


@dataclass
class SigningConfig:
    """Configuration for request signing."""

    secret_key: str
    algorithm: SigningAlgorithm = SigningAlgorithm.HMAC_SHA256
    timestamp_tolerance_seconds: int = 300    # 5 minutes
    include_headers: Tuple[str, ...] = ("content-type", "x-request-id")
    key_id: str = "default"    # For key rotation


@dataclass
class SignedRequest:
    """Signed request container."""

    method: str
    path: str
    body: Optional[bytes]
    timestamp: str
    signature: str
    key_id: str
    algorithm: str
    signed_headers: Dict[str, str]


class RequestSigner:
    """
    Signs and verifies requests for inter-service communication.

    Example:
        signer = RequestSigner(SigningConfig(secret_key="my-secret"))

        # Sign a request
        signature = signer.sign_request(
            method="POST",
            path="/api/v1/nodes",
            body=json.dumps({"name": "node-1"}).encode(),
            headers={"content-type": "application/json"}
        )

        # Verify a request
        is_valid = signer.verify_request(
            method="POST",
            path="/api/v1/nodes",
            body=b'{"name": "node-1"}',
            headers={"content-type": "application/json"},
            signature=signature,
            timestamp="2025-11-28T12:00:00Z"
        )
    """

    def __init__(self, config: SigningConfig):
        """
        Initialize request signer.

        Args:
            config: Signing configuration
        """
        self.config = config
        self._hash_func = self._get_hash_func(config.algorithm)

    def _get_hash_func(self, algorithm: SigningAlgorithm) -> Callable[..., Any]:
        """Get hash function for algorithm."""
        if algorithm == SigningAlgorithm.HMAC_SHA256:
            return hashlib.sha256
        elif algorithm == SigningAlgorithm.HMAC_SHA384:
            return hashlib.sha384
        elif algorithm == SigningAlgorithm.HMAC_SHA512:
            return hashlib.sha512
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    def _compute_body_hash(self, body: Optional[bytes]) -> str:
        """Compute hash of request body."""
        if body is None:
            body = b""
        return hashlib.sha256(body).hexdigest()

    def _build_canonical_request(
        self,
        method: str,
        path: str,
        body: Optional[bytes],
        timestamp: str,
        headers: Dict[str, str],
    ) -> str:
        """
        Build canonical request string for signing.

        Format:
        METHOD
        PATH
        TIMESTAMP
        HEADER1:value1
        HEADER2:value2
        BODY_HASH
        """
        # Normalize method
        method = method.upper()

        # Normalize path
        path = path.split("?")[0]    # Remove query string for signing

        # Filter and sort headers
        signed_headers = {}
        for header_name in sorted(self.config.include_headers):
            header_key = header_name.lower()
            for key, value in headers.items():
                if key.lower() == header_key:
                    signed_headers[header_key] = value.strip()
                    break

        # Build header string
        header_string = "\n".join(f"{k}:{v}" for k, v in sorted(signed_headers.items()))

        # Compute body hash
        body_hash = self._compute_body_hash(body)

        # Build canonical request
        canonical = f"{method}\n{path}\n{timestamp}\n{header_string}\n{body_hash}"

        return canonical

    def sign_request(
        self,
        method: str,
        path: str,
        body: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Sign a request.

        Args:
            method: HTTP method
            path: Request path
            body: Request body
            headers: Request headers
            timestamp: Request timestamp (auto-generated if not provided)

        Returns:
            Dictionary with signature headers to add to request
        """
        headers = headers or {}
        timestamp = timestamp or datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        # Build canonical request
        canonical = self._build_canonical_request(
            method, path, body, timestamp, headers
        )

        # Compute signature
        signature = hmac.new(
            self.config.secret_key.encode("utf-8"),
            canonical.encode("utf-8"),
            self._hash_func,
        ).hexdigest()

        # Build signed headers list
        signed_headers = ", ".join(sorted(self.config.include_headers))

        return {
            "X-DebVisor-Signature": signature,
            "X-DebVisor-Timestamp": timestamp,
            "X-DebVisor-Algorithm": self.config.algorithm.value,
            "X-DebVisor-Key-Id": self.config.key_id,
            "X-DebVisor-Signed-Headers": signed_headers,
        }

    def verify_request(
        self,
        method: str,
        path: str,
        body: Optional[bytes],
        headers: Dict[str, str],
        signature: str,
        timestamp: str,
        algorithm: Optional[str] = None,
        key_id: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """
        Verify a signed request.

        Args:
            method: HTTP method
            path: Request path
            body: Request body
            headers: Request headers
            signature: Request signature
            timestamp: Request timestamp
            algorithm: Signing algorithm (optional)
            key_id: Key ID (optional)

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Verify key ID matches
        if key_id and key_id != self.config.key_id:
            return False, f"Unknown key ID: {key_id}"

        # Verify algorithm matches
        if algorithm:
            try:
                algo = SigningAlgorithm(algorithm)
                if algo != self.config.algorithm:
                    return False, (
                        "Algorithm mismatch: expected "
                        f"{self.config.algorithm.value}, got {algorithm}"
                    )
            except ValueError:
                return False, f"Unsupported algorithm: {algorithm}"

        # Verify timestamp is recent
        try:
            request_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )
            now = datetime.now(timezone.utc)

            if (
                abs((now - request_time).total_seconds())
                > self.config.timestamp_tolerance_seconds
            ):
                return False, "Request timestamp is too old or in the future"
        except ValueError:
            return False, "Invalid timestamp format"

        # Build canonical request and compute expected signature
        canonical = self._build_canonical_request(
            method, path, body, timestamp, headers
        )

        expected_signature = hmac.new(
            self.config.secret_key.encode("utf-8"),
            canonical.encode("utf-8"),
            self._hash_func,
        ).hexdigest()

        # Compare signatures using constant-time comparison
        if not hmac.compare_digest(expected_signature, signature):
            return False, "Signature verification failed"

        return True, ""

    def extract_signature_headers(
        self, headers: Dict[str, str]
    ) -> Optional[Dict[str, str]]:
        """
        Extract signature-related headers from request headers.

        Args:
            headers: All request headers

        Returns:
            Dictionary with signature headers or None if not present
        """
        # Normalize header keys
        normalized = {k.lower(): v for k, v in headers.items()}

        required = [
            "x-debvisor-signature",
            "x-debvisor-timestamp",
        ]

        if not all(h in normalized for h in required):
            return None

        return {
            "signature": normalized.get("x-debvisor-signature", ""),
            "timestamp": normalized.get("x-debvisor-timestamp", ""),
            "algorithm": normalized["x-debvisor-algorithm"],
            "key_id": normalized["x-debvisor-key-id"],
            "signed_headers": normalized.get("x-debvisor-signed-headers", ""),
        }


# =============================================================================
# Flask Integration
# =============================================================================


def require_signed_request(signer: RequestSigner) -> Callable[[F], F]:
    """
    Flask decorator to require signed requests.

    Example:
        signer = RequestSigner(SigningConfig(secret_key=os.getenv("SIGNING_KEY")))

        @app.route("/api/internal/nodes", methods=["POST"])
        @require_signed_request(signer)
        def create_node():
            return jsonify({"status": "ok"})
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Import Flask here to avoid circular imports
            from flask import request, jsonify

            # Extract signature headers
            sig_headers = signer.extract_signature_headers(dict(request.headers))

            if not sig_headers:
                logger.warning(f"Missing signature headers for {request.path}")
                return (
                    jsonify(
                        {
                            "error": "Missing request signature",
                            "code": "SIGNATURE_REQUIRED",
                        }
                    ),
                    401,
                )

            # Verify signature
            is_valid, error = signer.verify_request(
                method=request.method,
                path=request.path,
                body=request.get_data(),
                headers=dict(request.headers),
                signature=sig_headers["signature"],
                timestamp=sig_headers["timestamp"],
                algorithm=sig_headers.get("algorithm"),
                key_id=sig_headers.get("key_id"),
            )

            if not is_valid:
                logger.warning(f"Invalid signature for {request.path}: {error}")
                return (
                    jsonify(
                        {
                            "error": "Invalid request signature",
                            "code": "INVALID_SIGNATURE",
                            "detail": error,
                        }
                    ),
                    401,
                )

            return func(*args, **kwargs)

        return wrapper    # type: ignore

    return decorator


# =============================================================================
# HTTP Client Integration
# =============================================================================


class SignedHTTPClient:
    """
    HTTP client wrapper that automatically signs requests.

    Example:
        client = SignedHTTPClient(
            base_url="http://node-service:8080",
            signer=RequestSigner(SigningConfig(secret_key="secret"))
        )

        response = await client.post("/api/nodes", json={"name": "node-1"})
    """

    def __init__(
        self, base_url: str, signer: RequestSigner, timeout_seconds: float = 30.0
    ):
        """
        Initialize signed HTTP client.

        Args:
            base_url: Base URL for requests
            signer: Request signer instance
            timeout_seconds: Request timeout
        """
        self.base_url = base_url.rstrip("/")
        self.signer = signer
        self.timeout_seconds = timeout_seconds

    async def request(
        self,
        method: str,
        path: str,
        body: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a signed HTTP request.

        Args:
            method: HTTP method
            path: Request path
            body: Raw body bytes
            headers: Additional headers
            json_data: JSON body (will be serialized)

        Returns:
            Response data
        """
        import aiohttp

        headers = headers or {}

        # Handle JSON body
        if json_data is not None:
            body = json.dumps(json_data).encode("utf-8")
            headers["Content-Type"] = "application/json"

        # Sign the request
        sig_headers = self.signer.sign_request(
            method=method, path=path, body=body, headers=headers
        )
        headers.update(sig_headers)

        # Make the request
        url = f"{self.base_url}{path}"

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                data=body,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.timeout_seconds),
            ) as response:
                response_body = await response.text()

                if response.content_type == "application/json":
                    return {
                        "status": response.status,
                        "data": json.loads(response_body),
                        "headers": dict(response.headers),
                    }
                else:
                    return {
                        "status": response.status,
                        "data": response_body,
                        "headers": dict(response.headers),
                    }

    async def get(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make signed GET request."""
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make signed POST request."""
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make signed PUT request."""
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make signed DELETE request."""
        return await self.request("DELETE", path, **kwargs)


# =============================================================================
# Key Rotation Support
# =============================================================================


class MultiKeyRequestSigner:
    """
    Request signer with multiple key support for rotation.

    Example:
        signer = MultiKeyRequestSigner()
        signer.add_key("key-2025-11", "secret-1", is_primary=True)
        signer.add_key("key-2025-10", "secret-0")    # Old key for verification

        # Signs with primary key
        sig = signer.sign_request(...)

        # Verifies with any registered key
        valid, error = signer.verify_request(...)
    """

    def __init__(self, algorithm: SigningAlgorithm = SigningAlgorithm.HMAC_SHA256):
        """Initialize multi-key signer."""
        self.algorithm = algorithm
        self._keys: Dict[str, RequestSigner] = {}
        self._primary_key_id: Optional[str] = None

    def add_key(self, key_id: str, secret_key: str, is_primary: bool = False) -> None:
        """
        Add a signing key.

        Args:
            key_id: Key identifier
            secret_key: Secret key value
            is_primary: Whether this is the primary key for signing
        """
        config = SigningConfig(
            secret_key=secret_key, algorithm=self.algorithm, key_id=key_id
        )
        self._keys[key_id] = RequestSigner(config)

        if is_primary:
            self._primary_key_id = key_id

        logger.info(f"Added signing key: {key_id} (primary: {is_primary})")

    def remove_key(self, key_id: str) -> None:
        """Remove a signing key."""
        if key_id in self._keys:
            del self._keys[key_id]
            if self._primary_key_id == key_id:
                self._primary_key_id = None
            logger.info(f"Removed signing key: {key_id}")

    def sign_request(self, **kwargs: Any) -> Dict[str, str]:
        """Sign request with primary key."""
        if not self._primary_key_id:
            raise RuntimeError("No primary signing key configured")

        return self._keys[self._primary_key_id].sign_request(**kwargs)

    def verify_request(
        self, key_id: Optional[str] = None, **kwargs: Any
    ) -> Tuple[bool, str]:
        """
        Verify request with appropriate key.

        Args:
            key_id: Key ID to use (or try all keys if not specified)
            **kwargs: Verification parameters

        Returns:
            Tuple of (is_valid, error_message)
        """
        if key_id:
            if key_id not in self._keys:
                return False, f"Unknown key ID: {key_id}"
            return self._keys[key_id].verify_request(**kwargs)

        # Try all keys
        for kid, signer in self._keys.items():
            is_valid, error = signer.verify_request(key_id=kid, **kwargs)
            if is_valid:
                return True, ""

        return False, "Signature verification failed with all registered keys"


# =============================================================================
# Convenience Functions
# =============================================================================


def get_default_signer() -> RequestSigner:
    """
    Get default request signer using environment variable.

    Uses DEBVISOR_SIGNING_KEY environment variable.
    """
    secret_key = os.getenv("DEBVISOR_SIGNING_KEY")
    if not secret_key:
        # Generate a random key for development
        secret_key = base64.b64encode(os.urandom(32)).decode("utf-8")
        logger.warning(
            "DEBVISOR_SIGNING_KEY not set, using random key. " "Set this in production!"
        )

    return RequestSigner(SigningConfig(secret_key=secret_key))
