#!/usr/bin/env python3
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

import grpc
import json
import logging
import os
import sys
import time
import threading
from concurrent import futures
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Dict, List, Optional

# Generated protobuf modules (from make protoc)
import debvisor_pb2
import debvisor_pb2_grpc

# Local modules
from auth import AuthenticationInterceptor, extract_identity
from authz import AuthorizationInterceptor, check_permission
from audit import AuditInterceptor
from validators import RequestValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)
logger = logging.getLogger(__name__)


class StatusCode(Enum):
    """Response status codes"""
    UNKNOWN = 0
    OK = 1
    WARN = 2
    ERROR = 3


class NodeServiceImpl(debvisor_pb2_grpc.NodeServiceServicer):
    """Implementation of NodeService RPC calls"""
    
    def __init__(self, backend=None):
        self.backend = backend
        self.nodes = {}  # In-memory store for demo (use persistent storage in production)
        logger.info('NodeServiceImpl initialized')
    
    def RegisterNode(self, request, context):
        """Register a new node or update existing node"""
        try:
            # Validate inputs
            hostname = RequestValidator.validate_hostname(request.hostname)
            ip = RequestValidator.validate_ipv4(request.ip)
            
            # Check authorization
            principal = extract_identity(context)
            check_permission(principal, 'node:register', context)
            
            # Store node (in production, write to persistent storage)
            node_id = f"node-{len(self.nodes) + 1:03d}"
            self.nodes[node_id] = {
                'id': node_id,
                'hostname': hostname,
                'ip': ip,
                'version': request.version,
                'status': 'registered',
                'registered_at': datetime.now(timezone.utc).isoformat(),
                'last_heartbeat': None,
            }
            
            logger.info(
                f'Node registered: {hostname} ({ip}), node_id={node_id}, '
                f'principal={principal.principal_id if principal else "unknown"}'
            )
            
            return debvisor_pb2.NodeAck(
                status=StatusCode.OK.value,
                message=f'Node {hostname} registered successfully',
                node_id=node_id,
            )
        
        except ValueError as e:
            logger.warning(f'RegisterNode validation error: {e}')
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        
        except PermissionError as e:
            logger.warning(f'RegisterNode permission denied: {e}')
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        
        except Exception as e:
            logger.error(f'RegisterNode error: {e}', exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, 'Registration failed')
    
    def Heartbeat(self, request, context):
        """Send heartbeat from node"""
        try:
            # Validate inputs
            node_id = RequestValidator.validate_uuid(request.node_id)
            
            # Check authorization
            principal = extract_identity(context)
            check_permission(principal, 'node:heartbeat', context)
            
            # Check node exists
            if node_id not in self.nodes:
                context.abort(grpc.StatusCode.NOT_FOUND, f'Node not found: {node_id}')
            
            # Update node state
            self.nodes[node_id]['last_heartbeat'] = datetime.now(timezone.utc).isoformat()
            self.nodes[node_id]['status'] = 'online'
            
            logger.info(f'Heartbeat received from node {node_id}')
            
            return debvisor_pb2.HealthAck(
                status=StatusCode.OK.value,
                timestamp=debvisor_pb2.Timestamp(
                    seconds=int(datetime.now(timezone.utc).timestamp()),
                    nanos=0,
                ),
            )
        
        except ValueError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        except PermissionError as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.error(f'Heartbeat error: {e}', exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, 'Heartbeat failed')
    
    def ListNodes(self, request, context):
        """List all registered nodes"""
        try:
            # Check authorization
            principal = extract_identity(context)
            check_permission(principal, 'node:list', context)
            
            nodes = list(self.nodes.values())
            
            node_summaries = [
                debvisor_pb2.NodeSummary(
                    node_id=n['id'],
                    hostname=n['hostname'],
                    ip=n['ip'],
                    status=n['status'],
                    registered_at=debvisor_pb2.Timestamp(
                        seconds=int(
                            datetime.fromisoformat(n['registered_at']).timestamp()
                        ),
                    ),
                )
                for n in nodes
            ]
            
            logger.info(f'Listed {len(node_summaries)} nodes, principal={principal.principal_id if principal else "unknown"}')
            
            return debvisor_pb2.NodeList(nodes=node_summaries)
        
        except PermissionError as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.error(f'ListNodes error: {e}', exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, 'List failed')


class StorageServiceImpl(debvisor_pb2_grpc.StorageServiceServicer):
    """Implementation of StorageService RPC calls"""
    
    def __init__(self, backend=None):
        self.backend = backend
        self.snapshots = {}  # In-memory store for demo
        logger.info('StorageServiceImpl initialized')
    
    def CreateSnapshot(self, request, context):
        """Create a ZFS or Ceph RBD snapshot"""
        try:
            # Validate inputs
            pool = RequestValidator.validate_label(request.pool, max_length=256)
            snapshot = RequestValidator.validate_label(request.snapshot, max_length=256)
            
            # Check authorization
            principal = extract_identity(context)
            check_permission(principal, 'storage:snapshot:create', context)
            
            # Create snapshot (in production, interact with ZFS/Ceph)
            snapshot_id = f"snap-{len(self.snapshots) + 1:06d}"
            self.snapshots[snapshot_id] = {
                'id': snapshot_id,
                'pool': pool,
                'snapshot': snapshot,
                'backend': request.backend,
                'tags': dict(request.tags),
                'status': 'created',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'size_bytes': 0,  # Would be populated from backend
            }
            
            logger.info(
                f'Snapshot created: {pool}@{snapshot}, snapshot_id={snapshot_id}, '
                f'principal={principal.principal_id if principal else "unknown"}'
            )
            
            return debvisor_pb2.SnapshotStatus(
                snapshot_id=snapshot_id,
                status=StatusCode.OK.value,
                message='Snapshot created successfully',
                created_at=debvisor_pb2.Timestamp(
                    seconds=int(datetime.now(timezone.utc).timestamp()),
                ),
            )
        
        except ValueError as e:
            logger.warning(f'CreateSnapshot validation error: {e}')
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        
        except PermissionError as e:
            logger.warning(f'CreateSnapshot permission denied: {e}')
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        
        except Exception as e:
            logger.error(f'CreateSnapshot error: {e}', exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, 'Snapshot creation failed')
    
    def ListSnapshots(self, request, context):
        """List storage snapshots"""
        try:
            # Check authorization
            principal = extract_identity(context)
            check_permission(principal, 'storage:snapshot:list', context)
            
            # Filter snapshots by pool if specified
            snapshots = list(self.snapshots.values())
            if request.pool:
                snapshots = [s for s in snapshots if s['pool'] == request.pool]
            
            snapshot_summaries = [
                debvisor_pb2.SnapshotSummary(
                    snapshot_id=s['id'],
                    pool=s['pool'],
                    snapshot=s['snapshot'],
                    backend=s['backend'],
                    size_bytes=s['size_bytes'],
                    created_at=debvisor_pb2.Timestamp(
                        seconds=int(
                            datetime.fromisoformat(s['created_at']).timestamp()
                        ),
                    ),
                )
                for s in snapshots
            ]
            
            logger.info(
                f'Listed {len(snapshot_summaries)} snapshots, '
                f'principal={principal.principal_id if principal else "unknown"}'
            )
            
            return debvisor_pb2.SnapshotList(snapshots=snapshot_summaries)
        
        except PermissionError as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.error(f'ListSnapshots error: {e}', exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, 'List failed')
    
    def DeleteSnapshot(self, request, context):
        """Delete a snapshot"""
        try:
            snapshot_id = RequestValidator.validate_uuid(request.snapshot_id)
            
            # Check authorization
            principal = extract_identity(context)
            check_permission(principal, 'storage:snapshot:delete', context)
            
            # Check snapshot exists
            if snapshot_id not in self.snapshots:
                context.abort(grpc.StatusCode.NOT_FOUND, 
                            f'Snapshot not found: {snapshot_id}')
            
            # Delete snapshot
            snapshot = self.snapshots.pop(snapshot_id)
            logger.info(
                f'Snapshot deleted: {snapshot["pool"]}@{snapshot["snapshot"]}, '
                f'principal={principal.principal_id if principal else "unknown"}'
            )
            
            return debvisor_pb2.SnapshotStatus(
                snapshot_id=snapshot_id,
                status=StatusCode.OK.value,
                message='Snapshot deleted successfully',
            )
        
        except ValueError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        except PermissionError as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.error(f'DeleteSnapshot error: {e}', exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, 'Snapshot deletion failed')


class MigrationServiceImpl(debvisor_pb2_grpc.MigrationServiceServicer):
    """Implementation of MigrationService RPC calls"""
    
    def __init__(self, backend=None):
        self.backend = backend
        self.migrations = {}  # Track in-flight migrations
        logger.info('MigrationServiceImpl initialized')
    
    def PlanMigration(self, request, context):
        """Plan a VM migration"""
        try:
            vm_id = RequestValidator.validate_uuid(request.vm_id)
            target_node = RequestValidator.validate_hostname(request.target_node)
            
            # Check authorization
            principal = extract_identity(context)
            check_permission(principal, 'migration:plan', context)
            
            # Plan migration (validate prerequisites)
            plan = {
                'vm_id': vm_id,
                'source_node': request.source_node,
                'target_node': target_node,
                'estimated_duration_seconds': 300,  # Placeholder
                'required_memory_mb': 4096,  # Placeholder
                'status': 'planned',
            }
            
            logger.info(f'Migration planned: {vm_id} from {request.source_node} to {target_node}')
            
            return debvisor_pb2.MigrationPlan(
                plan_id=f"plan-{datetime.now(timezone.utc).timestamp()}",
                status=StatusCode.OK.value,
                estimated_duration_seconds=plan['estimated_duration_seconds'],
                message='Migration plan created',
            )
        
        except ValueError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        except PermissionError as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.error(f'PlanMigration error: {e}', exc_info=True)
            context.abort(grpc.StatusCode.INTERNAL, 'Plan failed')


class RPCServer:
    """Main RPC server orchestrator"""
    
    def __init__(self, config_file):
        """Initialize RPC server with configuration"""
        self.config = self._load_config(config_file)
        self.server = None
        self.cert_monitor = None
        logger.info(f'RPCServer initialized from config: {config_file}')
    
    def _load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logger.info(f'Configuration loaded from {config_file}')
            return config
        except FileNotFoundError:
            logger.error(f'Configuration file not found: {config_file}')
            raise
        except json.JSONDecodeError as e:
            logger.error(f'Invalid JSON in configuration file: {e}')
            raise
    
    def _load_tls_credentials(self):
        """Load TLS certificates for server"""
        cert_file = self.config.get('tls_cert_file')
        key_file = self.config.get('tls_key_file')
        ca_file = self.config.get('tls_ca_file')
        
        try:
            with open(key_file, 'rb') as f:
                private_key = f.read()
            
            with open(cert_file, 'rb') as f:
                certificate_chain = f.read()
            
            ca_cert = None
            if ca_file:
                with open(ca_file, 'rb') as f:
                    ca_cert = f.read()
            
            logger.info('TLS credentials loaded successfully')
            
            return grpc.ssl_server_credentials(
                [(private_key, certificate_chain)],
                root_certificates=ca_cert,
                require_client_auth=self.config.get('require_client_auth', True),
            )
        
        except FileNotFoundError as e:
            logger.error(f'TLS certificate file not found: {e}')
            raise
        except Exception as e:
            logger.error(f'Failed to load TLS credentials: {e}')
            raise
    
    def start(self):
        """Start the RPC server"""
        logger.info('Starting DebVisor RPC service')
        
        # Create server with interceptors
        interceptors = [
            AuthenticationInterceptor(self.config),
            AuthorizationInterceptor(self.config),
            AuditInterceptor(self.config),
        ]
        
        # Configure Connection Pooling & Performance Options
        pool_config = self.config.get('connection_pool', {})
        max_workers = pool_config.get('max_connections', 50)
        
        # gRPC Channel Options for Performance & Keepalive
        options = [
            ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50MB
            ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50MB
            ('grpc.keepalive_time_ms', int(pool_config.get('idle_timeout', 300.0) * 1000)),
            ('grpc.keepalive_timeout_ms', int(pool_config.get('connection_timeout', 10.0) * 1000)),
            ('grpc.keepalive_permit_without_calls', 1),
            ('grpc.http2.max_pings_without_data', 0),
            ('grpc.http2.min_time_between_pings_ms', 10000),
            ('grpc.http2.min_ping_interval_without_data_ms', 5000),
        ]

        # Configure Compression
        compression_config = self.config.get('compression', {})
        compression_algorithm = grpc.Compression.NoCompression
        if compression_config.get('enabled', False):
            algo = compression_config.get('algorithm', 'gzip').lower()
            if algo == 'gzip':
                compression_algorithm = grpc.Compression.Gzip
            elif algo == 'deflate':
                compression_algorithm = grpc.Compression.Deflate
            logger.info(f"RPC Compression enabled: {algo}")

        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            interceptors=interceptors,
            options=options,
            compression=compression_algorithm
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
        tls_creds = self._load_tls_credentials()
        
        # Bind to port
        host = self.config.get('host', '127.0.0.1')
        port = self.config.get('port', 7443)
        self.server.add_secure_port(f'{host}:{port}', tls_creds)
        
        logger.info(f'RPC server listening on {host}:{port}')
        
        self.server.start()
        
        try:
            # Block while serving
            logger.info('RPC server started successfully')
            while True:
                time.sleep(86400)  # Sleep for a day
        except KeyboardInterrupt:
            logger.info('Shutting down RPC server')
            self.stop()
    
    def stop(self, grace_timeout=5):
        """Gracefully shutdown RPC server"""
        if self.server:
            logger.info(f'Shutting down server (grace timeout: {grace_timeout}s)')
            self.server.stop(grace_timeout)


def main():
    """Main entry point"""
    config_file = os.environ.get(
        'RPC_CONFIG_FILE',
        '/etc/debvisor/rpc/config.json'
    )
    
    try:
        server = RPCServer(config_file)
        server.start()
    except Exception as e:
        logger.error(f'Failed to start RPC server: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
