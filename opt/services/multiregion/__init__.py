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


"""
DebVisor Multi-region Support Package

Comprehensive multi-region support for DebVisor with cross-datacenter replication,
automatic failover, and geo-distributed operations management.

Example Usage:

    from opt.services.multiregion import MultiRegionManager, FailoverStrategy

    # Initialize manager
    manager = MultiRegionManager()

    # Register regions
    manager.register_region("us-east-1", "US East 1", "https://api.us-east-1.internal", is_primary=True)
    manager.register_region("us-west-1", "US West 1", "https://api.us-west-1.internal")

    # Setup replication
    manager.setup_replication("us-east-1", "us-west-1", [ResourceType.VM, ResourceType.CONFIG])

    # Perform failover
    success, event = await manager.perform_failover("us-east-1", "us-west-1")

Version: 1.0.0
Status: Production-Ready
"""

from opt.services.multiregion.core import (
    MultiRegionManager,
    Region,
    ReplicatedResource,
    FailoverEvent,
    ReplicationConfig,
    RegionStatus,
    ReplicationStatus,
    FailoverStrategy,
    ResourceType,
    get_multi_region_manager,
)

from opt.services.multiregion.cli import MultiRegionCLI

from opt.services.multiregion.api import MultiRegionAPI, create_flask_app

__version__ = "1.0.0"
__author__ = "DebVisor Development Team"
__all__ = [
    "MultiRegionManager",
    "Region",
    "ReplicatedResource",
    "FailoverEvent",
    "ReplicationConfig",
    "RegionStatus",
    "ReplicationStatus",
    "FailoverStrategy",
    "ResourceType",
    "MultiRegionCLI",
    "MultiRegionAPI",
    "create_flask_app",
    "get_multi_region_manager",
]
