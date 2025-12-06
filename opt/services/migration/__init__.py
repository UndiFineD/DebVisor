"""Migration services package for DebVisor.

Exposes advanced VM migration management utilities.
"""

from .advanced_migration import (
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

__all__ = [
    "MigrationStrategy",
    "MigrationState",
    "MigrationPlan",
    "MigrationProgress",
    "HostMetrics",
    "VMMemoryProfile",
    "TargetScore",
    "ConsolidationGoal",
    "ConsolidationPlan",
    "MemoryProfileAnalyzer",
    "TargetHostSelector",
    "TargetSelectionCriteria",
    "MigrationExecutor",
    "ResourceConsolidator",
    "AdvancedMigrationManager",
]
