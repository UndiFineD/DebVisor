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
Feature Flags Service.

This module provides a mechanism to toggle features on and off dynamically
without redeploying the application. It supports boolean flags and
percentage-based rollouts, backed by Redis for persistence.
"""

import json
import redis
import logging
import hashlib
import os
from typing import Any, Dict, Optional, List
from opt.core.config import settings

logger = logging.getLogger(__name__)


class FeatureFlagManager:
    """
    Manages feature flags using Redis as a backend.
    """

    def __init__(self, redis_url: str = settings.REDIS_URL):
        """
        Initialize the FeatureFlagManager.

        Args:
            redis_url: The URL of the Redis instance to use.
        """
        try:
            self.redis = redis.from_url(redis_url, decode_responses=True)
            self.prefix = "feature_flag:"
            self.enabled = True
        except Exception as e:
            logger.error(f"Failed to connect to Redis for feature flags: {e}")
            self.enabled = False

    def is_enabled(self, flag_name: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if a feature flag is enabled.

        Args:
            flag_name: The unique identifier for the flag.
            context: Optional dictionary containing context (e.g., user_id, tenant_id)
                    for targeted rollouts.

        Returns:
            bool: True if the feature is enabled, False otherwise.
        """
        # 1. Check Environment Variable Override
        env_key = f"DEBVISOR_FEATURE_{flag_name.upper()}"
        if env_key in os.environ:
            return os.environ[env_key].lower() in ("true", "1", "yes", "on")

        if not self.enabled:
        # If Redis is down or not configured, default to False (safe)
            return False

        try:
            flag_data_json = self.redis.get(f"{self.prefix}{flag_name}")
            if not flag_data_json:
                return False    # Default to disabled if not found

            flag_data = json.loads(flag_data_json)

            if not flag_data.get("enabled", False):
                return False

            # Targeted users/tenants
            if context:
                user_id = str(context.get("user_id", ""))
                tenant_id = str(context.get("tenant_id", ""))

                allowed_users = flag_data.get("users", [])
                if user_id and user_id in allowed_users:
                    return True

                allowed_tenants = flag_data.get("tenants", [])
                if tenant_id and tenant_id in allowed_tenants:
                    return True

            # Percentage-based rollout
            rollout_percentage = flag_data.get("rollout_percentage", 100)
            if rollout_percentage < 100:
                if not context:
                # If no context provided but rollout < 100%, default to disabled
                    return False

                identifier = str(context.get("user_id") or context.get("tenant_id") or "anonymous")
                # Deterministic hashing
                hash_input = f"{flag_name}:{identifier}".encode("utf-8")
                hash_val = int(hashlib.sha256(hash_input).hexdigest(), 16)
                if (hash_val % 100) >= rollout_percentage:
                    return False

            return True

        except redis.RedisError as e:
            logger.error(f"Error checking feature flag {flag_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error checking feature flag {flag_name}: {e}")
            return False

    def set_flag(
        self,
        flag_name: str,
        enabled: bool,
        rollout_percentage: int = 100,
        users: Optional[List[str]] = None,
        tenants: Optional[List[str]] = None,
    ) -> bool:
        """
        Set a feature flag's state.

        Args:
            flag_name: The unique identifier for the flag.
            enabled: Whether the flag is globally enabled.
            rollout_percentage: Percentage of users to enable for (0-100).
            users: List of user IDs to explicitly enable.
            tenants: List of tenant IDs to explicitly enable.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.enabled:
            return False

        data = {
            "enabled": enabled,
            "rollout_percentage": rollout_percentage,
            "users": users or [],
            "tenants": tenants or [],
        }
        try:
            self.redis.set(f"{self.prefix}{flag_name}", json.dumps(data))
            logger.info(
                f"Feature flag '{flag_name}' set to enabled={enabled}, "
                f"rollout={rollout_percentage}%, users={len(users or [])}, tenants={len(tenants or [])}"
            )
            return True
        except redis.RedisError as e:
            logger.error(f"Error setting feature flag {flag_name}: {e}")
            return False

    def delete_flag(self, flag_name: str) -> bool:
        """
        Remove a feature flag.

        Args:
            flag_name: The unique identifier for the flag.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.enabled:
            return False

        try:
            self.redis.delete(f"{self.prefix}{flag_name}")
            logger.info(f"Feature flag '{flag_name}' deleted")
            return True
        except redis.RedisError as e:
            logger.error(f"Error deleting feature flag {flag_name}: {e}")
            return False

    def list_flags(self) -> Dict[str, Any]:
        """
        List all defined feature flags.

        Returns:
            Dict[str, Any]: A dictionary of flag names and their configuration.
        """
        if not self.enabled:
            return {}

        try:
            keys = self.redis.keys(f"{self.prefix}*")
            flags = {}
            for key in keys:
                flag_name = key.replace(self.prefix, "")
                val = self.redis.get(key)
                if val:
                    flags[flag_name] = json.loads(val)
            return flags
        except redis.RedisError as e:
            logger.error(f"Error listing feature flags: {e}")
            return {}


# Singleton instance
feature_flags = FeatureFlagManager()
