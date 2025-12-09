#!/usr/bin/env python3
"""
RPC Audit Logging.

Implements gRPC interceptor for audit logging using the core audit system.
Persists signed audit entries to a log file.
"""

import grpc
import logging
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Callable

from opt.core.audit import AuditSigner, AuditLogger, AuditEntry

logger = logging.getLogger(__name__)


class FileAuditPersistence:
    """Persists audit entries to a file."""

    def __init__(self, log_path: str):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def write(self, entry: AuditEntry) -> None:
        """Write entry to log file."""
        try:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(entry.to_dict()) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")


class RPCAuditLogger(AuditLogger):
    """RPC-specific audit logger with persistence."""

    def __init__(self, signer: AuditSigner, persistence: FileAuditPersistence):
        super().__init__(signer)
        self.persistence = persistence
        self.last_hash = None

        # Try to read last hash from file
        try:
            if os.path.exists(persistence.log_path):
                with open(persistence.log_path, "r") as f:
                    lines = f.readlines()
                    if lines:
                        last_entry = json.loads(lines[-1])
                        self.last_hash = last_entry.get("signature")
        except Exception:
            pass

    def log_rpc_call(
        self, method: str, principal: str, status: str, details: Dict[str, Any]
    ) -> None:
        """Log an RPC call."""
        entry = self.create_entry(
            operation="execute",
            resource_type="rpc",
            resource_id=method,
            actor_id=principal,
            action=f"RPC Call: {method}",
            status=status,
            details=details,
            previous_hash=self.last_hash or "0" * 64,
        )

        self.persistence.write(entry)
        self.last_hash = entry.signature


class AuditInterceptor(grpc.ServerInterceptor):
    """
    Intercept RPC calls for audit logging.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        log_file = config.get("audit_log_file", "/var/log/debvisor/rpc-audit.log")
        
        # In production, SECRET_KEY must be set in environment
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            if os.getenv("FLASK_ENV") == "production":
                raise ValueError("SECRET_KEY not set in production environment")
            secret_key = "dev-key"
            
        signer = AuditSigner(secret_key=secret_key)
        persistence = FileAuditPersistence(log_file)
        self.audit = RPCAuditLogger(signer, persistence)
        logger.info(f"AuditInterceptor initialized (log: {log_file})")

    def intercept_service(
        self,
        continuation: Callable[[grpc.HandlerCallDetails], Any],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Any:
        method = handler_call_details.method
        start_time = datetime.now(timezone.utc)

        # Extract principal (placeholder - needs integration with auth context)
        principal = "anonymous"
        # In a real scenario, we'd extract this from context, but intercept_service
        # doesn't give easy access to context before calling continuation.
        # We might need to wrap the behavior.

        def _wrapped_behavior(request: Any, context: grpc.ServicerContext) -> Any:
            # Extract identity from context if available
            # This depends on AuthInterceptor running before this one
            # or we can try to extract metadata here.
            nonlocal principal
            try:
                from opt.services.rpc.auth import extract_identity

                identity = extract_identity(context)
                if identity:
                    principal = identity.principal_id
            except ImportError:
                pass
            except Exception:
                pass

            status = "success"
            error_details = None

            try:
                response = continuation(handler_call_details)(request, context)
                return response
            except Exception as e:
                status = "failure"
                error_details = str(e)
                raise
            finally:
                # Log the call
                duration = (
                    datetime.now(timezone.utc) - start_time
                ).total_seconds() * 1000
                details = {"duration_ms": duration, "error": error_details}
                self.audit.log_rpc_call(method, principal, status, details)

        return grpc.unary_unary_rpc_method_handler(
            _wrapped_behavior,
            request_deserializer=handler_call_details.method_handlers[
                handler_call_details.method
            ].request_deserializer,
            response_serializer=handler_call_details.method_handlers[
                handler_call_details.method
            ].response_serializer,
        )
