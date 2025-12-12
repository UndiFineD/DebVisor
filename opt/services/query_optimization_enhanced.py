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


"""
Database Query Optimization Framework - Enhanced Implementation

Provides:
- Advanced query analysis and optimization
- Automatic index recommendations
- Query plan generation and caching
- Performance metrics and monitoring
- N+1 query detection
- Field projection and pagination
- Batch query optimization

Author: DebVisor Team
Date: November 27, 2025
"""

import logging
from datetime import datetime, timezone
import time
from typing import Any, Optional, Dict, List, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import asyncio
import hashlib

_logger=logging.getLogger(__name__)


class QueryStatus(Enum):
    """Query execution status"""

    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CACHED = "cached"


@dataclass


class IndexRecommendation:
    """Recommendation for index creation"""

    table_name: str
    column_names: List[str]
    index_type: str = "btree"    # btree, hash, fulltext
    reason: str = ""
    estimated_improvement_percent: float = 0.0
    estimated_rows_examined_before: int = 0
    estimated_rows_examined_after: int = 0
    estimated_query_time_before_ms: float = 0.0
    estimated_query_time_after_ms: float = 0.0
    priority: int = 1    # 1=high, 2=medium, 3=low

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass


class QueryExecutionPlan:
    """Query execution plan"""

    query_id: str
    query_text: str
    estimated_cost: float = 0.0
    estimated_rows: int = 0
    table_access_order: List[str] = field(default_factory=list)
    indexes_used: List[str] = field(default_factory=list)
    join_strategy: str = ""    # nested_loop, hash_join, merge_join
    filters_applied: List[str] = field(default_factory=list)
    projections: List[str] = field(default_factory=list)
    created_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    ttl_seconds: int = 3600

    def is_expired(self) -> bool:
        """Check if plan is expired"""
        return (
            datetime.now(timezone.utc) - self.created_at
        ).total_seconds() > self.ttl_seconds

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        _d=asdict(self)
        d["created_at"] = self.created_at.isoformat()
        return d


@dataclass


class QueryProfile:
    """Detailed query profile"""

    query_id: str
    query_text: str
    status: QueryStatus
    start_time: datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    rows_scanned: int = 0
    rows_returned: int = 0
    rows_inserted: int = 0
    rows_updated: int = 0
    rows_deleted: int = 0
    indexes_used: List[str] = field(default_factory=list)
    query_plan: Optional[QueryExecutionPlan] = None
    cache_hit: bool = False
    optimizations_applied: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def finish(self, status: QueryStatus=QueryStatus.COMPLETED) -> None:
        """Mark query as finished"""
        self.end_time=datetime.now(timezone.utc)
        self.status = status
        if self.end_time and self.start_time:
            self.duration_ms=(self.end_time - self.start_time).total_seconds() * 1000

    def efficiency_ratio(self) -> float:
        """Calculate efficiency: rows_returned / rows_scanned"""
        if self.rows_scanned == 0:
            return 100.0 if self.rows_returned == 0 else 0.0
        return (self.rows_returned / self.rows_scanned) * 100

    def is_slow(self, threshold_ms: float=1000) -> bool:
        """Check if query is considered slow"""
        return self.duration_ms > threshold_ms

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "query_id": self.query_id,
            "query_text": self.query_text,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms,
            "rows_scanned": self.rows_scanned,
            "rows_returned": self.rows_returned,
            "rows_inserted": self.rows_inserted,
            "rows_updated": self.rows_updated,
            "rows_deleted": self.rows_deleted,
            "indexes_used": self.indexes_used,
            "cache_hit": self.cache_hit,
            "efficiency_ratio_percent": self.efficiency_ratio(),
            "optimizations_applied": self.optimizations_applied,
            "errors": self.errors,
            "query_plan": self.query_plan.to_dict() if self.query_plan else None,
        }


@dataclass


class QueryStatistics:
    """Aggregated statistics for query patterns"""

    query_signature: str
    total_executions: int = 0
    total_duration_ms: float = 0.0
    min_duration_ms: float=float("in")
    max_duration_ms: float = 0.0
    avg_duration_ms: float = 0.0
    median_duration_ms: float = 0.0
    total_rows_scanned: int = 0
    total_rows_returned: int = 0
    cache_hits: int = 0
    errors: int = 0
    last_executed: Optional[datetime] = None
    common_indexes: Dict[str, int] = field(default_factory=dict)
    slow_executions: int = 0

    def add_profile(self, profile: QueryProfile) -> None:
        """Add a query profile to statistics"""
        self.total_executions += 1
        self.total_duration_ms += profile.duration_ms
        self.min_duration_ms=min(self.min_duration_ms, profile.duration_ms)
        self.max_duration_ms=max(self.max_duration_ms, profile.duration_ms)
        self.avg_duration_ms = self.total_duration_ms / self.total_executions

        self.total_rows_scanned += profile.rows_scanned
        self.total_rows_returned += profile.rows_returned

        if profile.cache_hit:
            self.cache_hits += 1

        if profile.errors:
            self.errors += 1

        if profile.is_slow():
            self.slow_executions += 1

        self.last_executed=datetime.now(timezone.utc)

        # Track indexes used
        for idx in profile.indexes_used:
            self.common_indexes[idx] = self.common_indexes.get(idx, 0) + 1

    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        if self.total_executions == 0:
            return 0.0
        return (self.cache_hits / self.total_executions) * 100

    def slow_query_rate(self) -> float:
        """Calculate rate of slow queries"""
        if self.total_executions == 0:
            return 0.0
        return (self.slow_executions / self.total_executions) * 100

    def average_row_efficiency(self) -> float:
        """Calculate average row efficiency"""
        if self.total_rows_scanned == 0:
            return 100.0 if self.total_rows_returned == 0 else 0.0
        return (self.total_rows_returned / self.total_rows_scanned) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "query_signature": self.query_signature,
            "total_executions": self.total_executions,
            "total_duration_ms": self.total_duration_ms,
            "min_duration_ms": (
                self.min_duration_ms if self.min_duration_ms != float("inf") else 0
            ),
            "max_duration_ms": self.max_duration_ms,
            "avg_duration_ms": self.avg_duration_ms,
            "median_duration_ms": self.median_duration_ms,
            "total_rows_scanned": self.total_rows_scanned,
            "total_rows_returned": self.total_rows_returned,
            "cache_hit_rate_percent": self.cache_hit_rate(),
            "slow_query_rate_percent": self.slow_query_rate(),
            "average_row_efficiency_percent": self.average_row_efficiency(),
            "errors": self.errors,
            "slow_executions": self.slow_executions,
            "common_indexes": self.common_indexes,
            "last_executed": (
                self.last_executed.isoformat() if self.last_executed else None
            ),
        }


class QueryAnalyzer:
    """Analyzes queries for optimization opportunities"""

    @staticmethod

    def generate_signature(query_text: str) -> str:
        """Generate query signature for grouping similar queries"""
        # Normalize query: remove parameters, normalize whitespace
        _normalized=" ".join(query_text.upper().split())
        # Remove parameter placeholders
        _normalized=normalized.replace("?", "")

        return hashlib.sha256(normalized.encode()).hexdigest()[:16]

    @staticmethod
    async def analyze_query(query: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze query for optimization opportunities"""
        analysis: Dict[str, Any] = {"recommendations": [], "optimizations": [], "warnings": []}

        # Check for full table scans
        if "table" in query and "where" not in query:
            analysis["warnings"].append(
                "Full table scan - consider adding WHERE clause"
            )

        # Check for N+1 patterns
        if "joins" in query and len(query.get("joins", [])) > 3:
            analysis["recommendations"].append(
                "Consider using batch loading instead of multiple joins"
            )

        # Check for missing indexes
        if "filter_fields" in query:
            for field_name in query["filter_fields"]:
                analysis["recommendations"].append(
                    f"Consider creating index on field: {field_name}"
                )

        return analysis

    @staticmethod

    def recommend_indexes(query: Dict[str, Any]) -> List[IndexRecommendation]:
        """Recommend indexes for query optimization"""
        recommendations = []

        # Recommend indexes on filtered fields
        if "filter_fields" in query:
            _table=query.get("table", "unknown")
            for field_name in query["filter_fields"]:
                recommendations.append(
                    IndexRecommendation(
                        _table_name = table,
                        _column_names = [field_name],
                        _reason = "Field used in WHERE clause",
                        _estimated_improvement_percent = 50,
                        _priority = 1,
                    )
                )

        # Recommend composite indexes on join fields
        if "joins" in query:
            _table=query.get("table", "unknown")
            join_fields = []
            for join in query.get("joins", []):
                if "on" in join:
                    join_fields.extend(join["on"].split("="))

            if len(join_fields) > 1:
                recommendations.append(
                    IndexRecommendation(
                        _table_name = table,
                        _column_names = join_fields,
                        _reason = "Fields used in JOIN",
                        _estimated_improvement_percent = 30,
                        _priority = 2,
                        _index_type = "composite",
                    )
                )

        return recommendations


class QueryOptimizer:
    """Optimizes queries before execution"""

    @staticmethod
    async def optimize(query: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Optimize query and return optimized query + list of optimizations applied"""
        _optimized=query.copy()
        optimizations = []

        # Add projection if not specified
        if "projection" not in optimized and "select_fields" in query:
            optimized["projection"] = {field: 1 for field in query["select_fields"]}
            optimizations.append("projection")

        # Add pagination if not specified
        if "limit" not in optimized:
            optimized["limit"] = 100
            optimizations.append("pagination")

        # Push down filters
        if "filters" in optimized:
            filters = optimized["filters"]
            indexed = []
            expensive = []

            for filt in filters:
                if "indexed" in filt and filt["indexed"]:
                    indexed.append(filt)
                else:
                    expensive.append(filt)

            optimized["filters"] = indexed + expensive
            if indexed:
                optimizations.append("filter_pushdown")

        return optimized, optimizations


class QueryOptimizationEngine:
    """Central query optimization engine"""

    def __init__(self) -> None:
        self.profiles: List[QueryProfile] = []
        self.statistics: Dict[str, QueryStatistics] = {}
        self.execution_plans: Dict[str, QueryExecutionPlan] = {}
        self.index_recommendations: List[IndexRecommendation] = []
        self._lock=asyncio.Lock()

    async def start_query(self, query_text: str) -> QueryProfile:
        """Start profiling a query"""
        _query_id=hashlib.sha256(f"{query_text}:{time.time()}".encode()).hexdigest()[
            :12
        ]

        profile = QueryProfile(
            _query_id = query_id, query_text=query_text, status=QueryStatus.PENDING
        )

        async with self._lock:
            self.profiles.append(profile)

        return profile

    async def end_query(
        self,
        profile: QueryProfile,
        rows_scanned: int = 0,
        rows_returned: int = 0,
        optimizations: Optional[List[str]] = None,
        status: QueryStatus = QueryStatus.COMPLETED,
    ) -> None:
        """End profiling and record statistics"""
        profile.finish(status)
        profile.rows_scanned = rows_scanned
        profile.rows_returned = rows_returned

        if optimizations:
            profile.optimizations_applied = optimizations

        # Update statistics
        _signature=QueryAnalyzer.generate_signature(profile.query_text)

        async with self._lock:
            if signature not in self.statistics:
                self.statistics[signature] = QueryStatistics(query_signature=signature)

            self.statistics[signature].add_profile(profile)

        logger.debug(
            f"Query profiled: {profile.query_id} ({profile.duration_ms:.2f}ms, "
            f"{profile.rows_returned}/{profile.rows_scanned} rows)"
        )

    async def analyze_query(self, query_text: str) -> Dict[str, Any]:
        """Analyze query for optimization opportunities"""
        _analysis=await QueryAnalyzer.analyze_query({"query_text": query_text})

        # Get recommendations
        _recommendations=QueryAnalyzer.recommend_indexes({"query_text": query_text})
        analysis["index_recommendations"] = [r.to_dict() for r in recommendations]

        return analysis

    def get_slow_queries(self, threshold_ms: float=1000) -> List[QueryProfile]:
        """Find queries slower than threshold"""
        return [p for p in self.profiles if p.duration_ms > threshold_ms]

    def get_statistics(self, signature: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics for queries"""
        if signature:
            if signature in self.statistics:
                return {signature: self.statistics[signature].to_dict()}
            return {}

        return {sig: stats.to_dict() for sig, stats in self.statistics.items()}

    def detect_n_plus_one(self) -> List[Dict[str, Any]]:
        """Detect N+1 query patterns"""
        issues = []

        for signature, stats in self.statistics.items():
        # High execution count with low efficiency indicates potential N+1
            if stats.total_executions > 100 and stats.average_row_efficiency() < 30:
                issues.append(
                    {
                        "query_signature": signature,
                        "severity": "high",
                        "total_executions": stats.total_executions,
                        "efficiency_percent": stats.average_row_efficiency(),
                        "total_time_ms": stats.total_duration_ms,
                        "recommendation": "Consider using JOIN or batch loading",
                    }
                )

        return issues

    def get_optimization_report(self) -> Dict[str, Any]:
        """Generate comprehensive optimization report"""
        _slow_queries=self.get_slow_queries()
        _n_plus_one_issues=self.detect_n_plus_one()

        _top_slow=sorted(slow_queries, key=lambda p: p.duration_ms, reverse=True)[:10]

        return {
            "summary": {
                "total_profiles": len(self.profiles),
                "unique_queries": len(self.statistics),
                "slow_queries": len(slow_queries),
                "n_plus_one_issues": len(n_plus_one_issues),
                "total_time_ms": sum(p.duration_ms for p in self.profiles),
                "cache_hit_rate_percent": self._calculate_overall_cache_hit_rate(),
            },
            "slow_queries": [p.to_dict() for p in top_slow],
            "n_plus_one_issues": n_plus_one_issues,
            "statistics": self.get_statistics(),
            "recommendations": self._generate_recommendations(),
        }

    def _calculate_overall_cache_hit_rate(self) -> float:
        """Calculate overall cache hit rate"""
        _total_stats=sum(s.total_executions for s in self.statistics.values())
        if total_stats == 0:
            return 0.0

        _cache_hits=sum(s.cache_hits for s in self.statistics.values())
        return (cache_hits / total_stats) * 100

    def _generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        # Check for slow queries
        _slow=self.get_slow_queries(threshold_ms=500)
        if len(slow) > 0:
            recommendations.append(
                f"Found {len(slow)} queries slower than 500ms - "
                "add indexes on filtered columns"
            )

        # Check for N+1
        _n_plus_one=self.detect_n_plus_one()
        if len(n_plus_one) > 0:
            recommendations.append(
                f"Detected {len(n_plus_one)} potential N+1 query patterns - "
                "consider batching or JOIN operations"
            )

        # Check cache effectiveness
        _overall_cache_rate=self._calculate_overall_cache_hit_rate()
        if overall_cache_rate < 30:
            recommendations.append(
                "Low cache hit rate - consider enabling query result caching"
            )

        # Check for index usage
        index_usage: Dict[str, int] = {}
        for stats in self.statistics.values():
            for idx, count in stats.common_indexes.items():
                index_usage[idx] = index_usage.get(idx, 0) + count

        if not index_usage:
            recommendations.append(
                "No indexes detected in use - review and add indexes on filter columns"
            )

        return recommendations


# Global query optimization engine instance
_optimization_engine: Optional[QueryOptimizationEngine] = None


async def get_query_optimization_engine() -> QueryOptimizationEngine:
    """Get or create global optimization engine"""
    global _optimization_engine
    if _optimization_engine is None:
        _optimization_engine=QueryOptimizationEngine()
    return _optimization_engine
