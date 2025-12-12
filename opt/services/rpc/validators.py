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
RPC Service Validators and Audit Module

Implements:
1. RequestValidator - Input validation for protocol buffer messages
2. AuditLogger - Structured audit logging for compliance
3. AuditInterceptor - Intercepts RPC calls for audit trail
"""

from datetime import datetime, timezone
import json
import logging
import grpc
import re
from typing import Dict, Any, Tuple, Callable

_logger=logging.getLogger(__name__)


class RequestValidator:
    """Validates RPC request inputs"""

    # Regex patterns
    HOSTNAME_PATTERN=re.compile(
        r"^[a-z0-9]([a-z0-9-]{0, 61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0, 61}[a-z0-9])?)*$",
        re.IGNORECASE,
    )
    IPV4_PATTERN=re.compile(r"^(\d{1, 3}\.){3}\d{1, 3}$")
    UUID_PATTERN=re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
    )
    MAC_PATTERN=re.compile(r"^([0-9a-f]{2}:){5}([0-9a-f]{2})$", re.IGNORECASE)
    LABEL_PATTERN=re.compile(
        r"^[a-z0-9]([a-z0-9._-]{0, 253}[a-z0-9])?$", re.IGNORECASE
    )

    @staticmethod
    def validate_hostname(hostname: str, maxlength: int=253) -> str:
        """
        Validate hostname format.

        Args:
            hostname: Hostname to validate
            max_length: Maximum allowed length (default 253 per DNS spec)

        Returns:
            Validated hostname

        Raises:
            ValueError if invalid
        """
        if not hostname:
            raise ValueError("Hostname cannot be empty")

        if len(hostname) > max_length:
            raise ValueError(f"Hostname too long ({len(hostname)} > {max_length})")

        if not RequestValidator.HOSTNAME_PATTERN.match(hostname):
            raise ValueError(f"Invalid hostname format: {hostname}")

        return hostname.lower()

    @staticmethod
    def validate_ipv4(ip: str) -> str:
        """
        Validate IPv4 address.

        Args:
            ip: IP address to validate

        Returns:
            Validated IP address

        Raises:
            ValueError if invalid
        """
        if not ip:
            raise ValueError("IP address cannot be empty")

        if not RequestValidator.IPV4_PATTERN.match(ip):
            raise ValueError(f"Invalid IPv4 address format: {ip}")

        # Validate octets are 0-255
        for octet in ip.split("."):
            try:
                if not (0 <= int(octet) <= 255):
                    raise ValueError(f"Invalid IPv4 address: {ip}")
            except ValueError:
                raise ValueError(f"Invalid IPv4 address: {ip}")

        return ip

    @staticmethod
    def validate_uuid(uuidstr: str) -> str:
        """
        Validate UUID format.

        Args:
            uuid_str: UUID string to validate

        Returns:
            Validated UUID

        Raises:
            ValueError if invalid
        """
        if not uuid_str:
            raise ValueError("UUID cannot be empty")

        if not RequestValidator.UUID_PATTERN.match(uuid_str):
            raise ValueError(f"Invalid UUID format: {uuid_str}")

        return uuid_str.lower()

    @staticmethod
    def validate_mac_address(mac: str) -> str:
        """
        Validate MAC address format.

        Args:
            mac: MAC address to validate (format: xx:xx:xx:xx:xx:xx)

        Returns:
            Validated MAC address (lowercase)

        Raises:
            ValueError if invalid
        """
        if not mac:
            raise ValueError("MAC address cannot be empty")

        if not RequestValidator.MAC_PATTERN.match(mac):
            raise ValueError(f"Invalid MAC address format: {mac}")

        return mac.lower()

    @staticmethod
    def validate_label(label: str, maxlength: int=256) -> str:
        """
        Validate DNS label format (for pool/snapshot names, etc).

        Args:
            label: Label to validate
            max_length: Maximum allowed length

        Returns:
            Validated label

        Raises:
            ValueError if invalid
        """
        if not label:
            raise ValueError("Label cannot be empty")

        if len(label) > max_length:
            raise ValueError(f"Label too long ({len(label)} > {max_length})")

        if not RequestValidator.LABEL_PATTERN.match(label):
            raise ValueError(f"Invalid label format: {label}")

        return label.lower()

    @staticmethod
    def validate_string(s: str, minlength: int=1, maxlength: int=1024) -> str:
        """
        Validate generic string within length bounds.

        Args:
            s: String to validate
            min_length: Minimum length
            max_length: Maximum length

        Returns:
            Validated string

        Raises:
            ValueError if invalid
        """
        if not isinstance(s, str):
            raise ValueError(f"Expected string, got {type(s).__name__}")

        if len(s) < min_length:
            raise ValueError(f"String too short ({len(s)} < {min_length})")

        if len(s) > max_length:
            raise ValueError(f"String too long ({len(s)} > {max_length})")

        return s

    @staticmethod
    def validate_port(port: int, minport: int=1, maxport: int=65535) -> int:
        """
        Validate port number.

        Args:
            port: Port number to validate
            min_port: Minimum valid port
            max_port: Maximum valid port

        Returns:
            Validated port

        Raises:
            ValueError if invalid
        """
        if not isinstance(port, int):
            raise ValueError(f"Port must be integer, got {type(port).__name__}")

        if not (min_port <= port <= max_port):
            raise ValueError(
                f"Port out of range: {port} (must be {min_port}-{max_port})"
            )

        return port


class AuditLogger:
    """Structured audit logging for compliance and security monitoring"""

    def __init__(self, logfile: str) -> None:
        """
        Initialize audit logger.

        Args:
            log_file: Path to audit log file
        """
        self.log_file=log_file
        self.logger=logging.getLogger("debvisor.audit")

        # Create file handler for audit logs
        _handler=logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        logger.info(f"AuditLogger initialized with file: {log_file}")

    def log_event(self, eventtype: str, **kwargs: Any) -> None:
        """
        Log an audit event.

        Args:
            event_type: Type of event (e.g., 'rpc_call', 'permission_denied')
            **kwargs: Additional event details
        """
        event={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event_type,
            **kwargs,
        }

        # Redact sensitive data
        _event_str=self._redact_sensitive(json.dumps(event))

        self.logger.info(event_str)

    @staticmethod
    def _redact_sensitive(jsonstr: str) -> str:
        """Redact sensitive fields from JSON string"""
        # Simple redaction - replace sensitive field values
        sensitive_fields=["password", "token", "key", "secret", "api_key"]

        for field in sensitive_fields:
        # Match "fieldname": "value" and replace value with ***
            pattern=f'"{field}": "[^"]*"'
            json_str=re.sub(
                pattern, f'"{field}": "***"', json_str, flags=re.IGNORECASE
            )

        return json_str


class AuditInterceptor(grpc.ServerInterceptor):
    """
    Intercept RPC calls for audit logging.

    Logs:
    - RPC call start (principal, service, method)
    - RPC call result (success/error)
    - Authorization failures
    - Rate limit violations
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize audit interceptor.

        Args:
            config: Configuration dict with audit_log_file path
        """
        _audit_log_file=config.get("audit_log_file", "/var/log/debvisor/rpc-audit.log")
        self.audit=AuditLogger(audit_log_file)
        logger.info("AuditInterceptor initialized")

    def intercept_service(
        self,
        continuation: Callable[[grpc.HandlerCallDetails], Any],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Any:
        """
        Intercept RPC call and log audit events.

        Args:
            continuation: Handler to call
            handler_call_details: Details about RPC call

        Returns:
            Handler response
        """
        # Extract service and method
        service, method=self._extract_service_method(handler_call_details)

        # Get principal from context (set by AuthenticationInterceptor)
        principal="unknown"
        auth_method=None

        try:
            from auth import extract_identity

            _identity=extract_identity(handler_call_details.context)
            if identity:
                principal=identity.principal_id
                _auth_method=identity.auth_method
        except BaseException:
            pass

        # Log RPC call
        self.audit.log_event(
            "rpc_call",
            _principal=principal,
            _service=service,
            _method=method,
            _auth_method=auth_method,
        )

        # Wrap handler to log result

        def logged_handler(request: Any) -> Any:
            try:
            # Execute handler
                _response=continuation(handler_call_details)

                # Log success
                self.audit.log_event(
                    "rpc_success",
                    _principal=principal,
                    _service=service,
                    _method=method,
                )

                return response

            except grpc.RpcError as e:
            # Log gRPC error
                self.audit.log_event(
                    "rpc_error",
                    _principal=principal,
                    _service=service,
                    _method=method,
                    _error_code=str(e.code()),
                    _error_details=e.details(),
                )
                raise

            except Exception as e:
            # Log unexpected error
                self.audit.log_event(
                    "rpc_error",
                    _principal=principal,
                    _service=service,
                    _method=method,
                    _error=str(e),
                )
                raise

        return logged_handler

    @staticmethod
    def _extract_service_method(
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Tuple[str, str]:
        """
        Extract service and method from RPC path.

        Path format: /package.Service/Method
        Example: /debvisor.v1.NodeService/RegisterNode

        Args:
            handler_call_details: RPC call details

        Returns:
            Tuple of (service, method)
        """
        try:
        # Get the full method path from handler_call_details
            _full_method=getattr(handler_call_details, "method", "")

            if full_method:
            # Format: /package.Service/Method
                _parts=full_method.split("/")
                if len(parts) >= 2:
                    _service=parts[-2].split(".")[-1]    # Last component of service path
                    method=parts[-1]
                    return service, method
        except BaseException:
            pass

        return "unknown", "unknown"


if _name__== "__main__":
    # Test validators
    logging.basicConfig(level=logging.DEBUG)

    print("Testing RequestValidator:")

    # Test hostname
    try:
        print(
            f'Valid hostname: {RequestValidator.validate_hostname("node-01.example.com")}'
        )
    except ValueError as e:
        print(f"Invalid hostname: {e}")

    # Test IPv4
    try:
        print(f'Valid IPv4: {RequestValidator.validate_ipv4("192.168.1.1")}')
    except ValueError as e:
        print(f"Invalid IPv4: {e}")

    # Test UUID
    try:
        print(
            f'Valid UUID: {RequestValidator.validate_uuid("550e8400-e29b-41d4-a716-446655440000")}'
        )
    except ValueError as e:
        print(f"Invalid UUID: {e}")

    # Test MAC
    try:
        print(
            f'Valid MAC: {RequestValidator.validate_mac_address("aa:bb:cc:dd:ee:ff")}'
        )
    except ValueError as e:
        print(f"Invalid MAC: {e}")

    # Test audit logger
    print("\nTesting AuditLogger:")
    _audit=AuditLogger("/tmp/test-audit.log")    # nosec B108
    audit.log_event("test_event", principal="test-user", action="test_action")
    print("Audit event logged to /tmp/test-audit.log")
