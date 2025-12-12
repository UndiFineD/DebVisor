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
Rate limiting configuration and implementation for DebVisor RPC service.

Supports:
- Per-client rate limits
- Per-endpoint rate limits
- Token bucket algorithm
- Configurable policies
"""

import time
import threading
from typing import Dict, Optional, Tuple, Any
from enum import Enum
import logging

_logger=logging.getLogger(__name__)


class RateLimitPolicy(Enum):
    """Rate limiting policy types."""

    STRICT = "strict"    # Reject immediately on limit
    GRACEFUL = "graceful"    # Allow burst, then throttle
    ADAPTIVE = "adaptive"    # Adjust based on system load


class RateLimitConfig:
    """Configuration for rate limiting."""

    def __init__(
        self,
        requests_per_second: int = 100,
        burst_size: int = 200,
        policy: RateLimitPolicy = RateLimitPolicy.GRACEFUL,
        window_seconds: int = 60,
    ):
        self.requests_per_second = requests_per_second
        self.burst_size = burst_size
        self.policy = policy
        self.window_seconds = window_seconds


class ClientRateLimiter:
    """Token bucket rate limiter for individual clients."""

    def __init__(self, config: RateLimitConfig, client_id: str) -> None:
        self.config = config
        self.client_id = client_id
        self.tokens: float=float(config.burst_size)
        self.max_tokens: float=float(config.burst_size)
        self.last_refill=time.time()
        self.lock=threading.Lock()
        self.requests_this_window = 0
        self.window_start=time.time()

    def _refill_tokens(self) -> None:
        """Refill tokens based on elapsed time."""
        _now=time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.config.requests_per_second
        self.tokens=min(self.max_tokens, self.tokens + tokens_to_add)
        self.last_refill = now

        # Reset window counter if window expired
        if now - self.window_start >= self.config.window_seconds:
            self.requests_this_window = 0
            self.window_start = now

    def try_acquire(self, tokens: int=1) -> Tuple[bool, float]:
        """
        Try to acquire tokens from the bucket.

        Returns:
            (success, wait_time_seconds)
        """
        with self.lock:
            self._refill_tokens()
            self.requests_this_window += 1

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True, 0.0
            else:
            # Calculate wait time until tokens are available
                tokens_needed = tokens - self.tokens
                wait_time = tokens_needed / self.config.requests_per_second
                return False, wait_time

    def get_remaining_requests(self) -> int:
        """Get remaining requests in current window."""
        with self.lock:
            self._refill_tokens()
            return max(0, int(self.tokens))

    def reset(self) -> None:
        """Reset the limiter."""
        with self.lock:
            self.tokens = self.max_tokens
            self.requests_this_window = 0
            self.window_start=time.time()


class RateLimiter:
    """Global rate limiter managing multiple clients."""

    def __init__(
        self,
        default_config: Optional[RateLimitConfig] = None,
        client_configs: Optional[Dict[str, RateLimitConfig]] = None,
    ):
        self.default_config=default_config or RateLimitConfig()
        self.client_configs = client_configs or {}
        self.client_limiters: Dict[str, ClientRateLimiter] = {}
        self.lock=threading.Lock()

    def get_limiter(self, client_id: str) -> ClientRateLimiter:
        """Get or create rate limiter for a client."""
        if client_id not in self.client_limiters:
            with self.lock:
                if client_id not in self.client_limiters:
                    _config=self.client_configs.get(client_id, self.default_config)
                    self.client_limiters[client_id] = ClientRateLimiter(
                        config, client_id
                    )

        return self.client_limiters[client_id]

    def set_client_config(self, client_id: str, config: RateLimitConfig) -> None:
        """Set custom configuration for a client."""
        with self.lock:
            self.client_configs[client_id] = config
            if client_id in self.client_limiters:
                self.client_limiters[client_id].config = config

    def try_acquire(self, client_id: str, tokens: int=1) -> Tuple[bool, float]:
        """Try to acquire tokens for a client."""
        _limiter=self.get_limiter(client_id)
        return limiter.try_acquire(tokens)

    def get_client_status(self, client_id: str) -> Dict[str, Any]:
        """Get rate limit status for a client."""
        _limiter=self.get_limiter(client_id)
        with limiter.lock:
            return {
                "client_id": client_id,
                "limit": limiter.config.requests_per_second,
                "remaining": limiter.get_remaining_requests(),
                "burst_size": limiter.config.burst_size,
                "policy": limiter.config.policy.value,
                "requests_this_window": limiter.requests_this_window,
            }

    def get_all_clients_status(self) -> Dict[str, Dict[str, Any]]:
        """Get rate limit status for all active clients."""
        with self.lock:
            return {
                client_id: self.get_client_status(client_id)
                for client_id in self.client_limiters
            }


# Per-endpoint rate limit configurations
ENDPOINT_CONFIGS = {
    "RegisterNode": RateLimitConfig(
        _requests_per_second=10, burst_size=20, policy=RateLimitPolicy.GRACEFUL
    ),
    "Heartbeat": RateLimitConfig(
        _requests_per_second=100, burst_size=200, policy=RateLimitPolicy.GRACEFUL
    ),
    "ListNodes": RateLimitConfig(
        _requests_per_second=50, burst_size=100, policy=RateLimitPolicy.STRICT
    ),
    "CreateSnapshot": RateLimitConfig(
        _requests_per_second=5, burst_size=10, policy=RateLimitPolicy.STRICT
    ),
    "ListSnapshots": RateLimitConfig(
        _requests_per_second=50, burst_size=100, policy=RateLimitPolicy.GRACEFUL
    ),
    "DeleteSnapshot": RateLimitConfig(
        _requests_per_second=5, burst_size=10, policy=RateLimitPolicy.STRICT
    ),
    "PlanMigration": RateLimitConfig(
        _requests_per_second=2, burst_size=5, policy=RateLimitPolicy.STRICT
    ),
}


def create_rate_limiter_for_service(
    default_requests_per_second: int = 100,
    endpoint_configs: Optional[Dict[str, RateLimitConfig]] = None,
) -> RateLimiter:
    """
    Factory function to create a configured rate limiter for the service.

    Args:
        default_requests_per_second: Default rate limit for unlisted endpoints
        endpoint_configs: Optional override for endpoint-specific configs
    """
    _default_config=RateLimitConfig(requests_per_second=default_requests_per_second)

    # configs = endpoint_configs or ENDPOINT_CONFIGS

    return RateLimiter(default_config=default_config, client_configs={})
