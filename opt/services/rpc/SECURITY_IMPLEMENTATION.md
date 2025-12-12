# DebVisor RPC Service - Security & Implementation Guide

## Security Hardening

### 1. TLS Certificate Management

#### Certificate Generation & Rotation

    #!/bin/bash

## scripts/generate-rpc-certificates.sh

    set -e

    CERT_DIR=${1:-.}
    VALIDITY_DAYS=${2:-365}
    COUNTRY="US"
    STATE="CA"
    CITY="San Francisco"
    ORG="DebVisor"
    CN="debvisor-rpc"

    mkdir -p "$CERT_DIR"

## Generate CA private key

    echo "[*] Generating CA private key..."
    openssl genrsa -out "$CERT_DIR/ca-key.pem" 4096

## Generate CA certificate

    echo "[*] Generating CA certificate..."
    openssl req -new -x509 -days 3650 -key "$CERT_DIR/ca-key.pem" \

        - out "$CERT_DIR/ca-cert.pem" \
        - subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG/CN=$CN-CA"

## Generate server private key

    echo "[*] Generating server private key..."
    openssl genrsa -out "$CERT_DIR/server-key.pem" 4096

## Generate server CSR

    echo "[*] Generating server CSR..."
    openssl req -new -key "$CERT_DIR/server-key.pem" \

        - out "$CERT_DIR/server.csr" \
        - subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG/CN=$CN" \
        - config <(cat /etc/ssl/openssl.cnf; printf "[alt_names]\nDNS.1=debvisor-rpc\nDNS.2=localhost\nIP.1=127.0.0.1")

## Sign server certificate

    echo "[*] Signing server certificate..."
    openssl x509 -req -in "$CERT_DIR/server.csr" \

        - CA "$CERT_DIR/ca-cert.pem" \
        - CAkey "$CERT_DIR/ca-key.pem" \
        - CAcreateserial \
        - out "$CERT_DIR/server-cert.pem" \
        - days "$VALIDITY_DAYS" \
        - extensions alt_names \
        - extfile <(printf "subjectAltName=DNS:debvisor-rpc,DNS:localhost,IP:127.0.0.1")

## Generate client private key

    echo "[*] Generating client private key..."
    openssl genrsa -out "$CERT_DIR/client-key.pem" 4096

## Generate client CSR

    echo "[*] Generating client CSR..."
    openssl req -new -key "$CERT_DIR/client-key.pem" \

        - out "$CERT_DIR/client.csr" \
        - subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG/CN=web-panel"

## Sign client certificate

    echo "[*] Signing client certificate..."
    openssl x509 -req -in "$CERT_DIR/client.csr" \

        - CA "$CERT_DIR/ca-cert.pem" \
        - CAkey "$CERT_DIR/ca-key.pem" \
        - CAcreateserial \
        - out "$CERT_DIR/client-cert.pem" \
        - days "$VALIDITY_DAYS"

## Set permissions

    echo "[*] Setting permissions..."
    chmod 0600 "$CERT_DIR"/*.pem
    chmod 0644 "$CERT_DIR"/ca-cert.pem "$CERT_DIR"/server-cert.pem "$CERT_DIR"/client-cert.pem

## Verify certificates

    echo "[*] Verifying certificates..."
    openssl verify -CAfile "$CERT_DIR/ca-cert.pem" "$CERT_DIR/server-cert.pem"
    openssl verify -CAfile "$CERT_DIR/ca-cert.pem" "$CERT_DIR/client-cert.pem"

    echo "[?] Certificates generated successfully"
    ls -lh "$CERT_DIR"/*.pem

## Automated Certificate Renewal

## services/rpc/cert_renewal.py

    import os
    import subprocess
    import time
    from datetime import datetime, timedelta
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend

    class CertificateMonitor:
        """Monitor certificate expiration and trigger renewal"""

        RENEWAL_THRESHOLD_DAYS = 30  # Renew 30 days before expiry
        CHECK_INTERVAL_SECONDS = 86400  # Check daily

        def**init**(self, cert_path, ca_path, renewal_script):
            self.cert_path = cert_path
            self.ca_path = ca_path
            self.renewal_script = renewal_script

        def should_renew(self):
            """Check if certificate should be renewed"""
            try:
                with open(self.cert_path, 'rb') as f:
                    cert = x509.load_pem_x509_certificate(
                        f.read(),
                        default_backend()
                    )

                expires_at = cert.not_valid_after
                days_until_expiry = (expires_at - datetime.utcnow()).days

                return days_until_expiry < self.RENEWAL_THRESHOLD_DAYS
            except Exception as e:
                print(f"Error checking certificate: {e}")
                return False

        def renew(self):
            """Trigger certificate renewal"""
            try:
                print(f"[*] Renewing certificate: {self.cert_path}")
                result = subprocess.run(
                    [self.renewal_script, os.path.dirname(self.cert_path)],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                print(result.stdout)

## Notify RPC daemon to reload certificates

                subprocess.run(['systemctl', 'reload', 'debvisor-rpcd'])
                return True
            except subprocess.CalledProcessError as e:
                print(f"Certificate renewal failed: {e.stderr}")
                return False

        def monitor_loop(self):
            """Continuously monitor and renew certificates"""
            while True:
                try:
                    if self.should_renew():
                        self.renew()
                    time.sleep(self.CHECK_INTERVAL_SECONDS)
                except Exception as e:
                    print(f"Monitor loop error: {e}")
                    time.sleep(60)  # Retry after 1 minute

    if**name**== '**main**':
        monitor = CertificateMonitor(
            cert_path='/etc/debvisor/rpc/server-cert.pem',
            ca_path='/etc/debvisor/rpc/ca-cert.pem',
            renewal_script='/usr/local/sbin/generate-rpc-certificates.sh',
        )
        monitor.monitor_loop()

## 2. API Key Management

### Key Generation and Storage

## services/rpc/key_manager.py

    import os
    import base64
    import hashlib
    from datetime import datetime, timedelta

    class ApiKeyManager:
        """Manage API keys for RPC service"""

        def**init**(self, etcd_client):
            self.etcd = etcd_client
            self.key_prefix = '/debvisor/rpc/apikeys/'

        def generate_key(self, principal_id, permissions, description='', ttl_days=365):
            """Generate a new API key"""

## Generate random 256-bit key

            raw_key = os.urandom(32)
            api_key = base64.b64encode(raw_key).decode()

## Store in etcd with metadata

            key_id = hashlib.sha256(raw_key).hexdigest()[:16]
            key_path = f'{self.key_prefix}{key_id}'

            key_data = {
                'id': key_id,
                'principal_id': principal_id,
                'permissions': permissions,
                'description': description,
                'created_at': datetime.utcnow().isoformat(),
                'expires_at': (datetime.utcnow() + timedelta(days=ttl_days)).isoformat(),
                'last_used': None,
                'use_count': 0,
            }

## Store key hash (not raw key) for comparison

            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            key_data['key_hash'] = key_hash

            self.etcd.put(key_path, json.dumps(key_data))

            print(f"[?] API key generated for {principal_id}: {key_id}")
            print(f"    Key (save this, it won't be shown again): {api_key}")

            return api_key, key_id

        def validate_key(self, api_key):
            """Validate API key and return principal info"""
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()

## Scan all keys for matching hash

            for value in self.etcd.get_prefix(self.key_prefix):
                key_data = json.loads(value[0])

## Check hash

                if key_data['key_hash'] != key_hash:
                    continue

## Check expiration

                expires_at = datetime.fromisoformat(key_data['expires_at'])
                if datetime.utcnow() > expires_at:
                    return None  # Expired

## Update usage stats

                key_data['last_used'] = datetime.utcnow().isoformat()
                key_data['use_count'] += 1
                self.etcd.put(f'{self.key_prefix}{key_data["id"]}', json.dumps(key_data))

                return key_data

            return None  # Key not found

        def list_keys(self, principal_id=None):
            """List all API keys (optionally filtered by principal)"""
            keys = []
            for value in self.etcd.get_prefix(self.key_prefix):
                key_data = json.loads(value[0])
                if principal_id and key_data['principal_id'] != principal_id:
                    continue

## Don't expose key_hash in listings

                key_data.pop('key_hash', None)
                keys.append(key_data)
            return keys

        def revoke_key(self, key_id):
            """Revoke an API key"""
            key_path = f'{self.key_prefix}{key_id}'
            try:
                self.etcd.delete(key_path)
                print(f"[?] API key revoked: {key_id}")
                return True
            except Exception as e:
                print(f"[?] Failed to revoke key: {e}")
                return False

        def rotate_keys_for_principal(self, principal_id):
            """Rotate all keys for a principal (generate new, revoke old)"""
            old_keys = self.list_keys(principal_id)

            for key_data in old_keys:
                print(f"[*] Revoking old key: {key_data['id']}")
                self.revoke_key(key_data['id'])

## Generate new key

            permissions = old_keys[0]['permissions'] if old_keys else []
            new_key, new_id = self.generate_key(
                principal_id,
                permissions,
                f'Rotated from {old_keys[0]["id"] if old_keys else ""}',
            )

            return new_key, new_id

## Usage

    if**name**== '**main**':
        import etcd3

        etcd = etcd3.client()
        km = ApiKeyManager(etcd)

## Generate key for CI system

        api_key, key_id = km.generate_key(
            'ci-system',
            permissions=['storage:snapshot:create', 'storage:snapshot:list'],
            description='CI/CD pipeline automation',
            ttl_days=90,  # Shorter TTL for CI keys
        )

## List keys for a principal

        keys = km.list_keys('ci-system')
        print(f"Keys for ci-system: {keys}")

## 3. Request Validation & Input Sanitization

## services/rpc/validators.py

    import re
    from uuid import UUID

    class RequestValidator:
        """Validate and sanitize RPC request inputs"""

## Regex patterns

        HOSTNAME_PATTERN = re.compile(r'^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)*$')
        IPv4_PATTERN = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)

        @staticmethod
        def validate_hostname(hostname):
            """Validate hostname format"""
            if not isinstance(hostname, str) or len(hostname) > 253:
                raise ValueError(f'Invalid hostname: {hostname}')
            if not RequestValidator.HOSTNAME_PATTERN.match(hostname):
                raise ValueError(f'Invalid hostname format: {hostname}')
            return hostname

        @staticmethod
        def validate_ipv4(ip):
            """Validate IPv4 address"""
            if not isinstance(ip, str):
                raise ValueError('IP must be a string')
            if not RequestValidator.IPv4_PATTERN.match(ip):
                raise ValueError(f'Invalid IPv4 address: {ip}')

## Check each octet is 0-255

            octets = [int(x) for x in ip.split('.')]
            if any(x > 255 for x in octets):
                raise ValueError(f'Invalid IPv4 address: {ip}')
            return ip

        @staticmethod
        def validate_uuid(uuid_str):
            """Validate UUID format"""
            try:
                UUID(uuid_str)
                return uuid_str
            except (ValueError, AttributeError):
                raise ValueError(f'Invalid UUID: {uuid_str}')

        @staticmethod
        def validate_label(label, max_length=256):
            """Validate snapshot/pool label"""
            if not isinstance(label, str) or len(label) == 0:
                raise ValueError('Label must be a non-empty string')
            if len(label) > max_length:
                raise ValueError(f'Label too long (max {max_length} characters)')

## Only allow alphanumeric, hyphens, underscores

            if not re.match(r'^[a-zA-Z0-9_-]+$', label):
                raise ValueError(f'Label contains invalid characters: {label}')
            return label

        @staticmethod
        def validate_permission_spec(perm_spec):
            """Validate permission specification string"""

## Format: "service:resource:action" or "service:*" or "*"

            if perm_spec == '*':
                return perm_spec
            parts = perm_spec.split(':')
            if len(parts)  3:
                raise ValueError(f'Invalid permission spec: {perm_spec}')
            for part in parts:
                if part != '*' and not re.match(r'^[a-z][a-z0-9_]*$', part):
                    raise ValueError(f'Invalid permission spec: {perm_spec}')
            return perm_spec

## Usage in service handlers

    class NodeServiceImpl(debvisor_pb2_grpc.NodeServiceServicer):
        def RegisterNode(self, request, context):
            try:

## Validate inputs

                hostname = RequestValidator.validate_hostname(request.hostname)
                ip = RequestValidator.validate_ipv4(request.ip)

## Process request

                node = self._register_node(hostname, ip)

                return NodeAck(status=STATUS_OK, message='Node registered')

            except ValueError as e:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, 'Registration failed')

## 4. Rate Limiting & Quota Management

## services/rpc/rate_limiting.py

    import time
    import threading
    from collections import defaultdict, deque

    class RateLimiter:
        """Rate limiter with per-principal and global limits"""

        def**init**(self, global_rps=1000, per_principal_rps=100):
            self.global_rps = global_rps
            self.per_principal_rps = per_principal_rps

            self.global_requests = deque()
            self.principal_requests = defaultdict(deque)
            self.lock = threading.Lock()

        def is_allowed(self, principal, operation_cost=1):
            """Check if request from principal is allowed"""
            with self.lock:
                now = time.time()

## Check global rate limit

## Remove requests older than 1 second

                while self.global_requests and (now - self.global_requests[0]) > 1.0:
                    self.global_requests.popleft()

                if len(self.global_requests) >= self.global_rps:
                    return False, "Global rate limit exceeded"

## Check per-principal rate limit

                principal_deque = self.principal_requests[principal]
                while principal_deque and (now - principal_deque[0]) > 1.0:
                    principal_deque.popleft()

                if len(principal_deque) >= self.per_principal_rps:
                    return False, f"Rate limit exceeded for {principal}"

## Allow request

                self.global_requests.append(now)
                principal_deque.append(now)

                return True, ""

    class QuotaManager:
        """Manage per-principal quotas (e.g., snapshot count, total storage)"""

        def**init**(self, etcd_client):
            self.etcd = etcd_client
            self.quota_prefix = '/debvisor/rpc/quotas/'

        def get_quota(self, principal, resource_type):
            """Get quota for principal"""
            try:
                value = self.etcd.get(f'{self.quota_prefix}{principal}/{resource_type}')
                return json.loads(value[0])
            except:
                return self.default_quota(resource_type)

        def default_quota(self, resource_type):
            """Default quota values"""
            return {
                'snapshots': 100,
                'storage_gb': 1000,
                'concurrent_operations': 5,
            }.get(resource_type, 0)

        def check_quota(self, principal, resource_type, amount=1):
            """Check if principal has quota for operation"""
            quota = self.get_quota(principal, resource_type)

## In production, track actual usage

            return amount <= quota.get('limit', self.default_quota(resource_type))

        def consume_quota(self, principal, resource_type, amount=1):
            """Consume quota for operation"""

## Implementation depends on quota type and tracking mechanism

            pass

## Interceptor using rate limiter

    class RateLimitingInterceptor(grpc.ServerInterceptor):
        def**init**(self, rate_limiter):
            self.rate_limiter = rate_limiter

        def intercept_service(self, continuation, handler_call_details):
            principal = self._extract_principal(handler_call_details)
            allowed, message = self.rate_limiter.is_allowed(principal)

            if not allowed:
                return grpc.unary_unary_rpc_terminator(
                    grpc.StatusCode.RESOURCE_EXHAUSTED,
                    message,
                )

            return continuation(handler_call_details)

## Implementation Checklist

### Security Implementation

- [ ] TLS 1.3+ enabled for all connections
- [ ] Server certificate signed by internal CA
- [ ] Client authentication enabled (mTLS or API keys)
- [ ] Certificate rotation automated (monthly)
- [ ] API keys stored as hashes (never plain text)
- [ ] API key rotation policy enforced (quarterly)
- [ ] Rate limiting configured (global and per-principal)
- [ ] Input validation on all RPC parameters
- [ ] Size limits enforced (requests < 1MB, responses < 10MB)
- [ ] Timeout configured (requests must complete in < 5 minutes)
- [ ] Error messages don't expose internals

### Audit & Logging

- [ ] All authentication attempts logged
- [ ] All RPC calls logged (principal, method, timestamp)
- [ ] All permission denials logged
- [ ] Rate limit violations logged
- [ ] Errors logged with trace IDs
- [ ] Audit log written to /var/log/debvisor/rpc-audit.log
- [ ] Audit log rotated daily (keep 30 days)
- [ ] Sensitive data redacted from logs (API keys, passwords)
- [ ] Monitoring alerts configured for:
- Authentication failures (> 5/minute)
- Permission denials (> 10/minute)
- Rate limit violations (> 20/minute)
- Errors (> 1%  error rate)

### Operational Readiness

- [ ] Health check endpoint (/healthz) available
- [ ] Metrics exposed (Prometheus format)
- [ ] Graceful shutdown (drain existing requests)
- [ ] systemd service unit configured
- [ ] Resource limits set (memory, CPU)
- [ ] Backup/restore procedures documented
- [ ] Disaster recovery plan documented
- [ ] Runbooks created for common scenarios:
- Certificate expiration
- Service restart
- Key rotation
- Troubleshooting failed RPC calls

## Monitoring & Alerts

### Key Metrics

## services/rpc/metrics.py

    from prometheus_client import Counter, Histogram, Gauge

## Request metrics

    rpc_requests_total = Counter(
        'rpc_requests_total',
        'Total RPC requests',
        ['service', 'method', 'status']
    )

    rpc_request_duration_seconds = Histogram(
        'rpc_request_duration_seconds',
        'RPC request duration',
        ['service', 'method']
    )

## Authentication metrics

    auth_attempts_total = Counter(
        'auth_attempts_total',
        'Authentication attempts',
        ['method', 'result']  # result: success, failure
    )

## Authorization metrics

    authz_denials_total = Counter(
        'authz_denials_total',
        'Authorization denials',
        ['principal', 'permission']
    )

## Rate limiting metrics

    rate_limit_violations_total = Counter(
        'rate_limit_violations_total',
        'Rate limit violations',
        ['principal']
    )

## System metrics

    rpc_service_status = Gauge(
        'rpc_service_status',
        'RPC service status',
        value=1  # 1=ready, 0=degraded
    )

    backend_connection_errors_total = Counter(
        'backend_connection_errors_total',
        'Backend connection errors',
        ['backend_service']  # ceph, k8s, libvirt
    )

## Alert Rules

## prometheus-rules.yml

    groups:

- name: rpc-service

        rules:

- alert: HighAuthenticationFailureRate

            expr: rate(auth_attempts_total{result="failure"}[5m]) > 0.1
            for: 5m
            annotations:
              summary: "High authentication failure rate ({{ $value }}/sec)"
              action: "Check client credentials and network connectivity"

- alert: HighRateLimitViolations

            expr: rate(rate_limit_violations_total[5m]) > 0.5
            for: 5m
            annotations:
              summary: "High rate limit violations"
              action: "Check for malicious clients or legitimate traffic spike"

- alert: RpcErrorRate

            expr: rate(rpc_requests_total{status="error"}[5m]) > 0.01
            for: 5m
            annotations:
              summary: "RPC error rate > 1%"
              action: "Check server logs and backend service health"

- alert: BackendConnectionError

            expr: increase(backend_connection_errors_total[5m]) > 0
            for: 1m
            annotations:
              summary: "Cannot connect to {{ $labels.backend_service }}"
              action: "Check {{ $labels.backend_service }} service status"

## References

- Proto definitions: `proto/debvisor.proto`
- Original README: `README.md`
- Related: `opt/web/panel/SECURITY.md`,`opt/config/CONFIG_IMPROVEMENTS.md`
