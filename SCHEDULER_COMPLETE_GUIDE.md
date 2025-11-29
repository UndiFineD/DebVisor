# Advanced VM Scheduling System - Complete Guide

**Version:** 1.0.0
**Date:** November 27, 2025
**Status:** Production-Ready
**Phase:** Phase 7 - Feature 2

---

## Table of Contents

1. [Overview](#overview)
1. [Features](#features)
1. [Architecture](#architecture)
1. [Installation](#installation)
1. [Quick Start](#quick-start)
1. [CLI Usage](#cli-usage)
1. [REST API](#rest-api)
1. [Python API](#python-api)
1. [Configuration](#configuration)
1. [Advanced Usage](#advanced-usage)
1. [Troubleshooting](#troubleshooting)

---

## Overview

The Advanced VM Scheduling System is a comprehensive job scheduling solution for DebVisor that enables:

- **Cron-based scheduling** with standard cron syntax (minute, hour, day, month, weekday)
- **State management** with persistent storage of job definitions and execution history
- **Dependency resolution** allowing jobs to depend on other jobs' completion
- **Failure recovery** with automatic retry mechanisms and timeout handling
- **Multi-interface access** via CLI, REST API, and Python API
- **Event triggers** and notifications on job state changes
- **Audit logging** for compliance and troubleshooting
- **Performance monitoring** with execution statistics and trend analysis

### Key Use Cases

1. **Automated Backups** - Schedule periodic VM snapshots and backups
1. **Maintenance Tasks** - DNS updates, cloud-init generation, log rotation
1. **Compliance Operations** - Policy enforcement, scanning, reporting
1. **Resource Optimization** - Cost analysis, scaling recommendations
1. **Multi-step Workflows** - Complex operations with job dependencies

---

## Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Cron Scheduling** | Full cron expression support (minute, hour, day, month, weekday) |
| **Job Dependencies** | Jobs can require/conflict with other jobs |
| **State Persistence** | All job definitions and history stored to disk |
| **Failure Recovery** | Automatic retry with configurable backoff |
| **Timeout Handling** | Configurable job timeouts with graceful termination |
| **Priority Levels** | Critical, High, Normal, Low priority execution |
| **Execution History** | Full audit trail of all executions with timing |
| **Statistics** | Success rates, average duration, trend analysis |

### Interfaces

| Interface | Access | Use Case |
|-----------|--------|----------|
| **CLI** | Command-line | Ops engineers, scripting, automation |
| **REST API** | HTTP endpoints | Applications, integrations, dashboards |
| **Python API** | Direct import | Internal services, custom tools |

---

## Architecture

### Component Structure

```python
opt/services/scheduler/
+-- __init__.py              # Package initialization
+-- core.py                  # Core scheduler engine (500+ lines)
+-- cli.py                   # Command-line interface (400+ lines)
+-- api.py                   # REST API endpoints (400+ lines)
+-- tests.py                 # Test suite (300+ lines)
```python

### Data Models

**ScheduledJob**
```python
- job_id: str
- name: str
- cron_expression: CronExpression
- task_type: str
- task_config: Dict
- priority: JobPriority
- enabled: bool
- owner: str
- dependencies: List[JobDependency]
- execution_count: int
- failure_count: int
- last_execution: Optional[datetime]
- next_execution: Optional[datetime]
```python

**JobExecutionResult**
```python
- job_id: str
- execution_id: str
- status: JobStatus (pending, running, completed, failed, skipped)
- start_time: datetime
- end_time: Optional[datetime]
- exit_code: int
- stdout: str
- stderr: str
- duration_seconds: float
```python

### Storage

Jobs and execution history are stored as JSON files:

```python
/etc/debvisor/scheduler/
+-- <job_id>.json           # Job definition
+-- scheduler.log           # Execution log
```python

---

## Installation

### Requirements

- Python 3.8+
- asyncio (standard library)
- DebVisor core infrastructure

### Setup

1. **Copy scheduler files**
   ```bash
   mkdir -p /etc/debvisor/scheduler
   mkdir -p /opt/services/scheduler
   cp opt/services/scheduler/*.py /opt/services/scheduler/
```python

1. **Install CLI entry point** (optional)
   ```bash
   ln -s /opt/services/scheduler/cli.py /usr/local/bin/debvisor-schedule
```python

1. **Install as Python package** (optional)
   ```bash
   pip install -e /opt/services/scheduler
```python

---

## Quick Start

### 1. Create Your First Job

**Via CLI:**
```bash
schedule job create \
  --name="Daily Backup" \
  --cron="0 2 * * *" \
  --task-type="vm_snapshot" \
  --task-config='{"vm_id": "vm-123", "retention_days": 7}' \
  --owner="admin"
```python

**Via API:**
```bash
curl -X POST http://localhost:5000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daily Backup",
    "cron_expression": "0 2 * * *",
    "task_type": "vm_snapshot",
    "task_config": {"vm_id": "vm-123", "retention_days": 7},
    "owner": "admin"
  }'
```python

**Via Python:**
```python
from opt.services.scheduler.core import get_scheduler

scheduler = get_scheduler()
job = scheduler.create_job(
    name="Daily Backup",
    cron_expr="0 2 * * *",
    task_type="vm_snapshot",
    task_config={"vm_id": "vm-123", "retention_days": 7},
    owner="admin"
)
print(f"Created job: {job.job_id}")
```python

### 2. List Your Jobs

**Via CLI:**
```bash
schedule job list
schedule job list --owner=admin --format=json
```python

**Via API:**
```bash
curl http://localhost:5000/api/v1/jobs?owner=admin
```python

**Via Python:**
```python
jobs = scheduler.list_jobs(owner="admin")
for job in jobs:
    print(f"{job.job_id}: {job.name} ({job.cron_expression.to_string()})")
```python

### 3. Execute a Job Manually

**Via CLI:**
```bash
schedule job run f8a2d3c4
```python

**Via API:**
```bash
curl -X POST http://localhost:5000/api/v1/jobs/f8a2d3c4/run
```python

**Via Python:**
```python
result = await scheduler.execute_job("f8a2d3c4", manual=True)
print(f"Status: {result.status.value}")
print(f"Duration: {result.duration_seconds}s")
```python

### 4. View Job History

**Via CLI:**
```bash
schedule job history f8a2d3c4 --limit=20
```python

**Via API:**
```bash
curl http://localhost:5000/api/v1/jobs/f8a2d3c4/history?limit=20
```python

**Via Python:**
```python
history = scheduler.get_execution_history("f8a2d3c4", limit=20)
for execution in history:
    print(f"{execution.execution_id}: {execution.status.value} ({execution.duration_seconds}s)")
```python

---

## CLI Usage

### Job Management

#### Create a Job

```bash
schedule job create \
  --name="Snapshot Job" \
  --cron="0 * * * *" \
  --task-type=vm_snapshot \
  --task-config='{"vm_id": "vm-456"}' \
  --priority=high \
  --owner=admin \
  --timeout=1800 \
  --tag=environment production \
  --tag=team=infrastructure
```python

#### List Jobs

```bash

# List all jobs
schedule job list

# List jobs in JSON format
schedule job list --format=json

# Filter by owner
schedule job list --owner=admin

# Filter by status
schedule job list --status=running
```python

#### Show Job Details

```bash

# Text format
schedule job show f8a2d3c4

# JSON format
schedule job show f8a2d3c4 --format=json
```python

#### Update a Job

```bash
schedule job update f8a2d3c4 \
  --name="Updated Name" \
  --enabled=false \
  --priority=critical
```python

#### Delete a Job

```bash

# With confirmation
schedule job delete f8a2d3c4

# Force delete (skip confirmation)
schedule job delete f8a2d3c4 --force
```python

#### Execute Job Manually

```bash

# Execute immediately
schedule job run f8a2d3c4

# Dry-run mode (show what would happen)
schedule job run f8a2d3c4 --dry-run
```python

#### View Job History

```bash

# Default: 20 executions
schedule job history f8a2d3c4

# Custom limit
schedule job history f8a2d3c4 --limit=50

# JSON format [2]
schedule job history f8a2d3c4 --limit=20 --format=json
```python

#### Get Job Statistics

```bash

# Text format [2]
schedule job stats f8a2d3c4

# JSON format [3]
schedule job stats f8a2d3c4 --format=json
```python

### Configuration Management

#### List Configuration

```bash
schedule config list
schedule config list --format=json
```python

#### Backup Configuration

```bash
schedule config backup --output=/backups/scheduler_backup.json
```python

#### Restore Configuration

```bash
schedule config restore --input=/backups/scheduler_backup.json
schedule config restore --input=/backups/scheduler_backup.json --force
```python

---

## REST API

### Authentication

All API endpoints support authentication via:

- Bearer tokens in `Authorization` header
- API keys in `X-API-Key` header
- OAuth2 tokens (if configured)

### Base URL

```python
http://localhost:5000/api/v1
```python

### Endpoints

#### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/jobs` | Create a new job |
| GET | `/jobs` | List jobs |
| GET | `/jobs/:job_id` | Get job details |
| PUT | `/jobs/:job_id` | Update a job |
| DELETE | `/jobs/:job_id` | Delete a job |
| POST | `/jobs/:job_id/run` | Execute job immediately |
| GET | `/jobs/:job_id/history` | Get execution history |
| GET | `/jobs/:job_id/stats` | Get job statistics |
| POST | `/jobs/:job_id/executions/:execution_id/retry` | Retry execution |

#### Configuration

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/config` | Get scheduler configuration |
| GET | `/health` | Health check |

### Request/Response Examples

#### Create Job

```bash
POST /api/v1/jobs
Content-Type: application/json

{
  "name": "VM Snapshot",
  "cron_expression": "0 2 * * *",
  "task_type": "vm_snapshot",
  "task_config": {
    "vm_id": "vm-123",
    "retention_days": 7
  },
  "priority": "normal",
  "owner": "admin",
  "timeout_seconds": 3600
}

Response (201 Created):
{
  "status": "success",
  "data": {
    "job_id": "f8a2d3c4",
    "name": "VM Snapshot",
    "cron_expression": "0 2 * * *",
    "enabled": true,
    "execution_count": 0,
    ...
  },
  "timestamp": "2025-11-27T10:30:00"
}
```python

#### List Jobs [2]

```bash
GET /api/v1/jobs?owner=admin

Response (200 OK):
{
  "status": "success",
  "data": {
    "jobs": [
      {
        "job_id": "f8a2d3c4",
        "name": "VM Snapshot",
        ...
      }
    ],
    "count": 1
  },
  "timestamp": "2025-11-27T10:30:00"
}
```python

#### Execute Job

```bash
POST /api/v1/jobs/f8a2d3c4/run

Response (200 OK):
{
  "status": "success",
  "data": {
    "job_id": "f8a2d3c4",
    "execution_id": "exec_001",
    "status": "completed",
    "start_time": "2025-11-27T10:30:00",
    "end_time": "2025-11-27T10:35:00",
    "duration_seconds": 300.0,
    "exit_code": 0
  },
  "timestamp": "2025-11-27T10:35:00"
}
```python

#### Get Job Statistics [2]

```bash
GET /api/v1/jobs/f8a2d3c4/stats

Response (200 OK):
{
  "status": "success",
  "data": {
    "job_id": "f8a2d3c4",
    "name": "VM Snapshot",
    "total_executions": 28,
    "successful_executions": 27,
    "failed_executions": 1,
    "success_rate": 0.964,
    "average_duration_seconds": 305.2,
    "last_execution": "2025-11-27T02:00:00",
    "next_execution": "2025-11-28T02:00:00"
  },
  "timestamp": "2025-11-27T10:30:00"
}
```python

---

## Python API

### Basic Usage

```python
from opt.services.scheduler.core import get_scheduler, JobPriority

# Get scheduler instance
scheduler = get_scheduler()

# Create a job [2]
job = scheduler.create_job(
    name="Weekly Report",
    cron_expr="0 9 * * 1",  # Monday 9 AM
    task_type="generate_report",
    task_config={
        "report_type": "weekly",
        "include_metrics": True
    },
    priority=JobPriority.NORMAL,
    owner="analytics_team",
    timeout_seconds=7200,
    description="Generate weekly analytics report"
)

print(f"Created job: {job.job_id}")
print(f"Next execution: {job.next_execution}")
```python

### Task Handlers

Register handlers for custom task types:

```python
import asyncio
from opt.services.scheduler.core import get_scheduler

scheduler = get_scheduler()

# Define async handler
async def handle_backup_task(config):
    """Handler for backup tasks."""
    vm_id = config["vm_id"]
    print(f"Starting backup for {vm_id}")

    # Perform backup operation
    await asyncio.sleep(1)  # Simulated work

    print(f"Backup completed for {vm_id}")
    return True

# Register handler
scheduler.register_task_handler("backup", handle_backup_task)

# Create job that uses this handler
job = scheduler.create_job(
    name="VM Backup",
    cron_expr="0 3 * * *",  # 3 AM daily
    task_type="backup",
    task_config={"vm_id": "vm-789"}
)
```python

### Job Dependencies

Create jobs that depend on others:

```python
from opt.services.scheduler.core import JobDependency, DependencyType

# Create first job
backup_job = scheduler.create_job(
    name="Create Snapshot",
    cron_expr="0 2 * * *",
    task_type="create_snapshot",
    task_config={"vm_id": "vm-123"}
)

# Create second job that depends on first
verify_job = scheduler.create_job(
    name="Verify Backup",
    cron_expr="0 3 * * *",
    task_type="verify_backup",
    task_config={"backup_id": "backup-123"},
    dependencies=[
        JobDependency(
            job_id=backup_job.job_id,
            dependency_type=DependencyType.REQUIRES,
            timeout_seconds=3600
        )
    ]
)
```python

### Execute Jobs

```python
import asyncio

# Execute job manually [2]
async def run_job():
    result = await scheduler.execute_job(job.job_id, manual=True)
    print(f"Status: {result.status.value}")
    print(f"Duration: {result.duration_seconds}s")
    if result.stderr:
        print(f"Error: {result.stderr}")

asyncio.run(run_job())
```python

### View Statistics

```python

# Get job statistics [3]
stats = scheduler.get_job_statistics(job.job_id)
print(f"Total executions: {stats['total_executions']}")
print(f"Success rate: {stats['success_rate']*100:.1f}%")
print(f"Average duration: {stats['average_duration_seconds']:.2f}s")

# Get execution history
history = scheduler.get_execution_history(job.job_id, limit=10)
for execution in history:
    print(f"{execution.execution_id}: {execution.status.value}")
```python

---

## Configuration [2]

### Cron Expression Reference

```python
+------------- minute (0 - 59)
| +------------- hour (0 - 23)
| | +------------- day of month (1 - 31)
| | | +------------- month (1 - 12)
| | | | +------------- day of week (0 - 6) (0 = Sunday)
| | | | |
| | | | |
* * * * *
```python

### Examples

| Expression | Meaning |
|------------|---------|
| `0 * * * *` | Every hour |
| `0 0 * * *` | Daily at midnight |
| `0 2 * * *` | Daily at 2 AM |
| `0 9 * * 1` | Monday at 9 AM |
| `*/15 * * * *` | Every 15 minutes |
| `0 0,12 * * *` | Noon and midnight |
| `0 0 1 * *` | First day of month |
| `0 0 * * 0` | Every Sunday |

### Priority Levels

| Level | Value | Use Case |
|-------|-------|----------|
| CRITICAL | 3 | System-critical operations |
| HIGH | 2 | Important scheduled tasks |
| NORMAL | 1 | Regular operations (default) |
| LOW | 0 | Non-urgent background tasks |

---

## Advanced Usage

### Custom Task Types

```python

# Define multiple task handlers
async def handle_dns_update(config):
    """Update DNS records."""
    zone = config["zone"]
    records = config["records"]
    # Implementation...

async def handle_compliance_scan(config):
    """Run compliance scan."""
    policy = config["policy"]
    target = config["target"]
    # Implementation...

# Register handlers
scheduler.register_task_handler("dns_update", handle_dns_update)
scheduler.register_task_handler("compliance_scan", handle_compliance_scan)

# Create jobs
dns_job = scheduler.create_job(
    name="DNS Update",
    cron_expr="0 * * * *",
    task_type="dns_update",
    task_config={"zone": "example.com", "records": [...]}
)

scan_job = scheduler.create_job(
    name="Compliance Scan",
    cron_expr="0 0 * * 0",
    task_type="compliance_scan",
    task_config={"policy": "pci-dss", "target": "prod-cluster"}
)
```python

### Job Workflows

```python

# Create multi-step workflow
steps = [
    ("backup", {"vm_id": "vm-123"}),
    ("verify", {"backup_id": "latest"}),
    ("archive", {"retention_days": 30}),
]

prev_job = None
for task_type, task_config in steps:
    job = scheduler.create_job(
        name=f"Workflow: {task_type}",
        cron_expr="0 2 * * *",
        task_type=task_type,
        task_config=task_config
    )

    if prev_job:
        # Make this job dependent on previous
        job.dependencies.append(
            JobDependency(
                job_id=prev_job.job_id,
                dependency_type=DependencyType.REQUIRES
            )
        )

    prev_job = job
```python

### Backup and Restore

```python
import json

# Backup all jobs
backup_data = {
    "timestamp": datetime.utcnow().isoformat(),
    "jobs": [j.to_dict() for j in scheduler.jobs.values()]
}

with open("scheduler_backup.json", "w") as f:
    json.dump(backup_data, f, indent=2)

# Restore jobs
with open("scheduler_backup.json", "r") as f:
    backup_data = json.load(f)

for job_data in backup_data["jobs"]:
    # Reconstruct and save job
    pass
```python

---

## Troubleshooting

### Common Issues

#### Job Not Executing

**Symptom:** Job is created but never executes

**Solution:**

1. Check if job is enabled: `schedule job show <job_id>`
1. Verify cron expression: `schedule job show <job_id> | grep cron`
1. Check handler is registered: `schedule config list | grep handlers`
1. Review logs: `tail -f /etc/debvisor/scheduler/scheduler.log`

#### Handler Not Found

**Symptom:** Error "No handler for task type: xxx"

**Solution:**

1. Ensure handler is registered before job execution
1. Check handler name matches task_type exactly
1. Verify handler is async or can be run synchronously

#### Job Timeout

**Symptom:** Job executions always fail with timeout

**Solution:**

1. Increase timeout: `schedule job update <job_id> --timeout=7200`
1. Check task configuration is correct
1. Verify system resources are available

#### Dependencies Not Resolved

**Symptom:** Job always skipped due to unresolved dependencies

**Solution:**

1. Check dependency job exists: `schedule job show <dep_job_id>`
1. Verify dependency job has completed successfully
1. Review execution history: `schedule job history <dep_job_id>`

### Debug Mode

Enable debug logging:

```python
import logging
logger = logging.getLogger("DebVisor.Scheduler")
logger.setLevel(logging.DEBUG)

# Add console handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
```python

### Performance Tuning

1. **Max Workers**: Adjust for concurrent job limit
   ```python
   scheduler = JobScheduler(max_workers=20)
```python

1. **History Retention**: Clean old executions
   ```python
   # Remove executions older than 30 days
   cutoff = datetime.utcnow() - timedelta(days=30)
   scheduler.execution_history[job_id] = [
       e for e in scheduler.execution_history[job_id]
       if e.start_time > cutoff
   ]
```python

1. **Batch Operations**: Create multiple jobs efficiently
   ```python
   for config in configs:
       scheduler.create_job(**config)
```python

---

## Support

For issues, questions, or contributions:

- **Documentation**: See this guide
- **Logs**: `/etc/debvisor/scheduler/scheduler.log`
- **API Docs**: `GET /api/v1/health` for version info

---

**End of Advanced Scheduler Documentation**
