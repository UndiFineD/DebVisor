"""
Test suite for Multi-Cluster Foundation

Tests for MultiClusterManager including:
- Cluster registration and management
- Service discovery
- State synchronization
- Load balancing
- Federation policies
"""

import unittest
from opt.services.multi_cluster import (
    MultiClusterManager,
    ClusterNode,
    ClusterStatus,
    ClusterMetrics,
    CrossClusterService,
    ReplicationStrategy,
)


class TestClusterRegistry(unittest.TestCase):
    """Test cluster registry functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.manager = MultiClusterManager()

    def test_add_cluster(self) -> None:
        """Test adding a new cluster."""
        cluster_id = self.manager.add_cluster(
            name="test-cluster",
            endpoint="http://cluster.example.com:8080",
            region="us-west",
            version="1.0.0",
        )

        self.assertIsNotNone(cluster_id)
        cluster = self.manager.registry.get_cluster(cluster_id)
        self.assertIsNotNone(cluster)
        self.assertEqual(cluster.name, "test-cluster")
        self.assertEqual(cluster.region, "us-west")

    def test_register_cluster(self) -> None:
        """Test registering a cluster."""
        cluster = ClusterNode(
            cluster_id="test-1",
            name="test-cluster-1",
            endpoint="http://test.example.com:8080",
            region="us-east",
            version="1.0.0",
        )

        result = self.manager.registry.register_cluster(cluster)

        self.assertTrue(result)
        self.assertEqual(self.manager.registry.get_cluster("test-1"), cluster)

    def test_deregister_cluster(self) -> None:
        """Test deregistering a cluster."""
        cluster = ClusterNode(
            cluster_id="test-2",
            name="test-cluster-2",
            endpoint="http://test.example.com:8080",
            region="us-east",
            version="1.0.0",
        )

        self.manager.registry.register_cluster(cluster)
        result = self.manager.registry.deregister_cluster("test-2")

        self.assertTrue(result)
        self.assertIsNone(self.manager.registry.get_cluster("test-2"))

    def test_list_clusters(self) -> None:
        """Test listing clusters."""
        # Add clusters in different regions
        for i in range(3):
            self.manager.add_cluster(
                name=f"cluster-{i}",
                endpoint=f"http://cluster-{i}.example.com:8080",
                region="us-west" if i < 2 else "us-east",
                version="1.0.0",
            )

        all_clusters = self.manager.registry.list_clusters()
        self.assertEqual(len(all_clusters), 3)

        west_clusters = self.manager.registry.list_clusters(region="us-west")
        self.assertEqual(len(west_clusters), 2)

    def test_update_cluster_status(self) -> None:
        """Test updating cluster status."""
        cluster_id = self.manager.add_cluster(
            name="test",
            endpoint="http://test.example.com",
            region="us-west",
            version="1.0.0",
        )

        metrics = ClusterMetrics(
            cpu_usage_percent=45.0,
            memory_usage_percent=60.0,
            disk_usage_percent=30.0,
            node_count=10,
            active_jobs=5,
            active_services=3,
        )

        result = self.manager.registry.update_cluster_status(
            cluster_id, ClusterStatus.HEALTHY, metrics
        )

        self.assertTrue(result)
        cluster = self.manager.registry.get_cluster(cluster_id)
        self.assertEqual(cluster.status, ClusterStatus.HEALTHY)
        self.assertIsNotNone(cluster.metrics)

    def test_get_healthy_clusters(self) -> None:
        """Test getting healthy clusters."""
        # Add healthy cluster
        healthy_id = self.manager.add_cluster(
            name="healthy",
            endpoint="http://healthy.example.com",
            region="us-west",
            version="1.0.0",
        )

        # Add unhealthy cluster
        unhealthy_id = self.manager.add_cluster(
            name="unhealthy",
            endpoint="http://unhealthy.example.com",
            region="us-west",
            version="1.0.0",
        )

        # Update statuses
        self.manager.registry.update_cluster_status(healthy_id, ClusterStatus.HEALTHY)

        self.manager.registry.update_cluster_status(unhealthy_id, ClusterStatus.OFFLINE)

        healthy = self.manager.registry.get_healthy_clusters()
        self.assertGreater(len(healthy), 0)


class TestServiceDiscovery(unittest.TestCase):
    """Test service discovery functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.manager = MultiClusterManager()
        self.discovery = self.manager.discovery

    def test_register_service(self) -> None:
        """Test registering a service."""
        service = CrossClusterService(
            service_id="svc-1",
            name="test-service",
            type="api",
            clusters={"cluster-1": {"port": 8080}, "cluster-2": {"port": 8080}},
        )

        result = self.discovery.register_service(service)

        self.assertTrue(result)
        self.assertIn("svc-1", self.manager.registry.services)

    def test_discover_service_by_name(self) -> None:
        """Test discovering service by name."""
        service = CrossClusterService(
            service_id="svc-1",
            name="api-gateway",
            type="gateway",
            clusters={"cluster-1": {"port": 8080}},
        )

        self.discovery.register_service(service)

        discovered = self.discovery.discover_service("api-gateway")

        self.assertIsNotNone(discovered)
        self.assertEqual(discovered.name, "api-gateway")

    def test_discover_service_not_found(self) -> None:
        """Test discovering non-existent service."""
        discovered = self.discovery.discover_service("non-existent")

        self.assertIsNone(discovered)

    def test_get_service_endpoints(self) -> None:
        """Test getting service endpoints."""
        # Add clusters
        c1_id = self.manager.add_cluster(
            name="cluster-1",
            endpoint="http://cluster1.example.com:8080",
            region="us-west",
            version="1.0.0",
        )

        c2_id = self.manager.add_cluster(
            name="cluster-2",
            endpoint="http://cluster2.example.com:8080",
            region="us-east",
            version="1.0.0",
        )

        # Update cluster status
        self.manager.registry.update_cluster_status(c1_id, ClusterStatus.HEALTHY)
        self.manager.registry.update_cluster_status(c2_id, ClusterStatus.HEALTHY)

        # Register service
        service = CrossClusterService(
            service_id="svc-1",
            name="test-service",
            type="api",
            clusters={c1_id: {}, c2_id: {}},
        )

        self.discovery.register_service(service)

        endpoints = self.discovery.get_service_endpoints("svc-1")

        self.assertEqual(len(endpoints), 2)


class TestLoadBalancer(unittest.TestCase):
    """Test load balancing functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.manager = MultiClusterManager()
        self.load_balancer = self.manager.load_balancer

    def test_get_next_cluster_round_robin(self) -> None:
        """Test round-robin load balancing."""
        # Add healthy clusters
        for i in range(3):
            cluster_id = self.manager.add_cluster(
                name=f"cluster-{i}",
                endpoint=f"http://cluster{i}.example.com:8080",
                region="us-west",
                version="1.0.0",
            )

            metrics = ClusterMetrics(
                cpu_usage_percent=50.0,
                memory_usage_percent=60.0,
                disk_usage_percent=30.0,
                node_count=10,
                active_jobs=5,
                active_services=3,
            )

            self.manager.registry.update_cluster_status(
                cluster_id, ClusterStatus.HEALTHY, metrics
            )

        cluster = self.load_balancer.get_next_cluster(policy="round_robin")

        self.assertIsNotNone(cluster)
        self.assertEqual(cluster.status, ClusterStatus.HEALTHY)

    def test_get_next_cluster_least_loaded(self) -> None:
        """Test least-loaded load balancing."""
        # Add clusters with different CPU usage
        for i in range(2):
            cluster_id = self.manager.add_cluster(
                name=f"cluster-{i}",
                endpoint=f"http://cluster{i}.example.com:8080",
                region="us-west",
                version="1.0.0",
            )

            metrics = ClusterMetrics(
                cpu_usage_percent=20.0 + i * 50,  # 20% and 70%
                memory_usage_percent=60.0,
                disk_usage_percent=30.0,
                node_count=10,
                active_jobs=5,
                active_services=3,
            )

            self.manager.registry.update_cluster_status(
                cluster_id, ClusterStatus.HEALTHY, metrics
            )

        cluster = self.load_balancer.get_next_cluster(policy="least_loaded")

        self.assertIsNotNone(cluster)
        # Should select the least loaded cluster
        self.assertLess(cluster.metrics.cpu_usage_percent, 50)

    def test_distribute_work(self) -> None:
        """Test work distribution across clusters."""
        # Add clusters with different capacity
        for i in range(2):
            cluster_id = self.manager.add_cluster(
                name=f"cluster-{i}",
                endpoint=f"http://cluster{i}.example.com:8080",
                region="us-west",
                version="1.0.0",
            )

            metrics = ClusterMetrics(
                cpu_usage_percent=30.0 + i * 20,  # 30% and 50%
                memory_usage_percent=60.0,
                disk_usage_percent=30.0,
                node_count=10,
                active_jobs=5,
                active_services=3,
            )

            self.manager.registry.update_cluster_status(
                cluster_id, ClusterStatus.HEALTHY, metrics
            )

        distribution = self.load_balancer.distribute_work(100)

        self.assertEqual(sum(distribution.values()), 100)
        self.assertGreater(len(distribution), 0)


class TestMultiClusterManager(unittest.TestCase):
    """Test MultiClusterManager high-level interface."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.manager = MultiClusterManager()

    def test_get_federation_status(self) -> None:
        """Test getting federation status."""
        # Add some clusters
        for i in range(2):
            cluster_id = self.manager.add_cluster(
                name=f"cluster-{i}",
                endpoint=f"http://cluster{i}.example.com:8080",
                region="us-west",
                version="1.0.0",
            )

            metrics = ClusterMetrics(
                cpu_usage_percent=45.0,
                memory_usage_percent=60.0,
                disk_usage_percent=30.0,
                node_count=10,
                active_jobs=5,
                active_services=3,
            )

            self.manager.registry.update_cluster_status(
                cluster_id, ClusterStatus.HEALTHY, metrics
            )

        status = self.manager.get_federation_status()

        self.assertIn("total_clusters", status)
        self.assertIn("healthy_clusters", status)
        self.assertEqual(status["total_clusters"], 2)

    def test_create_federation_policy(self) -> None:
        """Test creating federation policy."""
        cluster_ids = []
        for i in range(2):
            cluster_id = self.manager.add_cluster(
                name=f"cluster-{i}",
                endpoint=f"http://cluster{i}.example.com:8080",
                region="us-west",
                version="1.0.0",
            )
            cluster_ids.append(cluster_id)

        policy_id = self.manager.create_federation_policy(
            name="high-availability",
            description="HA policy for critical services",
            clusters=cluster_ids,
            replication_strategy=ReplicationStrategy.SYNCHRONOUS,
            failover_enabled=True,
        )

        self.assertIsNotNone(policy_id)
        self.assertIn(policy_id, self.manager.policies)


if __name__ == "__main__":
    unittest.main()
