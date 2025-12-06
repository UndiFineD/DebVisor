# DebVisor RPC Service Design & Architecture

## Overview

The DebVisor RPC service (`debvisor.v1`) provides a secure, audited API for cluster operations. This document describes the architecture, security model, authentication/authorization framework, and deployment patterns for the RPC service.

## Table of Contents

1. Architecture
1. Authentication Model
1. Authorization Framework
1. TLS Configuration
1. Request Handling & Validation
1. Audit Logging
1. Error Handling
1. Deployment Patterns
1. Testing Strategy

## Architecture

### Service Components

    +-----------------------------------------------------------------+
    |                        Clients                                  |
    |  +--------------+  +--------------+  +------------------+      |
    |  |  Web Panel   |  |  CLI Tools   |  |  External API    |      |
    |  |  (flask)     |  |  (hvctl)     |  |  (integration)   |      |
    |  +--------------+  +--------------+  +------------------+      |
    +------------------------+--------------------------------------+
                             | gRPC + TLS
    +------------------------?--------------------------------------+
    |                  TLS/mTLS Termination                          |
    |              (client cert validation, encryption)              |
    +------------------------+--------------------------------------+
                             |
    +------------------------?--------------------------------------+
    |              Authentication & Identity                          |
    |  * Extract client certificate / API key / JWT token            |
    |  * Validate signature and expiration                           |
    |  * Map to user/service identity                                |
    +------------------------+--------------------------------------+
                             |
    +------------------------?--------------------------------------+
    |            Authorization & Access Control                       |
    |  * Load RBAC policy from etcd/config                           |
    |  * Check caller permissions for requested operation            |
    |  * Enforce multi-tenancy isolation                             |
    +------------------------+--------------------------------------+
                             |
    +------------------------?--------------------------------------+
    |           Request Validation & Rate Limiting                    |
    |  * Validate protocol buffers schema                            |
    |  * Check request size limits                                   |
    |  * Apply rate limiting per caller                              |
    |  * Log request for audit trail                                 |
    +------------------------+--------------------------------------+
                             |
    +------------------------?--------------------------------------+
    |              RPC Service Implementation                          |
    |  * NodeService (register, heartbeat, list nodes)               |
    |  * MigrationService (VM migration orchestration)               |
    |  * StorageService (snapshots, replication)                     |
    +------------------------+--------------------------------------+
                             |
    +------------------------?--------------------------------------+
    |         Backend Cluster Operations                              |
    |  * Ceph cluster API (librados, librbd)                         |
    |  * Kubernetes API (kubectl, kubeadm)                           |
    |  * Hypervisor API (libvirt)                                    |
    |  * ZFS administration (zpool, zfs commands)                    |
    +----------------------------------------------------------------+

### Service Responsibilities

### NodeService

- Register nodes with cluster
- Accept health/heartbeat reports
- List cluster nodes with last-known state

### MigrationService

- Plan VM migrations (validate resource availability)
- Execute VM migrations with monitoring
- Coordinate failover on node failure

### StorageService

- Create/prune snapshots (ZFS and Ceph)
- Orchestrate ZFS replication between nodes
- Clone Ceph RBD images from templates

### Deployment Topology

    +-----------------------------------------+
    |  Each DebVisor Node                     |
    |                                         |
    |  +------------------------------------+ |
    |  |  debvisor-rpcd.service             | |
    |  |  (systemd Type=notify)             | |
    |  |  User=debvisor-rpc                 | |
    |  |  Listen: 127.0.0.1:7443 (TLS)      | |
    |  |  venv: /var/lib/debvisor-rpc/venv  | |
    |  +------------------------------------+ |
    |                  |                       |
    |         +--------?---------+             |
    |         | Backend Services  |             |
    |         +------------------+             |
    |         | * Ceph cluster   |             |
    |         | * Kubernetes API |             |
    |         | * Libvirt        |             |
    |         | * ZFS storage    |             |
    |         +------------------+             |
    |                                         |
    +-----------------------------------------+
             |
             | gRPC calls
             | (localhost only initially)
             |
        +----?----+
        | Web Panel/
        | CLI Tools
        +---------+

## Authentication Model

### Three Authentication Methods (Choose One)

#### 1. Mutual TLS (mTLS) - Recommended for Service-to-Service

__When to use:__Service authentication, Kubernetes, trusted networks

### Implementation

- Both client and server present X.509 certificates
- Server validates client certificate
- Client certificate contains identity (CN, subjectAltName)
- No additional token needed

### Setup

## Generate CA certificate

    openssl genrsa -out ca-key.pem 4096
    openssl req -new -x509 -days 3650 -key ca-key.pem -out ca-cert.pem -subj "/CN=DebVisor-RPC-CA"

## Generate server certificate

    openssl genrsa -out server-key.pem 4096
    openssl req -new -key server-key.pem -out server.csr -subj "/CN=debvisor-rpc"
    openssl x509 -req -in server.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -days 365

## Generate client certificate

    openssl genrsa -out client-key.pem 4096
    openssl req -new -key client-key.pem -out client.csr -subj "/CN=web-panel"
    openssl x509 -req -in client.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out client-cert.pem -days 365

## Configuration

## Server

    creds = grpc.ssl_channel_credentials(
        root_certificates=open('ca-cert.pem', 'rb').read(),
        private_key=open('server-key.pem', 'rb').read(),
        certificate_chain=open('server-cert.pem', 'rb').read(),
    )
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.ssl_server_request_type', 2),  # REQUEST_AND_REQUIRE_CLIENT_CERTIFICATE
        ]
    )
    server.add_secure_port('0.0.0.0:7443', creds)

## Client

    creds = grpc.ssl_channel_credentials(
        root_certificates=open('ca-cert.pem', 'rb').read(),
        private_key=open('client-key.pem', 'rb').read(),
        certificate_chain=open('client-cert.pem', 'rb').read(),
    )
    channel = grpc.secure_channel('debvisor-rpc:7443', creds)

## 2. API Keys - Suitable for CLI Tools and Integrations

__When to use:__External integrations, CI/CD systems, command-line tools

### Implementation [2]

- Client sends API key in metadata header: `authorization: Bearer`
- Server validates key against known keys (etcd, config file)
- Keys are rotated regularly (quarterly minimum)

### Setup [2]

## Generate API key (256 bits, base64-encoded)

    openssl rand -base64 32  # Output: abc123xyz...

## Store in etcd

    etcd put /debvisor/rpc/apikeys/ci-system "abc123xyz..."

## Assign to principal

    etcd put /debvisor/rpc/principals/ci-system '{
      "type": "service",
      "apikey_id": "abc123xyz...",
      "permissions": ["storage:snapshot:create", "storage:snapshot:list"]
    }'

## Usage in gRPC

    def add_authorization_metadata(context, api_key):
        """Add API key to gRPC context"""
        metadata = [('authorization', f'Bearer {api_key}')]
        return metadata

## Client side

    metadata = add_authorization_metadata(None, 'abc123xyz...')
    result = stub.ListNodes(Empty(), metadata=metadata)

## 3. JWT Tokens - Flexible, Suitable for User Sessions

__When to use:__Web panel user sessions, OAuth2 integration, federated auth

### Implementation [3]

- Client obtains JWT from authentication service (OIDC, OAuth2, or local)
- JWT contains claims: user ID, permissions, expiration, issuer
- Server validates JWT signature and claims

### Setup [3]

    import jwt
    from cryptography.hazmat.primitives import serialization

## Server: Load public key for JWT verification

    public_key = open('jwt-public-key.pem', 'rb').read()

    def validate_jwt(token):
        """Validate JWT token"""
        try:
            payload = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience='debvisor-rpc',
                issuer='debvisor-auth'
            )
            return payload  # Contains user_id, permissions, exp, etc.
        except jwt.InvalidTokenError as e:
            return None  # Invalid or expired

## Client: Include JWT in metadata

    def with_jwt(context, token):
        """Add JWT to gRPC metadata"""
        metadata = [('authorization', f'Bearer {token}')]
        return metadata

    result = stub.ListNodes(Empty(), metadata=with_jwt(None, jwt_token))

## Authentication Hierarchy

    +------------------------------------+
    |  Request arrives at gRPC server    |
    +------------+-----------------------+
                 |
          +------?------+
          | Has mTLS    | <- Client certificate
          | cert?       |
          +------+------+
                 | Yes
          +------?------+
          | Extract CN  | <- Subject CN = principal ID
          | as identity |
          +------+------+
                 |
                 +-----? (authenticated, set context.identity)

          +------+------+
          | No mTLS,    |
          | check       |
          | metadata    |
          +------+------+
                 |
          +------?--------------+
          | Authorization:      |
          | "Bearer "?   |
          +------+--------------+
                 | Yes (JWT or API key)
          +------?------+
          | Validate    | <- Signature, expiration, issuer
          | token       |
          +------+------+
                 | Valid
                 +-----? (authenticated, extract claims)

## Authorization Framework

### RBAC Model

__Resources:__Operations that require permission

    debvisor.v1 RPC operations:
    +- node
    |  +- register
    |  +- heartbeat
    |  +- list
    +- migration
    |  +- plan
    |  +- execute
    |  +- failover
    +- storage
       +- snapshot
       |  +- create
       |  +- delete
       |  +- list
       +- replication
       |  +- plan
       |  +- execute
       |  +- status
       +- clone

### Role Definitions

### Operator Role

    name: operator
    permissions:

- node:*
- migration:*
- storage:*

    description: "Full cluster administrative access"

### Developer/CI Role

    name: developer
    permissions:

- node:list
- storage:snapshot:create
- storage:snapshot:list
- storage:clone:*

    description: "CI/CD pipeline automation (read-only + create snapshots)"

### Monitoring Role

    name: monitor
    permissions:

- node:list
- node:heartbeat

    description: "Monitoring agents can report health only"

### Viewer Role

    name: viewer
    permissions:

- node:list
- storage:snapshot:list
- migration:plan  # Plan but not execute

    description: "Read-only access to cluster state"

### Permission Checking

## In interceptor or decorator

    def check_permission(context, required_permission):
        """Check if caller has required permission"""

## Get authenticated identity from context

        identity = context.identity  # Extracted by auth interceptor

## Load caller's roles

        roles = load_roles_for_principal(identity)

## Collect all permissions

        caller_permissions = set()
        for role in roles:
            for perm in role.permissions:
                caller_permissions.add(perm)

## Check permission (support wildcards)

        if _permission_matches(required_permission, caller_permissions):
            return True

## Audit log: permission denied

        log_audit('permission_denied', {
            'principal': identity,
            'permission': required_permission,
            'timestamp': now(),
        })
        raise PermissionError(f'Principal {identity} lacks permission: {required_permission}')

    def _permission_matches(required, available):
        """Check if required permission is in available set (with wildcard support)"""
        if required in available:
            return True

## Check wildcards: "storage:*" matches "storage:snapshot:create"

        parts = required.split(':')
        for i in range(1, len(parts)):
            wildcard = ':'.join(parts[:i]) + ':*'
            if wildcard in available:
                return True
        return False

## TLS Configuration

### Server-Side TLS Setup

### Recommended: TLS 1.3 only

## In debvisor-rpcd.py

    def load_server_credentials():
        """Load TLS server credentials from files or secrets"""

## Get paths from config/secrets

        cert_path = os.getenv('RPC_TLS_CERT', '/etc/debvisor/rpc/cert.pem')
        key_path = os.getenv('RPC_TLS_KEY', '/etc/debvisor/rpc/key.pem')
        ca_path = os.getenv('RPC_TLS_CA', '/etc/debvisor/rpc/ca.pem')  # For mTLS

## Read certificate and key

        with open(cert_path, 'rb') as f:
            cert_chain = f.read()
        with open(key_path, 'rb') as f:
            private_key = f.read()

## Validate certificate (check expiration)

        cert = x509.load_pem_x509_certificate(cert_chain)
        if cert.not_valid_after <= datetime.now():
            raise ValueError(f'Certificate expired: {cert.not_valid_after}')

## Create credentials

        creds = grpc.ssl_server_credentials(
            [(private_key, cert_chain)],
            root_certificates=open(ca_path, 'rb').read() if ca_path else None,
            require_client_auth=bool(ca_path),
        )

        return creds

## Create server with TLS

    creds = load_server_credentials()
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[
            AuthInterceptor(),  # Validate auth metadata
            AuditInterceptor(),  # Log all requests
            RateLimitInterceptor(),  # Rate limiting
        ]
    )

## Add services

    debvisor_pb2_grpc.add_NodeServiceServicer_to_server(NodeServiceImpl(), server)
    debvisor_pb2_grpc.add_MigrationServiceServicer_to_server(MigrationServiceImpl(), server)
    debvisor_pb2_grpc.add_StorageServiceServicer_to_server(StorageServiceImpl(), server)

## Listen on secure port

    server.add_secure_port('[::]:7443', creds)
    server.start()

## Client-Side TLS

    def create_rpc_channel(host, port, auth_method='mTLS'):
        """Create gRPC channel with appropriate credentials"""

        if auth_method == 'mTLS':

## Mutual TLS

            with open('/etc/debvisor/rpc/client-cert.pem', 'rb') as f:
                client_cert = f.read()
            with open('/etc/debvisor/rpc/client-key.pem', 'rb') as f:
                client_key = f.read()
            with open('/etc/debvisor/rpc/ca-cert.pem', 'rb') as f:
                ca_cert = f.read()

            creds = grpc.ssl_channel_credentials(
                root_certificates=ca_cert,
                private_key=client_key,
                certificate_chain=client_cert,
            )

        elif auth_method == 'TLS':

## TLS with server cert validation only (use API key or JWT in metadata)

            with open('/etc/debvisor/rpc/ca-cert.pem', 'rb') as f:
                ca_cert = f.read()

            creds = grpc.ssl_channel_credentials(
                root_certificates=ca_cert,
            )

        channel = grpc.secure_channel(f'{host}:{port}', creds)
        return channel

## Request Handling & Validation

### Protocol Buffer Validation

## Validator decorator

    def validate_proto_message(message_type):
        """Decorator to validate protobuf message"""
        def decorator(func):
            def wrapper(self, request, context):

## Check required fields

                if not request.HasField('required_field'):
                    context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                                 'Missing required field: required_field')

## Validate field values

                if not _is_valid_id(request.vm_id):
                    context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                                 f'Invalid VM ID format: {request.vm_id}')

## Check size limits

                if len(request.label) > 256:
                    context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                                 'Label too long (max 256 characters)')

## Call actual handler

                return func(self, request, context)
            return wrapper
        return decorator

    class StorageServiceImpl(debvisor_pb2_grpc.StorageServiceServicer):
        @validate_proto_message(SnapshotRequest)
        def CreateSnapshot(self, request, context):

## Handler code

            pass

## Size & Rate Limiting

    class SizeLimitInterceptor(grpc.ServerInterceptor):
        """Limit request/response message sizes"""

        MAX_REQUEST_SIZE = 1 *1024* 1024  # 1MB
        MAX_RESPONSE_SIZE = 10 *1024* 1024  # 10MB

        def intercept_service(self, continuation, handler_call_details):

## Check metadata for content-length

            metadata = dict(handler_call_details.invocation_metadata)
            content_length = int(metadata.get('content-length', 0))

            if content_length > self.MAX_REQUEST_SIZE:
                return grpc.unary_unary_rpc_terminator(
                    grpc.StatusCode.RESOURCE_EXHAUSTED,
                    f'Request too large ({content_length} > {self.MAX_REQUEST_SIZE})',
                )

            return continuation(handler_call_details)

    class RateLimitInterceptor(grpc.ServerInterceptor):
        """Rate limit by caller"""

        def__init__(self, max_requests_per_minute=100):
            self.max_requests_per_minute = max_requests_per_minute
            self.request_counts = {}  # {principal_id: deque of timestamps}

        def intercept_service(self, continuation, handler_call_details):

## Get caller identity

            principal = self._get_principal(handler_call_details)

## Check rate limit

            now = time.time()
            if principal not in self.request_counts:
                self.request_counts[principal] = collections.deque()

            counts = self.request_counts[principal]

## Remove requests older than 1 minute

            while counts and (now - counts[0]) > 60:
                counts.popleft()

            if len(counts) >= self.max_requests_per_minute:
                return grpc.unary_unary_rpc_terminator(
                    grpc.StatusCode.RESOURCE_EXHAUSTED,
                    f'Rate limit exceeded: {self.max_requests_per_minute} requests/minute',
                )

            counts.append(now)
            return continuation(handler_call_details)

        def _get_principal(self, handler_call_details):
            """Extract principal from metadata"""
            metadata = dict(handler_call_details.invocation_metadata)

## Could be mTLS subject CN or API key

            return metadata.get('principal', 'anonymous')

## Audit Logging

### Events to Log

    import json
    from datetime import datetime

    class AuditLog:
        """Central audit logging for RPC service"""

        def__init__(self, log_file='/var/log/debvisor/rpc-audit.log'):
            self.log_file = log_file
            self.handler = None

        def log_authentication_success(self, principal, auth_method):
            """Log successful authentication"""
            self._write({
                'event': 'authentication_success',
                'principal': principal,
                'auth_method': auth_method,
                'timestamp': datetime.utcnow().isoformat(),
            })

        def log_authentication_failure(self, attempted_principal, reason):
            """Log failed authentication"""
            self._write({
                'event': 'authentication_failure',
                'attempted_principal': attempted_principal,
                'reason': reason,
                'timestamp': datetime.utcnow().isoformat(),
            })

        def log_rpc_call(self, principal, service, method, args):
            """Log RPC call"""
            self._write({
                'event': 'rpc_call',
                'principal': principal,
                'service': service,
                'method': method,
                'args_summary': str(args)[:200],  # Truncate large args
                'timestamp': datetime.utcnow().isoformat(),
            })

        def log_rpc_result(self, principal, service, method, status, error=None):
            """Log RPC result"""
            self._write({
                'event': 'rpc_result',
                'principal': principal,
                'service': service,
                'method': method,
                'status': status,
                'error': error,
                'timestamp': datetime.utcnow().isoformat(),
            })

        def log_permission_denied(self, principal, permission, resource):
            """Log permission denied"""
            self._write({
                'event': 'permission_denied',
                'principal': principal,
                'permission': permission,
                'resource': resource,
                'timestamp': datetime.utcnow().isoformat(),
            })

        def log_rate_limit_exceeded(self, principal):
            """Log rate limit exceeded"""
            self._write({
                'event': 'rate_limit_exceeded',
                'principal': principal,
                'timestamp': datetime.utcnow().isoformat(),
            })

        def _write(self, event_dict):
            """Write event to audit log"""
            try:
                with open(self.log_file, 'a') as f:
                    f.write(json.dumps(event_dict) + '\n')
                    f.flush()
            except Exception as e:

## Log to syslog as fallback

                import syslog
                syslog.syslog(f'RPC audit log write failed: {e}')

### Audit Log Interception

    class AuditInterceptor(grpc.ServerInterceptor):
        """Intercept all RPC calls for audit logging"""

        def__init__(self, audit_log):
            self.audit_log = audit_log

        def intercept_service(self, continuation, handler_call_details):

## Parse service and method from handler details

            full_method = handler_call_details.method
            service, method = full_method.rsplit('/', 1)

## Log the call

            principal = self._extract_principal(handler_call_details)
            self.audit_log.log_rpc_call(principal, service, method, None)

## Wrap handler to log result

            handler = continuation(handler_call_details)
            return self._wrap_handler(handler, principal, service, method)

        def _wrap_handler(self, handler, principal, service, method):
            """Wrap handler to log results"""
            def new_handler(request):
                try:
                    response = handler(request)
                    self.audit_log.log_rpc_result(principal, service, method, 'success')
                    return response
                except Exception as e:
                    self.audit_log.log_rpc_result(principal, service, method, 'error', str(e))
                    raise

            return new_handler

        def _extract_principal(self, handler_call_details):
            """Extract principal from metadata"""
            metadata = dict(handler_call_details.invocation_metadata)
            return metadata.get('principal', 'anonymous')

## Error Handling

### Standard Error Codes

| Status | Usage | Example |
|--------|-------|---------|
| OK | Success | Operation completed |
| CANCELLED | Client cancelled | User interrupted |
| UNKNOWN | Unknown error | Unexpected exception |
| INVALID_ARGUMENT | Bad input | Invalid VM ID format |
| DEADLINE_EXCEEDED | Timeout | Migration took too long |
| NOT_FOUND | Resource not found | VM doesn't exist |
| ALREADY_EXISTS | Duplicate | Node already registered |
| PERMISSION_DENIED | Auth failure | Caller lacks permission |
| RESOURCE_EXHAUSTED | Rate limit/quota | Too many requests |
| FAILED_PRECONDITION | Wrong state | Can't migrate running VM |
| ABORTED | Retry-able | Transient backend error |
| INTERNAL | Server error | Backend crashed |

### Error Response Format

    message ErrorDetails {
      string code = 1;           // e.g., "INVALID_VM_ID"
      string message = 2;        // Human-readable error message
      map context = 3;  // Additional context
      string trace_id = 4;       // For debugging (in server logs)
    }

    message RpcStatus {
      StatusCode status = 1;
      ErrorDetails error_details = 2;
    }

### Error Handling Pattern

    def MigrateVM(self, request, context):
        """Example error handling"""
        try:

## Validate input

            if not request.vm_id:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                             'VM ID is required')

## Check prerequisites

            vm = self._get_vm(request.vm_id)
            if not vm:
                context.abort(grpc.StatusCode.NOT_FOUND,
                             f'VM not found: {request.vm_id}')

            if vm.state == 'running':
                context.abort(grpc.StatusCode.FAILED_PRECONDITION,
                             'Cannot migrate running VM (use failover instead)')

## Perform operation

            result = self._execute_migration(request)

            return MigrationResult(
                status=debvisor_pb2.STATUS_OK,
                message='Migration completed successfully',
            )

        except TimeoutError:
            context.abort(grpc.StatusCode.DEADLINE_EXCEEDED,
                         'Migration timed out (check cluster status)')

        except Exception as e:

## Don't expose internal errors

            context.abort(grpc.StatusCode.INTERNAL,
                         'An error occurred during migration (check server logs)')

## Deployment Patterns

### Production Deployment Checklist

- [ ]**TLS/mTLS enabled**- No unencrypted connections
- [ ]**Authentication configured**- mTLS certs, API keys, or JWT
- [ ]**RBAC policies loaded**- Roles defined in etcd/config
- [ ]**Audit logging enabled**- All operations logged to file/syslog
- [ ]**Rate limiting configured**- Appropriate limits per principal
- [ ]**Certificates rotated quarterly**- Automated renewal process
- [ ]**Error handlers in place**- No internal error exposure
- [ ]**Health check endpoint**- For load balancers
- [ ]**Metrics exported**- Prometheus metrics for monitoring
- [ ]**Graceful shutdown**- Clean client disconnection handling

### systemd Unit Configuration

    [Unit]
    Description=DebVisor RPC Service
    After=network-online.target
    Wants=network-online.target

    [Service]
    Type=notify
    User=debvisor-rpc
    Group=debvisor-rpc
    WorkingDirectory=/var/lib/debvisor-rpc

    ExecStart=/var/lib/debvisor-rpc/venv/bin/python3 -m debvisor_rpcd
    ExecReload=/bin/kill -HUP $MAINPID

## Environment

    Environment="RPC_TLS_CERT=/etc/debvisor/rpc/cert.pem"
    Environment="RPC_TLS_KEY=/etc/debvisor/rpc/key.pem"
    Environment="RPC_TLS_CA=/etc/debvisor/rpc/ca.pem"
    Environment="RPC_LOG_LEVEL=INFO"
    Environment="RPC_LOG_FILE=/var/log/debvisor/rpc.log"
    Environment="RPC_AUDIT_LOG=/var/log/debvisor/rpc-audit.log"

## Security hardening

    ProtectSystem=strict
    ProtectHome=yes
    NoNewPrivileges=yes
    PrivateDevices=yes
    PrivateTmp=yes
    RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
    RestrictRealtime=yes
    RestrictNamespaces=yes
    LockPersonality=yes

## Resource limits

    MemoryLimit=512M
    CPUQuota=200%
    TasksMax=512

## Restart policy

    Restart=on-failure
    RestartSec=10

    [Install]
    WantedBy=multi-user.target

## Testing Strategy

### Unit Tests

## tests/test_auth.py

    class TestAuthentication(unittest.TestCase):

        def test_mTLS_valid_certificate(self):
            """Test mTLS with valid client certificate"""

## Create test channel with valid cert

            channel = create_test_channel(cert='valid-client.pem')
            stub = debvisor_pb2_grpc.NodeServiceStub(channel)

## Should succeed

            result = stub.ListNodes(Empty())
            self.assertIsNotNone(result)

        def test_mTLS_invalid_certificate(self):
            """Test mTLS with invalid certificate"""
            channel = create_test_channel(cert='invalid-client.pem')
            stub = debvisor_pb2_grpc.NodeServiceStub(channel)
            with self.assertRaises(grpc.RpcError):
                stub.ListNodes(Empty())

        def test_api_key_validation(self):
            """Test API key authentication"""
            metadata = [('authorization', 'Bearer valid-api-key')]

## Should succeed [2]

            result = stub.ListNodes(Empty(), metadata=metadata)

            metadata = [('authorization', 'Bearer invalid-api-key')]

## Should fail

            with self.assertRaises(grpc.RpcError):
                stub.ListNodes(Empty(), metadata=metadata)

## tests/test_authorization.py

    class TestAuthorization(unittest.TestCase):

        def test_operator_can_migrate(self):
            """Test operator role can execute migration"""
            principal = 'operator-user'
            check_permission(principal, 'migration:execute')  # Should succeed

        def test_viewer_cannot_execute_migration(self):
            """Test viewer role cannot execute migration"""
            principal = 'viewer-user'
            with self.assertRaises(PermissionError):
                check_permission(principal, 'migration:execute')

## Integration Tests

## tests/integration/test_rpc_service.py

    class TestRpcService(unittest.TestCase):

        def setUp(self):
            """Start RPC service in test mode"""
            self.server = start_test_rpc_server()
            self.channel = grpc.secure_channel(...)

        def test_node_registration_flow(self):
            """Test complete node registration flow"""

## Register node

            node_info = NodeInfo(
                id=NodeId(id='node-01'),
                hostname='node01.example.com',
                ip='192.168.1.10',
            )
            stub = debvisor_pb2_grpc.NodeServiceStub(self.channel)
            ack = stub.RegisterNode(node_info)
            self.assertEqual(ack.status, STATUS_OK)

## Send heartbeat

            health = Health(
                node_id=NodeId(id='node-01'),
                overall=STATUS_OK,
                cpu_load=0.5,
            )
            health_ack = stub.Heartbeat(health)
            self.assertEqual(health_ack.status, STATUS_OK)

## List nodes

            node_list = stub.ListNodes(Empty())
            self.assertEqual(len(node_list.nodes), 1)
            self.assertEqual(node_list.nodes[0].info.id.id, 'node-01')

## Load Testing

## tests/load/test_rpc_load.py

## Use ghz (gRPC load testing tool)

    ghz --insecure \
        --proto ./proto/debvisor.proto \
        --call debvisor.v1.NodeService/ListNodes \
        --metadata authorization:Bearer:test-api-key \
        -c 100 \
        -n 10000 \
        -m '{}' \
        debvisor-rpc:7443

## Related Documentation

- `opt/config/CONFIG_IMPROVEMENTS.md` - Build-time configuration
- `opt/build/BUILD_IMPROVEMENTS.md` - ISO build process
- `opt/web/panel/SECURITY.md` - Web panel security (uses this RPC service)
- `proto/debvisor.proto` - RPC API definitions
- `README.md` - RPC service overview
