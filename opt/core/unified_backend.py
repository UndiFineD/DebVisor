#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Unified Backend Abstraction - Enterprise Implementation.

Provides a shared operations layer for both TUI and Web Panel:
- Action dispatch with async support (operations, batch jobs, background tasks)
- Permission mediation (RBAC with role hierarchies)
- Event publishing (WebSocket + CLI subscription hooks)
- Audit logging with structured format
- Result caching with TTL and invalidation
- Rate limiting and concurrency control
- Middleware pipeline for cross-cutting concerns
- Structured JSON logging with correlation IDs
"""

from __future__ import annotations
from datetime import datetime, timezone
import logging
import time
import threading
import json
import hashlib
import os
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import uuid4
from enum import Enum
from collections import defaultdict
from functools import wraps

_logger=logging.getLogger(__name__)


# =============================================================================
# Structured JSON Logging
# =============================================================================
class StructuredLogFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.

    Outputs log records as single-line JSON for easy parsing by
    log aggregators (ELK, Loki, Splunk, etc.)
    """

    def __init__(self, servicename: str="debvisor", includeextra: bool=True) -> None:
        super().__init__()
        self.service_name=service_name  # type: ignore[name-defined]
        self.include_extra=include_extra  # type: ignore[name-defined]
        self._hostname=os.uname().nodename if hasattr(os, "uname") else "unknown"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        _log_entry={
            "@timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.service_name,
            "host": self._hostname,
        }

        # Add location info
        log_entry["source"] = {  # type: ignore[name-defined]
            "file": record.filename,
            "line": record.lineno,
            "function": record.funcName,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = {  # type: ignore[name-defined]
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info),
            }

        # Add extra fields from record
        if self.include_extra:
            _extra_fields={}  # type: ignore[var-annotated]
            for key, value in record.__dict__.items():
                if key not in (
                    "name",
                    "msg",
                    "args",
                    "created",
                    "filename",
                    "funcName",
                    "levelname",
                    "levelno",
                    "lineno",
                    "module",
                    "msecs",
                    "pathname",
                    "process",
                    "processName",
                    "relativeCreated",
                    "stack_info",
                    "exc_info",
                    "exc_text",
                    "thread",
                    "threadName",
                    "message",
                    "asctime",
                ):
                    try:
                    # Ensure value is JSON serializable
                        json.dumps(value)
                        extra_fields[key] = value  # type: ignore[name-defined]
                    except (TypeError, ValueError):
                        extra_fields[key] = str(value)  # type: ignore[name-defined]

            if extra_fields:  # type: ignore[name-defined]
                log_entry["extra"] = extra_fields  # type: ignore[name-defined]

        return json.dumps(log_entry, default=str)  # type: ignore[name-defined]


class CorrelationLogAdapter(logging.LoggerAdapter[Any]):
    """
    Log adapter that adds correlation ID to all log messages.

    Usage:
        _log=CorrelationLogAdapter(logger, {"correlation_id": "abc-123"})
        log.info("Processing request")    # includes correlation_id
    """

    def process(self, msg, kwargs) -> None:  # type: ignore[override]
        """Add correlation context to log record."""
        _extra=kwargs.get("extra", {})
        extra.update(self.extra)  # type: ignore[name-defined]
        kwargs["extra"] = extra  # type: ignore[name-defined]
        return msg, kwargs  # type: ignore[return-value]


def configure_structured_logging(
    level: int=logging.INFO,
    service_name: str="debvisor",
    log_file: Optional[str] = None,
    json_format: bool=True,
) -> None:
    """
    Configure structured logging for the application.

    Args:
        level: Logging level
        service_name: Service name for log entries
        log_file: Optional file path for JSON logs
        json_format: Use JSON format (True) or standard format (False)
    """
    _root_logger=logging.getLogger()
    root_logger.setLevel(level)  # type: ignore[name-defined]

    # Remove existing handlers
    for handler in root_logger.handlers[:]:  # type: ignore[name-defined]
        root_logger.removeHandler(handler)  # type: ignore[name-defined]

    if json_format:
        _formatter=StructuredLogFormatter(service_name=service_name)  # type: ignore[call-arg]
    else:
        formatter=logging.Formatter(  # type: ignore[assignment]
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    # Console handler
    _console_handler=logging.StreamHandler()
    console_handler.setFormatter(formatter)  # type: ignore[name-defined]
    root_logger.addHandler(console_handler)  # type: ignore[name-defined]

    # File handler (JSON logs)
    if log_file:
        _file_handler=logging.FileHandler(log_file)
        file_handler.setFormatter(StructuredLogFormatter(service_name=service_name))  # type: ignore[call-arg, name-defined]
        root_logger.addHandler(file_handler)  # type: ignore[name-defined]

    logger.info(  # type: ignore[name-defined]
        "Structured logging configured",
        _extra={
            "service": service_name,
            "level": logging.getLevelName(level),
            "json_format": json_format,
            "log_file": log_file,
        },
    )


class ActionError(Exception):
    """Base exception for action errors."""

    pass


class PermissionDenied(ActionError):
    """Permission denied for action."""

    pass


class RateLimitExceeded(ActionError):
    """Rate limit exceeded."""

    pass


class ActionStatus(Enum):
    """Action execution status."""

    PENDING="pending"
    RUNNING="running"
    COMPLETED="completed"
    FAILED="failed"
    CANCELLED="cancelled"
    TIMEOUT="timeout"


class Permission(Enum):
    """Base permissions."""

    READ="read"
    WRITE="write"
    ADMIN="admin"
    EXECUTE="execute"
    DELETE="delete"


class Role(Enum):
    """User roles with permission sets."""

    VIEWER="viewer"
    OPERATOR="operator"
    ADMIN="admin"
    SUPER_ADMIN="super_admin"


# Role to permission mapping
ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.VIEWER: {Permission.READ},
    Role.OPERATOR: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
    Role.ADMIN: {
        Permission.READ,
        Permission.WRITE,
        Permission.EXECUTE,
        Permission.DELETE,
    },
    Role.SUPER_ADMIN: {p for p in Permission},
}


@dataclass
class ResourceQuota:
    """Resource quotas for a tenant."""

    max_vms: int=10
    max_cpu_cores: int=20
    max_memory_gb: int=64
    max_storage_gb: int=1000
    max_networks: int=5
    max_snapshots: int=50


@dataclass
class Tenant:
    """Tenant definition."""

    id: str
    name: str
    description: str=""
    created_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    status: str="active"
    quotas: ResourceQuota=field(default_factory=ResourceQuota)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TenantManager:
    """Manages tenants and their resources."""

    def __init__(self) -> None:
        self._tenants: Dict[str, Tenant] = {}
        self._lock=threading.RLock()

        # Create default tenant
        self.create_tenant(
            "default",
            "Default Tenant",
            ResourceQuota(  # type: ignore[call-arg]
                _max_vms=100, max_cpu_cores=200, max_memory_gb=512, max_storage_gb=5000
            ),
        )

    def create_tenant(
        self, tenant_id: str, name: str, quotas: Optional[ResourceQuota] = None
    ) -> Tenant:
        """Create a new tenant."""
        with self._lock:
            if tenant_id in self._tenants:
                raise ValueError(f"Tenant {tenant_id} already exists")

            _tenant=Tenant(id=tenant_id, name=name, quotas=quotas or ResourceQuota())
            self._tenants[tenant_id] = tenant  # type: ignore[name-defined]
            logger.info(f"Created tenant: {tenant_id}")  # type: ignore[name-defined]
            return tenant  # type: ignore[name-defined]

    def get_tenant(self, tenantid: str) -> Optional[Tenant]:
        """Get tenant by ID."""
        with self._lock:
            return self._tenants.get(tenant_id)  # type: ignore[name-defined]

    def update_quotas(self, tenantid: str, quotas: ResourceQuota) -> bool:
        """Update tenant quotas."""
        with self._lock:
            _tenant=self._tenants.get(tenant_id)  # type: ignore[name-defined]
            if not tenant:  # type: ignore[name-defined]
                return False
            tenant.quotas=quotas  # type: ignore[name-defined]
            logger.info(f"Updated quotas for tenant: {tenant_id}")  # type: ignore[name-defined]
            return True

    def list_tenants(self) -> List[Tenant]:
        """List all tenants."""
        with self._lock:
            return list(self._tenants.values())


@dataclass
class ActionContext:
    """Context for action execution."""

    request_id: str
    user_id: str
    user_role: Role
    tenant_id: Optional[str] = None
    source: str="unknown"    # web, tui, api, grpc
    client_ip: Optional[str] = None
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def has_permission(self, permission: Permission) -> bool:
        """Check if context has required permission."""
        return permission in ROLE_PERMISSIONS.get(self.user_role, set())


@dataclass
class ActionResult:
    """Result of action execution."""

    id: str
    action: str
    status: ActionStatus
    started_at: datetime
    completed_at: Optional[datetime]
    data: Dict[str, Any]
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration_ms: Optional[int] = None
    context: Optional[ActionContext] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "action": self.action,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "data": self.data,
            "error": self.error,
            "error_code": self.error_code,
            "duration_ms": self.duration_ms,
        }


@dataclass
class ActionDefinition:
    """Definition of a registered action."""

    name: str
    handler: Callable[..., Any]
    required_permission: Permission
    description: str=""
    is_async: bool=False
    timeout_seconds: int=300
    rate_limit: Optional[int] = None    # requests per minute
    cacheable: bool=False
    cache_ttl: int=60


@dataclass
class AuditEntry:
    """Audit log entry."""

    timestamp: datetime
    action: str
    user_id: str
    tenant_id: Optional[str]
    source: str
    request_id: str
    success: bool
    error: Optional[str] = None
    duration_ms: Optional[int] = None
    params_hash: Optional[str] = None    # Hash of params for security

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "action": self.action,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "source": self.source,
            "request_id": self.request_id,
            "success": self.success,
            "error": self.error,
            "duration_ms": self.duration_ms,
        }


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, requestsper_minute: int=60) -> None:
        self._limit=requests_per_minute  # type: ignore[name-defined]
        self._window_seconds=60
        self._requests: Dict[str, List[float]] = defaultdict(list)
        self._lock=threading.Lock()

    def check(self, key: str) -> bool:
        """Check if request is allowed."""
        with self._lock:
            _now=time.time()
            window_start=now - self._window_seconds  # type: ignore[name-defined]

            # Clean old requests
            self._requests[key] = [t for t in self._requests[key] if t > window_start]

            if len(self._requests[key]) >= self._limit:
                return False

            self._requests[key].append(now)  # type: ignore[name-defined]
            return True

    def reset(self, key: str) -> None:
        """Reset rate limit for key."""
        with self._lock:
            self._requests.pop(key, None)


class CacheManager:
    """TTL-based cache with invalidation."""

    def __init__(self, defaultttl: int=60) -> None:
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._default_ttl=default_ttl  # type: ignore[name-defined]
        self._lock=threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        with self._lock:
            _entry=self._cache.get(key)
            if not entry:
                return None
            if time.time() > entry["expires_at"]:
                del self._cache[key]
                return None
            return entry["value"]

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached value with TTL."""
        with self._lock:
            self._cache[key] = {
                "value": value,
                "expires_at": time.time() + (ttl or self._default_ttl),
            }

    def delete(self, key: str) -> None:
        """Delete cached entry."""
        with self._lock:
            self._cache.pop(key, None)

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        with self._lock:
            keys_to_delete=[k for k in self._cache if pattern in k]
            for key in keys_to_delete:
                del self._cache[key]
            return len(keys_to_delete)

    def clear(self) -> None:
        """Clear all cache."""
        with self._lock:
            self._cache.clear()

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            _now=time.time()
            _valid=sum(1 for e in self._cache.values() if e["expires_at"] > now)  # type: ignore[name-defined]
            return {
                "total_entries": len(self._cache),
                "valid_entries": valid,  # type: ignore[name-defined]
                "expired_entries": len(self._cache) - valid,  # type: ignore[name-defined]
            }


class EventBus:
    """Simple event bus for action notifications."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[..., Any]]] = defaultdict(list[Any])
        self._lock=threading.Lock()

    def subscribe(self, eventtype: str, handler: Callable[..., Any]) -> None:
        """Subscribe to event type."""
        with self._lock:
            self._subscribers[event_type].append(handler)  # type: ignore[name-defined]

    def unsubscribe(self, eventtype: str, handler: Callable[..., Any]) -> None:
        """Unsubscribe from event type."""
        with self._lock:
            if handler in self._subscribers[event_type]:  # type: ignore[name-defined]
                self._subscribers[event_type].remove(handler)  # type: ignore[name-defined]

    def publish(self, eventtype: str, data: Dict[str, Any]) -> None:
        """Publish event to subscribers."""
        with self._lock:
            _handlers=list(self._subscribers.get(event_type, []))  # type: ignore[name-defined]
            handlers.extend(self._subscribers.get("*", []))    # Wildcard subscribers  # type: ignore[name-defined]

        for handler in handlers:  # type: ignore[name-defined]
            try:
                handler(event_type, data)  # type: ignore[name-defined]
            except Exception as e:
                logger.error(f"Event handler error for {event_type}: {e}")  # type: ignore[name-defined]


# Middleware type
Middleware=Callable[[str, Dict[str, Any], ActionContext, Callable[..., Any]], ActionResult]


class UnifiedBackend:
    """Enterprise unified backend for TUI/Web Panel convergence."""

    def __init__(self) -> None:
        self._actions: Dict[str, ActionDefinition] = {}
        self._audit_log: List[AuditEntry] = []
        self._max_audit_entries=10000

        # Core components
        self._cache=CacheManager(default_ttl=60)  # type: ignore[call-arg]
        self._rate_limiter=RateLimiter(requests_per_minute=100)  # type: ignore[call-arg]
        self._event_bus=EventBus()
        self._tenant_manager=TenantManager()

        # Middleware pipeline
        self._middlewares: List[Middleware] = []

        # Async job tracking
        self._running_jobs: Dict[str, ActionResult] = {}

        # Thread safety
        self._lock=threading.RLock()

        # Background cleanup task
        self._cleanup_thread: Optional[threading.Thread] = None
        self._stop_event=threading.Event()

        logger.info("UnifiedBackend initialized")  # type: ignore[name-defined]

    def get_tenant_manager(self) -> TenantManager:
        """Get the tenant manager instance."""
        return self._tenant_manager

    def register_action(
        self,
        name: str,
        handler: Callable[..., Any],
        permission: Permission=Permission.EXECUTE,
        description: str="",
        is_async: bool=False,
        timeout: int=300,
        rate_limit: Optional[int] = None,
        cacheable: bool=False,
        cache_ttl: int=60,
    ) -> None:
        """Register an action handler."""
        _definition=ActionDefinition(  # type: ignore[call-arg]
            _name=name,
            _handler=handler,
            _required_permission=permission,
            _description=description,
            _is_async=is_async,
            _timeout_seconds=timeout,
            _rate_limit=rate_limit,
            _cacheable=cacheable,
            _cache_ttl=cache_ttl,
        )
        self._actions[name] = definition  # type: ignore[name-defined]
        logger.info(f"Registered action: {name} (permission={permission.value})")  # type: ignore[name-defined]

    def add_middleware(self, middleware: Middleware) -> None:
        """Add middleware to the processing pipeline."""
        self._middlewares.append(middleware)

    def execute(
        self, name: str, params: Dict[str, Any], context: Optional[ActionContext] = None
    ) -> ActionResult:
        """Execute an action synchronously."""
        # Create default context if not provided
        if context is None:
            context=ActionContext(  # type: ignore[call-arg]
                _request_id=str(uuid4()),
                _user_id="system",
                _user_role=Role.SUPER_ADMIN,
                _source="internal",
                _tenant_id="default",
            )

        # Validate tenant
        if context.tenant_id:
            _tenant=self._tenant_manager.get_tenant(context.tenant_id)
            if not tenant:  # type: ignore[name-defined]
                return ActionResult(  # type: ignore[call-arg]
                    _id=str(uuid4()),
                    _action=name,
                    _status=ActionStatus.FAILED,
                    _started_at=datetime.now(timezone.utc),
                    _completed_at=datetime.now(timezone.utc),
                    _data={},
                    _error=f"Invalid tenant: {context.tenant_id}",
                    _error_code="INVALID_TENANT",
                    _context=context,
                )
            if tenant.status != "active":  # type: ignore[name-defined]
                return ActionResult(  # type: ignore[call-arg]
                    _id=str(uuid4()),
                    _action=name,
                    _status=ActionStatus.FAILED,
                    _started_at=datetime.now(timezone.utc),
                    _completed_at=datetime.now(timezone.utc),
                    _data={},
                    _error=f"Tenant is not active: {context.tenant_id}",
                    _error_code="TENANT_INACTIVE",
                    _context=context,
                )

        _started_at=datetime.now(timezone.utc)

        # Check if action exists
        _definition=self._actions.get(name)
        if not definition:  # type: ignore[name-defined]
            return ActionResult(  # type: ignore[call-arg]
                _id=context.request_id,
                _action=name,
                _status=ActionStatus.FAILED,
                _started_at=started_at,  # type: ignore[name-defined]
                _completed_at=datetime.now(timezone.utc),
                _data={},
                _error=f"Unknown action: {name}",
                _error_code="ACTION_NOT_FOUND",
                _context=context,
            )

        # Permission check
        if not context.has_permission(definition.required_permission):  # type: ignore[name-defined]
            self._audit(name, context, False, error="Permission denied")
            return ActionResult(  # type: ignore[call-arg]
                _id=context.request_id,
                _action=name,
                _status=ActionStatus.FAILED,
                _started_at=started_at,  # type: ignore[name-defined]
                _completed_at=datetime.now(timezone.utc),
                _data={},
                _error=f"Permission denied: requires {definition.required_permission.value}",  # type: ignore[name-defined]
                _error_code="PERMISSION_DENIED",
                _context=context,
            )

        # Rate limiting
        if definition.rate_limit:  # type: ignore[name-defined]
            rate_key=f"{name}:{context.user_id}"
            if not self._rate_limiter.check(rate_key):
                self._audit(name, context, False, error="Rate limit exceeded")
                return ActionResult(  # type: ignore[call-arg]
                    _id=context.request_id,
                    _action=name,
                    _status=ActionStatus.FAILED,
                    _started_at=started_at,  # type: ignore[name-defined]
                    _completed_at=datetime.now(timezone.utc),
                    _data={},
                    _error="Rate limit exceeded",
                    _error_code="RATE_LIMIT_EXCEEDED",
                    _context=context,
                )

        # Check cache for cacheable actions
        if definition.cacheable:  # type: ignore[name-defined]
            _cache_key=self._cache_key(name, params)
            _cached=self._cache.get(cache_key)  # type: ignore[name-defined]
            if cached is not None:  # type: ignore[name-defined]
                logger.debug(f"Cache hit for {name}")  # type: ignore[name-defined]
                return ActionResult(  # type: ignore[call-arg]
                    _id=context.request_id,
                    _action=name,
                    _status=ActionStatus.COMPLETED,
                    _started_at=started_at,  # type: ignore[name-defined]
                    _completed_at=datetime.now(timezone.utc),
                    _data=cached,  # type: ignore[name-defined]
                    _context=context,
                )

        # Execute with middleware pipeline
        try:
            _result=self._execute_with_middleware(name, params, context, definition)  # type: ignore[arg-type, name-defined]

            # Cache result if cacheable
            if definition.cacheable and result.status == ActionStatus.COMPLETED:  # type: ignore[name-defined, union-attr]
                _cache_key=self._cache_key(name, params)
                self._cache.set(cache_key, result.data, definition.cache_ttl)  # type: ignore[arg-type, name-defined, union-attr]

            # Publish event
            self._event_bus.publish(
                f"action.{name}",
                {
                    "action": name,
                    "status": result.status.value,  # type: ignore[name-defined, union-attr]
                    "user_id": context.user_id,
                    "request_id": context.request_id,
                },
            )

            return result  # type: ignore[name-defined, return-value]

        except Exception as e:
            logger.exception(f"Action {name} failed with exception")  # type: ignore[name-defined, union-attr]
            _completed_at=datetime.now(timezone.utc)
            _duration_ms=int((completed_at - started_at).total_seconds() * 1000)  # type: ignore[name-defined, operator]

            self._audit(  # type: ignore[call-arg]
                name,
                context,
                False,
                _error=str(e),
                _duration_ms=duration_ms,  # type: ignore[name-defined]
                _params=params,
            )

            return ActionResult(  # type: ignore[call-arg]
                _id=context.request_id,
                _action=name,
                _status=ActionStatus.FAILED,
                _started_at=started_at,  # type: ignore[name-defined]
                _completed_at=completed_at,  # type: ignore[name-defined]
                _data={},
                _error=str(e),
                _error_code="INTERNAL_ERROR",
                _duration_ms=duration_ms,  # type: ignore[name-defined]
                _context=context,
            )

    def _execute_with_middleware(
        self,
        name: str,
        params: Dict[str, Any],
        context: ActionContext,
        definition: ActionDefinition,
    ) -> ActionResult:
        """Execute action through middleware pipeline."""
        _started_at=datetime.now(timezone.utc)

        def final_handler(
            n: str, p: Dict[str, Any], ctx: ActionContext
        ) -> ActionResult:
            """Final handler that executes the actual action."""
            try:
                _data=definition.handler(p, ctx)
                _completed_at=datetime.now(timezone.utc)
                _duration_ms=int((completed_at - started_at).total_seconds() * 1000)  # type: ignore[name-defined]

                self._audit(n, ctx, True, duration_ms=duration_ms, params=p)  # type: ignore[name-defined]

                return ActionResult(  # type: ignore[call-arg]
                    _id=ctx.request_id,
                    _action=n,
                    _status=ActionStatus.COMPLETED,
                    _started_at=started_at,  # type: ignore[name-defined]
                    _completed_at=completed_at,  # type: ignore[name-defined]
                    _data=data if isinstance(data, dict) else {"result": data},  # type: ignore[name-defined]
                    _duration_ms=duration_ms,  # type: ignore[name-defined]
                    _context=ctx,
                )
            except Exception as e:
                _completed_at=datetime.now(timezone.utc)
                _duration_ms=int((completed_at - started_at).total_seconds() * 1000)  # type: ignore[name-defined]

                self._audit(
                    n, ctx, False, error=str(e), duration_ms=duration_ms, params=p  # type: ignore[name-defined]
                )

                return ActionResult(  # type: ignore[call-arg]
                    _id=ctx.request_id,
                    _action=n,
                    _status=ActionStatus.FAILED,
                    _started_at=started_at,  # type: ignore[name-defined]
                    _completed_at=completed_at,  # type: ignore[name-defined]
                    _data={},
                    _error=str(e),
                    _error_code="HANDLER_ERROR",
                    _duration_ms=duration_ms,  # type: ignore[name-defined]
                    _context=ctx,
                )

        # Build middleware chain
        handler=final_handler
        for middleware in reversed(self._middlewares):
            prev_handler=handler

            def handler(n, p, c, mw=middleware, ph=prevhandler) -> None:  # type: ignore[misc, name-defined]
                return mw(n, p, c, ph)

        return handler(name, params, context)

    def _cache_key(self, action: str, params: Dict[str, Any]) -> str:
        """Generate cache key from action and params."""
        params_hash=hashlib.sha256(
            json.dumps(params, sort_keys=True).encode()
        ).hexdigest()[
            :8
        ]
        return f"action:{action}:{params_hash}"

    def _audit(
        self,
        action: str,
        context: ActionContext,
        success: bool,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record audit entry."""
        params_hash=None
        if params:
            _params_hash=hashlib.sha256(
                json.dumps(params, sort_keys=True).encode()
            ).hexdigest()[:16]

        _entry=AuditEntry(  # type: ignore[call-arg]
            _timestamp=datetime.now(timezone.utc),
            _action=action,
            _user_id=context.user_id,
            _tenant_id=context.tenant_id,
            _source=context.source,
            _request_id=context.request_id,
            _success=success,
            _error=error,
            _duration_ms=duration_ms,
            _params_hash=params_hash,
        )

        with self._lock:
            self._audit_log.append(entry)
            # Trim audit log
            if len(self._audit_log) > self._max_audit_entries:
                self._audit_log=self._audit_log[-self._max_audit_entries :]

    def get_audit_log(
        self,
        action: Optional[str] = None,
        user_id: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: int=100,
    ) -> List[Dict[str, Any]]:
        """Get filtered audit log entries."""
        with self._lock:
            _entries=list(self._audit_log)

        if action:
            entries=[e for e in entries if e.action == action]  # type: ignore[has-type]
        if user_id:
            entries=[e for e in entries if e.user_id == user_id]
        if since:
            entries=[e for e in entries if e.timestamp >= since]

        return [e.to_dict() for e in entries[-limit:]]

    def list_actions(self) -> List[Dict[str, Any]]:
        """List all registered actions."""
        return [
            {
                "name": d.name,
                "description": d.description,
                "permission": d.required_permission.value,
                "is_async": d.is_async,
                "cacheable": d.cacheable,
            }
            for d in self._actions.values()
        ]

    def invalidate_cache(self, pattern: str) -> int:
        """Invalidate cache entries matching pattern."""
        return self._cache.invalidate_pattern(pattern)

    def subscribe_events(self, eventtype: str, handler: Callable[..., Any]) -> None:
        """Subscribe to backend events."""
        self._event_bus.subscribe(event_type, handler)  # type: ignore[name-defined]

    def publish_event(self, eventtype: str, data: Dict[str, Any]) -> None:
        """Publish custom event."""
        self._event_bus.publish(event_type, data)  # type: ignore[name-defined]

    def get_stats(self) -> Dict[str, Any]:
        """Get backend statistics."""
        with self._lock:
            _total_actions=len(self._audit_log)
            _successful=sum(1 for e in self._audit_log if e.success)
            failed=total_actions - successful  # type: ignore[name-defined]

        return {
            "registered_actions": len(self._actions),
            "total_executions": total_actions,  # type: ignore[name-defined]
            "successful": successful,  # type: ignore[name-defined]
            "failed": failed,
            "success_rate": (
                round(successful / total_actions * 100, 2) if total_actions > 0 else 0  # type: ignore[name-defined]
            ),
            "cache": self._cache.stats(),
        }


# Decorator for registering actions
def action(
    name: str,
    permission: Permission=Permission.EXECUTE,
    description: str="",
    cacheable: bool=False,
    cache_ttl: int=60,
):
    """Decorator to register a function as an action."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(params: Dict[str, Any], context: ActionContext) -> Any:
            return func(params, context)

        wrapper._action_config={  # type: ignore[attr-defined]
            "name": name,
            "permission": permission,
            "description": description,
            "cacheable": cacheable,
            "cache_ttl": cache_ttl,
        }
        return wrapper

    return decorator


# Factory for creating pre-configured backends
def create_backend(config: Optional[Dict[str, Any]] = None) -> UnifiedBackend:
    """Create a configured UnifiedBackend instance."""
    _backend=UnifiedBackend()

    # Register common actions
    backend.register_action(  # type: ignore[name-defined]
        "health_check",
        lambda p, c: {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        _permission=Permission.READ,
        _description="Check backend health",
        _cacheable=True,
        _cache_ttl=10,
    )

    backend.register_action(  # type: ignore[name-defined]
        "list_actions",
        lambda p, c: {"actions": backend.list_actions()},  # type: ignore[name-defined]
        _permission=Permission.READ,
        _description="List all registered actions",
    )

    backend.register_action(  # type: ignore[name-defined]
        "get_stats",
        lambda p, c: backend.get_stats(),  # type: ignore[name-defined]
        _permission=Permission.READ,
        _description="Get backend statistics",
    )

    return backend  # type: ignore[name-defined]


# CLI entry point
if _name__== "__main__":  # type: ignore[name-defined]
    import argparse

    _parser=argparse.ArgumentParser(description="DebVisor Unified Backend")
    parser.add_argument(  # type: ignore[name-defined]
        "action", choices=["demo", "list", "stats"], help="Action to perform"
    )
    _args=parser.parse_args()  # type: ignore[name-defined]

    logging.basicConfig(  # type: ignore[call-arg]
        _level=logging.INFO,
        _format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    _backend=create_backend()

    # Register demo actions
    backend.register_action(  # type: ignore[name-defined]
        "drain_node",
        lambda p, c: {"node": p.get("node"), "status": "drained"},
        _permission=Permission.ADMIN,
        _description="Drain a node for maintenance",
    )

    backend.register_action(  # type: ignore[name-defined]
        "list_vms",
        lambda p, c: {"vms": ["vm-001", "vm-002", "vm-003"]},
        _permission=Permission.READ,
        _description="List all VMs",
        _cacheable=True,
    )

    if args.action == "list":  # type: ignore[name-defined]
        print("Registered Actions:")
        for act in backend.list_actions():  # type: ignore[name-defined]
            print(
                f"  {act['name']:20} - {act['description']} (requires: {act['permission']})"
            )

    elif args.action == "stats":  # type: ignore[name-defined]
        print(json.dumps(backend.get_stats(), indent=2))  # type: ignore[name-defined]

    elif args.action == "demo":  # type: ignore[name-defined]
    # Create test context
        ctx=ActionContext(  # type: ignore[call-arg]
            _request_id=str(uuid4()), user_id="admin", user_role=Role.ADMIN, source="cli"
        )

        # Execute some actions
        print("\nExecuting drain_node...")
        _result=backend.execute("drain_node", {"node": "node-01"}, ctx)  # type: ignore[name-defined]
        print(f"  Result: {result.status.value} - {result.data}")  # type: ignore[name-defined]

        print("\nExecuting list_vms (first call - cache miss)...")
        _result=backend.execute("list_vms", {}, ctx)  # type: ignore[name-defined]
        print(f"  Result: {result.status.value} - {result.data}")  # type: ignore[name-defined]

        print("\nExecuting list_vms (second call - cache hit)...")
        _result=backend.execute("list_vms", {}, ctx)  # type: ignore[name-defined]
        print(f"  Result: {result.status.value} - {result.data}")  # type: ignore[name-defined]

        print("\nExecuting health_check...")
        _result=backend.execute("health_check", {}, ctx)  # type: ignore[name-defined]
        print(f"  Result: {result.status.value} - {result.data}")  # type: ignore[name-defined]

        print("\nAudit Log:")
        for entry in backend.get_audit_log():  # type: ignore[name-defined]
            print(
                f"  {entry['timestamp']}: {entry['action']} - {'?' if entry['success'] else '?'}"
            )
