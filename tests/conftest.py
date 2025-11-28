"""
Shared Test Configuration and Fixtures - Phase 6

This module provides common fixtures, mocking utilities, and test helpers used
across all Phase 6 test suites.

Common Features:
- Database fixtures and mocking
- Mock object factories
- Async test utilities
- Common assertions and helpers
- Test data generators
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, MagicMock, patch
from typing import Dict, Any, Optional, List, Callable
from contextlib import asynccontextmanager, contextmanager
import time
import uuid
import json
import logging


# ============================================================================
# Logging Configuration
# ============================================================================

@pytest.fixture(scope="session")
def setup_logging():
    """Configure logging for tests"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("test_debug.log")
        ]
    )
    yield
    logging.shutdown()


# ============================================================================
# Event Loop Configuration
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_context():
    """Provide async context for tests"""
    # Setup
    context = {
        "tasks": [],
        "resources": []
    }
    
    yield context
    
    # Cleanup
    for task in context.get("tasks", []):
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
    
    for resource in context.get("resources", []):
        if hasattr(resource, "close"):
            await resource.close()


# ============================================================================
# Mock Database Fixtures
# ============================================================================

@pytest.fixture
def mock_database():
    """Create mock database"""
    db = AsyncMock()
    db.connection = AsyncMock()
    db.cursor = AsyncMock()
    db.execute = AsyncMock()
    db.fetch_one = AsyncMock(return_value={"id": "1", "name": "test"})
    db.fetch_all = AsyncMock(return_value=[
        {"id": "1", "name": "test1"},
        {"id": "2", "name": "test2"}
    ])
    db.insert = AsyncMock(return_value="id-1")
    db.update = AsyncMock(return_value=1)
    db.delete = AsyncMock(return_value=1)
    return db


@pytest.fixture
def mock_cache():
    """Create mock cache (Redis-like)"""
    cache = AsyncMock()
    cache.get = AsyncMock(return_value=None)
    cache.set = AsyncMock(return_value=True)
    cache.delete = AsyncMock(return_value=True)
    cache.exists = AsyncMock(return_value=False)
    cache.incr = AsyncMock(return_value=1)
    cache.expire = AsyncMock(return_value=True)
    return cache


@pytest.fixture
def mock_queue():
    """Create mock message queue"""
    queue = AsyncMock()
    queue.push = AsyncMock(return_value=True)
    queue.pop = AsyncMock(return_value={"message": "test"})
    queue.length = AsyncMock(return_value=5)
    queue.clear = AsyncMock(return_value=True)
    return queue


# ============================================================================
# Mock External Services
# ============================================================================

@pytest.fixture
def mock_kubernetes():
    """Create mock Kubernetes client"""
    k8s = AsyncMock()
    k8s.create_pod = AsyncMock(return_value="pod-001")
    k8s.delete_pod = AsyncMock(return_value=True)
    k8s.get_pod_status = AsyncMock(return_value="Running")
    k8s.list_pods = AsyncMock(return_value=[
        {"name": "pod-1", "status": "Running"},
        {"name": "pod-2", "status": "Running"}
    ])
    return k8s


@pytest.fixture
def mock_http_client():
    """Create mock HTTP client"""
    client = AsyncMock()
    client.get = AsyncMock(return_value={
        "status": 200,
        "body": {"message": "success"}
    })
    client.post = AsyncMock(return_value={
        "status": 201,
        "body": {"id": "1"}
    })
    client.put = AsyncMock(return_value={
        "status": 200,
        "body": {"updated": True}
    })
    client.delete = AsyncMock(return_value={
        "status": 204,
        "body": {}
    })
    return client


@pytest.fixture
def mock_file_system():
    """Create mock file system"""
    fs = AsyncMock()
    fs.read = AsyncMock(return_value="file content")
    fs.write = AsyncMock(return_value=True)
    fs.delete = AsyncMock(return_value=True)
    fs.exists = AsyncMock(return_value=True)
    fs.list_files = AsyncMock(return_value=["file1.txt", "file2.txt"])
    fs.mkdir = AsyncMock(return_value=True)
    fs.rmdir = AsyncMock(return_value=True)
    return fs


# ============================================================================
# Test Data Generators
# ============================================================================

class TestDataFactory:
    """Factory for generating test data"""
    
    @staticmethod
    def generate_id(prefix: str = "id") -> str:
        """Generate unique ID"""
        return f"{prefix}-{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def generate_email() -> str:
        """Generate test email"""
        return f"test-{uuid.uuid4().hex[:8]}@example.com"
    
    @staticmethod
    def generate_ip() -> str:
        """Generate random IP address"""
        return f"192.168.{TestDataFactory._random_int(1, 255)}.{TestDataFactory._random_int(1, 255)}"
    
    @staticmethod
    def generate_cidr() -> str:
        """Generate random CIDR"""
        return f"192.168.{TestDataFactory._random_int(1, 255)}.0/24"
    
    @staticmethod
    def generate_uuid() -> str:
        """Generate UUID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_timestamp() -> float:
        """Generate current timestamp"""
        return time.time()
    
    @staticmethod
    def generate_json_data(depth: int = 1, size: int = 3) -> Dict[str, Any]:
        """Generate random JSON-like data"""
        if depth == 0:
            return {
                "value": TestDataFactory._random_int(1, 100),
                "text": f"text-{TestDataFactory._random_int(1, 1000)}"
            }
        
        return {
            f"field_{i}": TestDataFactory.generate_json_data(depth - 1, size)
            for i in range(size)
        }
    
    @staticmethod
    def _random_int(min_val: int, max_val: int) -> int:
        """Generate random integer"""
        import random
        return random.randint(min_val, max_val)


@pytest.fixture
def test_factory():
    """Provide test data factory"""
    return TestDataFactory


# ============================================================================
# Mock API Response Factory
# ============================================================================

class MockAPIResponseFactory:
    """Factory for generating mock API responses"""
    
    @staticmethod
    def success(data: Any = None, status: int = 200, message: str = "Success"):
        """Generate success response"""
        return {
            "status": status,
            "success": True,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(message: str, status: int = 400, error_code: str = "GENERAL_ERROR"):
        """Generate error response"""
        return {
            "status": status,
            "success": False,
            "message": message,
            "error_code": error_code
        }
    
    @staticmethod
    def paginated(items: List[Any], page: int = 1, page_size: int = 10, total: int = 50):
        """Generate paginated response"""
        return {
            "status": 200,
            "success": True,
            "data": items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "pages": (total + page_size - 1) // page_size
            }
        }


@pytest.fixture
def api_response_factory():
    """Provide API response factory"""
    return MockAPIResponseFactory


# ============================================================================
# Context Managers for Test Utilities
# ============================================================================

@contextmanager
def assert_raises(exception_type, message_contains: Optional[str] = None):
    """Context manager for asserting exceptions with optional message check"""
    try:
        yield
    except exception_type as e:
        if message_contains and message_contains not in str(e):
            raise AssertionError(
                f"Exception message '{str(e)}' does not contain '{message_contains}'"
            )
    except Exception as e:
        raise AssertionError(
            f"Expected {exception_type.__name__} but got {type(e).__name__}: {str(e)}"
        )
    else:
        raise AssertionError(f"Expected {exception_type.__name__} to be raised")


@contextmanager
def assert_runtime(max_seconds: float):
    """Context manager for asserting execution time"""
    start = time.time()
    yield
    elapsed = time.time() - start
    assert elapsed <= max_seconds, f"Execution took {elapsed}s, expected <= {max_seconds}s"


@asynccontextmanager
async def assert_async_runtime(max_seconds: float):
    """Context manager for asserting async execution time"""
    start = time.time()
    yield
    elapsed = time.time() - start
    assert elapsed <= max_seconds, f"Execution took {elapsed}s, expected <= {max_seconds}s"


@pytest.fixture
def mock_context_managers():
    """Provide context manager fixtures"""
    return {
        "assert_raises": assert_raises,
        "assert_runtime": assert_runtime,
        "assert_async_runtime": assert_async_runtime
    }


# ============================================================================
# Common Assertions
# ============================================================================

class CommonAssertions:
    """Common assertion helpers"""
    
    @staticmethod
    def assert_dict_contains(actual: Dict, expected: Dict):
        """Assert dict contains expected keys and values"""
        for key, value in expected.items():
            assert key in actual, f"Key '{key}' not found in actual dict"
            assert actual[key] == value, f"Value mismatch for key '{key}': {actual[key]} != {value}"
    
    @staticmethod
    def assert_list_contains_any(actual: List, *items):
        """Assert list contains any of the items"""
        for item in items:
            if item in actual:
                return
        raise AssertionError(f"List does not contain any of: {items}")
    
    @staticmethod
    def assert_list_contains_all(actual: List, *items):
        """Assert list contains all items"""
        for item in items:
            assert item in actual, f"List does not contain: {item}"
    
    @staticmethod
    def assert_response_valid(response: Dict):
        """Assert response has valid structure"""
        assert "status" in response, "Response missing 'status' field"
        assert "success" in response, "Response missing 'success' field"
        assert isinstance(response["success"], bool), "'success' must be bool"


@pytest.fixture
def assertions():
    """Provide common assertions"""
    return CommonAssertions


# ============================================================================
# Mock Decorators
# ============================================================================

def mock_external_calls(func: Callable):
    """Decorator to mock external calls"""
    async def wrapper(*args, **kwargs):
        with patch("requests.get") as mock_get, \
             patch("requests.post") as mock_post:
            mock_get.return_value.status_code = 200
            mock_post.return_value.status_code = 200
            return await func(*args, **kwargs)
    return wrapper


def skip_if_integration():
    """Decorator to skip tests in integration mode"""
    import os
    if os.getenv("INTEGRATION_TESTS") == "true":
        return pytest.mark.skip(reason="Skipped in integration mode")
    return lambda func: func


def skip_if_not_integration():
    """Decorator to skip tests unless in integration mode"""
    import os
    if os.getenv("INTEGRATION_TESTS") != "true":
        return pytest.mark.skip(reason="Skipped unless in integration mode")
    return lambda func: func


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow"
    )
    config.addinivalue_line(
        "markers", "requires_db: mark test as requiring database"
    )


# ============================================================================
# Autouse Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks before each test"""
    yield
    # Cleanup happens here if needed


@pytest.fixture(autouse=True)
def capture_test_time(request):
    """Capture and log test execution time"""
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"\n{request.node.name} took {elapsed:.3f}s")


# ============================================================================
# Parameterized Test Fixtures
# ============================================================================

@pytest.fixture(params=[
    {"name": "test_1", "value": 10},
    {"name": "test_2", "value": 20},
    {"name": "test_3", "value": 30}
])
def parametrized_test_data(request):
    """Provide parametrized test data"""
    return request.param


# ============================================================================
# Database Transaction Fixtures
# ============================================================================

@pytest.fixture
async def db_transaction(mock_database):
    """Mock database transaction"""
    async with mock_database.transaction() as tx:
        yield tx


# ============================================================================
# Cleanup Utilities
# ============================================================================

@pytest.fixture
def cleanup_stack():
    """Provide cleanup stack for resources"""
    cleanup_actions = []
    
    def register_cleanup(action: Callable, *args, **kwargs):
        cleanup_actions.append((action, args, kwargs))
    
    yield register_cleanup
    
    # Execute cleanup in reverse order
    for action, args, kwargs in reversed(cleanup_actions):
        try:
            if asyncio.iscoroutinefunction(action):
                asyncio.run(action(*args, **kwargs))
            else:
                action(*args, **kwargs)
        except Exception as e:
            logging.error(f"Cleanup error: {e}")


# ============================================================================
# Performance Testing Fixtures
# ============================================================================

@pytest.fixture
def performance_timer():
    """Timer for performance testing"""
    class PerformanceTimer:
        def __init__(self):
            self.marks = {}
        
        def mark(self, name: str):
            self.marks[name] = time.time()
        
        def elapsed(self, start_mark: str, end_mark: str) -> float:
            if start_mark not in self.marks or end_mark not in self.marks:
                raise ValueError("Mark not found")
            return self.marks[end_mark] - self.marks[start_mark]
    
    return PerformanceTimer()


# ============================================================================
# Module-level Fixtures
# ============================================================================

@pytest.fixture(scope="module")
def module_setup():
    """Module-level setup"""
    print("\n=== Module Setup ===")
    yield
    print("\n=== Module Teardown ===")


@pytest.fixture(scope="session")
def session_setup():
    """Session-level setup"""
    print("\n=== Session Setup ===")
    yield
    print("\n=== Session Teardown ===")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
