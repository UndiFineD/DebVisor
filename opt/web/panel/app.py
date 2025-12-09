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
from functools import wraps
from typing import Dict, Any, Optional, List

# Configure structured logging
try:
    from opt.core.logging import configure_logging

    configure_logging(service_name="web-panel")
except ImportError:
    logging.basicConfig(level=logging.INFO)

# Graceful Shutdown
from opt.web.panel.graceful_shutdown import (
    init_graceful_shutdown,
    create_database_cleanup_hook,
    ShutdownConfig,
)

try:
    from flask import Flask, redirect, url_for, request, jsonify, Response
    from flask_login import current_user, login_required
    from sqlalchemy import text
    from flask_cors import CORS
    from opt.web.panel.rbac import require_permission, Resource, Action
    from opt.web.panel.config import CORSConfig
    from opt.tracing_integration import FlaskTracingMiddleware
    
    # Import extensions
    from opt.web.panel.extensions import (
        db, migrate, login_manager, csrf, limiter, socketio_server
    )
except ImportError as e:
    print(f"Error: Install requirements: pip install -r requirements.txt. Details: {e}")
    sys.exit(1)

# Optional dependencies
try:
    from prometheus_client import (
        Counter,
        Histogram,
        generate_latest,
        CONTENT_TYPE_LATEST,
    )

    HAS_PROMETHEUS = True
except ImportError:
    HAS_PROMETHEUS = False


# =============================================================================
# Structured JSON Logging
# =============================================================================


class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
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


def setup_logging(json_format: bool = True) -> logging.Logger:
    """Configure structured logging."""
    handler = logging.StreamHandler()

    if json_format and os.getenv("LOG_FORMAT", "json") == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

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
        "debvisor_http_requests_total",
        "Total HTTP requests",
        ["method", "endpoint", "status"],
    )
    REQUEST_LATENCY = Histogram(
        "debvisor_http_request_duration_seconds",
        "HTTP request latency",
        ["method", "endpoint"],
    )
    ACTIVE_SESSIONS = Counter(
        "debvisor_active_sessions_total", "Total active user sessions"
    )


# =============================================================================
# OpenAPI Specification
# =============================================================================

OPENAPI_SPEC: Dict[str, Any] = {
    "openapi": "3.0.3",
    "info": {
        "title": "DebVisor API",
        "description": "DebVisor Enterprise Platform REST API",
        "version": "2.0.0",
        "contact": {"name": "DebVisor Support", "url": "https://debvisor.io/support"},
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0",
        },
    },
    "servers": [{"url": "/api/v1", "description": "Primary API server"}],
    "paths": {
        "/health": {
            "get": {
                "summary": "Health check",
                "description": "Returns service health status",
                "responses": {"200": {"description": "Service is healthy"}},
                "tags": ["System"],
            }
        },
        "/metrics": {
            "get": {
                "summary": "Prometheus metrics",
                "description": "Returns Prometheus-formatted metrics",
                "responses": {"200": {"description": "Metrics in Prometheus format"}},
                "tags": ["System"],
            }
        },
        "/passthrough/devices": {
            "get": {
                "summary": "List PCI devices",
                "description": "Returns all PCI devices available for passthrough",
                "responses": {"200": {"description": "List of PCI devices"}},
                "tags": ["Passthrough"],
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
                                    "address": {
                                        "type": "string",
                                        "pattern": "^[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\\.[0-9]$",
                                    }
                                },
                                "required": ["address"],
                            }
                        }
                    },
                },
                "responses": {
                    "200": {"description": "Device bound successfully"},
                    "400": {"description": "Invalid request"},
                    "500": {"description": "Binding failed"},
                },
                "tags": ["Passthrough"],
            }
        },
    },
    "components": {
        "securitySchemes": {
            "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
            "cookieAuth": {"type": "apiKey", "in": "cookie", "name": "session"},
        }
    },
    "security": [{"bearerAuth": []}, {"cookieAuth": []}],
    "tags": [
        {"name": "System", "description": "System health and monitoring"},
        {"name": "Passthrough", "description": "Hardware passthrough management"},
        {"name": "Nodes", "description": "Cluster node management"},
        {"name": "Storage", "description": "Storage management"},
    ],
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


def validate_json_schema(schema: Dict[str, Any]) -> Any:
    """Decorator to validate JSON request body against schema."""

    def decorator(f: Any) -> Any:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
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
                        return (
                            jsonify({"error": f"Field {field} must be a string"}),
                            400,
                        )
                    if rules.get("type") == "integer" and not isinstance(value, int):
                        return (
                            jsonify({"error": f"Field {field} must be an integer"}),
                            400,
                        )
                    if "pattern" in rules:
                        import re

                        if not re.match(rules["pattern"], str(value)):
                            return (
                                jsonify({"error": f"Field {field} has invalid format"}),
                                400,
                            )

            return f(*args, **kwargs)

        return wrapper

    return decorator


# =============================================================================
# Application Factory
# =============================================================================


def create_app(config_name: str = "production") -> Flask:
    app = Flask(__name__)

    # Load configuration from centralized settings
    from opt.core.config import settings

    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # PERF-004: Database connection pooling configuration
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,
        "pool_recycle": settings.DB_POOL_RECYCLE,
        "pool_pre_ping": True,
    }

    # Security Headers
    app.config["CORS_HEADERS"] = "Content-Type"
    app.config["RATELIMIT_STORAGE_URI"] = settings.RATELIMIT_STORAGE_URI

    # INFRA-003: Configuration Validation (Handled by Pydantic Settings)
    # We can double check here if needed, but Settings() init would have failed
    # if critical env vars were missing in prod.

    db.init_app(app)
    # DB-001: Database Migrations
    migrate.init_app(app, db, directory="opt/migrations")
    
    # API-001: Initialize Socket.IO
    socketio_server.init_app(app)
    
    login_manager.init_app(app)
    csrf.init_app(app)
    # Configure global rate limit defaults if provided
    default_limit = app.config.get("RATELIMIT_DEFAULT", None)
    if default_limit:
        try:
            limiter._default_limits = [
                default_limit
            ]  # apply string like "100 per minute"
            logger.info(f"Global rate limit default set: {default_limit}")
        except Exception:
            logger.warning("Invalid RATELIMIT_DEFAULT format; skipping")
    limiter.init_app(app)

    # TRACE-001: Distributed Tracing
    FlaskTracingMiddleware(app)

    # INFRA-001 & INFRA-002: Graceful Shutdown & Health Checks
    shutdown_config = ShutdownConfig(
        drain_timeout_seconds=30.0, request_timeout_seconds=60.0
    )
    shutdown_manager = init_graceful_shutdown(app, shutdown_config)

    def check_db_health() -> bool:
        try:
            # Use a lightweight query to check connection
            db.session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            app.logger.error(f"Health check failed (database): {e}")
            return False

    shutdown_manager.register_health_check("database", check_db_health)

    def check_redis_health() -> bool:
        from opt.core.config import settings

        url = settings.REDIS_URL
        if not url:
            return True
        try:
            import redis

            r = redis.Redis.from_url(url)
            return r.ping()
        except Exception as e:
            app.logger.error(f"Health check failed (redis): {e}")
            return False

    shutdown_manager.register_health_check("redis", check_redis_health)

    def check_smtp_health() -> bool:
        host = os.getenv("SMTP_HOST")
        if not host:
            return True
        try:
            import smtplib

            port = int(os.getenv("SMTP_PORT", "587"))
            with smtplib.SMTP(host, port, timeout=5) as client:
                client.noop()
            return True
        except Exception as e:
            app.logger.error(f"Health check failed (smtp): {e}")
            return False

    shutdown_manager.register_health_check("smtp", check_smtp_health)

    # Register cleanup hooks
    shutdown_manager.register_cleanup_hook(
        "database", create_database_cleanup_hook(db.session)
    )

    # Initialize CORS with whitelist validation
    cors_config = {
        "origins": app.config.get("CORS_ALLOWED_ORIGINS", []),
        "methods": app.config.get("CORS_ALLOWED_METHODS", ["GET", "POST"]),
        "allow_headers": app.config.get("CORS_ALLOWED_HEADERS", ["Content-Type"]),
        "expose_headers": app.config.get("CORS_EXPOSED_HEADERS", []),
        "supports_credentials": app.config.get("CORS_ALLOW_CREDENTIALS", True),
        "max_age": app.config.get("CORS_MAX_AGE", 3600),
    }
    CORS(app, resources={r"/api/*": cors_config})

    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)

    # -------------------------------------------------------------------------
    # Request Lifecycle Hooks
    # -------------------------------------------------------------------------

    @app.before_request
    def before_request_handler() -> None:
        """Pre-request processing."""
        request.start_time = time.time() # type: ignore
        request.request_id = request.headers.get("X-Request-ID", os.urandom(8).hex()) # type: ignore

    @app.before_request
    def validate_cors_origin() -> None:
        """Validate incoming cross-origin requests against whitelist."""
        origin = request.headers.get("Origin")

        if origin:
            allowed_origins = app.config.get("CORS_ALLOWED_ORIGINS", [])
            if not CORSConfig.validate_origin(origin, allowed_origins):
                logger.warning(
                    f"CORS validation failed: {origin} not in whitelist",
                    extra={"request_id": getattr(request, "request_id", "unknown")},
                )

    @app.before_request
    def enforce_https() -> Any:
        if not app.debug and not request.is_secure:
            # Validate host header to prevent Host Header Injection
            # In production, this should be handled by the web server (Nginx/Apache)
            allowed_hosts = app.config.get("ALLOWED_HOSTS", [])
            host = request.host.split(':')[0]

            if allowed_hosts:
                if host not in allowed_hosts:
                    logger.warning(f"Invalid Host header: {request.host}")
                    return "Invalid Host header", 400
            else:
                # If ALLOWED_HOSTS is not set, we cannot safely redirect
                # as we cannot validate the Host header.
                logger.warning("ALLOWED_HOSTS not set, skipping HTTPS redirect")
                return None

            # Securely reconstruct URL to prevent host header injection
            # We trust request.url only if Host header is validated above
            url = request.url.replace("http://", "https://", 1)
            return redirect(url, code=301)
        return None

    @app.after_request
    def set_security_headers(response: Response) -> Response:
        """Set comprehensive security headers."""
        # Standard security headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Content Security Policy
        response.headers["Content-Security-Policy"] = get_csp_header()

        # Permissions Policy (formerly Feature-Policy)
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
            "magnetometer=(), microphone=(), payment=(), usb=()"
        )

        # Request ID for tracing
        response.headers["X-Request-ID"] = getattr(request, "request_id", "unknown")

        return response

    @app.after_request
    def record_metrics(response: Response) -> Response:
        """Record Prometheus metrics."""
        if HAS_PROMETHEUS:
            duration = time.time() - getattr(request, "start_time", time.time())
            endpoint = request.endpoint or "unknown"
            REQUEST_COUNT.labels(
                method=request.method, endpoint=endpoint, status=response.status_code
            ).inc()
            REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(
                duration
            )
        return response

    # -------------------------------------------------------------------------
    # System Endpoints
    # -------------------------------------------------------------------------

    @app.errorhandler(404)
    def not_found(e: Any) -> Any:
        return jsonify({"error": "Not Found", "status": 404}), 404

    @app.errorhandler(429)
    def rate_limit_exceeded(e: Any) -> Any:
        return jsonify({"error": "Rate limit exceeded", "status": 429}), 429

    @app.errorhandler(500)
    def internal_error(e: Any) -> Any:
        logger.exception("Internal server error")
        return jsonify({"error": "Internal Server Error", "status": 500}), 500

    # Note: /health/live and /health/ready are provided by the shutdown blueprint

    @app.route("/metrics")
    @limiter.exempt  # type: ignore
    def metrics() -> Any:
        """Prometheus metrics endpoint."""
        if HAS_PROMETHEUS:
            return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
        return jsonify({"error": "Prometheus client not installed"}), 501

    @app.route("/api/openapi.json")
    @login_required  # type: ignore
    @require_permission(Resource.SYSTEM, Action.READ)
    @limiter.exempt  # type: ignore
    def openapi_spec() -> Response:
        """OpenAPI specification endpoint."""
        return jsonify(OPENAPI_SPEC)

    @app.route("/api/docs")
    @login_required  # type: ignore
    @require_permission(Resource.SYSTEM, Action.READ)
    @limiter.exempt  # type: ignore
    def api_docs() -> str:
        """Swagger UI documentation page."""
        return """
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
        """

    @app.route("/health/detail")
    @login_required  # type: ignore
    @require_permission(Resource.SYSTEM, Action.READ)
    @limiter.exempt  # type: ignore
    def health_detail() -> Any:
        """Detailed health endpoint for dashboards.

        Surfaces version/build info and dependency statuses (DB/Redis/SMTP).
        """
        # Version/build info
        version = OPENAPI_SPEC.get("info", {}).get("version", "unknown")
        build = {
            "version": version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hostname": request.host,
            "debug": app.debug,
        }

        # Dependencies: reuse readiness checks inline
        # Database
        try:
            db.session.execute(db.text("SELECT 1"))
            db_status = "ok"
        except Exception:
            db_status = "error"

        # Redis
        redis_status = "skipped"
        try:
            url = os.getenv("REDIS_URL")
            if url:
                import redis

                r = redis.Redis.from_url(url)
                r.ping()
                redis_status = "ok"
        except Exception:
            redis_status = "error"

        # SMTP
        smtp_status = "skipped"
        try:
            host = os.getenv("SMTP_HOST")
            if host:
                import smtplib

                port = int(os.getenv("SMTP_PORT", "587"))
                starttls = os.getenv("SMTP_STARTTLS", "true").lower() in (
                    "1",
                    "true",
                    "yes",
                )
                user = os.getenv("SMTP_USER")
                password = os.getenv("SMTP_PASSWORD")
                client = smtplib.SMTP(host, port, timeout=5)
                try:
                    if starttls:
                        client.starttls()
                    if user and password:
                        client.login(user, password)
                    smtp_status = "ok"
                finally:
                    try:
                        client.quit()
                    except Exception as e:
                        logger.debug(f"SMTP quit error: {e}")
        except Exception:
            smtp_status = "error"

        is_healthy = (
            db_status == "ok"
            and redis_status in ("ok", "skipped")
            and smtp_status in ("ok", "skipped")
        )

        detail = {
            "status": "ok" if is_healthy else "degraded",
            "build": build,
            "checks": {
                "database": db_status,
                "redis": redis_status,
                "smtp": smtp_status,
            },
        }
        return jsonify(detail), 200 if detail["status"] == "ok" else 503

    @app.route("/")
    def index() -> Any:
        if current_user.is_authenticated:
            return redirect(url_for("auth.profile"))
        return redirect(url_for("auth.login"))

    # -------------------------------------------------------------------------
    # Register Blueprints
    # -------------------------------------------------------------------------

    try:
        from opt.web.panel.routes import auth_bp, nodes_bp, storage_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(nodes_bp)
        app.register_blueprint(storage_bp)
    except ImportError as e:
        logger.warning(f"Could not import route blueprints: {e}")

    # Register health check endpoints (HEALTH-001)
    try:
        from opt.web.panel.routes.health import health_bp

        app.register_blueprint(health_bp)
        logger.info("Health check endpoints registered at /health/*")
    except ImportError as e:
        logger.warning(f"Health check blueprint not available: {e}")

    # Register passthrough blueprint
    try:
        from opt.web.panel.routes.passthrough import passthrough_bp

        app.register_blueprint(passthrough_bp)
    except ImportError:
        logger.debug("Passthrough blueprint not available")

    @app.context_processor
    def inject_user() -> Dict[str, Any]:
        return {"current_user": current_user}

    # DB-001: Database Migrations - db.create_all() removed in favor of Flask-Migrate
    # with app.app_context():
    #     db.create_all()

    logger.info(
        "DebVisor Web Panel initialized",
        extra={"config": config_name, "debug": app.debug},
    )

    return app


# Export for external use
__all__ = ["create_app", "db", "limiter", "validate_json_schema", "socketio_server"]


if __name__ == "__main__":
    app = create_app(os.getenv("FLASK_ENV", "production"))
    # nosec B104 - Binding to all interfaces is intended for containerized deployment
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"), port=443, debug=False
    )  # nosec B104
