# DebVisor Web Panel - Security Hardening Guide

This document provides comprehensive security guidance for the DebVisor web panel (`opt/web/panel/app.py`), including authentication, authorization, HTTPS/TLS, CSRF protection, input validation, and audit logging.

## Table of Contents

1. Overview
1. Authentication
1. Authorization
1. HTTPS/TLS Configuration
1. Session Management
1. CSRF Protection
1. Input Validation & Output Escaping
1. Audit Logging
1. Rate Limiting & DDoS Protection
1. Security Headers
1. Error Handling
1. Deployment Security Checklist

## Overview

The DebVisor web panel is a Flask-based web interface for cluster management. Security is critical because:

-__High Privilege__: Panel operations can modify cluster state (storage, networking, VM management)
-__Sensitive Data__: Credentials, keys, configuration details must be protected
-__Audit Requirements__: All state-changing operations must be logged for compliance
-__Multi-user Access__: Different users need different permission levels

### Security Architecture

    ┌─────────────┐
    │   Browser   │
    └──────┬──────┘
           │ HTTPS/TLS 1.3+
           │ (browser → panel)
           ▼
    ┌─────────────────────────────┐
    │   Flask Web Panel (app.py)  │
    ├─────────────────────────────┤
    │ ├─ CSRF Token Validation    │
    │ ├─ Input Validation         │
    │ ├─ Authentication (Session)  │
    │ ├─ Authorization (RBAC)      │
    │ └─ Audit Logging            │
    └──────────┬──────────────────┘
               │ gRPC + mTLS
               │ (panel → RPC service)
               ▼
    ┌──────────────────────────────┐
    │  debvisor-rpcd (RPC Service) │
    │  ├─ Authentication (mTLS)    │
    │  ├─ Authorization (RBAC)     │
    │  └─ Audit Logging           │
    └──────────────────────────────┘

## Authentication

### Overview [2]

The web panel supports multiple authentication methods:

1.__Local Authentication__: Username/password with secure hashing
1.__RPC Service Identity__: Tie panel user to RPC service credentials
1.__LDAP/AD__(Optional): Enterprise directory integration
1.__OIDC/OAuth2__(Implemented): External identity provider

### Local Authentication (Initial Implementation)

## app.py - Local authentication

    from werkzeug.security import generate_password_hash, check_password_hash
    from flask_login import UserMixin, LoginManager
    import secrets
    import hashlib

    class User(UserMixin):
        """User model with secure password handling"""

        def__init__(self, username, password_hash, role='viewer'):
            self.username = username
            self.password_hash = password_hash
            self.role = role
            self.created_at = datetime.utcnow()
            self.last_login = None
            self.mfa_enabled = False
            self.mfa_secret = None

        @staticmethod
        def set_password(password):
            """Hash password with argon2 or bcrypt"""

## Requires: pip install argon2-cffi

            return generate_password_hash(password, method='argon2')

        def check_password(self, password):
            """Verify password"""
            return check_password_hash(self.password_hash, password)

        def get_id(self):
            """Return username as unique identifier"""
            return self.username

## Flask-Login configuration

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.session_protection = 'strong'

    @login_manager.user_loader
    def load_user(user_id):
        """Load user from database"""
        return User.query.get(user_id)

## Login route

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Secure login with rate limiting"""
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

## Validate input

            if not username or not password:
                flash('Username and password required', 'error')
                return redirect(url_for('login'))

## Rate limiting check (implemented via RateLimiter)

            if rate_limiter.check_limit(f'login:{request.remote_addr}', 5, 300):
                flash('Too many login attempts. Try again in 5 minutes.', 'error')
                return redirect(url_for('login'))

## User lookup

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user, remember=request.form.get('remember_me'))
                audit_log('AUTH', f'User {username} logged in')
                return redirect(url_for('dashboard'))
            else:

## Log failed attempt

                audit_log('AUTH_FAILED', f'Failed login attempt for {username}',
                         extra={'ip': request.remote_addr})
                flash('Invalid username or password', 'error')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        """Logout and clear session"""
        username = current_user.username
        logout_user()
        audit_log('AUTH', f'User {username} logged out')
        return redirect(url_for('login'))

## Password Policy

### Requirements

- Minimum 12 characters
- Mix of uppercase, lowercase, digits, special characters
- No dictionary words or keyboard patterns
- No username in password
- No more than 3 repeated characters

    import re

    class PasswordValidator:
        """Validate password strength"""

        MIN_LENGTH = 12
        SPECIAL_CHARS = r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]'

        @staticmethod
        def validate(password, username):
            """Validate password meets requirements"""
            errors = []

## Length

            if len(password) < PasswordValidator.MIN_LENGTH:
                errors.append(f'Password must be at least {PasswordValidator.MIN_LENGTH} characters')

## Character types

            if not re.search(r'[A-Z]', password):
                errors.append('Password must contain uppercase letters')
            if not re.search(r'[a-z]', password):
                errors.append('Password must contain lowercase letters')
            if not re.search(r'[0-9]', password):
                errors.append('Password must contain digits')
            if not re.search(PasswordValidator.SPECIAL_CHARS, password):
                errors.append('Password must contain special characters')

## Username check

            if username.lower() in password.lower():
                errors.append('Password cannot contain username')

## Repeated characters

            if re.search(r'(.)\1{3,}', password):
                errors.append('Password cannot contain 4+ repeated characters')

            return errors

## Usage

    @app.route('/change-password', methods=['POST'])
    @login_required
    def change_password():
        """Change user password"""
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

## Verify old password

        if not current_user.check_password(old_password):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('settings'))

## Validate new password

        errors = PasswordValidator.validate(new_password, current_user.username)
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('settings'))

## Passwords match

        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('settings'))

## Update password

        current_user.password_hash = User.set_password(new_password)
        db.session.commit()

        audit_log('SECURITY', f'User {current_user.username} changed password')
        flash('Password changed successfully', 'success')
        return redirect(url_for('settings'))

## Multi-Factor Authentication (MFA)

    import pyotp
    import qrcode
    from io import BytesIO
    import base64

    class MFAManager:
        """Manage multi-factor authentication"""

        @staticmethod
        def generate_secret():
            """Generate TOTP secret"""
            return pyotp.random_base32()

        @staticmethod
        def get_qr_code(username, secret):
            """Generate QR code for TOTP setup"""
            totp = pyotp.TOTP(secret)
            uri = totp.provisioning_uri(name=username, issuer_name='DebVisor')

            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(uri)
            qr.make(fit=True)

            img = qr.make_image(fill_color='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            return base64.b64encode(buffer.getvalue()).decode()

        @staticmethod
        def verify_totp(secret, token):
            """Verify TOTP token"""
            totp = pyotp.TOTP(secret)

## Allow +/- 1 time window for clock skew

            return totp.verify(token, valid_window=1)

    @app.route('/mfa/setup', methods=['GET', 'POST'])
    @login_required
    def setup_mfa():
        """Setup MFA for user"""
        if request.method == 'POST':
            secret = request.form.get('secret')
            token = request.form.get('token')

## Verify token

            if not MFAManager.verify_totp(secret, token):
                flash('Invalid TOTP token', 'error')
                return redirect(url_for('setup_mfa'))

## Save secret

            current_user.mfa_enabled = True
            current_user.mfa_secret = secret
            db.session.commit()

            audit_log('SECURITY', f'User {current_user.username} enabled MFA')
            flash('MFA enabled successfully', 'success')
            return redirect(url_for('settings'))

## Generate new secret

        secret = MFAManager.generate_secret()
        qr_code = MFAManager.get_qr_code(current_user.username, secret)

        return render_template('setup_mfa.html', secret=secret, qr_code=qr_code)

## Login with MFA

    @app.route('/login/mfa', methods=['POST'])
    def login_mfa():
        """Verify MFA during login"""
        username = session.get('username_pending')
        if not username:
            return redirect(url_for('login'))

        token = request.form.get('token', '')
        user = User.query.filter_by(username=username).first()

        if not user or not user.mfa_enabled:
            return redirect(url_for('login'))

        if MFAManager.verify_totp(user.mfa_secret, token):
            login_user(user)
            session.pop('username_pending', None)
            audit_log('AUTH', f'User {username} logged in with MFA')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid MFA token', 'error')
            return redirect(url_for('login_mfa'))

## Authorization

### Role-Based Access Control (RBAC)

    from functools import wraps
    from flask import abort

## Define roles

    ROLES = {
        'admin': {
            'description': 'Full cluster administration',
            'permissions': ['*']  # Wildcard: all permissions
        },
        'operator': {
            'description': 'Cluster operations (deploy, scale, troubleshoot)',
            'permissions': [
                'nodes:*',
                'storage:*',
                'compute:read',
                'compute:create',
                'compute:delete',
                'network:*',
            ]
        },
        'developer': {
            'description': 'Application deployment and debugging',
            'permissions': [
                'compute:read',
                'compute:create',
                'compute:debug',
                'storage:read',
            ]
        },
        'viewer': {
            'description': 'Read-only cluster inspection',
            'permissions': [
                'nodes:read',
                'storage:read',
                'compute:read',
                'network:read',
            ]
        },
    }

    def check_permission(user, permission):
        """Check if user has permission"""
        if user.role not in ROLES:
            return False

        permissions = ROLES[user.role]['permissions']

## Wildcard match

        if '*' in permissions:
            return True

## Exact match

        if permission in permissions:
            return True

## Prefix match (e.g., 'nodes:*' matches 'nodes:list')

        for perm in permissions:
            if perm.endswith(':*'):
                prefix = perm[:-2]
                if permission.startswith(prefix + ':'):
                    return True

        return False

    def require_permission(permission):
        """Decorator to require permission"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args,__kwargs):
                if not check_permission(current_user, permission):
                    audit_log('AUTHZ_DENIED', f'Access denied for {current_user.username}',
                             extra={'required_permission': permission})
                    abort(403)
                return f(*args,__kwargs)
            return decorated_function
        return decorator

## Usage in routes

    @app.route('/api/nodes', methods=['GET'])
    @login_required
    @require_permission('nodes:read')
    def list_nodes():
        """List cluster nodes"""
        nodes = rpc_client.list_nodes()
        audit_log('AUDIT', f'User {current_user.username} listed nodes',
                 extra={'count': len(nodes)})
        return jsonify(nodes)

    @app.route('/api/nodes//shutdown', methods=['POST'])
    @login_required
    @require_permission('nodes:modify')
    def shutdown_node(node_id):
        """Shutdown node (state-changing operation)"""
        rpc_client.shutdown_node(node_id)
        audit_log('AUDIT', f'User {current_user.username} shutdown node {node_id}',
                 extra={'node_id': node_id})
        return jsonify({'status': 'ok'})

## HTTPS/TLS Configuration

### Certificate Setup

## app.py - HTTPS/TLS setup

    import ssl
    from pathlib import Path

## TLS Configuration

    TLS_CONFIG = {
        'cert_file': '/etc/debvisor/panel/tls/server.crt',
        'key_file': '/etc/debvisor/panel/tls/server.key',
        'min_tls_version': ssl.TLSVersion.TLSv1_3,
        'ciphers': 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256',
    }

    def create_ssl_context():
        """Create SSL context with strong security settings"""
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(TLS_CONFIG['cert_file'], TLS_CONFIG['key_file'])

## Set minimum TLS version

        context.minimum_version = TLS_CONFIG['min_tls_version']
        context.maximum_version = ssl.TLSVersion.TLSv1_3

## Set strong ciphers

        context.set_ciphers(TLS_CONFIG['ciphers'])

## Session tickets for resumption (but not session IDs)

        context.options |= ssl.OP_NO_TICKET

## Certificate verification options

        context.verify_mode = ssl.CERT_NONE  # Server doesn't verify client certs by default

## For client certificate validation

## context.verify_mode = ssl.CERT_REQUIRED

## context.load_verify_locations('/etc/debvisor/panel/tls/ca.crt')

        return context

## Start Flask with HTTPS

    if__name__== '__main__':
        ssl_context = create_ssl_context()
        app.run(
            host='0.0.0.0',
            port=443,
            ssl_context=ssl_context,
            debug=False,
            use_reloader=False,
        )

## Systemd Service with HTTPS

## /etc/systemd/system/debvisor-panel.service

    [Unit]
    Description=DebVisor Web Panel
    After=network-online.target debvisor-rpcd.service
    Wants=network-online.target

    [Service]
    Type=notify
    User=www-data
    Group=www-data
    WorkingDirectory=/opt/web/panel

## Security hardening

    ProtectSystem=strict
    ProtectHome=yes
    NoNewPrivileges=yes
    PrivateDevices=yes
    RestrictRealtime=yes
    RestrictNamespaces=yes
    LockPersonality=yes
    RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6

## Resource limits

    MemoryLimit=256M
    CPUQuota=150%
    TasksMax=256

## Capabilities

    CapabilityBoundingSet=
    AmbientCapabilities=

## Start service

    ExecStart=/usr/bin/python3 /opt/web/panel/app.py

## Restart on failure

    Restart=on-failure
    RestartSec=10

## Logging

    StandardOutput=journal
    StandardError=journal
    SyslogIdentifier=debvisor-panel

    [Install]
    WantedBy=multi-user.target

## Session Management

## app.py - Secure session configuration

    from datetime import timedelta

## Session configuration

    app.config['SESSION_COOKIE_SECURE'] = True      # HTTPS only
    app.config['SESSION_COOKIE_HTTPONLY'] = True    # No JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # CSRF protection
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
    app.config['SESSION_COOKIE_NAME'] = '__Host-debvisor_session'  #__Host- prefix for strictest scope
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True

## Force HTTPS

    @app.before_request
    def enforce_https():
        """Enforce HTTPS in production"""
        if not app.debug and not request.is_secure:
            url = request.url.replace('[http://',](http://',) '[https://',](https://',) 1)
            return redirect(url, code=301)

## Session timeout warning

    @app.route('/api/session/activity', methods=['POST'])
    @login_required
    def session_activity():
        """Update session activity timestamp"""
        session.modified = True
        return jsonify({'status': 'ok', 'expires_in': session.permanent_session_lifetime.total_seconds()})

## Session expiry page

    @app.route('/session-expired')
    def session_expired():
        """Session expired redirect"""
        return render_template('session_expired.html'), 401

## CSRF Protection

### Token Generation and Validation

    from flask_wtf.csrf import CSRFProtect, generate_csrf
    import secrets

    csrf = CSRFProtect(app)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Dashboard with CSRF token"""
        csrf_token = generate_csrf()
        return render_template('dashboard.html', csrf_token=csrf_token)

    @app.route('/api/nodes//restart', methods=['POST'])
    @login_required
    @csrf.protect  # Automatically validates CSRF token
    def restart_node(node_id):
        """Restart node (requires CSRF token)"""

## Token automatically validated by @csrf.protect

        rpc_client.restart_node(node_id)
        audit_log('AUDIT', f'User {current_user.username} restarted node {node_id}')
        return jsonify({'status': 'ok'})

### HTML Template Example

            Restart Node

    fetch('/api/nodes/{{ node_id }}/restart', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name=csrf_token]').value,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => console.log('Success:', data));

## Input Validation & Output Escaping

### Input Validation

    import re
    from urllib.parse import urlparse

    class InputValidator:
        """Validate user input"""

## Patterns for common inputs

        PATTERNS = {
            'hostname': r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$',
            'ipv4': r'^(\d{1,3}\.){3}\d{1,3}$',
            'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            'snapshot_name': r'^[a-zA-Z0-9_-]{1,64}$',
            'pool_name': r'^[a-zA-Z0-9_-]{1,32}$',
        }

        @staticmethod
        def validate_hostname(hostname):
            """Validate hostname format"""
            if not hostname or len(hostname) > 253:
                return False
            return bool(re.match(InputValidator.PATTERNS['hostname'], hostname))

        @staticmethod
        def validate_ipv4(ip):
            """Validate IPv4 address"""
            if not re.match(InputValidator.PATTERNS['ipv4'], ip):
                return False
            parts = ip.split('.')
            return all(0 <= int(p) <= 255 for p in parts)

        @staticmethod
        def validate_snapshot_name(name):
            """Validate snapshot name (alphanumeric, underscore, dash only)"""
            return bool(re.match(InputValidator.PATTERNS['snapshot_name'], name))

        @staticmethod
        def sanitize_string(value, max_length=1000):
            """Sanitize string input (remove control characters)"""
            if not isinstance(value, str):
                return None

## Remove control characters

            value = ''.join(c for c in value if ord(c) >= 32 or c in '\t\n\r')

## Truncate

            return value[:max_length]

## Usage in routes [2]

    @app.route('/api/snapshots', methods=['POST'])
    @login_required
    @require_permission('storage:write')
    def create_snapshot():
        """Create storage snapshot"""
        pool_name = request.form.get('pool', '').strip()
        snapshot_name = request.form.get('snapshot', '').strip()

## Input validation [2]

        if not InputValidator.validate_pool_name(pool_name):
            return jsonify({'error': 'Invalid pool name'}), 400

        if not InputValidator.validate_snapshot_name(snapshot_name):
            return jsonify({'error': 'Invalid snapshot name'}), 400

## Sanitize description

        description = InputValidator.sanitize_string(request.form.get('description', ''))

## Call RPC service

        result = rpc_client.create_snapshot(pool_name, snapshot_name)

        audit_log('AUDIT', f'User {current_user.username} created snapshot',
                 extra={'pool': pool_name, 'snapshot': snapshot_name})

        return jsonify(result)

## Output Escaping

    from markupsafe import escape
    from jinja2 import Markup

## Automatically escapes in Jinja2 templates

## {{ variable }} is automatically HTML-escaped

    @app.route('/nodes/')
    @login_required
    def node_details(node_id):
        """Node details page"""
        node_info = rpc_client.get_node_info(node_id)

## All variables auto-escaped in template

        return render_template('node.html', node=node_info)

## Template: templates/node.html

    """
    Node: {{ node.hostname }}
    Status: {{ node.status }}
    {{ node.config }}   -->
    """

## For JavaScript context (if needed)

    import json
    @app.route('/api/node//json')
    @login_required
    def node_json(node_id):
        """Node info as JSON (already escaped by json.dumps)"""
        node_info = rpc_client.get_node_info(node_id)
        return jsonify(node_info)

## Escape user-provided content for display

    def safe_display(user_content):
        """Safely display user-provided content"""
        return escape(user_content)

## Audit Logging

### Audit Event Format

    import json
    from datetime import datetime
    import logging

    class AuditLogger:
        """Comprehensive audit logging"""

        def__init__(self, log_file='/var/log/debvisor/panel-audit.log'):
            self.logger = logging.getLogger('debvisor.panel.audit')
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        def log(self, event_type, user, action, result='success', extra=None):
            """Log audit event"""
            event = {
                'timestamp': datetime.utcnow().isoformat(),
                'event_type': event_type,
                'user': user,
                'action': action,
                'result': result,
                'source_ip': request.remote_addr,
                'user_agent': request.headers.get('User-Agent', ''),
            }

            if extra:
                event['extra'] = extra

## Redact sensitive data

            event_json = json.dumps(event)
            event_json = event_json.replace('"password"', '"password":"***"')
            event_json = event_json.replace('"token"', '"token":"***"')
            event_json = event_json.replace('"key"', '"key":"***"')

            self.logger.info(event_json)

    audit = AuditLogger()

    def audit_log(event_type, action, result='success', extra=None):
        """Convenience function to log audit events"""
        if current_user:
            username = current_user.username
        else:
            username = 'anonymous'

        audit.log(event_type, username, action, result, extra)

## Audit event types

    AUDIT_EVENTS = {
        'AUTH': 'Authentication event (login/logout)',
        'AUTH_FAILED': 'Failed authentication attempt',
        'AUTHZ_DENIED': 'Authorization denial',
        'AUDIT': 'Auditable action (state change)',
        'SECURITY': 'Security-related event (password change, MFA, etc)',
        'ERROR': 'Error condition',
        'SUSPICIOUS': 'Suspicious activity detected',
    }

## Example Audit Logs

    {
      "timestamp": "2025-01-15T10:30:45.123456Z",
      "event_type": "AUTH",
      "user": "alice",
      "action": "User alice logged in",
      "result": "success",
      "source_ip": "192.168.1.100",
      "user_agent": "Mozilla/5.0..."
    }

    {
      "timestamp": "2025-01-15T10:31:20.654321Z",
      "event_type": "AUDIT",
      "user": "alice",
      "action": "User alice restarted node node-001",
      "result": "success",
      "source_ip": "192.168.1.100",
      "extra": {
        "node_id": "node-001",
        "rpc_status": "ok"
      }
    }

    {
      "timestamp": "2025-01-15T10:32:00.000000Z",
      "event_type": "AUTHZ_DENIED",
      "user": "bob",
      "action": "Access denied for bob",
      "result": "denied",
      "source_ip": "192.168.1.101",
      "extra": {
        "required_permission": "nodes:modify",
        "user_role": "viewer"
      }
    }

## Rate Limiting & DDoS Protection

    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    from redis import Redis

## Redis-backed rate limiting for distributed deployments

    redis_client = Redis(host='localhost', port=6379, db=0)

    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri='redis://localhost:6379',
        default_limits=['200 per day', '50 per hour'],
        strategy='fixed-window-elastic-expiry',
    )

## Rate limit specific routes

    @app.route('/login', methods=['POST'])
    @limiter.limit('5 per minute')
    def login():
        """Login with strict rate limiting"""
        pass

    @app.route('/api/nodes', methods=['GET'])
    @login_required
    @limiter.limit('100 per minute')
    def list_nodes():
        """List nodes with per-user rate limiting"""
        pass

## Custom rate limiting per user

    class PerUserRateLimiter:
        """Rate limit per authenticated user"""

        def__init__(self, redis_client):
            self.redis = redis_client
            self.default_limits = {
                'admin': 1000,      # 1000 req/min for admin
                'operator': 500,    # 500 req/min for operator
                'developer': 200,   # 200 req/min for developer
                'viewer': 100,      # 100 req/min for viewer
            }

        def check_limit(self, user, role):
            """Check if user is within rate limit"""
            limit = self.default_limits.get(role, 100)
            key = f'ratelimit:{user}:{int(time.time())}'

            count = self.redis.incr(key)
            if count == 1:
                self.redis.expire(key, 60)  # 1-minute window

            return count <= limit

    per_user_limiter = PerUserRateLimiter(redis_client)

    @app.before_request
    @login_required
    def check_rate_limit():
        """Check rate limit for each request"""
        if not per_user_limiter.check_limit(current_user.username, current_user.role):
            audit_log('SUSPICIOUS', f'Rate limit exceeded for {current_user.username}')
            abort(429)  # Too Many Requests

## Security Headers

## app.py - Security headers

    @app.after_request
    def set_security_headers(response):
        """Set security headers on every response"""

## Prevent clickjacking

        response.headers['X-Frame-Options'] = 'DENY'

## Prevent MIME type sniffing

        response.headers['X-Content-Type-Options'] = 'nosniff'

## Enable XSS protection

        response.headers['X-XSS-Protection'] = '1; mode=block'

## Content Security Policy

        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "  # Allow inline styles for Bootstrap etc
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )

## Referrer policy

        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

## Permissions policy

        response.headers['Permissions-Policy'] = (
            'accelerometer=(), '
            'camera=(), '
            'geolocation=(), '
            'gyroscope=(), '
            'magnetometer=(), '
            'microphone=(), '
            'payment=(), '
            'usb=()'
        )

## HSTS (HTTP Strict-Transport-Security)

        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'

        return response

## Error Handling

## app.py - Error handling

    @app.errorhandler(400)
    def bad_request(error):
        """Bad request error"""
        audit_log('ERROR', 'Bad request', extra={'error': str(error)})
        return render_template('error.html',
                             code=400,
                             message='Bad Request',
                             detail='The server could not understand the request.'), 400

    @app.errorhandler(403)
    def forbidden(error):
        """Forbidden error"""
        audit_log('AUTHZ_DENIED', 'Forbidden access attempt')
        return render_template('error.html',
                             code=403,
                             message='Forbidden',
                             detail='You do not have permission to access this resource.'), 403

    @app.errorhandler(404)
    def not_found(error):
        """Not found error"""
        return render_template('error.html',
                             code=404,
                             message='Not Found',
                             detail='The requested resource was not found.'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Internal server error"""
        audit_log('ERROR', 'Internal server error', extra={'error': str(error)})
        return render_template('error.html',
                             code=500,
                             message='Internal Server Error',
                             detail='An unexpected error occurred.'), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        """Service unavailable (RPC service down)"""
        audit_log('ERROR', 'RPC service unavailable')
        return render_template('error.html',
                             code=503,
                             message='Service Unavailable',
                             detail='Cluster management service is temporarily unavailable. Try again later.'), 503

## RPC service health check

    @app.route('/health')
    def health_check():
        """Health check endpoint for load balancers"""
        try:

## Quick RPC service check

            rpc_client.health_check()
            return jsonify({'status': 'healthy'}), 200
        except Exception as e:
            return jsonify({'status': 'unhealthy', 'error': str(e)}), 503

## Deployment Security Checklist

Use this checklist before deploying to production:

### Authentication & Authorization

- [ ] User authentication implemented (local, LDAP, OIDC)
- [ ] MFA enabled for admin/operator roles
- [ ] Passwords validated per policy (12+ chars, mix of types)
- [ ] RBAC roles defined and tested (admin, operator, developer, viewer)
- [ ] Permission checks on all state-changing operations
- [ ] Service account permissions minimal (principle of least privilege)

### HTTPS/TLS

- [ ] HTTPS enforced (HTTP redirects to HTTPS)
- [ ] TLS 1.3 or 1.2 only (no SSL/TLS 1.0/1.1)
- [ ] Strong ciphers configured
- [ ] Certificate valid and not expired
- [ ] Certificate pinning considered for internal clients
- [ ] Client certificate authentication considered for sensitive operations

### Session Management [2]

- [ ] Session cookies secure (HTTPS only)
- [ ] Session cookies HttpOnly (no JavaScript access)
- [ ] Session cookies SameSite=Lax (CSRF protection)
- [ ] Session timeout configured (8 hours default)
- [ ] Session token regeneration on login
- [ ] Session invalidation on logout

### CSRF Protection [2]

- [ ] CSRF tokens generated for all forms
- [ ] CSRF tokens validated on POST/PUT/DELETE
- [ ] CSRF tokens short-lived (match session lifetime)
- [ ] Double-submit cookie pattern considered

### Input Validation [2] [2]

- [ ] All user input validated (type, length, format)
- [ ] Whitelist approach (accept known good input)
- [ ] Special characters escaped or rejected
- [ ] SQL injection prevention (parameterized queries)
- [ ] Command injection prevention (avoid shell execution)

### Output Escaping [2]

- [ ] HTML output escaped (prevent XSS)
- [ ] JavaScript context handled safely
- [ ] JSON output properly formatted
- [ ] User-provided content never trusted

### Audit Logging [2]

- [ ] All authentication attempts logged (success/failure)
- [ ] All authorization denials logged
- [ ] All state-changing operations logged
- [ ] Sensitive data redacted from logs (passwords, tokens, keys)
- [ ] Audit logs stored securely with restricted access
- [ ] Audit logs monitored for suspicious patterns
- [ ] Audit log retention policy (e.g., 90 days)

### Rate Limiting & DDoS

- [ ] Rate limiting on login endpoint (5 per minute)
- [ ] Rate limiting on API endpoints (100-1000 per minute per user)
- [ ] Rate limiting per user role (viewer < developer < operator < admin)
- [ ] DDoS protection configured (WAF, reverse proxy)
- [ ] Health check endpoint for load balancer

### Security Headers [2]

- [ ] X-Frame-Options: DENY (prevent clickjacking)
- [ ] X-Content-Type-Options: nosniff (prevent MIME sniffing)
- [ ] X-XSS-Protection: 1; mode=block (XSS protection)
- [ ] Content-Security-Policy configured
- [ ] Referrer-Policy configured
- [ ] Permissions-Policy configured
- [ ] HSTS header configured

### Error Handling [2]

- [ ] Generic error messages (no sensitive details to users)
- [ ] Detailed error logs (for debugging)
- [ ] Error pages don't leak system information
- [ ] 4xx/5xx error handlers implemented
- [ ] RPC service availability errors handled gracefully

### Dependencies & Patching

- [ ] All Python packages pinned to specific versions
- [ ] No vulnerable package versions (check with `pip-audit`)
- [ ] Security patches applied immediately
- [ ] Changelog monitored for upstream vulnerabilities

### Monitoring & Alerting

- [ ] Authentication failures monitored (alert on spikes)
- [ ] Authorization denials monitored
- [ ] Rate limit violations monitored
- [ ] RPC service unavailability alerted
- [ ] Application errors logged and alerted
- [ ] Disk space for audit logs monitored

### Systemd Service Security

- [ ] Service runs as unprivileged user (www-data)
- [ ] ProtectSystem=strict enabled
- [ ] ProtectHome=yes enabled
- [ ] NoNewPrivileges=yes enabled
- [ ] PrivateDevices=yes enabled
- [ ] RestrictNamespaces=yes enabled
- [ ] CapabilityBoundingSet empty (no capabilities)
- [ ] Resource limits configured (memory, CPU, tasks)

---

### Next Steps

1. Review this guide with your security team
1. Implement authentication/authorization methods appropriate for your environment
1. Configure TLS certificates (self-signed for lab, CA-signed for production)
1. Deploy to test environment and run security scan
1. Review audit logs for patterns
1. Harden based on findings before production deployment
