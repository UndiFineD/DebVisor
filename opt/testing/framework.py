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


"""
Testing Framework for DebVisor Phase 4 Integration Tests.

Provides:
- Flask test client setup
- Mocking utilities
- WebSocket testing helpers
- Database fixtures
- Common test patterns
- Performance testing utilities
"""

import pytest
from datetime import datetime, timezone
import json
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Generator, List, Optional, Tuple
from unittest.mock import Mock, patch

# Flask testing imports
try:
    from flask import Flask
    from flask.testing import FlaskClient
except ImportError:
    Flask = None  # type: ignore[assignment, misc]
    FlaskClient = None  # type: ignore[assignment, misc]

# SQLAlchemy testing imports
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session
except ImportError:
    create_engine = None  # type: ignore[assignment, misc]
    sessionmaker = None  # type: ignore[assignment, misc]
    Session = None  # type: ignore[assignment, misc]


class TestConfig:
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret-key"
    PRESERVE_CONTEXT_ON_EXCEPTION = False


@dataclass
class TestResponse:
    """Test response wrapper."""

    status_code: int
    data: Any
    json_data: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None

    @classmethod
    def from_flask_response(cls, response):
        """Create from Flask response."""
        json_data = None
        try:
            json_data = response.get_json()
        except Exception:
            pass

        return cls(
            status_code=response.status_code,
            data=response.data,
            json_data=json_data,
            headers=dict(response.headers),
        )

    def assert_status(self, expected: int) -> None:
        """Assert status code."""
        assert (
            self.status_code == expected
        ), f"Expected {expected}, got {self.status_code}"

    def assert_status_ok(self) -> None:
        """Assert 200 OK."""
        self.assert_status(200)

    def assert_status_created(self) -> None:
        """Assert 201 Created."""
        self.assert_status(201)

    def assert_status_bad_request(self) -> None:
        """Assert 400 Bad Request."""
        self.assert_status(400)

    def assert_status_unauthorized(self) -> None:
        """Assert 401 Unauthorized."""
        self.assert_status(401)

    def assert_status_forbidden(self) -> None:
        """Assert 403 Forbidden."""
        self.assert_status(403)

    def assert_status_not_found(self) -> None:
        """Assert 404 Not Found."""
        self.assert_status(404)

    def assert_json_key(self, key: str) -> Any:
        """Assert JSON key exists and return value."""
        assert self.json_data is not None, "Response is not JSON"
        assert key in self.json_data, f"Key '{key}' not found in response"
        return self.json_data[key]


class FlaskTestClient:
    """Wrapper for Flask test client."""

    def __init__(self, app: "Flask"):
        """
        Initialize test client.

        Args:
            app: Flask application instance
        """
        self.app = app
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def get(self, path: str, **kwargs) -> TestResponse:
        """GET request."""
        response = self.client.get(path, **kwargs)
        return TestResponse.from_flask_response(response)

    def post(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> TestResponse:
        """POST request."""
        if json:
            response = self.client.post(path, json=json, **kwargs)
        else:
            response = self.client.post(path, data=data, **kwargs)
        return TestResponse.from_flask_response(response)

    def put(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> TestResponse:
        """PUT request."""
        if json:
            response = self.client.put(path, json=json, **kwargs)
        else:
            response = self.client.put(path, data=data, **kwargs)
        return TestResponse.from_flask_response(response)

    def delete(self, path: str, **kwargs) -> TestResponse:
        """DELETE request."""
        response = self.client.delete(path, **kwargs)
        return TestResponse.from_flask_response(response)

    def cleanup(self) -> None:
        """Clean up test client."""
        self.app_context.pop()


class MockWebSocket:
    """Mock WebSocket for testing."""

    def __init__(self) -> None:
        """Initialize mock WebSocket."""
        self.sent_messages: List[str] = []
        self.received_messages: List[str] = []

    async def send(self, message: str) -> None:
        """Send message."""
        self.sent_messages.append(message)

    async def receive(self) -> str:
        """Receive message."""
        if not self.received_messages:
            raise RuntimeError("No messages to receive")
        return self.received_messages.pop(0)

    def queue_message(self, message: str) -> None:
        """Queue message for reception."""
        self.received_messages.append(message)

    def get_sent_messages(self) -> List[str]:
        """Get all sent messages."""
        return self.sent_messages.copy()

    def clear(self) -> None:
        """Clear message history."""
        self.sent_messages.clear()
        self.received_messages.clear()


class MockDatabase:
    """Mock database for testing."""

    def __init__(self) -> None:
        """Initialize mock database."""
        self.data: Dict[str, List[Dict[str, Any]]] = {}
        self.call_log: List[Dict[str, Any]] = []

    def set_table(self, table_name: str, data: List[Dict[str, Any]]) -> None:
        """Set table data."""
        self.data[table_name] = data

    def query(self, table_name: str, **filters) -> List[Dict[str, Any]]:
        """Query table."""
        self.call_log.append(
            {
                "action": "query",
                "table": table_name,
                "filters": filters,
            }
        )

        if table_name not in self.data:
            return []

        results = self.data[table_name]

        # Apply filters
        for key, value in filters.items():
            results = [r for r in results if r.get(key) == value]

        return results

    def insert(self, table_name: str, record: Dict[str, Any]) -> None:
        """Insert record."""
        self.call_log.append(
            {
                "action": "insert",
                "table": table_name,
                "record": record,
            }
        )

        if table_name not in self.data:
            self.data[table_name] = []

        self.data[table_name].append(record)

    def update(self, table_name: str, filters: Dict[str, Any], updates: Dict[str, Any]) -> None:
        """Update records."""
        self.call_log.append(
            {
                "action": "update",
                "table": table_name,
                "filters": filters,
                "updates": updates,
            }
        )

        if table_name not in self.data:
            return

        for record in self.data[table_name]:
            if all(record.get(k) == v for k, v in filters.items()):
                record.update(updates)

    def delete(self, table_name: str, **filters) -> None:
        """Delete records."""
        self.call_log.append(
            {
                "action": "delete",
                "table": table_name,
                "filters": filters,
            }
        )

        if table_name not in self.data:
            return

        self.data[table_name] = [
            r
            for r in self.data[table_name]
            if not all(r.get(k) == v for k, v in filters.items())
        ]

    def get_call_log(self) -> List[Dict[str, Any]]:
        """Get call log."""
        return self.call_log.copy()


@pytest.fixture
def flask_app() -> "Flask":
    """Create Flask test application."""
    if Flask is None:
        pytest.skip("Flask not installed")

    app = Flask(__name__)
    app.config.from_object(TestConfig)
    return app


@pytest.fixture
def test_client(flask_app: "Flask") -> FlaskTestClient:
    """Create Flask test client."""
    return FlaskTestClient(flask_app)


@pytest.fixture
def mock_websocket() -> MockWebSocket:
    """Create mock WebSocket."""
    return MockWebSocket()


@pytest.fixture
def mock_database() -> MockDatabase:
    """Create mock database."""
    return MockDatabase()


class TestDataBuilder:
    """Builder for creating test data."""

    @staticmethod
    def build_user(
        user_id: str = "test_user",
        email: str = "test@example.com",
        roles: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Build user test data."""
        return {
            "user_id": user_id,
            "email": email,
            "roles": roles or ["user"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def build_node(
        node_id: str = "node1",
        status: str = "online",
        cpu_usage: float = 50.0,
        memory_usage: float = 60.0,
    ) -> Dict[str, Any]:
        """Build node test data."""
        return {
            "node_id": node_id,
            "status": status,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "last_update": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def build_job(
        job_id: str = "job1",
        status: str = "running",
        progress: int = 50,
    ) -> Dict[str, Any]:
        """Build job test data."""
        return {
            "job_id": job_id,
            "status": status,
            "progress": progress,
            "started_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def build_alert(
        alert_id: str = "alert1",
        alert_type: str = "WARNING",
        severity: str = "warning",
        message: str = "Test alert",
    ) -> Dict[str, Any]:
        """Build alert test data."""
        return {
            "alert_id": alert_id,
            "type": alert_type,
            "severity": severity,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


@dataclass
class PerformanceMetrics:
    """Performance metrics for a test."""

    duration_ms: float
    memory_usage_mb: float
    cpu_usage_percent: float
    calls_made: int

    @property
    def is_acceptable(self) -> bool:
        """Check if metrics are acceptable."""
        return (
            self.duration_ms < 1000    # Less than 1 second
            and self.memory_usage_mb < 500    # Less than 500MB
        )


class PerformanceTester:
    """Test performance of functions."""

    @staticmethod
    def measure_execution_time(
        func,
        *args,
        iterations: int = 100,
        **kwargs,
    ) -> PerformanceMetrics:
        """
        Measure function execution time.

        Args:
            func: Function to measure
            *args: Function arguments
            iterations: Number of iterations
            **kwargs: Function keyword arguments

        Returns:
            PerformanceMetrics
        """
        import time

        start = time.time()

        for _ in range(iterations):
            func(*args, **kwargs)

        duration = (time.time() - start) * 1000 / iterations

        return PerformanceMetrics(
            duration_ms=duration,
            memory_usage_mb=0,
            cpu_usage_percent=0,
            calls_made=iterations,
        )

    @staticmethod
    async def measure_async_execution_time(
        func,
        *args,
        iterations: int = 100,
        **kwargs,
    ) -> PerformanceMetrics:
        """Measure async function execution time."""
        import time

        start = time.time()

        for _ in range(iterations):
            await func(*args, **kwargs)

        duration = (time.time() - start) * 1000 / iterations

        return PerformanceMetrics(
            duration_ms=duration,
            memory_usage_mb=0,
            cpu_usage_percent=0,
            calls_made=iterations,
        )


class IntegrationTestHelper:
    """Helper for integration tests."""

    def __init__(self, test_client: FlaskTestClient):
        """
        Initialize helper.

        Args:
            test_client: FlaskTestClient instance
        """
        self.test_client = test_client
        self.created_resources: List[Tuple[str, str]] = []

    def track_resource(self, resource_type: str, resource_id: str) -> None:
        """Track created resource for cleanup."""
        self.created_resources.append((resource_type, resource_id))

    def cleanup(self) -> None:
        """Clean up all tracked resources."""
        # Delete in reverse order
        for resource_type, resource_id in reversed(self.created_resources):
            try:
            # Implement resource-specific cleanup
                pass
            except Exception as e:
                print(f"Cleanup error: {e}")

    def assert_response_structure(
        self,
        response: TestResponse,
        required_keys: List[str],
    ) -> None:
        """Assert response has required keys."""
        assert response.json_data is not None
        for key in required_keys:
            assert (
                key in response.json_data
            ), f"Required key '{key}' not found in response"


# Common test utilities


def assert_valid_json(data: str) -> Dict[str, Any]:
    """Assert string is valid JSON."""
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON: {e}")


def assert_valid_iso_datetime(date_str: str) -> datetime:
    """Assert string is valid ISO datetime."""
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError as e:
        raise AssertionError(f"Invalid ISO datetime: {e}")


@contextmanager
def assert_raises(exception_type: type) -> Generator:
    """Context manager for asserting exception is raised."""
    try:
        yield
        raise AssertionError(f"Expected {exception_type.__name__} to be raised")
    except exception_type:  # type: ignore[misc]
        pass


@contextmanager
def mock_external_service(
    service_name: str,
    mock_responses: Dict[str, Any],
) -> Generator[Mock, None, None]:
    """Context manager for mocking external service."""
    with patch(f"opt.services.{service_name}") as mock_service:
        for method, response in mock_responses.items():
            setattr(mock_service, method, Mock(return_value=response))
        yield mock_service
