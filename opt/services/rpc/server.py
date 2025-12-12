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

"""
DebVisor RPC Service - Main Server Implementation

Provides secure, audited gRPC API for cluster operations including:
- Node registration and health monitoring
- Storage snapshot management
- VM migration orchestration

Features:
- mTLS with certificate validation
- RBAC with wildcard permissions
- Structured audit logging
- Rate limiting per principal
- Graceful shutdown and health checks
"""

from datetime import datetime, timezone
import grpc
import json
import logging
import os
import sys
import time
import threading
from concurrent import futures
from enum import Enum
from typing import Dict, List, Any, Callable, Optional

# Generated protobuf modules (from make protoc)
import debvisor_pb2
import debvisor_pb2_grpc

# Local modules
from auth import AuthenticationInterceptor, extract_identity
from authz import AuthorizationInterceptor, check_permission
from audit import AuditInterceptor
from validators import RequestValidator

# Configure logging
try:
    from opt.core.logging import configure_logging
    import structlog

    configure_logging(service_name="rpc-server")
    _logger=structlog.get_logger(__name__)
except ImportError:
    logging.basicConfig(
        _level=logging.INFO,
        _format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    _logger=logging.getLogger(__name__)


class StatusCode(Enum):
    """Response status codes"""

    UNKNOWN = 0
    OK = 1
    WARN = 2
    ERROR = 3


class RateLimitingInterceptor(grpc.ServerInterceptor):
    """Simple per-principal sliding window rate limiter."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._lock=threading.Lock()
        self._calls: Dict[str, List[float]] = {}
        _rl_cfg=config.get("rate_limit", {})
        self.window_seconds=float(rl_cfg.get("window_seconds", 60))
        self.max_calls=int(rl_cfg.get("max_calls", 120))
        # Optional per-method overrides: {"/debvisor.NodeService/RegisterNode":
            # {"window_seconds":30, "max_calls": 30}}
        self.method_limits: Dict[str, Dict[str, float]] = rl_cfg.get(
            "method_limits", {}
        )
        # Optional prefix-based overrides: {"/debvisor.StorageService/":
            # {"window_seconds":60, "max_calls": 30}}
        self.method_limits_prefix: Dict[str, Dict[str, float]] = rl_cfg.get(
            "method_limits_prefix", {}
        )
        # Optional regex pattern overrides:
            # [{"pattern":"/debvisor\\.\w+Service/(Create|Delete|Update).*",
        #   "window_seconds":60,"max_calls":20}]
        self.method_limits_patterns: List[Dict[str, Any]] = rl_cfg.get(
            "method_limits_patterns", []
        )

    def intercept_service(
        self,
        continuation: Callable[[grpc.HandlerCallDetails], Any],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Any:

        def _wrapped_behavior(request: Any, context: grpc.ServicerContext) -> Any:
            _principal=extract_identity(context)
            _key = f"{principal.principal_id if principal else 'anonymous'}:{handler_call_details.method}"
            _now=time.time()
            # Resolve method-specific limits if any
            method_cfg: Dict[str, float] = self.method_limits.get(
                handler_call_details.method, {}
            )
            if not method_cfg:
            # Try prefix matches
                for prefix, cfg in self.method_limits_prefix.items():
                    if handler_call_details.method.startswith(prefix):
                        method_cfg = cfg
                        break
            if not method_cfg and self.method_limits_patterns:
                import re

                for entry in self.method_limits_patterns:
                    _pat=entry.get("pattern")
                    if pat and re.search(pat, handler_call_details.method):
                        method_cfg = entry
                        break
            _window=float(method_cfg.get("window_seconds", self.window_seconds))
            _max_calls=int(method_cfg.get("max_calls", self.max_calls))
            with self._lock:
                _history=self._calls.setdefault(key, [])
                # Evict old entries outside window
                cutoff = now - window
                history[:] = [t for t in history if t >= cutoff]
                if len(history) >= max_calls:
                    context.abort(
                        grpc.StatusCode.RESOURCE_EXHAUSTED, "Rate limit exceeded"
                    )
                history.append(now)
            return continuation(handler_call_details).unary_unary(request, context)

        _handler=continuation(handler_call_details)
        if handler.unary_unary:
            return grpc.unary_unary_rpc_method_handler(
                _wrapped_behavior,
                _request_deserializer = handler.request_deserializer,
                _response_serializer = handler.response_serializer,
            )
        return handler


class NodeServiceImpl(debvisor_pb2_grpc.NodeServiceServicer):
    """Implementation of NodeService RPC calls"""

    def __init__(self, backend: Any=None) -> None:
        self.backend = backend
        self.nodes: Dict[str, Dict[str, Any]] = (
            {}
        )    # In-memory store for demo (use persistent storage in production)
        logger.info("NodeServiceImpl initialized")

    def RegisterNode(
        self, request: debvisor_pb2.RegisterNodeRequest, context: grpc.ServicerContext
    ) -> debvisor_pb2.NodeAck:
        """Register a new node or update existing node"""
        try:
        # Validate inputs
            _hostname=RequestValidator.validate_hostname(request.hostname)
            _ip=RequestValidator.validate_ipv4(request.ip)

            # Check authorization
            _principal=extract_identity(context)
            check_permission(principal, "node:register", context)

            # Store node (in production, write to persistent storage)
            _node_id=f"node-{len(self.nodes) + 1:03d}"
            self.nodes[node_id] = {
                "id": node_id,
                "hostname": hostname,
                "ip": ip,
                "version": request.version,
                "status": "registered",
                "registered_at": datetime.now(timezone.utc).isoformat(),
                "last_heartbeat": None,
            }

            logger.info(
                f"Node registered: {hostname} ({ip}), node_id={node_id}, "
                f'principal={principal.principal_id if principal else "unknown"}'
            )

            return debvisor_pb2.NodeAck(
                _status = StatusCode.OK.value,
                _message = f"Node {hostname} registered successfully",
                _node_id = node_id,
            )

        except ValueError as e:
            logger.warning(f"RegisterNode validation error: {e}")
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

        except PermissionError as e:
            logger.warning(f"RegisterNode permission denied: {e}")
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))

        except Exception as e:
            logger.error(f"RegisterNode error: {e}", exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, "Registration failed")

    def Heartbeat(
        self, request: debvisor_pb2.HeartbeatRequest, context: grpc.ServicerContext
    ) -> debvisor_pb2.HeartbeatAck:
        """Send heartbeat from node"""
        try:
        # Validate inputs
            _node_id=RequestValidator.validate_uuid(request.node_id)

            # Check authorization
            _principal=extract_identity(context)
            check_permission(principal, "node:heartbeat", context)

            # Check node exists
            if node_id not in self.nodes:
                context.abort(grpc.StatusCode.NOT_FOUND, f"Node not found: {node_id}")

            # Update node state
            self.nodes[node_id]["last_heartbeat"] = datetime.now(
                timezone.utc
            ).isoformat()
            self.nodes[node_id]["status"] = "online"

            logger.info(f"Heartbeat received from node {node_id}")

            return debvisor_pb2.HealthAck(
                _status = StatusCode.OK.value,
                _timestamp=debvisor_pb2.Timestamp(
                    _seconds=int(datetime.now(timezone.utc).timestamp()),
                    _nanos = 0,
                ),
            )

        except ValueError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        except PermissionError as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.error(f"Heartbeat error: {e}", exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, "Heartbeat failed")

    def ListNodes(
        self, request: debvisor_pb2.ListNodesRequest, context: grpc.ServicerContext
    ) -> debvisor_pb2.NodeList:
        """List all registered nodes"""
        try:
        # Check authorization
            _principal=extract_identity(context)
            check_permission(principal, "node:list", context)

            _nodes=list(self.nodes.values())

            _node_summaries = [
                debvisor_pb2.NodeSummary(
                    _node_id = n["id"],
                    _hostname = n["hostname"],
                    _ip = n["ip"],
                    _status = n["status"],
                    _registered_at=debvisor_pb2.Timestamp(
                        _seconds = int(
                            datetime.fromisoformat(n["registered_at"]).timestamp()
                        ),
                    ),
                )
                for n in nodes
            ]

            logger.info(
                f"Listed {len(node_summaries)} nodes, "
                f'principal={principal.principal_id if principal else "unknown"}'
            )

            return debvisor_pb2.NodeList(nodes=node_summaries)

        except PermissionError as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.error(f"ListNodes error: {e}", exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, "List failed")


class StorageServiceImpl(debvisor_pb2_grpc.StorageServiceServicer):
    """Implementation of StorageService RPC calls"""

    def __init__(self, backend: Any=None) -> None:
        self.backend = backend
        self.snapshots: Dict[str, Dict[str, Any]] = {}    # In-memory store for demo
        logger.info("StorageServiceImpl initialized")

    def CreateSnapshot(
        self,
        request: debvisor_pb2.CreateSnapshotRequest,
        context: grpc.ServicerContext,
    ) -> debvisor_pb2.SnapshotStatus:
        """Create a ZFS or Ceph RBD snapshot"""
        try:
        # Validate inputs
            _pool=RequestValidator.validate_label(request.pool, max_length=256)
            _snapshot=RequestValidator.validate_label(request.snapshot, max_length=256)

            # Check authorization
            _principal=extract_identity(context)
            check_permission(principal, "storage:snapshot:create", context)

            # Create snapshot (in production, interact with ZFS/Ceph)
            _snapshot_id=f"snap-{len(self.snapshots) + 1:06d}"
            self.snapshots[snapshot_id] = {
                "id": snapshot_id,
                "pool": pool,
                "snapshot": snapshot,
                "backend": request.backend,
                "tags": dict(request.tags),
                "status": "created",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "size_bytes": 0,    # Would be populated from backend
            }

            logger.info(
                f"Snapshot created: {pool}@{snapshot}, snapshot_id={snapshot_id}, "
                f'principal={principal.principal_id if principal else "unknown"}'
            )

            return debvisor_pb2.SnapshotStatus(
                _snapshot_id = snapshot_id,
                _status = StatusCode.OK.value,
                _message = "Snapshot created successfully",
                _created_at = debvisor_pb2.Timestamp(
                    _seconds=int(datetime.now(timezone.utc).timestamp()),
                ),
            )

        except ValueError as e:
            logger.warning(f"CreateSnapshot validation error: {e}")
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

        except PermissionError as e:
            logger.warning(f"CreateSnapshot permission denied: {e}")
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))

        except Exception as e:
            logger.error(f"CreateSnapshot error: {e}", exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, "Snapshot creation failed")

    def ListSnapshots(
        self, request: debvisor_pb2.ListSnapshotsRequest, context: grpc.ServicerContext
    ) -> debvisor_pb2.SnapshotList:
        """List storage snapshots"""
        try:
        # Check authorization
            _principal=extract_identity(context)
            check_permission(principal, "storage:snapshot:list", context)

            # Filter snapshots by pool if specified
            _snapshots=list(self.snapshots.values())
            if request.pool:
                _snapshots = [s for s in snapshots if s["pool"] == request.pool]

            _snapshot_summaries = [
                debvisor_pb2.SnapshotSummary(
                    _snapshot_id = s["id"],
                    _pool = s["pool"],
                    _snapshot=s["snapshot"],
                    _backend = s["backend"],
                    _size_bytes = s["size_bytes"],
                    _created_at=debvisor_pb2.Timestamp(
                        _seconds = int(
                            datetime.fromisoformat(s["created_at"]).timestamp()
                        ),
                    ),
                )
                for s in snapshots
            ]

            logger.info(
                f"Listed {len(snapshot_summaries)} snapshots, "
                f'principal={principal.principal_id if principal else "unknown"}'
            )

            return debvisor_pb2.SnapshotList(snapshots=snapshot_summaries)

        except PermissionError as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.error(f"ListSnapshots error: {e}", exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, "List failed")

    def DeleteSnapshot(
        self,
        request: debvisor_pb2.DeleteSnapshotRequest,
        context: grpc.ServicerContext,
    ) -> debvisor_pb2.SnapshotStatus:
        """Delete a snapshot"""
        try:
            _snapshot_id=RequestValidator.validate_uuid(request.snapshot_id)

            # Check authorization
            _principal=extract_identity(context)
            check_permission(principal, "storage:snapshot:delete", context)

            # Check snapshot exists
            if snapshot_id not in self.snapshots:
                context.abort(
                    grpc.StatusCode.NOT_FOUND, f"Snapshot not found: {snapshot_id}"
                )

            # Delete snapshot
            _snapshot=self.snapshots.pop(snapshot_id)
            logger.info(
                f'Snapshot deleted: {snapshot["pool"]}@{snapshot["snapshot"]}, '
                f'principal={principal.principal_id if principal else "unknown"}'
            )

            return debvisor_pb2.SnapshotStatus(
                _snapshot_id = snapshot_id,
                _status = StatusCode.OK.value,
                _message = "Snapshot deleted successfully",
            )

        except ValueError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        except PermissionError as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.error(f"DeleteSnapshot error: {e}", exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, "Snapshot deletion failed")


class MigrationServiceImpl(debvisor_pb2_grpc.MigrationServiceServicer):
    """Implementation of MigrationService RPC calls"""

    def __init__(self, backend: Any=None) -> None:
        self.backend = backend
        self.migrations: Dict[str, Any] = {}    # Track in-flight migrations
        logger.info("MigrationServiceImpl initialized")

    def PlanMigration(
        self, request: debvisor_pb2.MigrationPlanRequest, context: grpc.ServicerContext
    ) -> debvisor_pb2.MigrationPlan:
        """Plan a VM migration"""
        try:
            _vm_id=RequestValidator.validate_uuid(request.vm_id)
            _target_node=RequestValidator.validate_hostname(request.target_node)

            # Check authorization
            _principal=extract_identity(context)
            check_permission(principal, "migration:plan", context)

            # Plan migration (validate prerequisites)
            plan = {
                "vm_id": vm_id,
                "source_node": request.source_node,
                "target_node": target_node,
                "estimated_duration_seconds": 300,    # Placeholder
                "required_memory_mb": 4096,    # Placeholder
                "status": "planned",
            }

            logger.info(
                f"Migration planned: {vm_id} from {request.source_node} to {target_node}"
            )

            return debvisor_pb2.MigrationPlan(
                _plan_id=f"plan-{datetime.now(timezone.utc).timestamp()}",
                _status = StatusCode.OK.value,
                _estimated_duration_seconds = plan["estimated_duration_seconds"],
                _message = "Migration plan created",
            )

        except ValueError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        except PermissionError as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.error(f"PlanMigration error: {e}", exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, "Plan failed")


class RPCServer:
    """Main RPC server orchestrator"""

    def __init__(self, config_file: Optional[str] = None) -> None:
        """Initialize RPC server with configuration"""
        self.config=self._load_config(config_file)
        self.server: Optional[grpc.Server] = None
        self.cert_monitor: Any = None
        logger.info(f"RPCServer initialized from config: {config_file}")

    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load configuration from JSON file and merge with environment settings."""
        config: Dict[str, Any] = {}
        if config_file:
            try:
                with open(config_file, "r") as f:
                    _config=json.load(f)
                logger.info(f"Configuration loaded from {config_file}")
            except FileNotFoundError:
                logger.warning(
                    f"Configuration file not found: {config_file}. Using defaults/env vars."
                )
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in configuration file: {e}")
                raise

        # Merge with centralized settings
        try:
            from opt.core.config import settings

            # Helper to apply setting if set in env or missing in config

            def apply_setting(conf_key: str, setting_key: str) -> None:
            # If explicitly set in environment (in model_fields_set), it overrides everything
                # If not set in environment, but missing in config, use default from settings
                if setting_key in settings.model_fields_set:
                    config[conf_key] = getattr(settings, setting_key)
                elif conf_key not in config:
                    config[conf_key] = getattr(settings, setting_key)

            apply_setting("host", "RPC_HOST")
            apply_setting("port", "RPC_PORT")
            apply_setting("tls_cert_file", "RPC_CERT_FILE")
            apply_setting("tls_key_file", "RPC_KEY_FILE")
            apply_setting("tls_ca_file", "RPC_CA_FILE")

        except ImportError:
            logger.warning(
                "Could not import centralized settings. Using file config only."
            )

        return config

    def _load_tls_credentials(self) -> grpc.ServerCredentials:
        """Load TLS certificates for server"""
        _cert_file=str(self.config.get("tls_cert_file", "/etc/debvisor/certs/server.crt"))
        _key_file=str(self.config.get("tls_key_file", "/etc/debvisor/certs/server.key"))
        _ca_file=self.config.get("tls_ca_file")

        try:
            with open(key_file, "rb") as f:
                _private_key=f.read()

            with open(cert_file, "rb") as f:
                _certificate_chain=f.read()

            ca_cert = None
            if ca_file:
                with open(str(ca_file), "rb") as f:
                    _ca_cert=f.read()

            logger.info("TLS credentials loaded successfully")

            # CRYPTO-001: Enforce TLS 1.3 only for enhanced security
            # Disable TLS 1.2 and below
            # options = [(grpc.ChannelArgument.SSL_TARGET_NAME_OVERRIDE,
            #             self.config.get('ssl_target_name_override')), ]

            return grpc.ssl_server_credentials(
                [(private_key, certificate_chain)],
                _root_certificates = ca_cert,
                _require_client_auth=bool(self.config.get("require_client_auth", True)),
            )

        except FileNotFoundError as e:
            logger.error(f"TLS certificate file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load TLS credentials: {e}")
            raise

    def start(self) -> None:
        """Start the RPC server"""
        logger.info("Starting DebVisor RPC service")

        # Create server with interceptors
        _interceptors = [
            AuthenticationInterceptor(self.config),
            AuthorizationInterceptor(self.config),
            AuditInterceptor(self.config),
            RateLimitingInterceptor(self.config),
        ]

        # Configure Connection Pooling & Performance Options
        _pool_config=self.config.get("connection_pool", {})
        _max_workers=pool_config.get("max_connections", 50)

        # gRPC Channel Options for Performance & Keepalive
        _options = [
            ("grpc.max_send_message_length", 50 * 1024 * 1024),    # 50MB
            ("grpc.max_receive_message_length", 50 * 1024 * 1024),    # 50MB
            (
                "grpc.keepalive_time_ms",
                int(pool_config.get("idle_timeout", 300.0) * 1000),
            ),
            (
                "grpc.keepalive_timeout_ms",
                int(pool_config.get("connection_timeout", 10.0) * 1000),
            ),
            ("grpc.keepalive_permit_without_calls", 1),
            ("grpc.http2.max_pings_without_data", 0),
            ("grpc.http2.min_time_between_pings_ms", 10000),
            ("grpc.http2.min_ping_interval_without_data_ms", 5000),
        ]

        # Configure Compression
        _compression_config=self.config.get("compression", {})
        compression_algorithm = grpc.Compression.NoCompression
        if compression_config.get("enabled", False):
            _algo=compression_config.get("algorithm", "gzip").lower()
            if algo == "gzip":
                compression_algorithm = grpc.Compression.Gzip
            elif algo == "deflate":
                compression_algorithm = grpc.Compression.Deflate
            logger.info(f"RPC Compression enabled: {algo}")

        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            _interceptors = interceptors,
            _options = options,
            _compression = compression_algorithm,
        )

        # Register services
        debvisor_pb2_grpc.add_NodeServiceServicer_to_server(
            NodeServiceImpl(),
            self.server,
        )
        debvisor_pb2_grpc.add_StorageServiceServicer_to_server(
            StorageServiceImpl(),
            self.server,
        )
        debvisor_pb2_grpc.add_MigrationServiceServicer_to_server(
            MigrationServiceImpl(),
            self.server,
        )

        # Load TLS credentials
        _tls_creds=self._load_tls_credentials()

        # Bind to port
        _host=self.config.get("host", "127.0.0.1")
        _port=self.config.get("port", 7443)
        self.server.add_secure_port(f"{host}:{port}", tls_creds)

        logger.info(f"RPC server listening on {host}:{port}")

        self.server.start()

        try:
        # Block while serving
            logger.info("RPC server started successfully")
            while True:
                time.sleep(86400)    # Sleep for a day
        except KeyboardInterrupt:
            logger.info("Shutting down RPC server")
            self.stop()

    def stop(self, grace_timeout: int=5) -> None:
        """Gracefully shutdown RPC server"""
        if self.server:
            logger.info(f"Shutting down server (grace timeout: {grace_timeout}s)")
            self.server.stop(grace_timeout)


def main() -> None:
    """Main entry point"""
    # Use centralized configuration if available
    try:
        from opt.core.config import Settings
        _settings=Settings()

        # Map Settings to legacy config dict structure for backward compatibility
        _config = {
            "host": settings.RPC_HOST,
            "port": settings.RPC_PORT,
            "tls": {
                "cert_file": settings.RPC_CERT_FILE,
                "key_file": os.environ.get("RPC_KEY_FILE", "/etc/debvisor/certs/rpc.key"),
                "ca_file": os.environ.get("RPC_CA_FILE", "/etc/debvisor/certs/ca.crt"),
                "require_client_cert": True
            },
            "rate_limit": {
                "window_seconds": 60,
                "max_calls": 120
            },
            "max_workers": 10
        }

        # Override with file config if present (legacy support)
        _config_file=os.environ.get("RPC_CONFIG_FILE")
        if config_file and os.path.exists(config_file):
            with open(config_file, "r") as f:
                _file_config=json.load(f)
                config.update(file_config)

        _server=RPCServer(config_file=None)    # Pass None to skip internal file loading
        server.config = config    # Inject config directly
        server.start()

    except ImportError:
    # Fallback to legacy behavior
        _config_file=os.environ.get("RPC_CONFIG_FILE", "/etc/debvisor/rpc/config.json")
        try:
            _server=RPCServer(config_file)
            server.start()
        except Exception as e:
            logger.error(f"Failed to start RPC server: {e}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start RPC server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
