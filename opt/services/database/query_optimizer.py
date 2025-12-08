#!/usr/bin/env python3
"""
Database Query Optimization for DebVisor

Implements PERF-002: Database query optimization with indexes, caching, and async operations.

Features:
- Automatic index management and recommendations
- Query result caching with Redis
- Query execution time logging and profiling
- Async database operations
- Connection pooling with health checks
- Query plan analysis and optimization suggestions
"""

import asyncio
import logging
import time
import hashlib
import json
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from contextlib import asynccontextmanager
import asyncpg
import redis.asyncio as aioredis

logger = logging.getLogger(__name__)


class IndexType(Enum):
    """Database index types."""

    BTREE = "btree"
    HASH = "hash"
    GIN = "gin"
    GIST = "gist"
    BRIN = "brin"


@dataclass
class IndexDefinition:
    """Index definition for a table."""

    table: str
    columns: List[str]
    index_type: IndexType = IndexType.BTREE
    unique: bool = False
    where_clause: Optional[str] = None
    name: Optional[str] = None

    def get_name(self) -> str:
        """Generate index name if not provided."""
        if self.name:
            return self.name

        cols = "_".join(self.columns)
        return f"idx_{self.table}_{cols}"

    def to_sql(self) -> str:
        """Generate CREATE INDEX SQL statement."""
        index_name = self.get_name()
        unique = "UNIQUE " if self.unique else ""
        columns = ", ".join(self.columns)
        using = f"USING {self.index_type.value}"
        where = f" WHERE {self.where_clause}" if self.where_clause else ""

        return (
            f"CREATE {unique}INDEX {index_name} "
            f"ON {self.table} {using} ({columns}){where}"
        )


@dataclass
class QueryMetrics:
    """Metrics for a database query."""

    query_hash: str
    query: str
    execution_time_ms: float
    rows_returned: int
    cache_hit: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    plan: Optional[Dict[str, Any]] = None


@dataclass
class CacheConfig:
    """Redis cache configuration."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    default_ttl: int = 300  # 5 minutes
    max_key_size: int = 1024
    enabled: bool = True


class QueryCache:
    """
    Redis-based query result cache.

    Implements PERF-002: Query result caching.
    """

    def __init__(self, config: CacheConfig):
        self.config = config
        self.redis: Optional[aioredis.Redis] = None
        self.cache_hits = 0
        self.cache_misses = 0

        logger.info(
            f"QueryCache initialized: host={config.host}:{config.port}, "
            f"ttl={config.default_ttl}s"
        )

    async def connect(self):
        """Connect to Redis."""
        if not self.config.enabled:
            logger.info("Query cache disabled")
            return

        try:
            self.redis = await aioredis.from_url(
                f"redis://{self.config.host}:{self.config.port}/{self.config.db}",
                password=self.config.password,
                encoding="utf-8",
                decode_responses=False,
            )

            # Test connection
            await self.redis.ping()
            logger.info("Connected to Redis cache")

        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.config.enabled = False

    async def close(self):
        """Close Redis connection."""
        if self.redis:
            await self.redis.close()
            logger.info("Redis cache connection closed")

    def _generate_cache_key(self, query: str, params: Tuple = ()) -> str:
        """Generate cache key from query and parameters."""
        key_data = f"{query}:{params}"
        return f"query:{hashlib.sha256(key_data.encode()).hexdigest()}"

    async def get(self, query: str, params: Tuple = ()) -> Optional[List[Dict]]:
        """Get cached query result."""
        if not self.config.enabled or not self.redis:
            return None

        try:
            cache_key = self._generate_cache_key(query, params)
            cached = await self.redis.get(cache_key)

            if cached:
                self.cache_hits += 1
                result = json.loads(cached)
                logger.debug(f"Cache hit: {cache_key[:16]}...")
                return result

            self.cache_misses += 1
            return None

        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    async def set(
        self, query: str, params: Tuple, result: List[Dict], ttl: Optional[int] = None
    ):
        """Cache query result."""
        if not self.config.enabled or not self.redis:
            return

        try:
            cache_key = self._generate_cache_key(query, params)
            ttl = ttl or self.config.default_ttl

            # Serialize result
            cached_data = json.dumps(result)

            # Check size
            if len(cached_data) > self.config.max_key_size * 1024:
                logger.warning(
                    f"Query result too large to cache: {len(cached_data)} bytes"
                )
                return

            await self.redis.setex(cache_key, ttl, cached_data)
            logger.debug(f"Cached result: {cache_key[:16]}... (ttl={ttl}s)")

        except Exception as e:
            logger.error(f"Cache set error: {e}")

    async def invalidate_pattern(self, pattern: str):
        """Invalidate all cache keys matching pattern."""
        if not self.config.enabled or not self.redis:
            return

        try:
            # Scan for matching keys
            keys = []
            async for key in self.redis.scan_iter(match=f"query:*{pattern}*"):
                keys.append(key)

            if keys:
                await self.redis.delete(*keys)
                logger.info(
                    f"Invalidated {len(keys)} cache entries matching: {pattern}"
                )

        except Exception as e:
            logger.error(f"Cache invalidation error: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0

        return {
            "enabled": self.config.enabled,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": f"{hit_rate:.2f}%",
            "total_requests": total_requests,
        }


class AsyncDatabasePool:
    """
    Async PostgreSQL connection pool with query optimization.

    Implements PERF-002: Async operations and connection pooling.
    """

    def __init__(
        self,
        dsn: str,
        min_size: int = 5,
        max_size: int = 20,
        cache_config: Optional[CacheConfig] = None,
    ):
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self.pool: Optional[asyncpg.Pool] = None

        # Query cache
        self.cache = QueryCache(cache_config or CacheConfig())

        # Query metrics
        self.query_metrics: List[QueryMetrics] = []
        self.slow_query_threshold_ms = 1000

        # Recommended indexes
        self.recommended_indexes: List[IndexDefinition] = []

        logger.info(f"AsyncDatabasePool initialized: min={min_size}, max={max_size}")

    async def connect(self):
        """Initialize connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                self.dsn,
                min_size=self.min_size,
                max_size=self.max_size,
                command_timeout=60,
            )

            await self.cache.connect()

            logger.info("Database pool connected successfully")

        except Exception as e:
            logger.error(f"Failed to create database pool: {e}")
            raise

    async def close(self):
        """Close connection pool."""
        if self.pool:
            await self.pool.close()

        await self.cache.close()
        logger.info("Database pool closed")

    @asynccontextmanager
    async def acquire(self):
        """Acquire connection from pool."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            yield conn

    async def execute(self, query: str, *params, timeout: float = 30) -> str:
        """Execute query without returning results."""
        start_time = time.time()

        try:
            async with self.acquire() as conn:
                result = await conn.execute(query, *params, timeout=timeout)

            execution_time = (time.time() - start_time) * 1000

            # Log execution
            logger.debug(f"Executed query in {execution_time:.2f}ms: {query[:100]}...")

            return result

        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise

    async def fetch(
        self,
        query: str,
        *params,
        timeout: float = 30,
        use_cache: bool = True,
        cache_ttl: Optional[int] = None,
    ) -> List[Dict]:
        """
        Fetch query results with caching and metrics.

        Implements PERF-002: Query execution time logging and caching.
        """
        query_hash = hashlib.sha256(f"{query}{params}".encode()).hexdigest()
        start_time = time.time()

        # Try cache first
        cache_hit = False
        if use_cache:
            cached_result = await self.cache.get(query, params)
            if cached_result is not None:
                execution_time = (time.time() - start_time) * 1000

                self._record_metrics(
                    QueryMetrics(
                        query_hash=query_hash,
                        query=query,
                        execution_time_ms=execution_time,
                        rows_returned=len(cached_result),
                        cache_hit=True,
                    )
                )

                return cached_result

        # Execute query
        try:
            async with self.acquire() as conn:
                # Get query plan for slow query analysis
                if logger.isEnabledFor(logging.DEBUG):
                    plan = await self._explain_query(conn, query, params)
                else:
                    plan = None

                rows = await conn.fetch(query, *params, timeout=timeout)

            execution_time = (time.time() - start_time) * 1000

            # Convert to list of dicts
            result = [dict(row) for row in rows]

            # Cache result
            if use_cache and result:
                await self.cache.set(query, params, result, cache_ttl)

            # Record metrics
            metrics = QueryMetrics(
                query_hash=query_hash,
                query=query,
                execution_time_ms=execution_time,
                rows_returned=len(result),
                cache_hit=cache_hit,
                plan=plan,
            )
            self._record_metrics(metrics)

            # Log slow queries
            if execution_time > self.slow_query_threshold_ms:
                logger.warning(
                    f"Slow query detected ({execution_time:.2f}ms): {query[:100]}..."
                )

                # Analyze for index recommendations
                if plan:
                    self._analyze_query_plan(query, plan)

            logger.debug(
                f"Fetched {len(result)} rows in {execution_time:.2f}ms: "
                f"{query[:100]}..."
            )

            return result

        except Exception as e:
            logger.error(f"Query fetch error: {e}")
            raise

    async def fetchrow(
        self,
        query: str,
        *params,
        timeout: float = 30,
        use_cache: bool = True,
    ) -> Optional[Dict]:
        """Fetch single row."""
        results = await self.fetch(query, *params, timeout=timeout, use_cache=use_cache)
        return results[0] if results else None

    async def fetchval(
        self,
        query: str,
        *params,
        timeout: float = 30,
        use_cache: bool = True,
    ) -> Any:
        """Fetch single value."""
        row = await self.fetchrow(query, *params, timeout=timeout, use_cache=use_cache)
        return list(row.values())[0] if row else None

    async def _explain_query(
        self, conn: asyncpg.Connection, query: str, params: Tuple
    ) -> Dict[str, Any]:
        """Get query execution plan."""
        try:
            explain_query = f"EXPLAIN (FORMAT JSON, ANALYZE) {query}"
            rows = await conn.fetch(explain_query, *params)

            if rows:
                plan = rows[0][0][0]  # Extract JSON plan
                return plan

        except Exception as e:
            logger.debug(f"Failed to explain query: {e}")

        return {}

    def _analyze_query_plan(self, query: str, plan: Dict[str, Any]):
        """
        Analyze query plan for optimization opportunities.

        Implements PERF-002: Automatic index recommendations.
        """
        # Look for sequential scans that could benefit from indexes
        if "Plan" in plan:
            self._check_plan_node(query, plan["Plan"])

    def _check_plan_node(self, query: str, node: Dict[str, Any]):
        """Recursively check plan nodes for optimization opportunities."""
        node_type = node.get("Node Type", "")

        # Sequential scan without index
        if node_type == "Seq Scan":
            table = node.get("Relation Name")
            filter_cond = node.get("Filter")

            if filter_cond and table:
                # Recommend index on filtered columns
                # This is simplified - production would parse filter conditions
                logger.info(
                    f"Index recommendation: Consider adding index on {table} "
                    f"for filter: {filter_cond}"
                )

                # Add to recommendations (simplified)
                # In production, would parse filter to extract actual columns
                recommendation = IndexDefinition(
                    table=table,
                    columns=["id"],  # Placeholder
                    index_type=IndexType.BTREE,
                )

                if recommendation not in self.recommended_indexes:
                    self.recommended_indexes.append(recommendation)

        # Check child nodes
        if "Plans" in node:
            for child in node["Plans"]:
                self._check_plan_node(query, child)

    def _record_metrics(self, metrics: QueryMetrics):
        """Record query metrics."""
        self.query_metrics.append(metrics)

        # Keep last 1000 metrics
        if len(self.query_metrics) > 1000:
            self.query_metrics = self.query_metrics[-1000:]

    def get_query_stats(self) -> Dict[str, Any]:
        """Get query performance statistics."""
        if not self.query_metrics:
            return {
                "total_queries": 0,
                "avg_execution_time_ms": 0,
                "p50_ms": 0,
                "p95_ms": 0,
                "p99_ms": 0,
                "cache_hit_rate": 0,
            }

        times = sorted([m.execution_time_ms for m in self.query_metrics])
        cache_hits = sum(1 for m in self.query_metrics if m.cache_hit)

        return {
            "total_queries": len(self.query_metrics),
            "avg_execution_time_ms": sum(times) / len(times),
            "p50_ms": times[int(len(times) * 0.50)],
            "p95_ms": times[int(len(times) * 0.95)],
            "p99_ms": times[int(len(times) * 0.99)],
            "cache_hit_rate": f"{cache_hits / len(self.query_metrics) * 100:.2f}%",
            "slow_queries": sum(1 for t in times if t > self.slow_query_threshold_ms),
        }

    async def create_indexes(self, indexes: List[IndexDefinition]):
        """Create database indexes."""
        for index in indexes:
            try:
                sql = index.to_sql()
                await self.execute(sql)
                logger.info(f"Created index: {index.get_name()}")

            except Exception as e:
                logger.error(f"Failed to create index {index.get_name()}: {e}")

    def get_index_recommendations(self) -> List[IndexDefinition]:
        """Get recommended indexes based on query patterns."""
        return self.recommended_indexes


# Example usage
async def main():
    logging.basicConfig(level=logging.INFO)

    # Initialize database pool
    dsn = "postgresql://user:pass@localhost/debvisor"
    cache_config = CacheConfig(
        host="localhost",
        port=6379,
        default_ttl=300,
        enabled=True,
    )

    pool = AsyncDatabasePool(dsn, cache_config=cache_config)
    await pool.connect()

    try:
        # Create table
        await pool.execute(
            """
            CREATE TABLE IF NOT EXISTS vms (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                status VARCHAR(50),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """
        )

        # Insert data
        await pool.execute(
            "INSERT INTO vms (name, status) VALUES ($1, $2)",
            "vm-001",
            "running",
        )

        # Query with caching
        result = await pool.fetch(
            "SELECT * FROM vms WHERE status = $1",
            "running",
            use_cache=True,
        )
        print(f"VMs: {result}")

        # Get statistics
        stats = pool.get_query_stats()
        print(f"Query stats: {stats}")

        cache_stats = pool.cache.get_stats()
        print(f"Cache stats: {cache_stats}")

        # Get index recommendations
        recommendations = pool.get_index_recommendations()
        if recommendations:
            print(f"Recommended indexes: {[idx.get_name() for idx in recommendations]}")

    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
