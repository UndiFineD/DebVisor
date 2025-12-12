# !/usr/bin/env python3
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


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


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
_scheduler=get_scheduler()

# Register task handler


async def handle_vm_snapshot(config):
    _vm_id = config["vm_id"]
    # Perform snapshot
    return True

scheduler.register_task_handler("vm_snapshot", handle_vm_snapshot)

# Create job
job = scheduler.create_job(
    _name = "Daily VM Snapshot",
    _cron_expr = "0 2 * * *",    # 2 AM daily
    _task_type = "vm_snapshot",
    _task_config = {"vm_id": "vm-123"},
    _owner = "admin"
)

# Execute job manually
_result=await scheduler.execute_job(job.job_id, manual=True)

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
