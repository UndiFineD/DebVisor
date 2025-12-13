# DebVisor Web Panel - Security Hardening Guide\n\nThis document provides comprehensive

security

guidance for the DebVisor web panel (`opt/web/panel/app.py`), including
authentication,
authorization, HTTPS/TLS, CSRF protection, input validation, and audit
logging.\n\n##
Table of
Contents\n\n1. Overview\n\n1. Authentication\n\n1. Authorization\n\n1. HTTPS/TLS
Configuration\n\n1.
Session Management\n\n1. CSRF Protection\n\n1. Input Validation & Output
Escaping\n\n1.
Audit
Logging\n\n1. Rate Limiting & DDoS Protection\n\n1. Security Headers\n\n1. Error
Handling\n\n1.
Deployment Security Checklist\n\n## Overview\n\nThe DebVisor web panel is a
Flask-based
web
interface for cluster management. Security is critical because:\n\n- **High
Privilege**:
Panel
operations can modify cluster state (storage, networking, VM management)\n\n-
**Sensitive
Data**:
Credentials, keys, configuration details must be protected\n\n- **Audit
Requirements**:
All
state-changing operations must be logged for compliance\n\n- **Multi-user
Access**:
Different users
need different permission levels\n\n### Security Architecture\n\n +-------------+\n |
Browser |\n
+------+------+\n | HTTPS/TLS 1.3+\n | (browser -> panel)\n ?\n
+-----------------------------+\n |
Flask Web Panel (app.py) |\n +-----------------------------+\n | +- CSRF Token Validation
|\n | +-
Input Validation |\n | +- Authentication (Session) |\n | +- Authorization (RBAC) |\n | +-
Audit
Logging |\n +----------+------------------+\n | gRPC + mTLS\n | (panel -> RPC service)\n
?\n
+------------------------------+\n | debvisor-rpcd (RPC Service) |\n | +- Authentication
(mTLS) |\n
| +- Authorization (RBAC) |\n | +- Audit Logging |\n +------------------------------+\n\n##
Authentication\n\n### Overview [2]\n\nThe web panel supports multiple
authentication
methods:\n1.**Local Authentication**: Username/password with secure
hashing\n1.**RPC
Service
Identity**: Tie panel user to RPC service credentials\n1.**LDAP/AD**(Optional):
Enterprise
directory
integration\n1.**OIDC/OAuth2**(Implemented): External identity provider\n\n###
Local
Authentication
(Initial Implementation)\n\n## app.py - Local authentication\n\n from
werkzeug.security
import
generate_password_hash, check_password_hash\n from flask_login import UserMixin,
LoginManager\n
import secrets\n import hashlib\n class User(UserMixin):\n """User model with
secure
password
handling"""\n def**init**(self, username, password_hash, role='viewer'):\n
self.username =
username\n self.password_hash = password_hash\n self.role = role\n
self.created_at =
datetime.utcnow()\n self.last_login = None\n self.mfa_enabled = False\n
self.mfa_secret =
None\n
@staticmethod\n def set_password(password):\n """Hash password with argon2 or
bcrypt"""\n\n##
Requires: pip install argon2-cffi\n\n return generate_password_hash(password,
method='argon2')\n def
check_password(self, password):\n """Verify password"""\n return
check_password_hash(self.password_hash, password)\n def get_id(self):\n
"""Return username
as unique
identifier"""\n return self.username\n\n## Flask-Login configuration\n\n
login_manager =
LoginManager()\n login_manager.login_view = 'login'\n
login_manager.session_protection =
'strong'\n
@login_manager.user_loader\n def load_user(user_id):\n """Load user from
database"""\n
return
User.query.get(user_id)\n\n## Login route\n\n @app.route('/login',
methods=['GET',
'POST'])\n def
login():\n """Secure login with rate limiting"""\n if request.method ==
'POST':\n username
=
request.form.get('username', '').strip()\n password =
request.form.get('password',
'')\n\n##
Validate input\n\n if not username or not password:\n flash('Username and
password
required',
'error')\n return redirect(url_for('login'))\n\n## Rate limiting check
(implemented via
RateLimiter)\n\n if rate_limiter.check_limit(f'login:{request.remote_addr}', 5,
300):\n
flash('Too
many login attempts. Try again in 5 minutes.', 'error')\n return
redirect(url_for('login'))\n\n##
User lookup\n\n user = User.query.filter_by(username=username).first()\n if user
and
user.check_password(password):\n login_user(user,
remember=request.form.get('remember_me'))\n
audit_log('AUTH', f'User {username} logged in')\n return
redirect(url_for('dashboard'))\n
else:\n\n## Log failed attempt\n\n audit_log('AUTH_FAILED', f'Failed login
attempt for
{username}',\n extra={'ip': request.remote_addr})\n flash('Invalid username or
password',
'error')\n
return render_template('login.html')\n @app.route('/logout')\n @login_required\n
def
logout():\n
"""Logout and clear session"""\n username = current_user.username\n
logout_user()\n
audit_log('AUTH', f'User {username} logged out')\n return
redirect(url_for('login'))\n\n##
Password
Policy\n\n### Requirements\n\n- Minimum 12 characters\n\n- Mix of uppercase,
lowercase,
digits,
special characters\n\n- No dictionary words or keyboard patterns\n\n- No
username in
password\n\n-
No more than 3 repeated characters\n\n import re\n class PasswordValidator:\n
"""Validate
password
strength"""\n MIN_LENGTH = 12\n SPECIAL*CHARS =
r'[!@#$%^&*()*+\-=\[\]{};:\'",.<>?/\\|`~]'\n
@staticmethod\n def validate(password, username):\n """Validate password meets
requirements"""\n
errors = []\n\n## Length\n\n if len(password)  response.json())\n .then(data =>
console.log('Success:', data));\n\n## Input Validation & Output Escaping\n\n###
Input
Validation\n\n
import re\n from urllib.parse import urlparse\n class InputValidator:\n
"""Validate user
input"""\n\n## Patterns for common inputs\n\n PATTERNS = {\n 'hostname':
r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$',\n 'ipv4': r'^(\d{1,3}\.){3}\d{1,3}$',\n
'uuid':
r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',\n
'snapshot*name':
r'^[a-zA-Z0-9*-]{1,64}$',\n 'pool*name': r'^[a-zA-Z0-9*-]{1,32}$',\n }\n
@staticmethod\n
def
validate_hostname(hostname):\n """Validate hostname format"""\n if not hostname
or
len(hostname) >
253:\n return False\n return bool(re.match(InputValidator.PATTERNS['hostname'],
hostname))\n
@staticmethod\n def validate_ipv4(ip):\n """Validate IPv4 address"""\n if not
re.match(InputValidator.PATTERNS['ipv4'], ip):\n return False\n parts =
ip.split('.')\n
return all(0
= 32 or c in '\t\n\r')\n\n## Truncate\n\n return
value[:max_length]\n\n##
Usage in routes [2]\n\n @app.route('/api/snapshots', methods=['POST'])\n
@login_required\n
@require_permission('storage:write')\n def create_snapshot():\n """Create
storage
snapshot"""\n
pool_name = request.form.get('pool', '').strip()\n snapshot_name =
request.form.get('snapshot',
'').strip()\n\n## Input validation [2]\n\n if not
InputValidator.validate_pool_name(pool_name):\n
return jsonify({'error': 'Invalid pool name'}), 400\n if not
InputValidator.validate_snapshot_name(snapshot_name):\n return jsonify({'error':
'Invalid
snapshot
name'}), 400\n\n## Sanitize description\n\n description =
InputValidator.sanitize_string(request.form.get('description', ''))\n\n## Call
RPC
service\n\n
result = rpc_client.create_snapshot(pool_name, snapshot_name)\n
audit_log('AUDIT', f'User
{current_user.username} created snapshot',\n extra={'pool': pool_name,
'snapshot':
snapshot_name})\n
return jsonify(result)\n\n## Output Escaping\n\n from markupsafe import escape\n
from
jinja2 import
Markup\n\n## Automatically escapes in Jinja2 templates\n\n## {{ variable }} is
automatically
HTML-escaped\n\n @app.route('/nodes/')\n @login_required\n def
node_details(node_id):\n
"""Node
details page"""\n node_info = rpc_client.get_node_info(node_id)\n\n## All
variables
auto-escaped in
template\n\n return render_template('node.html', node=node_info)\n\n## Template:
templates/node.html\n\n """\n Node: {{ node.hostname }}\n Status: {{ node.status
}}\n {{
node.config
}} -->\n """\n\n## For JavaScript context (if needed)\n\n import json\n
@app.route('/api/node//json')\n @login_required\n def node_json(node_id):\n
"""Node info
as JSON
(already escaped by json.dumps)"""\n node_info =
rpc_client.get_node_info(node_id)\n
return
jsonify(node_info)\n\n## Escape user-provided content for display\n\n def
safe_display(user_content):\n """Safely display user-provided content"""\n
return
escape(user_content)\n\n## Audit Logging\n\n### Audit Event Format\n\n import
json\n from
datetime
import datetime\n import logging\n class AuditLogger:\n """Comprehensive audit
logging"""\n
def**init**(self, log_file='/var/log/debvisor/panel-audit.log'):\n self.logger =
logging.getLogger('debvisor.panel.audit')\n handler =
logging.FileHandler(log_file)\n
formatter =
logging.Formatter('%(message)s')\n handler.setFormatter(formatter)\n
self.logger.addHandler(handler)\n self.logger.setLevel(logging.INFO)\n def
log(self,
event_type,
user, action, result='success', extra=None):\n """Log audit event"""\n event =
{\n
'timestamp':
datetime.utcnow().isoformat(),\n 'event_type': event_type,\n 'user': user,\n
'action':
action,\n
'result': result,\n 'source_ip': request.remote_addr,\n 'user_agent':
request.headers.get('User-Agent', ''),\n }\n if extra:\n event['extra'] =
extra\n\n##
Redact
sensitive data\n\n event_json = json.dumps(event)\n event_json =
event_json.replace('"password"',
'"password":"***"')\n event_json = event_json.replace('"token"',
'"token":"***"')\n
event_json =
event_json.replace('"key"', '"key":"***"')\n self.logger.info(event_json)\n
audit =
AuditLogger()\n
def audit_log(event_type, action, result='success', extra=None):\n
"""Convenience function
to log
audit events"""\n if current_user:\n username = current_user.username\n else:\n
username =
'anonymous'\n audit.log(event_type, username, action, result, extra)\n\n## Audit
event
types\n\n
AUDIT_EVENTS = {\n 'AUTH': 'Authentication event (login/logout)',\n
'AUTH_FAILED': 'Failed
authentication attempt',\n 'AUTHZ_DENIED': 'Authorization denial',\n 'AUDIT':
'Auditable
action
(state change)',\n 'SECURITY': 'Security-related event (password change, MFA,
etc)',\n
'ERROR':
'Error condition',\n 'SUSPICIOUS': 'Suspicious activity detected',\n }\n\n##
Example Audit
Logs\n\n
{\n "timestamp": "2025-01-15T10:30:45.123456Z",\n "event_type": "AUTH",\n
"user":
"alice",\n
"action": "User alice logged in",\n "result": "success",\n "source_ip":
"192.168.1.100",\n
"user_agent": "Mozilla/5.0..."\n }\n {\n "timestamp":
"2025-01-15T10:31:20.654321Z",\n
"event_type":
"AUDIT",\n "user": "alice",\n "action": "User alice restarted node node-001",\n
"result":
"success",\n "source_ip": "192.168.1.100",\n "extra": {\n "node_id":
"node-001",\n
"rpc_status":
"ok"\n }\n }\n {\n "timestamp": "2025-01-15T10:32:00.000000Z",\n "event_type":
"AUTHZ_DENIED",\n
"user": "bob",\n "action": "Access denied for bob",\n "result": "denied",\n
"source_ip":
"192.168.1.101",\n "extra": {\n "required_permission": "nodes:modify",\n
"user_role":
"viewer"\n }\n
}\n\n## Rate Limiting & DDoS Protection\n\n from flask_limiter import Limiter\n
from
flask_limiter.util import get_remote_address\n from redis import Redis\n\n##
Redis-backed
rate
limiting for distributed deployments\n\n redis_client = Redis(host='localhost',
port=6379,
db=0)\n
limiter = Limiter(\n app=app,\n key_func=get_remote_address,\n
storage_uri='redis://localhost:6379',\n default_limits=['200 per day', '50 per
hour'],\n
strategy='fixed-window-elastic-expiry',\n )\n\n## Rate limit specific routes\n\n
@app.route('/login', methods=['POST'])\n @limiter.limit('5 per minute')\n def
login():\n
"""Login
with strict rate limiting"""\n pass\n @app.route('/api/nodes',
methods=['GET'])\n
@login_required\n
@limiter.limit('100 per minute')\n def list_nodes():\n """List nodes with
per-user rate
limiting"""\n pass\n\n## Custom rate limiting per user\n\n class
PerUserRateLimiter:\n
"""Rate limit
per authenticated user"""\n def**init**(self, redis_client):\n self.redis =
redis_client\n
self.default_limits = {\n 'admin': 1000, # 1000 req/min for admin\n 'operator':
500, # 500
req/min
for operator\n 'developer': 200, # 200 req/min for developer\n 'viewer': 100, #
100
req/min for
viewer\n }\n def check_limit(self, user, role):\n """Check if user is within
rate
limit"""\n limit =
self.default_limits.get(role, 100)\n key =
f'ratelimit:{user}:{int(time.time())}'\n count
=
self.redis.incr(key)\n if count == 1:\n self.redis.expire(key, 60) # 1-minute
window\n
return count
<= limit\n per_user_limiter = PerUserRateLimiter(redis_client)\n
@app.before_request\n
@login_required\n def check_rate_limit():\n """Check rate limit for each
request"""\n if
not
per_user_limiter.check_limit(current_user.username, current_user.role):\n
audit_log('SUSPICIOUS',
f'Rate limit exceeded for {current_user.username}')\n abort(429) # Too Many
Requests\n\n##
Security
Headers\n\n## app.py - Security headers\n\n @app.after_request\n def
set_security_headers(response):\n """Set security headers on every
response"""\n\n##
Prevent
clickjacking\n\n response.headers['X-Frame-Options'] = 'DENY'\n\n## Prevent MIME
type
sniffing\n\n
response.headers['X-Content-Type-Options'] = 'nosniff'\n\n## Enable XSS
protection\n\n
response.headers['X-XSS-Protection'] = '1; mode=block'\n\n## Content Security
Policy\n\n
response.headers['Content-Security-Policy'] = (\n "default-src 'self'; "\n
"script-src
'self'; "\n
"style-src 'self' 'unsafe-inline'; " # Allow inline styles for Bootstrap etc\n
"img-src
'self'
data:; "\n "font-src 'self'; "\n "connect-src 'self'; "\n "frame-ancestors
'none'; "\n
"base-uri
'self'; "\n "form-action 'self'"\n )\n\n## Referrer policy\n\n
response.headers['Referrer-Policy'] =
'strict-origin-when-cross-origin'\n\n## Permissions policy\n\n
response.headers['Permissions-Policy'] = (\n 'accelerometer=(), '\n 'camera=(),
'\n
'geolocation=(),
'\n 'gyroscope=(), '\n 'magnetometer=(), '\n 'microphone=(), '\n 'payment=(),
'\n
'usb=()'\n )\n\n##
HSTS (HTTP Strict-Transport-Security)\n\n
response.headers['Strict-Transport-Security'] =
'max-age=31536000; includeSubDomains; preload'\n return response\n\n## Error
Handling\n\n## app.py -
Error handling\n\n @app.errorhandler(400)\n def bad_request(error):\n """Bad
request
error"""\n
audit_log('ERROR', 'Bad request', extra={'error': str(error)})\n return
render_template('error.html',\n code=400,\n message='Bad Request',\n detail='The
server
could not
understand the request.'), 400\n @app.errorhandler(403)\n def
forbidden(error):\n
"""Forbidden
error"""\n audit_log('AUTHZ_DENIED', 'Forbidden access attempt')\n return
render_template('error.html',\n code=403,\n message='Forbidden',\n detail='You
do not have
permission to access this resource.'), 403\n @app.errorhandler(404)\n def
not_found(error):\n """Not
found error"""\n return render_template('error.html',\n code=404,\n message='Not
Found',\n
detail='The requested resource was not found.'), 404\n @app.errorhandler(500)\n
def
internal_error(error):\n """Internal server error"""\n audit_log('ERROR',
'Internal server
error',
extra={'error': str(error)})\n return render_template('error.html',\n
code=500,\n
message='Internal
Server Error',\n detail='An unexpected error occurred.'), 500\n
@app.errorhandler(503)\n
def
service_unavailable(error):\n """Service unavailable (RPC service down)"""\n
audit_log('ERROR', 'RPC
service unavailable')\n return render_template('error.html',\n code=503,\n
message='Service
Unavailable',\n detail='Cluster management service is temporarily unavailable.
Try again
later.'),
503\n\n## RPC service health check\n\n @app.route('/health')\n def
health_check():\n
"""Health check
endpoint for load balancers"""\n try:\n\n## Quick RPC service check\n\n
rpc_client.health_check()\n
return jsonify({'status': 'healthy'}), 200\n except Exception as e:\n return
jsonify({'status':
'unhealthy', 'error': str(e)}), 503\n\n## Deployment Security Checklist\n\nUse
this
checklist before
deploying to production:\n\n### Authentication & Authorization\n\n- [] User
authentication
implemented (local, LDAP, OIDC)\n\n- [] MFA enabled for admin/operator
roles\n\n- []
Passwords
validated per policy (12+ chars, mix of types)\n\n- [] RBAC roles defined and
tested
(admin,
operator, developer, viewer)\n\n- [] Permission checks on all state-changing
operations\n\n- []
Service account permissions minimal (principle of least privilege)\n\n###
HTTPS/TLS\n\n-
[] HTTPS
enforced (HTTP redirects to HTTPS)\n\n- [] TLS 1.3 or 1.2 only (no SSL/TLS
1.0/1.1)\n\n-
[] Strong
ciphers configured\n\n- [] Certificate valid and not expired\n\n- [] Certificate
pinning
considered
for internal clients\n\n- [] Client certificate authentication considered for
sensitive
operations\n\n### Session Management [2]\n\n- [] Session cookies secure (HTTPS
only)\n\n-
[] Session
cookies HttpOnly (no JavaScript access)\n\n- [] Session cookies SameSite=Lax
(CSRF
protection)\n\n-
[] Session timeout configured (8 hours default)\n\n- [] Session token
regeneration on
login\n\n- []
Session invalidation on logout\n\n### CSRF Protection [2]\n\n- [] CSRF tokens
generated
for all
forms\n\n- [] CSRF tokens validated on POST/PUT/DELETE\n\n- [] CSRF tokens
short-lived
(match
session lifetime)\n\n- [] Double-submit cookie pattern considered\n\n### Input
Validation
[2]
[2]\n\n- [] All user input validated (type, length, format)\n\n- [] Whitelist
approach
(accept known
good input)\n\n- [] Special characters escaped or rejected\n\n- [] SQL injection
prevention
(parameterized queries)\n\n- [] Command injection prevention (avoid shell
execution)\n\n### Output
Escaping [2]\n\n- [] HTML output escaped (prevent XSS)\n\n- [] JavaScript
context handled
safely\n\n- [] JSON output properly formatted\n\n- [] User-provided content
never
trusted\n\n###
Audit Logging [2]\n\n- [] All authentication attempts logged
(success/failure)\n\n- [] All
authorization denials logged\n\n- [] All state-changing operations logged\n\n-
[]
Sensitive data
redacted from logs (passwords, tokens, keys)\n\n- [] Audit logs stored securely
with
restricted
access\n\n- [] Audit logs monitored for suspicious patterns\n\n- [] Audit log
retention
policy
(e.g., 90 days)\n\n### Rate Limiting & DDoS\n\n- [] Rate limiting on login
endpoint (5 per
minute)\n\n- [] Rate limiting on API endpoints (100-1000 per minute per
user)\n\n- [] Rate
limiting
per user role (viewer < developer < operator < admin)\n\n- [] DDoS protection
configured
(WAF,
reverse proxy)\n\n- [] Health check endpoint for load balancer\n\n### Security
Headers
[2]\n\n- []
X-Frame-Options: DENY (prevent clickjacking)\n\n- [] X-Content-Type-Options:
nosniff
(prevent MIME
sniffing)\n\n- [] X-XSS-Protection: 1; mode=block (XSS protection)\n\n- []
Content-Security-Policy
configured\n\n- [] Referrer-Policy configured\n\n- [] Permissions-Policy
configured\n\n-
[] HSTS
header configured\n\n### Error Handling [2]\n\n- [] Generic error messages (no
sensitive
details to
users)\n\n- [] Detailed error logs (for debugging)\n\n- [] Error pages don't
leak system
information\n\n- [] 4xx/5xx error handlers implemented\n\n- [] RPC service
availability
errors
handled gracefully\n\n### Dependencies & Patching\n\n- [] All Python packages
pinned to
specific
versions\n\n- [] No vulnerable package versions (check with `pip-audit`)\n\n- []
Security
patches
applied immediately\n\n- [] Changelog monitored for upstream
vulnerabilities\n\n###
Monitoring &
Alerting\n\n- [] Authentication failures monitored (alert on spikes)\n\n- []
Authorization
denials
monitored\n\n- [] Rate limit violations monitored\n\n- [] RPC service
unavailability
alerted\n\n- []
Application errors logged and alerted\n\n- [] Disk space for audit logs
monitored\n\n###
Systemd
Service Security\n\n- [] Service runs as unprivileged user (www-data)\n\n- []
ProtectSystem=strict
enabled\n\n- [] ProtectHome=yes enabled\n\n- [] NoNewPrivileges=yes enabled\n\n-
[]
PrivateDevices=yes enabled\n\n- [] RestrictNamespaces=yes enabled\n\n- []
CapabilityBoundingSet
empty (no capabilities)\n\n- [ ] Resource limits configured (memory, CPU,
tasks)\n\n-
--\n\n### Next
Steps\n\n1. Review this guide with your security team\n\n1. Implement
authentication/authorization
methods appropriate for your environment\n\n1. Configure TLS certificates
(self-signed for
lab,
CA-signed for production)\n\n1. Deploy to test environment and run security
scan\n\n1.
Review audit
logs for patterns\n\n1. Harden based on findings before production
deployment\n\n
