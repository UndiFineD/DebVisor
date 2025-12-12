# DebVisor RPC Service Implementation Examples

## Complete Server Implementation

## services/rpc/server.py

    import grpc
    import json
    import logging
    import os
    import sys
    from concurrent import futures
    from datetime import datetime, timedelta
    from enum import Enum

## Generated protobuf modules (from make protoc)

    import debvisor_pb2
    import debvisor_pb2_grpc

## Local modules

    from auth import AuthenticationInterceptor, extract_identity
    from authz import AuthorizationInterceptor, check_permission
    from audit import AuditInterceptor
    from rate_limiting import RateLimitingInterceptor, RateLimiter
    from validators import RequestValidator
    from key_manager import ApiKeyManager
    from cert_manager import CertificateMonitor

## Configure logging

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    )
    logger = logging.getLogger(**name**)
    class StatusCode(Enum):
        UNKNOWN = 0
        OK = 1
        WARN = 2
        ERROR = 3
    class NodeServiceImpl(debvisor_pb2_grpc.NodeServiceServicer):
        """Implementation of NodeService RPC calls"""
        def**init**(self, backend):
            self.backend = backend
            self.nodes = {}  # In-memory store (use persistent storage in production)
        def RegisterNode(self, request, context):
            """Register a new node or update existing"""
            try:

## Validate inputs

                hostname = RequestValidator.validate_hostname(request.hostname)
                ip = RequestValidator.validate_ipv4(request.ip)

## Check authorization

                context.principal = extract_identity(context)
                check_permission(context, 'node:register')

## Register with backend

                node_id = self.backend.register_node(
                    hostname=hostname,
                    ip=ip,
                    version=request.version,
                )
                logger.info(f'Node registered: {hostname} ({ip}), node_id={node_id}')
                return debvisor_pb2.NodeAck(
                    status=StatusCode.OK.value,
                    message=f'Node {hostname} registered successfully',
                    node_id=node_id,
                )
            except ValueError as e:
                logger.warning(f'Invalid RegisterNode request: {e}')
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
                node_id = RequestValidator.validate_uuid(request.node_id)
                context.principal = extract_identity(context)
                check_permission(context, 'node:heartbeat')

## Update node state

                self.backend.update_node_heartbeat(node_id, request.health)
                return debvisor_pb2.HealthAck(
                    status=StatusCode.OK.value,
                    timestamp=debvisor_pb2.Timestamp(
                        seconds=int(datetime.utcnow().timestamp()),
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
                context.principal = extract_identity(context)
                check_permission(context, 'node:list')
                nodes = self.backend.list_nodes()
                node_summaries = [
                    debvisor_pb2.NodeSummary(
                        node_id=n['id'],
                        hostname=n['hostname'],
                        ip=n['ip'],
                        status=n['status'],
                        last_heartbeat=debvisor_pb2.Timestamp(
                            seconds=int(n['last_heartbeat'].timestamp()),
                        ),
                    )
                    for n in nodes
                ]
                return debvisor_pb2.NodeList(nodes=node_summaries)
            except PermissionError as e:
                context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
            except Exception as e:
                logger.error(f'ListNodes error: {e}', exc_info=True)
                context.abort(grpc.StatusCode.INTERNAL, 'List failed')
    class StorageServiceImpl(debvisor_pb2_grpc.StorageServiceServicer):
        """Implementation of StorageService RPC calls"""
        def**init**(self, backend):
            self.backend = backend
        def CreateSnapshot(self, request, context):
            """Create a ZFS or RBD snapshot"""
            try:

## Validate inputs [2]

                pool = RequestValidator.validate_label(request.pool)
                snapshot = RequestValidator.validate_label(request.snapshot)
                context.principal = extract_identity(context)
                check_permission(context, 'storage:snapshot:create')

## Create snapshot

                snapshot_id = self.backend.create_snapshot(
                    backend=request.backend,
                    pool=pool,
                    snapshot=snapshot,
                    tags=dict(request.tags),
                )
                logger.info(
                    f'Snapshot created: {pool}@{snapshot}, '
                    f'snapshot_id={snapshot_id}, principal={context.principal}'
                )
                return debvisor_pb2.SnapshotStatus(
                    snapshot_id=snapshot_id,
                    status=StatusCode.OK.value,
                    created_at=debvisor_pb2.Timestamp(
                        seconds=int(datetime.utcnow().timestamp()),
                    ),
                )
            except ValueError as e:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
            except PermissionError as e:
                context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
            except Exception as e:
                logger.error(f'CreateSnapshot error: {e}', exc_info=True)
                context.abort(grpc.StatusCode.INTERNAL, 'Snapshot creation failed')
        def ListSnapshots(self, request, context):
            """List snapshots"""
            try:
                context.principal = extract_identity(context)
                check_permission(context, 'storage:snapshot:list')
                snapshots = self.backend.list_snapshots(
                    backend=request.backend,
                    pool=request.pool if request.pool else None,
                )
                return debvisor_pb2.SnapshotList(snapshots=snapshots)
            except PermissionError as e:
                context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
            except Exception as e:
                logger.error(f'ListSnapshots error: {e}', exc_info=True)
                context.abort(grpc.StatusCode.INTERNAL, 'List failed')
    class RPCServer:
        """Main RPC server orchestrator"""
        def**init**(self, config_file):
            self.config = self._load_config(config_file)
            self.backend = self._init_backend()
            self.rate_limiter = RateLimiter(
                global_rps=self.config.get('global_rps', 1000),
                per_principal_rps=self.config.get('per_principal_rps', 100),
            )
            self.cert_monitor = None
        def _load_config(self, config_file):
            """Load configuration from file"""
            with open(config_file, 'r') as f:
                return json.load(f)
        def _init_backend(self):
            """Initialize backend (Ceph, libvirt, K8s, etc)"""

## Implementation depends on backend

            pass
        def _load_tls_credentials(self):
            """Load TLS certificates for server"""
            cert_file = self.config['tls_cert_file']
            key_file = self.config['tls_key_file']
            ca_file = self.config.get('tls_ca_file')
            with open(key_file, 'rb') as f:
                private_key = f.read()
            with open(cert_file, 'rb') as f:
                certificate_chain = f.read()
            ca_cert = None
            if ca_file:
                with open(ca_file, 'rb') as f:
                    ca_cert = f.read()
            return grpc.ssl_server_credentials(
                [(private_key, certificate_chain)],
                root_certificates=ca_cert,
                require_client_auth=self.config.get('require_client_auth', True),
            )
        def start(self):
            """Start the RPC server"""
            logger.info('Starting DebVisor RPC service')

## Create server with interceptors

            interceptors = [
                AuthenticationInterceptor(self.config),
                AuthorizationInterceptor(self.config),
                RateLimitingInterceptor(self.rate_limiter),
                AuditInterceptor(self.config),
            ]
            server = grpc.server(
                futures.ThreadPoolExecutor(max_workers=10),
                interceptors=interceptors,
            )

## Register services

            debvisor_pb2_grpc.add_NodeServiceServicer_to_server(
                NodeServiceImpl(self.backend),
                server,
            )
            debvisor_pb2_grpc.add_StorageServiceServicer_to_server(
                StorageServiceImpl(self.backend),
                server,
            )

## Add MigrationService implementation similarly

## Load TLS credentials

            tls_creds = self._load_tls_credentials()

## Bind to port

            host = self.config.get('host', '127.0.0.1')
            port = self.config.get('port', 7443)
            server.add_secure_port(f'{host}:{port}', tls_creds)
            logger.info(f'RPC server listening on {host}:{port}')

## Start certificate monitor in background

            if self.config.get('auto_renew_certificates'):
                cert_path = self.config['tls_cert_file']
                self.cert_monitor = CertificateMonitor(
                    cert_path=cert_path,
                    ca_path=self.config.get('tls_ca_file'),
                    renewal_script=self.config.get('cert_renewal_script'),
                )

## Run monitor in separate thread

                import threading
                monitor_thread = threading.Thread(
                    target=self.cert_monitor.monitor_loop,
                    daemon=True,
                )
                monitor_thread.start()
            server.start()
            try:

## Block while serving

                while True:
                    time.sleep(86400)  # Sleep for a day
            except KeyboardInterrupt:
                logger.info('Shutting down RPC server')
                server.stop(5)  # 5 seconds graceful shutdown
    if**name**== '**main**':
        import time
        config_file = os.environ.get('RPC_CONFIG_FILE', '/etc/debvisor/rpc/config.json')
        server = RPCServer(config_file)
        server.start()

## Authentication Implementation

## services/rpc/auth.py

    import grpc
    import jwt
    import json
    import hashlib
    import base64
    from datetime import datetime
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    class Identity:
        """Represents authenticated identity"""
        def**init**(self, principal_id, auth_method, permissions=None):
            self.principal_id = principal_id
            self.auth_method = auth_method  # 'mtls', 'api-key', 'jwt'
            self.permissions = permissions or []
            self.auth_time = datetime.utcnow()
    def extract_identity(context):
        """Extract identity from gRPC context"""

## Identity should be set by AuthenticationInterceptor

        return getattr(context, '_identity', None)
    class AuthenticationInterceptor(grpc.ServerInterceptor):
        """Authenticate requests using mTLS, API keys, or JWT"""
        def**init**(self, config):
            self.config = config
            self.jwt_public_key = self._load_jwt_public_key()
        def _load_jwt_public_key(self):
            """Load JWT public key for verification"""
            key_path = self.config.get('jwt_public_key_file')
            if not key_path:
                return None
            try:
                with open(key_path, 'r') as f:
                    return f.read()
            except Exception as e:
                print(f"Failed to load JWT public key: {e}")
                return None
        def intercept_service(self, continuation, handler_call_details):
            """Intercept RPC call and authenticate"""

## Try to authenticate

            identity = self._authenticate(handler_call_details)
            if not identity:
                return grpc.unary_unary_rpc_terminator(
                    grpc.StatusCode.UNAUTHENTICATED,
                    'Authentication failed',
                )

## Store identity in context for handler

            def new_handler(request):
                context = handler_call_details.context
                context._identity = identity
                return continuation(handler_call_details)
            return new_handler
        def _authenticate(self, handler_call_details):
            """Try all authentication methods"""

## Method 1: Try mTLS

            identity = self._authenticate_mtls(handler_call_details)
            if identity:
                return identity

## Method 2: Try API key or JWT in metadata

            identity = self._authenticate_metadata(handler_call_details)
            if identity:
                return identity
            return None
        def _authenticate_mtls(self, handler_call_details):
            """Authenticate using mTLS certificates"""

## gRPC provides client certificate info in peer metadata

            peer_metadata = handler_call_details.invocation_metadata or []

## Look for x509 certificate in peer metadata

            for key, value in peer_metadata:
                if key == 'x509-subject':

## Extract CN from certificate subject

## Example: "/C=US/ST=CA/L=SF/O=DebVisor/CN=web-panel"

                    try:
                        subject_parts = value.split('/')
                        for part in subject_parts:
                            if part.startswith('CN='):
                                cn = part[3:]

## Load permissions for this principal

                                permissions = self._load_permissions(cn)
                                return Identity(cn, 'mtls', permissions)
                    except:
                        pass
            return None
        def _authenticate_metadata(self, handler_call_details):
            """Authenticate using API key or JWT in metadata"""
            metadata = dict(handler_call_details.invocation_metadata or [])
            auth_header = metadata.get('authorization', '')
            if not auth_header.startswith('Bearer '):
                return None
            token = auth_header[7:]  # Remove 'Bearer ' prefix

## Try JWT

            if self.jwt_public_key:
                identity = self._verify_jwt(token)
                if identity:
                    return identity

## Try API key

            identity = self._verify_api_key(token)
            if identity:
                return identity
            return None
        def _verify_jwt(self, token):
            """Verify JWT token"""
            if not self.jwt_public_key:
                return None
            try:
                payload = jwt.decode(
                    token,
                    self.jwt_public_key,
                    algorithms=['RS256'],
                )

## Check expiration

                if 'exp' in payload:
                    from datetime import datetime
                    if datetime.utcfromtimestamp(payload['exp']) < datetime.utcnow():
                        return None

## Check issuer and audience

                issuer = self.config.get('jwt_issuer')
                if issuer and payload.get('iss') != issuer:
                    return None
                audience = self.config.get('jwt_audience')
                if audience and payload.get('aud') != audience:
                    return None
                principal_id = payload.get('sub') or payload.get('user_id')
                permissions = payload.get('permissions', [])
                return Identity(principal_id, 'jwt', permissions)
            except jwt.InvalidTokenError:
                return None
        def _verify_api_key(self, api_key):
            """Verify API key"""

## Hash the key for comparison

            key_hash = hashlib.sha256(api_key.encode()).hexdigest()

## Look up in key storage

            key_data = self._lookup_key_hash(key_hash)
            if not key_data:
                return None

## Check expiration [2]

            from datetime import datetime
            if 'expires_at' in key_data:
                if datetime.fromisoformat(key_data['expires_at']) < datetime.utcnow():
                    return None
            principal_id = key_data['principal_id']
            permissions = key_data.get('permissions', [])
            return Identity(principal_id, 'api-key', permissions)
        def _lookup_key_hash(self, key_hash):
            """Look up API key hash in storage"""

## Implementation depends on storage backend (etcd, database, etc)

            pass
        def _load_permissions(self, principal_id):
            """Load permissions for principal from RBAC"""

## Implementation depends on RBAC backend

## Returns list of permission strings like ['node:*', 'storage:snapshot:list']

            pass

## Authorization Implementation

## services/rpc/authz.py

    import grpc
    import logging
    logger = logging.getLogger(**name**)
    class PermissionMatcher:
        """Match permission specs with wildcards"""
        @staticmethod
        def matches(required_permission, caller_permissions):
            """Check if caller has required permission"""

## Examples

## required: 'storage:snapshot:create'

## caller has: 'storage:*' -> MATCH

## caller has: 'storage:snapshot:*' -> MATCH

## caller has: 'storage:snapshot:create' -> MATCH

## caller has: 'node:*' -> NO MATCH

            for perm in caller_permissions:
                if PermissionMatcher._perm_matches(required_permission, perm):
                    return True
            return False
        @staticmethod
        def _perm_matches(required, pattern):
            """Check if required permission matches wildcard pattern"""
            if pattern == '*':
                return True
            required_parts = required.split(':')
            pattern_parts = pattern.split(':')

## Pattern can't have more parts than required

            if len(pattern_parts) > len(required_parts):
                return False
            for i, pattern_part in enumerate(pattern_parts):
                if pattern_part == '*':

## Wildcard matches remaining

                    return True
                if pattern_part != required_parts[i]:
                    return False
            return len(pattern_parts) == len(required_parts)
    def check_permission(context, required_permission):
        """Check if context principal has permission"""
        identity = getattr(context, '_identity', None)
        if not identity:
            logger.warning('check_permission called without identity')
            raise PermissionError('Not authenticated')
        if PermissionMatcher.matches(required_permission, identity.permissions):
            return True
        logger.warning(
            f'Permission denied: principal={identity.principal_id}, '
            f'permission={required_permission}'
        )
        raise PermissionError(
            f'Principal {identity.principal_id} lacks permission: {required_permission}'
        )
    class AuthorizationInterceptor(grpc.ServerInterceptor):
        """Log authorization checks"""
        def**init**(self, config):
            self.config = config
        def intercept_service(self, continuation, handler_call_details):

## Authorization is checked per-operation in handlers

            return continuation(handler_call_details)

## Audit Logging Implementation

## services/rpc/audit.py

    import json
    import logging
    import grpc
    from datetime import datetime
    class AuditLogger:
        """Structured audit logging"""
        def**init**(self, log_file):
            self.logger = logging.getLogger('audit')
            handler = logging.FileHandler(log_file)
            handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        def log_event(self, event_type,__kwargs):
            """Log audit event"""
            event = {
                'timestamp': datetime.utcnow().isoformat(),
                'event': event_type,
                __kwargs,
            }
            self.logger.info(json.dumps(event))
    class AuditInterceptor(grpc.ServerInterceptor):
        """Audit all RPC calls"""
        def**init**(self, config):
            self.audit = AuditLogger(config.get('audit_log_file', '/var/log/debvisor/rpc-audit.log'))
        def intercept_service(self, continuation, handler_call_details):
            """Wrap handler to log calls"""
            def audit_handler(request):

## Extract info

                service, method = self._extract_service_method(handler_call_details)
                identity = getattr(handler_call_details.context, '_identity', None)
                principal = identity.principal_id if identity else 'unknown'

## Log call

                self.audit.log_event(
                    'rpc_call',
                    principal=principal,
                    service=service,
                    method=method,
                    auth_method=identity.auth_method if identity else None,
                )
                try:

## Execute handler

                    response = continuation(handler_call_details)

## Log success

                    self.audit.log_event(
                        'rpc_success',
                        principal=principal,
                        service=service,
                        method=method,
                    )
                    return response
                except Exception as e:

## Log error

                    self.audit.log_event(
                        'rpc_error',
                        principal=principal,
                        service=service,
                        method=method,
                        error=str(e),
                    )
                    raise
            return audit_handler
        def _extract_service_method(self, handler_call_details):
            """Extract service and method from RPC path"""

## Path format: /package.Service/Method

            path = handler_call_details.invocation_metadata

## Extraction logic

            return 'service', 'method'

## Configuration Example

    {
      "host": "127.0.0.1",
      "port": 7443,
      "tls_cert_file": "/etc/debvisor/rpc/server-cert.pem",
      "tls_key_file": "/etc/debvisor/rpc/server-key.pem",
      "tls_ca_file": "/etc/debvisor/rpc/ca-cert.pem",
      "require_client_auth": true,
      "auto_renew_certificates": true,
      "cert_renewal_script": "/usr/local/sbin/generate-rpc-certificates.sh",
      "jwt_public_key_file": "/etc/debvisor/rpc/jwt-public.pem",
      "jwt_issuer": "[https://auth.debvisor.local",](https://auth.debvisor.local",)
      "jwt_audience": "rpc.debvisor.local",
      "audit_log_file": "/var/log/debvisor/rpc-audit.log",
      "global_rps": 1000,
      "per_principal_rps": 100,
      "request_size_limit": 1048576,
      "response_size_limit": 10485760,
      "request_timeout_seconds": 300,
      "rbac_storage": "etcd",
      "etcd_endpoints": ["[http://127.0.0.1:2379"]](http://127.0.0.1:2379"])
    }

## Client Usage Examples

## Example: CLI client

    import grpc
    import debvisor_pb2
    import debvisor_pb2_grpc

## Load client credentials

    with open('client-cert.pem', 'rb') as f:
        client_cert = f.read()
    with open('client-key.pem', 'rb') as f:
        client_key = f.read()
    with open('ca-cert.pem', 'rb') as f:
        ca_cert = f.read()

## Create secure channel

    creds = grpc.ssl_channel_credentials(
        root_certificates=ca_cert,
        private_key=client_key,
        certificate_chain=client_cert,
    )
    channel = grpc.secure_channel('127.0.0.1:7443', creds)
    stub = debvisor_pb2_grpc.NodeServiceStub(channel)

## Make RPC call

    response = stub.ListNodes(debvisor_pb2.Empty())
    for node in response.nodes:
        print(f"{node.hostname} ({node.ip}) - {node.status}")
    channel.close()

## References

- Proto definitions: `proto/debvisor.proto`

- Design documentation: `DESIGN.md`

- Security implementation: `SECURITY_IMPLEMENTATION.md`
