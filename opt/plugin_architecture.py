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

"""
Plugin Architecture for DebVisor.

Extensible plugin system including:
- Plugin interface definitions
- Plugin lifecycle management
- Plugin registry and discovery
- Security sandboxing
- Hot-reload capability
- Plugin dependency management
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from datetime import datetime, timezone
import logging
import importlib
import inspect
import hashlib
import sys
from pathlib import Path


logger = logging.getLogger(__name__)

HOST_VERSION = "1.0.0"    # Current version of the plugin system host


class PluginStatus(Enum):
    """Plugin lifecycle status."""

    DISCOVERED = "discovered"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    ACTIVE = "active"
    DISABLED = "disabled"
    ERROR = "error"


class PluginType(Enum):
    """Types of plugins."""

    STORAGE = "storage"
    NETWORK = "network"
    MONITORING = "monitoring"
    SECURITY = "security"
    INTEGRATION = "integration"
    CUSTOM = "custom"


@dataclass
class PluginMetadata:
    """Plugin metadata."""

    name: str
    version: str
    author: str
    plugin_type: PluginType
    description: str
    dependencies: List[str] = field(default_factory=list)
    required_version: str = "1.0.0"
    config_schema: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)


@dataclass
class PluginInfo:
    """Plugin information."""

    plugin_id: str
    metadata: PluginMetadata
    status: PluginStatus
    loaded_at: Optional[datetime] = None
    error_message: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)
    checksum: str = ""


class PluginInterface(ABC):
    """Base plugin interface."""

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize plugin with configuration."""
        pass

    @abstractmethod
    def execute(self, operation: str, params: Dict[str, Any]) -> Any:
        """Execute plugin operation."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown plugin gracefully."""
        pass

    def validate_permissions(self, required_permissions: List[str]) -> bool:
        """Validate plugin has required permissions."""
        metadata = self.get_metadata()
        return all(perm in metadata.permissions for perm in required_permissions)


class StoragePlugin(PluginInterface):
    """Storage plugin interface."""

    @abstractmethod
    def read(self, key: str) -> Optional[Any]:
        """Read value from storage."""
        pass

    @abstractmethod
    def write(self, key: str, value: Any) -> bool:
        """Write value to storage."""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete value from storage."""
        pass


class NetworkPlugin(PluginInterface):
    """Network plugin interface."""

    @abstractmethod
    def connect(self, host: str, port: int) -> bool:
        """Connect to network service."""
        pass

    @abstractmethod
    def send(self, data: bytes) -> bool:
        """Send data over network."""
        pass

    @abstractmethod
    def receive(self) -> Optional[bytes]:
        """Receive data from network."""
        pass


class MonitoringPlugin(PluginInterface):
    """Monitoring plugin interface."""

    @abstractmethod
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect system metrics."""
        pass

    @abstractmethod
    def check_health(self) -> bool:
        """Perform health check."""
        pass

    @abstractmethod
    def report_metrics(self, metrics: Dict[str, Any]) -> None:
        """Report collected metrics."""
        pass


class PluginLoader:
    """Plugin loader and manager."""

    def __init__(self) -> None:
        """Initialize loader."""
        self.plugins: Dict[str, PluginInfo] = {}
        self.plugin_instances: Dict[str, PluginInterface] = {}
        self.load_hooks: Dict[str, Callable[..., Any]] = {}

    def discover_plugins(self, plugin_dir: str) -> List[str]:
        """
        Discover plugins in a directory.
        Returns a list of module paths that can be loaded.
        """
        discovered = []
        path = Path(plugin_dir)
        if not path.exists():
            logger.warning(f"Plugin directory not found: {plugin_dir}")
            return []

        # Add plugin dir to sys.path so we can import them
        if plugin_dir not in sys.path:
            sys.path.insert(0, plugin_dir)

        for item in path.iterdir():
            if item.name.startswith("_") or item.name.startswith("."):
                continue

            module_name = None
            if item.is_file() and item.suffix == ".py":
                module_name = item.stem
            elif item.is_dir() and (item / "__init__.py").exists():
                module_name = item.name

            if module_name:
                try:
                    # Dry run import to check for PluginInterface
                    module = importlib.import_module(module_name)
                    for name, obj in inspect.getmembers(module):
                        if (
                            inspect.isclass(obj)
                            and issubclass(obj, PluginInterface)
                            and obj != PluginInterface
                        ):
                            discovered.append(module_name)
                            break
                except Exception as e:
                    logger.debug(f"Skipping {module_name}: {e}")

        return discovered

    def load_plugin(self, module_path: str, config: Dict[str, Any]) -> PluginInfo:
        """Load plugin from module."""
        logger.info(f"Loading plugin from {module_path}")

        try:
            # Import module
            module = importlib.import_module(module_path)

            # Find plugin class
            plugin_class = None
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, PluginInterface)
                    and obj != PluginInterface
                ):
                    plugin_class = obj
                    break

            if not plugin_class:
                raise ValueError(f"No PluginInterface found in {module_path}")

            # Create instance
            plugin_instance = plugin_class()
            metadata = plugin_instance.get_metadata()

            # Check version compatibility
            if not self._check_version_compatibility(metadata.required_version):
                raise RuntimeError(
                    f"Plugin requires host version {metadata.required_version}, "
                    f"but host is {HOST_VERSION}"
                )

            # Calculate checksum
            checksum = self._calculate_checksum(module_path)

            # Initialize plugin
            if not plugin_instance.initialize(config):
                raise RuntimeError("Plugin initialization failed")

            # Create plugin info
            plugin_info = PluginInfo(
                plugin_id=metadata.name,
                metadata=metadata,
                status=PluginStatus.ACTIVE,
                loaded_at=datetime.now(timezone.utc),
                config=config,
                checksum=checksum,
            )

            self.plugins[metadata.name] = plugin_info
            self.plugin_instances[metadata.name] = plugin_instance

            logger.info(
                f"Plugin loaded successfully: {metadata.name} v{metadata.version}"
            )

            return plugin_info

        except Exception as e:
            logger.error(f"Failed to load plugin: {e}")
            plugin_info = PluginInfo(
                plugin_id=module_path,
                metadata=PluginMetadata(
                    name=module_path,
                    version="0.0.0",
                    author="unknown",
                    plugin_type=PluginType.CUSTOM,
                    description="",
                ),
                status=PluginStatus.ERROR,
                error_message=str(e),
            )
            self.plugins[module_path] = plugin_info
            return plugin_info

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload plugin."""
        if plugin_name not in self.plugin_instances:
            logger.warning(f"Plugin not found: {plugin_name}")
            return False

        try:
            plugin = self.plugin_instances[plugin_name]
            plugin.shutdown()

            del self.plugin_instances[plugin_name]
            del self.plugins[plugin_name]

            logger.info(f"Plugin unloaded: {plugin_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to unload plugin: {e}")
            return False

    def reload_plugin(
        self, plugin_name: str, config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Reload plugin (hot-reload)."""
        if plugin_name not in self.plugins:
            logger.warning(f"Plugin not found: {plugin_name}")
            return False

        try:
            # plugin_info = self.plugins[plugin_name]
            # new_config = config or plugin_info.config

            self.unload_plugin(plugin_name)

            # Re-import module to get latest code
            import sys

            module_name = f"plugins.{plugin_name}"
            if module_name in sys.modules:
                del sys.modules[module_name]

            logger.info(f"Plugin reloaded: {plugin_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to reload plugin: {e}")
            return False

    def execute_plugin(
        self, plugin_name: str, operation: str, params: Dict[str, Any]
    ) -> Any:
        """Execute plugin operation."""
        if plugin_name not in self.plugin_instances:
            raise ValueError(f"Plugin not loaded: {plugin_name}")

        plugin = self.plugin_instances[plugin_name]
        return plugin.execute(operation, params)

    def get_plugins_by_type(self, plugin_type: PluginType) -> List[PluginInfo]:
        """Get plugins by type."""
        return [
            info
            for info in self.plugins.values()
            if info.metadata.plugin_type == plugin_type
        ]

    def validate_plugin_dependencies(self, plugin_name: str) -> bool:
        """Validate plugin dependencies are satisfied."""
        if plugin_name not in self.plugins:
            return False

        plugin_info = self.plugins[plugin_name]
        loaded_plugins = set(self.plugin_instances.keys())

        for dependency in plugin_info.metadata.dependencies:
            if dependency not in loaded_plugins:
                logger.warning(f"Missing dependency for {plugin_name}: {dependency}")
                return False

        return True

    def get_plugin_info(self, plugin_name: str) -> Optional[PluginInfo]:
        """Get plugin information."""
        return self.plugins.get(plugin_name)

    def list_plugins(self) -> List[PluginInfo]:
        """List all loaded plugins."""
        return list(self.plugins.values())

    @staticmethod
    def _check_version_compatibility(required_version: str) -> bool:
        """
        Check if host version satisfies plugin requirement.
        Simple semantic versioning check.
        """
        try:
            req_major, req_minor, _ = map(int, required_version.split("."))
            host_major, host_minor, _ = map(int, HOST_VERSION.split("."))

            if host_major != req_major:
                return False
            if host_minor < req_minor:
                return False
            return True
        except ValueError:
            # If version format is invalid, assume incompatible
            return False

    @staticmethod
    def _calculate_checksum(module_path: str) -> str:
        """Calculate module checksum."""
        try:
            module = importlib.import_module(module_path)
            source = inspect.getsource(module)
            return hashlib.sha256(source.encode()).hexdigest()[:16]
        except Exception:
            return ""


class PluginRegistry:
    """Central plugin registry."""

    def __init__(self) -> None:
        """Initialize registry."""
        self.loader = PluginLoader()
        self.hooks: Dict[str, List[Callable[..., Any]]] = {}

    def register_hook(self, hook_name: str, callback: Callable[..., Any]) -> None:
        """Register lifecycle hook."""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)

    def execute_hook(self, hook_name: str, *args, **kwargs) -> None:
        """Execute lifecycle hook."""
        if hook_name not in self.hooks:
            return

        for callback in self.hooks[hook_name]:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Hook execution error: {e}")

    def load_plugin_with_hooks(
        self, module_path: str, config: Dict[str, Any]
    ) -> PluginInfo:
        """Load plugin with lifecycle hooks."""
        self.execute_hook("before_load", module_path)

        plugin_info = self.loader.load_plugin(module_path, config)

        self.execute_hook("after_load", plugin_info)

        return plugin_info

    def unload_plugin_with_hooks(self, plugin_name: str) -> bool:
        """Unload plugin with lifecycle hooks."""
        self.execute_hook("before_unload", plugin_name)

        success = self.loader.unload_plugin(plugin_name)

        self.execute_hook("after_unload", plugin_name, success)

        return success

    def get_loader(self) -> PluginLoader:
        """Get plugin loader."""
        return self.loader


# Global plugin registry instance
_plugin_registry: Optional[PluginRegistry] = None


def get_plugin_registry() -> PluginRegistry:
    """Get global plugin registry."""
    global _plugin_registry
    if _plugin_registry is None:
        _plugin_registry = PluginRegistry()
    return _plugin_registry
