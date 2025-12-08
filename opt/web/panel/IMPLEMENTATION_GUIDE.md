# DebVisor Web Panel - Implementation Guide

This document provides complete implementation guidance for the DebVisor web panel (`opt/web/panel/app.py`), including Flask application structure, RPC integration, authentication, authorization, and deployment.

## Table of Contents

1. Project Structure
1. Flask Application Setup
1. RPC Service Integration
1. Authentication & Authorization
1. API Endpoints
1. Frontend Templates
1. Deployment
1. Testing

## Project Structure

    opt/web/panel/
    +-- app.py                          # Main Flask application
    +-- requirements.txt                # Python dependencies
    +-- config.py                       # Configuration (dev/prod)
    +-- wsgi.py                         # WSGI entry point (gunicorn)
    +-- README.md                       # Overview
    +-- SECURITY.md                     # Security guide
    +-- INPUT_VALIDATION.md             # Input validation guide
    +-- IMPLEMENTATION_GUIDE.md         # This file
    |
    +-- debvisor_pb2.py                 # Generated RPC protocol buffers
    +-- debvisor_pb2_grpc.py            # Generated RPC service stubs
    |
    +-- core/                           # Core application logic
    |   +--**init**.py
    |   +-- rpc_client.py               # RPC service client wrapper
    |   +-- auth.py                     # Authentication logic
    |   +-- authz.py                    # Authorization logic
    |   +-- validators.py               # Input validators
    |
    +-- models/                         # SQLAlchemy models
    |   +--**init**.py
    |   +-- user.py                     # User model
    |   +-- audit_log.py                # Audit logging
    |
    +-- routes/                         # API routes organized by feature
    |   +--**init**.py
    |   +-- auth.py                     # Login/logout/profile routes
    |   +-- nodes.py                    # Node management routes
    |   +-- storage.py                  # Storage management routes
    |   +-- compute.py                  # VM management routes
    |
    +-- templates/                      # Jinja2 HTML templates
    |   +-- base.html                   # Base template with layout
    |   +-- login.html                  # Login page
    |   +-- dashboard.html              # Main dashboard
    |   +-- nodes.html                  # Node list page
    |   +-- nodes/                      # Node-related templates
    |   |   +-- detail.html
    |   |   +-- create.html
    |   |   +-- edit.html
    |   +-- storage/                    # Storage-related templates
    |   +-- error.html                  # Error page
    |
    +-- static/                         # Static files (CSS, JS, images)
    |   +-- css/
    |   |   +-- bootstrap.min.css
    |   |   +-- app.css
    |   +-- js/
    |   |   +-- jquery.min.js
    |   |   +-- bootstrap.min.js
    |   |   +-- app.js
    |   +-- images/
    |
    +-- tests/                          # Unit and integration tests
        +--**init**.py
        +-- test_auth.py                # Authentication tests
        +-- test_nodes.py               # Node endpoint tests
        +-- test_validators.py          # Validator tests

## Flask Application Setup

### Basic Flask Application (app.py)

    """
    DebVisor Web Panel - Flask Application

    Main entry point for the web panel serving cluster management UI.
    """

    import os
    import logging
    from datetime import timedelta
    from pathlib import Path

    from flask import Flask, render_template, redirect, url_for, session
    from flask_login import LoginManager
    from flask_sqlalchemy import SQLAlchemy
    from flask_wtf.csrf import CSRFProtect
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

## Initialize extensions

    db = SQLAlchemy()
    login_manager = LoginManager()
    csrf = CSRFProtect()
    limiter = Limiter(key_func=get_remote_address)

    def create_app(config_name='production'):
        """Application factory"""

        app = Flask(**name**)

## Configuration

        from config import config
        app.config.from_object(config[config_name])

## Initialize extensions [2]

        db.init_app(app)
        login_manager.init_app(app)
        csrf.init_app(app)
        limiter.init_app(app)

## Session security

        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        app.config['SESSION_COOKIE_NAME'] = '__Host-debvisor_session'
        app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

## Logging

        setup_logging(app)

## Middleware

        @app.before_request
        def enforce_https():
            """Enforce HTTPS in production"""
            if not app.debug and not request.is_secure:
                url = request.url.replace('[http://',](http://',) '[https://',](https://',) 1)
                return redirect(url, code=301)

        @app.after_request
        def set_security_headers(response):
            """Set security headers"""
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            response.headers['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; "
                "font-src 'self'; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            )
            return response

## Error handlers

        @app.errorhandler(400)
        def bad_request(error):
            return render_template('error.html', code=400,
                                 message='Bad Request'), 400

        @app.errorhandler(403)
        def forbidden(error):
            return render_template('error.html', code=403,
                                 message='Forbidden'), 403

        @app.errorhandler(404)
        def not_found(error):
            return render_template('error.html', code=404,
                                 message='Not Found'), 404

        @app.errorhandler(500)
        def internal_error(error):
            logging.error(f'Internal error: {error}')
            return render_template('error.html', code=500,
                                 message='Internal Server Error'), 500

        @app.errorhandler(503)
        def service_unavailable(error):
            return render_template('error.html', code=503,
                                 message='RPC Service Unavailable'), 503

## Register blueprints

        from routes.auth import auth_bp
        from routes.nodes import nodes_bp
        from routes.storage import storage_bp
        from routes.compute import compute_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(nodes_bp)
        app.register_blueprint(storage_bp)
        app.register_blueprint(compute_bp)

## Health check

        @app.route('/health')
        def health_check():
            """Health check endpoint"""
            try:
                from core.rpc_client import rpc_client
                rpc_client.health_check()
                return {'status': 'healthy'}, 200
            except Exception as e:
                return {'status': 'unhealthy', 'error': str(e)}, 503

## Root redirect

        @app.route('/')
        def index():
            """Root path redirect"""
            if current_user.is_authenticated:
                return redirect(url_for('nodes.dashboard'))
            return redirect(url_for('auth.login'))

## Context processors

        @app.context_processor
        def inject_user():
            """Inject current user into templates"""
            from flask_login import current_user
            return dict(current_user=current_user)

## Create tables

        with app.app_context():
            db.create_all()

        return app

    def setup_logging(app):
        """Configure application logging"""
        log_dir = Path('/var/log/debvisor')
        log_dir.mkdir(exist_ok=True, parents=True)

## Application log

        app_handler = logging.FileHandler(log_dir / 'panel.log')
        app_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        app.logger.addHandler(app_handler)
        app.logger.setLevel(logging.INFO)

## Audit log

        audit_handler = logging.FileHandler(log_dir / 'panel-audit.log')
        audit_handler.setFormatter(logging.Formatter('%(message)s'))
        audit_logger = logging.getLogger('debvisor.audit')
        audit_logger.addHandler(audit_handler)
        audit_logger.setLevel(logging.INFO)

    if**name**== '**main**':
        from pathlib import Path
        import ssl

        app = create_app(os.getenv('FLASK_ENV', 'production'))

## Load SSL certificates

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(
            '/etc/debvisor/panel/tls/server.crt',
            '/etc/debvisor/panel/tls/server.key'
        )
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        ssl_context.set_ciphers('TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256')

        app.run(
            host='0.0.0.0',
            port=443,
            ssl_context=ssl_context,
            debug=False,
        )

## Configuration File (config.py)

    """
    Flask application configuration
    """

    import os
    from datetime import timedelta

    class Config:
        """Base configuration"""

## Flask settings

        SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
        DEBUG = False
        TESTING = False

## Session settings

        PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
        SESSION_REFRESH_EACH_REQUEST = True

## Database

        SQLALCHEMY_DATABASE_URI = os.getenv(
            'DATABASE_URL',
            'sqlite:////var/lib/debvisor/panel/panel.db'
        )
        SQLALCHEMY_TRACK_MODIFICATIONS = False

## RPC Service

        RPC_HOST = os.getenv('RPC_HOST', 'localhost')
        RPC_PORT = int(os.getenv('RPC_PORT', '50051'))
        RPC_CA_CERT = os.getenv('RPC_CA_CERT', '/etc/debvisor/panel/tls/ca.crt')
        RPC_CLIENT_CERT = os.getenv('RPC_CLIENT_CERT', '/etc/debvisor/panel/tls/client.crt')
        RPC_CLIENT_KEY = os.getenv('RPC_CLIENT_KEY', '/etc/debvisor/panel/tls/client.key')

## TLS

        TLS_CERT = '/etc/debvisor/panel/tls/server.crt'
        TLS_KEY = '/etc/debvisor/panel/tls/server.key'

## Rate limiting

        RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    class DevelopmentConfig(Config):
        """Development configuration"""
        DEBUG = True
        TESTING = False
        SQLALCHEMY_ECHO = True

    class TestingConfig(Config):
        """Testing configuration"""
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        WTF_CSRF_ENABLED = False

    class ProductionConfig(Config):
        """Production configuration"""
        DEBUG = False
        TESTING = False

    config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': ProductionConfig,
    }

## RPC Service Integration

### RPC Client Wrapper (core/rpc_client.py)

    """
    RPC Service Client Wrapper

    Provides high-level interface to debvisor-rpcd service with
    automatic error handling and connection management.
    """

    import grpc
    import logging
    from contextlib import contextmanager
    from ssl import SSLContext

    import debvisor_pb2
    import debvisor_pb2_grpc

    logger = logging.getLogger(**name**)

    class RPCClient:
        """Wrapper for RPC service client"""

        def**init**(self, host, port, ca_cert, client_cert, client_key):
            self.host = host
            self.port = port
            self.ca_cert = ca_cert
            self.client_cert = client_cert
            self.client_key = client_key
            self._channel = None

        def _get_channel(self):
            """Get or create gRPC channel with mTLS"""
            if self._channel is None:

## Load credentials

                with open(self.ca_cert, 'rb') as f:
                    ca_pem = f.read()
                with open(self.client_cert, 'rb') as f:
                    client_cert_pem = f.read()
                with open(self.client_key, 'rb') as f:
                    client_key_pem = f.read()

## Create credentials

                credentials = grpc.ssl_channel_credentials(
                    root_certificates=ca_pem,
                    private_key=client_key_pem,
                    certificate_chain=client_cert_pem
                )

## Create channel

                self._channel = grpc.secure_channel(
                    f'{self.host}:{self.port}',
                    credentials
                )

            return self._channel

        def health_check(self):
            """Check RPC service health"""
            try:
                channel = self._get_channel()
                stub = debvisor_pb2_grpc.NodeServiceStub(channel)

                response = stub.HealthCheck(debvisor_pb2.HealthCheckRequest())
                return response.status == debvisor_pb2.HealthCheckResponse.SERVING
            except Exception as e:
                logger.error(f'Health check failed: {e}')
                raise

## Node Service methods

        def list_nodes(self):
            """List all cluster nodes"""
            channel = self._get_channel()
            stub = debvisor_pb2_grpc.NodeServiceStub(channel)

            request = debvisor_pb2.ListNodesRequest()
            response = stub.ListNodes(request)

            return [self._proto_to_dict(node) for node in response.nodes]

        def get_node(self, node_id):
            """Get node details"""
            channel = self._get_channel()
            stub = debvisor_pb2_grpc.NodeServiceStub(channel)

            request = debvisor_pb2.GetNodeRequest(node_id=node_id)
            response = stub.GetNode(request)

            return self._proto_to_dict(response.node)

        def create_node(self, hostname, management_ip, mac_address):
            """Create node"""
            channel = self._get_channel()
            stub = debvisor_pb2_grpc.NodeServiceStub(channel)

            node = debvisor_pb2.Node(
                hostname=hostname,
                management_ip=management_ip,
                mac_address=mac_address,
            )
            request = debvisor_pb2.CreateNodeRequest(node=node)
            response = stub.CreateNode(request)

            return self._proto_to_dict(response.node)

        def shutdown_node(self, node_id):
            """Shutdown node"""
            channel = self._get_channel()
            stub = debvisor_pb2_grpc.NodeServiceStub(channel)

            request = debvisor_pb2.ShutdownNodeRequest(node_id=node_id)
            response = stub.ShutdownNode(request)

            return response.success

## Storage Service methods

        def list_pools(self):
            """List storage pools"""
            channel = self._get_channel()
            stub = debvisor_pb2_grpc.StorageServiceStub(channel)

            request = debvisor_pb2.ListPoolsRequest()
            response = stub.ListPools(request)

            return [self._proto_to_dict(pool) for pool in response.pools]

        def create_snapshot(self, pool_id, snapshot_name):
            """Create storage snapshot"""
            channel = self._get_channel()
            stub = debvisor_pb2_grpc.StorageServiceStub(channel)

            request = debvisor_pb2.CreateSnapshotRequest(
                pool_id=pool_id,
                snapshot_name=snapshot_name
            )
            response = stub.CreateSnapshot(request)

            return self._proto_to_dict(response.snapshot)

        @staticmethod
        def _proto_to_dict(proto_obj):
            """Convert protobuf message to dict"""
            return {
                field.name: getattr(proto_obj, field.name)
                for field in proto_obj.DESCRIPTOR.fields
            }

## Singleton instance

    _rpc_client = None

    def get_rpc_client():
        """Get RPC client singleton"""
        global _rpc_client
        if _rpc_client is None:
            from flask import current_app
            _rpc_client = RPCClient(
                host=current_app.config['RPC_HOST'],
                port=current_app.config['RPC_PORT'],
                ca_cert=current_app.config['RPC_CA_CERT'],
                client_cert=current_app.config['RPC_CLIENT_CERT'],
                client_key=current_app.config['RPC_CLIENT_KEY'],
            )
        return _rpc_client

## Convenience alias

    rpc_client = get_rpc_client()

## Authentication & Authorization

### User Model (models/user.py)

    """
    User model for authentication
    """

    from datetime import datetime
    from werkzeug.security import generate_password_hash, check_password_hash
    from flask_login import UserMixin

    from app import db

    class User(UserMixin, db.Model):
        """User model with secure password handling"""

        **tablename**= 'users'

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False, index=True)
        password_hash = db.Column(db.String(255), nullable=False)
        role = db.Column(db.String(20), nullable=False, default='viewer')  # admin, operator, developer, viewer
        email = db.Column(db.String(120), unique=True)

## MFA

        mfa_enabled = db.Column(db.Boolean, default=False)
        mfa_secret = db.Column(db.String(32))  # Base32 encoded TOTP secret

## Account status

        active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        last_login = db.Column(db.DateTime)

        def set_password(self, password):
            """Hash and set password"""
            self.password_hash = generate_password_hash(password, method='argon2')

        def check_password(self, password):
            """Verify password"""
            return check_password_hash(self.password_hash, password)

        def has_permission(self, permission):
            """Check if user has permission"""
            from core.authz import check_permission
            return check_permission(self, permission)

        def**repr**(self):
            return f''

### Authorization Module (core/authz.py)

    """
    Authorization framework - RBAC with wildcard matching
    """

    ROLES = {
        'admin': {
            'description': 'Full cluster administration',
            'permissions': ['*']
        },
        'operator': {
            'description': 'Cluster operations',
            'permissions': [
                'nodes:*',
                'storage:*',
                'compute:*',
                'network:*',
            ]
        },
        'developer': {
            'description': 'Application deployment',
            'permissions': [
                'nodes:read',
                'compute:*',
                'storage:read',
            ]
        },
        'viewer': {
            'description': 'Read-only access',
            'permissions': [
                'nodes:read',
                'storage:read',
                'compute:read',
            ]
        },
    }

    def check_permission(user, permission):
        """Check if user has permission"""
        if user.role not in ROLES:
            return False

        permissions = ROLES[user.role]['permissions']

## Wildcard: admin has all permissions

        if '*' in permissions:
            return True

## Exact match

        if permission in permissions:
            return True

## Prefix match (e.g., 'nodes:*' matches 'nodes:read')

        for perm in permissions:
            if perm.endswith(':*'):
                prefix = perm[:-2]
                if permission.startswith(prefix + ':'):
                    return True

        return False

    def require_permission(permission):
        """Decorator to require permission"""
        from functools import wraps
        from flask import abort
        from flask_login import current_user
        from models.audit_log import audit_log

        def decorator(f):
            @wraps(f)
            def decorated_function(*args,__kwargs):
                if not current_user.has_permission(permission):
                    audit_log('AUTHZ_DENIED',
                             f'Access denied for {current_user.username}',
                             extra={'required_permission': permission})
                    abort(403)
                return f(*args,__kwargs)
            return decorated_function
        return decorator

### Audit Logging (models/audit_log.py)

    """
    Audit logging for compliance and security monitoring
    """

    import json
    import logging
    from datetime import datetime
    from flask import request
    from flask_login import current_user

    audit_logger = logging.getLogger('debvisor.audit')

    def audit_log(event_type, action, result='success', extra=None):
        """Log audit event"""

        try:
            username = current_user.username if current_user.is_authenticated else 'anonymous'
        except RuntimeError:
            username = 'anonymous'

        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user': username,
            'action': action,
            'result': result,
            'source_ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', ''),
        }

        if extra:
            event['extra'] = extra

## Redact sensitive data

        event_str = json.dumps(event)
        event_str = event_str.replace('"password"', '"password":"***"')
        event_str = event_str.replace('"token"', '"token":"***"')
        event_str = event_str.replace('"key"', '"key":"***"')

        audit_logger.info(event_str)

## API Endpoints

### Node Management Routes (routes/nodes.py)

    """
    Node management API endpoints
    """

    from flask import Blueprint, render_template, request, jsonify, abort
    from flask_login import login_required, current_user

    from core.rpc_client import get_rpc_client
    from core.authz import require_permission
    from core.validators import Validators
    from models.audit_log import audit_log

    nodes_bp = Blueprint('nodes',**name**, url_prefix='/nodes')
    rpc_client = get_rpc_client()

    @nodes_bp.route('/')
    @login_required
    @require_permission('nodes:read')
    def list_nodes():
        """List nodes page"""
        nodes = rpc_client.list_nodes()
        return render_template('nodes/list.html', nodes=nodes)

    @nodes_bp.route('/api', methods=['GET'])
    @login_required
    @require_permission('nodes:read')
    def api_list_nodes():
        """API: List nodes"""
        try:
            nodes = rpc_client.list_nodes()
            audit_log('AUDIT', f'Listed {len(nodes)} nodes')
            return jsonify({'nodes': nodes})
        except Exception as e:
            audit_log('ERROR', f'Failed to list nodes: {e}', result='failed')
            return jsonify({'error': 'Failed to list nodes'}), 503

    @nodes_bp.route('/')
    @login_required
    @require_permission('nodes:read')
    def node_detail(node_id):
        """Node detail page"""
        try:
            node_id = Validators.validate_uuid(node_id)
            node = rpc_client.get_node(node_id)
            return render_template('nodes/detail.html', node=node)
        except ValueError as e:
            abort(400)
        except Exception as e:
            abort(503)

    @nodes_bp.route('//shutdown', methods=['POST'])
    @login_required
    @require_permission('nodes:modify')
    def shutdown_node(node_id):
        """API: Shutdown node"""
        try:
            node_id = Validators.validate_uuid(node_id)
            result = rpc_client.shutdown_node(node_id)

            audit_log('AUDIT', f'Shutdown node {node_id}', extra={'node_id': node_id})
            return jsonify({'success': result})

        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            audit_log('ERROR', f'Failed to shutdown node: {e}', result='failed')
            return jsonify({'error': 'RPC service error'}), 503

    @nodes_bp.route('/api', methods=['POST'])
    @login_required
    @require_permission('nodes:create')
    def api_create_node():
        """API: Create node"""
        try:

## Validate input

            hostname = Validators.validate_hostname(request.json.get('hostname', ''))
            mgmt_ip = Validators.validate_ipv4(request.json.get('mgmt_ip', ''))
            mac_addr = Validators.validate_mac_address(request.json.get('mac_address', ''))

## Create node

            node = rpc_client.create_node(hostname, mgmt_ip, mac_addr)

            audit_log('AUDIT', f'Created node {hostname}',
                     extra={'node_id': node.get('id'), 'hostname': hostname})

            return jsonify(node), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            audit_log('ERROR', f'Failed to create node: {e}', result='failed')
            return jsonify({'error': 'RPC service error'}), 503

## Frontend Templates

### Base Template (templates/base.html)

        {% block title %}DebVisor{% endblock %}

        {% block extra_css %}{% endblock %}

                DebVisor

                {% if current_user.is_authenticated %}

                            Nodes

                            Storage

                            Compute

                            <a class="nav-link dropdown-toggle" href="#" id="userMenu" role="button"
                               data-bs-toggle="dropdown" aria-expanded="false">
                                {{ current_user.username }}

                                Profile
                                Settings

                                Logout

                {% endif %}

                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show"
                             role="alert">
                            {{ message }}

                        {% endfor %}
                    {% endif %}
                {% endwith %}

                {% block content %}{% endblock %}

                &copy; 2025 DebVisor Cluster Management. All rights reserved.

            // CSRF token for AJAX requests
            const csrfToken = document.querySelector('input[name=csrf_token]')?.value;
            if (csrfToken) {
                $.ajaxSetup({
                    headers: {'X-CSRFToken': csrfToken}
                });
            }

        {% block extra_js %}{% endblock %}

### Login Template (templates/login.html)

    {% extends "base.html" %}

    {% block title %}Login - DebVisor{% endblock %}

    {% block content %}

                    Login

                        {{ form.hidden_tag() }}

                            {{ form.username.label(class="form-label") }}
                            {{ form.username(class="form-control") }}
                            {% if form.username.errors %}

                                    {{ form.username.errors[0] }}

                            {% endif %}

                            {{ form.password.label(class="form-label") }}
                            {{ form.password(class="form-control") }}
                            {% if form.password.errors %}

                                    {{ form.password.errors[0] }}

                            {% endif %}

                            {{ form.remember_me(class="form-check-input") }}
                            {{ form.remember_me.label(class="form-check-label") }}

                        Login

    {% endblock %}

## Deployment

### Requirements File (requirements.txt)

    Flask>=3.0.3
    Flask-Login>=0.6.3
    Flask-SQLAlchemy>=3.1.1
    Flask-WTF>=1.2.1
    Flask-Limiter>=3.7.0
    Werkzeug>=3.0.3
    SQLAlchemy>=2.0.30
    WTForms>=3.1.2
    python-dotenv>=1.0.1
    grpcio>=1.64.0
    grpcio-tools>=1.64.0
    protobuf>=5.27.0
    pyotp>=2.9.0
    qrcode>=7.4.2
    Pillow>=10.3.0
    redis>=5.0.4
    gunicorn>=22.0.0
    bleach>=6.1.0
    markdown>=3.6.0
    requests>=2.32.3
    pip-audit>=2.7.3

### WSGI Entry Point (wsgi.py)

    """
    WSGI entry point for gunicorn
    """

    import os
    from app import create_app

    app = create_app(os.getenv('FLASK_ENV', 'production'))

    if**name**== '**main**':
        app.run()

### Systemd Service

    [Unit]
    Description=DebVisor Web Panel
    After=network-online.target debvisor-rpcd.service
    Wants=network-online.target

    [Service]
    Type=notify
    User=www-data
    Group=www-data
    WorkingDirectory=/opt/web/panel

    Environment="FLASK_ENV=production"
    Environment="SECRET_KEY=..."  # Generate: python -c 'import secrets; print(secrets.token_hex(32))'

    ExecStart=/usr/bin/python3 -m gunicorn \
        --workers 4 \
        --worker-class sync \
        --bind 127.0.0.1:8000 \
        --timeout 30 \
        --access-logfile /var/log/debvisor/panel-access.log \
        --error-logfile /var/log/debvisor/panel-error.log \
        wsgi:app

    ProtectSystem=strict
    ProtectHome=yes
    NoNewPrivileges=yes
    PrivateDevices=yes

    MemoryLimit=512M
    CPUQuota=200%

    Restart=on-failure
    RestartSec=10

    StandardOutput=journal
    StandardError=journal

    [Install]
    WantedBy=multi-user.target

### Nginx Reverse Proxy

    upstream debvisor_panel {
        server 127.0.0.1:8000;
    }

    server {
        listen 443 ssl http2;
        server_name cluster.example.com;

## SSL certificates

        ssl_certificate /etc/debvisor/panel/tls/server.crt;
        ssl_certificate_key /etc/debvisor/panel/tls/server.key;

## SSL settings

        ssl_protocols TLSv1.3 TLSv1.2;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

## Security headers

        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

## Proxy settings

        proxy_pass [http://debvisor_panel;](http://debvisor_panel;)
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

## Request limits

        client_max_body_size 10M;
        proxy_read_timeout 30s;

## WebSocket support (if needed)

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

## Redirect HTTP to HTTPS

    server {
        listen 80;
        server_name cluster.example.com;
        return 301 [https://$server_name$request_uri;](https://$server_name$request_uri;)
    }

## Testing

### Test Structure (tests/test_nodes.py)

    """
    Tests for node management endpoints
    """

    import pytest
    from flask_login import FlaskLoginClient

    @pytest.fixture
    def client(app):
        """Authenticated test client"""
        return app.test_client(use_cookies=True)

    @pytest.fixture
    def auth_client(client):
        """Login test client"""
        client.post('/login', json={
            'username': 'testuser',
            'password': 'TestPassword123!',
        })
        return client

    def test_list_nodes_requires_auth(client):
        """Test that listing nodes requires authentication"""
        response = client.get('/nodes/api')
        assert response.status_code == 302  # Redirect to login

    def test_list_nodes(auth_client, mocker):
        """Test listing nodes"""

## Mock RPC call

        mocker.patch('core.rpc_client.get_rpc_client').return_value.list_nodes.return_value = [
            {'id': 'node-1', 'hostname': 'node-001', 'status': 'online'},
            {'id': 'node-2', 'hostname': 'node-002', 'status': 'offline'},
        ]

        response = auth_client.get('/nodes/api')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['nodes']) == 2

    def test_shutdown_node_requires_permission(auth_client, mocker):
        """Test that shutdown requires permission"""

## Mock user with viewer role (no modify permission)

        response = auth_client.post('/nodes/node-1/shutdown', json={})
        assert response.status_code == 403

    def test_input_validation(auth_client):
        """Test input validation"""

## Invalid UUID format

        response = auth_client.post('/nodes/invalid-id/shutdown', json={})
        assert response.status_code == 400

---

### Deployment Checklist

- [ ] Generate SECRET_KEY: `python -c 'import secrets; print(secrets.token_hex(32))'`
- [ ] Create database: `flask db upgrade`
- [ ] Create admin user: `flask create-user --username admin --role admin`
- [ ] Generate TLS certificates
- [ ] Configure nginx reverse proxy
- [ ] Set environment variables (RPC_HOST, RPC_PORT, etc)
- [ ] Run tests: `pytest tests/`
- [ ] Deploy systemd service
- [ ] Configure log rotation
- [ ] Monitor health endpoint: `/health`
