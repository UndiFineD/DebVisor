# DebVisor RPC Service Design & Architecture\n\n## Overview\n\nThe DebVisor RPC service

(`debvisor.v1`) provides a secure, audited API for cluster operations. This
document
describes the
architecture, security model, authentication/authorization framework, and
deployment
patterns for
the RPC service.\n\n## Table of Contents\n\n1. Architecture\n\n1. Authentication
Model\n\n1.
Authorization Framework\n\n1. TLS Configuration\n\n1. Request Handling &
Validation\n\n1.
Audit
Logging\n\n1. Error Handling\n\n1. Deployment Patterns\n\n1. Testing
Strategy\n\n##
Architecture\n\n### Service Components\n\n
+-----------------------------------------------------------------+\n | Clients |\n |
+--------------+ +--------------+ +------------------+ |\n | | Web Panel | | CLI Tools | |
External
API | |\n | | (flask) | | (hvctl) | | (integration) | |\n | +--------------+
+--------------+
+------------------+ |\n
+------------------------+--------------------------------------+\n | gRPC

- TLS\n +------------------------?--------------------------------------+\n | TLS/mTLS
Termination
|\n | (client cert validation, encryption) |\n
+------------------------+--------------------------------------+\n |\n
+------------------------?--------------------------------------+\n | Authentication &
Identity |\n
| *Extract client certificate / API key / JWT token |\n |*Validate signature and expiration |\n
|*Map to user/service identity |\n
+------------------------+--------------------------------------+\n |\n
+------------------------?--------------------------------------+\n | Authorization &
Access Control
|\n |*Load RBAC policy from etcd/config |\n |*Check caller permissions for requested operation |\n
|*Enforce multi-tenancy isolation |\n
+------------------------+--------------------------------------+\n |\n
+------------------------?--------------------------------------+\n | Request Validation &
Rate
Limiting |\n |*Validate protocol buffers schema |\n |*Check request size limits |\n
|*Apply rate
limiting per caller |\n |*Log request for audit trail |\n
+------------------------+--------------------------------------+\n |\n
+------------------------?--------------------------------------+\n | RPC Service
Implementation |\n
|*NodeService (register, heartbeat, list nodes) |\n |*MigrationService (VM migration orchestration)
|\n |*StorageService (snapshots, replication) |\n
+------------------------+--------------------------------------+\n |\n
+------------------------?--------------------------------------+\n | Backend Cluster
Operations |\n
|*Ceph cluster API (librados, librbd) |\n |*Kubernetes API (kubectl, kubeadm) |\n |*Hypervisor API
(libvirt) |\n |*ZFS administration (zpool, zfs commands) |\n
+----------------------------------------------------------------+\n\n###
Service
Responsibilities\n\n### NodeService\n\n- Register nodes with cluster\n\n- Accept
health/heartbeat
reports\n\n- List cluster nodes with last-known state\n\n###
MigrationService\n\n- Plan VM
migrations (validate resource availability)\n\n- Execute VM migrations with
monitoring\n\n-
Coordinate failover on node failure\n\n### StorageService\n\n- Create/prune
snapshots (ZFS
and
Ceph)\n\n- Orchestrate ZFS replication between nodes\n\n- Clone Ceph RBD images
from
templates\n\n### Deployment Topology\n\n +-----------------------------------------+\n |
Each
DebVisor Node |\n | |\n | +------------------------------------+ |\n | |
debvisor-rpcd.service | |\n
| | (systemd Type=notify) | |\n | | User=debvisor-rpc | |\n | | Listen: 127.0.0.1:7443 (TLS) | |\n |
| venv: /var/lib/debvisor-rpc/venv | |\n | +------------------------------------+ |\n | | |\n |
+--------?---------+ |\n | | Backend Services | |\n | +------------------+ |\n | |*Ceph
cluster |
|\n | |*Kubernetes API | |\n | |*Libvirt | |\n | |*ZFS storage | |\n | +------------------+ |\n |
|\n +-----------------------------------------+\n |\n | gRPC calls\n | (localhost only initially)\n
|\n +----?----+\n | Web Panel/\n | CLI Tools\n +---------+\n\n## Authentication Model\n\n### Three
Authentication Methods (Choose One)\n\n#### 1. Mutual TLS (mTLS) - Recommended
for
Service-to-Service\n\n-*When to use:**Service authentication, Kubernetes,
trusted
networks\n\n###
Implementation\n\n- Both client and server present X.509 certificates\n\n-
Server
validates client
certificate\n\n- Client certificate contains identity (CN, subjectAltName)\n\n-
No
additional token
needed\n\n### Setup\n\n## Generate CA certificate\n\n openssl genrsa -out
ca-key.pem
4096\n openssl
req -new -x509 -days 3650 -key ca-key.pem -out ca-cert.pem -subj
"/CN=DebVisor-RPC-CA"\n\n##
Generate server certificate\n\n openssl genrsa -out server-key.pem 4096\n
openssl req -new
-key
server-key.pem -out server.csr -subj "/CN=debvisor-rpc"\n openssl x509 -req -in
server.csr
-CA
ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -days
365\n\n##
Generate client
certificate\n\n openssl genrsa -out client-key.pem 4096\n openssl req -new -key
client-key.pem -out
client.csr -subj "/CN=web-panel"\n openssl x509 -req -in client.csr -CA
ca-cert.pem -CAkey
ca-key.pem -CAcreateserial -out client-cert.pem -days 365\n\n##
Configuration\n\n##
Server\n\n creds
= grpc.ssl_channel_credentials(\n root_certificates=open('ca-cert.pem',
'rb').read(),\n
private_key=open('server-key.pem', 'rb').read(),\n
certificate_chain=open('server-cert.pem',
'rb').read(),\n )\n server = grpc.server(\n
futures.ThreadPoolExecutor(max_workers=10),\n
options=[\n ('grpc.ssl_server_request_type', 2), #
REQUEST_AND_REQUIRE_CLIENT_CERTIFICATE\n ]\n )\n
server.add_secure_port('0.0.0.0:7443', creds)\n\n## Client\n\n creds =
grpc.ssl_channel_credentials(\n root_certificates=open('ca-cert.pem',
'rb').read(),\n
private_key=open('client-key.pem', 'rb').read(),\n
certificate_chain=open('client-cert.pem',
'rb').read(),\n )\n channel = grpc.secure_channel('debvisor-rpc:7443',
creds)\n\n## 2. API
Keys -
Suitable for CLI Tools and Integrations\n\n- *When to use:**External
integrations, CI/CD
systems,
command-line tools\n\n### Implementation [2]\n\n- Client sends API key in
metadata header:
`authorization: Bearer`\n\n- Server validates key against known keys (etcd,
config
file)\n\n- Keys
are rotated regularly (quarterly minimum)\n\n### Setup [2]\n\n## Generate API
key (256
bits,
base64-encoded)\n\n openssl rand -base64 32 # Output: abc123xyz...\n\n## Store
in etcd\n\n
etcd put
/debvisor/rpc/apikeys/ci-system "abc123xyz..."\n\n## Assign to principal\n\n
etcd put
/debvisor/rpc/principals/ci-system '{\n "type": "service",\n "apikey_id":
"abc123xyz...",\n
"permissions": ["storage:snapshot:create", "storage:snapshot:list"]\n }'\n\n##
Usage in
gRPC\n\n def
add_authorization_metadata(context, api_key):\n """Add API key to gRPC
context"""\n
metadata =
[('authorization', f'Bearer {api_key}')]\n return metadata\n\n## Client side\n\n
metadata
=
add_authorization_metadata(None, 'abc123xyz...')\n result =
stub.ListNodes(Empty(),
metadata=metadata)\n\n## 3. JWT Tokens - Flexible, Suitable for User
Sessions\n\n- *When
to
use:**Web panel user sessions, OAuth2 integration, federated auth\n\n###
Implementation
[3]\n\n-
Client obtains JWT from authentication service (OIDC, OAuth2, or local)\n\n- JWT
contains
claims:
user ID, permissions, expiration, issuer\n\n- Server validates JWT signature and
claims\n\n### Setup
[3]\n\n import jwt\n from cryptography.hazmat.primitives import
serialization\n\n##
Server: Load
public key for JWT verification\n\n public_key = open('jwt-public-key.pem',
'rb').read()\n
def
validate_jwt(token):\n """Validate JWT token"""\n try:\n payload = jwt.decode(\n
token,\n
public_key,\n algorithms=['RS256'],\n audience='debvisor-rpc',\n
issuer='debvisor-auth'\n
)\n return
payload # Contains user_id, permissions, exp, etc.\n except
jwt.InvalidTokenError as e:\n
return
None # Invalid or expired\n\n## Client: Include JWT in metadata\n\n def
with_jwt(context,
token):\n
"""Add JWT to gRPC metadata"""\n metadata = [('authorization', f'Bearer
{token}')]\n
return
metadata\n result = stub.ListNodes(Empty(), metadata=with_jwt(None,
jwt_token))\n\n##
Authentication
Hierarchy\n\n +------------------------------------+\n | Request arrives at gRPC server
|\n
+------------+-----------------------+\n |\n +------?------+\n | Has mTLS |  256:\n
context.abort(grpc.StatusCode.INVALID_ARGUMENT,\n 'Label too long (max 256
characters)')\n\n## Call
actual handler\n\n return func(self, request, context)\n return wrapper\n return
decorator\n class
StorageServiceImpl(debvisor_pb2_grpc.StorageServiceServicer):\n
@validate_proto_message(SnapshotRequest)\n def CreateSnapshot(self, request,
context):\n\n## Handler
code\n\n pass\n\n## Size & Rate Limiting\n\n class
SizeLimitInterceptor(grpc.ServerInterceptor):\n
"""Limit request/response message sizes"""\n MAX_REQUEST_SIZE = 1 *1024*1024 #
1MB\n
MAX_RESPONSE_SIZE = 10*1024* 1024 # 10MB\n def intercept_service(self,
continuation,
handler_call_details):\n\n## Check metadata for content-length\n\n metadata =
dict(handler_call_details.invocation_metadata)\n content_length =
int(metadata.get('content-length',
0))\n if content_length > self.MAX_REQUEST_SIZE:\n return
grpc.unary_unary_rpc_terminator(\n
grpc.StatusCode.RESOURCE_EXHAUSTED,\n f'Request too large ({content_length} >
{self.MAX_REQUEST_SIZE})',\n )\n return continuation(handler_call_details)\n
class
RateLimitInterceptor(grpc.ServerInterceptor):\n """Rate limit by caller"""\n
def**init**(self,
max_requests_per_minute=100):\n self.max_requests_per_minute =
max_requests_per_minute\n
self.request_counts = {} # {principal_id: deque of timestamps}\n def
intercept_service(self,
continuation, handler_call_details):\n\n## Get caller identity\n\n principal =
self._get_principal(handler_call_details)\n\n## Check rate limit\n\n now =
time.time()\n
if
principal not in self.request_counts:\n self.request_counts[principal] =
collections.deque()\n
counts = self.request_counts[principal]\n\n## Remove requests older than 1
minute\n\n
while counts
and (now - counts[0]) > 60:\n counts.popleft()\n if len(counts) >=
self.max_requests_per_minute:\n
return grpc.unary_unary_rpc_terminator(\n grpc.StatusCode.RESOURCE_EXHAUSTED,\n
f'Rate
limit
exceeded: {self.max_requests_per_minute} requests/minute',\n )\n
counts.append(now)\n
return
continuation(handler_call_details)\n def _get_principal(self,
handler_call_details):\n
"""Extract
principal from metadata"""\n metadata =
dict(handler_call_details.invocation_metadata)\n\n## Could
be mTLS subject CN or API key\n\n return metadata.get('principal',
'anonymous')\n\n##
Audit
Logging\n\n### Events to Log\n\n import json\n from datetime import datetime\n
class
AuditLog:\n
"""Central audit logging for RPC service"""\n def**init**(self,
log_file='/var/log/debvisor/rpc-audit.log'):\n self.log_file = log_file\n
self.handler =
None\n def
log_authentication_success(self, principal, auth_method):\n """Log successful
authentication"""\n
self._write({\n 'event': 'authentication_success',\n 'principal': principal,\n
'auth_method':
auth_method,\n 'timestamp': datetime.utcnow().isoformat(),\n })\n def
log_authentication_failure(self, attempted_principal, reason):\n """Log failed
authentication"""\n
self._write({\n 'event': 'authentication_failure',\n 'attempted_principal':
attempted_principal,\n
'reason': reason,\n 'timestamp': datetime.utcnow().isoformat(),\n })\n def
log_rpc_call(self,
principal, service, method, args):\n """Log RPC call"""\n self._write[:200]({\n
'event':
'rpc_call',\n 'principal': principal,\n 'service': service,\n 'method':
method,\n
'args_summary':
str(args), # Truncate large args\n 'timestamp': datetime.utcnow().isoformat(),\n
})\n def
log_rpc_result(self, principal, service, method, status, error=None):\n """Log
RPC
result"""\n
self._write({\n 'event': 'rpc_result',\n 'principal': principal,\n 'service':
service,\n
'method':
method,\n 'status': status,\n 'error': error,\n 'timestamp':
datetime.utcnow().isoformat(),\n })\n
def log_permission_denied(self, principal, permission, resource):\n """Log
permission
denied"""\n
self._write({\n 'event': 'permission_denied',\n 'principal': principal,\n
'permission':
permission,\n 'resource': resource,\n 'timestamp':
datetime.utcnow().isoformat(),\n })\n
def
log_rate_limit_exceeded(self, principal):\n """Log rate limit exceeded"""\n
self._write({\n 'event':
'rate_limit_exceeded',\n 'principal': principal,\n 'timestamp':
datetime.utcnow().isoformat(),\n
})\n def _write(self, event_dict):\n """Write event to audit log"""\n try:\n
with
open(self.log_file, 'a') as f:\n f.write(json.dumps(event_dict) + '\n')\n
f.flush()\n
except
Exception as e:\n\n## Log to syslog as fallback\n\n import syslog\n
syslog.syslog(f'RPC
audit log
write failed: {e}')\n\n### Audit Log Interception\n\n class
AuditInterceptor(grpc.ServerInterceptor):\n """Intercept all RPC calls for audit
logging"""\n
def**init**(self, audit_log):\n self.audit_log = audit_log\n def
intercept_service(self,
continuation, handler_call_details):\n\n## Parse service and method from handler
details\n\n
full_method = handler_call_details.method\n service, method =
full_method.rsplit('/',
1)\n\n## Log
the call\n\n principal = self._extract_principal(handler_call_details)\n
self.audit_log.log_rpc_call(principal, service, method, None)\n\n## Wrap handler
to log
result\n\n
handler = continuation(handler_call_details)\n return
self._wrap_handler(handler,
principal,
service, method)\n def _wrap_handler(self, handler, principal, service,
method):\n """Wrap
handler
to log results"""\n def new_handler(request):\n try:\n response =
handler(request)\n
self.audit_log.log_rpc_result(principal, service, method, 'success')\n return
response\n
except
Exception as e:\n self.audit_log.log_rpc_result(principal, service, method,
'error',
str(e))\n
raise\n return new_handler\n def _extract_principal(self,
handler_call_details):\n
"""Extract
principal from metadata"""\n metadata =
dict(handler_call_details.invocation_metadata)\n
return
metadata.get('principal', 'anonymous')\n\n## Error Handling\n\n### Standard
Error
Codes\n\n| Status
| Usage | Example |\n|--------|-------|---------|\n| OK | Success | Operation completed |\n|
CANCELLED | Client cancelled | User interrupted |\n| UNKNOWN | Unknown error | Unexpected
exception
|\n| INVALID_ARGUMENT | Bad input | Invalid VM ID format |\n| DEADLINE_EXCEEDED | Timeout |
Migration took too long |\n| NOT_FOUND | Resource not found | VM doesn't exist |\n|
ALREADY_EXISTS |
Duplicate | Node already registered |\n| PERMISSION_DENIED | Auth failure | Caller lacks
permission
|\n| RESOURCE_EXHAUSTED | Rate limit/quota | Too many requests |\n| FAILED_PRECONDITION | Wrong
state | Can't migrate running VM |\n| ABORTED | Retry-able | Transient backend error |\n|
INTERNAL |
Server error | Backend crashed |\n\n### Error Response Format\n\n message ErrorDetails {\n
string
code = 1; // e.g., "INVALID_VM_ID"\n string message = 2; // Human-readable error
message\n
map
context = 3; // Additional context\n string trace_id = 4; // For debugging (in
server
logs)\n }\n
message RpcStatus {\n StatusCode status = 1;\n ErrorDetails error_details = 2;\n
}\n\n###
Error
Handling Pattern\n\n def MigrateVM(self, request, context):\n """Example error
handling"""\n
try:\n\n## Validate input\n\n if not request.vm_id:\n
context.abort(grpc.StatusCode.INVALID_ARGUMENT,\n 'VM ID is required')\n\n##
Check
prerequisites\n\n
vm = self._get_vm(request.vm_id)\n if not vm:\n
context.abort(grpc.StatusCode.NOT_FOUND,\n
f'VM not
found: {request.vm_id}')\n if vm.state == 'running':\n
context.abort(grpc.StatusCode.FAILED_PRECONDITION,\n 'Cannot migrate running VM
(use
failover
instead)')\n\n## Perform operation\n\n result =
self._execute_migration(request)\n return
MigrationResult(\n status=debvisor_pb2.STATUS_OK,\n message='Migration completed
successfully',\n
)\n except TimeoutError:\n context.abort(grpc.StatusCode.DEADLINE_EXCEEDED,\n
'Migration
timed out
(check cluster status)')\n except Exception as e:\n\n## Don't expose internal
errors\n\n
context.abort(grpc.StatusCode.INTERNAL,\n 'An error occurred during migration
(check
server
logs)')\n\n## Deployment Patterns\n\n### Production Deployment Checklist\n\n-
[]**TLS/mTLS
enabled**- No unencrypted connections\n\n- []**Authentication configured**- mTLS
certs,
API keys, or
JWT\n\n- []**RBAC policies loaded**- Roles defined in etcd/config\n\n- []**Audit
logging
enabled**-
All operations logged to file/syslog\n\n- []**Rate limiting configured**-
Appropriate
limits per
principal\n\n- []**Certificates rotated quarterly**- Automated renewal
process\n\n-
[]**Error
handlers in place**- No internal error exposure\n\n- []**Health check
endpoint**- For load
balancers\n\n- []**Metrics exported**- Prometheus metrics for monitoring\n\n-
[]**Graceful
shutdown**- Clean client disconnection handling\n\n### systemd Unit
Configuration\n\n
[Unit]\n
Description=DebVisor RPC Service\n After=network-online.target\n
Wants=network-online.target\n
[Service]\n Type=notify\n User=debvisor-rpc\n Group=debvisor-rpc\n
WorkingDirectory=/var/lib/debvisor-rpc\n
ExecStart=/var/lib/debvisor-rpc/venv/bin/python3
-m
debvisor_rpcd\n ExecReload=/bin/kill -HUP $MAINPID\n\n## Environment\n\n
Environment="RPC_TLS_CERT=/etc/debvisor/rpc/cert.pem"\n
Environment="RPC_TLS_KEY=/etc/debvisor/rpc/key.pem"\n
Environment="RPC_TLS_CA=/etc/debvisor/rpc/ca.pem"\n
Environment="RPC_LOG_LEVEL=INFO"\n
Environment="RPC_LOG_FILE=/var/log/debvisor/rpc.log"\n
Environment="RPC_AUDIT_LOG=/var/log/debvisor/rpc-audit.log"\n\n## Security
hardening\n\n
ProtectSystem=strict\n ProtectHome=yes\n NoNewPrivileges=yes\n
PrivateDevices=yes\n
PrivateTmp=yes\n
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6\n RestrictRealtime=yes\n
RestrictNamespaces=yes\n
LockPersonality=yes\n\n## Resource limits\n\n MemoryLimit=512M\n CPUQuota=200%\n
TasksMax=512\n\n##
Restart policy\n\n Restart=on-failure\n RestartSec=10\n [Install]\n
WantedBy=multi-user.target\n\n##
Testing Strategy\n\n### Unit Tests\n\n## tests/test_auth.py\n\n class
TestAuthentication(unittest.TestCase):\n def
test_mTLS_valid_certificate(self):\n """Test
mTLS with
valid client certificate"""\n\n## Create test channel with valid cert\n\n
channel =
create_test_channel(cert='valid-client.pem')\n stub =
debvisor_pb2_grpc.NodeServiceStub(channel)\n\n## Should succeed\n\n result =
stub.ListNodes(Empty())\n self.assertIsNotNone(result)\n def
test_mTLS_invalid_certificate(self):\n
"""Test mTLS with invalid certificate"""\n channel =
create_test_channel(cert='invalid-client.pem')\n stub =
debvisor_pb2_grpc.NodeServiceStub(channel)\n
with self.assertRaises(grpc.RpcError):\n stub.ListNodes(Empty())\n def
test_api_key_validation(self):\n """Test API key authentication"""\n metadata =
[('authorization',
'Bearer valid-api-key')]\n\n## Should succeed [2]\n\n result =
stub.ListNodes(Empty(),
metadata=metadata)\n metadata = [('authorization', 'Bearer
invalid-api-key')]\n\n## Should
fail\n\n
with self.assertRaises(grpc.RpcError):\n stub.ListNodes(Empty(),
metadata=metadata)\n\n##
tests/test_authorization.py\n\n class TestAuthorization(unittest.TestCase):\n
def
test_operator_can_migrate(self):\n """Test operator role can execute
migration"""\n
principal =
'operator-user'\n check_permission(principal, 'migration:execute') # Should
succeed\n def
test_viewer_cannot_execute_migration(self):\n """Test viewer role cannot execute
migration"""\n
principal = 'viewer-user'\n with self.assertRaises(PermissionError):\n
check_permission(principal,
'migration:execute')\n\n## Integration Tests\n\n##
tests/integration/test_rpc_service.py\n\n class
TestRpcService(unittest.TestCase):\n def setUp(self):\n """Start RPC service in
test
mode"""\n
self.server = start_test_rpc_server()\n self.channel =
grpc.secure_channel(...)\n def
test_node_registration_flow(self):\n """Test complete node registration
flow"""\n\n##
Register
node\n\n node_info = NodeInfo(\n id=NodeId(id='node-01'),\n
hostname='node01.example.com',\n
ip='192.168.1.10',\n )\n stub =
debvisor_pb2_grpc.NodeServiceStub(self.channel)\n ack =
stub.RegisterNode(node_info)\n self.assertEqual(ack.status, STATUS_OK)\n\n##
Send
heartbeat\n\n
health = Health(\n node_id=NodeId(id='node-01'),\n overall=STATUS_OK,\n
cpu_load=0.5,\n
)\n
health_ack = stub.Heartbeat(health)\n self.assertEqual(health_ack.status,
STATUS_OK)\n\n##
List
nodes\n\n node_list = stub.ListNodes(Empty())\n
self.assertEqual(len(node_list.nodes),
1)\n
self.assertEqual(node_list.nodes[0].info.id.id, 'node-01')\n\n## Load
Testing\n\n##
tests/load/test_rpc_load.py\n\n## Use ghz (gRPC load testing tool)\n\n ghz
--insecure
\\n\n - -proto
./proto/debvisor.proto \\n\n - -call debvisor.v1.NodeService/ListNodes \\n\n -
-metadata
authorization:Bearer:test-api-key \\n\n - c 100 \\n\n - n 10000 \\n\n - m '{}'
\\n\n
debvisor-rpc:7443\n\n## Related Documentation\n\n-
`opt/config/CONFIG_IMPROVEMENTS.md`-
Build-time
configuration\n\n-`opt/build/BUILD_IMPROVEMENTS.md`- ISO build
process\n\n-`opt/web/panel/SECURITY.md`- Web panel security (uses this RPC
service)\n\n-`proto/debvisor.proto`- RPC API definitions\n\n-`README.md` - RPC
service
overview\n\n
