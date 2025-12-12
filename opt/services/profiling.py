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

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
Performance Profiling for DebVisor Services

Provides runtime performance monitoring, bottleneck detection, and metrics collection
for identifying and optimizing slow code paths.

Features:
- Function-level performance profiling
- Memory usage tracking
- CPU profiling integration
- Bottleneck detection
- Performance trend analysis
- Flame graph support
- Resource utilization monitoring

Author: DebVisor Team
Date: 2025-11-26
"""

import time
from typing import TypeVar
from typing import Tuple
from datetime import datetime, timezone
import asyncio
import logging
import psutil
import os
from typing import Any, Optional, Dict, List, Callable, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import functools
import tracemalloc
from collections import defaultdict

_logger=logging.getLogger(__name__)

# Type variable for decorated functions
F=TypeVar("F", bound=Callable[..., Any])


class ResourceType(Enum):
    """Types of resources to monitor"""

    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    THREADS = "threads"


@dataclass


class FunctionProfile:
    """Profile data for a single function call"""

    function_name: str
    module_name: str
    call_count: int = 1
    total_time_ms: float = 0.0
    min_time_ms: float=float("inf")
    max_time_ms: float=float("inf")
    avg_time_ms: float = 0.0
    memory_delta_mb: float = 0.0
    peak_memory_mb: float = 0.0
    start_time: datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    children: List["FunctionProfile"] = field(default_factory=list)

    @property

    def full_name(self) -> str:
        """Get fully qualified name"""
        return f"{self.module_name}.{self.function_name}"

    def add_call(self, duration_ms: float, memory_mb: float=0.0) -> None:
        """Record a function call"""
        self.call_count += 1
        self.total_time_ms += duration_ms
        self.min_time_ms=min(self.min_time_ms, duration_ms)
        self.max_time_ms=max(self.max_time_ms, duration_ms)
        self.avg_time_ms = self.total_time_ms / self.call_count
        self.memory_delta_mb += memory_mb
        self.peak_memory_mb=max(self.peak_memory_mb, memory_mb)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        _d=asdict(self)
        d["full_name"] = self.full_name
        d["start_time"] = self.start_time.isoformat()
        d["children"] = [c.to_dict() for c in self.children]
        return d


@dataclass


class ResourceSnapshot:
    """Snapshot of system resource usage"""

    timestamp: datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    process_cpu_percent: float = 0.0
    process_memory_mb: float = 0.0
    system_cpu_percent: float = 0.0
    system_memory_percent: float = 0.0
    disk_usage_percent: float = 0.0
    threads_count: int = 0
    open_files: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        _d=asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


class PerformanceProfiler:
    """
    Main performance profiler for DebVisor.

    Tracks function execution times, memory usage, and system resources.
    Provides reports on performance hotspots and bottlenecks.

    Attributes:
        profiles: Dictionary of function profiles keyed by full name
        resource_snapshots: List of resource usage snapshots
        current_stack: Stack of active function profiles
        process: Current process handle for resource monitoring
        enabled: Whether profiling is active
    """

    def __init__(self) -> None:
        """Initialize the performance profiler."""
        self.profiles: Dict[str, FunctionProfile] = {}
        self.resource_snapshots: List[ResourceSnapshot] = []
        self.current_stack: List[FunctionProfile] = []
        self.process=psutil.Process(os.getpid())
        self.enabled = True

    def profile_function(self, func_name: str, module_name: str) -> FunctionProfile:
        """
        Get or create profile for function.

        Args:
            func_name: Function name
            module_name: Module name

        Returns:
            FunctionProfile for the function
        """
        key = f"{module_name}.{func_name}"
        if key not in self.profiles:
            self.profiles[key] = FunctionProfile(
                _function_name = func_name, module_name=module_name
            )
        return self.profiles[key]

    def start_profiling(
        self, func_name: str, module_name: str
    ) -> Tuple[Optional[FunctionProfile], Optional[float], Optional[float]]:
        """
        Start profiling a function.

        Args:
            func_name: Function name
            module_name: Module name

        Returns:
            Tuple of (profile, start_time, mem_before) or (None, None, None) if disabled
        """
        if not self.enabled:
            return None, None, None

        _profile=self.profile_function(func_name, module_name)
        _start_time=time.perf_counter()

        # Capture memory before
        tracemalloc.start()
        _mem_before=self._get_memory_usage()

        return profile, start_time, mem_before

    def end_profiling(
        self,
        profile: Optional[FunctionProfile],
        start_time: Optional[float],
        mem_before: Optional[float],
    ) -> None:
        """
        End profiling and record results.

        Args:
            profile: FunctionProfile from start_profiling
            start_time: Start timestamp from start_profiling
            mem_before: Memory usage from start_profiling
        """
        if not self.enabled or profile is None:
            return

        _end_time=time.perf_counter()
        _mem_after=self._get_memory_usage()

        _duration_ms=(end_time - start_time) * 1000 if start_time is not None else 0.0
        memory_delta = mem_after - mem_before if mem_before else 0.0

        profile.add_call(duration_ms, memory_delta)
        tracemalloc.stop()

    def _get_memory_usage(self) -> float:
        """
        Get process memory usage in MB.

        Returns:
            Memory usage in megabytes
        """
        try:
            return float(self.process.memory_info().rss / (1024 * 1024))
        except BaseException:
            return 0.0

    def capture_resource_snapshot(self) -> ResourceSnapshot:
        """Capture current resource usage"""
        try:
            _cpu_percent=self.process.cpu_percent(interval=0.1)
            _memory_mb=self._get_memory_usage()
            # memory_percent = self.process.memory_percent()

            # System-wide metrics
            _system_cpu=psutil.cpu_percent(interval=0.1)
            _system_memory=psutil.virtual_memory().percent
            _disk=psutil.disk_usage("/").percent

            _threads=self.process.num_threads()
            _open_files=len(self.process.open_files())

            _snapshot = ResourceSnapshot(
                _process_cpu_percent = cpu_percent,
                _process_memory_mb = memory_mb,
                _system_cpu_percent = system_cpu,
                _system_memory_percent = system_memory,
                _disk_usage_percent = disk,
                _threads_count = threads,
                _open_files = open_files,
            )

            self.resource_snapshots.append(snapshot)
            return snapshot
        except Exception as e:
            logger.error(f"Error capturing resource snapshot: {e}")
            return ResourceSnapshot()

    def get_top_functions(
        self, n: int = 10, sort_by: str = "total_time_ms"
    ) -> List[FunctionProfile]:
        """
        Get top N functions by metric.

        Args:
            n: Number of functions to return
            sort_by: Metric to sort by (total_time_ms, call_count, memory_delta_mb)

        Returns:
            List of top FunctionProfile instances
        """
        _profiles=list(self.profiles.values())
        profiles.sort(key=lambda p: getattr(p, sort_by, 0), reverse=True)
        return profiles[:n]

    def get_slow_functions(self, threshold_ms: float=100) -> List[FunctionProfile]:
        """
        Get functions slower than threshold.

        Args:
            threshold_ms: Minimum average time in milliseconds

        Returns:
            List of slow FunctionProfile instances
        """
        return [p for p in self.profiles.values() if p.avg_time_ms > threshold_ms]

    def get_memory_heavy_functions(
        self, threshold_mb: float = 10.0
    ) -> List[FunctionProfile]:
        """
        Get functions using lots of memory.

        Args:
            threshold_mb: Minimum memory delta in megabytes

        Returns:
            List of memory-heavy FunctionProfile instances
        """
        return [p for p in self.profiles.values() if p.memory_delta_mb > threshold_mb]

    def get_profile_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive profile report.

        Returns:
            Dictionary with summary, top functions, slow functions,
            memory-heavy functions, and resource snapshots
        """
        _top_by_time=self.get_top_functions(n=10, sort_by="total_time_ms")
        _top_by_calls=self.get_top_functions(n=10, sort_by="call_count")
        _top_by_memory=self.get_top_functions(n=10, sort_by="memory_delta_mb")

        _slow=self.get_slow_functions(threshold_ms=50)
        _memory_heavy=self.get_memory_heavy_functions(threshold_mb=5.0)

        # Calculate total time
        _total_time=sum(p.total_time_ms for p in self.profiles.values())

        return {
            "summary": {
                "total_functions": len(self.profiles),
                "total_time_ms": total_time,
                "slow_functions": len(slow),
                "memory_heavy_functions": len(memory_heavy),
                "total_snapshots": len(self.resource_snapshots),
            },
            "top_by_time": [p.to_dict() for p in top_by_time],
            "top_by_calls": [p.to_dict() for p in top_by_calls],
            "top_by_memory": [p.to_dict() for p in top_by_memory],
            "slow_functions": [p.to_dict() for p in slow[:5]],
            "memory_heavy": [p.to_dict() for p in memory_heavy[:5]],
            "resource_snapshots": [s.to_dict() for s in self.resource_snapshots[-10:]],
        }

    def get_flame_graph_data(self) -> Dict[str, Any]:
        """
        Generate data for flame graph visualization.

        Returns:
            Dictionary with stacks and total_time_ms for flame graph rendering
        """
        call_stacks: Dict[str, float] = defaultdict(int)
        total_time = 0.0

        for name, profile in self.profiles.items():
        # Create simplified call stack
            _stack_str=" ".join([name] * profile.call_count)
            call_stacks[stack_str] = profile.total_time_ms
            total_time += profile.total_time_ms

        return {
            "stacks": [
                {
                    "stack": stack,
                    "time_ms": time_ms,
                    "percent": (time_ms / total_time * 100) if total_time > 0 else 0,
                }
                for stack, time_ms in sorted(
                    call_stacks.items(), key=lambda x: x[1], reverse=True
                )
            ],
            "total_time_ms": total_time,
        }

    def reset(self) -> None:
        """Reset all profiling data."""
        self.profiles.clear()
        self.resource_snapshots.clear()
        self.current_stack.clear()

    def enable(self) -> None:
        """Enable profiling."""
        self.enabled = True

    def disable(self) -> None:
        """Disable profiling."""
        self.enabled = False


def profile_function(func_or_coro: Optional[F] = None) -> Union[F, Callable[[F], F]]:
    """
    Decorator to profile async and sync functions.

    Tracks execution time and memory usage for the decorated function.
    Can be used with or without parentheses.

    Args:
        func_or_coro: Function to decorate (optional)

    Returns:
        Decorated function or decorator

    Example:
        @profile_function

        def my_function() -> None:
            pass

        @profile_function()
        async def my_async_function():
            pass
    """

    def decorator(fn: F) -> F:
    # Get profiler instance
        _profiler=_get_global_profiler()

        # Determine if async or sync
        if asyncio.iscoroutinefunction(fn):

            @functools.wraps(fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                module = fn.__module__
                func_name = fn.__name__

                profile, start_time, mem_before = profiler.start_profiling(
                    func_name, module
                )

                try:
                    _result=await fn(*args, **kwargs)
                    return result
                finally:
                    profiler.end_profiling(profile, start_time, mem_before)

            return async_wrapper    # type: ignore
        else:

            @functools.wraps(fn)

            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                module = fn.__module__
                func_name = fn.__name__

                profile, start_time, mem_before = profiler.start_profiling(
                    func_name, module
                )

                try:
                    _result=fn(*args, **kwargs)
                    return result
                finally:
                    profiler.end_profiling(profile, start_time, mem_before)

            return sync_wrapper    # type: ignore

    # Handle both @profile_function and @profile_function() usage
    if func_or_coro is None:
        return decorator
    else:
        return decorator(func_or_coro)


class MonitoringContext:
    """
    Context manager for monitoring a code block.

    Provides a convenient way to profile specific sections of code
    without decorating entire functions.

    Example:
        with MonitoringContext("database_query"):
            _results=db.execute(query)
    """

    def __init__(
        self, name: str, profiler: Optional[PerformanceProfiler] = None
    ) -> None:
        """
        Initialize monitoring context.

        Args:
            name: Name for the profiled code block
            profiler: Optional custom profiler instance
        """
        self.name = name
        self.profiler=profiler or _get_global_profiler()
        self.start_time: Optional[float] = None
        self.mem_before: Optional[float] = None
        self.profile: Optional[FunctionProfile] = None

    def __enter__(self) -> "MonitoringContext":
        """Start monitoring."""
        self.profile, self.start_time, self.mem_before = self.profiler.start_profiling(
            self.name, "__main__"
        )
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Stop monitoring."""
        self.profiler.end_profiling(self.profile, self.start_time, self.mem_before)


class ResourceMonitor:
    """
    Monitor system resource constraints.

    Checks CPU, memory, and disk usage against thresholds
    and generates alerts when exceeded.

    Attributes:
        cpu_threshold: CPU usage percentage threshold
        memory_threshold: Memory usage percentage threshold
        disk_threshold: Disk usage percentage threshold
        process: Current process handle
        alerts: List of generated alert messages
    """

    def __init__(
        self,
        cpu_threshold: float = 90.0,
        memory_threshold: float = 85.0,
        disk_threshold: float = 90.0,
    ) -> None:
        """
        Initialize resource monitor.

        Args:
            cpu_threshold: CPU alert threshold percentage
            memory_threshold: Memory alert threshold percentage
            disk_threshold: Disk alert threshold percentage
        """
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold
        self.process=psutil.Process(os.getpid())
        self.alerts: List[str] = []

    def check_resources(self) -> Dict[str, Any]:
        """
        Check resource usage and return status.

        Returns:
            Dictionary with 'ok' status, 'warnings' list, and 'metrics' dict
        """
        try:
        # Get metrics
            _process_cpu=self.process.cpu_percent(interval=0.1)
            _process_mem_percent=self.process.memory_percent()
            _system_mem=psutil.virtual_memory()
            _disk=psutil.disk_usage("/").percent

            status: Dict[str, Any] = {
                "ok": True,
                "warnings": [],
                "metrics": {
                    "process_cpu_percent": process_cpu,
                    "process_memory_percent": process_mem_percent,
                    "system_memory_percent": system_mem.percent,
                    "disk_usage_percent": disk,
                },
            }

            # Check thresholds
            if process_cpu > self.cpu_threshold:
                status["warnings"].append(
                    f"CPU usage {process_cpu:.1f}% exceeds threshold {self.cpu_threshold}%"
                )
                status["ok"] = False

            if process_mem_percent > self.memory_threshold:
                status["warnings"].append(
                    f"Memory usage {process_mem_percent:.1f}% exceeds threshold {self.memory_threshold}%"
                )
                status["ok"] = False

            if disk > self.disk_threshold:
                status["warnings"].append(
                    f"Disk usage {disk:.1f}% exceeds threshold {self.disk_threshold}%"
                )
                status["ok"] = False

            if status["warnings"]:
                self.alerts.extend(status["warnings"])

            return status
        except Exception as e:
            logger.error(f"Error checking resources: {e}")
            return {
                "ok": False,
                "warnings": [f"Error checking resources: {e}"],
                "metrics": {},
            }

    def get_alerts(self, clear: bool=False) -> List[str]:
        """
        Get accumulated resource alerts.

        Args:
            clear: Whether to clear alerts after retrieval

        Returns:
            List of alert message strings
        """
        _alerts=self.alerts.copy()
        if clear:
            self.alerts.clear()
        return alerts


# Global profiler instance
_global_profiler: Optional[PerformanceProfiler] = None
_resource_monitor: Optional[ResourceMonitor] = None


def _get_global_profiler() -> PerformanceProfiler:
    """
    Get or create global profiler.

    Returns:
        Global PerformanceProfiler instance
    """
    global _global_profiler
    if _global_profiler is None:
        _global_profiler=PerformanceProfiler()
    return _global_profiler


def get_global_profiler() -> PerformanceProfiler:
    """
    Expose global profiler.

    Returns:
        Global PerformanceProfiler instance
    """
    return _get_global_profiler()


def get_resource_monitor() -> ResourceMonitor:
    """
    Get or create global resource monitor.

    Returns:
        Global ResourceMonitor instance
    """
    global _resource_monitor
    if _resource_monitor is None:
        _resource_monitor=ResourceMonitor()
    return _resource_monitor
