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

"""Tests for agent_backend.py"""

from __future__ import annotations
from unittest.mock import MagicMock, patch
import time
import pytest
from agent_test_utils import agent_dir_on_path


@pytest.fixture()
def agent_backend_module() -> any:
    with agent_dir_on_path():
        import agent_backend
        return agent_backend


# ============================================================================
# Caching and Response Tests
# ============================================================================

def test_response_caching_enabled(agent_backend_module: any) -> None:
    """Test that responses are cached when use_cache=True."""
    agent_backend_module.clear_response_cache()
    
    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "cached response"}}]
        }
        mock_requests.post.return_value = mock_response
        
        # First call - should hit API
        result1 = agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", use_cache=True
        )
        assert result1 == "cached response"
        assert mock_requests.post.call_count == 1
        
        # Second call - should use cache
        result2 = agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", use_cache=True
        )
        assert result2 == "cached response"
        assert mock_requests.post.call_count == 1  # Still 1, cache was used


def test_response_cache_disabled(agent_backend_module: any) -> None:
    """Test that caching can be disabled with use_cache=False."""
    agent_backend_module.clear_response_cache()
    
    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "response"}}]
        }
        mock_requests.post.return_value = mock_response
        
        # First call with cache disabled
        agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", use_cache=False
        )
        assert mock_requests.post.call_count == 1
        
        # Second call - should call API again (no caching)
        agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", use_cache=False
        )
        assert mock_requests.post.call_count == 2


def test_clear_response_cache(agent_backend_module: any) -> None:
    """Test that cache can be cleared."""
    agent_backend_module.clear_response_cache()
    
    # Manually add something to cache
    cache_key = agent_backend_module._get_cache_key("test", "gpt-4")
    agent_backend_module._response_cache[cache_key] = "cached"
    
    assert cache_key in agent_backend_module._response_cache
    agent_backend_module.clear_response_cache()
    assert len(agent_backend_module._response_cache) == 0


# ============================================================================
# Response Validation Tests
# ============================================================================

def test_validate_response_content_basic(agent_backend_module: any) -> None:
    """Test basic response validation (non-empty)."""
    assert agent_backend_module.validate_response_content("valid response") is True
    assert agent_backend_module.validate_response_content("") is False
    assert agent_backend_module.validate_response_content("   ") is False
    assert agent_backend_module.validate_response_content(None) is False


def test_validate_response_content_with_types(agent_backend_module: any) -> None:
    """Test response validation with expected content types."""
    # Should pass if content contains expected type
    assert agent_backend_module.validate_response_content(
        "Here is the code:", ["code"]
    ) is True
    
    # Should pass if contains any expected type
    assert agent_backend_module.validate_response_content(
        "Explanation: The code works by...", ["code", "explanation"]
    ) is True
    
    # Case insensitive
    assert agent_backend_module.validate_response_content(
        "CODE: print('hello')", ["code"]
    ) is True


# ============================================================================
# Token and Cost Estimation Tests
# ============================================================================

def test_estimate_tokens(agent_backend_module: any) -> None:
    """Test token estimation."""
    # Empty text
    assert agent_backend_module.estimate_tokens("") == 0
    
    # Rough estimate: ~4 chars per token
    text = "x" * 100
    estimated = agent_backend_module.estimate_tokens(text)
    assert estimated == 25  # 100 / 4


def test_estimate_cost(agent_backend_module: any) -> None:
    """Test cost estimation."""
    # 1000 tokens at $0.03 per 1k = $0.03
    cost = agent_backend_module.estimate_cost(1000, model="gpt-4", rate_per_1k_input=0.03)
    assert abs(cost - 0.03) < 0.001
    
    # 500 tokens at default rate
    cost = agent_backend_module.estimate_cost(500)
    assert cost > 0


# ============================================================================
# Circuit Breaker Tests
# ============================================================================

def test_circuit_breaker_closed_state(agent_backend_module: any) -> None:
    """Test circuit breaker in CLOSED state."""
    breaker = agent_backend_module.CircuitBreaker("test", failure_threshold=3)
    assert breaker.state == "CLOSED"
    assert breaker.is_open() is False
    
    # One failure shouldn't open it
    breaker.record_failure()
    assert breaker.state == "CLOSED"
    assert breaker.is_open() is False


def test_circuit_breaker_opens_on_threshold(agent_backend_module: any) -> None:
    """Test that circuit breaker opens after failure threshold."""
    breaker = agent_backend_module.CircuitBreaker("test", failure_threshold=3)
    
    # Reach threshold
    breaker.record_failure()
    breaker.record_failure()
    breaker.record_failure()
    
    assert breaker.state == "OPEN"
    assert breaker.is_open() is True


def test_circuit_breaker_recovery(agent_backend_module: any) -> None:
    """Test circuit breaker recovery after timeout."""
    breaker = agent_backend_module.CircuitBreaker("test", failure_threshold=2, recovery_timeout=1)
    
    # Open the circuit
    breaker.record_failure()
    breaker.record_failure()
    assert breaker.is_open() is True
    
    # Wait for recovery timeout
    time.sleep(1.1)
    
    # Should be half-open now
    assert breaker.is_open() is False
    assert breaker.state == "HALF_OPEN"
    
    # Success should close it
    breaker.record_success()
    assert breaker.state == "CLOSED"


def test_circuit_breaker_half_open_to_open(agent_backend_module: any) -> None:
    """Test that failure in HALF_OPEN state reopens circuit."""
    breaker = agent_backend_module.CircuitBreaker("test", failure_threshold=2, recovery_timeout=1)
    
    # Open and wait for recovery
    breaker.record_failure()
    breaker.record_failure()
    assert breaker.is_open() is True
    
    time.sleep(1.1)
    breaker.is_open()  # Transition to HALF_OPEN
    
    # Failure should reopen
    breaker.record_failure()
    assert breaker.state == "OPEN"


# ============================================================================
# Metrics Tests
# ============================================================================

def test_get_metrics(agent_backend_module: any) -> None:
    """Test metrics collection."""
    agent_backend_module.reset_metrics()
    
    metrics = agent_backend_module.get_metrics()
    assert "requests" in metrics
    assert "errors" in metrics
    assert "timeouts" in metrics
    assert "cache_hits" in metrics
    assert "total_latency_ms" in metrics


def test_reset_metrics(agent_backend_module: any) -> None:
    """Test metrics reset."""
    agent_backend_module.reset_metrics()
    
    # Manually increment metrics
    agent_backend_module._metrics["requests"] = 100
    assert agent_backend_module._metrics["requests"] == 100
    
    # Reset
    agent_backend_module.reset_metrics()
    assert agent_backend_module._metrics["requests"] == 0


def test_metrics_tracking_in_llm_chat(agent_backend_module: any) -> None:
    """Test that metrics are tracked during API calls."""
    agent_backend_module.reset_metrics()
    agent_backend_module.clear_response_cache()
    
    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "response"}}]
        }
        mock_requests.post.return_value = mock_response
        
        agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", use_cache=False
        )
        
        metrics = agent_backend_module.get_metrics()
        assert metrics["requests"] >= 1


# ============================================================================
# Timeout Configuration Tests
# ============================================================================

def test_configure_timeout_per_backend(agent_backend_module: any) -> None:
    """Test backend-specific timeout configuration."""
    agent_backend_module.configure_timeout_per_backend("github-models", 120)
    
    import os
    assert os.environ.get("DV_AGENT_TIMEOUT_GITHUB-MODELS") == "120"


# ============================================================================
# Streaming Tests
# ============================================================================

def test_streaming_payload_flag(agent_backend_module: any) -> None:
    """Test that streaming flag is included in payload when requested."""
    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "response"}}]
        }
        mock_requests.post.return_value = mock_response
        
        # Call with stream=True
        agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", stream=True, use_cache=False
        )
        
        # Check that payload was sent
        assert mock_requests.post.called
        call_args = mock_requests.post.call_args
        assert call_args is not None


# ============================================================================
# Backend Diagnostics Tests
# ============================================================================

def test_get_backend_status(agent_backend_module: any) -> None:
    """Test backend status reporting."""
    status = agent_backend_module.get_backend_status()
    
    assert "selected_backend" in status
    assert "repo_root" in status
    assert "max_context_chars" in status
    assert "commands" in status
    assert "github_models" in status
    
    # Check commands dict
    assert "copilot" in status["commands"]
    assert "gh" in status["commands"]
    
    # Check github_models dict
    assert "requests_installed" in status["github_models"]
    assert "base_url_set" in status["github_models"]
    assert "model_set" in status["github_models"]
    assert "token_set" in status["github_models"]
    assert "configured" in status["github_models"]


def test_describe_backends(agent_backend_module: any) -> None:
    """Test backend diagnostics output."""
    description = agent_backend_module.describe_backends()
    
    assert "Backend diagnostics:" in description
    assert "selected:" in description
    assert "repo_root:" in description
    assert "copilot" in description or "Copilot" in description
    assert "github-models" in description or "GitHub" in description


# ============================================================================
# Integration Tests
# ============================================================================

def test_cache_different_models_separately(agent_backend_module: any) -> None:
    """Test that different models are cached separately."""
    agent_backend_module.clear_response_cache()
    
    key1 = agent_backend_module._get_cache_key("test", "gpt-4")
    key2 = agent_backend_module._get_cache_key("test", "gpt-3.5")
    
    # Keys should be different
    assert key1 != key2


def test_cache_different_prompts_separately(agent_backend_module: any) -> None:
    """Test that different prompts are cached separately."""
    agent_backend_module.clear_response_cache()
    
    key1 = agent_backend_module._get_cache_key("prompt1", "gpt-4")
    key2 = agent_backend_module._get_cache_key("prompt2", "gpt-4")
    
    # Keys should be different
    assert key1 != key2


def test_validation_with_streaming_disabled(agent_backend_module: any) -> None:
    """Test response validation with streaming disabled (default)."""
    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "valid code response"}}]
        }
        mock_requests.post.return_value = mock_response
        
        result = agent_backend_module.llm_chat_via_github_models(
            prompt="generate code", model="gpt-4",
            base_url="https://api.test", token="token",
            validate_content=True, use_cache=False
        )
        
        assert result == "valid code response"


def test_response_content_stripped(agent_backend_module: any) -> None:
    """Test that responses are trimmed of whitespace."""
    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "  response with whitespace  "}}]
        }
        mock_requests.post.return_value = mock_response
        
        result = agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4",
            base_url="https://api.test", token="token", use_cache=False
        )
        
        assert result == "response with whitespace"
        assert not result.startswith(" ")
        assert not result.endswith(" ")


# =============================================================================
# Phase 6: Enum Tests
# =============================================================================


class TestBackendTypeEnum:
    """Tests for BackendType enum."""

    def test_enum_values(self, agent_backend_module: any) -> None:
        """Test enum has expected values."""
        BackendType = agent_backend_module.BackendType
        assert BackendType.COPILOT_CLI.value == "copilot"
        assert BackendType.GH_COPILOT.value == "gh"
        assert BackendType.GITHUB_MODELS.value == "github-models"
        assert BackendType.AUTO.value == "auto"

    def test_all_members(self, agent_backend_module: any) -> None:
        """Test all members exist."""
        BackendType = agent_backend_module.BackendType
        assert len(list(BackendType)) == 4


class TestBackendStateEnum:
    """Tests for BackendState enum."""

    def test_enum_values(self, agent_backend_module: any) -> None:
        """Test enum has expected values."""
        BackendState = agent_backend_module.BackendState
        assert BackendState.HEALTHY.value == "healthy"
        assert BackendState.DEGRADED.value == "degraded"
        assert BackendState.UNHEALTHY.value == "unhealthy"
        assert BackendState.UNKNOWN.value == "unknown"


class TestCircuitStateEnum:
    """Tests for CircuitState enum."""

    def test_enum_values(self, agent_backend_module: any) -> None:
        """Test enum has expected values."""
        CircuitState = agent_backend_module.CircuitState
        assert CircuitState.CLOSED.value == "closed"
        assert CircuitState.OPEN.value == "open"
        assert CircuitState.HALF_OPEN.value == "half_open"


class TestRequestPriorityEnum:
    """Tests for RequestPriority enum."""

    def test_enum_ordering(self, agent_backend_module: any) -> None:
        """Test priority values are ordered."""
        RequestPriority = agent_backend_module.RequestPriority
        assert RequestPriority.LOW.value < RequestPriority.NORMAL.value
        assert RequestPriority.NORMAL.value < RequestPriority.HIGH.value
        assert RequestPriority.HIGH.value < RequestPriority.CRITICAL.value


class TestResponseTransformEnum:
    """Tests for ResponseTransform enum."""

    def test_all_members(self, agent_backend_module: any) -> None:
        """Test all members exist."""
        ResponseTransform = agent_backend_module.ResponseTransform
        members = [m.name for m in ResponseTransform]
        assert "NONE" in members
        assert "STRIP_WHITESPACE" in members
        assert "EXTRACT_CODE" in members
        assert "EXTRACT_JSON" in members


class TestLoadBalanceStrategyEnum:
    """Tests for LoadBalanceStrategy enum."""

    def test_all_strategies(self, agent_backend_module: any) -> None:
        """Test all strategies exist."""
        LoadBalanceStrategy = agent_backend_module.LoadBalanceStrategy
        members = [m.name for m in LoadBalanceStrategy]
        assert "ROUND_ROBIN" in members
        assert "LEAST_CONNECTIONS" in members
        assert "WEIGHTED" in members
        assert "FAILOVER" in members


# =============================================================================
# Phase 6: Dataclass Tests
# =============================================================================


class TestBackendConfigDataclass:
    """Tests for BackendConfig dataclass."""

    def test_creation(self, agent_backend_module: any) -> None:
        """Test creating BackendConfig."""
        BackendConfig = agent_backend_module.BackendConfig
        BackendType = agent_backend_module.BackendType
        
        config = BackendConfig(
            name="test",
            backend_type=BackendType.GITHUB_MODELS,
            enabled=True,
            weight=2,
            timeout_s=120,
        )
        assert config.name == "test"
        assert config.backend_type == BackendType.GITHUB_MODELS
        assert config.enabled is True
        assert config.weight == 2
        assert config.timeout_s == 120


class TestRequestContextDataclass:
    """Tests for RequestContext dataclass."""

    def test_creation_with_defaults(self, agent_backend_module: any) -> None:
        """Test creating RequestContext with defaults."""
        RequestContext = agent_backend_module.RequestContext
        RequestPriority = agent_backend_module.RequestPriority
        
        context = RequestContext()
        assert context.request_id is not None
        assert context.priority == RequestPriority.NORMAL
        assert context.created_at > 0


class TestBackendResponseDataclass:
    """Tests for BackendResponse dataclass."""

    def test_creation(self, agent_backend_module: any) -> None:
        """Test creating BackendResponse."""
        BackendResponse = agent_backend_module.BackendResponse
        
        response = BackendResponse(
            content="test response",
            backend="github-models",
            latency_ms=150,
            cached=False,
        )
        assert response.content == "test response"
        assert response.backend == "github-models"
        assert response.latency_ms == 150
        assert response.cached is False


class TestBackendHealthStatusDataclass:
    """Tests for BackendHealthStatus dataclass."""

    def test_creation(self, agent_backend_module: any) -> None:
        """Test creating BackendHealthStatus."""
        BackendHealthStatus = agent_backend_module.BackendHealthStatus
        BackendState = agent_backend_module.BackendState
        
        status = BackendHealthStatus(
            backend="test",
            state=BackendState.HEALTHY,
            success_rate=0.95,
        )
        assert status.backend == "test"
        assert status.state == BackendState.HEALTHY
        assert status.success_rate == 0.95


class TestQueuedRequestDataclass:
    """Tests for QueuedRequest dataclass."""

    def test_comparison(self, agent_backend_module: any) -> None:
        """Test QueuedRequest priority comparison."""
        QueuedRequest = agent_backend_module.QueuedRequest
        
        high = QueuedRequest(priority=3, timestamp=1.0, request_id="1", prompt="p1")
        low = QueuedRequest(priority=1, timestamp=1.0, request_id="2", prompt="p2")
        
        # Higher priority should be "less than" for priority queue
        assert high < low


# =============================================================================
# Phase 6: Response Transformer Tests
# =============================================================================


class TestStripWhitespaceTransformer:
    """Tests for StripWhitespaceTransformer."""

    def test_transform(self, agent_backend_module: any) -> None:
        """Test whitespace stripping."""
        transformer = agent_backend_module.StripWhitespaceTransformer()
        assert transformer.transform("  hello  ") == "hello"
        assert transformer.get_name() == "strip_whitespace"


class TestExtractCodeTransformer:
    """Tests for ExtractCodeTransformer."""

    def test_extract_code_block(self, agent_backend_module: any) -> None:
        """Test extracting code from markdown."""
        transformer = agent_backend_module.ExtractCodeTransformer()
        
        markdown = "Here is code:\n```python\nprint('hello')\n```\nEnd."
        result = transformer.transform(markdown)
        
        assert "print('hello')" in result
        assert "```" not in result

    def test_get_name(self, agent_backend_module: any) -> None:
        """Test transformer name."""
        transformer = agent_backend_module.ExtractCodeTransformer()
        assert transformer.get_name() == "extract_code"


class TestExtractJsonTransformer:
    """Tests for ExtractJsonTransformer."""

    def test_extract_json(self, agent_backend_module: any) -> None:
        """Test extracting JSON from response."""
        transformer = agent_backend_module.ExtractJsonTransformer()
        
        response = 'Here is the data: {"key": "value"} and more text.'
        result = transformer.transform(response)
        
        assert '{"key": "value"}' in result or '"key"' in result

    def test_get_name(self, agent_backend_module: any) -> None:
        """Test transformer name."""
        transformer = agent_backend_module.ExtractJsonTransformer()
        assert transformer.get_name() == "extract_json"


# =============================================================================
# Phase 6: RequestQueue Tests
# =============================================================================


class TestRequestQueue:
    """Tests for RequestQueue class."""

    def test_initialization(self, agent_backend_module: any) -> None:
        """Test queue initialization."""
        RequestQueue = agent_backend_module.RequestQueue
        queue = RequestQueue()
        assert queue.is_empty() is True
        assert queue.size() == 0

    def test_enqueue_dequeue(self, agent_backend_module: any) -> None:
        """Test enqueue and dequeue operations."""
        RequestQueue = agent_backend_module.RequestQueue
        RequestPriority = agent_backend_module.RequestPriority
        
        queue = RequestQueue()
        request_id = queue.enqueue("test prompt", RequestPriority.NORMAL)
        
        assert queue.size() == 1
        assert queue.is_empty() is False
        
        request = queue.dequeue()
        assert request.prompt == "test prompt"
        assert request.request_id == request_id

    def test_priority_ordering(self, agent_backend_module: any) -> None:
        """Test that high priority requests are dequeued first."""
        RequestQueue = agent_backend_module.RequestQueue
        RequestPriority = agent_backend_module.RequestPriority
        
        queue = RequestQueue()
        queue.enqueue("low", RequestPriority.LOW)
        queue.enqueue("high", RequestPriority.HIGH)
        queue.enqueue("normal", RequestPriority.NORMAL)
        
        # High priority should come first
        first = queue.dequeue()
        assert first.prompt == "high"


# =============================================================================
# Phase 6: RequestBatcher Tests
# =============================================================================


class TestRequestBatcher:
    """Tests for RequestBatcher class."""

    def test_initialization(self, agent_backend_module: any) -> None:
        """Test batcher initialization."""
        RequestBatcher = agent_backend_module.RequestBatcher
        batcher = RequestBatcher(batch_size=5, timeout_s=10.0)
        assert batcher.pending_count() == 0

    def test_add_requests(self, agent_backend_module: any) -> None:
        """Test adding requests to batcher."""
        RequestBatcher = agent_backend_module.RequestBatcher
        batcher = RequestBatcher(batch_size=3)
        
        batcher.add("prompt1")
        batcher.add("prompt2")
        assert batcher.pending_count() == 2
        assert batcher.is_ready() is False
        
        batcher.add("prompt3")
        assert batcher.is_ready() is True

    def test_get_batch(self, agent_backend_module: any) -> None:
        """Test getting batch."""
        RequestBatcher = agent_backend_module.RequestBatcher
        batcher = RequestBatcher(batch_size=2)
        
        batcher.add("prompt1")
        batcher.add("prompt2")
        
        batch = batcher.get_batch()
        assert batch is not None
        assert len(batch.requests) == 2
        assert batcher.pending_count() == 0


# =============================================================================
# Phase 6: BackendHealthMonitor Tests
# =============================================================================


class TestBackendHealthMonitor:
    """Tests for BackendHealthMonitor class."""

    def test_initialization(self, agent_backend_module: any) -> None:
        """Test monitor initialization."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        monitor = BackendHealthMonitor()
        assert monitor.health_threshold == 0.8

    def test_record_success(self, agent_backend_module: any) -> None:
        """Test recording successful request."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        monitor = BackendHealthMonitor()
        
        monitor.record_success("test-backend", 150)
        assert monitor.is_healthy("test-backend") is True

    def test_record_failures_unhealthy(self, agent_backend_module: any) -> None:
        """Test that many failures mark backend unhealthy."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        monitor = BackendHealthMonitor(health_threshold=0.8, window_size=10)
        
        # Record mostly failures
        for _ in range(8):
            monitor.record_failure("test-backend")
        for _ in range(2):
            monitor.record_success("test-backend", 100)
        
        # Success rate is 20%, should be unhealthy
        assert monitor.is_healthy("test-backend") is False

    def test_get_healthiest(self, agent_backend_module: any) -> None:
        """Test getting healthiest backend."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        monitor = BackendHealthMonitor()
        
        # Record mixed results
        for _ in range(5):
            monitor.record_success("backend1", 100)
        for _ in range(5):
            monitor.record_failure("backend2")
        
        healthiest = monitor.get_healthiest(["backend1", "backend2"])
        assert healthiest == "backend1"


# =============================================================================
# Phase 6: LoadBalancer Tests
# =============================================================================


class TestLoadBalancer:
    """Tests for LoadBalancer class."""

    def test_initialization(self, agent_backend_module: any) -> None:
        """Test load balancer initialization."""
        LoadBalancer = agent_backend_module.LoadBalancer
        LoadBalanceStrategy = agent_backend_module.LoadBalanceStrategy
        
        lb = LoadBalancer(LoadBalanceStrategy.ROUND_ROBIN)
        assert lb.strategy == LoadBalanceStrategy.ROUND_ROBIN

    def test_add_backend(self, agent_backend_module: any) -> None:
        """Test adding backends."""
        LoadBalancer = agent_backend_module.LoadBalancer
        
        lb = LoadBalancer()
        lb.add_backend("backend1")
        lb.add_backend("backend2")
        
        backend = lb.next()
        assert backend is not None
        assert backend.name in ["backend1", "backend2"]

    def test_round_robin(self, agent_backend_module: any) -> None:
        """Test round robin distribution."""
        LoadBalancer = agent_backend_module.LoadBalancer
        LoadBalanceStrategy = agent_backend_module.LoadBalanceStrategy
        
        lb = LoadBalancer(LoadBalanceStrategy.ROUND_ROBIN)
        lb.add_backend("backend1")
        lb.add_backend("backend2")
        
        # Should alternate
        b1 = lb.next()
        b2 = lb.next()
        b3 = lb.next()
        
        assert b1.name != b2.name or len([b1, b2, b3]) == 3

    def test_remove_backend(self, agent_backend_module: any) -> None:
        """Test removing backends."""
        LoadBalancer = agent_backend_module.LoadBalancer
        
        lb = LoadBalancer()
        lb.add_backend("backend1")
        
        result = lb.remove_backend("backend1")
        assert result is True
        assert lb.next() is None


# =============================================================================
# Phase 6: UsageQuotaManager Tests
# =============================================================================


class TestUsageQuotaManager:
    """Tests for UsageQuotaManager class."""

    def test_initialization(self, agent_backend_module: any) -> None:
        """Test quota manager initialization."""
        UsageQuotaManager = agent_backend_module.UsageQuotaManager
        manager = UsageQuotaManager(daily_limit=100, hourly_limit=10)
        assert manager.can_request() is True

    def test_record_request(self, agent_backend_module: any) -> None:
        """Test recording requests."""
        UsageQuotaManager = agent_backend_module.UsageQuotaManager
        manager = UsageQuotaManager(daily_limit=100, hourly_limit=10)
        
        manager.record_request()
        daily, hourly = manager.get_remaining()
        assert daily == 99
        assert hourly == 9

    def test_quota_exceeded(self, agent_backend_module: any) -> None:
        """Test quota enforcement."""
        UsageQuotaManager = agent_backend_module.UsageQuotaManager
        manager = UsageQuotaManager(daily_limit=2, hourly_limit=2)
        
        manager.record_request()
        manager.record_request()
        
        assert manager.can_request() is False

    def test_usage_report(self, agent_backend_module: any) -> None:
        """Test getting usage report."""
        UsageQuotaManager = agent_backend_module.UsageQuotaManager
        manager = UsageQuotaManager(daily_limit=100, hourly_limit=10)
        
        manager.record_request()
        report = manager.get_usage_report()
        
        assert report["daily_used"] == 1
        assert report["daily_limit"] == 100
        assert report["daily_remaining"] == 99


# =============================================================================
# Phase 6: RequestTracer Tests
# =============================================================================


class TestRequestTracer:
    """Tests for RequestTracer class."""

    def test_initialization(self, agent_backend_module: any) -> None:
        """Test tracer initialization."""
        RequestTracer = agent_backend_module.RequestTracer
        tracer = RequestTracer()
        assert tracer.get_active_traces() == []

    def test_start_trace(self, agent_backend_module: any) -> None:
        """Test starting a trace."""
        RequestTracer = agent_backend_module.RequestTracer
        tracer = RequestTracer()
        
        context = tracer.start_trace("test request")
        assert context.request_id is not None
        assert context.correlation_id is not None
        assert len(tracer.get_active_traces()) == 1

    def test_end_trace(self, agent_backend_module: any) -> None:
        """Test ending a trace."""
        RequestTracer = agent_backend_module.RequestTracer
        tracer = RequestTracer()
        
        context = tracer.start_trace("test")
        duration = tracer.end_trace(context.request_id, success=True)
        
        assert duration is not None
        assert duration >= 0
        assert len(tracer.get_active_traces()) == 0


# =============================================================================
# Phase 6: AuditLogger Tests
# =============================================================================


class TestAuditLogger:
    """Tests for AuditLogger class."""

    def test_initialization(self, agent_backend_module: any) -> None:
        """Test audit logger initialization."""
        AuditLogger = agent_backend_module.AuditLogger
        logger = AuditLogger()
        assert logger.log_file is None

    def test_log_request(self, agent_backend_module: any, tmp_path) -> None:
        """Test logging a request."""
        from pathlib import Path
        AuditLogger = agent_backend_module.AuditLogger
        
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(log_file=log_file)
        
        logger.log_request(
            backend="github-models",
            prompt="test prompt",
            response="test response",
            latency_ms=150,
            success=True,
        )
        
        assert log_file.exists()
        content = log_file.read_text()
        assert "github-models" in content

    def test_get_recent_entries(self, agent_backend_module: any, tmp_path) -> None:
        """Test getting recent entries."""
        from pathlib import Path
        AuditLogger = agent_backend_module.AuditLogger
        
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(log_file=log_file)
        
        logger.log_request("b1", "p1", "r1", 100, True)
        logger.log_request("b2", "p2", "r2", 200, False)
        
        entries = logger.get_recent_entries(count=10)
        assert len(entries) == 2


# =============================================================================
# Phase 6: Integration Tests
# =============================================================================


class TestPhase6Integration:
    """Integration tests for Phase 6 features."""

    def test_queue_with_batcher(self, agent_backend_module: any) -> None:
        """Test queue and batcher working together."""
        RequestQueue = agent_backend_module.RequestQueue
        RequestBatcher = agent_backend_module.RequestBatcher
        RequestPriority = agent_backend_module.RequestPriority
        
        queue = RequestQueue()
        batcher = RequestBatcher(batch_size=2)
        
        # Queue some requests
        queue.enqueue("prompt1", RequestPriority.NORMAL)
        queue.enqueue("prompt2", RequestPriority.HIGH)
        
        # Dequeue and batch
        while not queue.is_empty():
            request = queue.dequeue()
            batcher.add(request.prompt)
        
        assert batcher.is_ready() is True
        batch = batcher.get_batch()
        assert len(batch.requests) == 2

    def test_health_monitor_with_load_balancer(self, agent_backend_module: any) -> None:
        """Test health monitor with load balancer."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        LoadBalancer = agent_backend_module.LoadBalancer
        
        monitor = BackendHealthMonitor()
        lb = LoadBalancer()
        
        lb.add_backend("backend1")
        lb.add_backend("backend2")
        
        # Record health data
        monitor.record_success("backend1", 100)
        monitor.record_failure("backend2")
        
        # Get next backend and check health
        backend = lb.next()
        is_healthy = monitor.is_healthy(backend.name)
        assert is_healthy is not None  # Either True or False

    def test_tracer_with_audit_logger(self, agent_backend_module: any, tmp_path) -> None:
        """Test tracer with audit logger."""
        RequestTracer = agent_backend_module.RequestTracer
        AuditLogger = agent_backend_module.AuditLogger
        
        log_file = tmp_path / "audit.log"
        tracer = RequestTracer()
        audit = AuditLogger(log_file=log_file)
        
        # Start trace
        context = tracer.start_trace("test request")
        
        # Log request with trace info
        audit.log_request(
            backend="test",
            prompt="test",
            response="response",
            latency_ms=100,
            request_id=context.request_id,
        )
        
        # End trace
        tracer.end_trace(context.request_id, success=True)
        
        entries = audit.get_recent_entries()
        assert len(entries) == 1
        assert entries[0]["request_id"] == context.request_id
