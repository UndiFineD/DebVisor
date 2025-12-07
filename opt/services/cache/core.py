"""
Distributed Caching Service for DebVisor.

Provides a unified caching interface supporting:
- Redis backend
- In-memory fallback
- Cache invalidation
- Serialization/Deserialization
- Async support
"""

import asyncio
import json
import logging
import pickle
from abc import ABC, abstractmethod
from typing import Any, Optional, Union, List
from datetime import timedelta

logger = logging.getLogger(__name__)

class CacheBackend(ABC):
    """Abstract base class for cache backends."""
    
    @abstractmethod
    async def get(self, key: str) -> Any:
        """Get value from cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL in seconds."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        """Clear all values."""
        pass

class InMemoryCache(CacheBackend):
    """Simple in-memory cache for development/fallback."""
    
    def __init__(self):
        self._store = {}
        self._expiry = {}
    
    async def get(self, key: str) -> Any:
        if key in self._expiry:
            if asyncio.get_event_loop().time() > self._expiry[key]:
                del self._store[key]
                del self._expiry[key]
                return None
        return self._store.get(key)

    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        self._store[key] = value
        self._expiry[key] = asyncio.get_event_loop().time() + ttl
        return True

    async def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            if key in self._expiry:
                del self._expiry[key]
            return True
        return False

    async def clear(self) -> bool:
        self._store.clear()
        self._expiry.clear()
        return True

class RedisCache(CacheBackend):
    """Redis-based cache backend."""
    
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        try:
            import redis.asyncio as redis
            self.redis = redis.Redis(
                host=host, 
                port=port, 
                db=db, 
                password=password, 
                decode_responses=False
            )
            self.enabled = True
        except ImportError:
            logger.warning("redis-py not installed, falling back to in-memory cache")
            self.enabled = False

    async def get(self, key: str) -> Any:
        if not self.enabled: return None
        try:
            data = await self.redis.get(key)
            if data:
                return pickle.loads(data)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        if not self.enabled: return False
        try:
            data = pickle.dumps(value)
            return await self.redis.setex(key, ttl, data)
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        if not self.enabled: return False
        try:
            return await self.redis.delete(key) > 0
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False

    async def clear(self) -> bool:
        if not self.enabled: return False
        try:
            return await self.redis.flushdb()
        except Exception as e:
            logger.error(f"Redis clear error: {e}")
            return False

class CacheManager:
    """Main entry point for caching."""
    
    def __init__(self, backend: str = 'memory', **kwargs):
        if backend == 'redis':
            self.backend = RedisCache(**kwargs)
            if not self.backend.enabled:
                self.backend = InMemoryCache()
        else:
            self.backend = InMemoryCache()
    
    async def get(self, key: str) -> Any:
        return await self.backend.get(key)
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        return await self.backend.set(key, value, ttl)
    
    async def delete(self, key: str) -> bool:
        return await self.backend.delete(key)
    
    async def clear(self) -> bool:
        return await self.backend.clear()

# Global instance
cache = CacheManager()
