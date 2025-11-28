#!/usr/bin/env python3
"""
DebVisor Live Migration Integration Tests
==========================================

Comprehensive test suite for advanced VM migration features.
Tests pre-copy, post-copy, hybrid strategies, and consolidation.

Author: DebVisor Development Team
Date: November 28, 2025
"""

import asyncio
import json
import os
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any, List

# Add project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opt.services.migration.advanced_migration import (
    MigrationStrategy,
    MigrationState,
    MigrationPlan,
    MigrationProgress,
    HostMetrics,
    VMMemoryProfile,
    TargetScore,
    ConsolidationGoal,
    ConsolidationPlan,
    MemoryProfileAnalyzer,
    TargetHostSelector,
    TargetSelectionCriteria,
    MigrationExecutor,
    ResourceConsolidator,
    AdvancedMigrationManager,
)


class TestHostMetrics(unittest.TestCase):
    """Test HostMetrics data model."""

    def test_create_host_metrics(self):
        """Test creating host metrics."""
        metrics = HostMetrics(
            host_id="host-001",
            hostname="node-01.local",
            cpu_total_mhz=48000,
            cpu_used_mhz=24000,
            cpu_free_percent=50.0,
            ram_total_mb=131072,
            ram_used_mb=65536,
            ram_free_mb=65536,
            ram_free_percent=50.0,
            network_bandwidth_mbps=10000,
            network_used_mbps=1000,
            storage_iops_available=10000,
            latency_ms=0.5,
            vm_count=10
        )
        
        self.assertEqual(metrics.host_id, "host-001")
        self.assertEqual(metrics.cpu_free_percent, 50.0)
        self.assertEqual(metrics.ram_free_mb, 65536)
        self.assertFalse(metrics.maintenance_mode)


class TestVMMemoryProfile(unittest.TestCase):
    """Test VMMemoryProfile data model."""

    def test_create_memory_profile(self):
        """Test creating VM memory profile."""
        profile = VMMemoryProfile(
            vm_id="vm-001",
            total_memory_mb=16384,
            working_set_mb=8192,
            dirty_rate_pages_per_sec=1000.0,
            access_pattern="mixed",
            hot_regions=[(0, 1000), (5000, 2000)]
        )
        
        self.assertEqual(profile.vm_id, "vm-001")
        self.assertEqual(profile.total_memory_mb, 16384)
        self.assertEqual(len(profile.hot_regions), 2)


class TestMigrationPlan(unittest.TestCase):
    """Test MigrationPlan data model."""

    def test_create_migration_plan(self):
        """Test creating a migration plan."""
        plan = MigrationPlan(
            id="mig-001",
            vm_id="vm-test-001",
            source_host="host-001",
            target_host="host-002",
            strategy=MigrationStrategy.PRE_COPY,
            estimated_downtime_ms=100,
            estimated_duration_seconds=60,
            estimated_bandwidth_mbps=1000
        )
        
        self.assertEqual(plan.id, "mig-001")
        self.assertEqual(plan.strategy, MigrationStrategy.PRE_COPY)
        self.assertEqual(plan.estimated_downtime_ms, 100)
        self.assertFalse(plan.pre_warm)


class TestMemoryProfileAnalyzer(unittest.TestCase):
    """Test MemoryProfileAnalyzer."""

    def setUp(self):
        self.analyzer = MemoryProfileAnalyzer(sample_interval_seconds=0.01)

    def test_profile_vm(self):
        """Test profiling a VM's memory access patterns."""
        async def run_test():
            profile = await self.analyzer.profile_vm("vm-test", duration_seconds=0.1)
            
            self.assertEqual(profile.vm_id, "vm-test")
            self.assertGreater(profile.total_memory_mb, 0)
            self.assertIn(profile.access_pattern, ["sequential", "random", "mixed"])
        
        asyncio.run(run_test())

    def test_get_cached_profile(self):
        """Test getting cached profile."""
        async def run_test():
            await self.analyzer.profile_vm("vm-cached", duration_seconds=0.05)
            
            cached = self.analyzer.get_profile("vm-cached")
            self.assertIsNotNone(cached)
            self.assertEqual(cached.vm_id, "vm-cached")
        
        asyncio.run(run_test())

    def test_get_nonexistent_profile(self):
        """Test getting non-existent profile returns None."""
        profile = self.analyzer.get_profile("nonexistent-vm")
        self.assertIsNone(profile)


class TestTargetHostSelector(unittest.TestCase):
    """Test TargetHostSelector."""

    def setUp(self):
        self.selector = TargetHostSelector()
        
        # Add some test hosts
        self.host1_metrics = HostMetrics(
            host_id="host-001",
            hostname="node-01",
            cpu_total_mhz=48000,
            cpu_used_mhz=20000,
            cpu_free_percent=58.3,
            ram_total_mb=131072,
            ram_used_mb=50000,
            ram_free_mb=81072,
            ram_free_percent=61.8,
            network_bandwidth_mbps=10000,
            network_used_mbps=1000,
            storage_iops_available=10000,
            latency_ms=0.5,
            vm_count=10
        )
        
        self.host2_metrics = HostMetrics(
            host_id="host-002",
            hostname="node-02",
            cpu_total_mhz=48000,
            cpu_used_mhz=40000,
            cpu_free_percent=16.7,
            ram_total_mb=131072,
            ram_used_mb=100000,
            ram_free_mb=31072,
            ram_free_percent=23.7,
            network_bandwidth_mbps=10000,
            network_used_mbps=5000,
            storage_iops_available=5000,
            latency_ms=1.0,
            vm_count=20
        )
        
        self.host3_metrics = HostMetrics(
            host_id="host-003",
            hostname="node-03",
            cpu_total_mhz=48000,
            cpu_used_mhz=10000,
            cpu_free_percent=79.2,
            ram_total_mb=131072,
            ram_used_mb=30000,
            ram_free_mb=101072,
            ram_free_percent=77.1,
            network_bandwidth_mbps=25000,
            network_used_mbps=500,
            storage_iops_available=20000,
            latency_ms=0.3,
            vm_count=5
        )
        
        self.selector.update_host_metrics(self.host1_metrics)
        self.selector.update_host_metrics(self.host2_metrics)
        self.selector.update_host_metrics(self.host3_metrics)

    def test_select_target_balanced(self):
        """Test selecting target with balanced criteria."""
        target, score = self.selector.select_target(
            vm_id="vm-001",
            required_cpu_mhz=4000,
            required_memory_mb=8192,
            criteria=TargetSelectionCriteria.BALANCED
        )
        
        # host-003 should score highest (most free resources)
        self.assertEqual(target, "host-003")
        self.assertIsInstance(score, TargetScore)
        self.assertFalse(score.disqualified)

    def test_select_target_cpu_focused(self):
        """Test selecting target with CPU focus."""
        target, score = self.selector.select_target(
            vm_id="vm-001",
            required_cpu_mhz=4000,
            required_memory_mb=8192,
            criteria=TargetSelectionCriteria.CPU_FOCUSED
        )
        
        # host-003 has highest CPU free percentage
        self.assertEqual(target, "host-003")

    def test_select_target_memory_focused(self):
        """Test selecting target with memory focus."""
        target, score = self.selector.select_target(
            vm_id="vm-001",
            required_cpu_mhz=4000,
            required_memory_mb=8192,
            criteria=TargetSelectionCriteria.MEMORY_FOCUSED
        )
        
        # host-003 has most free memory
        self.assertEqual(target, "host-003")

    def test_select_target_excludes_hosts(self):
        """Test excluding hosts from selection."""
        target, score = self.selector.select_target(
            vm_id="vm-001",
            required_cpu_mhz=4000,
            required_memory_mb=8192,
            exclude_hosts=["host-003"]
        )
        
        # Should select host-001 (second best)
        self.assertEqual(target, "host-001")

    def test_select_target_insufficient_memory(self):
        """Test selection when memory is insufficient."""
        # Request more memory than available
        with self.assertRaises(ValueError):
            self.selector.select_target(
                vm_id="vm-001",
                required_cpu_mhz=4000,
                required_memory_mb=500000,  # 500 GB - too much
                exclude_hosts=[]
            )

    def test_maintenance_mode_excluded(self):
        """Test that maintenance mode hosts are excluded."""
        # Put host-003 in maintenance
        self.host3_metrics.maintenance_mode = True
        self.selector.update_host_metrics(self.host3_metrics)
        
        target, score = self.selector.select_target(
            vm_id="vm-001",
            required_cpu_mhz=4000,
            required_memory_mb=8192
        )
        
        self.assertNotEqual(target, "host-003")

    def test_affinity_rules(self):
        """Test affinity rules affect selection."""
        # Place vm-db on host-001
        self.selector.update_vm_placement("vm-db", "host-001")
        
        # Add affinity rule: vm-app should be with vm-db
        self.selector.add_affinity_rule("vm-app", "vm-db")
        
        target, score = self.selector.select_target(
            vm_id="vm-app",
            required_cpu_mhz=2000,
            required_memory_mb=4096,
            criteria=TargetSelectionCriteria.AFFINITY
        )
        
        # With AFFINITY criteria, should prefer host-001
        self.assertEqual(target, "host-001")
        self.assertGreater(score.affinity_score, 0)

    def test_anti_affinity_rules(self):
        """Test anti-affinity rules disqualify hosts."""
        # Place vm-db-primary on host-001
        self.selector.update_vm_placement("vm-db-primary", "host-001")
        
        # Add anti-affinity: vm-db-replica must not be with primary
        self.selector.add_anti_affinity_rule("vm-db-replica", "vm-db-primary")
        
        target, score = self.selector.select_target(
            vm_id="vm-db-replica",
            required_cpu_mhz=2000,
            required_memory_mb=4096
        )
        
        # Should NOT select host-001
        self.assertNotEqual(target, "host-001")


class TestMigrationExecutor(unittest.TestCase):
    """Test MigrationExecutor."""

    def setUp(self):
        self.executor = MigrationExecutor(default_bandwidth_mbps=1000)

    def test_execute_pre_copy(self):
        """Test pre-copy migration execution."""
        plan = MigrationPlan(
            id="mig-precopy-001",
            vm_id="vm-test",
            source_host="host-001",
            target_host="host-002",
            strategy=MigrationStrategy.PRE_COPY,
            estimated_downtime_ms=100,
            estimated_duration_seconds=10,
            estimated_bandwidth_mbps=1000,
            max_iterations=5,
            convergence_threshold_mb=10
        )
        
        async def run_test():
            progress = await self.executor.execute(plan)
            
            self.assertEqual(progress.plan_id, plan.id)
            self.assertEqual(progress.state, MigrationState.COMPLETED)
            self.assertIsNotNone(progress.completed_at)
            self.assertGreater(progress.transferred_mb, 0)
        
        asyncio.run(run_test())

    def test_execute_post_copy(self):
        """Test post-copy migration execution."""
        plan = MigrationPlan(
            id="mig-postcopy-001",
            vm_id="vm-test",
            source_host="host-001",
            target_host="host-002",
            strategy=MigrationStrategy.POST_COPY,
            estimated_downtime_ms=50,
            estimated_duration_seconds=30,
            estimated_bandwidth_mbps=1000
        )
        
        async def run_test():
            progress = await self.executor.execute(plan)
            
            self.assertEqual(progress.state, MigrationState.COMPLETED)
            self.assertGreater(progress.post_copy_faults, 0)
        
        asyncio.run(run_test())

    def test_execute_hybrid(self):
        """Test hybrid migration execution."""
        plan = MigrationPlan(
            id="mig-hybrid-001",
            vm_id="vm-test",
            source_host="host-001",
            target_host="host-002",
            strategy=MigrationStrategy.HYBRID,
            estimated_downtime_ms=75,
            estimated_duration_seconds=20,
            estimated_bandwidth_mbps=1000
        )
        
        async def run_test():
            progress = await self.executor.execute(plan)
            
            self.assertEqual(progress.state, MigrationState.COMPLETED)
        
        asyncio.run(run_test())

    def test_progress_callback(self):
        """Test progress callbacks are invoked."""
        plan = MigrationPlan(
            id="mig-callback-001",
            vm_id="vm-test",
            source_host="host-001",
            target_host="host-002",
            strategy=MigrationStrategy.PRE_COPY,
            estimated_downtime_ms=100,
            estimated_duration_seconds=10,
            estimated_bandwidth_mbps=1000,
            max_iterations=3
        )
        
        callback_invocations = []
        
        def on_progress(progress):
            callback_invocations.append(progress.iteration)
        
        self.executor.register_progress_callback(on_progress)
        
        async def run_test():
            await self.executor.execute(plan)
        
        asyncio.run(run_test())
        
        # Should have received progress updates
        self.assertGreater(len(callback_invocations), 0)

    def test_completion_callback(self):
        """Test completion callbacks are invoked."""
        plan = MigrationPlan(
            id="mig-complete-001",
            vm_id="vm-test",
            source_host="host-001",
            target_host="host-002",
            strategy=MigrationStrategy.OFFLINE,
            estimated_downtime_ms=1000,
            estimated_duration_seconds=60,
            estimated_bandwidth_mbps=1000
        )
        
        completion_results = []
        
        def on_completion(progress):
            completion_results.append(progress)
        
        self.executor.register_completion_callback(on_completion)
        
        async def run_test():
            await self.executor.execute(plan)
        
        asyncio.run(run_test())
        
        self.assertEqual(len(completion_results), 1)
        self.assertEqual(completion_results[0].state, MigrationState.COMPLETED)


class TestResourceConsolidator(unittest.TestCase):
    """Test ResourceConsolidator."""

    def setUp(self):
        self.selector = TargetHostSelector()
        self.consolidator = ResourceConsolidator(
            self.selector,
            min_host_utilization=0.3,
            max_host_utilization=0.8
        )
        
        # Set up hosts with varying utilization
        # Host-001: Low utilization (candidate for evacuation)
        self.selector.update_host_metrics(HostMetrics(
            host_id="host-001",
            hostname="node-01",
            cpu_total_mhz=48000,
            cpu_used_mhz=5000,
            cpu_free_percent=89.6,
            ram_total_mb=131072,
            ram_used_mb=13000,
            ram_free_mb=118072,
            ram_free_percent=90.1,
            network_bandwidth_mbps=10000,
            network_used_mbps=100,
            storage_iops_available=10000,
            latency_ms=0.5,
            vm_count=2
        ))
        
        # Host-002: Medium utilization (potential target)
        self.selector.update_host_metrics(HostMetrics(
            host_id="host-002",
            hostname="node-02",
            cpu_total_mhz=48000,
            cpu_used_mhz=24000,
            cpu_free_percent=50.0,
            ram_total_mb=131072,
            ram_used_mb=65536,
            ram_free_mb=65536,
            ram_free_percent=50.0,
            network_bandwidth_mbps=10000,
            network_used_mbps=2000,
            storage_iops_available=8000,
            latency_ms=0.5,
            vm_count=10
        ))
        
        # Host-003: Medium utilization (potential target)
        self.selector.update_host_metrics(HostMetrics(
            host_id="host-003",
            hostname="node-03",
            cpu_total_mhz=48000,
            cpu_used_mhz=28000,
            cpu_free_percent=41.7,
            ram_total_mb=131072,
            ram_used_mb=70000,
            ram_free_mb=61072,
            ram_free_percent=46.6,
            network_bandwidth_mbps=10000,
            network_used_mbps=3000,
            storage_iops_available=7000,
            latency_ms=0.5,
            vm_count=12
        ))
        
        # Place VMs and register resources
        self.selector.update_vm_placement("vm-001", "host-001")
        self.selector.update_vm_placement("vm-002", "host-001")
        self.consolidator.register_vm_resources("vm-001", 2000, 4096)
        self.consolidator.register_vm_resources("vm-002", 2000, 4096)

    def test_plan_consolidation_power_saving(self):
        """Test consolidation planning for power saving."""
        plan = self.consolidator.plan_consolidation(ConsolidationGoal.POWER_SAVING)
        
        self.assertIsInstance(plan, ConsolidationPlan)
        self.assertEqual(plan.goal, ConsolidationGoal.POWER_SAVING)
        
        # host-001 should be identified for evacuation (low utilization)
        self.assertIn("host-001", plan.hosts_to_evacuate)

    def test_plan_includes_migrations(self):
        """Test that consolidation plan includes necessary migrations."""
        plan = self.consolidator.plan_consolidation(ConsolidationGoal.BALANCED)
        
        if plan.hosts_to_evacuate:
            # Should have migrations for VMs on evacuated hosts
            self.assertGreater(len(plan.migrations), 0)
            
            for migration in plan.migrations:
                self.assertIn(migration.source_host, plan.hosts_to_evacuate)
                self.assertNotIn(migration.target_host, plan.hosts_to_evacuate)

    def test_estimates_power_savings(self):
        """Test power savings estimation."""
        plan = self.consolidator.plan_consolidation(ConsolidationGoal.POWER_SAVING)
        
        # Power savings should be calculated based on hosts to power off
        expected_savings = len(plan.hosts_to_power_off) * 300  # ~300W per host
        self.assertEqual(plan.estimated_power_savings_watts, expected_savings)

    def test_calculates_risk_score(self):
        """Test risk score calculation."""
        plan = self.consolidator.plan_consolidation(ConsolidationGoal.BALANCED)
        
        # Risk should be between 0 and 1
        self.assertGreaterEqual(plan.risk_score, 0)
        self.assertLessEqual(plan.risk_score, 1)


class TestAdvancedMigrationManager(unittest.TestCase):
    """Test unified AdvancedMigrationManager."""

    def setUp(self):
        self.manager = AdvancedMigrationManager(
            default_bandwidth_mbps=1000,
            enable_pre_warming=True
        )
        
        # Initialize some hosts
        for host_id in ["host-001", "host-002", "host-003"]:
            self.manager.collect_host_metrics(host_id)

    def test_collect_host_metrics(self):
        """Test host metrics collection."""
        metrics = self.manager.collect_host_metrics("host-test")
        
        self.assertIsInstance(metrics, HostMetrics)
        self.assertEqual(metrics.host_id, "host-test")
        self.assertGreater(metrics.cpu_total_mhz, 0)

    def test_select_optimal_target(self):
        """Test optimal target selection."""
        target = self.manager.select_optimal_target(
            vm_id="vm-001",
            exclude_hosts=["host-001"],
            required_cpu=4000,
            required_memory=8192
        )
        
        self.assertIsNotNone(target)
        self.assertNotEqual(target, "host-001")

    def test_plan_migration_auto_strategy(self):
        """Test migration planning with automatic strategy selection."""
        # Set high dirty rate for post-copy
        self.manager._memory_change_rates["vm-dirty"] = 6000
        
        plan = self.manager.plan_migration(
            vm_id="vm-dirty",
            source="host-001",
            required_cpu=4000,
            required_memory=8192
        )
        
        # High dirty rate should select POST_COPY
        self.assertEqual(plan.strategy, MigrationStrategy.POST_COPY)

    def test_plan_migration_pre_copy_for_stable(self):
        """Test pre-copy strategy for stable VMs."""
        self.manager._memory_change_rates["vm-stable"] = 100
        
        plan = self.manager.plan_migration(
            vm_id="vm-stable",
            source="host-001",
            required_cpu=2000,
            required_memory=4096
        )
        
        # Low dirty rate should select PRE_COPY
        self.assertEqual(plan.strategy, MigrationStrategy.PRE_COPY)

    def test_plan_migration_hybrid_for_medium(self):
        """Test hybrid strategy for medium dirty rate VMs."""
        self.manager._memory_change_rates["vm-medium"] = 2000
        
        plan = self.manager.plan_migration(
            vm_id="vm-medium",
            source="host-001",
            required_cpu=4000,
            required_memory=8192
        )
        
        # Medium dirty rate should select HYBRID
        self.assertEqual(plan.strategy, MigrationStrategy.HYBRID)

    def test_execute_migration(self):
        """Test full migration execution."""
        plan = self.manager.plan_migration(
            vm_id="vm-execute-test",
            source="host-001",
            required_cpu=2000,
            required_memory=4096
        )
        
        async def run_test():
            progress = await self.manager.execute_migration(plan)
            
            self.assertEqual(progress.state, MigrationState.COMPLETED)
            self.assertIsNotNone(progress.completed_at)
        
        asyncio.run(run_test())

    def test_plan_consolidation(self):
        """Test consolidation planning."""
        plan = self.manager.plan_consolidation(ConsolidationGoal.POWER_SAVING)
        
        self.assertIsInstance(plan, ConsolidationPlan)
        self.assertIsNotNone(plan.id)


class TestMigrationStrategies(unittest.TestCase):
    """Test all migration strategy variations."""

    def setUp(self):
        self.executor = MigrationExecutor()

    def test_live_block_migration(self):
        """Test live block migration with storage."""
        plan = MigrationPlan(
            id="mig-block-001",
            vm_id="vm-storage",
            source_host="host-001",
            target_host="host-002",
            strategy=MigrationStrategy.LIVE_BLOCK,
            estimated_downtime_ms=200,
            estimated_duration_seconds=120,
            estimated_bandwidth_mbps=500
        )
        
        async def run_test():
            progress = await self.executor.execute(plan)
            self.assertEqual(progress.state, MigrationState.COMPLETED)
        
        asyncio.run(run_test())

    def test_offline_migration(self):
        """Test offline (cold) migration."""
        plan = MigrationPlan(
            id="mig-offline-001",
            vm_id="vm-cold",
            source_host="host-001",
            target_host="host-002",
            strategy=MigrationStrategy.OFFLINE,
            estimated_downtime_ms=60000,  # Full downtime
            estimated_duration_seconds=300,
            estimated_bandwidth_mbps=1000
        )
        
        async def run_test():
            progress = await self.executor.execute(plan)
            self.assertEqual(progress.state, MigrationState.COMPLETED)
        
        asyncio.run(run_test())


class TestMigrationDowntimeMetrics(unittest.TestCase):
    """Test migration downtime tracking."""

    def setUp(self):
        self.executor = MigrationExecutor()

    def test_tracks_downtime(self):
        """Test that downtime is tracked during switchover."""
        plan = MigrationPlan(
            id="mig-downtime-001",
            vm_id="vm-test",
            source_host="host-001",
            target_host="host-002",
            strategy=MigrationStrategy.PRE_COPY,
            estimated_downtime_ms=100,
            estimated_duration_seconds=30,
            estimated_bandwidth_mbps=1000,
            max_iterations=3
        )
        
        async def run_test():
            progress = await self.executor.execute(plan)
            
            # Downtime should be recorded
            self.assertGreater(progress.downtime_ms, 0)
        
        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
