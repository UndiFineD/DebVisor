"""
Multi-region Support Test Suite

Comprehensive tests for multi-region functionality including region management,
replication, failover, and statistics.
"""

import asyncio
import os
import shutil
import tempfile
import unittest
from opt.services.multiregion.core import (
    MultiRegionManager,
    RegionStatus,
    ReplicationStatus,
    ResourceType,
)
from opt.services.multiregion.api import MultiRegionAPI


class TestRegionManagement(unittest.TestCase):
    """Test region management functionality."""

    def setUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = MultiRegionManager(self.temp_dir)

    def tearDown(self):
        """Cleanup test fixtures."""
        self.manager.close()
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_register_region(self):
        """Test region registration."""
        region = self.manager.register_region(
            name="US East 1",
            location="us-east-1",
            api_endpoint="https://api.us-east-1.internal",
            is_primary=True,
            capacity_vms=1000
        )

        self.assertEqual(region.region_id, "us-east-1")
        self.assertEqual(region.name, "US East 1")
        self.assertTrue(region.is_primary)
        self.assertEqual(region.capacity_vms, 1000)

    def test_register_multiple_regions(self):
        """Test registering multiple regions."""
        region1 = self.manager.register_region(
            "US East 1",
            "us-east-1",
            "https://api.us-east-1.internal",
            is_primary=True)
        region2 = self.manager.register_region(
            "US West 1", "us-west-1", "https://api.us-west-1.internal"
        )

        self.assertEqual(len(self.manager.regions), 2)
        self.assertTrue(region1.is_primary)
        self.assertFalse(region2.is_primary)

    def test_primary_region_promotion(self):
        """Test primary region promotion."""
        region1 = self.manager.register_region(
            "US East 1",
            "us-east-1",
            "https://api.us-east-1.internal",
            is_primary=True)
        region2 = self.manager.register_region(
            "US West 1",
            "us-west-1",
            "https://api.us-west-1.internal",
            is_primary=True)

        # First region should no longer be primary
        self.assertFalse(region1.is_primary)
        self.assertTrue(region2.is_primary)

    def test_get_region(self):
        """Test retrieving a region."""
        self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )

        region = self.manager.get_region("us-east-1")
        self.assertIsNotNone(region)
        self.assertEqual(region.name, "US East 1")

    def test_get_nonexistent_region(self):
        """Test retrieving nonexistent region."""
        region = self.manager.get_region("nonexistent")
        self.assertIsNone(region)

    def test_get_primary_region(self):
        """Test getting primary region."""
        self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )
        self.manager.register_region(
            "US West 1",
            "us-west-1",
            "https://api.us-west-1.internal",
            is_primary=True)

        primary = self.manager.get_primary_region()
        self.assertEqual(primary.region_id, "us-west-1")

    def test_list_regions(self):
        """Test listing regions."""
        self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )
        self.manager.register_region(
            "US West 1", "us-west-1", "https://api.us-west-1.internal"
        )

        regions = self.manager.list_regions()
        self.assertEqual(len(regions), 2)

    def test_list_regions_by_status(self):
        """Test listing regions by status."""
        region = self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )
        region.status = RegionStatus.HEALTHY

        healthy_regions = self.manager.list_regions(
            status=RegionStatus.HEALTHY)
        self.assertEqual(len(healthy_regions), 1)
        self.assertEqual(healthy_regions[0].region_id, "us-east-1")

    def test_region_to_dict(self):
        """Test region serialization."""
        region = self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )

        region_dict = region.to_dict()
        self.assertEqual(region_dict["region_id"], "us-east-1")
        self.assertEqual(region_dict["name"], "US East 1")
        self.assertIn("last_heartbeat", region_dict)


class TestRegionHealth(unittest.IsolatedAsyncioTestCase):
    """Test region health checking."""

    async def asyncSetUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = MultiRegionManager(self.temp_dir)

    async def asyncTearDown(self):
        """Cleanup test fixtures."""
        if self.manager:
            self.manager.close()
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_check_region_health_healthy(self):
        """Test health check for healthy region."""
        region = self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )

        status = await self.manager.check_region_health("us-east-1")
        self.assertIn(status, [RegionStatus.HEALTHY, RegionStatus.DEGRADED])
        self.assertGreater(region.latency_ms, 0)

    async def test_check_nonexistent_region(self):
        """Test health check for nonexistent region."""
        status = await self.manager.check_region_health("nonexistent")
        self.assertEqual(status, RegionStatus.UNKNOWN)

    async def test_health_check_updates_heartbeat(self):
        """Test that health check updates last heartbeat."""
        region = self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )
        old_heartbeat = region.last_heartbeat

        await asyncio.sleep(0.1)
        await self.manager.check_region_health("us-east-1")

        self.assertGreater(region.last_heartbeat, old_heartbeat)


class TestReplication(unittest.TestCase):
    """Test replication functionality."""

    def setUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = MultiRegionManager(self.temp_dir)

    def tearDown(self):
        """Cleanup test fixtures."""
        if self.manager:
            self.manager.close()
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_setup_replication(self):
        """Test setting up replication."""
        config = self.manager.setup_replication(
            "us-east-1",
            "us-west-1",
            [ResourceType.VM, ResourceType.CONFIG],
            sync_interval_seconds=300
        )

        self.assertEqual(config.source_region_id, "us-east-1")
        self.assertEqual(config.target_region_id, "us-west-1")
        self.assertEqual(len(config.resource_types), 2)

    def test_setup_bidirectional_replication(self):
        """Test bidirectional replication setup."""
        config = self.manager.setup_replication(
            "us-east-1",
            "us-west-1",
            [ResourceType.VM],
            bidirectional=True
        )

        self.assertTrue(config.bidirectional)

    def test_replicate_vm(self):
        """Test registering VM for replication."""
        resource = self.manager.replicate_vm(
            vm_id="vm-12345",
            primary_region_id="us-east-1",
            replica_regions=["us-west-1", "eu-west-1"]
        )

        self.assertEqual(resource.resource_id, "vm-12345")
        self.assertEqual(resource.resource_type, ResourceType.VM)
        self.assertEqual(resource.primary_region_id, "us-east-1")
        self.assertEqual(len(resource.replica_regions), 2)

    def test_replication_status_initial_syncing(self):
        """Test initial replication status is syncing."""
        resource = self.manager.replicate_vm(
            "vm-12345",
            "us-east-1",
            ["us-west-1"]
        )

        status = resource.replication_status["us-west-1"]
        self.assertEqual(status, ReplicationStatus.SYNCING)

    def test_get_replication_status(self):
        """Test getting replication status."""
        self.manager.replicate_vm(
            "vm-12345",
            "us-east-1",
            ["us-west-1"]
        )

        status = self.manager.get_replication_status("vm-12345")
        self.assertEqual(status["resource_id"], "vm-12345")
        self.assertIn("us-west-1", status["replicas"])

    def test_replication_config_to_dict(self):
        """Test replication config serialization."""
        config = self.manager.setup_replication(
            "us-east-1",
            "us-west-1",
            [ResourceType.VM, ResourceType.CONFIG]
        )

        config_dict = config.to_dict()
        self.assertEqual(config_dict["source_region_id"], "us-east-1")
        self.assertEqual(len(config_dict["resource_types"]), 2)


class TestReplicationSync(unittest.IsolatedAsyncioTestCase):
    """Test resource synchronization."""

    async def asyncSetUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = MultiRegionManager(self.temp_dir)

    async def asyncTearDown(self):
        """Cleanup test fixtures."""
        self.manager.close()
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    async def test_sync_resource(self):
        """Test syncing a resource."""
        self.manager.replicate_vm(
            "vm-12345",
            "us-east-1",
            ["us-west-1"]
        )

        success = await self.manager.sync_resource(
            "vm-12345",
            "us-east-1",
            "us-west-1"
        )

        self.assertTrue(success)

    async def test_sync_nonexistent_resource(self):
        """Test syncing nonexistent resource."""
        success = await self.manager.sync_resource(
            "nonexistent",
            "us-east-1",
            "us-west-1"
        )

        self.assertFalse(success)

    async def test_sync_updates_status(self):
        """Test that sync updates replication status."""
        self.manager.replicate_vm(
            "vm-12345",
            "us-east-1",
            ["us-west-1"]
        )

        resource = self.manager.resources["vm-12345"]
        self.assertEqual(
            resource.replication_status["us-west-1"],
            ReplicationStatus.SYNCING)

        await self.manager.sync_resource(
            "vm-12345",
            "us-east-1",
            "us-west-1"
        )

        self.assertEqual(
            resource.replication_status["us-west-1"],
            ReplicationStatus.IN_SYNC)


class TestFailover(unittest.IsolatedAsyncioTestCase):
    """Test failover functionality."""

    async def asyncSetUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = MultiRegionManager(self.temp_dir)

        # Setup regions
        self.manager.register_region(
            "US East 1",
            "us-east-1",
            "https://api.us-east-1.internal",
            is_primary=True)
        self.manager.register_region(
            "US West 1", "us-west-1", "https://api.us-west-1.internal"
        )

    async def asyncTearDown(self):
        """Cleanup test fixtures."""
        self.manager.close()
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    async def test_perform_failover(self):
        """Test performing failover."""
        success, event = await self.manager.perform_failover(
            "us-east-1",
            "us-west-1",
            reason="Test failover"
        )

        self.assertTrue(success)
        self.assertEqual(event.from_region_id, "us-east-1")
        self.assertEqual(event.to_region_id, "us-west-1")

    async def test_failover_updates_primary(self):
        """Test that failover updates primary region."""
        old_primary = self.manager.get_primary_region()
        self.assertEqual(old_primary.region_id, "us-east-1")

        await self.manager.perform_failover(
            "us-east-1",
            "us-west-1"
        )

        new_primary = self.manager.get_primary_region()
        self.assertEqual(new_primary.region_id, "us-west-1")

    async def test_failover_to_unreachable_region(self):
        """Test failover to unreachable region."""
        region = self.manager.get_region("us-west-1")
        region.status = RegionStatus.UNREACHABLE

        success, event = await self.manager.perform_failover(
            "us-east-1",
            "us-west-1"
        )

        # Failover should still attempt, but health check will fail
        self.assertIsNotNone(event)

    async def test_failover_event_recorded(self):
        """Test that failover events are recorded."""
        await self.manager.perform_failover(
            "us-east-1",
            "us-west-1"
        )

        self.assertEqual(len(self.manager.failover_events), 1)

    async def test_failover_event_to_dict(self):
        """Test failover event serialization."""
        success, event = await self.manager.perform_failover(
            "us-east-1",
            "us-west-1"
        )

        event_dict = event.to_dict()
        self.assertEqual(event_dict["from_region_id"], "us-east-1")
        self.assertEqual(event_dict["to_region_id"], "us-west-1")


class TestStatistics(unittest.TestCase):
    """Test statistics functionality."""

    def setUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = MultiRegionManager(self.temp_dir)

    def tearDown(self):
        """Cleanup test fixtures."""
        self.manager.close()
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_region_statistics(self):
        """Test getting region statistics."""
        self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )

        stats = self.manager.get_region_statistics("us-east-1")

        self.assertEqual(stats["region_id"], "us-east-1")
        self.assertIn("status", stats)
        self.assertIn("utilization_percent", stats)

    def test_global_statistics(self):
        """Test getting global statistics."""
        self.manager.register_region(
            "US East 1",
            "us-east-1",
            "https://api.us-east-1.internal",
            is_primary=True)
        self.manager.register_region(
            "US West 1", "us-west-1", "https://api.us-west-1.internal"
        )

        stats = self.manager.get_global_statistics()

        self.assertEqual(stats["total_regions"], 2)
        self.assertEqual(stats["healthy_regions"], 0)  # No health checks yet
        self.assertIsNotNone(stats["primary_region"])

    def test_global_stats_with_resources(self):
        """Test global statistics with resources."""
        self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )
        self.manager.replicate_vm("vm-1", "us-east-1", ["us-west-1"])
        self.manager.replicate_vm("vm-2", "us-east-1", ["us-west-1"])

        stats = self.manager.get_global_statistics()

        self.assertEqual(stats["total_resources"], 2)


class TestFailoverHistory(unittest.IsolatedAsyncioTestCase):
    """Test failover history retrieval."""

    async def asyncSetUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = MultiRegionManager(self.temp_dir)

        self.manager.register_region(
            "US East 1",
            "us-east-1",
            "https://api.us-east-1.internal",
            is_primary=True)
        self.manager.register_region(
            "US West 1", "us-west-1", "https://api.us-west-1.internal"
        )

    async def asyncTearDown(self):
        """Cleanup test fixtures."""
        self.manager.close()
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    async def test_get_failover_history(self):
        """Test retrieving failover history."""
        await self.manager.perform_failover("us-east-1", "us-west-1")

        history = self.manager.get_failover_history()

        self.assertEqual(len(history), 1)

    async def test_get_failover_history_by_region(self):
        """Test filtering failover history by region."""
        await self.manager.perform_failover("us-east-1", "us-west-1")

        history = self.manager.get_failover_history(region_id="us-east-1")

        self.assertEqual(len(history), 1)


class TestMultiRegionAPI(unittest.TestCase):
    """Test REST API functionality."""

    def setUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = MultiRegionManager(self.temp_dir)
        self.api = MultiRegionAPI(self.manager)

    def tearDown(self):
        """Cleanup test fixtures."""
        self.manager.close()
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_register_region_api(self):
        """Test region registration via API."""
        response, status = self.api.register_region({
            "name": "US East 1",
            "location": "us-east-1",
            "api_endpoint": "https://api.us-east-1.internal",
            "is_primary": True
        })

        self.assertEqual(status, 201)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["data"]["region_id"], "us-east-1")

    def test_list_regions_api(self):
        """Test listing regions via API."""
        self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )

        response, status = self.api.list_regions()

        self.assertEqual(status, 200)
        self.assertEqual(len(response["data"]), 1)

    def test_get_region_api(self):
        """Test getting region via API."""
        self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )

        response, status = self.api.get_region("us-east-1")

        self.assertEqual(status, 200)
        self.assertEqual(response["data"]["name"], "US East 1")

    def test_setup_replication_api(self):
        """Test setting up replication via API."""
        response, status = self.api.setup_replication({
            "source_region_id": "us-east-1",
            "target_region_id": "us-west-1",
            "resource_types": ["vm", "config"]
        })

        self.assertEqual(status, 201)
        self.assertEqual(response["status"], "success")

    def test_replicate_vm_api(self):
        """Test registering VM via API."""
        response, status = self.api.replicate_vm({
            "vm_id": "vm-12345",
            "primary_region_id": "us-east-1",
            "replica_regions": ["us-west-1"]
        })

        self.assertEqual(status, 201)
        self.assertEqual(response["data"]["resource_id"], "vm-12345")

    def test_get_global_stats_api(self):
        """Test getting global stats via API."""
        self.manager.register_region(
            "US East 1", "us-east-1", "https://api.us-east-1.internal"
        )

        response, status = self.api.get_global_stats()

        self.assertEqual(status, 200)
        self.assertEqual(response["data"]["total_regions"], 1)

    def test_health_check_api(self):
        """Test health check via API."""
        response, status = self.api.get_health()

        self.assertEqual(status, 200)
        self.assertEqual(response["status"], "success")


if __name__ == "__main__":
    unittest.main()
