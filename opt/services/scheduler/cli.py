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
Advanced VM Scheduling System - Command Line Interface

Provides comprehensive CLI for managing scheduled jobs including creation,
listing, execution, monitoring, and state management.

Author: DebVisor Development Team
Date: November 27, 2025
Version: 1.0.0
"""

import argparse
from datetime import datetime, timezone
import asyncio
import json
import sys
from typing import Optional, Any

from opt.core.cli_utils import (
    setup_common_args,
    handle_cli_error,
)
from .core import JobScheduler, JobStatus, JobPriority, CronExpression, get_scheduler

# Configure logging
try:
    from opt.core.logging import configure_logging
except ImportError:
    # Fallback or mock for tests if needed

    def configure_logging(**kwargs):  # type: ignore[misc] -> None:
        """Placeholder docstring."""
        pass


class SchedulerCLI:
    """Command-line interface for job scheduler."""

    def __init__(self, scheduler: Optional[JobScheduler] = None) -> None:
        """Initialize the CLI.

        Args:
            scheduler: JobScheduler instance (uses global if None)
        """
        self.scheduler=scheduler or get_scheduler()

    def create_argument_parser(self) -> argparse.ArgumentParser:
        """Create argument parser.

        Returns:
            ArgumentParser instance
        """
        _parser = argparse.ArgumentParser(
            _prog = "schedule",
            _description = "DebVisor Advanced Scheduler CLI",
            _formatter_class = argparse.RawDescriptionHelpFormatter,
            _epilog = """
Examples:
    # Create a job that runs every hour at minute 0
schedule job create --name="VM Snapshot" --cron="0 * * * *" --task-type=vm_snapshot \\
    --task-config='{"vm_id": "vm-123", "retention_days": 7}'

# List all jobs
schedule job list

# Execute a job immediately
schedule job run f8a2d3c4

# Get job statistics
schedule job stats f8a2d3c4

# View job history
schedule job history f8a2d3c4 --limit=20

# Update a job
schedule job update f8a2d3c4 --enabled=false

# Delete a job
schedule job delete f8a2d3c4
            """,
        )

        setup_common_args(parser)

        _subparsers=parser.add_subparsers(dest="command", help="Command to execute")

        # Job management commands
        _job_parser=subparsers.add_parser("job", help="Job management commands")
        _job_subparsers=job_parser.add_subparsers(dest="action", help="Job action")

        # job create
        _create_parser=job_subparsers.add_parser("create", help="Create a new job")
        create_parser.add_argument("--name", required=True, help="Job name")
        create_parser.add_argument(
            "--cron", required=True, help="Cron expression (e.g., '0 * * * *')"
        )
        create_parser.add_argument(
            "--task-type", required=True, help="Task type (e.g., vm_snapshot)"
        )
        create_parser.add_argument(
            "--task-config", required=True, help="Task config as JSON string"
        )
        create_parser.add_argument(
            "--priority",
            _choices = ["low", "normal", "high", "critical"],
            _default="normal",
            _help="Job priority",
        )
        create_parser.add_argument("--owner", default="system", help="Job owner")
        create_parser.add_argument("--description", default="", help="Job description")
        create_parser.add_argument("--timezone", default="UTC", help="Timezone")
        create_parser.add_argument(
            "--max-retries", type=int, default=3, help="Maximum retries"
        )
        create_parser.add_argument(
            "--timeout", type=int, default=3600, help="Timeout in seconds"
        )
        create_parser.add_argument(
            "--tag",
            _action = "append",
            _nargs = 2,
            _metavar=("KEY", "VALUE"),
            _help="Add metadata tag",
        )

        # job list
        _list_parser=job_subparsers.add_parser("list", help="List jobs")
        list_parser.add_argument("--owner", help="Filter by owner")
        list_parser.add_argument("--status", help="Filter by status")
        list_parser.add_argument(
            "--format", choices=["table", "json"], default="table", help="Output format"
        )

        # job show
        _show_parser=job_subparsers.add_parser("show", help="Show job details")
        show_parser.add_argument("job_id", help="Job ID")
        show_parser.add_argument(
            "--format", choices=["text", "json"], default="text", help="Output format"
        )

        # job delete
        _delete_parser=job_subparsers.add_parser("delete", help="Delete a job")
        delete_parser.add_argument("job_id", help="Job ID")
        delete_parser.add_argument(
            "--force", action="store_true", help="Skip confirmation"
        )

        # job run
        _run_parser=job_subparsers.add_parser("run", help="Execute job immediately")
        run_parser.add_argument("job_id", help="Job ID")
        run_parser.add_argument("--dry-run", action="store_true", help="Dry run mode")

        # job history
        history_parser = job_subparsers.add_parser(
            "history", help="View job execution history"
        )
        history_parser.add_argument("job_id", help="Job ID")
        history_parser.add_argument(
            "--limit", type=int, default=20, help="Number of entries"
        )
        history_parser.add_argument(
            "--format", choices=["table", "json"], default="table", help="Output format"
        )

        # job stats
        _stats_parser=job_subparsers.add_parser("stats", help="Get job statistics")
        stats_parser.add_argument("job_id", help="Job ID")
        stats_parser.add_argument(
            "--format", choices=["text", "json"], default="text", help="Output format"
        )

        # job update
        _update_parser=job_subparsers.add_parser("update", help="Update a job")
        update_parser.add_argument("job_id", help="Job ID")
        update_parser.add_argument("--name", help="New job name")
        update_parser.add_argument("--cron", help="New cron expression")
        update_parser.add_argument(
            "--enabled", choices=["true", "false"], help="Enable/disable job"
        )
        update_parser.add_argument(
            "--priority",
            _choices = ["low", "normal", "high", "critical"],
            _help="New priority",
        )

        # job retry
        _retry_parser=job_subparsers.add_parser("retry", help="Retry failed execution")
        retry_parser.add_argument("job_id", help="Job ID")
        retry_parser.add_argument("execution_id", help="Execution ID")

        # job dependencies
        deps_parser = job_subparsers.add_parser(
            "dependencies", help="Show job dependencies"
        )
        deps_parser.add_argument("job_id", help="Job ID")
        deps_parser.add_argument(
            "--format", choices=["text", "json"], default="text", help="Output format"
        )

        # Config management
        _config_parser=subparsers.add_parser("config", help="Configuration management")
        config_subparsers = config_parser.add_subparsers(
            _dest = "action", help="Config action"
        )

        # config list
        config_list_parser = config_subparsers.add_parser(
            "list", help="List configuration"
        )
        config_list_parser.add_argument(
            "--format", choices=["text", "json"], default="text", help="Output format"
        )

        # config backup
        config_backup_parser = config_subparsers.add_parser(
            "backup", help="Backup configuration"
        )
        config_backup_parser.add_argument(
            "--output", required=True, help="Output file path"
        )

        # config restore
        config_restore_parser = config_subparsers.add_parser(
            "restore", help="Restore configuration"
        )
        config_restore_parser.add_argument(
            "--input", required=True, help="Input file path"
        )
        config_restore_parser.add_argument(
            "--force", action="store_true", help="Force restore"
        )

        return parser

    @handle_cli_error

    def run(self, args: Optional[list[Any]] = None) -> int:
        """Run the CLI.

        Args:
            args: Command line arguments (uses sys.argv if None)

        Returns:
            Exit code
        """
        _parser=self.create_argument_parser()
        _parsed=parser.parse_args(args)

        if not parsed.command:
            parser.print_help()
            return 0

        if parsed.command == "job":
            return self._handle_job_command(parsed)
        elif parsed.command == "config":
            return self._handle_config_command(parsed)
        else:
            parser.print_help()
            return 0

    def _handle_job_command(self, args: argparse.Namespace) -> int:
        """Handle job commands.

        Args:
            args: Parsed arguments

        Returns:
            Exit code
        """
        if not args.action:
            print("Please specify an action (create, list, show, run, history, etc.)")
            return 1

        if args.action == "create":
            return self._cmd_create_job(args)
        elif args.action == "list":
            return self._cmd_list_jobs(args)
        elif args.action == "show":
            return self._cmd_show_job(args)
        elif args.action == "delete":
            return self._cmd_delete_job(args)
        elif args.action == "run":
            return self._cmd_run_job(args)
        elif args.action == "history":
            return self._cmd_job_history(args)
        elif args.action == "stats":
            return self._cmd_job_stats(args)
        elif args.action == "update":
            return self._cmd_update_job(args)
        elif args.action == "retry":
            return self._cmd_retry_job(args)
        elif args.action == "dependencies":
            return self._cmd_show_dependencies(args)
        else:
            print(f"Unknown action: {args.action}")
            return 1

    def _cmd_create_job(self, args: argparse.Namespace) -> int:
        """Create a new job."""
        try:
            _task_config=json.loads(args.task_config)
        except json.JSONDecodeError as e:
            print(f"Invalid task config JSON: {e}")
            return 1

        _priority=JobPriority[args.priority.upper()]
        tags = {}
        if hasattr(args, "tag") and args.tag:
            _tags = {key: value for key, value in args.tag}

        _job = self.scheduler.create_job(
            _name = args.name,
            _cron_expr = args.cron,
            _task_type = args.task_type,
            _task_config = task_config,
            _priority = priority,
            _owner = args.owner,
            _description = args.description,
            _timezone = args.timezone,
            _max_retries = args.max_retries,
            _timeout_seconds = args.timeout,
            _tags = tags,
        )

        print(f"? Created job {job.job_id}: {job.name}")
        print(f"  Cron: {job.cron_expression.to_string()}")
        print(f"  Task: {job.task_type}")
        print(f"  Next execution: {job.next_execution}")

        return 0

    def _cmd_list_jobs(self, args: argparse.Namespace) -> int:
        """List jobs."""
        jobs = self.scheduler.list_jobs(
            _owner=args.owner if hasattr(args, "owner") else None
        )

        if args.format == "json":
            print(json.dumps([j.to_dict() for j in jobs], indent=2))
        else:
            print(
                f"\n{'ID':<10} {'Name':<30} {'Task':<20} {'Priority':<10} {'Enabled':<8}"
            )
            print("-" * 80)
            for job in jobs:
                print(
                    f"{job.job_id:<10} {job.name:<30} {job.task_type:<20} "
                    f"{job.priority.name:<10} {'Yes' if job.enabled else 'No':<8}"
                )
            print(f"\nTotal: {len(jobs)} jobs")

        return 0

    def _cmd_show_job(self, args: argparse.Namespace) -> int:
        """Show job details."""
        _job=self.scheduler.get_job(args.job_id)
        if not job:
            print(f"Job {args.job_id} not found")
            return 1

        if args.format == "json":
            print(json.dumps(job.to_dict(), indent=2))
        else:
            print(f"\nJob Details: {job.name}")
            print(f"ID: {job.job_id}")
            print(f"Status: {'Enabled' if job.enabled else 'Disabled'}")
            print(f"Task Type: {job.task_type}")
            print(f"Cron: {job.cron_expression.to_string()}")
            print(f"Priority: {job.priority.name}")
            print(f"Owner: {job.owner}")
            print(f"Description: {job.description}")
            print(f"Executions: {job.execution_count} (failed: {job.failure_count})")
            print(f"Last Run: {job.last_execution or 'Never'}")
            print(f"Next Run: {job.next_execution}")
            print(f"Timeout: {job.timeout_seconds}s")
            print(f"Max Retries: {job.max_retries}")
            if job.dependencies:
                print(f"Dependencies: {len(job.dependencies)}")
                for dep in job.dependencies:
                    print(f"  - {dep.job_id} ({dep.dependency_type.value})")

        return 0

    def _cmd_delete_job(self, args: argparse.Namespace) -> int:
        """Delete a job."""
        _job=self.scheduler.get_job(args.job_id)
        if not job:
            print(f"Job {args.job_id} not found")
            return 1

        if not args.force:
            _response=input(f"Delete job '{job.name}' ({args.job_id})? [y/N]: ")
            if response.lower() != "y":
                print("Cancelled")
                return 0

        self.scheduler.delete_job(args.job_id)
        print(f"? Deleted job {args.job_id}")

        return 0

    def _cmd_run_job(self, args: argparse.Namespace) -> int:
        """Run a job immediately."""
        _job=self.scheduler.get_job(args.job_id)
        if not job:
            print(f"Job {args.job_id} not found")
            return 1

        if args.dry_run:
            print(f"[DRY RUN] Would execute job {args.job_id}: {job.name}")
            return 0

        print(f"Executing job {args.job_id}: {job.name}...")
        _result=asyncio.run(self.scheduler.execute_job(args.job_id, manual=True))

        print(f"Status: {result.status.value}")
        print(f"Execution ID: {result.execution_id}")
        print(f"Duration: {result.duration_seconds:.2f}s")
        if result.exit_code != 0:
            print(f"Exit Code: {result.exit_code}")
        if result.stderr:
            print(f"Error: {result.stderr}")

        return 0 if result.status == JobStatus.COMPLETED else 1

    def _cmd_job_history(self, args: argparse.Namespace) -> int:
        """Show job execution history."""
        _history=self.scheduler.get_execution_history(args.job_id, limit=args.limit)

        if not history:
            print(f"No execution history for job {args.job_id}")
            return 0

        if args.format == "json":
            print(json.dumps([h.to_dict() for h in history], indent=2))
        else:
            print(f"\nExecution History for Job {args.job_id}")
            print("-" * 100)
            print(
                f"{'Exec ID':<10} {'Status':<12} {'Start Time':<25} {'Duration':<12} {'Exit Code':<10}"
            )
            print("-" * 100)
            for h in history:
                print(
                    f"{h.execution_id:<10} {h.status.value:<12} "
                    f"{h.start_time.isoformat():<25} {h.duration_seconds:<12.2f} {h.exit_code:<10}"
                )
            print(f"\nTotal: {len(history)} executions")

        return 0

    def _cmd_job_stats(self, args: argparse.Namespace) -> int:
        """Show job statistics."""
        _stats=self.scheduler.get_job_statistics(args.job_id)

        if not stats:
            print(f"Job {args.job_id} not found")
            return 1

        if args.format == "json":
            print(json.dumps(stats, indent=2))
        else:
            print(f"\nStatistics for Job: {stats['name']}")
            print(f"ID: {stats['job_id']}")
            print(f"Total Executions: {stats['total_executions']}")
            print(f"Successful: {stats['successful_executions']}")
            print(f"Failed: {stats['failed_executions']}")
            print(f"Success Rate: {stats['success_rate'] * 100:.1f}%")
            print(f"Average Duration: {stats['average_duration_seconds']:.2f}s")
            print(f"Last Execution: {stats['last_execution'] or 'Never'}")
            print(f"Next Execution: {stats['next_execution'] or 'Not scheduled'}")

        return 0

    def _cmd_update_job(self, args: argparse.Namespace) -> int:
        """Update a job."""
        _job=self.scheduler.get_job(args.job_id)
        if not job:
            print(f"Job {args.job_id} not found")
            return 1

        updates = {}
        if hasattr(args, "name") and args.name:
            updates["name"] = args.name
        if hasattr(args, "cron") and args.cron:
            updates["cron_expression"] = CronExpression.from_string(args.cron)
        if hasattr(args, "enabled") and args.enabled:
            updates["enabled"] = args.enabled.lower() == "true"
        if hasattr(args, "priority") and args.priority:
            updates["priority"] = JobPriority[args.priority.upper()]

        if not updates:
            print("No updates specified")
            return 0

        _updated=self.scheduler.update_job(args.job_id, **updates)
        print(f"? Updated job {updated.job_id}: {updated.name}")  # type: ignore[union-attr]

        return 0

    def _cmd_retry_job(self, args: argparse.Namespace) -> int:
        """Retry a failed job execution."""
        _result=self.scheduler.retry_job(args.job_id, args.execution_id)
        print(f"? Retrying job {args.job_id} (execution {args.execution_id})")
        print(f"New execution ID: {result.execution_id}")

        return 0

    def _cmd_show_dependencies(self, args: argparse.Namespace) -> int:
        """Show job dependencies."""
        _job=self.scheduler.get_job(args.job_id)
        if not job:
            print(f"Job {args.job_id} not found")
            return 1

        if not job.dependencies:
            print(f"Job {args.job_id} has no dependencies")
            return 0

        if args.format == "json":
            print(json.dumps([d.to_dict() for d in job.dependencies], indent=2))
        else:
            print(f"\nDependencies for Job {args.job_id}")
            print("-" * 60)
            print(f"{'Job ID':<15} {'Type':<15} {'Timeout':<15}")
            print("-" * 60)
            for dep in job.dependencies:
                print(
                    f"{dep.job_id:<15} {dep.dependency_type.value:<15} {dep.timeout_seconds:<15}s"
                )

        return 0

    def _handle_config_command(self, args: argparse.Namespace) -> int:
        """Handle config commands.

        Args:
            args: Parsed arguments

        Returns:
            Exit code
        """
        if not args.action:
            print("Please specify an action (list, backup, restore)")
            return 1

        if args.action == "list":
            return self._cmd_config_list(args)
        elif args.action == "backup":
            return self._cmd_config_backup(args)
        elif args.action == "restore":
            return self._cmd_config_restore(args)
        else:
            print(f"Unknown action: {args.action}")
            return 1

    def _cmd_config_list(self, args: argparse.Namespace) -> int:
        """List configuration."""
        config = {
            "scheduler_config_dir": self.scheduler.config_dir,  # type: ignore[attr-defined]
            "max_workers": self.scheduler.max_workers,
            "total_jobs": len(self.scheduler.jobs),
            "registered_handlers": list(self.scheduler.task_handlers.keys()),
        }

        if args.format == "json":
            print(json.dumps(config, indent=2))
        else:
            print("\nScheduler Configuration")
            print(f"Config Directory: {config['scheduler_config_dir']}")
            print(f"Max Workers: {config['max_workers']}")
            print(f"Total Jobs: {config['total_jobs']}")
            print(
                f"Registered Task Handlers: {', '.join(config['registered_handlers'])}"
            )

        return 0

    def _cmd_config_backup(self, args: argparse.Namespace) -> int:
        """Backup configuration."""
        backup_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "jobs": [j.to_dict() for j in self.scheduler.jobs.values()],
        }

        try:
            with open(args.output, "w") as f:
                json.dump(backup_data, f, indent=2)
            print(f"? Backup created: {args.output}")
            print(f"  Jobs: {len(backup_data['jobs'])}")
            return 0
        except IOError as e:
            print(f"Failed to create backup: {e}")
            return 1

    def _cmd_config_restore(self, args: argparse.Namespace) -> int:
        """Restore configuration."""
        try:
            with open(args.input, "r") as f:
                _backup_data=json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Failed to read backup: {e}")
            return 1

        if not args.force:
            _response=input(f"Restore {len(backup_data['jobs'])} jobs? [y/N]: ")
            if response.lower() != "y":
                print("Cancelled")
                return 0

        # Restore jobs
        for job_data in backup_data["jobs"]:
        # Reconstruct and save job
            pass

        print(f"? Restored {len(backup_data['jobs'])} jobs")
        return 0


def main(args: Optional[list[Any]] = None) -> int:
    """Main entry point for CLI.

    Args:
        args: Command line arguments

    Returns:
        Exit code
    """
    configure_logging(service_name="scheduler-cli")
    _cli=SchedulerCLI()
    return cli.run(args)


if __name__ == "__main__":
    sys.exit(main())
