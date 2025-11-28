#!/usr/bin/env python3
"""
Test suite for DebVisor Mock Mode Infrastructure.
"""

import asyncio
import json
import os
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from opt.testing.mock_mode import (
    MockConfig,
    MockBehavior,
    MockServiceError,
    MockTimeoutError,
    MockVMManager,
    MockContainerManager,
    MockStorageManager,
    MockNetworkManager,
    MockHealthChecker,
    MockSecretsManager,
    enable_mock_mode,
    disable_mock_mode,
    is_mock_mode,
    get_mock_config,
    mock_mode,
    get_mock_state,
    reset_mock_state,
    get_mock_manager,
    inject_vm,
    inject_container,
    clear_vms,
    clear_containers,
    auto_enable_mock_mode,
)


class TestMockModeConfiguration(unittest.TestCase):
    """Test mock mode enable/disable and configuration."""
    
    def setUp(self):
        disable_mock_mode()
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_enable_mock_mode_default(self):
        """Test enabling mock mode with default config."""
        self.assertFalse(is_mock_mode())
        enable_mock_mode()
        self.assertTrue(is_mock_mode())
    
    def test_enable_mock_mode_custom_config(self):
        """Test enabling mock mode with custom configuration."""
        config = MockConfig(
            latency_ms=50.0,
            failure_rate=0.1,
            vm_count=5
        )
        enable_mock_mode(config)
        
        active_config = get_mock_config()
        self.assertEqual(active_config.latency_ms, 50.0)
        self.assertEqual(active_config.failure_rate, 0.1)
        self.assertEqual(active_config.vm_count, 5)
    
    def test_disable_mock_mode(self):
        """Test disabling mock mode."""
        enable_mock_mode()
        self.assertTrue(is_mock_mode())
        
        disable_mock_mode()
        self.assertFalse(is_mock_mode())
        self.assertIsNone(get_mock_config())
    
    def test_mock_mode_context_manager(self):
        """Test mock_mode context manager."""
        self.assertFalse(is_mock_mode())
        
        with mock_mode(latency_ms=10.0):
            self.assertTrue(is_mock_mode())
            config = get_mock_config()
            self.assertEqual(config.latency_ms, 10.0)
        
        self.assertFalse(is_mock_mode())
    
    def test_mock_mode_context_manager_preserves_previous(self):
        """Test that context manager preserves previous mock state."""
        enable_mock_mode(MockConfig(latency_ms=100.0))
        
        with mock_mode(latency_ms=5.0):
            self.assertEqual(get_mock_config().latency_ms, 5.0)
        
        self.assertEqual(get_mock_config().latency_ms, 100.0)


class TestMockBehaviors(unittest.TestCase):
    """Test different mock behavior modes."""
    
    def setUp(self):
        disable_mock_mode()
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_normal_behavior(self):
        """Test NORMAL behavior returns mock data."""
        enable_mock_mode(MockConfig(behavior=MockBehavior.NORMAL))
        vm_manager = MockVMManager()
        
        vms = vm_manager.list_vms()
        self.assertIsInstance(vms, list)
        self.assertTrue(len(vms) > 0)
    
    def test_fail_always_behavior(self):
        """Test FAIL_ALWAYS raises exception."""
        enable_mock_mode(MockConfig(behavior=MockBehavior.FAIL_ALWAYS))
        vm_manager = MockVMManager()
        
        with self.assertRaises(MockServiceError):
            vm_manager.list_vms()
    
    def test_flaky_behavior_with_high_failure_rate(self):
        """Test FLAKY behavior with 100% failure rate."""
        enable_mock_mode(MockConfig(
            behavior=MockBehavior.FLAKY,
            failure_rate=1.0  # Always fail
        ))
        vm_manager = MockVMManager()
        
        with self.assertRaises(MockServiceError):
            vm_manager.list_vms()
    
    def test_flaky_behavior_with_zero_failure_rate(self):
        """Test FLAKY behavior with 0% failure rate succeeds."""
        enable_mock_mode(MockConfig(
            behavior=MockBehavior.FLAKY,
            failure_rate=0.0  # Never fail
        ))
        vm_manager = MockVMManager()
        
        # Should succeed
        vms = vm_manager.list_vms()
        self.assertIsInstance(vms, list)
    
    def test_latency_simulation(self):
        """Test latency is added when configured."""
        latency_ms = 50.0
        enable_mock_mode(MockConfig(latency_ms=latency_ms))
        vm_manager = MockVMManager()
        
        start = time.perf_counter()
        vm_manager.list_vms()
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        # Should take at least the configured latency
        self.assertGreaterEqual(elapsed_ms, latency_ms * 0.9)  # Allow 10% variance


class TestMockVMManager(unittest.TestCase):
    """Test MockVMManager operations."""
    
    def setUp(self):
        enable_mock_mode(MockConfig(vm_count=5))
        self.vm_manager = MockVMManager()
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_list_vms(self):
        """Test listing VMs."""
        vms = self.vm_manager.list_vms()
        
        self.assertIsInstance(vms, list)
        self.assertEqual(len(vms), 5)  # vm_count=5
        
        # Check VM structure
        vm = vms[0]
        self.assertIn('id', vm)
        self.assertIn('name', vm)
        self.assertIn('status', vm)
        self.assertIn('vcpus', vm)
        self.assertIn('memory_mb', vm)
    
    def test_get_vm(self):
        """Test getting a specific VM."""
        vms = self.vm_manager.list_vms()
        vm_id = vms[0]['id']
        
        vm = self.vm_manager.get_vm(vm_id=vm_id)
        
        self.assertIsNotNone(vm)
        self.assertEqual(vm['id'], vm_id)
    
    def test_get_vm_not_found(self):
        """Test getting non-existent VM returns None."""
        vm = self.vm_manager.get_vm(vm_id='nonexistent-vm')
        self.assertIsNone(vm)
    
    def test_create_vm(self):
        """Test creating a new VM."""
        result = self.vm_manager.create_vm(
            name='test-new-vm',
            vcpus=4,
            memory_mb=8192
        )
        
        self.assertIn('id', result)
        self.assertEqual(result['name'], 'test-new-vm')
        self.assertEqual(result['status'], 'stopped')
        
        # Verify it's in the state
        state = get_mock_state()
        self.assertIn(result['id'], state['vms'])
    
    def test_start_vm(self):
        """Test starting a VM."""
        vms = self.vm_manager.list_vms()
        vm_id = vms[0]['id']
        
        result = self.vm_manager.start_vm(vm_id=vm_id)
        
        self.assertEqual(result['status'], 'success')
        
        # Verify VM status changed
        state = get_mock_state()
        self.assertEqual(state['vms'][vm_id]['status'], 'running')
    
    def test_stop_vm(self):
        """Test stopping a VM."""
        # First start a VM
        vms = self.vm_manager.list_vms()
        vm_id = vms[0]['id']
        self.vm_manager.start_vm(vm_id=vm_id)
        
        # Then stop it
        result = self.vm_manager.stop_vm(vm_id=vm_id)
        
        self.assertEqual(result['status'], 'success')
        
        # Verify VM status changed
        state = get_mock_state()
        self.assertEqual(state['vms'][vm_id]['status'], 'stopped')
    
    def test_delete_vm(self):
        """Test deleting a VM."""
        vms = self.vm_manager.list_vms()
        vm_id = vms[0]['id']
        initial_count = len(vms)
        
        result = self.vm_manager.delete_vm(vm_id=vm_id)
        
        self.assertEqual(result['status'], 'success')
        
        # Verify VM was removed
        state = get_mock_state()
        self.assertNotIn(vm_id, state['vms'])
        self.assertEqual(len(state['vms']), initial_count - 1)


class TestMockContainerManager(unittest.TestCase):
    """Test MockContainerManager operations."""
    
    def setUp(self):
        enable_mock_mode(MockConfig(container_count=10))
        self.container_manager = MockContainerManager()
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_list_containers(self):
        """Test listing containers."""
        containers = self.container_manager.list_containers()
        
        self.assertIsInstance(containers, list)
        self.assertEqual(len(containers), 10)
        
        # Check container structure
        container = containers[0]
        self.assertIn('id', container)
        self.assertIn('name', container)
        self.assertIn('status', container)
        self.assertIn('image', container)
    
    def test_get_container(self):
        """Test getting a specific container."""
        containers = self.container_manager.list_containers()
        container_id = containers[0]['id']
        
        container = self.container_manager.get_container(container_id=container_id)
        
        self.assertIsNotNone(container)
        self.assertEqual(container['id'], container_id)


class TestMockStorageManager(unittest.TestCase):
    """Test MockStorageManager operations."""
    
    def setUp(self):
        enable_mock_mode(MockConfig(storage_pool_count=3))
        self.storage_manager = MockStorageManager()
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_list_pools(self):
        """Test listing storage pools."""
        pools = self.storage_manager.list_pools()
        
        self.assertIsInstance(pools, list)
        self.assertEqual(len(pools), 3)
        
        # Check pool structure
        pool = pools[0]
        self.assertIn('id', pool)
        self.assertIn('name', pool)
        self.assertIn('capacity_gb', pool)
        self.assertIn('used_gb', pool)
    
    def test_get_pool(self):
        """Test getting a specific pool."""
        pools = self.storage_manager.list_pools()
        pool_id = pools[0]['id']
        
        pool = self.storage_manager.get_pool(pool_id=pool_id)
        
        self.assertIsNotNone(pool)
        self.assertEqual(pool['id'], pool_id)


class TestMockHealthChecker(unittest.TestCase):
    """Test MockHealthChecker operations."""
    
    def setUp(self):
        enable_mock_mode()
        self.health_checker = MockHealthChecker()
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_check_health(self):
        """Test health check returns healthy status."""
        health = self.health_checker.check_health()
        
        self.assertEqual(health['status'], 'healthy')
        self.assertIn('services', health)
        self.assertIn('kvm', health['services'])


class TestMockSecretsManager(unittest.TestCase):
    """Test MockSecretsManager operations."""
    
    def setUp(self):
        enable_mock_mode()
        self.secrets_manager = MockSecretsManager()
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_list_secrets(self):
        """Test listing secrets."""
        secrets = self.secrets_manager.list_secrets()
        
        self.assertIsInstance(secrets, list)
        self.assertTrue(len(secrets) > 0)
        
        # Check secret structure (metadata only)
        secret = secrets[0]
        self.assertIn('id', secret)
        self.assertIn('name', secret)
        self.assertIn('type', secret)
    
    def test_get_secret(self):
        """Test getting a secret value."""
        secrets = self.secrets_manager.list_secrets()
        secret_id = secrets[0]['id']
        
        secret = self.secrets_manager.get_secret(secret_id=secret_id)
        
        self.assertIsNotNone(secret)
        self.assertIn('value', secret)  # Should have decrypted value
        self.assertFalse(secret['value_masked'])


class TestMockStateManagement(unittest.TestCase):
    """Test mock state management utilities."""
    
    def setUp(self):
        enable_mock_mode(MockConfig(vm_count=5))
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_get_mock_state(self):
        """Test getting mock state returns copy."""
        state = get_mock_state()
        
        self.assertIn('vms', state)
        self.assertIn('containers', state)
        self.assertIn('storage_pools', state)
    
    def test_reset_mock_state(self):
        """Test resetting mock state."""
        # Modify state
        vm_manager = MockVMManager()
        vm_manager.create_vm(name='test-vm')
        
        initial_count = len(get_mock_state()['vms'])
        
        # Reset state
        reset_mock_state()
        
        # Should be back to original count
        self.assertEqual(len(get_mock_state()['vms']), 5)  # vm_count=5
    
    def test_inject_vm(self):
        """Test injecting a VM into mock state."""
        custom_vm = {
            'name': 'injected-vm',
            'status': 'running',
            'vcpus': 16,
            'memory_mb': 32768
        }
        
        vm_id = inject_vm(custom_vm)
        
        state = get_mock_state()
        self.assertIn(vm_id, state['vms'])
        self.assertEqual(state['vms'][vm_id]['name'], 'injected-vm')
    
    def test_inject_container(self):
        """Test injecting a container into mock state."""
        custom_container = {
            'name': 'injected-container',
            'status': 'running',
            'image': 'custom:latest'
        }
        
        container_id = inject_container(custom_container)
        
        state = get_mock_state()
        self.assertIn(container_id, state['containers'])
    
    def test_clear_vms(self):
        """Test clearing all VMs."""
        self.assertTrue(len(get_mock_state()['vms']) > 0)
        
        clear_vms()
        
        self.assertEqual(len(get_mock_state()['vms']), 0)
    
    def test_clear_containers(self):
        """Test clearing all containers."""
        self.assertTrue(len(get_mock_state()['containers']) > 0)
        
        clear_containers()
        
        self.assertEqual(len(get_mock_state()['containers']), 0)


class TestMockManagerFactory(unittest.TestCase):
    """Test mock manager factory function."""
    
    def setUp(self):
        enable_mock_mode()
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_get_vm_manager(self):
        """Test getting VM manager."""
        manager = get_mock_manager('vm')
        self.assertIsInstance(manager, MockVMManager)
    
    def test_get_container_manager(self):
        """Test getting container manager."""
        manager = get_mock_manager('container')
        self.assertIsInstance(manager, MockContainerManager)
    
    def test_get_storage_manager(self):
        """Test getting storage manager."""
        manager = get_mock_manager('storage')
        self.assertIsInstance(manager, MockStorageManager)
    
    def test_get_network_manager(self):
        """Test getting network manager."""
        manager = get_mock_manager('network')
        self.assertIsInstance(manager, MockNetworkManager)
    
    def test_get_health_manager(self):
        """Test getting health checker."""
        manager = get_mock_manager('health')
        self.assertIsInstance(manager, MockHealthChecker)
    
    def test_get_secrets_manager(self):
        """Test getting secrets manager."""
        manager = get_mock_manager('secrets')
        self.assertIsInstance(manager, MockSecretsManager)
    
    def test_invalid_manager_type(self):
        """Test invalid manager type raises error."""
        with self.assertRaises(ValueError):
            get_mock_manager('invalid')


class TestStatePersistence(unittest.TestCase):
    """Test mock state persistence."""
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_persist_state_to_file(self):
        """Test persisting state to file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            state_file = f.name
        
        try:
            enable_mock_mode(MockConfig(
                vm_count=3,
                persist_state=True,
                state_file=state_file
            ))
            
            # Create a VM to modify state
            vm_manager = MockVMManager()
            vm_manager.create_vm(name='persistent-vm')
            
            # Verify file was created (note: save happens on create)
            self.assertTrue(os.path.exists(state_file))
            
            # Read and verify JSON
            with open(state_file, 'r') as f:
                data = json.load(f)
            
            self.assertIn('vms', data)
        finally:
            if os.path.exists(state_file):
                os.unlink(state_file)


class TestAutoEnableMockMode(unittest.TestCase):
    """Test auto-enable mock mode detection."""
    
    def setUp(self):
        disable_mock_mode()
        # Clear environment variables
        for var in ['DEBVISOR_MOCK_MODE', 'CI', 'GITHUB_ACTIONS']:
            if var in os.environ:
                del os.environ[var]
    
    def tearDown(self):
        disable_mock_mode()
        # Clean up environment
        for var in ['DEBVISOR_MOCK_MODE', 'CI', 'GITHUB_ACTIONS']:
            if var in os.environ:
                del os.environ[var]
    
    def test_auto_enable_with_mock_mode_env(self):
        """Test auto-enable with DEBVISOR_MOCK_MODE=1."""
        os.environ['DEBVISOR_MOCK_MODE'] = '1'
        
        result = auto_enable_mock_mode()
        
        self.assertTrue(result)
        self.assertTrue(is_mock_mode())
    
    def test_auto_enable_with_ci_env(self):
        """Test auto-enable with CI environment."""
        os.environ['CI'] = 'true'
        
        result = auto_enable_mock_mode()
        
        self.assertTrue(result)
        self.assertTrue(is_mock_mode())
    
    def test_auto_enable_with_github_actions(self):
        """Test auto-enable with GITHUB_ACTIONS environment."""
        os.environ['GITHUB_ACTIONS'] = 'true'
        
        result = auto_enable_mock_mode()
        
        self.assertTrue(result)
        self.assertTrue(is_mock_mode())
    
    def test_auto_enable_without_env_vars(self):
        """Test auto-enable without environment variables returns True (pytest detected)."""
        # Since we're running under pytest, it should detect that
        result = auto_enable_mock_mode()
        
        # pytest is imported, so it should enable mock mode
        self.assertTrue(result)


class TestMockDataGeneration(unittest.TestCase):
    """Test mock data generation quality."""
    
    def setUp(self):
        enable_mock_mode(MockConfig(
            vm_count=100,
            container_count=50,
            seed=42  # Reproducible
        ))
    
    def tearDown(self):
        disable_mock_mode()
    
    def test_vm_data_completeness(self):
        """Test VMs have all required fields."""
        state = get_mock_state()
        vm = list(state['vms'].values())[0]
        
        required_fields = [
            'id', 'uuid', 'name', 'status', 'vcpus', 'memory_mb',
            'disk_gb', 'hypervisor', 'host', 'created_at', 'updated_at',
            'network_interfaces', 'disks', 'tags', 'metadata'
        ]
        
        for field in required_fields:
            self.assertIn(field, vm, f"Missing field: {field}")
    
    def test_vm_status_distribution(self):
        """Test VMs have realistic status distribution."""
        state = get_mock_state()
        vms = list(state['vms'].values())
        
        statuses = [vm['status'] for vm in vms]
        running_count = statuses.count('running')
        
        # Most VMs should be running (weighted 60%)
        self.assertGreater(running_count, len(vms) * 0.4)
    
    def test_container_data_completeness(self):
        """Test containers have all required fields."""
        state = get_mock_state()
        container = list(state['containers'].values())[0]
        
        required_fields = [
            'id', 'short_id', 'name', 'status', 'image',
            'created_at', 'ports', 'labels', 'resource_limits'
        ]
        
        for field in required_fields:
            self.assertIn(field, container, f"Missing field: {field}")
    
    def test_storage_pool_capacity_logic(self):
        """Test storage pools have valid capacity calculations."""
        state = get_mock_state()
        pools = list(state['storage_pools'].values())
        
        for pool in pools:
            self.assertGreater(pool['capacity_gb'], 0)
            self.assertGreaterEqual(pool['available_gb'], 0)
            self.assertEqual(
                pool['available_gb'],
                pool['capacity_gb'] - pool['used_gb']
            )
    
    def test_seed_reproducibility(self):
        """Test that seed produces reproducible data."""
        state1 = get_mock_state()
        vm_ids_1 = sorted(state1['vms'].keys())
        
        # Reset with same seed
        reset_mock_state()
        
        state2 = get_mock_state()
        vm_ids_2 = sorted(state2['vms'].keys())
        
        # With same seed, should have same VM IDs
        self.assertEqual(vm_ids_1, vm_ids_2)


if __name__ == '__main__':
    unittest.main()
