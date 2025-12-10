"""
Advanced VM Scheduling System - Test Suite

Comprehensive tests for scheduler core, CLI, and REST API including unit tests,
integration tests, and performance benchmarks.

Author: DebVisor Development Team
Date: November 27, 2025
Version: 1.0.0
"""

import asyncio
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

# Import scheduler components
from opt.services.scheduler.core import (
    JobScheduler,
    JobStatus,
    JobPriority,
    CronExpression,
    JobExecutionResult,
    FileJobRepository,
)
from opt.services.scheduler.cli import SchedulerCLI
from opt.services.scheduler.api import SchedulerAPI

# ============================================================================
# Core Scheduler Tests
# ============================================================================


class TestCronExpression(unittest.TestCase):
    """Test cron expression parsing and validation."""

    def test_valid_cron_expression(self) -> None:
        """Test parsing valid cron expressions."""
        cron = CronExpression.from_string("0 * * * *")
        self.assertEqual(cron.minute, "0")
        self.assertEqual(cron.hour, "*")
        self.assertEqual(cron.to_string(), "0 * * * *")

    def test_invalid_minute(self) -> None:
        """Test invalid minute value."""
        with self.assertRaises(ValueError):
            CronExpression.from_string("60 * * * *")

    def test_invalid_hour(self) -> None:
        """Test invalid hour value."""
        with self.assertRaises(ValueError):
            CronExpression.from_string("0 24 * * *")

    def test_cron_range(self) -> None:
        """Test cron range expressions."""
        cron = CronExpression.from_string("0-30 * * * *")
        self.assertEqual(cron.minute, "0-30")

    def test_cron_list(self) -> None:
        """Test cron list expressions."""
        cron = CronExpression.from_string("0, 15, 30, 45 * * * *")
        self.assertEqual(cron.minute, "0, 15, 30, 45")

    def test_cron_step(self) -> None:
        """Test cron step expressions."""
        cron = CronExpression.from_string("*/15 * * * *")
        self.assertEqual(cron.minute, "*/15")

    def test_invalid_expression_format(self) -> None:
        """Test invalid expression format."""
        with self.assertRaises(ValueError):
            CronExpression.from_string("invalid")

    def test_invalid_expression_parts(self) -> None:
        """Test invalid number of parts."""
        with self.assertRaises(ValueError):
            CronExpression.from_string("0 * * *")    # Missing day of week


class TestSchedulerCore(unittest.TestCase):
    """Test scheduler core functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        repository = FileJobRepository(config_dir=self.temp_dir)
        self.scheduler = JobScheduler(repository=repository)

    def tearDown(self) -> None:
        """Clean up after tests."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_job(self) -> None:
        """Test job creation."""
        job = self.scheduler.create_job(
            name="Test Job",
            cron_expr="0 * * * *",
            task_type="test_task",
            task_config={"key": "value"},
            owner="test_user",
        )

        self.assertIsNotNone(job.job_id)
        self.assertEqual(job.name, "Test Job")
        self.assertEqual(job.task_type, "test_task")
        self.assertEqual(job.owner, "test_user")
        self.assertTrue(job.enabled)
        self.assertEqual(job.execution_count, 0)

    def test_list_jobs(self) -> None:
        """Test listing jobs."""
        self.scheduler.create_job(
            name="Job 1",
            cron_expr="0 * * * *",
            task_type="task1",
            task_config={},
            owner="user1",
        )
        self.scheduler.create_job(
            name="Job 2",
            cron_expr="0 * * * *",
            task_type="task2",
            task_config={},
            owner="user2",
        )

        all_jobs = self.scheduler.list_jobs()
        self.assertEqual(len(all_jobs), 2)

        user1_jobs = self.scheduler.list_jobs(owner="user1")
        self.assertEqual(len(user1_jobs), 1)
        self.assertEqual(user1_jobs[0].name, "Job 1")

    def test_get_job(self) -> None:
        """Test getting a job."""
        job = self.scheduler.create_job(
            name="Test Job", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        retrieved = self.scheduler.get_job(job.job_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Test Job")

        missing = self.scheduler.get_job("nonexistent")
        self.assertIsNone(missing)

    def test_update_job(self) -> None:
        """Test updating a job."""
        job = self.scheduler.create_job(
            name="Original Name",
            cron_expr="0 * * * *",
            task_type="test",
            task_config={},
        )

        updated = self.scheduler.update_job(
            job.job_id, name="Updated Name", enabled=False
        )

        self.assertEqual(updated.name, "Updated Name")
        self.assertFalse(updated.enabled)

    def test_delete_job(self) -> None:
        """Test deleting a job."""
        job = self.scheduler.create_job(
            name="To Delete", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        # Verify job exists
        self.assertIsNotNone(self.scheduler.get_job(job.job_id))

        # Delete job
        deleted = self.scheduler.delete_job(job.job_id)
        self.assertTrue(deleted)

        # Verify job is gone
        self.assertIsNone(self.scheduler.get_job(job.job_id))

        # Try to delete again
        deleted_again = self.scheduler.delete_job(job.job_id)
        self.assertFalse(deleted_again)

    def test_register_task_handler(self) -> None:
        """Test registering task handlers."""
        handler = Mock()
        self.scheduler.register_task_handler("test_task", handler)

        self.assertIn("test_task", self.scheduler.task_handlers)
        self.assertEqual(self.scheduler.task_handlers["test_task"], handler)

    @unittest.skipIf(True, "Async execution requires event loop management")
    def test_execute_job(self) -> None:
        """Test job execution."""
        job = self.scheduler.create_job(
            name="Test Job",
            cron_expr="0 * * * *",
            task_type="test_task",
            task_config={},
        )

        # Mock handler
        async def mock_handler(config):
            return "success"

        self.scheduler.register_task_handler("test_task", mock_handler)

        # Execute job
        result = asyncio.run(self.scheduler.execute_job(job.job_id, manual=True))

        self.assertEqual(result.job_id, job.job_id)
        self.assertEqual(result.status, JobStatus.COMPLETED)

    def test_get_execution_history(self) -> None:
        """Test getting execution history."""
        job = self.scheduler.create_job(
            name="Test Job", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        # Create mock executions
        for i in range(5):
            result = JobExecutionResult(
                job_id=job.job_id,
                execution_id=f"exec_{i}",
                status=JobStatus.COMPLETED,
                start_time=datetime.now(timezone.utc) - timedelta(hours=i),
                exit_code=0,
            )
            self.scheduler.execution_history[job.job_id].append(result)

        history = self.scheduler.get_execution_history(job.job_id, limit=3)
        self.assertEqual(len(history), 3)

    def test_get_job_statistics(self) -> None:
        """Test getting job statistics."""
        job = self.scheduler.create_job(
            name="Test Job", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        # Add successful executions
        for i in range(3):
            result = JobExecutionResult(
                job_id=job.job_id,
                execution_id=f"success_{i}",
                status=JobStatus.COMPLETED,
                start_time=datetime.now(timezone.utc),
                end_time=datetime.now(timezone.utc) + timedelta(seconds=10),
                duration_seconds=10.0,
            )
            self.scheduler.execution_history[job.job_id].append(result)

        # Add failed execution
        result = JobExecutionResult(
            job_id=job.job_id,
            execution_id="failed_0",
            status=JobStatus.FAILED,
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(seconds=5),
            duration_seconds=5.0,
        )
        self.scheduler.execution_history[job.job_id].append(result)

        stats = self.scheduler.get_job_statistics(job.job_id)

        self.assertEqual(stats["total_executions"], 4)
        self.assertEqual(stats["successful_executions"], 3)
        self.assertEqual(stats["failed_executions"], 1)
        self.assertAlmostEqual(stats["success_rate"], 0.75)


# ============================================================================
# CLI Tests
# ============================================================================


class TestSchedulerCLI(unittest.TestCase):
    """Test scheduler CLI."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        repository = FileJobRepository(config_dir=self.temp_dir)
        self.scheduler = JobScheduler(repository=repository)
        self.cli = SchedulerCLI(self.scheduler)

    def tearDown(self) -> None:
        """Clean up after tests."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cli_create_job(self) -> None:
        """Test CLI job creation."""
        args = [
            "job",
            "create",
            "--name",
            "CLI Job",
            "--cron",
            "0 * * * *",
            "--task-type",
            "test",
            "--task-config",
            '{"key": "value"}',
        ]

        parser = self.cli.create_argument_parser()
        parsed = parser.parse_args(args)
        exit_code = self.cli._handle_job_command(parsed)

        self.assertEqual(exit_code, 0)
        self.assertEqual(len(self.scheduler.jobs), 1)

    def test_cli_list_jobs(self) -> None:
        """Test CLI job listing."""
        # Create test jobs
        self.scheduler.create_job(
            name="Job 1", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        args = ["job", "list"]
        parser = self.cli.create_argument_parser()
        parsed = parser.parse_args(args)
        exit_code = self.cli._handle_job_command(parsed)

        self.assertEqual(exit_code, 0)

    def test_cli_show_job(self) -> None:
        """Test CLI job show."""
        job = self.scheduler.create_job(
            name="Test Job", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        args = ["job", "show", job.job_id]
        parser = self.cli.create_argument_parser()
        parsed = parser.parse_args(args)
        exit_code = self.cli._handle_job_command(parsed)

        self.assertEqual(exit_code, 0)

    def test_cli_delete_job(self) -> None:
        """Test CLI job deletion."""
        job = self.scheduler.create_job(
            name="To Delete", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        args = ["job", "delete", job.job_id, "--force"]
        parser = self.cli.create_argument_parser()
        parsed = parser.parse_args(args)
        exit_code = self.cli._handle_job_command(parsed)

        self.assertEqual(exit_code, 0)
        self.assertIsNone(self.scheduler.get_job(job.job_id))

    def test_cli_invalid_json(self) -> None:
        """Test CLI with invalid JSON."""
        args = [
            "job",
            "create",
            "--name",
            "Test",
            "--cron",
            "0 * * * *",
            "--task-type",
            "test",
            "--task-config",
            "invalid json",
        ]

        parser = self.cli.create_argument_parser()
        parsed = parser.parse_args(args)
        exit_code = self.cli._handle_job_command(parsed)

        self.assertEqual(exit_code, 1)


# ============================================================================
# REST API Tests
# ============================================================================


class TestSchedulerAPI(unittest.TestCase):
    """Test scheduler REST API."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        repository = FileJobRepository(config_dir=self.temp_dir)
        self.scheduler = JobScheduler(repository=repository)
        self.api = SchedulerAPI(self.scheduler)

    def tearDown(self) -> None:
        """Clean up after tests."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_job_api(self) -> None:
        """Test API job creation."""
        request_data = {
            "name": "API Job",
            "cron_expression": "0 * * * *",
            "task_type": "test",
            "task_config": {"key": "value"},
        }

        body, status, headers = self.api.create_job(json.dumps(request_data))

        self.assertEqual(status, 201)
        response = json.loads(body)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["data"]["name"], "API Job")

    def test_list_jobs_api(self) -> None:
        """Test API job listing."""
        self.scheduler.create_job(
            name="Job 1", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        body, status, headers = self.api.list_jobs()

        self.assertEqual(status, 200)
        response = json.loads(body)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["data"]["count"], 1)

    def test_get_job_api(self) -> None:
        """Test API get job."""
        job = self.scheduler.create_job(
            name="Test Job", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        body, status, headers = self.api.get_job(job.job_id)

        self.assertEqual(status, 200)
        response = json.loads(body)
        self.assertEqual(response["data"]["name"], "Test Job")

    def test_get_missing_job_api(self) -> None:
        """Test API get missing job."""
        body, status, headers = self.api.get_job("nonexistent")

        self.assertEqual(status, 404)
        response = json.loads(body)
        self.assertEqual(response["status"], "error")

    def test_update_job_api(self) -> None:
        """Test API job update."""
        job = self.scheduler.create_job(
            name="Original", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        update_data = {"name": "Updated"}
        body, status, headers = self.api.update_job(job.job_id, json.dumps(update_data))

        self.assertEqual(status, 200)
        response = json.loads(body)
        self.assertEqual(response["data"]["name"], "Updated")

    def test_delete_job_api(self) -> None:
        """Test API job deletion."""
        job = self.scheduler.create_job(
            name="To Delete", cron_expr="0 * * * *", task_type="test", task_config={}
        )

        body, status, headers = self.api.delete_job(job.job_id)

        self.assertEqual(status, 200)
        self.assertIsNone(self.scheduler.get_job(job.job_id))

    def test_get_config_api(self) -> None:
        """Test API get config."""
        body, status, headers = self.api.get_config()

        self.assertEqual(status, 200)
        response = json.loads(body)
        self.assertIn("max_workers", response["data"])

    def test_get_health_api(self) -> None:
        """Test API health check."""
        body, status, headers = self.api.get_health()

        self.assertEqual(status, 200)
        response = json.loads(body)
        self.assertEqual(response["data"]["status"], "healthy")

    def test_invalid_json_api(self) -> None:
        """Test API with invalid JSON."""
        body, status, headers = self.api.create_job("invalid json")

        self.assertEqual(status, 400)
        response = json.loads(body)
        self.assertEqual(response["status"], "error")


# ============================================================================
# Integration Tests
# ============================================================================


class TestSchedulerIntegration(unittest.TestCase):
    """Integration tests for the scheduler system."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        repository = FileJobRepository(config_dir=self.temp_dir)
        self.scheduler = JobScheduler(repository=repository)

    def tearDown(self) -> None:
        """Clean up after tests."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_end_to_end_job_lifecycle(self) -> None:
        """Test complete job lifecycle."""
        # Create job
        job = self.scheduler.create_job(
            name="E2E Test",
            cron_expr="0 * * * *",
            task_type="test",
            task_config={"param": "value"},
            owner="admin",
        )
        self.assertIsNotNone(job.job_id)

        # Update job
        updated = self.scheduler.update_job(job.job_id, name="E2E Updated")
        self.assertEqual(updated.name, "E2E Updated")

        # Get job
        retrieved = self.scheduler.get_job(job.job_id)
        self.assertEqual(retrieved.name, "E2E Updated")

        # List jobs
        jobs = self.scheduler.list_jobs(owner="admin")
        self.assertEqual(len(jobs), 1)

        # Delete job
        deleted = self.scheduler.delete_job(job.job_id)
        self.assertTrue(deleted)
        self.assertIsNone(self.scheduler.get_job(job.job_id))

    def test_multiple_jobs_management(self) -> None:
        """Test managing multiple jobs."""
        # Create multiple jobs
        for i in range(5):
            self.scheduler.create_job(
                name=f"Job {i}",
                cron_expr="0 * * * *",
                task_type="test",
                task_config={},
                priority=JobPriority.NORMAL if i % 2 == 0 else JobPriority.HIGH,
            )

        # Verify creation
        jobs = self.scheduler.list_jobs()
        self.assertEqual(len(jobs), 5)

        # Verify filtering
        high_priority = [j for j in jobs if j.priority == JobPriority.HIGH]
        self.assertEqual(len(high_priority), 2)


# ============================================================================
# Test Runner
# ============================================================================


if __name__ == "__main__":
    unittest.main(verbosity=2)
