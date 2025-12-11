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
Query Optimization for DebVisor Services

Provides query analysis, optimization strategies, and lazy loading mechanisms
for efficient data retrieval and API response performance.

Features:
    - Query analysis and optimization suggestions
    - Lazy loading with pagination
    - Result filtering and projection
    - N+1 query detection
    - Query plan caching
    - Batch query execution
    - Performance profiling

Author: DebVisor Team
Date: 2025-11-26
"""

import logging
from typing import TypeVar
from typing import Tuple
from datetime import datetime, timezone
from typing import Any, Optional, Dict, List
from dataclasses import dataclass, field, asdict
from enum import Enum
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

# Type variable for generic query results
T = TypeVar("T")


class QueryOptimizationType(Enum):
    """Types of query optimizations"""

    INDEX_USAGE = "index_usage"
    EARLY_TERMINATION = "early_termination"
    PROJECTION = "projection"    # Select only needed fields
    LAZY_LOADING = "lazy_loading"
    PAGINATION = "pagination"
    BATCH_LOADING = "batch_loading"
    CACHING = "caching"
    FILTER_PUSHDOWN = "filter_pushdown"


@dataclass
class QueryProfile:
    """Profile for a single query execution"""

    query_name: str
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    rows_fetched: int = 0
    rows_examined: int = 0
    indexes_used: List[str] = field(default_factory=list)
    optimizations_applied: List[QueryOptimizationType] = field(default_factory=list)
    cache_hit: bool = False
    error: Optional[str] = None

    def finish(self, rows_fetched: int = 0, rows_examined: int = 0) -> None:
        """Mark query as finished"""
        self.end_time = datetime.now(timezone.utc)
        self.rows_fetched = rows_fetched
        self.rows_examined = rows_examined
        self.duration_ms = (self.end_time - self.start_time).total_seconds() * 1000

    def efficiency_ratio(self) -> float:
        """Calculate efficiency: rows_fetched / rows_examined"""
        if self.rows_examined == 0:
            return 0.0
        return (self.rows_fetched / self.rows_examined) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        d = asdict(self)
        d["start_time"] = self.start_time.isoformat()
        d["end_time"] = self.end_time.isoformat() if self.end_time else None
        d["optimizations_applied"] = [opt.value for opt in self.optimizations_applied]
        d["efficiency_ratio_percent"] = self.efficiency_ratio()
        return d


@dataclass
class QueryStatistics:
    """Aggregated statistics for query patterns"""

    query_name: str
    total_executions: int = 0
    total_duration_ms: float = 0.0
    min_duration_ms: float = float("inf")
    max_duration_ms: float = 0.0
    avg_duration_ms: float = 0.0
    errors: int = 0
    cache_hits: int = 0
    avg_efficiency_ratio: float = 0.0

    def add_profile(self, profile: QueryProfile) -> None:
        """Add a query profile to statistics"""
        self.total_executions += 1
        self.total_duration_ms += profile.duration_ms
        self.min_duration_ms = min(self.min_duration_ms, profile.duration_ms)
        self.max_duration_ms = max(self.max_duration_ms, profile.duration_ms)
        self.avg_duration_ms = self.total_duration_ms / self.total_executions

        if profile.error:
            self.errors += 1
        if profile.cache_hit:
            self.cache_hits += 1

        # Running average of efficiency
        self.avg_efficiency_ratio = (
            self.avg_efficiency_ratio + profile.efficiency_ratio()
        ) / 2

    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        if self.total_executions == 0:
            return 0.0
        return (self.cache_hits / self.total_executions) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "query_name": self.query_name,
            "total_executions": self.total_executions,
            "total_duration_ms": self.total_duration_ms,
            "min_duration_ms": (
                self.min_duration_ms if self.min_duration_ms != float("inf") else 0
            ),
            "max_duration_ms": self.max_duration_ms,
            "avg_duration_ms": self.avg_duration_ms,
            "errors": self.errors,
            "cache_hits": self.cache_hits,
            "cache_hit_rate_percent": self.cache_hit_rate(),
            "avg_efficiency_ratio_percent": self.avg_efficiency_ratio,
        }


class QueryOptimizer(ABC):
    """
    Abstract query optimizer.

    Base class for all query optimization strategies.
    Subclasses implement specific optimization techniques.
    """

    @abstractmethod
    async def optimize(
        self, query: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[QueryOptimizationType]]:
        """
        Optimize query and return optimized query + list of optimizations applied.

        Args:
            query: Query dictionary to optimize

        Returns:
            Tuple of (optimized query dict, list of optimizations applied)
        """
        pass

    @abstractmethod
    async def analyze(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze query and return suggestions.

        Args:
            query: Query dictionary to analyze

        Returns:
            Dictionary with optimizer name and suggestions list
        """
        pass


class ProjectionOptimizer(QueryOptimizer):
    """
    Optimize queries by projecting only needed fields.

    Reduces bandwidth and processing by limiting returned fields
    to only those explicitly requested.
    """

    async def optimize(
        self, query: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[QueryOptimizationType]]:
        """
        Add projection if not present.

        Args:
            query: Query dictionary with optional 'requested_fields'

        Returns:
            Tuple of (optimized query, list of optimizations)
        """
        optimized = query.copy()
        optimizations: List[QueryOptimizationType] = []

        # If query has requested_fields, project only those
        if "requested_fields" in query and "projection" not in query:
            optimized["projection"] = {field: 1 for field in query["requested_fields"]}
            optimizations.append(QueryOptimizationType.PROJECTION)

        return optimized, optimizations

    async def analyze(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest projection if querying many fields.

        Args:
            query: Query dictionary to analyze

        Returns:
            Analysis dictionary with suggestions
        """
        suggestions: List[str] = []

        if "projection" not in query:
            suggestions.append(
                "Consider projecting only needed fields to reduce bandwidth"
            )

        return {"optimizer": "ProjectionOptimizer", "suggestions": suggestions}


class PaginationOptimizer(QueryOptimizer):
    """
    Optimize large result sets with pagination.

    Automatically adds limits to queries that might return
    large result sets to prevent memory issues.
    """

    def __init__(self, default_page_size: int = 100) -> None:
        """
        Initialize pagination optimizer.

        Args:
            default_page_size: Default number of results per page
        """
        self.default_page_size = default_page_size

    async def optimize(
        self, query: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[QueryOptimizationType]]:
        """
        Add pagination if result size might be large.

        Args:
            query: Query dictionary

        Returns:
            Tuple of (optimized query with limit, list of optimizations)
        """
        optimized = query.copy()
        optimizations: List[QueryOptimizationType] = []

        # If no limit specified, add pagination
        if "limit" not in query and "page_size" not in query:
            optimized["limit"] = self.default_page_size
            optimizations.append(QueryOptimizationType.PAGINATION)

        return optimized, optimizations

    async def analyze(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest pagination for large queries.

        Args:
            query: Query dictionary to analyze

        Returns:
            Analysis dictionary with suggestions
        """
        suggestions: List[str] = []

        # Check if likely to return many rows
        if "filter" not in query or "limit" not in query:
            suggestions.append("Large result sets benefit from pagination with limits")

        return {"optimizer": "PaginationOptimizer", "suggestions": suggestions}


class FilterPushdownOptimizer(QueryOptimizer):
    """
    Push filters down to reduce rows examined.

    Reorders filters so indexed fields are checked first,
    reducing the number of rows that need expensive filtering.
    """

    async def optimize(
        self, query: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[QueryOptimizationType]]:
        """
        Optimize filter placement.

        Args:
            query: Query dictionary with optional 'filters' list

        Returns:
            Tuple of (optimized query with reordered filters, list of optimizations)
        """
        optimized = query.copy()
        optimizations: List[QueryOptimizationType] = []

        # Move expensive filters after index-based filters
        if "filters" in query:
            filters = query["filters"]
            indexed: List[Any] = []
            expensive: List[Any] = []

            for filt in filters:
                if "indexed_field" in filt:
                    indexed.append(filt)
                else:
                    expensive.append(filt)

            # Apply indexed filters first
            optimized["filters"] = indexed + expensive
            if len(indexed) > 0:
                optimizations.append(QueryOptimizationType.FILTER_PUSHDOWN)

        return optimized, optimizations

    async def analyze(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest filter optimization.

        Args:
            query: Query dictionary to analyze

        Returns:
            Analysis dictionary with suggestions
        """
        suggestions: List[str] = []

        if "filters" in query:
            suggestions.append("Ensure filters on indexed fields are applied first")

        return {"optimizer": "FilterPushdownOptimizer", "suggestions": suggestions}


class LazyLoadingOptimizer(QueryOptimizer):
    """
    Enable lazy loading for relationships.

    Prevents eager loading of related entities by default,
    helping avoid N+1 query problems.
    """

    async def optimize(
        self, query: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[QueryOptimizationType]]:
        """
        Enable lazy loading.

        Args:
            query: Query dictionary with optional 'relationships'

        Returns:
            Tuple of (optimized query with lazy_load flag, list of optimizations)
        """
        optimized = query.copy()
        optimizations: List[QueryOptimizationType] = []

        # If loading relationships, enable lazy loading
        if "relationships" in query and "eager_load" not in query:
            optimized["lazy_load"] = True
            optimizations.append(QueryOptimizationType.LAZY_LOADING)

        return optimized, optimizations

    async def analyze(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest lazy loading.

        Args:
            query: Query dictionary to analyze

        Returns:
            Analysis dictionary with suggestions
        """
        suggestions: List[str] = []

        if "relationships" in query:
            suggestions.append("Use lazy loading to avoid N+1 query problems")

        return {"optimizer": "LazyLoadingOptimizer", "suggestions": suggestions}


@dataclass
class PaginationParams:
    """Pagination parameters"""

    page: int = 1
    page_size: int = 100
    sort_by: Optional[str] = None
    sort_order: str = "asc"

    @property
    def offset(self) -> int:
        """Calculate offset"""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit"""
        return self.page_size


class PaginatedResult:
    """
    Result of a paginated query.

    Encapsulates paginated data with metadata for navigation.

    Attributes:
        items: List of result items
        total_count: Total items across all pages
        page: Current page number
        page_size: Items per page
        has_next: Whether there are more pages
        has_previous: Whether there are previous pages
    """

    def __init__(
        self,
        items: List[Any],
        total_count: int,
        page: int,
        page_size: int,
        has_next: bool = False,
        has_previous: bool = False,
    ) -> None:
        """
        Initialize paginated result.

        Args:
            items: List of result items
            total_count: Total items across all pages
            page: Current page number
            page_size: Items per page
            has_next: Whether there are more pages
            has_previous: Whether there are previous pages
        """
        self.items = items
        self.total_count = total_count
        self.page = page
        self.page_size = page_size
        self.has_next = has_next
        self.has_previous = has_previous

    @property
    def total_pages(self) -> int:
        """
        Calculate total pages.

        Returns:
            Total number of pages
        """
        return (self.total_count + self.page_size - 1) // self.page_size

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary.

        Returns:
            Dictionary with items and pagination metadata
        """
        return {
            "items": self.items,
            "pagination": {
                "page": self.page,
                "page_size": self.page_size,
                "total_count": self.total_count,
                "total_pages": self.total_pages,
                "has_next": self.has_next,
                "has_previous": self.has_previous,
            },
        }


class QueryOptimizationEngine:
    """
    Central query optimization engine.

    Orchestrates multiple optimization strategies and provides
    query profiling, statistics, and N+1 detection.

    Attributes:
        optimizers: List of QueryOptimizer instances
        profiles: List of QueryProfile instances
        statistics: Dictionary of QueryStatistics by query name
    """

    def __init__(self) -> None:
        """Initialize optimization engine with default optimizers."""
        self.optimizers: List[QueryOptimizer] = [
            ProjectionOptimizer(),
            PaginationOptimizer(),
            FilterPushdownOptimizer(),
            LazyLoadingOptimizer(),
        ]
        self.profiles: List[QueryProfile] = []
        self.statistics: Dict[str, QueryStatistics] = {}

    async def optimize_query(
        self, query: Dict[str, Any], query_name: str = "unnamed"
    ) -> Tuple[Dict[str, Any], List[QueryOptimizationType]]:
        """
        Run all optimizers on a query.

        Args:
            query: Query dictionary to optimize
            query_name: Name for logging and profiling

        Returns:
            Tuple of (optimized query, list of all optimizations applied)
        """
        optimized = query.copy()
        all_optimizations: List[QueryOptimizationType] = []

        for optimizer in self.optimizers:
            try:
                optimized, optimizations = await optimizer.optimize(optimized)
                all_optimizations.extend(optimizations)
            except Exception as e:
                logger.warning(f"Optimizer {optimizer.__class__.__name__} failed: {e}")

        return optimized, all_optimizations

    async def analyze_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze query for optimization opportunities.

        Args:
            query: Query dictionary to analyze

        Returns:
            Analysis dictionary with aggregated suggestions
        """
        analysis: Dict[str, Any] = {"suggestions": [], "optimizations": []}

        for optimizer in self.optimizers:
            try:
                result = await optimizer.analyze(query)
                if "suggestions" in result:
                    analysis["suggestions"].extend(result["suggestions"])
            except Exception as e:
                logger.warning(f"Analyzer {optimizer.__class__.__name__} failed: {e}")

        return analysis

    def start_profile(self, query_name: str) -> QueryProfile:
        """
        Start profiling a query.

        Args:
            query_name: Name for the query profile

        Returns:
            QueryProfile instance for tracking
        """
        profile = QueryProfile(query_name=query_name)
        self.profiles.append(profile)
        return profile

    def end_profile(
        self,
        profile: QueryProfile,
        rows_fetched: int = 0,
        rows_examined: int = 0,
        optimizations: Optional[List[QueryOptimizationType]] = None,
    ) -> None:
        """
        End profiling and record statistics.

        Args:
            profile: QueryProfile from start_profile
            rows_fetched: Number of rows returned
            rows_examined: Number of rows scanned
            optimizations: List of optimizations applied
        """
        profile.finish(rows_fetched, rows_examined)
        if optimizations:
            profile.optimizations_applied = optimizations

        # Update statistics
        if profile.query_name not in self.statistics:
            self.statistics[profile.query_name] = QueryStatistics(
                query_name=profile.query_name
            )

        self.statistics[profile.query_name].add_profile(profile)
        logger.debug(
            f"Query profiled: {profile.query_name} ({profile.duration_ms:.2f}ms)"
        )

    def get_statistics(self, query_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics for queries.

        Args:
            query_name: Optional filter by query name

        Returns:
            Dictionary of statistics keyed by query name
        """
        if query_name:
            if query_name in self.statistics:
                return {query_name: self.statistics[query_name].to_dict()}
            return {}

        return {name: stats.to_dict() for name, stats in self.statistics.items()}

    def get_slow_queries(self, threshold_ms: float = 1000) -> List[QueryProfile]:
        """
        Find queries slower than threshold.

        Args:
            threshold_ms: Minimum duration in milliseconds

        Returns:
            List of slow QueryProfile instances
        """
        return [p for p in self.profiles if p.duration_ms > threshold_ms]

    def detect_n_plus_one(self) -> List[Dict[str, Any]]:
        """
        Detect N+1 query patterns.

        Analyzes statistics for queries that run frequently
        with low efficiency, indicating potential N+1 issues.

        Returns:
            List of issue dictionaries with query, severity, reason, and statistics
        """
        issues: List[Dict[str, Any]] = []

        for query_name, stats in self.statistics.items():
            if stats.total_executions > 10:
                # Check if query runs many times in short succession
                if stats.avg_efficiency_ratio < 50:    # Low efficiency
                    issues.append(
                        {
                            "query": query_name,
                            "severity": "high",
                            "reason": "Low efficiency ratio suggests potential N+1",
                            "statistics": stats.to_dict(),
                        }
                    )

        return issues

    def get_optimization_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive optimization report.

        Returns:
            Dictionary with summary, slow queries, N+1 issues,
            statistics, and recommendations
        """
        slow_queries = self.get_slow_queries()
        n_plus_one_issues = self.detect_n_plus_one()

        return {
            "summary": {
                "total_profiles": len(self.profiles),
                "unique_queries": len(self.statistics),
                "slow_queries": len(slow_queries),
                "n_plus_one_issues": len(n_plus_one_issues),
            },
            "slow_queries": [p.to_dict() for p in slow_queries[:10]],
            "n_plus_one_issues": n_plus_one_issues,
            "statistics": self.get_statistics(),
            "recommendations": self._generate_recommendations(),
        }

    def _generate_recommendations(self) -> List[str]:
        """
        Generate optimization recommendations.

        Returns:
            List of recommendation strings based on collected data
        """
        recommendations: List[str] = []

        # Check for slow queries
        slow = self.get_slow_queries(threshold_ms=500)
        if slow:
            recommendations.append(
                f"Found {len(slow)} queries slower than 500ms - consider adding indexes"
            )

        # Check for N+1
        n_plus_one = self.detect_n_plus_one()
        if n_plus_one:
            recommendations.append(
                f"Detected {len(n_plus_one)} potential N+1 query patterns"
            )

        # Check cache effectiveness
        cache_hits = sum(stats.cache_hits for stats in self.statistics.values())
        if cache_hits == 0 and self.profiles:
            recommendations.append(
                "No cache hits detected - consider enabling query caching"
            )

        return recommendations


# Global query optimization engine
_optimization_engine: Optional[QueryOptimizationEngine] = None


async def get_optimization_engine() -> QueryOptimizationEngine:
    """
    Get or create global optimization engine.

    Returns:
        Global QueryOptimizationEngine instance
    """
    global _optimization_engine
    if _optimization_engine is None:
        _optimization_engine = QueryOptimizationEngine()
    return _optimization_engine
