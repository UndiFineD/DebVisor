#!/usr/bin/env python3
"""
DebVisor Web Panel - Flask Application
Main entry point for cluster management UI.

Features:
- CORS whitelist validation on all cross-origin requests
- Content Security Policy (CSP) headers
- Security headers enforcement
- CSRF protection
- Rate limiting
- HTTPS enforcement
- OpenAPI/Swagger documentation
- Prometheus metrics endpoint
- Structured JSON logging
"""

import os
import sys
import logging
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from functools import wraps

try:
    from flask import Flask, redirect, url_for, request, jsonify, Response
    from flask_login import LoginManager, current_user
    from flask_sqlalchemy import SQLAlchemy
    from flask_wtf.csrf import CSRFProtect
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    from flask_cors import CORS
except ImportError:
    print('Error: Install requirements: pip install -r requirements.txt')
    sys.exit(1)

# Optional dependencies
try:
    from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
    HAS_PROMETHEUS = True
except ImportError:
    HAS_PROMETHEUS = False

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)


# =============================================================================
# Structured JSON Logging
# =============================================================================

class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        
        return json.dumps(log_data)


def setup_logging(json_format: bool = True):
    """Configure structured logging."""
    handler = logging.StreamHandler()
    
    if json_format and os.getenv("LOG_FORMAT", "json") == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    
    return logging.getLogger(__name__)


logger = setup_logging()


# =============================================================================
# Prometheus Metrics
# =============================================================================

if HAS_PROMETHEUS:
    REQUEST_COUNT = Counter(
        'debvisor_http_requests_total',
        'Total HTTP requests',
        ['method', 'endpoint', 'status']
    )
    REQUEST_LATENCY = Histogram(
        'debvisor_http_request_duration_seconds',
        'HTTP request latency',
        ['method', 'endpoint']
    )
    ACTIVE_SESSIONS = Counter(
        'debvisor_active_sessions_total',
        'Total active user sessions'
    )


# =============================================================================
# OpenAPI Specification
# =============================================================================

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "DebVisor API",
        "description": "DebVisor Enterprise Platform REST API",
        "version": "2.0.0",
        "contact": {
            "name": "DebVisor Support",
            "url": "https://debvisor.io/support"
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0"
        }
    },
    "servers": [
        {"url": "/api/v1", "description": "Primary API server"}
    ],
    "paths": {
        "/health": {
            "get": {
                "summary": "Health check",
                "description": "Returns service health status",
                "responses": {
                    "200": {"description": "Service is healthy"}
                },
                "tags": ["System"]
            }
        },
        "/metrics": {
            "get": {
                "summary": "Prometheus metrics",
                "description": "Returns Prometheus-formatted metrics",
                "responses": {
                    "200": {"description": "Metrics in Prometheus format"}
                },
                "tags": ["System"]
            }
        },
        "/passthrough/devices": {
            "get": {
                "summary": "List PCI devices",
                "description": "Returns all PCI devices available for passthrough",
                "responses": {
                    "200": {"description": "List of PCI devices"}
                },
                "tags": ["Passthrough"]
            }
        },
        "/passthrough/bind": {
            "post": {
                "summary": "Bind device to VFIO",
                "description": "Binds a PCI device to VFIO driver for passthrough",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "address": {"type": "string", "pattern": "^[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\\.[0-9]$"}
                                },
                                "required": ["address"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Device bound successfully"},
                    "400": {"description": "Invalid request"},
                    "500": {"description": "Binding failed"}
                },
                "tags": ["Passthrough"]
            }
        }
    },
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            },
            "cookieAuth": {
                "type": "apiKey",
                "in": "cookie",
                "name": "session"
            }
        }
    },
    "security": [
        {"bearerAuth": []},
        {"cookieAuth": []}
    ],
    "tags": [
        {"name": "System", "description": "System health and monitoring"},
        {"name": "Passthrough", "description": "Hardware passthrough management"},
        {"name": "Nodes", "description": "Cluster node management"},
        {"name": "Storage", "description": "Storage management"}
    ]
}


# =============================================================================
# Content Security Policy
# =============================================================================

def get_csp_header() -> str:
    """Generate Content Security Policy header."""
    policies = [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'",  # Adjust based on needs
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data: https:",
        "font-src 'self' data:",
        "connect-src 'self' wss: https:",
        "frame-ancestors 'none'",
        "form-action 'self'",
        "base-uri 'self'",
        "object-src 'none'",
        "upgrade-insecure-requests",
    ]
    return "; ".join(policies)


# =============================================================================
# Request Validation
# =============================================================================

def validate_json_schema(schema: dict):
    """Decorator to validate JSON request body against schema."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({"error": "Content-Type must be application/json"}), 400
            
            data = request.get_json()
            
            # Basic schema validation (for complex validation use jsonschema)
            required = schema.get("required", [])
            properties = schema.get("properties", {})
            
            for field in required:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
            
            for field, rules in properties.items():
                if field in data:
                    value = data[field]
                    if rules.get("type") == "string" and not isinstance(value, str):
                        return jsonify({"error": f"Field {field} must be a string"}), 400
                    if rules.get("type") == "integer" and not isinstance(value, int):
                        return jsonify({"error": f"Field {field} must be an integer"}), 400
                    if "pattern" in rules:
                        import re
                        if not re.match(rules["pattern"], str(value)):
                            return jsonify({"error": f"Field {field} has invalid format"}), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


# =============================================================================
# Application Factory
# =============================================================================

def create_app(config_name='production'):
    app = Flask(__name__)
    
    try:
        from config import config, CORSConfig
        app.config.from_object(config[config_name])
    except ImportError:
        # Fallback configuration
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            if os.getenv('FLASK_ENV') == 'production':
                raise RuntimeError(
                    "SECRET_KEY environment variable must be set in production. "
                    "Generate with: python -c 'import secrets; print(secrets.token_hex(32))'"
                )
            logger.warning("Using insecure default SECRET_KEY - DO NOT USE IN PRODUCTION")
            secret_key = 'dev-key-change-in-production'
        app.config['SECRET_KEY'] = secret_key
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///debvisor.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # PERF-004: Database connection pooling configuration
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': int(os.getenv('DB_POOL_SIZE', '20')),
            'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', '10')),
            'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', '30')),
            'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', '3600')),
            'pool_pre_ping': True,  # Verify connections before checkout
        }
        CORSConfig = None
    
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    # Configure global rate limit defaults if provided
    default_limit = app.config.get('RATELIMIT_DEFAULT', None)
    if default_limit:
        try:
            limiter._default_limits = [default_limit]  # apply string like "100 per minute"
            logger.info(f"Global rate limit default set: {default_limit}")
        except Exception:
            logger.warning("Invalid RATELIMIT_DEFAULT format; skipping")
    limiter.init_app(app)
    
    # Initialize CORS with whitelist validation
    cors_config = {
        'origins': app.config.get('CORS_ALLOWED_ORIGINS', []),
        'methods': app.config.get('CORS_ALLOWED_METHODS', ['GET', 'POST']),
        'allow_headers': app.config.get('CORS_ALLOWED_HEADERS', ['Content-Type']),
        'expose_headers': app.config.get('CORS_EXPOSED_HEADERS', []),
        'supports_credentials': app.config.get('CORS_ALLOW_CREDENTIALS', True),
        'max_age': app.config.get('CORS_MAX_AGE', 3600),
    }
    CORS(app, resources={r'/api/*': cors_config})
    
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
    
    # -------------------------------------------------------------------------
    # Request Lifecycle Hooks
    # -------------------------------------------------------------------------
    
    @app.before_request
    def before_request_handler():
        """Pre-request processing."""
        request.start_time = time.time()
        request.request_id = request.headers.get('X-Request-ID', os.urandom(8).hex())
    
    @app.before_request
    def validate_cors_origin():
        """Validate incoming cross-origin requests against whitelist."""
        origin = request.headers.get('Origin')
        
        if origin and CORSConfig:
            allowed_origins = app.config.get('CORS_ALLOWED_ORIGINS', [])
            if not CORSConfig.validate_origin(origin, allowed_origins):
                logger.warning(
                    f"CORS validation failed: {origin} not in whitelist",
                    extra={"request_id": getattr(request, 'request_id', 'unknown')}
                )
    
    @app.before_request
    def enforce_https():
        if not app.debug and not request.is_secure:
            return redirect(request.url.replace('http://', 'https://'), code=301)
    
    @app.after_request
    def set_security_headers(response):
        """Set comprehensive security headers."""
        # Standard security headers
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = get_csp_header()
        
        # Permissions Policy (formerly Feature-Policy)
        response.headers['Permissions-Policy'] = (
            "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
            "magnetometer=(), microphone=(), payment=(), usb=()"
        )
        
        # Request ID for tracing
        response.headers['X-Request-ID'] = getattr(request, 'request_id', 'unknown')
        
        return response
    
    @app.after_request
    def record_metrics(response):
        """Record Prometheus metrics."""
        if HAS_PROMETHEUS:
            duration = time.time() - getattr(request, 'start_time', time.time())
            endpoint = request.endpoint or 'unknown'
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                status=response.status_code
            ).inc()
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=endpoint
            ).observe(duration)
        return response
    
    # -------------------------------------------------------------------------
    # System Endpoints
    # -------------------------------------------------------------------------
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not Found', 'status': 404}), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return jsonify({'error': 'Rate limit exceeded', 'status': 429}), 429
    
    @app.errorhandler(500)
    def internal_error(e):
        logger.exception("Internal server error")
        return jsonify({'error': 'Internal Server Error', 'status': 500}), 500
    
    @app.route('/health')
    @limiter.exempt
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'version': '2.0.0'
        }), 200
    
    @app.route('/ready')
    @limiter.exempt
    def readiness():
        """Kubernetes readiness probe."""
        # Check database connectivity
        try:
            db.session.execute(db.text('SELECT 1'))
            db_status = 'ok'
        except Exception:
            db_status = 'error'

        # Optional: Check Redis connectivity for rate limiting if configured
        redis_status = 'skipped'
        try:
            import os as _os
            url = _os.getenv('REDIS_URL')
            if url:
                try:
                    import redis as _redis
                    r = _redis.Redis.from_url(url)
                    r.ping()
                    redis_status = 'ok'
                except Exception:
                    redis_status = 'error'
        except Exception:
            redis_status = 'skipped'

        # Optional: Check SMTP connectivity if configured
        smtp_status = 'skipped'
        try:
            import os as _os
            host = _os.getenv('SMTP_HOST')
            if host:
                import smtplib as _smtplib
                port = int(_os.getenv('SMTP_PORT', '587'))
                starttls = _os.getenv('SMTP_STARTTLS', 'true').lower() in ('1','true','yes')
                user = _os.getenv('SMTP_USER')
                password = _os.getenv('SMTP_PASSWORD')
                client = _smtplib.SMTP(host, port, timeout=5)
                try:
                    if starttls:
                        client.starttls()
                    if user and password:
                        client.login(user, password)
                    smtp_status = 'ok'
                finally:
                    try:
                        client.quit()
                    except Exception:
                        pass
        except Exception:
            smtp_status = 'error'
        
        ready = (
            db_status == 'ok'
            and (redis_status in ('ok', 'skipped'))
            and (smtp_status in ('ok', 'skipped'))
        )
        return jsonify({
            'ready': ready,
            'checks': {
                'database': db_status,
                'redis': redis_status,
                'smtp': smtp_status
            }
        }), 200 if ready else 503
    
    @app.route('/metrics')
    @limiter.exempt
    def metrics():
        """Prometheus metrics endpoint."""
        if HAS_PROMETHEUS:
            return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
        return jsonify({'error': 'Prometheus client not installed'}), 501
    
    @app.route('/api/openapi.json')
    @limiter.exempt
    def openapi_spec():
        """OpenAPI specification endpoint."""
        return jsonify(OPENAPI_SPEC)
    
    @app.route('/api/docs')
    @limiter.exempt
    def api_docs():
        """Swagger UI documentation page."""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>DebVisor API Documentation</title>
            <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
            <script>
                SwaggerUIBundle({
                    url: '/api/openapi.json',
                    dom_id: '#swagger-ui',
                    presets: [SwaggerUIBundle.presets.apis],
                    layout: "BaseLayout"
                });
            </script>
        </body>
        </html>
        '''

    @app.route('/health/detail')
    @limiter.exempt
    def health_detail():
        """Detailed health endpoint for dashboards.

        Surfaces version/build info and dependency statuses (DB/Redis/SMTP).
        """
        # Version/build info
        version = OPENAPI_SPEC.get('info', {}).get('version', 'unknown')
        build = {
            'version': version,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'hostname': request.host,
            'debug': app.debug,
        }

        # Dependencies: reuse readiness checks inline
        # Database
        try:
            db.session.execute(db.text('SELECT 1'))
            db_status = 'ok'
        except Exception:
            db_status = 'error'

        # Redis
        redis_status = 'skipped'
        try:
            url = os.getenv('REDIS_URL')
            if url:
                import redis
                r = redis.Redis.from_url(url)
                r.ping()
                redis_status = 'ok'
        except Exception:
            redis_status = 'error'

        # SMTP
        smtp_status = 'skipped'
        try:
            host = os.getenv('SMTP_HOST')
            if host:
                import smtplib
                port = int(os.getenv('SMTP_PORT', '587'))
                starttls = os.getenv('SMTP_STARTTLS', 'true').lower() in ('1','true','yes')
                user = os.getenv('SMTP_USER')
                password = os.getenv('SMTP_PASSWORD')
                client = smtplib.SMTP(host, port, timeout=5)
                try:
                    if starttls:
                        client.starttls()
                    if user and password:
                        client.login(user, password)
                    smtp_status = 'ok'
                finally:
                    try:
                        client.quit()
                    except Exception:
                        pass
        except Exception:
            smtp_status = 'error'

        detail = {
            'status': 'ok' if (db_status == 'ok' and redis_status in ('ok','skipped') and smtp_status in ('ok','skipped')) else 'degraded',
            'build': build,
            'checks': {
                'database': db_status,
                'redis': redis_status,
                'smtp': smtp_status,
            }
        }
        return jsonify(detail), 200 if detail['status'] == 'ok' else 503
    
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('auth.profile'))
        return redirect(url_for('auth.login'))
    
    # -------------------------------------------------------------------------
    # Register Blueprints
    # -------------------------------------------------------------------------
    
    try:
        from routes import auth_bp, nodes_bp, storage_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(nodes_bp)
        app.register_blueprint(storage_bp)
    except ImportError:
        logger.warning("Could not import route blueprints")
    
    # Register health check endpoints (HEALTH-001)
    try:
        from routes.health import health_bp
        app.register_blueprint(health_bp)
        logger.info("Health check endpoints registered at /health/*")
    except ImportError:
        logger.warning("Health check blueprint not available")
    
    # Register passthrough blueprint
    try:
        from routes.passthrough import passthrough_bp
        app.register_blueprint(passthrough_bp)
    except ImportError:
        logger.debug("Passthrough blueprint not available")
    
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}
    
    with app.app_context():
        db.create_all()
    
    logger.info("DebVisor Web Panel initialized", extra={
        "config": config_name,
        "debug": app.debug
    })
    
    return app


# Export for external use
__all__ = ['create_app', 'db', 'limiter', 'validate_json_schema']


if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'production'))
    app.run(host='0.0.0.0', port=443, debug=False)
