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

"""
GraphQL Flask Integration for DebVisor.

Integrates GraphQL server with Flask web framework for HTTP endpoint handling.

Features:
- GraphQL query and mutation endpoints
- WebSocket subscriptions
- Authentication and authorization
- Rate limiting and caching
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Any, Callable, Dict, Optional
from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphQLAuthenticator:
    """Handle GraphQL authentication and authorization."""

    def __init__(self) -> None:
        """Initialize authenticator."""
        self.valid_tokens: Dict[str, Dict[str, Any]] = {}

    def authenticate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate bearer token.

        Args:
            token: Bearer token

        Returns:
            Token data or None if invalid
        """
        if token in self.valid_tokens:
            token_data = self.valid_tokens[token]
            expires_at = token_data.get("expires_at")
            # Normalize expires_at to a datetime
            if isinstance(expires_at, datetime):
                exp_dt = expires_at
            elif isinstance(expires_at, str):
                try:
                # Expect ISO 8601 string; parse deterministically
                    exp_dt = datetime.fromisoformat(expires_at)
                    # If naive, assume UTC
                    if exp_dt.tzinfo is None:
                        exp_dt = exp_dt.replace(tzinfo=timezone.utc)
                except ValueError:
                    return None
            else:
                return None

            if exp_dt > datetime.now(timezone.utc):
                return token_data
        return None

    def create_token(
        self, user_id: str, cluster: str, expires_in_hours: int = 24
    ) -> str:
        """
        Create authentication token.

        Args:
            user_id: User identifier
            cluster: Cluster context
            expires_in_hours: Token expiration

        Returns:
            Bearer token
        """
        import uuid

        token = f"token_{uuid.uuid4().hex}"
        self.valid_tokens[token] = {
            "user_id": user_id,
            "cluster": cluster,
            "created_at": datetime.now(timezone.utc),
            "expires_at": datetime.now(timezone.utc)
            + timedelta(hours=expires_in_hours),
        }
        return token


class GraphQLCache:
    """Simple query result cache."""

    def __init__(self, ttl_seconds: int = 300):
        """
        Initialize cache.

        Args:
            ttl_seconds: Time to live for cache entries
        """
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value.

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        if key in self.cache:
            entry = self.cache[key]
            if entry["expires_at"] > datetime.now(timezone.utc):
                return entry["value"]
            del self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """
        Set cache value.

        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = {
            "value": value,
            "expires_at": datetime.now(timezone.utc)
            + timedelta(seconds=self.ttl_seconds),
        }

    def clear(self) -> None:
        """Clear all cached values."""
        self.cache.clear()


class GraphQLMiddleware:
    """Middleware for GraphQL request processing."""

    def __init__(self, authenticator: GraphQLAuthenticator, cache: GraphQLCache):
        """
        Initialize middleware.

        Args:
            authenticator: Authentication handler
            cache: Query result cache
        """
        self.authenticator = authenticator
        self.cache = cache

    def require_auth(self, f: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator for endpoints requiring authentication.

        Args:
            f: Endpoint function

        Returns:
            Decorated function
        """

        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Any:
            auth_header = request.headers.get("Authorization", "")

            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing authorization token"}), 401

            token = auth_header[7:]
            token_data = self.authenticator.authenticate_token(token)

            if not token_data:
                return jsonify({"error": "Invalid or expired token"}), 401

            # Add token data to request context
            request.token_data = token_data    # type: ignore

            return f(*args, **kwargs)

        return decorated_function


def create_graphql_blueprint(graphql_server: Any) -> Blueprint:
    """
    Create Flask blueprint for GraphQL endpoints.

    Args:
        graphql_server: GraphQL server instance

    Returns:
        Blueprint with GraphQL endpoints
    """
    bp = Blueprint("graphql", __name__, url_prefix="/graphql")

    authenticator = GraphQLAuthenticator()
    cache = GraphQLCache(ttl_seconds=300)
    middleware = GraphQLMiddleware(authenticator, cache)
    limiter = Limiter(key_func=get_remote_address)

    @bp.route("/query", methods=["POST"])
    @middleware.require_auth
    @limiter.limit("100 per minute")
    def graphql_query() -> Any:
        """
        GraphQL query endpoint.

        Returns:
            JSON response with query results
        """
        try:
            body = request.get_json()

            if not body:
                return jsonify({"error": "Empty request body"}), 400

            query = body.get("query")
            if not query:
                return jsonify({"error": "Missing query"}), 400

            # Generate cache key
            cache_key = (
                f"query_{hash(query)}_{request.token_data.get('cluster', 'default')}"    # type: ignore
            )

            # Check cache
            cached_result = cache.get(cache_key)
            if cached_result:
                cached_result["cached"] = True
                return jsonify(cached_result)

            # Execute query
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                response = loop.run_until_complete(graphql_server.handle_request(body))
            finally:
                loop.close()

            # Cache successful response
            if not response.get("errors"):
                cache.set(cache_key, response)

            return jsonify(response)

        except Exception as e:
            logger.error(f"GraphQL query error: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @bp.route("/mutation", methods=["POST"])
    @middleware.require_auth
    @limiter.limit("50 per minute")
    def graphql_mutation() -> Any:
        """
        GraphQL mutation endpoint.

        Returns:
            JSON response with mutation results
        """
        try:
            body = request.get_json()

            if not body:
                return jsonify({"error": "Empty request body"}), 400

            mutation = body.get("mutation")
            if not mutation:
                return jsonify({"error": "Missing mutation"}), 400

            # Execute mutation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                response = loop.run_until_complete(graphql_server.handle_request(body))
            finally:
                loop.close()

            return jsonify(response)

        except Exception as e:
            logger.error(f"GraphQL mutation error: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @bp.route("/schema", methods=["GET"])
    @middleware.require_auth
    def schema_introspection() -> Any:
        """
        Get GraphQL schema introspection.

        Returns:
            Schema definition
        """
        try:
            schema = graphql_server.get_schema_introspection()
            return jsonify(schema)

        except Exception as e:
            logger.error(f"Schema introspection error: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @bp.route("/auth/token", methods=["POST"])
    def create_token() -> Any:
        """
        Create authentication token.

        Returns:
            Bearer token
        """
        try:
            body = request.get_json()
            user_id = body.get("user_id", "anonymous")
            cluster = body.get("cluster", "default")

            token = authenticator.create_token(user_id, cluster)

            return jsonify(
                {"token": token, "expires_in_hours": 24, "token_type": "Bearer"}
            )

        except Exception as e:
            logger.error(f"Token creation error: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @bp.route("/health", methods=["GET"])
    def health_check() -> Any:
        """
        Health check endpoint.

        Returns:
            Health status
        """
        return jsonify(
            {
                "status": "healthy",
                "service": "graphql",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    return bp


class GraphQLMetrics:
    """Metrics collection for GraphQL operations."""

    def __init__(self) -> None:
        """Initialize metrics."""
        self.query_count = 0
        self.mutation_count = 0
        self.error_count = 0
        self.total_execution_time = 0.0
        self.cache_hits = 0

    def record_query(self, execution_time: float, error: bool = False) -> None:
        """
        Record query execution.

        Args:
            execution_time: Execution time in seconds
            error: Whether query failed
        """
        self.query_count += 1
        self.total_execution_time += execution_time
        if error:
            self.error_count += 1

    def record_cache_hit(self) -> None:
        """Record cache hit."""
        self.cache_hits += 1

    def get_stats(self) -> Dict[str, Any]:
        """
        Get metrics statistics.

        Returns:
            Metrics dictionary
        """
        total = self.query_count + self.mutation_count
        avg_time = self.total_execution_time / total if total > 0 else 0

        return {
            "queries": self.query_count,
            "mutations": self.mutation_count,
            "errors": self.error_count,
            "cache_hits": self.cache_hits,
            "average_execution_time_ms": avg_time * 1000,
            "error_rate": (self.error_count / total * 100) if total > 0 else 0,
        }

    def reset(self) -> None:
        """Reset all metrics."""
        self.query_count = 0
        self.mutation_count = 0
        self.error_count = 0
        self.total_execution_time = 0.0
        self.cache_hits = 0
