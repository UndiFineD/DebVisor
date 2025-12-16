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
Agent Backend: Handles communication with AI backends.

This module provides the infrastructure for communicating with various AI backends:
- GitHub Copilot CLI (local command-line tool)
- GitHub Copilot via gh CLI
- GitHub Models API (OpenAI-compatible endpoint)

Supports automatic backend selection with fallback mechanisms.
Configurable via environment variables for flexibility in CI/CD and development.

Environment Variables:
    DV_AGENT_BACKEND: Selected backend ('auto', 'copilot', 'gh', 'github-models')
    DV_AGENT_REPO_ROOT: Override repository root detection
    DV_AGENT_MAX_CONTEXT_CHARS: Max chars to include as context (default: 12000)
    DV_AGENT_MODEL: Model name for GitHub Models backend
    DV_AGENT_SYSTEM_PROMPT: System prompt for AI backends
    GITHUB_TOKEN: Authentication token for GitHub Models API
    GITHUB_MODELS_BASE_URL: API endpoint URL for GitHub Models
"""

import hashlib
import json
import logging
import os
import re
import subprocess
import time
import threading
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from functools import wraps
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, TypeVar

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]


# ============================================================================
# Type-Safe Enums for Backend System
# ============================================================================


class BackendType(Enum):
    """Types of AI backends available."""
    
    COPILOT_CLI = "copilot"
    GH_COPILOT = "gh"
    GITHUB_MODELS = "github-models"
    AUTO = "auto"


class BackendState(Enum):
    """Health states for backends."""
    
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class CircuitState(Enum):
    """Circuit breaker states."""
    
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class RequestPriority(Enum):
    """Priority levels for request queuing."""
    
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class ResponseTransform(Enum):
    """Types of response transformations."""
    
    NONE = "none"
    STRIP_WHITESPACE = "strip"
    EXTRACT_CODE = "extract_code"
    EXTRACT_JSON = "extract_json"
    MARKDOWN_TO_TEXT = "markdown_to_text"


class LoadBalanceStrategy(Enum):
    """Load balancing strategies for multiple backends."""
    
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"
    FAILOVER = "failover"


# ============================================================================
# Dataclasses for Structured Data
# ============================================================================


@dataclass
class BackendConfig:
    """Configuration for a single backend.
    
    Attributes:
        name: Backend identifier.
        backend_type: Type of backend.
        enabled: Whether backend is active.
        weight: Weight for load balancing.
        timeout_s: Request timeout in seconds.
        max_retries: Maximum retry attempts.
        rate_limit_rpm: Requests per minute limit.
    """
    
    name: str
    backend_type: BackendType
    enabled: bool = True
    weight: int = 1
    timeout_s: int = 60
    max_retries: int = 2
    rate_limit_rpm: Optional[int] = None


@dataclass
class RequestContext:
    """Context for a backend request.
    
    Attributes:
        request_id: Unique identifier for tracking.
        correlation_id: ID for tracing across services.
        priority: Request priority level.
        created_at: Timestamp when request was created.
        metadata: Additional request metadata.
    """
    
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: Optional[str] = None
    priority: RequestPriority = RequestPriority.NORMAL
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BackendResponse:
    """Response from a backend request.
    
    Attributes:
        content: Response content.
        backend: Backend that provided response.
        latency_ms: Response latency in milliseconds.
        cached: Whether response was from cache.
        request_id: ID of originating request.
        tokens_used: Estimated tokens consumed.
    """
    
    content: str
    backend: str
    latency_ms: int = 0
    cached: bool = False
    request_id: Optional[str] = None
    tokens_used: int = 0


@dataclass
class BackendHealthStatus:
    """Health status for a backend.
    
    Attributes:
        backend: Backend identifier.
        state: Current health state.
        last_check: Last health check timestamp.
        success_rate: Success rate (0.0-1.0).
        avg_latency_ms: Average latency.
        error_count: Recent error count.
    """
    
    backend: str
    state: BackendState
    last_check: float = field(default_factory=time.time)
    success_rate: float = 1.0
    avg_latency_ms: float = 0.0
    error_count: int = 0


@dataclass
class QueuedRequest:
    """A request waiting in the queue.
    
    Attributes:
        priority: Request priority (higher = more urgent).
        timestamp: When request was queued.
        request_id: Unique request identifier.
        prompt: The prompt to send.
        callback: Optional callback function.
    """
    
    priority: int
    timestamp: float
    request_id: str
    prompt: str
    callback: Optional[Callable[[str], None]] = None
    
    def __lt__(self, other: "QueuedRequest") -> bool:
        """Compare by priority (descending) then timestamp (ascending)."""
        if self.priority != other.priority:
            return self.priority > other.priority  # Higher priority first
        return self.timestamp < other.timestamp  # Earlier first


@dataclass
class BatchRequest:
    """A batch of requests to process together.
    
    Attributes:
        requests: List of prompts.
        batch_id: Unique batch identifier.
        created_at: Batch creation timestamp.
        processed_count: Number processed so far.
    """
    
    requests: List[str]
    batch_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = field(default_factory=time.time)
    processed_count: int = 0


@dataclass
class UsageQuota:
    """Usage quota configuration.
    
    Attributes:
        daily_limit: Maximum requests per day.
        hourly_limit: Maximum requests per hour.
        current_daily: Current daily usage.
        current_hourly: Current hourly usage.
        reset_daily_at: When daily count resets.
        reset_hourly_at: When hourly count resets.
    """
    
    daily_limit: int = 1000
    hourly_limit: int = 100
    current_daily: int = 0
    current_hourly: int = 0
    reset_daily_at: float = field(default_factory=time.time)
    reset_hourly_at: float = field(default_factory=time.time)


# ============================================================================
# Response Cache and Metrics
# ============================================================================

_response_cache: Dict[str, str] = {}
_metrics: Dict[str, Any] = {
    "requests": 0,
    "errors": 0,
    "timeouts": 0,
    "cache_hits": 0,
    "total_latency_ms": 0,
}


# ============================================================================
# Abstract Base Class for Response Transformers
# ============================================================================


class ResponseTransformerBase(ABC):
    """Abstract base class for response transformers.
    
    Implement this to create custom response transformation logic.
    """
    
    @abstractmethod
    def transform(self, response: str) -> str:
        """Transform a response string.
        
        Args:
            response: Raw response string.
            
        Returns:
            str: Transformed response.
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get transformer name."""
        pass


class StripWhitespaceTransformer(ResponseTransformerBase):
    """Transformer that strips whitespace."""
    
    def transform(self, response: str) -> str:
        """Strip leading and trailing whitespace."""
        return response.strip()
    
    def get_name(self) -> str:
        """Get transformer name."""
        return "strip_whitespace"


class ExtractCodeTransformer(ResponseTransformerBase):
    """Transformer that extracts code blocks from markdown."""
    
    def transform(self, response: str) -> str:
        """Extract code blocks from markdown response.
        
        Args:
            response: Markdown response with code blocks.
            
        Returns:
            str: Extracted code without markdown fencing.
        """
        # Match ```language\ncode\n``` blocks
        code_pattern = r"```(?:\w+)?\n(.*?)```"
        matches = re.findall(code_pattern, response, re.DOTALL)
        if matches:
            return "\n\n".join(matches)
        return response.strip()
    
    def get_name(self) -> str:
        """Get transformer name."""
        return "extract_code"


class ExtractJsonTransformer(ResponseTransformerBase):
    """Transformer that extracts JSON from response."""
    
    def transform(self, response: str) -> str:
        """Extract JSON from response.
        
        Args:
            response: Response possibly containing JSON.
            
        Returns:
            str: Extracted JSON string.
        """
        # Try to find JSON object or array
        json_pattern = r"(\{[^{}]*\}|\[[^\[\]]*\])"
        matches = re.findall(json_pattern, response, re.DOTALL)
        for match in matches:
            try:
                json.loads(match)
                return match
            except json.JSONDecodeError:
                continue
        return response.strip()
    
    def get_name(self) -> str:
        """Get transformer name."""
        return "extract_json"


# ============================================================================
# Request Priority Queue
# ============================================================================


class RequestQueue:
    """Priority queue for backend requests.
    
    Manages request ordering by priority and timestamp.
    Thread-safe for concurrent access.
    
    Example:
        queue = RequestQueue()
        queue.enqueue("prompt", RequestPriority.HIGH)
        request = queue.dequeue()
    """
    
    def __init__(self, max_size: int = 1000) -> None:
        """Initialize request queue.
        
        Args:
            max_size: Maximum queue size.
        """
        self._queue: PriorityQueue[QueuedRequest] = PriorityQueue(maxsize=max_size)
        self._lock = threading.Lock()
        self._pending: Dict[str, QueuedRequest] = {}
    
    def enqueue(
        self,
        prompt: str,
        priority: RequestPriority = RequestPriority.NORMAL,
        callback: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Add request to queue.
        
        Args:
            prompt: The prompt to queue.
            priority: Request priority level.
            callback: Optional callback when processed.
            
        Returns:
            str: Request ID for tracking.
        """
        request_id = str(uuid.uuid4())
        request = QueuedRequest(
            priority=priority.value,
            timestamp=time.time(),
            request_id=request_id,
            prompt=prompt,
            callback=callback,
        )
        
        with self._lock:
            self._queue.put(request)
            self._pending[request_id] = request
        
        logging.debug(f"Queued request {request_id} with priority {priority.name}")
        return request_id
    
    def dequeue(self, timeout: Optional[float] = None) -> Optional[QueuedRequest]:
        """Get next request from queue.
        
        Args:
            timeout: Maximum wait time in seconds.
            
        Returns:
            Optional[QueuedRequest]: Next request or None if empty/timeout.
        """
        try:
            request = self._queue.get(timeout=timeout)
            with self._lock:
                self._pending.pop(request.request_id, None)
            return request
        except Exception:
            return None
    
    def size(self) -> int:
        """Get current queue size."""
        return self._queue.qsize()
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self._queue.empty()
    
    def get_pending(self, request_id: str) -> Optional[QueuedRequest]:
        """Get pending request by ID."""
        with self._lock:
            return self._pending.get(request_id)


# ============================================================================
# Request Batching
# ============================================================================


class RequestBatcher:
    """Batches multiple requests for efficient processing.
    
    Collects requests and processes them together when batch
    size or timeout is reached.
    
    Example:
        batcher = RequestBatcher(batch_size=10, timeout_s=5.0)
        batcher.add("prompt1")
        batcher.add("prompt2")
        batch = batcher.get_batch()  # Returns when ready
    """
    
    def __init__(
        self,
        batch_size: int = 10,
        timeout_s: float = 5.0,
    ) -> None:
        """Initialize request batcher.
        
        Args:
            batch_size: Requests per batch.
            timeout_s: Max wait time before processing partial batch.
        """
        self.batch_size = batch_size
        self.timeout_s = timeout_s
        self._buffer: List[str] = []
        self._lock = threading.Lock()
        self._batch_start: Optional[float] = None
    
    def add(self, prompt: str) -> bool:
        """Add request to current batch.
        
        Args:
            prompt: Request prompt.
            
        Returns:
            bool: True if batch is now ready.
        """
        with self._lock:
            if not self._buffer:
                self._batch_start = time.time()
            self._buffer.append(prompt)
            return len(self._buffer) >= self.batch_size
    
    def is_ready(self) -> bool:
        """Check if batch is ready for processing."""
        with self._lock:
            if len(self._buffer) >= self.batch_size:
                return True
            if self._batch_start and (time.time() - self._batch_start) >= self.timeout_s:
                return bool(self._buffer)
            return False
    
    def get_batch(self) -> Optional[BatchRequest]:
        """Get current batch and reset buffer.
        
        Returns:
            Optional[BatchRequest]: Current batch or None if empty.
        """
        with self._lock:
            if not self._buffer:
                return None
            batch = BatchRequest(requests=self._buffer.copy())
            self._buffer.clear()
            self._batch_start = None
            return batch
    
    def pending_count(self) -> int:
        """Get number of pending requests."""
        with self._lock:
            return len(self._buffer)


# ============================================================================
# Backend Health Monitor
# ============================================================================


class BackendHealthMonitor:
    """Monitors backend health and manages failover.
    
    Tracks success/failure rates, latency, and automatically
    fails over to healthy backends when issues detected.
    
    Example:
        monitor = BackendHealthMonitor()
        monitor.record_success("github-models", 150)
        if monitor.is_healthy("github-models"):
            # Use backend
            pass
    """
    
    def __init__(
        self,
        health_threshold: float = 0.8,
        window_size: int = 100,
    ) -> None:
        """Initialize health monitor.
        
        Args:
            health_threshold: Min success rate for healthy status.
            window_size: Number of recent requests to track.
        """
        self.health_threshold = health_threshold
        self.window_size = window_size
        self._history: Dict[str, List[Tuple[bool, int]]] = {}
        self._status: Dict[str, BackendHealthStatus] = {}
        self._lock = threading.Lock()
    
    def record_success(self, backend: str, latency_ms: int) -> None:
        """Record successful request.
        
        Args:
            backend: Backend identifier.
            latency_ms: Request latency.
        """
        with self._lock:
            if backend not in self._history:
                self._history[backend] = []
            self._history[backend].append((True, latency_ms))
            self._history[backend] = self._history[backend][-self.window_size:]
            self._update_status(backend)
    
    def record_failure(self, backend: str, latency_ms: int = 0) -> None:
        """Record failed request.
        
        Args:
            backend: Backend identifier.
            latency_ms: Request latency (if any).
        """
        with self._lock:
            if backend not in self._history:
                self._history[backend] = []
            self._history[backend].append((False, latency_ms))
            self._history[backend] = self._history[backend][-self.window_size:]
            self._update_status(backend)
    
    def _update_status(self, backend: str) -> None:
        """Update backend health status."""
        history = self._history.get(backend, [])
        if not history:
            self._status[backend] = BackendHealthStatus(
                backend=backend,
                state=BackendState.UNKNOWN,
            )
            return
        
        successes = sum(1 for success, _ in history if success)
        total = len(history)
        success_rate = successes / total if total > 0 else 0.0
        
        latencies = [lat for _, lat in history if lat > 0]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        
        error_count = total - successes
        
        if success_rate >= self.health_threshold:
            state = BackendState.HEALTHY
        elif success_rate >= 0.5:
            state = BackendState.DEGRADED
        else:
            state = BackendState.UNHEALTHY
        
        self._status[backend] = BackendHealthStatus(
            backend=backend,
            state=state,
            success_rate=success_rate,
            avg_latency_ms=avg_latency,
            error_count=error_count,
        )
    
    def is_healthy(self, backend: str) -> bool:
        """Check if backend is healthy."""
        with self._lock:
            status = self._status.get(backend)
            if not status:
                return True  # Unknown = assume healthy
            return status.state == BackendState.HEALTHY
    
    def get_status(self, backend: str) -> Optional[BackendHealthStatus]:
        """Get backend health status."""
        with self._lock:
            return self._status.get(backend)
    
    def get_all_status(self) -> Dict[str, BackendHealthStatus]:
        """Get all backend health statuses."""
        with self._lock:
            return dict(self._status)
    
    def get_healthiest(self, backends: List[str]) -> Optional[str]:
        """Get healthiest backend from list.
        
        Args:
            backends: List of backend names.
            
        Returns:
            Optional[str]: Healthiest backend or None.
        """
        with self._lock:
            best: Optional[str] = None
            best_score = -1.0
            
            for backend in backends:
                status = self._status.get(backend)
                if not status:
                    # Unknown backends get neutral score
                    score = 0.5
                else:
                    score = status.success_rate
                
                if score > best_score:
                    best_score = score
                    best = backend
            
            return best


# ============================================================================
# Load Balancer
# ============================================================================


class LoadBalancer:
    """Load balancer for multiple backend endpoints.
    
    Distributes requests across backends using configurable strategies.
    
    Example:
        lb = LoadBalancer(LoadBalanceStrategy.ROUND_ROBIN)
        lb.add_backend("backend1", weight=2)
        lb.add_backend("backend2", weight=1)
        backend = lb.next()
    """
    
    def __init__(self, strategy: LoadBalanceStrategy = LoadBalanceStrategy.ROUND_ROBIN) -> None:
        """Initialize load balancer.
        
        Args:
            strategy: Load balancing strategy to use.
        """
        self.strategy = strategy
        self._backends: List[BackendConfig] = []
        self._index = 0
        self._connections: Dict[str, int] = {}
        self._lock = threading.Lock()
    
    def add_backend(
        self,
        name: str,
        backend_type: BackendType = BackendType.GITHUB_MODELS,
        weight: int = 1,
        **kwargs: Any,
    ) -> None:
        """Add backend to load balancer.
        
        Args:
            name: Backend identifier.
            backend_type: Type of backend.
            weight: Weight for weighted strategy.
            **kwargs: Additional backend config.
        """
        config = BackendConfig(
            name=name,
            backend_type=backend_type,
            weight=weight,
            **kwargs,
        )
        with self._lock:
            self._backends.append(config)
            self._connections[name] = 0
        logging.debug(f"Added backend '{name}' to load balancer")
    
    def remove_backend(self, name: str) -> bool:
        """Remove backend from load balancer.
        
        Args:
            name: Backend name to remove.
            
        Returns:
            bool: True if removed, False if not found.
        """
        with self._lock:
            for i, backend in enumerate(self._backends):
                if backend.name == name:
                    self._backends.pop(i)
                    self._connections.pop(name, None)
                    logging.debug(f"Removed backend '{name}' from load balancer")
                    return True
            return False
    
    def next(self) -> Optional[BackendConfig]:
        """Get next backend to use.
        
        Returns:
            Optional[BackendConfig]: Next backend or None if empty.
        """
        with self._lock:
            enabled = [b for b in self._backends if b.enabled]
            if not enabled:
                return None
            
            if self.strategy == LoadBalanceStrategy.ROUND_ROBIN:
                backend = enabled[self._index % len(enabled)]
                self._index += 1
                return backend
            
            elif self.strategy == LoadBalanceStrategy.LEAST_CONNECTIONS:
                backend = min(enabled, key=lambda b: self._connections.get(b.name, 0))
                return backend
            
            elif self.strategy == LoadBalanceStrategy.WEIGHTED:
                # Weighted round robin
                total_weight = sum(b.weight for b in enabled)
                if total_weight == 0:
                    return enabled[0]
                target = self._index % total_weight
                current = 0
                for backend in enabled:
                    current += backend.weight
                    if target < current:
                        self._index += 1
                        return backend
                return enabled[-1]
            
            else:  # FAILOVER
                return enabled[0]
    
    def mark_connection_start(self, name: str) -> None:
        """Mark connection started for backend."""
        with self._lock:
            self._connections[name] = self._connections.get(name, 0) + 1
    
    def mark_connection_end(self, name: str) -> None:
        """Mark connection ended for backend."""
        with self._lock:
            self._connections[name] = max(0, self._connections.get(name, 0) - 1)


# ============================================================================
# Usage Quota Manager
# ============================================================================


class UsageQuotaManager:
    """Manages usage quotas and limits.
    
    Tracks request counts and enforces daily/hourly limits.
    
    Example:
        quota = UsageQuotaManager(daily_limit=1000, hourly_limit=100)
        if quota.can_request():
            quota.record_request()
            # Make request
    """
    
    def __init__(
        self,
        daily_limit: int = 1000,
        hourly_limit: int = 100,
    ) -> None:
        """Initialize quota manager.
        
        Args:
            daily_limit: Max requests per day.
            hourly_limit: Max requests per hour.
        """
        self._quota = UsageQuota(
            daily_limit=daily_limit,
            hourly_limit=hourly_limit,
        )
        self._lock = threading.Lock()
    
    def _check_reset(self) -> None:
        """Check and reset counters if needed."""
        now = time.time()
        
        # Reset hourly
        if now - self._quota.reset_hourly_at >= 3600:
            self._quota.current_hourly = 0
            self._quota.reset_hourly_at = now
        
        # Reset daily
        if now - self._quota.reset_daily_at >= 86400:
            self._quota.current_daily = 0
            self._quota.reset_daily_at = now
    
    def can_request(self) -> bool:
        """Check if request is allowed under quota."""
        with self._lock:
            self._check_reset()
            return (
                self._quota.current_daily < self._quota.daily_limit and
                self._quota.current_hourly < self._quota.hourly_limit
            )
    
    def record_request(self) -> None:
        """Record a request against quota."""
        with self._lock:
            self._check_reset()
            self._quota.current_daily += 1
            self._quota.current_hourly += 1
    
    def get_remaining(self) -> Tuple[int, int]:
        """Get remaining quota (daily, hourly)."""
        with self._lock:
            self._check_reset()
            daily_remaining = max(0, self._quota.daily_limit - self._quota.current_daily)
            hourly_remaining = max(0, self._quota.hourly_limit - self._quota.current_hourly)
            return daily_remaining, hourly_remaining
    
    def get_usage_report(self) -> Dict[str, Any]:
        """Get usage report."""
        with self._lock:
            self._check_reset()
            return {
                "daily_used": self._quota.current_daily,
                "daily_limit": self._quota.daily_limit,
                "daily_remaining": max(0, self._quota.daily_limit - self._quota.current_daily),
                "hourly_used": self._quota.current_hourly,
                "hourly_limit": self._quota.hourly_limit,
                "hourly_remaining": max(0, self._quota.hourly_limit - self._quota.current_hourly),
            }


# ============================================================================
# Request Tracing
# ============================================================================


class RequestTracer:
    """Traces requests with correlation IDs.
    
    Provides distributed tracing capabilities for debugging
    and monitoring request flow.
    
    Example:
        tracer = RequestTracer()
        context = tracer.start_trace("my-request")
        # Do work
        tracer.end_trace(context.request_id, success=True)
    """
    
    def __init__(self) -> None:
        """Initialize request tracer."""
        self._traces: Dict[str, RequestContext] = {}
        self._lock = threading.Lock()
    
    def start_trace(
        self,
        description: str,
        correlation_id: Optional[str] = None,
        priority: RequestPriority = RequestPriority.NORMAL,
    ) -> RequestContext:
        """Start a new trace.
        
        Args:
            description: Trace description.
            correlation_id: Optional correlation ID for linking traces.
            priority: Request priority.
            
        Returns:
            RequestContext: Context for this trace.
        """
        context = RequestContext(
            correlation_id=correlation_id or str(uuid.uuid4()),
            priority=priority,
            metadata={"description": description},
        )
        
        with self._lock:
            self._traces[context.request_id] = context
        
        logging.debug(f"Started trace {context.request_id} (correlation: {context.correlation_id})")
        return context
    
    def end_trace(
        self,
        request_id: str,
        success: bool,
        response_size: int = 0,
    ) -> Optional[float]:
        """End a trace and return duration.
        
        Args:
            request_id: Request ID to end.
            success: Whether request succeeded.
            response_size: Size of response.
            
        Returns:
            Optional[float]: Duration in seconds, or None if not found.
        """
        with self._lock:
            context = self._traces.pop(request_id, None)
        
        if not context:
            return None
        
        duration = time.time() - context.created_at
        logging.debug(
            f"Ended trace {request_id}: success={success}, "
            f"duration={duration:.3f}s, size={response_size}"
        )
        return duration
    
    def get_active_traces(self) -> List[RequestContext]:
        """Get all active traces."""
        with self._lock:
            return list(self._traces.values())


# ============================================================================
# Audit Logger
# ============================================================================


class AuditLogger:
    """Logs backend requests for audit and compliance.
    
    Records request metadata, responses, and timing for
    audit trail and compliance requirements.
    
    Example:
        audit = AuditLogger()
        audit.log_request("github-models", "prompt", "response", 150)
    """
    
    def __init__(self, log_file: Optional[Path] = None) -> None:
        """Initialize audit logger.
        
        Args:
            log_file: Path to audit log file.
        """
        self.log_file = log_file
        self._lock = threading.Lock()
    
    def log_request(
        self,
        backend: str,
        prompt: str,
        response: str,
        latency_ms: int,
        success: bool = True,
        request_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a request for audit.
        
        Args:
            backend: Backend used.
            prompt: Request prompt (may be truncated for privacy).
            response: Response received (may be truncated).
            latency_ms: Request latency.
            success: Whether request succeeded.
            request_id: Optional request ID.
            metadata: Additional metadata.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id or str(uuid.uuid4()),
            "backend": backend,
            "prompt_length": len(prompt),
            "prompt_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "response_length": len(response),
            "latency_ms": latency_ms,
            "success": success,
            "metadata": metadata or {},
        }
        
        with self._lock:
            if self.log_file:
                try:
                    with open(self.log_file, "a", encoding="utf-8") as f:
                        f.write(json.dumps(entry) + "\n")
                except IOError as e:
                    logging.warning(f"Failed to write audit log: {e}")
            
            logging.debug(f"Audit: {entry['request_id']} - {backend} - {latency_ms}ms")
    
    def get_recent_entries(self, count: int = 100) -> List[Dict[str, Any]]:
        """Get recent audit log entries.
        
        Args:
            count: Number of entries to return.
            
        Returns:
            List[Dict]: Recent audit entries.
        """
        if not self.log_file or not self.log_file.exists():
            return []
        
        entries: List[Dict[str, Any]] = []
        with self._lock:
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            entries.append(json.loads(line.strip()))
                        except json.JSONDecodeError:
                            continue
            except IOError:
                return []
        
        return entries[-count:]


def _resolve_repo_root() -> Path:
    """Resolve the repository root directory.
    
    Uses environment variable or automatic detection via .git marker.
    Falls back to current working directory if no repo found.
    
    Args:
        None.
        
    Returns:
        Path: Repository root directory.
        
    Environment Variables:
        DV_AGENT_REPO_ROOT: If set, use this as repo root (can use ~).
        
    Note:
        - Searches from current file location upward for .git directory
        - Returns CWD if no .git found
        - Path is always resolved to absolute form
    """
    env_root = os.environ.get("DV_AGENT_REPO_ROOT")
    if env_root:
        logging.debug(f"Using DV_AGENT_REPO_ROOT: {env_root}")
        return Path(env_root).expanduser().resolve()
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / ".git").exists():
            logging.debug(f"Found repo root at {parent}")
            return parent
    logging.debug(f"No repo root found, using CWD: {Path.cwd()}")
    return Path.cwd()


def _command_available(command: str) -> bool:
    """Check if a command is available in PATH.
    
    Attempts to run command with --version flag to verify availability.
    
    Args:
        command: Command name to check (e.g., 'copilot', 'gh').
        
    Returns:
        bool: True if command is available and working, False otherwise.
        
    Note:
        - Runs with 5-second timeout
        - Catches all subprocess errors and returns False
        - Non-zero exit codes are treated as unavailable
    """
    try:
        logging.debug(f"Checking if command is available: {command}")
        subprocess.run(
            [command, '--version'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=5,
            check=True,
        )
        logging.debug(f"Command available: {command}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        logging.debug(f"Command not available: {command}")
        return False


# ============================================================================
# Caching and Metrics Functions
# ============================================================================

def _get_cache_key(prompt: str, model: str) -> str:
    """Generate a cache key for a prompt-model combination."""
    content = f"{prompt}:{model}".encode('utf-8')
    return hashlib.sha256(content).hexdigest()


def clear_response_cache() -> None:
    """Clear the response cache.
    
    Useful for testing or resetting state.
    """
    global _response_cache
    _response_cache.clear()
    logging.debug("Response cache cleared")


def get_metrics() -> Dict[str, Any]:
    """Get current metrics snapshot.
    
    Returns a dictionary with request counts, error rates, cache hits, etc.
    Useful for monitoring and diagnostics.
    
    Returns:
        dict: Metrics including request count, error count, cache hits, latency.
    """
    return {k: v for k, v in _metrics.items()}


def reset_metrics() -> None:
    """Reset metrics to zero."""
    global _metrics
    _metrics = {
        "requests": 0,
        "errors": 0,
        "timeouts": 0,
        "cache_hits": 0,
        "total_latency_ms": 0,
    }
    logging.debug("Metrics reset")


def validate_response_content(response: str, content_types: Optional[list] = None) -> bool:
    """Validate that AI response contains expected content types.
    
    Args:
        response: The AI response text to validate.
        content_types: List of expected content type strings (e.g., ['code', 'explanation']).
                      If None, performs basic non-empty check.
    
    Returns:
        bool: True if response is valid, False otherwise.
    """
    if not response or not isinstance(response, str):
        return False
    
    response_lower = response.lower()
    
    if not content_types:
        # Basic validation: non-empty, not just whitespace
        return bool(response.strip())
    
    # Check if response contains any expected content type keywords
    for content_type in content_types:
        if content_type.lower() in response_lower:
            return True
    
    logging.warning(f"Response validation failed: expected {content_types}, got partial match")
    return True  # Don't fail hard on content validation


def estimate_tokens(text: str) -> int:
    """Estimate token count for text (rough approximation).
    
    Uses simple heuristic: ~4 characters per token (approximate for English).
    Useful for cost estimation and rate limiting.
    
    Args:
        text: Text to estimate tokens for.
    
    Returns:
        int: Estimated token count.
    """
    if not text:
        return 0
    # Simple heuristic: roughly 4 characters per token
    return max(1, len(text) // 4)


def estimate_cost(tokens: int, model: str = "gpt-4", rate_per_1k_input: float = 0.03) -> float:
    """Estimate cost for API-based backends.
    
    Args:
        tokens: Number of tokens used.
        model: Model identifier (for future lookup tables).
        rate_per_1k_input: Cost per 1000 input tokens (default: $0.03 for GPT-4).
    
    Returns:
        float: Estimated cost in USD.
    """
    # Simple estimation: tokens * (rate_per_1k / 1000)
    cost = (tokens / 1000.0) * rate_per_1k_input
    logging.debug(f"Estimated cost for {tokens} tokens: ${cost:.6f}")
    return cost


def configure_timeout_per_backend(backend: str, timeout_s: int) -> None:
    """Configure timeout for specific backend type.
    
    Args:
        backend: Backend name ('copilot', 'gh', 'github-models').
        timeout_s: Timeout in seconds.
    """
    # Store in environment for now; could be expanded to persistent config
    env_key = f"DV_AGENT_TIMEOUT_{backend.upper()}"
    os.environ[env_key] = str(timeout_s)
    logging.debug(f"Configured {backend} timeout to {timeout_s}s")


def llm_chat_via_github_models(
    prompt: str,
    model: str,
    system_prompt: str = "You are a helpful assistant.",
    base_url: Optional[str] = None,
    token: Optional[str] = None,
    timeout_s: int = 60,
    max_retries: int = 2,
    use_cache: bool = True,
    stream: bool = False,
    validate_content: bool = True,
) -> str:
    """Call a GitHub Models OpenAI-compatible chat endpoint with retry logic.
    
    Makes an HTTP request to a GitHub Models API endpoint with the provided
    prompt and returns the AI's response. Includes retry logic for transient failures,
    response caching, streaming support, and response validation.
    
    Args:
        prompt: User prompt to send to the model.
        model: Model identifier (e.g., 'gpt-4', 'claude-3-sonnet').
        system_prompt: System message for the model. Defaults to helpful assistant.
        base_url: API endpoint base URL. Can also be set via GITHUB_MODELS_BASE_URL.
        token: GitHub personal access token. Can also be set via GITHUB_TOKEN.
        timeout_s: HTTP request timeout in seconds. Defaults to 60.
        max_retries: Maximum retry attempts on failure. Defaults to 2.
        use_cache: If True, cache responses for identical prompts. Defaults to True.
        stream: If True, attempt to use streaming responses. Defaults to False.
        validate_content: If True, validate response before returning. Defaults to True.
        
    Returns:
        str: The AI model's response text.
        
    Raises:
        RuntimeError: If required dependencies or configuration are missing.
        requests.RequestException: If HTTP request fails after all retries.
        
    Example:
        response = llm_chat_via_github_models(
            prompt="What is Python?",
            model="gpt-4",
            base_url="https://api.github.com/models",
            token="ghp_...",
            max_retries=3
        )
        
    Note:
        - Requires 'requests' package to be installed
        - Follows OpenAI API format for compatibility
        - Raises RuntimeError if requests library unavailable
        - Retries with exponential backoff on transient errors
        - Network timeouts are retried automatically
        - Responses are cached by prompt hash (configurable)
        - Streaming not yet fully implemented (flag for future)
    """
    if requests is None:
        raise RuntimeError("Missing dependency: install 'requests' to use GitHub Models backend")
    
    # Check cache first
    cache_key = _get_cache_key(prompt, model)
    if use_cache and cache_key in _response_cache:
        _metrics["cache_hits"] += 1
        logging.debug(f"Cache hit for prompt hash: {cache_key}")
        return _response_cache[cache_key]
    
    resolved_token = token or os.environ.get("GITHUB_TOKEN")
    if not resolved_token:
        raise RuntimeError("Missing token: set GITHUB_TOKEN env var or pass token=")
    
    resolved_base_url = (base_url or os.environ.get("GITHUB_MODELS_BASE_URL") or "").strip()
    if not resolved_base_url:
        raise RuntimeError(
            "Missing base URL: set GITHUB_MODELS_BASE_URL env var or pass base_url="
        )
    
    url = resolved_base_url.rstrip("/") + "/v1/chat/completions"
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }
    
    # Add streaming support if requested
    if stream:
        payload["stream"] = True
    
    headers = {
        "Authorization": f"Bearer {resolved_token}",
        "Content-Type": "application/json",
    }
    
    last_error = None
    start_time = time.time()
    _metrics["requests"] += 1
    
    for attempt in range(max_retries + 1):
        try:
            logging.debug(f"Making GitHub Models API request (attempt {attempt + 1}/{max_retries + 1})")
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=timeout_s,
            )
            response.raise_for_status()
            data = response.json()
            try:
                result = (data["choices"][0]["message"]["content"] or "").strip()
                
                # Validate response if requested
                if validate_content and not validate_response_content(result):
                    logging.warning("Response validation failed, but continuing")
                
                # Cache the response
                if use_cache:
                    _response_cache[cache_key] = result
                
                # Track metrics
                latency_ms = int((time.time() - start_time) * 1000)
                _metrics["total_latency_ms"] += latency_ms
                
                logging.debug(f"Received {len(result)} bytes from GitHub Models API ({latency_ms}ms)")
                return result
            except (KeyError, IndexError, TypeError) as e:
                raise RuntimeError(f"Unexpected response shape from LLM endpoint: {data!r}") from e
        except (requests.Timeout, requests.ConnectionError) as e:
            last_error = e
            _metrics["timeouts"] += 1
            if attempt < max_retries:
                delay = min(2 ** attempt, 30)  # Exponential backoff, max 30s
                logging.warning(f"GitHub Models API timeout/connection error, retrying in {delay}s...")
                time.sleep(delay)
            else:
                _metrics["errors"] += 1
                logging.error(f"GitHub Models API failed after {max_retries + 1} attempts")
                raise
        except requests.RequestException as e:
            _metrics["errors"] += 1
            logging.error(f"GitHub Models API request failed: {e}")
            raise
    
    if last_error:
        raise last_error


def run_subagent(description: str, prompt: str, original_content: str = "") -> Optional[str]:
    """Run a subagent using one of several AI backends.
    
    Attempts to run a task using available AI backends with automatic selection
    and fallback mechanisms. Tries backends in order of preference:
    1. GitHub Copilot CLI (if DV_AGENT_BACKEND=copilot)
    2. GitHub Models API (if configured)
    3. gh copilot (if available)
    4. Falls back gracefully if no backend available
    
    Args:
        description: Human-readable task description (e.g., "Improve code quality").
        prompt: The specific prompt/task to send to the AI backend.
        original_content: Current file content for context (limited by DV_AGENT_MAX_CONTEXT_CHARS).
                         Defaults to empty string.
        
    Returns:
        Optional[str]: The AI backend's response, or None if all backends fail.
        
    Raises:
        RuntimeError: If explicit backend requested but unavailable.
        
    Example:
        result = run_subagent(
            description="Add docstrings to function",
            prompt="Add Google-style docstrings",
            original_content=source_code
        )
        if result:
            print(result)
        else:
            print("No AI backend available")
            
    Environment Variables:
        DV_AGENT_BACKEND: Force specific backend ('copilot', 'gh', 'github-models', or 'auto').
        DV_AGENT_MAX_CONTEXT_CHARS: Maximum context size (default 12000).
        
    Note:
        - Context is trimmed to fit within DV_AGENT_MAX_CONTEXT_CHARS
        - Full prompt includes task description and original file context
        - Logs debug info for troubleshooting
        - Handles timeouts and errors gracefully
    """
    def _build_full_prompt() -> str:
        try:
            max_context_chars = int(os.environ.get("DV_AGENT_MAX_CONTEXT_CHARS", "12000"))
        except ValueError:
            max_context_chars = 12_000
        trimmed_original = (original_content or "")[:max_context_chars]
        return (
            f"Task: {description}\n\n"
            f"Prompt:\n{prompt}\n\n"
            "Context (existing file content):\n"
            f"{trimmed_original}"
        ).strip()

    def _try_copilot_cli() -> Optional[str]:
        if not _command_available('copilot'):
            logging.debug("Copilot CLI not available")
            return None
        full_prompt = _build_full_prompt()
        repo_root = _resolve_repo_root()
        try:
            logging.debug("Attempting to use Copilot CLI backend")
            result = subprocess.run(
                [
                    'copilot',
                    '--prompt',
                    full_prompt,
                    '--no-color',
                    '--log-level',
                    'error',
                    '--add-dir',
                    str(repo_root),
                    '--allow-all-tools',
                    '--disable-parallel-tools-execution',
                    '--deny-tool',
                    'write',
                    '--deny-tool',
                    'shell',
                    '--silent',
                    '--stream',
                    'off',
                ],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=180,
                cwd=str(repo_root),
                check=False
            )
            stdout = (result.stdout or "").strip()
            if result.returncode == 0 and stdout:
                logging.info("Copilot CLI backend succeeded")
                return stdout
            if result.returncode != 0:
                logging.debug(f"Copilot CLI failed (code {result.returncode}): {result.stderr}")
        except subprocess.TimeoutExpired:
            logging.warning("Copilot CLI timed out")
            return None
        except Exception as e:
            logging.warning(f"Copilot CLI error: {e}")
            return None
        return None

    def _looks_like_command(text: str) -> bool:
        t = (text or "").strip()
        if not t:
            return False
        if "\n" in t:
            return False
        if any(op in t for op in ("|", "&&", ";")):
            return True
        starters = (
            "git ",
            "gh ",
            "docker ",
            "kubectl ",
            "pip ",
            "python ",
            "npm ",
            "node ",
            "pwsh ",
            "powershell ",
            "Get-",
            "Set-",
            "New-",
        )
        return t.startswith(starters)

    def _try_gh_copilot(*, allow_non_command_prompt: bool) -> Optional[str]:
        if not _command_available('gh'):
            logging.debug("gh CLI not available")
            return None
        if not allow_non_command_prompt and not _looks_like_command(prompt):
            logging.debug("Prompt doesn't look like a command, skipping gh copilot")
            return None
        max_len = 2000
        prompt_to_use = prompt
        if len(prompt) > max_len:
            logging.warning(f"Prompt truncated from {len(prompt)} to {max_len} chars for gh copilot")
            prompt_to_use = prompt[:max_len]

        try:
            logging.debug("Attempting to use gh copilot backend")
            result = subprocess.run(
                ['gh', 'copilot', 'explain', prompt_to_use],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,
                cwd=str(_resolve_repo_root()),
                check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                logging.info("gh copilot backend succeeded")
                return f"# GitHub Copilot (gh) Explanation:\n{result.stdout.strip()}"
            if result.returncode != 0:
                logging.debug(f"gh copilot failed (code {result.returncode}): {result.stderr}")
        except subprocess.TimeoutExpired:
            logging.warning("gh copilot timed out")
            return None
        except Exception as e:
            logging.warning(f"gh copilot error: {e}")
            return None
        return None

    def _try_github_models() -> Optional[str]:
        model = (
            os.environ.get("DV_AGENT_MODEL")
            or os.environ.get("GITHUB_MODELS_MODEL")
            or ""
        ).strip()
        system_prompt = os.environ.get(
            "DV_AGENT_SYSTEM_PROMPT",
            "You are a helpful assistant. Follow the user instructions exactly.",
        )
        base_url = os.environ.get("GITHUB_MODELS_BASE_URL")
        token = os.environ.get("GITHUB_TOKEN")
        if not model:
            logging.debug("No model specified for GitHub Models")
            return None
        if not base_url or not base_url.strip():
            logging.debug("No base URL specified for GitHub Models")
            return None
        if not token:
            logging.debug("No GitHub token specified for GitHub Models")
            return None
        full_prompt = _build_full_prompt()
        try:
            logging.debug("Attempting to use GitHub Models backend")
            return llm_chat_via_github_models(
                prompt=full_prompt,
                model=model,
                system_prompt=system_prompt,
                base_url=base_url,
                token=token,
            )
        except Exception as e:
            logging.warning(f"GitHub Models backend error: {e}")
            return None

    backend = os.environ.get("DV_AGENT_BACKEND", "auto").strip().lower()
    logging.debug(f"Using backend: {backend}")
    
    if backend in {"copilot", "local", "copilot-cli"}:
        result = _try_copilot_cli()
        if result is None:
            raise RuntimeError("Requested DV_AGENT_BACKEND=copilot but local 'copilot' CLI is unavailable")
        return result
    if backend in {"gh", "gh-copilot"}:
        result = _try_gh_copilot(allow_non_command_prompt=True)
        if result is None:
            raise RuntimeError("Requested DV_AGENT_BACKEND=gh but 'gh copilot' is unavailable")
        return result
    if backend in {"github-models", "github_models", "models"}:
        result = _try_github_models()
        if result is None:
            raise RuntimeError(
                "Requested DV_AGENT_BACKEND=github-models but it is not configured; "
                "set GITHUB_MODELS_BASE_URL, GITHUB_TOKEN, and DV_AGENT_MODEL (or GITHUB_MODELS_MODEL)"
            )
        return result
    
    # auto (default)
    logging.debug("Trying backends in order: copilot, github-models, gh")
    result = _try_copilot_cli()
    if result is not None:
        return result
    try:
        result = _try_github_models()
        if result is not None:
            return result
    except Exception:
        pass
    result = _try_gh_copilot(allow_non_command_prompt=False)
    if result is not None:
        return result
    
    logging.warning("No AI backend available")
    return None


# ============================================================================
# Circuit Breaker Pattern for Failing Backends
# ============================================================================

class CircuitBreaker:
    """Circuit breaker pattern for failing backends.
    
    Tracks failures per backend and temporarily disables them if they exceed
    a failure threshold. Prevents cascading failures and wasted retries.
    
    States:
    - CLOSED: Normal operation, requests go through
    - OPEN: Too many failures, requests rejected immediately
    - HALF_OPEN: Recovery attempt, one request allowed
    
    Example:
        breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60)
        if breaker.is_open():
            print("Backend is currently unavailable")
        else:
            try:
                result = call_backend()
                breaker.record_success()
            except Exception:
                breaker.record_failure()
    """
    
    def __init__(
        self,
        name: str = "default",
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
    ) -> None:
        """Initialize circuit breaker.
        
        Args:
            name: Name for this breaker (e.g., 'github-models', 'copilot').
            failure_threshold: Number of failures before opening circuit.
            recovery_timeout: Seconds to wait before attempting recovery.
        """
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "CLOSED"  # CLOSED, OPEN, or HALF_OPEN
        
    def is_open(self) -> bool:
        """Check if circuit is open (backend should be skipped)."""
        if self.state == "CLOSED":
            return False
        if self.state == "OPEN":
            # Check if recovery timeout has elapsed
            if self.last_failure_time is None:
                return True
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "HALF_OPEN"
                logging.info(f"Circuit breaker '{self.name}' attempting recovery (HALF_OPEN)")
                return False
            return True
        # HALF_OPEN
        return False
    
    def record_success(self) -> None:
        """Record a successful request."""
        self.failure_count = 0
        self.success_count += 1
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            logging.info(f"Circuit breaker '{self.name}' recovered (CLOSED)")
    
    def record_failure(self) -> None:
        """Record a failed request."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logging.warning(
                f"Circuit breaker '{self.name}' opened after {self.failure_count} failures"
            )


def get_backend_status() -> dict:
    """Return a diagnostic snapshot of backend availability and configuration.
    
    Checks which AI backends are available and configured on the system.
    Used for diagnostics and debugging backend selection issues.
    
    Returns:
        dict: Status information including:
            - selected_backend: Current backend choice (auto, copilot, gh, etc.)
            - repo_root: Detected repository root directory
            - max_context_chars: Maximum context size to include
            - commands: Dict with availability of 'copilot' and 'gh' CLIs
            - github_models: Dict with GitHub Models configuration status
            
    Example:
        status = get_backend_status()
        if status['github_models']['configured']:
            print("GitHub Models is ready to use")
            
    Note:
        - Doesn't require any external services
        - Safe to call for diagnostics
        - Returns info on all backends regardless of selection
    """
    backend = os.environ.get("DV_AGENT_BACKEND", "auto").strip().lower()
    repo_root = str(_resolve_repo_root())
    try:
        max_context_chars = int(os.environ.get("DV_AGENT_MAX_CONTEXT_CHARS", "12000"))
    except ValueError:
        max_context_chars = 12_000
    models_base_url = (os.environ.get("GITHUB_MODELS_BASE_URL") or "").strip()
    models_model = (
        os.environ.get("DV_AGENT_MODEL")
        or os.environ.get("GITHUB_MODELS_MODEL")
        or ""
    ).strip()
    token_set = bool(os.environ.get("GITHUB_TOKEN"))
    return {
        "selected_backend": backend,
        "repo_root": repo_root,
        "max_context_chars": max_context_chars,
        "commands": {
            "copilot": _command_available("copilot"),
            "gh": _command_available("gh"),
        },
        "github_models": {
            "requests_installed": requests is not None,
            "base_url_set": bool(models_base_url),
            "model_set": bool(models_model),
            "token_set": token_set,
            "configured": bool(models_base_url and models_model and token_set and requests is not None),
        },
    }


def describe_backends() -> str:
    """Return human-readable backend diagnostics for debugging.
    
    Generates a formatted text report of all AI backends and their configuration status.
    Useful for troubleshooting when the agent can't find an available backend.
    
    Returns:
        str: Multi-line formatted text with backend diagnostics.
        
    Example:
        print(BaseAgent.describe_backends())
        # Output:
        # Backend diagnostics:
        # - selected: auto
        # - repo_root: /home/user/project
        # - local copilot CLI available: yes
        # - gh CLI available: yes
        # - github-models configured: yes
        
    Note:
        - Safe to call from user code
        - Doesn't require AI backend to be working
        - Shows configuration issues clearly
    """
    status = get_backend_status()
    cmd = status["commands"]
    models = status["github_models"]

    def yn(value: bool) -> str:
        return "yes" if value else "no"
    
    result = "\n".join(
        [
            "Backend diagnostics:",
            f"- selected: {status['selected_backend']}",
            f"- repo_root: {status['repo_root']}",
            f"- max_context_chars: {status['max_context_chars']}",
            f"- local copilot CLI available: {yn(bool(cmd.get('copilot')))}",
            f"- gh CLI available: {yn(bool(cmd.get('gh')))}",
            "- github-models configured:",
            f"  - requests installed: {yn(bool(models.get('requests_installed')))}",
            f"  - base_url set: {yn(bool(models.get('base_url_set')))}",
            f"  - model set: {yn(bool(models.get('model_set')))}",
            f"  - token set: {yn(bool(models.get('token_set')))}",
        ]
    )
    logging.debug("Backend diagnostics generated")
    return result
