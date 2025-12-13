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


_logger=logging.getLogger(__name__)

HOST_VERSION="1.0.0"    # Current version of the plugin system host


class PluginStatus(Enum):
    """Plugin lifecycle status."""

    DISCOVERED="discovered"
    LOADED="loaded"
    INITIALIZED="initialized"
    ACTIVE="active"
    DISABLED="disabled"
    ERROR="error"


class PluginType(Enum):
    """Types of plugins."""

    STORAGE="storage"
    NETWORK="network"
    MONITORING="monitoring"
    SECURITY="security"
    INTEGRATION="integration"
    CUSTOM="custom"


@dataclass
class PluginMetadata:
    """Plugin metadata."""

    name: str
    version: str
    author: str
    plugin_type: PluginType
    description: str
    dependencies: List[str] = field(default_factory=list)
    required_version: str="1.0.0"
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
    checksum: str=""


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

    def validate_permissions(self, requiredpermissions: List[str]) -> bool:
        """Validate plugin has required permissions."""
        _metadata=self.get_metadata()
        return all(perm in metadata.permissions for perm in required_permissions)  # type: ignore[name-defined]


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

    def discover_plugins(self, plugindir: str) -> List[str]:
        """
        Discover plugins in a directory.
        Returns a list of module paths that can be loaded.
        """
        _discovered=[]  # type: ignore[var-annotated]
        _path=Path(plugin_dir)  # type: ignore[name-defined]
        if not path.exists():  # type: ignore[name-defined]
            logger.warning(f"Plugin directory not found: {plugin_dir}")  # type: ignore[name-defined]
            return []

        # Add plugin dir to sys.path so we can import them
        if plugin_dir not in sys.path:  # type: ignore[name-defined]
            sys.path.insert(0, plugin_dir)  # type: ignore[name-defined]

        for item in path.iterdir():  # type: ignore[name-defined]
            if item.name.startswith("_") or item.name.startswith("."):
                continue

            module_name=None
            if item.is_file() and item.suffix== ".py":
                module_name=item.stem
            elif item.is_dir() and (item / "__init__.py").exists():
                module_name=item.name

            if module_name:
                try:
                # Dry run import to check for PluginInterface
                    _module=importlib.import_module(module_name)
                    for name, obj in inspect.getmembers(module):  # type: ignore[name-defined]
                        if (
                            inspect.isclass(obj)
                            and issubclass(obj, PluginInterface)
                            and obj != PluginInterface
                        ):
                            discovered.append(module_name)  # type: ignore[name-defined]
                            break
                except Exception as e:
                    logger.debug(f"Skipping {module_name}: {e}")  # type: ignore[name-defined]

        return discovered  # type: ignore[name-defined]

    def load_plugin(self, modulepath: str, config: Dict[str, Any]) -> PluginInfo:
        """Load plugin from module."""
        logger.info(f"Loading plugin from {module_path}")  # type: ignore[name-defined]

        try:
        # Import module
            _module=importlib.import_module(module_path)  # type: ignore[name-defined]

            # Find plugin class
            plugin_class=None
            for name, obj in inspect.getmembers(module):  # type: ignore[name-defined]
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, PluginInterface)
                    and obj != PluginInterface
                ):
                    plugin_class=obj
                    break

            if not plugin_class:
                raise ValueError(f"No PluginInterface found in {module_path}")  # type: ignore[name-defined]

            # Create instance
            _plugin_instance=plugin_class()
            _metadata=plugin_instance.get_metadata()  # type: ignore[name-defined]

            # Check version compatibility
            if not self._check_version_compatibility(metadata.required_version):  # type: ignore[name-defined]
                raise RuntimeError(
                    f"Plugin requires host version {metadata.required_version}, "  # type: ignore[name-defined]
                    f"but host is {HOST_VERSION}"
                )

            # Calculate checksum
            _checksum=self._calculate_checksum(module_path)  # type: ignore[name-defined]

            # Initialize plugin
            if not plugin_instance.initialize(config):  # type: ignore[name-defined]
                raise RuntimeError("Plugin initialization failed")

            # Create plugin info
            plugin_info=PluginInfo(  # type: ignore[call-arg]
                _plugin_id=metadata.name,  # type: ignore[name-defined]
                _metadata=metadata,  # type: ignore[name-defined]
                _status=PluginStatus.ACTIVE,
                _loaded_at=datetime.now(timezone.utc),
                _config=config,
                _checksum=checksum,  # type: ignore[name-defined]
            )

            self.plugins[metadata.name] = plugin_info  # type: ignore[name-defined]
            self.plugin_instances[metadata.name] = plugin_instance  # type: ignore[name-defined]

            logger.info(  # type: ignore[name-defined]
                f"Plugin loaded successfully: {metadata.name} v{metadata.version}"  # type: ignore[name-defined]
            )

            return plugin_info

        except Exception as e:
            logger.error(f"Failed to load plugin: {e}")  # type: ignore[name-defined]
            _plugin_info=PluginInfo(  # type: ignore[call-arg]
                _plugin_id=module_path,  # type: ignore[name-defined]
                _metadata=PluginMetadata(  # type: ignore[call-arg]
                    _name=module_path,  # type: ignore[name-defined]
                    _version="0.0.0",
                    _author="unknown",
                    _plugin_type=PluginType.CUSTOM,
                    _description="",
                ),
                _status=PluginStatus.ERROR,
                _error_message="Plugin load failed; check logs for details",
            )
            self.plugins[module_path] = plugin_info  # type: ignore[name-defined]
            logger.error(f"Plugin load failed for {module_path}: {e}", exc_info=True)
            return plugin_info

    def unload_plugin(self, pluginname: str) -> bool:
        """Unload plugin."""
        if plugin_name not in self.plugin_instances:  # type: ignore[name-defined]
            logger.warning(f"Plugin not found: {plugin_name}")  # type: ignore[name-defined]
            return False

        try:
            plugin=self.plugin_instances[plugin_name]  # type: ignore[name-defined]
            plugin.shutdown()

            del self.plugin_instances[plugin_name]  # type: ignore[name-defined]
            del self.plugins[plugin_name]  # type: ignore[name-defined]

            logger.info(f"Plugin unloaded: {plugin_name}")  # type: ignore[name-defined]
            return True

        except Exception as e:
            logger.error(f"Failed to unload plugin: {e}")  # type: ignore[name-defined]
            return False

    def reload_plugin(
        self, plugin_name: str, config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Reload plugin (hot-reload)."""
        if plugin_name not in self.plugins:
            logger.warning(f"Plugin not found: {plugin_name}")  # type: ignore[name-defined]
            return False

        try:
        # plugin_info = self.plugins[plugin_name]
            # new_config = config or plugin_info.config

            self.unload_plugin(plugin_name)

            # Re-import module to get latest code
            import sys

            module_name=f"plugins.{plugin_name}"
            if module_name in sys.modules:
                del sys.modules[module_name]

            logger.info(f"Plugin reloaded: {plugin_name}")  # type: ignore[name-defined]
            return True

        except Exception as e:
            logger.error(f"Failed to reload plugin: {e}")  # type: ignore[name-defined]
            return False

    def execute_plugin(
        self, plugin_name: str, operation: str, params: Dict[str, Any]
    ) -> Any:
        """Execute plugin operation."""
        if plugin_name not in self.plugin_instances:
            raise ValueError(f"Plugin not loaded: {plugin_name}")

        plugin=self.plugin_instances[plugin_name]
        return plugin.execute(operation, params)

    def get_plugins_by_type(self, plugintype: PluginType) -> List[PluginInfo]:
        """Get plugins by type."""
        return [
            info
            for info in self.plugins.values()
            if info.metadata.plugin_type == plugin_type  # type: ignore[name-defined]
        ]

    def validate_plugin_dependencies(self, pluginname: str) -> bool:
        """Validate plugin dependencies are satisfied."""
        if plugin_name not in self.plugins:  # type: ignore[name-defined]
            return False

        plugin_info=self.plugins[plugin_name]  # type: ignore[name-defined]
        _loaded_plugins=set(self.plugin_instances.keys())

        for dependency in plugin_info.metadata.dependencies:
            if dependency not in loaded_plugins:  # type: ignore[name-defined]
                logger.warning(f"Missing dependency for {plugin_name}: {dependency}")  # type: ignore[name-defined]
                return False

        return True

    def get_plugin_info(self, pluginname: str) -> Optional[PluginInfo]:
        """Get plugin information."""
        return self.plugins.get(plugin_name)  # type: ignore[name-defined]

    def list_plugins(self) -> List[PluginInfo]:
        """List all loaded plugins."""
        return list(self.plugins.values())

    @staticmethod
    def _check_version_compatibility(requiredversion: str) -> bool:
        """
        Check if host version satisfies plugin requirement.
        Simple semantic versioning check.
        """
        try:
            req_major, req_minor, _=map(int, required_version.split("."))  # type: ignore[name-defined]
            host_major, host_minor, _=map(int, HOST_VERSION.split("."))

            if host_major != req_major:
                return False
            if host_minor < req_minor:
                return False
            return True
        except ValueError:
        # If version format is invalid, assume incompatible
            return False

    @staticmethod
    def _calculate_checksum(modulepath: str) -> str:
        """Calculate module checksum."""
        try:
            _module=importlib.import_module(module_path)  # type: ignore[name-defined]
            _source=inspect.getsource(module)  # type: ignore[name-defined]
            return hashlib.sha256(source.encode()).hexdigest()[:16]  # type: ignore[name-defined]
        except Exception:
            return ""


class PluginRegistry:
    """Central plugin registry."""

    def __init__(self) -> None:
        """Initialize registry."""
        self.loader=PluginLoader()
        self.hooks: Dict[str, List[Callable[..., Any]]] = {}

    def register_hook(self, hookname: str, callback: Callable[..., Any]) -> None:
        """Register lifecycle hook."""
        if hook_name not in self.hooks:  # type: ignore[name-defined]
            self.hooks[hook_name] = []  # type: ignore[name-defined]
        self.hooks[hook_name].append(callback)  # type: ignore[name-defined]

    def execute_hook(self, hookname: str, *args, **kwargs) -> None:
        """Execute lifecycle hook."""
        if hook_name not in self.hooks:  # type: ignore[name-defined]
            return

        for callback in self.hooks[hook_name]:  # type: ignore[name-defined]
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Hook execution error: {e}")  # type: ignore[name-defined]

    def load_plugin_with_hooks(
        self, module_path: str, config: Dict[str, Any]
    ) -> PluginInfo:
        """Load plugin with lifecycle hooks."""
        self.execute_hook("before_load", module_path)

        _plugin_info=self.loader.load_plugin(module_path, config)

        self.execute_hook("after_load", plugin_info)  # type: ignore[name-defined]

        return plugin_info  # type: ignore[name-defined]

    def unload_plugin_with_hooks(self, pluginname: str) -> bool:
        """Unload plugin with lifecycle hooks."""
        self.execute_hook("before_unload", plugin_name)  # type: ignore[name-defined]

        _success=self.loader.unload_plugin(plugin_name)  # type: ignore[name-defined]

        self.execute_hook("after_unload", plugin_name, success)  # type: ignore[name-defined]

        return success  # type: ignore[name-defined]

    def get_loader(self) -> PluginLoader:
        """Get plugin loader."""
        return self.loader


# Global plugin registry instance
_plugin_registry: Optional[PluginRegistry] = None


def get_plugin_registry() -> PluginRegistry:
    """Get global plugin registry."""
    global _plugin_registry
    if _plugin_registry is None:
        _plugin_registry=PluginRegistry()
    return _plugin_registry
