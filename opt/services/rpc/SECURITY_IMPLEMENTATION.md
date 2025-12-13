# DebVisor RPC Service - Security & Implementation Guide\n\n## Security Hardening\n\n###

1. TLS

Certificate Management\n\n#### Certificate Generation & Rotation\n\n

## !/bin/bash\n\n##

scripts/generate-rpc-certificates.sh\n\n set -e\n CERT_DIR=${1:-.}\n
VALIDITY_DAYS=${2:-365}\n
COUNTRY="US"\n STATE="CA"\n CITY="San Francisco"\n ORG="DebVisor"\n
CN="debvisor-rpc"\n
mkdir -p
"$CERT_DIR"\n\n## Generate CA private key\n\n echo "[*] Generating CA private
key..."\n
openssl
genrsa -out "$CERT_DIR/ca-key.pem" 4096\n\n## Generate CA certificate\n\n echo
"[*]
Generating CA
certificate..."\n openssl req -new -x509 -days 3650 -key "$CERT_DIR/ca-key.pem"
\\n\n -
out
"$CERT_DIR/ca-cert.pem" \\n\n - subj
"/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG/CN=$CN-CA"\n\n## Generate
server private key\n\n echo "[*] Generating server private key..."\n openssl
genrsa -out
"$CERT_DIR/server-key.pem" 4096\n\n## Generate server CSR\n\n echo "[*]
Generating server
CSR..."\n
openssl req -new -key "$CERT_DIR/server-key.pem" \\n\n - out
"$CERT_DIR/server.csr" \\n\n

- subj
"/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG/CN=$CN" \\n\n - config expires_at:\n
return None # Expired\n\n## Update usage stats\n\n
key_data['last_used'] = datetime.utcnow().isoformat()\n key_data['use_count'] +=
1\n
self.etcd.put(f'{self.key_prefix}{key_data["id"]}', json.dumps(key_data))\n
return
key_data\n return
None # Key not found\n def list_keys(self, principal_id=None):\n """List all API
keys
(optionally
filtered by principal)"""\n keys = []\n for value in
self.etcd.get_prefix(self.key_prefix):\n
key_data = json.loads(value[0])\n if principal_id and key_data['principal_id']
!=
principal_id:\n
continue\n\n## Don't expose key_hash in listings\n\n key_data.pop('key_hash',
None)\n
keys.append(key_data)\n return keys\n def revoke_key(self, key_id):\n """Revoke
an API
key"""\n
key_path = f'{self.key_prefix}{key_id}'\n try:\n self.etcd.delete(key_path)\n
print(f"[?]
API key
revoked: {key_id}")\n return True\n except Exception as e:\n print(f"[?] Failed
to revoke
key:
{e}")\n return False\n def rotate_keys_for_principal(self, principal_id):\n
"""Rotate all
keys for a
principal (generate new, revoke old)"""\n old_keys =
self.list_keys(principal_id)\n for
key_data in
old_keys:\n print(f"[*] Revoking old key: {key_data['id']}")\n
self.revoke_key(key_data['id'])\n\n##
Generate new key\n\n permissions = old_keys[0]['permissions'] if old_keys else
[]\n
new_key, new_id
= self.generate_key(\n principal_id,\n permissions,\n f'Rotated from
{old_keys[0]["id"] if
old_keys
else ""}',\n )\n return new_key, new_id\n\n## Usage\n\n if**name**==
'**main**':\n import
etcd3\n
etcd = etcd3.client()\n km = ApiKeyManager(etcd)\n\n## Generate key for CI
system\n\n
api_key,
key_id = km.generate_key(\n 'ci-system',\n
permissions=['storage:snapshot:create',
'storage:snapshot:list'],\n description='CI/CD pipeline automation',\n
ttl_days=90, #
Shorter TTL
for CI keys\n )\n\n## List keys for a principal\n\n keys =
km.list_keys('ci-system')\n
print(f"Keys
for ci-system: {keys}")\n\n## 3. Request Validation & Input Sanitization\n\n##
services/rpc/validators.py\n\n import re\n from uuid import UUID\n class
RequestValidator:\n
"""Validate and sanitize RPC request inputs"""\n\n## Regex patterns\n\n
HOSTNAME_PATTERN =
re.compile(r'^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)*$')\n
IPv4_PATTERN = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')\n UUID_PATTERN =
re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
re.I)\n
@staticmethod\n def validate_hostname(hostname):\n """Validate hostname
format"""\n if not
isinstance(hostname, str) or len(hostname) > 253:\n raise ValueError(f'Invalid
hostname:
{hostname}')\n if not RequestValidator.HOSTNAME_PATTERN.match(hostname):\n raise
ValueError(f'Invalid hostname format: {hostname}')\n return hostname\n
@staticmethod\n def
validate_ipv4(ip):\n """Validate IPv4 address"""\n if not isinstance(ip, str):\n
raise
ValueError('IP must be a string')\n if not
RequestValidator.IPv4_PATTERN.match(ip):\n
raise
ValueError(f'Invalid IPv4 address: {ip}')\n\n## Check each octet is 0-255\n\n
octets =
[int(x) for x
in ip.split('.')]\n if any(x > 255 for x in octets):\n raise
ValueError(f'Invalid IPv4
address:
{ip}')\n return ip\n @staticmethod\n def validate_uuid(uuid_str):\n """Validate
UUID
format"""\n
try:\n UUID(uuid_str)\n return uuid_str\n except (ValueError, AttributeError):\n
raise
ValueError(f'Invalid UUID: {uuid_str}')\n @staticmethod\n def
validate_label(label,
max_length=256):\n """Validate snapshot/pool label"""\n if not isinstance(label,
str) or
len(label)
== 0:\n raise ValueError('Label must be a non-empty string')\n if len(label) >
max_length:\n raise
ValueError(f'Label too long (max {max*length} characters)')\n\n## Only allow
alphanumeric,
hyphens,
underscores\n\n if not re.match(r'^[a-zA-Z0-9*-]+$', label):\n raise
ValueError(f'Label
contains
invalid characters: {label}')\n return label\n @staticmethod\n def
validate_permission_spec(perm_spec):\n """Validate permission specification
string"""\n\n## Format:
"service:resource:action" or "service:*" or "*"\n\n if perm_spec == '*':\n
return
perm_spec\n parts
= perm_spec.split(':')\n if len(parts) 3:\n raise ValueError(f'Invalid
permission spec:
{perm*spec}')\n for part in parts:\n if part != '*' and not
re.match(r'^[a-z][a-z0-9*]*$',
part):\n
raise ValueError(f'Invalid permission spec: {perm_spec}')\n return
perm_spec\n\n## Usage
in service
handlers\n\n class NodeServiceImpl(debvisor_pb2_grpc.NodeServiceServicer):\n def
RegisterNode(self,
request, context):\n try:\n\n## Validate inputs\n\n hostname =
RequestValidator.validate_hostname(request.hostname)\n ip =
RequestValidator.validate_ipv4(request.ip)\n\n## Process request\n\n node =
self._register_node(hostname, ip)\n return NodeAck(status=STATUS_OK,
message='Node
registered')\n
except ValueError as e:\n context.abort(grpc.StatusCode.INVALID_ARGUMENT,
str(e))\n except
Exception
as e:\n context.abort(grpc.StatusCode.INTERNAL, 'Registration failed')\n\n## 4.
Rate
Limiting &
Quota Management\n\n## services/rpc/rate_limiting.py\n\n import time\n import
threading\n
from
collections import defaultdict, deque\n class RateLimiter:\n """Rate limiter
with
per-principal and
global limits"""\n def**init**(self, global_rps=1000, per_principal_rps=100):\n
self.global_rps =
global_rps\n self.per_principal_rps = per_principal_rps\n self.global_requests =
deque()\n
self.principal_requests = defaultdict(deque)\n self.lock = threading.Lock()\n
def
is_allowed(self,
principal, operation_cost=1):\n """Check if request from principal is
allowed"""\n with
self.lock:\n
now = time.time()\n\n## Check global rate limit\n\n## Remove requests older than
1
second\n\n while
self.global_requests and (now - self.global_requests[0]) > 1.0:\n
self.global_requests.popleft()\n
if len(self.global_requests) >= self.global_rps:\n return False, "Global rate
limit
exceeded"\n\n##
Check per-principal rate limit\n\n principal_deque =
self.principal_requests[principal]\n
while
principal_deque and (now - principal_deque[0]) > 1.0:\n
principal_deque.popleft()\n if
len(principal_deque) >= self.per_principal_rps:\n return False, f"Rate limit
exceeded for
{principal}"\n\n## Allow request\n\n self.global_requests.append(now)\n
principal_deque.append(now)\n return True, ""\n class QuotaManager:\n """Manage
per-principal quotas
(e.g., snapshot count, total storage)"""\n def**init**(self, etcd_client):\n
self.etcd =
etcd_client\n self.quota_prefix = '/debvisor/rpc/quotas/'\n def get_quota(self,
principal,
resource_type):\n """Get quota for principal"""\n try:\n value =
self.etcd.get(f'{self.quota_prefix}{principal}/{resource_type}')\n return
json.loads(value[0])\n
except:\n return self.default_quota(resource_type)\n def default_quota(self,
resource_type):\n
"""Default quota values"""\n return {\n 'snapshots': 100,\n 'storage_gb':
1000,\n
'concurrent_operations': 5,\n }.get(resource_type, 0)\n def check_quota(self,
principal,
resource_type, amount=1):\n """Check if principal has quota for operation"""\n
quota =
self.get_quota(principal, resource_type)\n\n## In production, track actual
usage\n\n
return amount
 5/minute)\n\n- Permission denials (> 10/minute)\n\n- Rate limit
violations (> 20/minute)\n\n- Errors (> 1% error rate)\n\n### Operational
Readiness\n\n-
[] Health
check endpoint (/healthz) available\n\n- [] Metrics exposed (Prometheus
format)\n\n- []
Graceful
shutdown (drain existing requests)\n\n- [] systemd service unit configured\n\n-
[]
Resource limits
set (memory, CPU)\n\n- [] Backup/restore procedures documented\n\n- [] Disaster
recovery
plan
documented\n\n- [] Runbooks created for common scenarios:\n\n- Certificate
expiration\n\n-
Service
restart\n\n- Key rotation\n\n- Troubleshooting failed RPC calls\n\n## Monitoring
&
Alerts\n\n### Key
Metrics\n\n## services/rpc/metrics.py\n\n from prometheus_client import Counter,
Histogram,
Gauge\n\n## Request metrics\n\n rpc_requests_total = Counter(\n
'rpc_requests_total',\n
'Total RPC
requests',\n ['service', 'method', 'status']\n )\n rpc_request_duration_seconds
=
Histogram(\n
'rpc_request_duration_seconds',\n 'RPC request duration',\n ['service',
'method']\n
)\n\n##
Authentication metrics\n\n auth_attempts_total = Counter(\n
'auth_attempts_total',\n
'Authentication
attempts',\n ['method', 'result'] # result: success, failure\n )\n\n##
Authorization
metrics\n\n
authz_denials_total = Counter(\n 'authz_denials_total',\n 'Authorization
denials',\n
['principal',
'permission']\n )\n\n## Rate limiting metrics\n\n rate_limit_violations_total =
Counter(\n
'rate_limit_violations_total',\n 'Rate limit violations',\n ['principal']\n
)\n\n## System
metrics\n\n rpc_service_status = Gauge(\n 'rpc_service_status',\n 'RPC service
status',\n
value=1 #
1=ready, 0=degraded\n )\n backend_connection_errors_total = Counter(\n
'backend_connection_errors_total',\n 'Backend connection errors',\n
['backend_service'] #
ceph, k8s,
libvirt\n )\n\n## Alert Rules\n\n## prometheus-rules.yml\n\n groups:\n\n- name:
rpc-service\n\n
rules:\n\n- alert: HighAuthenticationFailureRate\n\n expr:
rate(auth_attempts_total{result="failure"}[5m]) > 0.1\n for: 5m\n annotations:\n
summary:
"High
authentication failure rate ({{ $value }}/sec)"\n action: "Check client
credentials and
network
connectivity"\n\n- alert: HighRateLimitViolations\n\n expr:
rate(rate_limit_violations_total[5m]) >
0.5\n for: 5m\n annotations:\n summary: "High rate limit violations"\n action:
"Check for
malicious
clients or legitimate traffic spike"\n\n- alert: RpcErrorRate\n\n expr:
rate(rpc_requests_total{status="error"}[5m]) > 0.01\n for: 5m\n annotations:\n
summary:
"RPC error
rate > 1%"\n action: "Check server logs and backend service health"\n\n- alert:
BackendConnectionError\n\n expr: increase(backend_connection_errors_total[5m]) >
0\n for:
1m\n
annotations:\n summary: "Cannot connect to {{ $labels.backend_service }}"\n
action: "Check
{{
$labels.backend_service }} service status"\n\n## References\n\n- Proto
definitions:
`proto/debvisor.proto`\n\n- Original README: `README.md`\n\n- Related:
`opt/web/panel/SECURITY.md`,`opt/config/CONFIG_IMPROVEMENTS.md`\n\n
