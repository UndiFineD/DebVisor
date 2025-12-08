"""
Feature Flags Service.

This module provides a mechanism to toggle features on and off dynamically
without redeploying the application. It supports boolean flags and
percentage-based rollouts, backed by Redis for persistence.
"""

import json
import logging
import hashlib
from typing import Any, Dict, Optional
import redis
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
        if not self.enabled:
            # If Redis is down or not configured, default to False (safe)
            # Or could default to True depending on philosophy, but False is safer.
            return False

        try:
            flag_data_json = self.redis.get(f"{self.prefix}{flag_name}")
            if not flag_data_json:
                return False  # Default to disabled if not found

            flag_data = json.loads(flag_data_json)

            if not flag_data.get("enabled", False):
                return False

            # Percentage-based rollout
            rollout_percentage = flag_data.get("rollout_percentage", 100)
            if rollout_percentage < 100:
                if not context:
                    # If no context provided but rollout < 100%, default to disabled
                    # to avoid random behavior per request if not intended.
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

    def set_flag(self, flag_name: str, enabled: bool, rollout_percentage: int = 100) -> bool:
        """
        Set a feature flag's state.

        Args:
            flag_name: The unique identifier for the flag.
            enabled: Whether the flag is globally enabled.
            rollout_percentage: Percentage of users to enable for (0-100).

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.enabled:
            return False

        data = {
            "enabled": enabled,
            "rollout_percentage": rollout_percentage
        }
        try:
            self.redis.set(f"{self.prefix}{flag_name}", json.dumps(data))
            logger.info(f"Feature flag '{flag_name}' set to enabled={enabled}, rollout={rollout_percentage}%")
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
