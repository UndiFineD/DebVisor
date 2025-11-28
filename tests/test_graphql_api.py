#!/usr/bin/env python3
"""
Unit tests for GraphQL API implementation.

Tests for:
  - GraphQL schema definition
  - Query and mutation resolution
  - Data loaders and caching
  - Authentication and authorization
  - Integration with Flask
"""

import asyncio
import json
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone

import sys
from pathlib import Path

opt_path = Path(__file__).parent.parent / "opt"
sys.path.insert(0, str(opt_path))

from graphql_api import (
    GraphQLSchema, GraphQLResolver, GraphQLServer, GraphQLResponse,
    GraphQLError, QueryContext, DataLoader, ResourceType, OperationStatus
)
from graphql_integration import (
    GraphQLAuthenticator, GraphQLCache, GraphQLMiddleware, GraphQLMetrics
)


class TestGraphQLSchema(unittest.TestCase):
    """Tests for GraphQL schema."""

    def setUp(self):
        """Set up test fixtures."""
        self.schema = GraphQLSchema()

    def test_schema_initialization(self):
        """Test schema is properly initialized."""
        self.assertIsNotNone(self.schema.types)
        self.assertGreater(len(self.schema.types), 0)

    def test_query_type_exists(self):
        """Test Query type is defined."""
        query_type = self.schema.get_type("Query")
        self.assertIsNotNone(query_type)
        self.assertEqual(query_type["kind"], "object")

    def test_mutation_type_exists(self):
        """Test Mutation type is defined."""
        mutation_type = self.schema.get_type("Mutation")
        self.assertIsNotNone(mutation_type)
        self.assertEqual(mutation_type["kind"], "object")

    def test_subscription_type_exists(self):
        """Test Subscription type is defined."""
        subscription_type = self.schema.get_type("Subscription")
        self.assertIsNotNone(subscription_type)

    def test_query_fields(self):
        """Test Query fields are defined."""
        fields = self.schema.get_query_fields()
        self.assertIn("cluster", fields)
        self.assertIn("clusters", fields)
        self.assertIn("nodes", fields)
        self.assertIn("pods", fields)

    def test_mutation_fields(self):
        """Test Mutation fields are defined."""
        fields = self.schema.get_mutation_fields()
        self.assertIn("drainNode", fields)
        self.assertIn("scaleDeployment", fields)
        self.assertIn("executeCephOperation", fields)

    def test_custom_type_definitions(self):
        """Test custom types are properly defined."""
        types_to_check = ["Cluster", "Node", "Pod", "Metrics", "Operation"]
        for type_name in types_to_check:
            type_def = self.schema.get_type(type_name)
            self.assertIsNotNone(type_def)
            self.assertEqual(type_def["kind"], "object")
            self.assertIn("fields", type_def)


class TestDataLoader(unittest.TestCase):
    """Tests for DataLoader batching."""

    @staticmethod
    async def batch_load_fn(keys):
        """Sample batch load function."""
        await asyncio.sleep(0.01)
        return {key: f"value_{key}" for key in keys}

    def setUp(self):
        """Set up test fixtures."""
        self.loader = DataLoader(self.batch_load_fn, batch_size=10)

    async def test_load_single_key(self):
        """Test loading single key."""
        result = await self.loader.load("key1")
        self.assertIsNotNone(result)

    async def test_load_multiple_keys(self):
        """Test loading multiple keys."""
        results = await self.loader.load_many(["key1", "key2", "key3"])
        self.assertEqual(len(results), 3)

    async def test_cache_hit(self):
        """Test cache hits work correctly."""
        await self.loader.load("key1")
        cached_result = await self.loader.load("key1")
        self.assertEqual(len(self.loader.cache), 1)

    def test_batch_size_enforcement(self):
        """Test batch size is enforced."""
        self.assertEqual(self.loader.batch_size, 10)


class TestGraphQLResolver(unittest.TestCase):
    """Tests for GraphQL resolver."""

    def setUp(self):
        """Set up test fixtures."""
        self.schema = GraphQLSchema()
        self.resolver = GraphQLResolver(self.schema)

    async def test_resolve_simple_query(self):
        """Test resolving simple query."""
        query = "query { cluster(name: \"default\") { name } }"
        context = QueryContext(user_id="test", cluster="default")

        response = await self.resolver.resolve_query(query, context=context)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, GraphQLResponse)

    async def test_resolve_query_with_variables(self):
        """Test resolving query with variables."""
        query = "query { clusters(limit: 10) { name } }"
        variables = {"limit": 10}
        context = QueryContext(user_id="test", cluster="default")

        response = await self.resolver.resolve_query(
            query, variables=variables, context=context
        )

        self.assertIsNotNone(response)

    async def test_resolve_mutation(self):
        """Test resolving mutation."""
        mutation = "mutation { drainNode(cluster: \"default\", node: \"node1\", gracePeriod: 300) { id status } }"
        context = QueryContext(user_id="test", cluster="default")

        response = await self.resolver.resolve_mutation(mutation, context=context)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, GraphQLResponse)

    async def test_invalid_query_handling(self):
        """Test invalid query handling."""
        query = "invalid query syntax"
        context = QueryContext(user_id="test", cluster="default")

        response = await self.resolver.resolve_query(query, context=context)

        self.assertIsNotNone(response.errors)

    async def test_resolver_with_default_context(self):
        """Test resolver creates default context."""
        query = "query { cluster(name: \"default\") { name } }"

        response = await self.resolver.resolve_query(query)

        self.assertIsNotNone(response)


class TestGraphQLServer(unittest.TestCase):
    """Tests for GraphQL server."""

    def setUp(self):
        """Set up test fixtures."""
        self.server = GraphQLServer()

    async def test_handle_query_request(self):
        """Test handling query request."""
        request = {
            "query": "query { cluster(name: \"default\") { name } }",
            "context": {"cluster": "default"}
        }

        response = await self.server.handle_request(request)

        self.assertIn("data", response)

    async def test_handle_mutation_request(self):
        """Test handling mutation request."""
        request = {
            "mutation": "mutation { scaleDeployment(cluster: \"default\", deployment: \"app\", namespace: \"default\", replicas: 5) { id } }",
            "context": {"cluster": "default"}
        }

        response = await self.server.handle_request(request)

        self.assertIn("data", response)

    async def test_empty_request_handling(self):
        """Test handling empty request."""
        response = await self.server.handle_request({})

        self.assertIn("errors", response)

    def test_schema_introspection(self):
        """Test schema introspection."""
        introspection = self.server.get_schema_introspection()

        self.assertIn("types", introspection)
        self.assertIn("queryType", introspection)
        self.assertEqual(introspection["queryType"], "Query")


class TestGraphQLAuthenticator(unittest.TestCase):
    """Tests for authentication."""

    def setUp(self):
        """Set up test fixtures."""
        self.authenticator = GraphQLAuthenticator()

    def test_create_token(self):
        """Test token creation."""
        token = self.authenticator.create_token("user1", "cluster1")

        self.assertIsNotNone(token)
        self.assertTrue(token.startswith("token_"))

    def test_authenticate_valid_token(self):
        """Test authenticating valid token."""
        token = self.authenticator.create_token("user1", "cluster1")
        token_data = self.authenticator.authenticate_token(token)

        self.assertIsNotNone(token_data)
        self.assertEqual(token_data["user_id"], "user1")

    def test_authenticate_invalid_token(self):
        """Test authenticating invalid token."""
        token_data = self.authenticator.authenticate_token("invalid_token")

        self.assertIsNone(token_data)

    def test_token_expiration(self):
        """Test token expiration."""
        token = self.authenticator.create_token("user1", "cluster1", expires_in_hours=0)
        # Manually expire token
        self.authenticator.valid_tokens[token]["expires_at"] = datetime.now(timezone.utc) - timedelta(seconds=1)

        token_data = self.authenticator.authenticate_token(token)

        self.assertIsNone(token_data)

    def test_multiple_tokens(self):
        """Test multiple tokens."""
        token1 = self.authenticator.create_token("user1", "cluster1")
        token2 = self.authenticator.create_token("user2", "cluster2")

        self.assertNotEqual(token1, token2)
        self.assertEqual(len(self.authenticator.valid_tokens), 2)


class TestGraphQLCache(unittest.TestCase):
    """Tests for query caching."""

    def setUp(self):
        """Set up test fixtures."""
        self.cache = GraphQLCache(ttl_seconds=5)

    def test_set_and_get(self):
        """Test setting and getting cache value."""
        self.cache.set("key1", {"data": "value1"})
        result = self.cache.get("key1")

        self.assertEqual(result, {"data": "value1"})

    def test_cache_miss(self):
        """Test cache miss."""
        result = self.cache.get("nonexistent")

        self.assertIsNone(result)

    def test_cache_expiration(self):
        """Test cache expiration."""
        self.cache.set("key1", {"data": "value1"})
        self.cache.cache["key1"]["expires_at"] = datetime.now(timezone.utc) - timedelta(seconds=1)

        result = self.cache.get("key1")

        self.assertIsNone(result)

    def test_clear_cache(self):
        """Test clearing cache."""
        self.cache.set("key1", {"data": "value1"})
        self.cache.set("key2", {"data": "value2"})
        self.cache.clear()

        self.assertEqual(len(self.cache.cache), 0)

    def test_multiple_entries(self):
        """Test multiple cache entries."""
        for i in range(5):
            self.cache.set(f"key{i}", {"value": i})

        self.assertEqual(len(self.cache.cache), 5)


class TestGraphQLMetrics(unittest.TestCase):
    """Tests for metrics collection."""

    def setUp(self):
        """Set up test fixtures."""
        self.metrics = GraphQLMetrics()

    def test_record_query(self):
        """Test recording query."""
        self.metrics.record_query(0.5)

        self.assertEqual(self.metrics.query_count, 1)

    def test_record_error(self):
        """Test recording error."""
        self.metrics.record_query(0.5, error=True)

        self.assertEqual(self.metrics.error_count, 1)

    def test_record_cache_hit(self):
        """Test recording cache hit."""
        self.metrics.record_cache_hit()

        self.assertEqual(self.metrics.cache_hits, 1)

    def test_get_stats(self):
        """Test getting statistics."""
        self.metrics.record_query(0.1)
        self.metrics.record_query(0.2, error=True)
        self.metrics.record_cache_hit()

        stats = self.metrics.get_stats()

        self.assertEqual(stats["queries"], 2)
        self.assertEqual(stats["errors"], 1)
        self.assertEqual(stats["cache_hits"], 1)

    def test_error_rate_calculation(self):
        """Test error rate calculation."""
        self.metrics.record_query(0.1)
        self.metrics.record_query(0.1, error=True)

        stats = self.metrics.get_stats()

        self.assertEqual(stats["error_rate"], 50.0)

    def test_reset_metrics(self):
        """Test resetting metrics."""
        self.metrics.record_query(0.1)
        self.metrics.record_cache_hit()
        self.metrics.reset()

        self.assertEqual(self.metrics.query_count, 0)
        self.assertEqual(self.metrics.cache_hits, 0)


class TestIntegration(unittest.TestCase):
    """Integration tests."""

    async def test_end_to_end_query(self):
        """Test end-to-end query execution."""
        server = GraphQLServer()
        request = {
            "query": "query { cluster(name: \"default\") { name status } }",
            "context": {"cluster": "default"}
        }

        response = await server.handle_request(request)

        self.assertIn("data", response)

    async def test_auth_with_graphql(self):
        """Test authentication with GraphQL."""
        authenticator = GraphQLAuthenticator()
        token = authenticator.create_token("user1", "cluster1")
        token_data = authenticator.authenticate_token(token)

        self.assertIsNotNone(token_data)
        self.assertEqual(token_data["cluster"], "cluster1")

    async def test_caching_with_resolver(self):
        """Test caching with resolver."""
        cache = GraphQLCache()
        cache_key = "test_query"
        cache.set(cache_key, {"result": "cached_data"})

        result = cache.get(cache_key)

        self.assertEqual(result["result"], "cached_data")


if __name__ == "__main__":
    unittest.main()
