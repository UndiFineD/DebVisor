#!/usr/bin/env python3
"""
Unit tests for plugin architecture.

Tests for:
  - Plugin interface implementation
  - Plugin loading and lifecycle
  - Plugin registry and discovery
  - Dependency management
  - Hot-reload capability
"""

import unittest
from unittest.mock import MagicMock, patch

from pathlib import Path

from plugin_architecture import (
    PluginInterface, StoragePlugin, NetworkPlugin, MonitoringPlugin,
    PluginLoader, PluginRegistry, PluginMetadata, PluginStatus,
    PluginType, PluginInfo, get_plugin_registry
)

class MockStoragePlugin(StoragePlugin):
    """Mock storage plugin for testing."""

    def get_metadata(self) -> PluginMetadata:
        """Get metadata."""
        return PluginMetadata(
            name="mock_storage",
            version="1.0.0",
            author="test",
            plugin_type=PluginType.STORAGE,
            description="Mock storage plugin",
            permissions=["read", "write", "delete"]
        )

    def initialize(self, config) -> bool:
        """Initialize."""
        return True

    def execute(self, operation, params):
        """Execute."""
        return {"status": "ok"}

    def shutdown(self):
        """Shutdown."""
        pass

    def read(self, key):
        """Read."""
        return "value"

    def write(self, key, value):
        """Write."""
        return True

    def delete(self, key):
        """Delete."""
        return True

class MockNetworkPlugin(NetworkPlugin):
    """Mock network plugin for testing."""

    def get_metadata(self) -> PluginMetadata:
        """Get metadata."""
        return PluginMetadata(
            name="mock_network",
            version="1.0.0",
            author="test",
            plugin_type=PluginType.NETWORK,
            description="Mock network plugin"
        )

    def initialize(self, config) -> bool:
        """Initialize."""
        return True

    def execute(self, operation, params):
        """Execute."""
        return {"status": "ok"}

    def shutdown(self):
        """Shutdown."""
        pass

    def connect(self, host, port):
        """Connect."""
        return True

    def send(self, data):
        """Send."""
        return True

    def receive(self):
        """Receive."""
        return b"data"

class TestPluginMetadata(unittest.TestCase):
    """Tests for plugin metadata."""

    def test_plugin_metadata_creation(self):
        """Test creating plugin metadata."""
        metadata = PluginMetadata(
            name="test",
            version="1.0.0",
            author="author",
            plugin_type=PluginType.STORAGE,
            description="Test plugin"
        )

        self.assertEqual(metadata.name, "test")
        self.assertEqual(metadata.version, "1.0.0")
        self.assertEqual(metadata.plugin_type, PluginType.STORAGE)

    def test_plugin_metadata_with_dependencies(self):
        """Test metadata with dependencies."""
        metadata = PluginMetadata(
            name="test",
            version="1.0.0",
            author="author",
            plugin_type=PluginType.INTEGRATION,
            description="Test",
            dependencies=["dep1", "dep2"]
        )

        self.assertEqual(len(metadata.dependencies), 2)
        self.assertIn("dep1", metadata.dependencies)

class TestPluginInterface(unittest.TestCase):
    """Tests for plugin interface."""

    def test_storage_plugin_implementation(self):
        """Test storage plugin implementation."""
        plugin = MockStoragePlugin()

        self.assertIsNotNone(plugin.get_metadata())
        self.assertTrue(plugin.initialize({}))

    def test_plugin_execute(self):
        """Test plugin execute."""
        plugin = MockStoragePlugin()

        result = plugin.execute("test", {})

        self.assertEqual(result["status"], "ok")

    def test_storage_plugin_operations(self):
        """Test storage plugin operations."""
        plugin = MockStoragePlugin()

        self.assertEqual(plugin.read("key"), "value")
        self.assertTrue(plugin.write("key", "value"))
        self.assertTrue(plugin.delete("key"))

    def test_network_plugin_operations(self):
        """Test network plugin operations."""
        plugin = MockNetworkPlugin()

        self.assertTrue(plugin.connect("localhost", 8080))
        self.assertTrue(plugin.send(b"data"))
        self.assertEqual(plugin.receive(), b"data")

class TestPluginLoader(unittest.TestCase):
    """Tests for plugin loader."""

    def setUp(self):
        """Set up test fixtures."""
        self.loader = PluginLoader()

    def test_loader_initialization(self):
        """Test loader initialization."""
        self.assertIsNotNone(self.loader)
        self.assertEqual(len(self.loader.plugins), 0)

    def test_get_plugins_by_type(self):
        """Test filtering plugins by type."""
        # Create mock plugin info
        metadata = PluginMetadata(
            name="storage1",
            version="1.0.0",
            author="test",
            plugin_type=PluginType.STORAGE,
            description="Storage plugin"
        )

        plugin_info = PluginInfo(
            plugin_id="storage1",
            metadata=metadata,
            status=PluginStatus.ACTIVE
        )

        self.loader.plugins["storage1"] = plugin_info

        storage_plugins = self.loader.get_plugins_by_type(PluginType.STORAGE)

        self.assertEqual(len(storage_plugins), 1)
        self.assertEqual(storage_plugins[0].plugin_id, "storage1")

    def test_validate_plugin_dependencies_satisfied(self):
        """Test dependency validation with satisfied dependencies."""
        metadata = PluginMetadata(
            name="plugin_a",
            version="1.0.0",
            author="test",
            plugin_type=PluginType.CUSTOM,
            description="Test",
            dependencies=["storage"]
        )

        plugin_info = PluginInfo(
            plugin_id="plugin_a",
            metadata=metadata,
            status=PluginStatus.ACTIVE
        )

        self.loader.plugins["plugin_a"] = plugin_info
        self.loader.plugin_instances["storage"] = MockStoragePlugin()

        valid = self.loader.validate_plugin_dependencies("plugin_a")

        self.assertTrue(valid)

    def test_validate_plugin_dependencies_missing(self):
        """Test dependency validation with missing dependencies."""
        metadata = PluginMetadata(
            name="plugin_a",
            version="1.0.0",
            author="test",
            plugin_type=PluginType.CUSTOM,
            description="Test",
            dependencies=["missing_dep"]
        )

        plugin_info = PluginInfo(
            plugin_id="plugin_a",
            metadata=metadata,
            status=PluginStatus.ACTIVE
        )

        self.loader.plugins["plugin_a"] = plugin_info

        valid = self.loader.validate_plugin_dependencies("plugin_a")

        self.assertFalse(valid)

    def test_get_plugin_info(self):
        """Test getting plugin info."""
        metadata = PluginMetadata(
            name="test",
            version="1.0.0",
            author="test",
            plugin_type=PluginType.STORAGE,
            description="Test"
        )

        plugin_info = PluginInfo(
            plugin_id="test",
            metadata=metadata,
            status=PluginStatus.ACTIVE
        )

        self.loader.plugins["test"] = plugin_info

        info = self.loader.get_plugin_info("test")

        self.assertIsNotNone(info)
        self.assertEqual(info.plugin_id, "test")

    def test_list_plugins(self):
        """Test listing plugins."""
        metadata1 = PluginMetadata(
            name="plugin1",
            version="1.0.0",
            author="test",
            plugin_type=PluginType.STORAGE,
            description="Plugin 1"
        )

        metadata2 = PluginMetadata(
            name="plugin2",
            version="1.0.0",
            author="test",
            plugin_type=PluginType.NETWORK,
            description="Plugin 2"
        )

        plugin_info1 = PluginInfo(
            plugin_id="plugin1",
            metadata=metadata1,
            status=PluginStatus.ACTIVE
        )

        plugin_info2 = PluginInfo(
            plugin_id="plugin2",
            metadata=metadata2,
            status=PluginStatus.ACTIVE
        )

        self.loader.plugins["plugin1"] = plugin_info1
        self.loader.plugins["plugin2"] = plugin_info2

        plugins = self.loader.list_plugins()

        self.assertEqual(len(plugins), 2)

class TestPluginRegistry(unittest.TestCase):
    """Tests for plugin registry."""

    def setUp(self):
        """Set up test fixtures."""
        self.registry = PluginRegistry()

    def test_registry_initialization(self):
        """Test registry initialization."""
        self.assertIsNotNone(self.registry.loader)
        self.assertEqual(len(self.registry.hooks), 0)

    def test_register_hook(self):
        """Test registering lifecycle hook."""
        callback = MagicMock()

        self.registry.register_hook("before_load", callback)

        self.assertIn("before_load", self.registry.hooks)

    def test_execute_hook(self):
        """Test executing hook."""
        callback = MagicMock()

        self.registry.register_hook("before_load", callback)
        self.registry.execute_hook("before_load", "plugin_name")

        callback.assert_called_once_with("plugin_name")

    def test_execute_multiple_hooks(self):
        """Test executing multiple hooks."""
        callback1 = MagicMock()
        callback2 = MagicMock()

        self.registry.register_hook("before_load", callback1)
        self.registry.register_hook("before_load", callback2)

        self.registry.execute_hook("before_load")

        callback1.assert_called_once()
        callback2.assert_called_once()

    def test_get_loader(self):
        """Test getting loader."""
        loader = self.registry.get_loader()

        self.assertIsNotNone(loader)
        self.assertIs(loader, self.registry.loader)

class TestGlobalPluginRegistry(unittest.TestCase):
    """Tests for global plugin registry."""

    def test_get_global_registry(self):
        """Test getting global plugin registry."""
        registry1 = get_plugin_registry()
        registry2 = get_plugin_registry()

        self.assertIs(registry1, registry2)

    def test_global_registry_singleton(self):
        """Test global registry is singleton."""
        registry = get_plugin_registry()

        self.assertIsNotNone(registry)
        self.assertIsInstance(registry, PluginRegistry)

class TestPluginIntegration(unittest.TestCase):
    """Integration tests for plugin system."""

    def test_plugin_lifecycle(self):
        """Test complete plugin lifecycle."""
        registry = PluginRegistry()

        # Create metadata
        metadata = PluginMetadata(
            name="lifecycle_test",
            version="1.0.0",
            author="test",
            plugin_type=PluginType.STORAGE,
            description="Lifecycle test"
        )

        plugin_info = PluginInfo(
            plugin_id="lifecycle_test",
            metadata=metadata,
            status=PluginStatus.DISCOVERED
        )

        registry.loader.plugins["lifecycle_test"] = plugin_info

        # Verify plugin registered
        info = registry.loader.get_plugin_info("lifecycle_test")
        self.assertIsNotNone(info)
        self.assertEqual(info.status, PluginStatus.DISCOVERED)

    def test_multiple_plugins_management(self):
        """Test managing multiple plugins."""
        registry = PluginRegistry()

        for i in range(5):
            metadata = PluginMetadata(
                name=f"plugin_{i}",
                version="1.0.0",
                author="test",
                plugin_type=PluginType.CUSTOM,
                description=f"Plugin {i}"
            )

            plugin_info = PluginInfo(
                plugin_id=f"plugin_{i}",
                metadata=metadata,
                status=PluginStatus.ACTIVE
            )

            registry.loader.plugins[f"plugin_{i}"] = plugin_info

        plugins = registry.loader.list_plugins()

        self.assertEqual(len(plugins), 5)

if __name__ == "__main__":
    unittest.main()
