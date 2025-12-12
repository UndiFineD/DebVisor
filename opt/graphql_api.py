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

"""
GraphQL API Layer for DebVisor.

Provides GraphQL schema with queries, mutations, and subscriptions for
comprehensive cluster management and monitoring.

Features:
- Type-safe GraphQL schema
- Query optimization with DataLoader
- Real-time subscriptions
- Mutation support for operational tasks
"""

from datetime import datetime, timezone
import asyncio
import json
import logging
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResourceType(Enum):
    """Supported resource types."""

    CLUSTER = "cluster"
    NODE = "node"
    POD = "pod"
    VOLUME = "volume"
    SERVICE = "service"
    INGRESS = "ingress"
    CONFIG = "config"
    VM = "vm"
    HOST = "host"


class OperationStatus(Enum):
    """Operation execution status."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class GraphQLError:
    """GraphQL error representation."""

    message: str
    code: str
    extensions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphQLResponse:
    """GraphQL response structure."""

    data: Optional[Dict[str, Any]] = None
    errors: List[GraphQLError] = field(default_factory=list)
    extensions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryContext:
    """GraphQL query execution context."""

    user_id: str
    cluster: str
    namespace: Optional[str] = None
    timeout_seconds: int = 30
    enable_cache: bool = True


@dataclass
class DataLoaderCache:
    """Cache for batched data loading."""

    cache: Dict[str, Any] = field(default_factory=dict)
    pending_keys: Set[str] = field(default_factory=set)
    batch_size: int = 100


class DataLoader:
    """
    DataLoader for batching and caching queries.

    Reduces N+1 query problems by batching multiple requests.
    """

    def __init__(self, batch_load_fn: Callable[..., Any], batch_size: int = 100):
        """
        Initialize DataLoader.

        Args:
            batch_load_fn: Async function to batch load data
            batch_size: Maximum batch size
        """
        self.batch_load_fn = batch_load_fn
        self.batch_size = batch_size
        self.cache: Dict[str, Any] = {}
        self.queue: List[str] = []

    async def load(self, key: str) -> Any:
        """
        Load single item, using cache or queueing for batch.

        Args:
            key: Item key

        Returns:
            Loaded item
        """
        if key in self.cache:
            return self.cache[key]

        self.queue.append(key)

        if len(self.queue) >= self.batch_size:
            await self._flush()
            return self.cache.get(key)

        # Simulate async batch loading with small delay to allow batching
        await asyncio.sleep(0.01)

        # Flush pending items to process the queue
        await self._flush()

        return self.cache.get(key)

    async def load_many(self, keys: List[str]) -> List[Any]:
        """
        Load multiple items.

        Args:
            keys: List of keys

        Returns:
            List of loaded items
        """
        results = []
        for key in keys:
            result = await self.load(key)
            results.append(result)

        await self._flush()
        return results

    async def _flush(self) -> None:
        """Flush pending keys through batch loader."""
        if not self.queue:
            return

        keys = self.queue[: self.batch_size]
        self.queue = self.queue[self.batch_size :]

        try:
            results = await self.batch_load_fn(keys)
            # Handle both dict and list results
            if isinstance(results, dict):
                for key in keys:
                    if key in results:
                        self.cache[key] = results[key]
            else:
                for key, result in zip(keys, results):
                    self.cache[key] = result
        except Exception as e:
            logger.error(f"Batch load error: {e}")


class GraphQLSchema:
    """
    GraphQL schema definition for DebVisor.

    Defines queries, mutations, and subscriptions for infrastructure
    management and monitoring.
    """

    def __init__(self) -> None:
        """Initialize GraphQL schema."""
        self.types: Dict[str, Dict[str, Any]] = {}
        self.resolvers: Dict[str, Callable[..., Any]] = {}
        self.subscriptions: Dict[str, Callable[..., Any]] = {}
        self._build_schema()

    def _build_schema(self) -> None:
        """Build complete GraphQL schema."""
        # Scalar types
        self.types["DateTime"] = {"kind": "scalar", "description": "ISO 8601 datetime"}
        self.types["JSON"] = {"kind": "scalar", "description": "JSON object"}

        # Query type
        self.types["Query"] = {
            "kind": "object",
            "fields": {
                "cluster": {
                    "type": "Cluster",
                    "args": {"name": "String!"},
                    "description": "Get cluster by name",
                },
                "clusters": {
                    "type": "[Cluster]",
                    "args": {
                        "limit": "Int",
                        "offset": "Int",
                        "filter": "ClusterFilter",
                    },
                    "description": "List all clusters",
                },
                "nodes": {
                    "type": "[Node]",
                    "args": {
                        "cluster": "String!",
                        "limit": "Int",
                        "filter": "NodeFilter",
                    },
                    "description": "List cluster nodes",
                },
                "pods": {
                    "type": "[Pod]",
                    "args": {
                        "cluster": "String!",
                        "namespace": "String",
                        "limit": "Int",
                    },
                    "description": "List pods",
                },
                "resources": {
                    "type": "[Resource]",
                    "args": {"cluster": "String!", "type": "ResourceType"},
                    "description": "List resources by type",
                },
                "metrics": {
                    "type": "Metrics",
                    "args": {"cluster": "String!"},
                    "description": "Get cluster metrics",
                },
                "operations": {
                    "type": "[Operation]",
                    "args": {
                        "cluster": "String!",
                        "status": "OperationStatus",
                        "limit": "Int",
                    },
                    "description": "List operations",
                },
            },
        }

        # Mutation type
        self.types["Mutation"] = {
            "kind": "object",
            "fields": {
                "drainNode": {
                    "type": "Operation",
                    "args": {
                        "cluster": "String!",
                        "node": "String!",
                        "gracePeriod": "Int",
                    },
                    "description": "Drain Kubernetes node",
                },
                "migrateWorkload": {
                    "type": "Operation",
                    "args": {
                        "cluster": "String!",
                        "workload": "String!",
                        "namespace": "String!",
                        "targetCluster": "String!",
                    },
                    "description": "Migrate workload to cluster",
                },
                "scaleDeployment": {
                    "type": "Operation",
                    "args": {
                        "cluster": "String!",
                        "deployment": "String!",
                        "namespace": "String!",
                        "replicas": "Int!",
                    },
                    "description": "Scale deployment replicas",
                },
                "executeCephOperation": {
                    "type": "Operation",
                    "args": {
                        "cluster": "String!",
                        "operation": "String!",
                        "parameters": "JSON",
                    },
                    "description": "Execute Ceph operation",
                },
                "configureNetwork": {
                    "type": "Operation",
                    "args": {
                        "cluster": "String!",
                        "interface": "String!",
                        "configuration": "JSON!",
                    },
                    "description": "Configure network interface",
                },
            },
        }

        # Subscription type
        self.types["Subscription"] = {
            "kind": "object",
            "fields": {
                "clusterEvents": {
                    "type": "Event",
                    "args": {"cluster": "String!"},
                    "description": "Subscribe to cluster events",
                },
                "operationProgress": {
                    "type": "Operation",
                    "args": {"operationId": "String!"},
                    "description": "Subscribe to operation progress",
                },
                "metricsUpdates": {
                    "type": "Metrics",
                    "args": {"cluster": "String!", "interval": "Int"},
                    "description": "Subscribe to metrics updates",
                },
            },
        }

        # Object types
        self.types["Cluster"] = {
            "kind": "object",
            "fields": {
                "name": "String!",
                "type": "String!",
                "status": "String!",
                "version": "String!",
                "nodeCount": "Int!",
                "podCount": "Int!",
                "nodes": "[Node]",
                "metrics": "Metrics",
                "createdAt": "DateTime!",
            },
        }

        self.types["Node"] = {
            "kind": "object",
            "fields": {
                "name": "String!",
                "status": "String!",
                "cpu": "ResourceMetrics!",
                "memory": "ResourceMetrics!",
                "storage": "ResourceMetrics!",
                "podCount": "Int!",
                "labels": "JSON",
                "annotations": "JSON",
                "updatedAt": "DateTime!",
            },
        }

        self.types["Pod"] = {
            "kind": "object",
            "fields": {
                "name": "String!",
                "namespace": "String!",
                "status": "String!",
                "node": "String",
                "containers": "[Container]",
                "volumes": "[Volume]",
                "createdAt": "DateTime!",
            },
        }

        self.types["Resource"] = {
            "kind": "object",
            "fields": {
                "id": "String!",
                "type": "ResourceType!",
                "name": "String!",
                "status": "String!",
                "metadata": "JSON",
                "updatedAt": "DateTime!",
            },
        }

        self.types["Metrics"] = {
            "kind": "object",
            "fields": {
                "cluster": "String!",
                "timestamp": "DateTime!",
                "cpu": "ResourceMetrics!",
                "memory": "ResourceMetrics!",
                "network": "NetworkMetrics!",
                "storage": "ResourceMetrics!",
                "nodeMetrics": "[NodeMetrics]",
            },
        }

        self.types["ResourceMetrics"] = {
            "kind": "object",
            "fields": {
                "total": "Float!",
                "used": "Float!",
                "available": "Float!",
                "utilizationPercent": "Float!",
            },
        }

        self.types["NetworkMetrics"] = {
            "kind": "object",
            "fields": {
                "inMbps": "Float!",
                "outMbps": "Float!",
                "packetsIn": "Int!",
                "packetsOut": "Int!",
                "errors": "Int!",
            },
        }

        self.types["Operation"] = {
            "kind": "object",
            "fields": {
                "id": "String!",
                "type": "String!",
                "status": "OperationStatus!",
                "progress": "Int!",
                "startedAt": "DateTime!",
                "completedAt": "DateTime",
                "result": "JSON",
                "error": "String",
            },
        }

        self.types["Event"] = {
            "kind": "object",
            "fields": {
                "id": "String!",
                "type": "String!",
                "timestamp": "DateTime!",
                "resource": "Resource!",
                "message": "String!",
                "severity": "String!",
            },
        }

    def get_type(self, type_name: str) -> Optional[Dict[str, Any]]:
        """
        Get type definition.

        Args:
            type_name: Type name

        Returns:
            Type definition or None
        """
        return self.types.get(type_name)

    def get_query_fields(self) -> Dict[str, Any]:
        """
        Get query root fields.

        Returns:
            Query field definitions
        """
        return self.types.get("Query", {}).get("fields", {})

    def get_mutation_fields(self) -> Dict[str, Any]:
        """
        Get mutation root fields.

        Returns:
            Mutation field definitions
        """
        return self.types.get("Mutation", {}).get("fields", {})

    def get_subscription_fields(self) -> Dict[str, Any]:
        """
        Get subscription root fields.

        Returns:
            Subscription field definitions
        """
        return self.types.get("Subscription", {}).get("fields", {})


class GraphQLResolver:
    """
    Resolver for executing GraphQL queries and mutations.

    Coordinates with data loaders and external services.
    """

    def __init__(self, schema: GraphQLSchema):
        """
        Initialize resolver.

        Args:
            schema: GraphQL schema
        """
        self.schema = schema
        self.data_loaders: Dict[str, DataLoader] = {}
        self.contexts: Dict[str, QueryContext] = {}

    def register_resolver(self, field_name: str, resolver_fn: Callable[..., Any]) -> None:
        """
        Register field resolver.

        Args:
            field_name: Field name
            resolver_fn: Resolver function
        """
        self.schema.resolvers[field_name] = resolver_fn

    async def resolve_query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        context: Optional[QueryContext] = None,
    ) -> GraphQLResponse:
        """
        Resolve GraphQL query.

        Args:
            query: GraphQL query string
            variables: Query variables
            context: Execution context

        Returns:
            GraphQL response
        """
        try:
            if not context:
                context = QueryContext(user_id="anonymous", cluster="default")

            # Parse and validate query
            query_obj = self._parse_query(query)
            if not query_obj:
                return GraphQLResponse(
                    errors=[
                        GraphQLError(message="Invalid query syntax", code="PARSE_ERROR")
                    ]
                )

            # Execute query
            data = await self._execute_query(query_obj, variables, context)

            return GraphQLResponse(data=data)

        except Exception as e:
            logger.error(f"Query resolution error: {e}")
            return GraphQLResponse(
                errors=[GraphQLError(message=str(e), code="EXECUTION_ERROR")]
            )

    def _parse_query(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Parse GraphQL query string.

        Args:
            query: Query string

        Returns:
            Parsed query object or None
        """
        try:
        # Simple validation - in production would use graphql-core
            if "query" not in query and "mutation" not in query:
                return None
            return {"raw": query}
        except Exception:
            return None

    async def _execute_query(
        self,
        query_obj: Dict[str, Any],
        variables: Optional[Dict[str, Any]],
        context: QueryContext,
    ) -> Dict[str, Any]:
        """
        Execute parsed query.

        Args:
            query_obj: Parsed query
            variables: Query variables
            context: Execution context

        Returns:
            Query result
        """
        # Simulate query execution
        return {
            "cluster": {
                "name": context.cluster,
                "status": "healthy",
                "nodeCount": 3,
                "podCount": 50,
            }
        }

    async def resolve_mutation(
        self,
        mutation: str,
        variables: Optional[Dict[str, Any]] = None,
        context: Optional[QueryContext] = None,
    ) -> GraphQLResponse:
        """
        Resolve GraphQL mutation.

        Args:
            mutation: GraphQL mutation string
            variables: Mutation variables
            context: Execution context

        Returns:
            GraphQL response
        """
        try:
            if not context:
                context = QueryContext(user_id="anonymous", cluster="default")

            # Parse and validate mutation
            mutation_obj = self._parse_query(mutation)
            if not mutation_obj:
                return GraphQLResponse(
                    errors=[
                        GraphQLError(
                            message="Invalid mutation syntax", code="PARSE_ERROR"
                        )
                    ]
                )

            # Execute mutation
            data = await self._execute_mutation(mutation_obj, variables, context)

            return GraphQLResponse(data=data)

        except Exception as e:
            logger.error(f"Mutation resolution error: {e}")
            return GraphQLResponse(
                errors=[GraphQLError(message=str(e), code="EXECUTION_ERROR")]
            )

    async def _execute_mutation(
        self,
        mutation_obj: Dict[str, Any],
        variables: Optional[Dict[str, Any]],
        context: QueryContext,
    ) -> Dict[str, Any]:
        """
        Execute parsed mutation.

        Args:
            mutation_obj: Parsed mutation
            variables: Mutation variables
            context: Execution context

        Returns:
            Mutation result
        """
        # Simulate mutation execution
        import uuid

        return {
            "operation": {
                "id": str(uuid.uuid4()),
                "status": "running",
                "progress": 0,
                "startedAt": datetime.now(timezone.utc).isoformat(),
            }
        }


class GraphQLServer:
    """
    GraphQL server for DebVisor.

    Manages schema, resolvers, and subscriptions.
    """

    def __init__(self) -> None:
        """Initialize GraphQL server."""
        self.schema = GraphQLSchema()
        self.resolver = GraphQLResolver(self.schema)
        self.subscriptions = SubscriptionManager()

    async def handle_request(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle GraphQL request.

        Args:
            body: Request body with query/mutation and variables

        Returns:
            Response data
        """
        query = body.get("query")
        mutation = body.get("mutation")
        variables = body.get("variables")
        context_data = body.get("context", {})

        context = QueryContext(
            user_id=context_data.get("user_id", "anonymous"),
            cluster=context_data.get("cluster", "default"),
            namespace=context_data.get("namespace"),
            timeout_seconds=context_data.get("timeout_seconds", 30),
            enable_cache=context_data.get("enable_cache", True),
        )

        if query:
            response = await self.resolver.resolve_query(query, variables, context)
        elif mutation:
            response = await self.resolver.resolve_mutation(
                mutation, variables, context
            )
        else:
            response = GraphQLResponse(
                errors=[
                    GraphQLError(
                        message="No query or mutation provided", code="INVALID_REQUEST"
                    )
                ]
            )

        return asdict(response)

    def get_schema_introspection(self) -> Dict[str, Any]:
        """
        Get GraphQL schema introspection.

        Returns:
            Schema introspection data
        """
        return {
            "types": self.schema.types,
            "queryType": "Query",
            "mutationType": "Mutation",
            "subscriptionType": "Subscription",
        }

    # =========================================================================
    # Subscription Support
    # =========================================================================

    async def subscribe(
        self,
        subscription_name: str,
        variables: Optional[Dict[str, Any]] = None,
        context: Optional[QueryContext] = None,
    ) -> str:
        """
        Subscribe to a GraphQL subscription.

        Args:
            subscription_name: Name of subscription field
            variables: Subscription variables
            context: Query context

        Returns:
            Subscription ID
        """
        if not context:
            context = QueryContext(user_id="anonymous", cluster="default")

        return await self.subscriptions.subscribe(
            subscription_name, variables or {}, context
        )

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe from a subscription.

        Args:
            subscription_id: Subscription ID to cancel

        Returns:
            True if successfully unsubscribed
        """
        return await self.subscriptions.unsubscribe(subscription_id)

    def publish_event(self, subscription_name: str, data: Dict[str, Any]) -> None:
        """
        Publish event to subscription subscribers.

        Args:
            subscription_name: Subscription field name
            data: Event data to publish
        """
        self.subscriptions.publish(subscription_name, data)


# =============================================================================
# Subscription Manager - Real-time Event Support
# =============================================================================


@dataclass
class Subscription:
    """Active subscription record."""

    id: str
    name: str
    variables: Dict[str, Any]
    context: QueryContext
    created_at: datetime
    callback: Optional[Callable[..., Any]] = None


class SubscriptionManager:
    """
    Manages GraphQL subscriptions for real-time updates.

    Supports:
    - clusterEvents: Kubernetes cluster events
    - operationProgress: Long-running operation updates
    - metricsUpdates: Real-time metrics
    """

    def __init__(self) -> None:
        """Initialize subscription manager."""
        self._subscriptions: Dict[str, Subscription] = {}
        self._topic_subscribers: Dict[str, Set[str]] = {}
        self._lock = asyncio.Lock()
        self._event_queues: Dict[str, asyncio.Queue[Any]] = {}

    async def subscribe(
        self, subscription_name: str, variables: Dict[str, Any], context: QueryContext
    ) -> str:
        """
        Create new subscription.

        Args:
            subscription_name: Subscription field name
            variables: Subscription variables
            context: Query context

        Returns:
            Subscription ID
        """
        import uuid

        subscription_id = str(uuid.uuid4())

        async with self._lock:
            subscription = Subscription(
                id=subscription_id,
                name=subscription_name,
                variables=variables,
                context=context,
                created_at=datetime.now(timezone.utc),
            )

            self._subscriptions[subscription_id] = subscription

            # Track by topic
            if subscription_name not in self._topic_subscribers:
                self._topic_subscribers[subscription_name] = set()
            self._topic_subscribers[subscription_name].add(subscription_id)

            # Create event queue
            self._event_queues[subscription_id] = asyncio.Queue(maxsize=100)

            logger.info(
                f"Created subscription: {subscription_id} for {subscription_name}"
            )

        return subscription_id

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Remove subscription.

        Args:
            subscription_id: Subscription to remove

        Returns:
            True if removed
        """
        async with self._lock:
            if subscription_id not in self._subscriptions:
                return False

            subscription = self._subscriptions[subscription_id]

            # Remove from topic tracking
            if subscription.name in self._topic_subscribers:
                self._topic_subscribers[subscription.name].discard(subscription_id)

            # Remove queue
            self._event_queues.pop(subscription_id, None)

            # Remove subscription
            del self._subscriptions[subscription_id]

            logger.info(f"Removed subscription: {subscription_id}")

        return True

    def publish(self, subscription_name: str, data: Dict[str, Any]) -> int:
        """
        Publish event to all subscribers of a topic.

        Args:
            subscription_name: Topic name
            data: Event data

        Returns:
            Number of subscribers notified
        """
        subscriber_ids = self._topic_subscribers.get(subscription_name, set())
        count = 0

        event = {
            "subscription": subscription_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }

        for sub_id in subscriber_ids:
            queue = self._event_queues.get(sub_id)
            if queue:
                try:
                    queue.put_nowait(event)
                    count += 1
                except asyncio.QueueFull:
                    logger.warning(f"Event queue full for subscription {sub_id}")

        return count

    async def get_events(
        self, subscription_id: str, timeout: float = 30.0
    ) -> Optional[Dict[str, Any]]:
        """
        Get next event for subscription (long-polling).

        Args:
            subscription_id: Subscription ID
            timeout: Max wait time in seconds

        Returns:
            Event data or None if timeout
        """
        queue = self._event_queues.get(subscription_id)
        if not queue:
            return None

        try:
            return await asyncio.wait_for(queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    async def stream_events(self, subscription_id: str) -> Any:
        """
        Async generator for streaming events.

        Args:
            subscription_id: Subscription ID

        Yields:
            Event data
        """
        queue = self._event_queues.get(subscription_id)
        if not queue:
            return

        while subscription_id in self._subscriptions:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=60.0)
                yield event
            except asyncio.TimeoutError:
            # Send keepalive
                yield {
                    "type": "keepalive",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

    def get_active_subscriptions(self) -> List[Dict[str, Any]]:
        """Get list of active subscriptions."""
        return [
            {
                "id": sub.id,
                "name": sub.name,
                "created_at": sub.created_at.isoformat(),
                "user_id": sub.context.user_id,
                "cluster": sub.context.cluster,
            }
            for sub in self._subscriptions.values()
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Get subscription statistics."""
        return {
            "total_subscriptions": len(self._subscriptions),
            "topics": {
                topic: len(subs) for topic, subs in self._topic_subscribers.items()
            },
            "queue_sizes": {
                sub_id: queue.qsize() for sub_id, queue in self._event_queues.items()
            },
        }


# Example usage
if __name__ == "__main__":

    async def example() -> None:
        """Example usage."""
        server = GraphQLServer()

        # Example query
        query_request = {
            "query": 'query { cluster(name: "default") { name status } }',
            "context": {"cluster": "default"},
        }

        response = await server.handle_request(query_request)
        print("Query Response:")
        print(json.dumps(response, indent=2))

        # Example mutation
        mutation_request = {
            "mutation": (
                'mutation { scaleDeployment(cluster: "default", '
                'deployment: "app", namespace: "default", '
                "replicas: 5) { id status } }"
            ),
            "context": {"cluster": "default"},
        }

        response = await server.handle_request(mutation_request)
        print("\nMutation Response:")
        print(json.dumps(response, indent=2))

        # Schema introspection
        introspection = server.get_schema_introspection()
        print("\nSchema Types:")
        print(f"Total types: {len(introspection['types'])}")

    asyncio.run(example())
