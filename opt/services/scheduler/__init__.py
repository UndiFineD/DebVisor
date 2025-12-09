"""
DebVisor Advanced Scheduler Package

Comprehensive job scheduling system with cron-based scheduling, state management,
dependency resolution, and failure recovery.

Components:
- core: Core scheduler engine
- cli: Command-line interface
- api: REST API interface

Example Usage:

from opt.services.scheduler.core import get_scheduler

  # Get scheduler instance
scheduler = get_scheduler()

  # Register task handler
async def handle_vm_snapshot(config):
    vm_id = config["vm_id"]
      # Perform snapshot
    return True

scheduler.register_task_handler("vm_snapshot", handle_vm_snapshot)

  # Create job
job = scheduler.create_job(
    name="Daily VM Snapshot",
    cron_expr="0 2 * * *",  # 2 AM daily
    task_type="vm_snapshot",
    task_config={"vm_id": "vm-123"},
    owner="admin"
)

  # Execute job manually
result = await scheduler.execute_job(job.job_id, manual=True)

Author: DebVisor Development Team
Date: November 27, 2025
Version: 1.0.0
"""

from .core import (
    JobScheduler,
    ScheduledJob,
    JobStatus,
    JobPriority,
    DependencyType,
    CronExpression,
    JobDependency,
    JobExecutionResult,
    get_scheduler,
)

from .cli import SchedulerCLI, main as cli_main
from .api import SchedulerAPI, create_flask_app

__all__ = [
    "JobScheduler",
    "ScheduledJob",
    "JobStatus",
    "JobPriority",
    "DependencyType",
    "CronExpression",
    "JobDependency",
    "JobExecutionResult",
    "get_scheduler",
    "SchedulerCLI",
    "cli_main",
    "SchedulerAPI",
    "create_flask_app",
]

__version__ = "1.0.0"
__author__ = "DebVisor Development Team"
