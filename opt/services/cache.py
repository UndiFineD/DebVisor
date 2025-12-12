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


"""
Cache Layer for DebVisor Services

Provides Redis-backed caching with TTL, invalidation, and performance metrics.
Supports query result caching, report caching, and real-time event deduplication.

Features:
- Multi-tier caching (L1: in-memory, L2: Redis)
- Automatic TTL management and key versioning
- Cache invalidation patterns (tag-based, pattern-based)
- Performance metrics and hit rate tracking
- Distributed cache coherency
- Fallback mechanisms for cache failures

Author: DebVisor Team
Date: 2025-11-26
"""

import json
from datetime import datetime, timezone

import hashlib
import asyncio
import time
# import logging
from typing import Any, Optional, Dict, Callable, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
import functools
from abc import ABC, abstractmethod
from typing import TypeVar

try:
    import aioredis  # type: ignore
except ImportError:  # pragma: no cover
    aioredis = None

# Type variable for cached function returns
CacheF = TypeVar("CacheF", bound=Callable[..., Any])

# Third-party imports (to be installed)


logger = logging.getLogger(__name__)


class CacheStrategy(Enum):
    """Cache storage strategy"""

    L1_ONLY = "l1_only"    # In-memory only
    L2_ONLY = "l2_only"    # Redis only
    L1_L2 = "l1_l2"    # Both (write-through)
    L1_L2_WRITE_BACK = "l1_l2_write_back"    # Async write to L2


class CacheKeyType(Enum):
    """Cache key categorization for invalidation"""

    QUERY_RESULT = "query"
    REPORT = "report"
    TOPOLOGY = "topology"
    HEALTH = "health"
    RESOURCE = "resource"
    SESSION = "session"
    METRIC = "metric"
    EVENT = "event"


@dataclass
class CacheMetrics:
    """Cache performance metrics"""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    errors: int = 0
    avg_latency_ms: float = 0.0
    total_requests: int = 0

    def hit_rate(self) -> float:
        """Calculate cache hit rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.hits / self.total_requests) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        return {**asdict(self), "hit_rate_percent": self.hit_rate()}


@dataclass
class CacheEntry:
    """Single cache entry with metadata"""

    key: str
    value: Any
    ttl_seconds: int
    key_type: CacheKeyType
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    accessed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    access_count: int = 0
    tags: Set[str] = field(default_factory=set)

    def is_expired(self) -> bool:
        """Check if entry has expired"""
        if self.ttl_seconds == 0:
            return False
        elapsed = (datetime.now(timezone.utc) - self.created_at).total_seconds()
        return elapsed > self.ttl_seconds

    def to_json(self) -> str:
        """Serialize entry to JSON"""
        return json.dumps(
            {
                "key": self.key,
                "value": self.value,
                "ttl_seconds": self.ttl_seconds,
                "key_type": self.key_type.value,
                "created_at": self.created_at.isoformat(),
                "accessed_at": self.accessed_at.isoformat(),
                "access_count": self.access_count,
                "tags": list(self.tags),
            }
        )


class CacheProvider(ABC):
    """Abstract base class for cache implementations"""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int) -> bool:
        """Set value in cache"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        pass

    @abstractmethod
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate keys matching pattern"""
        pass

    @abstractmethod
    async def invalidate_tags(self, tags: Set[str]) -> int:
        """Invalidate all keys with given tags"""
        pass

    @abstractmethod
    async def clear(self) -> bool:
        """Clear entire cache"""
        pass

    @abstractmethod
    async def get_metrics(self) -> CacheMetrics:
        """Get cache performance metrics"""
        pass


class L1Cache(CacheProvider):
    """In-memory L1 cache using dict"""

    def __init__(self, max_size: int = 1000):
        self.data: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.metrics = CacheMetrics()
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from L1 cache"""
        async with self._lock:
            start = time.time()
            entry = self.data.get(key)

            if entry is None:
                self.metrics.misses += 1
                self.metrics.total_requests += 1
                return None

            if entry.is_expired():
                del self.data[key]
                self.metrics.misses += 1
                self.metrics.total_requests += 1
                self.metrics.evictions += 1
                return None

            # Update access tracking
            entry.accessed_at = datetime.now(timezone.utc)
            entry.access_count += 1

            self.metrics.hits += 1
            self.metrics.total_requests += 1
            latency = (time.time() - start) * 1000    # ms
            self.metrics.avg_latency_ms = (self.metrics.avg_latency_ms + latency) / 2

            return entry.value

    async def set(self, key: str, value: Any, ttl_seconds: int) -> bool:
        """Set value in L1 cache"""
        async with self._lock:
            try:
                if len(self.data) >= self.max_size:
                # Evict least recently used entry
                    lru_key = min(
                        self.data.keys(), key=lambda k: self.data[k].accessed_at
                    )
                    del self.data[lru_key]
                    self.metrics.evictions += 1

                entry = CacheEntry(
                    key=key,
                    value=value,
                    ttl_seconds=ttl_seconds,
                    key_type=CacheKeyType.RESOURCE,
                )
                self.data[key] = entry
                return True
            except Exception as e:
                logger.error(f"L1 cache set error: {e}")
                self.metrics.errors += 1
                return False

    async def delete(self, key: str) -> bool:
        """Delete value from L1 cache"""
        async with self._lock:
            if key in self.data:
                del self.data[key]
                return True
            return False

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate keys matching pattern"""
        async with self._lock:
            import fnmatch

            keys_to_delete = [
                k for k in self.data.keys() if fnmatch.fnmatch(k, pattern)
            ]
            for key in keys_to_delete:
                del self.data[key]
            return len(keys_to_delete)

    async def invalidate_tags(self, tags: Set[str]) -> int:
        """Invalidate keys with given tags"""
        async with self._lock:
            keys_to_delete = [
                k for k, v in self.data.items() if any(tag in v.tags for tag in tags)
            ]
            for key in keys_to_delete:
                del self.data[key]
            return len(keys_to_delete)

    async def clear(self) -> bool:
        """Clear entire cache"""
        async with self._lock:
            self.data.clear()
            return True

    async def get_metrics(self) -> CacheMetrics:
        """Get cache metrics"""
        return self.metrics


class RedisCache(CacheProvider):
    """Redis L2 cache provider"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client: Optional[aioredis.Redis[str]] = None
        self.metrics = CacheMetrics()

    async def connect(self) -> bool:
        """Connect to Redis"""
        try:
            self.redis_client = await aioredis.from_url(
                self.redis_url, decode_responses=True
            )
            # Test connection
            await self.redis_client.ping()
            logger.info("Connected to Redis cache")
            return True
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            return False

    async def disconnect(self) -> bool:
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
            self.redis_client = None
        return True

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        if not self.redis_client:
            self.metrics.errors += 1
            return None

        try:
            start = time.time()
            value = await self.redis_client.get(key)

            if value is None:
                self.metrics.misses += 1
            else:
                self.metrics.hits += 1
                latency = (time.time() - start) * 1000
                self.metrics.avg_latency_ms = (
                    self.metrics.avg_latency_ms + latency
                ) / 2

            self.metrics.total_requests += 1
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            self.metrics.errors += 1
            self.metrics.misses += 1
            self.metrics.total_requests += 1
            return None

    async def set(self, key: str, value: Any, ttl_seconds: int) -> bool:
        """Set value in Redis"""
        if not self.redis_client:
            self.metrics.errors += 1
            return False

        try:
            serialized = json.dumps(value)
            if ttl_seconds > 0:
                await self.redis_client.setex(key, ttl_seconds, serialized)
            else:
                await self.redis_client.set(key, serialized)
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            self.metrics.errors += 1
            return False

    async def delete(self, key: str) -> bool:
        """Delete from Redis"""
        if not self.redis_client:
            return False

        try:
            result = await self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            self.metrics.errors += 1
            return False

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate keys matching pattern"""
        if not self.redis_client:
            return 0

        try:
            cursor = 0
            count = 0
            while True:
                cursor, keys = await self.redis_client.scan(
                    cursor, match=pattern, count=100
                )
                if keys:
                    await self.redis_client.delete(*keys)
                    count += len(keys)
                if cursor == 0:
                    break
            return count
        except Exception as e:
            logger.error(f"Redis pattern invalidation error: {e}")
            self.metrics.errors += 1
            return 0

    async def invalidate_tags(self, tags: Set[str]) -> int:
        """Invalidate keys with tags (requires tag index)"""
        if not self.redis_client:
            return 0

        try:
            count = 0
            for tag in tags:
                pattern = f"tag:{tag}:*"
                count += await self.invalidate_pattern(pattern)
            return count
        except Exception as e:
            logger.error(f"Redis tag invalidation error: {e}")
            self.metrics.errors += 1
            return 0

    async def clear(self) -> bool:
        """Clear entire Redis cache"""
        if not self.redis_client:
            return False

        try:
            await self.redis_client.flushdb()
            return True
        except Exception as e:
            logger.error(f"Redis clear error: {e}")
            self.metrics.errors += 1
            return False

    async def get_metrics(self) -> CacheMetrics:
        """Get Redis cache metrics"""
        return self.metrics


class HybridCache(CacheProvider):
    """Hybrid L1+L2 cache with multi-tier strategy"""

    def __init__(
        self, l1: L1Cache, l2: RedisCache, strategy: CacheStrategy = CacheStrategy.L1_L2
    ):
        self.l1 = l1
        self.l2 = l2
        self.strategy = strategy
        self.metrics = CacheMetrics()

    async def get(self, key: str) -> Optional[Any]:
        """Get from cache hierarchy"""
        # Try L1 first
        if self.strategy != CacheStrategy.L2_ONLY:
            value = await self.l1.get(key)
            if value is not None:
                self.metrics.hits += 1
                self.metrics.total_requests += 1
                return value

        # Fall back to L2
        if self.strategy != CacheStrategy.L1_ONLY:
            value = await self.l2.get(key)
            if value is not None:
            # Populate L1 for next access
                if self.strategy != CacheStrategy.L2_ONLY:
                    await self.l1.set(key, value, 3600)
                self.metrics.hits += 1
                self.metrics.total_requests += 1
                return value

        self.metrics.misses += 1
        self.metrics.total_requests += 1
        return None

    async def set(self, key: str, value: Any, ttl_seconds: int) -> bool:
        """Set in cache hierarchy"""
        if self.strategy == CacheStrategy.L1_ONLY:
            return await self.l1.set(key, value, ttl_seconds)
        elif self.strategy == CacheStrategy.L2_ONLY:
            return await self.l2.set(key, value, ttl_seconds)
        elif self.strategy == CacheStrategy.L1_L2:
        # Write-through: set both
            l1_ok = await self.l1.set(key, value, ttl_seconds)
            l2_ok = await self.l2.set(key, value, ttl_seconds)
            return l1_ok and l2_ok
        else:    # L1_L2_WRITE_BACK
        # Write L1 first, async write L2
            l1_ok = await self.l1.set(key, value, ttl_seconds)
            if l1_ok:
                asyncio.create_task(self.l2.set(key, value, ttl_seconds))
            return l1_ok

    async def delete(self, key: str) -> bool:
        """Delete from all tiers"""
        l1_ok = await self.l1.delete(key)
        l2_ok = await self.l2.delete(key)
        return l1_ok or l2_ok

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate pattern in all tiers"""
        l1_count = await self.l1.invalidate_pattern(pattern)
        l2_count = await self.l2.invalidate_pattern(pattern)
        return l1_count + l2_count

    async def invalidate_tags(self, tags: Set[str]) -> int:
        """Invalidate tags in all tiers"""
        l1_count = await self.l1.invalidate_tags(tags)
        l2_count = await self.l2.invalidate_tags(tags)
        return l1_count + l2_count

    async def clear(self) -> bool:
        """Clear all cache tiers"""
        l1_ok = await self.l1.clear()
        l2_ok = await self.l2.clear()
        return l1_ok and l2_ok

    async def get_metrics(self) -> CacheMetrics:
        """Get combined metrics"""
        l1_metrics = await self.l1.get_metrics()
        l2_metrics = await self.l2.get_metrics()

        return CacheMetrics(
            hits=l1_metrics.hits + l2_metrics.hits,
            misses=l1_metrics.misses + l2_metrics.misses,
            evictions=l1_metrics.evictions + l2_metrics.evictions,
            errors=l1_metrics.errors + l2_metrics.errors,
            avg_latency_ms=(l1_metrics.avg_latency_ms + l2_metrics.avg_latency_ms) / 2,
            total_requests=l1_metrics.total_requests + l2_metrics.total_requests,
        )


def cached(
    ttl_seconds: int = 3600,
    key_prefix: str = "cache",
    cache: Optional[HybridCache] = None,
    tags: Optional[Set[str]] = None,
) -> Callable[[CacheF], CacheF]:
    """Decorator for caching async function results"""

    def decorator(func: CacheF) -> CacheF:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Generate cache key from function name and arguments
            key_data = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            cache_key = f"{key_prefix}:{hashlib.sha256(key_data.encode()).hexdigest()}"

            # Try to get from cache
            if cache:
                cached_value = await cache.get(cache_key)
                if cached_value is not None:
                    return cached_value

            # Execute function
            result = await func(*args, **kwargs)

            # Store in cache
            if cache:
                await cache.set(cache_key, result, ttl_seconds)

            return result

        return wrapper    # type: ignore

    return decorator


class CacheManager:
    """Central cache management for DebVisor"""

    def __init__(self) -> None:
        self.l1 = L1Cache(max_size=1000)
        self.l2 = RedisCache()
        self.hybrid = HybridCache(self.l1, self.l2, CacheStrategy.L1_L2)

    async def initialize(self) -> bool:
        """Initialize cache system"""
        try:
            redis_ok = await self.l2.connect()
            if not redis_ok:
                logger.warning("Redis cache unavailable, using L1 only")
            logger.info("Cache manager initialized")
            return True
        except Exception as e:
            logger.error(f"Cache initialization error: {e}")
            return False

    async def shutdown(self) -> bool:
        """Shutdown cache system"""
        try:
            await self.l2.disconnect()
            await self.hybrid.clear()
            logger.info("Cache manager shutdown")
            return True
        except Exception as e:
            logger.error(f"Cache shutdown error: {e}")
            return False

    async def get_cache_status(self) -> Dict[str, Any]:
        """Get cache system status"""
        l1_metrics = await self.l1.get_metrics()
        l2_metrics = await self.l2.get_metrics()

        return {
            "l1": {
                "metrics": l1_metrics.to_dict(),
                "size": len(self.l1.data),
                "max_size": self.l1.max_size,
            },
            "l2": {
                "metrics": l2_metrics.to_dict(),
                "connected": self.l2.redis_client is not None,
            },
            "hybrid_metrics": (await self.hybrid.get_metrics()).to_dict(),
        }


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


async def get_cache_manager() -> CacheManager:
    """Get or create global cache manager"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
        await _cache_manager.initialize()
    return _cache_manager
