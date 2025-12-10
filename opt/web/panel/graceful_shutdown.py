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

"""
Graceful Shutdown Handler for DebVisor Web Panel.

Implements clean shutdown with connection draining, in-flight request
completion, and health check status updates.

Author: DebVisor Team
Date: November 28, 2025
"""

from datetime import datetime, timezone

import atexit
import logging
import signal
import sys
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Iterator, List, Optional

logger = logging.getLogger(__name__)


# =============================================================================
# Enums & Types
# =============================================================================


class ShutdownPhase(Enum):
    """Phases of graceful shutdown."""

    RUNNING = "running"
    DRAINING = "draining"    # Stop accepting new requests
    COMPLETING = "completing"    # Wait for in-flight requests
    CLEANUP = "cleanup"    # Run cleanup hooks
    TERMINATED = "terminated"    # Fully stopped


class SignalType(Enum):
    """Supported shutdown signals."""

    SIGTERM = signal.SIGTERM
    SIGINT = signal.SIGINT
    SIGHUP = getattr(signal, "SIGHUP", None)    # Not available on Windows


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class ShutdownConfig:
    """Configuration for graceful shutdown behavior."""

    # Draining phase
    drain_timeout_seconds: float = 30.0
    health_check_fail_delay_seconds: float = 5.0

    # Completing phase
    request_timeout_seconds: float = 60.0
    force_after_seconds: float = 90.0

    # Cleanup phase
    cleanup_timeout_seconds: float = 10.0

    # Behavior
    exit_code_normal: int = 0
    exit_code_forced: int = 1
    exit_code_error: int = 2


@dataclass
class RequestContext:
    """Context for tracking in-flight requests."""

    request_id: str
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    method: str = ""
    path: str = ""
    client_ip: str = ""

    @property
    def duration_seconds(self) -> float:
        """Get duration of request in seconds."""
        delta = datetime.now(timezone.utc) - self.started_at
        return delta.total_seconds()


@dataclass
class ShutdownMetrics:
    """Metrics collected during shutdown."""

    shutdown_started_at: Optional[datetime] = None
    shutdown_completed_at: Optional[datetime] = None
    requests_drained: int = 0
    requests_completed: int = 0
    requests_abandoned: int = 0
    hooks_executed: int = 0
    hooks_failed: int = 0

    @property
    def total_shutdown_seconds(self) -> float:
        """Get total shutdown duration."""
        if not self.shutdown_started_at:
            return 0.0
        end = self.shutdown_completed_at or datetime.now(timezone.utc)
        return (end - self.shutdown_started_at).total_seconds()


# =============================================================================
# Shutdown Manager
# =============================================================================


class GracefulShutdownManager:
    """
    Manages graceful shutdown of the application.

    Features:
    - Signal handling (SIGTERM, SIGINT)
    - Connection draining
    - In-flight request tracking
    - Cleanup hook registration
    - Timeout enforcement
    """

    def __init__(self, config: Optional[ShutdownConfig] = None):
        """
        Initialize shutdown manager.

        Args:
            config: Shutdown configuration options
        """
        self.config = config or ShutdownConfig()
        self._phase = ShutdownPhase.RUNNING
        self._phase_lock = threading.Lock()

        # Request tracking
        self._active_requests: Dict[str, RequestContext] = {}
        self._requests_lock = threading.Lock()

        # Cleanup hooks
        self._cleanup_hooks: List[tuple[str, Callable[[], None]]] = []
        self._hooks_lock = threading.Lock()

        # Health checks
        self._health_checks: Dict[str, Callable[[], bool]] = {}
        self._health_lock = threading.Lock()

        # Metrics
        self.metrics = ShutdownMetrics()

        # Shutdown event
        self._shutdown_event = threading.Event()

        # Original signal handlers
        self._original_handlers: Dict[int, Any] = {}

        logger.info("GracefulShutdownManager initialized")

    @property
    def phase(self) -> ShutdownPhase:
        """Get current shutdown phase."""
        with self._phase_lock:
            return self._phase

    @property
    def is_shutting_down(self) -> bool:
        """Check if shutdown is in progress."""
        return self._phase != ShutdownPhase.RUNNING

    @property
    def accepting_requests(self) -> bool:
        """Check if new requests should be accepted."""
        return self._phase == ShutdownPhase.RUNNING

    @property
    def active_request_count(self) -> int:
        """Get count of active requests."""
        with self._requests_lock:
            return len(self._active_requests)

    # =========================================================================
    # Signal Handling
    # =========================================================================

    def install_signal_handlers(self) -> None:
        """Install signal handlers for graceful shutdown."""
        signals = [SignalType.SIGTERM, SignalType.SIGINT]

        for sig_type in signals:
            if sig_type.value is not None:
                try:
                    original = signal.signal(
                        sig_type.value, self._create_signal_handler(sig_type)
                    )
                    self._original_handlers[sig_type.value] = original
                    logger.debug(f"Installed handler for {sig_type.name}")
                except (ValueError, OSError) as e:
                    logger.warning(
                        f"Could not install handler for {sig_type.name}: {e}"
                    )

        # Also register atexit handler
        atexit.register(self._atexit_handler)

        logger.info("Signal handlers installed")

    def _create_signal_handler(
        self, sig_type: SignalType
    ) -> Callable[[int, Any], None]:
        """Create a signal handler function."""

        def handler(signum: int, frame: Any) -> None:
            logger.info(f"Received signal {sig_type.name} ({signum})")
            self.initiate_shutdown(f"Signal {sig_type.name}")

        return handler

    def _atexit_handler(self) -> None:
        """Handler called on normal exit."""
        if self._phase == ShutdownPhase.RUNNING:
            logger.info("atexit handler triggered")
            self.initiate_shutdown("atexit")

    def restore_signal_handlers(self) -> None:
        """Restore original signal handlers."""
        for signum, handler in self._original_handlers.items():
            try:
                signal.signal(signum, handler)
            except (ValueError, OSError):
                pass
        self._original_handlers.clear()

    # =========================================================================
    # Request Tracking
    # =========================================================================

    def track_request(self, context: RequestContext) -> None:
        """
        Start tracking an in-flight request.

        Args:
            context: Request context to track
        """
        with self._requests_lock:
            self._active_requests[context.request_id] = context
            logger.debug(f"Tracking request {context.request_id}")

    def complete_request(self, request_id: str) -> None:
        """
        Mark a request as complete.

        Args:
            request_id: ID of completed request
        """
        with self._requests_lock:
            if request_id in self._active_requests:
                del self._active_requests[request_id]
                self.metrics.requests_completed += 1
                logger.debug(f"Completed request {request_id}")

    @contextmanager
    def request_scope(self, request_id: str, **kwargs: Any) -> Iterator[RequestContext]:
        """
        Context manager for request lifecycle.

        Args:
            request_id: Unique request identifier
            **kwargs: Additional context (method, path, client_ip)

        Yields:
            RequestContext for the request
        """
        context = RequestContext(request_id=request_id, **kwargs)
        self.track_request(context)
        try:
            yield context
        finally:
            self.complete_request(request_id)

    def get_active_requests(self) -> List[RequestContext]:
        """Get list of active requests."""
        with self._requests_lock:
            return list(self._active_requests.values())

    # =========================================================================
    # Cleanup Hooks
    # =========================================================================

    def register_cleanup_hook(
        self, name: str, hook: Callable[[], None], priority: int = 50
    ) -> None:
        """
        Register a cleanup hook to run during shutdown.

        Args:
            name: Name of the hook for logging
            hook: Callable to execute
            priority: Lower runs first (0-100)
        """
        with self._hooks_lock:
            self._cleanup_hooks.append((name, hook))
            # Sort by priority (stored separately would be better,
            # but keeping simple for now)
            logger.debug(f"Registered cleanup hook: {name}")

    def _run_cleanup_hooks(self) -> None:
        """Run all registered cleanup hooks."""
        with self._hooks_lock:
            hooks = list(self._cleanup_hooks)

        for name, hook in hooks:
            try:
                logger.info(f"Running cleanup hook: {name}")
                hook()
                self.metrics.hooks_executed += 1
            except Exception as e:
                logger.error(f"Cleanup hook '{name}' failed: {e}")
                self.metrics.hooks_failed += 1

    # =========================================================================
    # Shutdown Process
    # =========================================================================

    def initiate_shutdown(self, reason: str = "Unknown") -> None:
        """
        Initiate graceful shutdown.

        Args:
            reason: Reason for shutdown (for logging)
        """
        with self._phase_lock:
            if self._phase != ShutdownPhase.RUNNING:
                logger.warning("Shutdown already in progress")
                return

            self._phase = ShutdownPhase.DRAINING
            self.metrics.shutdown_started_at = datetime.now(timezone.utc)

        logger.info(f"Initiating graceful shutdown. Reason: {reason}")

        # Run shutdown in background thread to not block signal handler
        shutdown_thread = threading.Thread(
            target=self._run_shutdown_sequence, name="shutdown-sequence", daemon=False
        )
        shutdown_thread.start()

        # Signal waiting threads
        self._shutdown_event.set()

    def _run_shutdown_sequence(self) -> None:
        """Execute the shutdown sequence."""
        try:
            # Phase 1: Draining
            self._phase_draining()

            # Phase 2: Completing
            self._phase_completing()

            # Phase 3: Cleanup
            self._phase_cleanup()

            # Phase 4: Terminated
            self._phase_terminated()

        except Exception as e:
            logger.error(f"Shutdown sequence error: {e}")
            self.metrics.shutdown_completed_at = datetime.now(timezone.utc)
            sys.exit(self.config.exit_code_error)

    def _phase_draining(self) -> None:
        """
        Draining phase: Stop accepting new requests.

        Updates health check status and waits for load balancers
        to stop sending traffic.
        """
        logger.info("PHASE: Draining - Stopping new requests")

        with self._phase_lock:
            self._phase = ShutdownPhase.DRAINING

        # Wait for health checks to fail and LB to drain
        delay = self.config.health_check_fail_delay_seconds
        logger.info(f"Waiting {delay}s for load balancer drain...")
        time.sleep(delay)

        self.metrics.requests_drained = self.active_request_count
        logger.info(f"Drain complete. Active requests: {self.active_request_count}")

    def _phase_completing(self) -> None:
        """
        Completing phase: Wait for in-flight requests.

        Waits for active requests to complete with timeout.
        """
        logger.info("PHASE: Completing - Waiting for in-flight requests")

        with self._phase_lock:
            self._phase = ShutdownPhase.COMPLETING

        timeout = self.config.request_timeout_seconds
        start_time = time.time()
        poll_interval = 0.5

        while True:
            active = self.active_request_count
            elapsed = time.time() - start_time

            if active == 0:
                logger.info("All requests completed")
                break

            if elapsed >= timeout:
                logger.warning(
                    f"Request timeout after {timeout}s. "
                    f"Abandoning {active} requests"
                )
                self.metrics.requests_abandoned = active
                break

            # Log progress periodically
            if int(elapsed) % 5 == 0 and int(elapsed) > 0:
                remaining = timeout - elapsed
                requests = self.get_active_requests()
                logger.info(
                    f"Waiting for {active} requests. " f"Timeout in {remaining:.1f}s"
                )
                for req in requests[:5]:    # Log first 5
                    logger.debug(
                        f"  - {req.request_id}: {req.method} {req.path} "
                        f"({req.duration_seconds:.1f}s)"
                    )

            time.sleep(poll_interval)

    def _phase_cleanup(self) -> None:
        """
        Cleanup phase: Run registered cleanup hooks.

        Executes cleanup functions with timeout.
        """
        logger.info("PHASE: Cleanup - Running cleanup hooks")

        with self._phase_lock:
            self._phase = ShutdownPhase.CLEANUP

        self._run_cleanup_hooks()

        logger.info(
            f"Cleanup complete. Hooks: {self.metrics.hooks_executed} executed, "
            f"{self.metrics.hooks_failed} failed"
        )

    def _phase_terminated(self) -> None:
        """
        Terminated phase: Final shutdown.
        """
        logger.info("PHASE: Terminated - Shutdown complete")

        with self._phase_lock:
            self._phase = ShutdownPhase.TERMINATED

        self.metrics.shutdown_completed_at = datetime.now(timezone.utc)

        total_time = self.metrics.total_shutdown_seconds
        logger.info(
            f"Graceful shutdown completed in {total_time:.2f}s. "
            f"Completed: {self.metrics.requests_completed}, "
            f"Abandoned: {self.metrics.requests_abandoned}"
        )

        # Restore signal handlers
        self.restore_signal_handlers()

    def wait_for_shutdown(self, timeout: Optional[float] = None) -> bool:
        """
        Wait for shutdown to complete.

        Args:
            timeout: Maximum time to wait

        Returns:
            True if shutdown completed, False on timeout
        """
        return self._shutdown_event.wait(timeout)

    # =========================================================================
    # Health Check Integration
    # =========================================================================

    def register_health_check(self, name: str, check_func: Callable[[], bool]) -> None:
        """
        Register a dependency health check.

        Args:
            name: Name of the dependency (e.g., 'database', 'redis')
            check_func: Function returning True if healthy, False otherwise
        """
        with self._health_lock:
            self._health_checks[name] = check_func
            logger.debug(f"Registered health check: {name}")

    def get_health_status(self) -> Dict[str, Any]:
        """
        Get health status for health check endpoints.

        Returns unhealthy when shutting down to trigger LB drain.
        """
        is_healthy = self._phase == ShutdownPhase.RUNNING

        dependencies = {}
        # Check dependencies even if shutting down, for visibility
        with self._health_lock:
            for name, check in self._health_checks.items():
                try:
                    status = check()
                    dependencies[name] = "healthy" if status else "unhealthy"
                    if not status and self._phase == ShutdownPhase.RUNNING:
                        is_healthy = False
                except Exception as e:
                    logger.error(f"Health check '{name}' failed: {e}")
                    dependencies[name] = f"error: {str(e)}"
                    if self._phase == ShutdownPhase.RUNNING:
                        is_healthy = False

        return {
            "healthy": is_healthy,
            "phase": self._phase.value,
            "active_requests": self.active_request_count,
            "accepting_requests": self.accepting_requests,
            "dependencies": dependencies,
            "shutdown_started": (
                self.metrics.shutdown_started_at.isoformat()
                if self.metrics.shutdown_started_at
                else None
            ),
        }


# =============================================================================
# Flask Integration
# =============================================================================


class FlaskShutdownMiddleware:
    """
    Flask WSGI middleware for graceful shutdown.

    Integrates GracefulShutdownManager with Flask applications.
    """

    def __init__(self, app: Any, shutdown_manager: GracefulShutdownManager):
        """
        Initialize middleware.

        Args:
            app: Flask/WSGI application
            shutdown_manager: Shutdown manager instance
        """
        self.app = app
        self.shutdown_manager = shutdown_manager

    def __call__(self, environ: Dict[str, Any], start_response: Callable[..., Any]) -> Any:
        """WSGI application interface."""
        import uuid

        # Check if accepting requests
        if not self.shutdown_manager.accepting_requests:
            # Return 503 Service Unavailable
            status = "503 Service Unavailable"
            headers = [
                ("Content-Type", "application/json"),
                ("Retry-After", "30"),
                ("Connection", "close"),
            ]
            start_response(status, headers)
            return [b'{"error": "Service is shutting down"}']

        # Track request
        request_id = environ.get("HTTP_X_REQUEST_ID", str(uuid.uuid4()))

        with self.shutdown_manager.request_scope(
            request_id=request_id,
            method=environ.get("REQUEST_METHOD", "UNKNOWN"),
            path=environ.get("PATH_INFO", "/"),
            client_ip=environ.get("REMOTE_ADDR", "unknown"),
        ):
            return self.app(environ, start_response)


def create_shutdown_blueprint(shutdown_manager: GracefulShutdownManager) -> Any:
    """
    Create Flask blueprint with shutdown-related endpoints.

    Args:
        shutdown_manager: Shutdown manager instance

    Returns:
        Flask Blueprint
    """
    from flask import Blueprint, jsonify

    bp = Blueprint("shutdown", __name__)

    @bp.route("/health/live")
    def liveness() -> Any:
        """Liveness probe - always returns 200 unless crashed."""
        return jsonify({"status": "alive"})

    @bp.route("/health/ready")
    def readiness() -> Any:
        """Readiness probe - returns 503 during shutdown."""
        status = shutdown_manager.get_health_status()
        if status["healthy"]:
            return jsonify(status), 200
        return jsonify(status), 503

    @bp.route("/admin/shutdown", methods=["POST"])
    def admin_shutdown() -> Any:
        """Administrative shutdown endpoint (should be protected)."""
        shutdown_manager.initiate_shutdown("Admin request")
        return jsonify(
            {"message": "Shutdown initiated", "phase": shutdown_manager.phase.value}
        )

    return bp


# =============================================================================
# Global Instance
# =============================================================================

_shutdown_manager: Optional[GracefulShutdownManager] = None


def get_shutdown_manager() -> GracefulShutdownManager:
    """Get or create global shutdown manager."""
    global _shutdown_manager
    if _shutdown_manager is None:
        _shutdown_manager = GracefulShutdownManager()
    return _shutdown_manager


def init_graceful_shutdown(
    app: Optional[Any] = None, config: Optional[ShutdownConfig] = None
) -> GracefulShutdownManager:
    """
    Initialize graceful shutdown for an application.

    Args:
        app: Flask application (optional)
        config: Shutdown configuration

    Returns:
        Configured shutdown manager
    """
    global _shutdown_manager

    _shutdown_manager = GracefulShutdownManager(config)
    _shutdown_manager.install_signal_handlers()

    if app is not None:
        # Wrap app with middleware
        app.wsgi_app = FlaskShutdownMiddleware(app.wsgi_app, _shutdown_manager)

        # Register blueprint
        bp = create_shutdown_blueprint(_shutdown_manager)
        app.register_blueprint(bp)

    return _shutdown_manager


# =============================================================================
# Example Cleanup Hooks
# =============================================================================


def create_database_cleanup_hook(db_session: Any) -> Callable[[], None]:
    """Create a cleanup hook for database connections."""

    def cleanup() -> None:
        logger.info("Closing database connections...")
        try:
            db_session.close()
            db_session.remove()
        except Exception as e:
            logger.error(f"Database cleanup error: {e}")

    return cleanup


def create_cache_cleanup_hook(cache_client: Any) -> Callable[[], None]:
    """Create a cleanup hook for cache connections."""

    def cleanup() -> None:
        logger.info("Closing cache connections...")
        try:
            cache_client.close()
        except Exception as e:
            logger.error(f"Cache cleanup error: {e}")

    return cleanup


def create_message_queue_cleanup_hook(mq_client: Any) -> Callable[[], None]:
    """Create a cleanup hook for message queue connections."""

    def cleanup() -> None:
        logger.info("Closing message queue connections...")
        try:
            mq_client.close()
        except Exception as e:
            logger.error(f"Message queue cleanup error: {e}")

    return cleanup


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # Demo

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    manager = GracefulShutdownManager()
    manager.install_signal_handlers()

    # Register some test hooks
    manager.register_cleanup_hook("test-hook-1", lambda: print("Hook 1 executed"))
    manager.register_cleanup_hook("test-hook-2", lambda: print("Hook 2 executed"))

    print("Graceful shutdown manager ready. Press Ctrl+C to test shutdown.")

    try:
        while not manager.is_shutting_down:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    # Wait for shutdown to complete
    manager.wait_for_shutdown(timeout=30.0)
    print("Done!")
