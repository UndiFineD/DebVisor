"""
Advanced VM Scheduling System - REST API

Provides comprehensive REST API endpoints for managing scheduled jobs including
creation, execution, monitoring, and state management via HTTP.

Author: DebVisor Development Team
Date: November 27, 2025
Version: 1.0.0
"""

import json
from datetime import datetime, timezone
import logging
from typing import Any, Dict, Optional, Tuple

from .core import JobScheduler, JobPriority, CronExpression, get_scheduler


class SchedulerAPI:
    """REST API for job scheduler."""

    def __init__(self, scheduler: Optional[JobScheduler] = None, debug: bool = False):
        """Initialize the API.

        Args:
            scheduler: JobScheduler instance (uses global if None)
            debug: Enable debug mode
        """
        self.scheduler = scheduler or get_scheduler()
        self.debug = debug
        self.logger = logging.getLogger("DebVisor.SchedulerAPI")

    def _json_response(
        self, data: Any, status: int = 200, headers: Optional[Dict[str, str]] = None
    ) -> Tuple[str, int, Dict[str, str]]:
        """Create a JSON response.

        Args:
            data: Response data
            status: HTTP status code
            headers: Additional headers

        Returns:
            (body, status, headers) tuple
        """
        response_headers = {"Content-Type": "application/json"}
        if headers:
            response_headers.update(headers)

        body = json.dumps(
            {
                "status": "success" if 200 <= status < 300 else "error",
                "data": data,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

        return body, status, response_headers

    def _error_response(
        self, message: str, status: int = 400, details: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, int, Dict[str, str]]:
        """Create an error response.

        Args:
            message: Error message
            status: HTTP status code
            details: Additional error details

        Returns:
            (body, status, headers) tuple
        """
        error_data = {"error": message, "status_code": status}
        if details:
            error_data.update(details)

        return self._json_response(error_data, status)

    def _validate_json(self, body: str) -> Optional[Dict[str, Any]]:
        """Validate and parse JSON body.

        Args:
            body: Request body

        Returns:
            Parsed JSON or None if invalid
        """
        try:
            return json.loads(body)
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON: {e}")
            return None

    # ========================================================================
    # Job Management Endpoints
    # ========================================================================

    def create_job(self, body: str) -> Tuple[str, int, Dict[str, str]]:
        """Create a new job.

        POST /api/v1/jobs

        Request body:
        {
            "name": "VM Snapshot",
            "cron_expression": "0 * * * *",
            "task_type": "vm_snapshot",
            "task_config": {"vm_id": "vm-123"},
            "priority": "normal",
            "owner": "admin",
            "timeout_seconds": 3600
        }

        Args:
            body: Request body

        Returns:
            Response tuple
        """
        data = self._validate_json(body)
        if data is None:
            return self._error_response("Invalid JSON", 400)

        try:
            # Validate required fields
            required_fields = ["name", "cron_expression", "task_type", "task_config"]
            for field in required_fields:
                if field not in data:
                    return self._error_response(f"Missing field: {field}", 400)

            # Parse cron expression
            try:
                CronExpression.from_string(data["cron_expression"])
            except ValueError as e:
                return self._error_response(f"Invalid cron expression: {e}", 400)

            # Parse task config
            if isinstance(data["task_config"], str):
                task_config = json.loads(data["task_config"])
            else:
                task_config = data["task_config"]

            # Get optional fields
            priority_str = data.get("priority", "normal")
            try:
                priority = JobPriority[priority_str.upper()]
            except KeyError:
                return self._error_response(f"Invalid priority: {priority_str}", 400)

            # Create job
            job = self.scheduler.create_job(
                name=data["name"],
                cron_expr=data["cron_expression"],
                task_type=data["task_type"],
                task_config=task_config,
                priority=priority,
                owner=data.get("owner", "system"),
                description=data.get("description", ""),
                timezone=data.get("timezone", "UTC"),
                max_retries=data.get("max_retries", 3),
                timeout_seconds=data.get("timeout_seconds", 3600),
            )

            self.logger.info(f"Created job {job.job_id}")
            return self._json_response(job.to_dict(), 201)

        except Exception as e:
            self.logger.error(f"Error creating job: {e}")
            return self._error_response(f"Failed to create job: {e}", 500)

    def list_jobs(
        self, owner: Optional[str] = None, status: Optional[str] = None
    ) -> Tuple[str, int, Dict[str, str]]:
        """List jobs.

        GET /api/v1/jobs?owner=admin&status=running

        Args:
            owner: Filter by owner
            status: Filter by status

        Returns:
            Response tuple
        """
        try:
            jobs = self.scheduler.list_jobs(owner=owner)
            jobs_data = [j.to_dict() for j in jobs]
            return self._json_response({"jobs": jobs_data, "count": len(jobs_data)})
        except Exception as e:
            self.logger.error(f"Error listing jobs: {e}")
            return self._error_response(f"Failed to list jobs: {e}", 500)

    def get_job(self, job_id: str) -> Tuple[str, int, Dict[str, str]]:
        """Get job details.

        GET /api/v1/jobs/:job_id

        Args:
            job_id: Job ID

        Returns:
            Response tuple
        """
        try:
            job = self.scheduler.get_job(job_id)
            if not job:
                return self._error_response(f"Job {job_id} not found", 404)

            return self._json_response(job.to_dict())
        except Exception as e:
            self.logger.error(f"Error getting job {job_id}: {e}")
            return self._error_response(f"Failed to get job: {e}", 500)

    def update_job(self, job_id: str, body: str) -> Tuple[str, int, Dict[str, str]]:
        """Update a job.

        PUT /api/v1/jobs/:job_id

        Request body:
        {
            "name": "Updated Name",
            "enabled": false,
            "priority": "high"
        }

        Args:
            job_id: Job ID
            body: Request body

        Returns:
            Response tuple
        """
        data = self._validate_json(body)
        if data is None:
            return self._error_response("Invalid JSON", 400)

        try:
            job = self.scheduler.get_job(job_id)
            if not job:
                return self._error_response(f"Job {job_id} not found", 404)

            updates = {}

            if "name" in data:
                updates["name"] = data["name"]
            if "enabled" in data:
                updates["enabled"] = data["enabled"]
            if "priority" in data:
                try:
                    updates["priority"] = JobPriority[data["priority"].upper()]
                except KeyError:
                    return self._error_response(
                        f"Invalid priority: {data['priority']}", 400
                    )
            if "cron_expression" in data:
                try:
                    updates["cron_expression"] = CronExpression.from_string(
                        data["cron_expression"]
                    )
                except ValueError as e:
                    return self._error_response(f"Invalid cron expression: {e}", 400)

            updated = self.scheduler.update_job(job_id, **updates)
            self.logger.info(f"Updated job {job_id}")
            return self._json_response(updated.to_dict())  # type: ignore[union-attr]

        except Exception as e:
            self.logger.error(f"Error updating job {job_id}: {e}")
            return self._error_response(f"Failed to update job: {e}", 500)

    def delete_job(self, job_id: str) -> Tuple[str, int, Dict[str, str]]:
        """Delete a job.

        DELETE /api/v1/jobs/:job_id

        Args:
            job_id: Job ID

        Returns:
            Response tuple
        """
        try:
            job = self.scheduler.get_job(job_id)
            if not job:
                return self._error_response(f"Job {job_id} not found", 404)

            self.scheduler.delete_job(job_id)
            self.logger.info(f"Deleted job {job_id}")
            return self._json_response({"message": f"Job {job_id} deleted"})

        except Exception as e:
            self.logger.error(f"Error deleting job {job_id}: {e}")
            return self._error_response(f"Failed to delete job: {e}", 500)

    # ========================================================================
    # Job Execution Endpoints
    # ========================================================================

    def execute_job(self, job_id: str) -> Tuple[str, int, Dict[str, str]]:
        """Execute a job immediately.

        POST /api/v1/jobs/:job_id/run

        Args:
            job_id: Job ID

        Returns:
            Response tuple
        """
        try:
            job = self.scheduler.get_job(job_id)
            if not job:
                return self._error_response(f"Job {job_id} not found", 404)

            result = await_sync(self.scheduler.execute_job(job_id, manual=True))
            self.logger.info(f"Executed job {job_id}")
            return self._json_response(result.to_dict())

        except Exception as e:
            self.logger.error(f"Error executing job {job_id}: {e}")
            return self._error_response(f"Failed to execute job: {e}", 500)

    def get_execution_history(
        self, job_id: str, limit: int = 20, offset: int = 0
    ) -> Tuple[str, int, Dict[str, str]]:
        """Get job execution history.

        GET /api/v1/jobs/:job_id/history?limit=20&offset=0

        Args:
            job_id: Job ID
            limit: Number of results
            offset: Result offset

        Returns:
            Response tuple
        """
        try:
            job = self.scheduler.get_job(job_id)
            if not job:
                return self._error_response(f"Job {job_id} not found", 404)

            history = self.scheduler.get_execution_history(job_id, limit, offset)
            return self._json_response(
                {
                    "job_id": job_id,
                    "history": [h.to_dict() for h in history],
                    "count": len(history),
                }
            )

        except Exception as e:
            self.logger.error(f"Error getting history for {job_id}: {e}")
            return self._error_response(f"Failed to get history: {e}", 500)

    def get_job_stats(self, job_id: str) -> Tuple[str, int, Dict[str, str]]:
        """Get job statistics.

        GET /api/v1/jobs/:job_id/stats

        Args:
            job_id: Job ID

        Returns:
            Response tuple
        """
        try:
            job = self.scheduler.get_job(job_id)
            if not job:
                return self._error_response(f"Job {job_id} not found", 404)

            stats = self.scheduler.get_job_statistics(job_id)
            return self._json_response(stats)

        except Exception as e:
            self.logger.error(f"Error getting stats for {job_id}: {e}")
            return self._error_response(f"Failed to get statistics: {e}", 500)

    def retry_job_execution(
        self, job_id: str, execution_id: str
    ) -> Tuple[str, int, Dict[str, str]]:
        """Retry a job execution.

        POST /api/v1/jobs/:job_id/executions/:execution_id/retry

        Args:
            job_id: Job ID
            execution_id: Execution ID

        Returns:
            Response tuple
        """
        try:
            result = self.scheduler.retry_job(job_id, execution_id)
            self.logger.info(f"Retried job {job_id} execution {execution_id}")
            return self._json_response(result.to_dict())

        except ValueError as e:
            return self._error_response(str(e), 404)
        except Exception as e:
            self.logger.error(f"Error retrying job: {e}")
            return self._error_response(f"Failed to retry job: {e}", 500)

    # ========================================================================
    # Configuration Endpoints
    # ========================================================================

    def get_config(self) -> Tuple[str, int, Dict[str, str]]:
        """Get scheduler configuration.

        GET /api/v1/config

        Returns:
            Response tuple
        """
        try:
            config = {
                "scheduler_config_dir": getattr(
                    self.scheduler.repository, "config_dir", "unknown"
                ),
                "max_workers": self.scheduler.max_workers,
                "total_jobs": len(self.scheduler.jobs),
                "registered_task_types": list(self.scheduler.task_handlers.keys()),
                "active_executions": len(self.scheduler.execution_tasks),
            }
            return self._json_response(config)
        except Exception as e:
            self.logger.error(f"Error getting config: {e}")
            return self._error_response(f"Failed to get configuration: {e}", 500)

    def get_health(self) -> Tuple[str, int, Dict[str, str]]:
        """Get scheduler health status.

        GET /api/v1/health

        Returns:
            Response tuple
        """
        try:
            health = {
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "jobs_count": len(self.scheduler.jobs),
                "active_executions": len(self.scheduler.execution_tasks),
                "config_dir": getattr(
                    self.scheduler.repository, "config_dir", "unknown"
                ),
                "version": "1.0.0",
            }
            return self._json_response(health)
        except Exception as e:
            self.logger.error(f"Error getting health: {e}")
            return self._error_response("Unhealthy", 503)


def await_sync(coro: Any) -> Any:
    """Helper to run async code synchronously (for testing/integration).

    Args:
        coro: Coroutine to run

    Returns:
        Result of coroutine
    """
    import asyncio

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(coro)


# Flask integration (optional)


def create_flask_app(scheduler: Optional[JobScheduler] = None) -> Any:
    """Create Flask application for scheduler API.

    Args:
        scheduler: JobScheduler instance

    Returns:
        Flask app instance
    """
    try:
        from flask import Flask, request
        from opt.web.panel.graceful_shutdown import init_graceful_shutdown
    except ImportError:
        raise ImportError(
            "Flask is required for REST API. Install with: pip install flask"
        )

    app = Flask(__name__)

    # Load and validate configuration (INFRA-003)
    from opt.core.config import Settings
    settings = Settings.load_validated_config()
    app.config["SETTINGS"] = settings

    # Initialize graceful shutdown
    shutdown_manager = init_graceful_shutdown(app)

    # Register standard health checks
    def check_scheduler() -> bool:
        return scheduler is not None

    shutdown_manager.register_health_check("scheduler", check_scheduler)

    api = SchedulerAPI(scheduler)

    @app.route("/api/v1/jobs", methods=["POST"])
    def create_job_route() -> Tuple[str, int, Dict[str, str]]:
        body, status, headers = api.create_job(request.get_data(as_text=True))
        return body, status, headers

    @app.route("/api/v1/jobs", methods=["GET"])
    def list_jobs_route() -> Tuple[str, int, Dict[str, str]]:
        owner = request.args.get("owner")
        status = request.args.get("status")
        body, status_code, headers = api.list_jobs(owner=owner, status=status)
        return body, status_code, headers

    @app.route("/api/v1/jobs/<job_id>", methods=["GET"])
    def get_job_route(job_id: str) -> Tuple[str, int, Dict[str, str]]:
        body, status, headers = api.get_job(job_id)
        return body, status, headers

    @app.route("/api/v1/jobs/<job_id>", methods=["PUT"])
    def update_job_route(job_id: str) -> Tuple[str, int, Dict[str, str]]:
        body, status, headers = api.update_job(job_id, request.get_data(as_text=True))
        return body, status, headers

    @app.route("/api/v1/jobs/<job_id>", methods=["DELETE"])
    def delete_job_route(job_id: str) -> Tuple[str, int, Dict[str, str]]:
        body, status, headers = api.delete_job(job_id)
        return body, status, headers

    @app.route("/api/v1/jobs/<job_id>/run", methods=["POST"])
    def execute_job_route(job_id: str) -> Tuple[str, int, Dict[str, str]]:
        body, status, headers = api.execute_job(job_id)
        return body, status, headers

    @app.route("/api/v1/jobs/<job_id>/history", methods=["GET"])
    def job_history_route(job_id: str) -> Tuple[str, int, Dict[str, str]]:
        limit = request.args.get("limit", 20, type=int)
        offset = request.args.get("offset", 0, type=int)
        body, status, headers = api.get_execution_history(job_id, limit, offset)
        return body, status, headers

    @app.route("/api/v1/jobs/<job_id>/stats", methods=["GET"])
    def job_stats_route(job_id: str) -> Tuple[str, int, Dict[str, str]]:
        body, status, headers = api.get_job_stats(job_id)
        return body, status, headers

    @app.route("/api/v1/config", methods=["GET"])
    def config_route() -> Tuple[str, int, Dict[str, str]]:
        body, status, headers = api.get_config()
        return body, status, headers

    @app.route("/api/v1/health", methods=["GET"])
    def health_route() -> Tuple[str, int, Dict[str, str]]:
        body, status, headers = api.get_health()
        return body, status, headers

    return app