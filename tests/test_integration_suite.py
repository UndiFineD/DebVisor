from typing import List
#!/usr/bin/env python3
"""
Integration Test Suite for DebVisor

Implements TEST-002: Multi-service integration tests for end-to-end workflows.

Features:
- Multi-service integration tests
- End-to-end workflow testing
- Database migration testing
- Service dependency validation
- Realistic test scenarios
- Automatic cleanup and teardown
"""

import pytest
from redis import Redis
import asyncio
import time

# Import services for integration testing
from opt.services.secrets.vault_manager import VaultClient, VaultConfig, AuthMethod
from opt.services.rbac.fine_grained_rbac import (
    RoleManager,
    AuthorizationContext,
    ResourceType,
    Action,
)
from opt.services.database.query_optimizer import (
    AsyncDatabasePool,
    CacheConfig,
    IndexDefinition,
    IndexType,
)


@pytest.fixture(scope="function")
def event_loop() -> None:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def vault_client() -> None:
    """Initialize Vault client for testing."""
    config = VaultConfig(
        url="http://127.0.0.1:8200",
        auth_method=AuthMethod.TOKEN,
        token="dev-only-token",
        verify_ssl=False,
    )

    client = VaultClient(config)
    yield client
    client.close()


@pytest.fixture(scope="function")
def role_manager() -> None:
    """Initialize RBAC manager for testing."""
    return RoleManager()


@pytest.fixture(scope="function")
async def database_pool() -> None:
    """Initialize database pool for testing."""
    dsn = "postgresql://test:test@localhost/debvisor_test"
    cache_config = CacheConfig(
        host="localhost",
        port=6379,
        enabled=True,
        default_ttl=60,
    )

    pool = AsyncDatabasePool(dsn, cache_config=cache_config)
    await pool.connect()

    # Create test schema
    await pool.execute(
        """
        CREATE TABLE IF NOT EXISTS test_vms (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            status VARCHAR(50),
            owner VARCHAR(255),
            tags JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """
    )

    yield pool

    # Cleanup
    await pool.execute("DROP TABLE IF EXISTS test_vms")
    await pool.close()


@pytest.mark.skip(reason="Requires Vault service running")
class TestSecretsManagement:
    """
    Integration tests for secrets management.

    Tests SECRET-001 implementation.
    """

    def test_create_and_read_secret(self, vault_client):
        """Test creating and reading secrets."""
        # Create secret
        metadata = vault_client.create_secret(
            path="integration/test/db_password",
            data={
                "username": "testuser",
                "password": "secret123",
                "host": "localhost",
            },
            custom_metadata={
                "owner": "integration_test",
                "environment": "test",
            },
        )

        assert metadata.version == 1
        assert metadata.path == "integration/test/db_password"

        # Read secret
        secret = vault_client.read_secret("integration/test/db_password")
        assert secret is not None
        assert secret["username"] == "testuser"
        assert secret["password"] == "secret123"

    def test_secret_rotation(self, vault_client):
        """Test secret rotation workflow."""
        path = "integration/test/rotated_secret"

        # Create initial secret
        vault_client.create_secret(
            path=path,
            data={"api_key": "initial_key"},
        )

        # Rotate secret
        new_metadata = vault_client.rotate_secret(
            path=path,
            new_data={"api_key": "rotated_key"},
        )

        assert new_metadata.version == 2

        # Read new version
        secret = vault_client.read_secret(path)
        assert secret["api_key"] == "rotated_key"

        # Read old version
        old_secret = vault_client.read_secret(path, version=1)
        assert old_secret["api_key"] == "initial_key"

    def test_secret_listing(self, vault_client):
        """Test listing secrets in a path."""
        # Create multiple secrets
        for i in range(3):
            vault_client.create_secret(
                path=f"integration/test/list/secret_{i}",
                data={"value": f"test_{i}"},
            )

        # List secrets
        secrets = vault_client.list_secrets("integration/test/list")
        assert len(secrets) >= 3
        assert any("secret_0" in s for s in secrets)


@pytest.mark.skip(reason="Requires Vault and RBAC services running")
class TestRBACIntegration:
    """
    Integration tests for fine-grained RBAC.

    Tests RBAC-001 implementation.
    """

    def test_role_assignment_and_authorization(self, role_manager):
        """Test role assignment and authorization decision."""
        # Assign operator role
        role_manager.assign_role("test_operator@example.com", "operator")

        # Test VM read permission (should be allowed)
        context = AuthorizationContext(
            principal_id="test_operator@example.com",
            principal_attributes={"department": "ops"},
            resource_type=ResourceType.VM,
            resource_id="vm-test-001",
            resource_attributes={},
            action=Action.READ,
        )

        decision = role_manager.authorize(context)
        assert decision.allowed is True
        assert len(decision.matched_permissions) > 0

        # Test user management permission (should be denied)
        context.resource_type = ResourceType.USER
        context.action = Action.DELETE

        decision = role_manager.authorize(context)
        assert decision.allowed is False
        assert len(decision.matched_permissions) == 0

    def test_conditional_permissions(self, role_manager):
        """Test time-based and IP-based conditional permissions."""
        from opt.services.rbac.fine_grained_rbac import (
            Role,
            Permission,
            Condition,
            ConditionType,
        )

        # Create role with office hours restriction
        office_hours = Condition(
            type=ConditionType.TIME_RANGE,
            parameters={
                "start_time": "00:00:00",    # Always allowed for testing
                "end_time": "23:59:59",
            },
        )

        office_network = Condition(
            type=ConditionType.IP_NETWORK,
            parameters={
                "allowed_networks": ["192.168.0.0/16"],
            },
        )

        test_role = Role(
            name="test_conditional",
            description="Test role with conditions",
            permissions=[
                Permission(
                    resource_type=ResourceType.VM,
                    resource_id=None,
                    actions=[Action.READ],
                    conditions=[office_hours, office_network],
                ),
            ],
        )

        role_manager.create_role(test_role)
        role_manager.assign_role("conditional_user@example.com", "test_conditional")

Test from office network (should be allowed)
        context = AuthorizationContext(
            principal_id="conditional_user@example.com",
            principal_attributes={},
            resource_type=ResourceType.VM,
            resource_id="vm-001",
            resource_attributes={},
            action=Action.READ,
            client_ip="192.168.1.100",
        )

        decision = role_manager.authorize(context)
        assert decision.allowed is True

Test from external IP (should be denied)
        context.client_ip = "8.8.8.8"
        decision = role_manager.authorize(context)
        assert decision.allowed is False

    def test_permission_inheritance(self, role_manager):
        """Test role hierarchy and permission inheritance."""
        from opt.services.rbac.fine_grained_rbac import Role, Permission

        # Create parent role
        parent_role = Role(
            name="test_parent",
            description="Parent role",
            permissions=[
                Permission(
                    resource_type=ResourceType.VM,
                    resource_id=None,
                    actions=[Action.READ],
                ),
            ],
        )

Create child role that inherits from parent
        child_role = Role(
            name="test_child",
            description="Child role",
            permissions=[
                Permission(
                    resource_type=ResourceType.SNAPSHOT,
                    resource_id=None,
                    actions=[Action.CREATE],
                ),
            ],
            parent_roles=["test_parent"],
        )

        role_manager.create_role(parent_role)
        role_manager.create_role(child_role)
        role_manager.assign_role("child_user@example.com", "test_child")

        # Get all permissions (should include inherited)
        all_permissions = role_manager.get_principal_permissions(
            "child_user@example.com"
        )

        # Should have both VM read and snapshot create
        has_vm_read = any(
            p.resource_type == ResourceType.VM and Action.READ in p.actions
            for p in all_permissions
        )
        has_snapshot_create = any(
            p.resource_type == ResourceType.SNAPSHOT and Action.CREATE in p.actions
            for p in all_permissions
        )

        assert has_vm_read is True
        assert has_snapshot_create is True


@pytest.mark.skip(reason="Requires PostgreSQL and Redis running")
class TestDatabaseOptimization:
    """
    Integration tests for database query optimization.

    Tests PERF-002 implementation.
    """

    @pytest.mark.asyncio
    async def test_query_caching(self, database_pool):
        """Test query result caching with Redis."""
        # Insert test data
        await database_pool.execute(
            "INSERT INTO test_vms (name, status, owner) VALUES ($1, $2, $3)",
            "test-vm-001",
            "running",
            "test@example.com",
        )

        # First query (cache miss)
        result1 = await database_pool.fetch(
            "SELECT * FROM test_vms WHERE status = $1",
            "running",
            use_cache=True,
        )

        assert len(result1) >= 1

        # Second query (cache hit)
        start_time = time.time()
        result2 = await database_pool.fetch(
            "SELECT * FROM test_vms WHERE status = $1",
            "running",
            use_cache=True,
        )
        cache_time = (time.time() - start_time) * 1000

        assert result1 == result2
        assert cache_time < 10    # Cache should be much faster

        # Verify cache hit in stats
        cache_stats = database_pool.cache.get_stats()
        assert cache_stats["cache_hits"] > 0

    @pytest.mark.asyncio
    async def test_async_operations(self, database_pool):
        """Test concurrent async database operations."""

        # Insert multiple VMs concurrently
        async def insert_vm(name: str) -> None:
            await database_pool.execute(
                "INSERT INTO test_vms (name, status, owner) VALUES ($1, $2, $3)",
                name,
                "running",
                "async@example.com",
            )

        # Run 10 inserts concurrently
        await asyncio.gather(*[insert_vm(f"async-vm-{i:03d}") for i in range(10)])

        # Verify all inserted
        result = await database_pool.fetch(
            "SELECT COUNT(*) as count FROM test_vms WHERE owner = $1",
            "async@example.com",
        )

        assert result[0]["count"] >= 10

    @pytest.mark.asyncio
    async def test_index_creation(self, database_pool):
        """Test automatic index creation."""
        # Create index on status column
        indexes = [
            IndexDefinition(
                table="test_vms",
                columns=["status"],
                index_type=IndexType.BTREE,
            ),
            IndexDefinition(
                table="test_vms",
                columns=["owner"],
                index_type=IndexType.BTREE,
            ),
        ]

        await database_pool.create_indexes(indexes)

        # Query should now use index (verify in query plan)
        _result = await database_pool.fetch(
            "SELECT * FROM test_vms WHERE status = $1",
            "running",
        )

        # Check query stats
        stats = database_pool.get_query_stats()
        assert stats["total_queries"] > 0

    @pytest.mark.asyncio
    async def test_query_metrics(self, database_pool):
        """Test query performance metrics collection."""
        # Execute several queries
        for i in range(5):
            await database_pool.fetch(
                "SELECT * FROM test_vms WHERE name = $1",
                f"test-vm-{i}",
            )

        # Get statistics
        stats = database_pool.get_query_stats()

        assert stats["total_queries"] >= 5
        assert stats["avg_execution_time_ms"] > 0
        assert stats["p50_ms"] >= 0
        assert stats["p95_ms"] >= 0
        assert stats["p99_ms"] >= 0


@pytest.mark.skip(reason="Requires Vault, PostgreSQL, and Redis running")
class TestEndToEndWorkflows:
    """
    End-to-end integration tests combining multiple services.

    Tests complete workflows across SECRET-001, RBAC-001, and PERF-002.
    """

    @pytest.mark.asyncio
    async def test_vm_creation_workflow(
        self,
        vault_client,
        role_manager,
        database_pool,
    ):
        """Test complete VM creation workflow with secrets and RBAC."""
        # Step 1: Store database credentials in Vault
        vault_client.create_secret(
            path="workflow/db/credentials",
            data={
                "username": "workflow_user",
                "password": "workflow_pass",
            },
        )

        # Step 2: Assign operator role
        principal_id = "workflow@example.com"
        role_manager.assign_role(principal_id, "operator")

        # Step 3: Check authorization for VM creation
        context = AuthorizationContext(
            principal_id=principal_id,
            principal_attributes={"department": "engineering"},
            resource_type=ResourceType.VM,
            resource_id="vm-workflow-001",
            resource_attributes={},
            action=Action.CREATE,
        )

        decision = role_manager.authorize(context)
        assert decision.allowed is True, "User should be authorized to create VM"

        # Step 4: Create VM in database
        await database_pool.execute(
            "INSERT INTO test_vms (name, status, owner, tags) VALUES ($1, $2, $3, $4)",
            "vm-workflow-001",
            "creating",
            principal_id,
            '{"environment": "test", "workflow": "integration"}',
        )

Step 5: Retrieve DB credentials from Vault
        db_creds = vault_client.read_secret("workflow/db/credentials")
        assert db_creds is not None
        assert db_creds["username"] == "workflow_user"

        # Step 6: Update VM status
        await database_pool.execute(
            "UPDATE test_vms SET status = $1 WHERE name = $2",
            "running",
            "vm-workflow-001",
        )

        # Step 7: Verify VM created successfully
        vm = await database_pool.fetchrow(
            "SELECT * FROM test_vms WHERE name = $1",
            "vm-workflow-001",
        )

        assert vm is not None
        assert vm["status"] == "running"
        assert vm["owner"] == principal_id

    @pytest.mark.asyncio
    async def test_secret_rotation_workflow(self, vault_client, database_pool):
        """Test secret rotation workflow with database update."""
        path = "workflow/rotation/api_key"

        # Create initial secret
        vault_client.create_secret(
            path=path,
            data={"api_key": "initial_key_v1"},
        )

        # Store reference in database
        await database_pool.execute(
            "INSERT INTO test_vms (name, status, tags) VALUES ($1, $2, $3)",
            "rotation-test",
            "running",
            '{"secret_path": "workflow/rotation/api_key", "secret_version": 1}',
        )

        # Rotate secret
        new_metadata = vault_client.rotate_secret(
            path=path,
            new_data={"api_key": "rotated_key_v2"},
        )

        # Update database with new version
        await database_pool.execute(
            "UPDATE test_vms SET tags = $1 WHERE name = $2",
            f'{{"secret_path": "{path}", "secret_version": {new_metadata.version}}}',
            "rotation-test",
        )

        # Verify workflow
        vm = await database_pool.fetchrow(
            "SELECT * FROM test_vms WHERE name = $1",
            "rotation-test",
        )

        import json

        tags = json.loads(vm["tags"])
        assert tags["secret_version"] == 2

        # Verify new secret
        secret = vault_client.read_secret(path)
        assert secret["api_key"] == "rotated_key_v2"

    def test_rbac_with_secrets(self, vault_client, role_manager):
        """Test RBAC authorization for secret access."""
        # Store sensitive secret
        vault_client.create_secret(
            path="workflow/sensitive/production_key",
            data={"key": "super_secret_production"},
            custom_metadata={"sensitivity": "high"},
        )

        # Check if user can access secrets
        context = AuthorizationContext(
            principal_id="user@example.com",
            principal_attributes={},
            resource_type=ResourceType.SECRET,
            resource_id="workflow/sensitive/production_key",
            resource_attributes={"sensitivity": "high"},
            action=Action.READ,
        )

        # Viewer role should NOT have secret access
        role_manager.assign_role("user@example.com", "viewer")
        decision = role_manager.authorize(context)

        # Note: This will fail because viewer doesn't have SECRET permissions
        # In production, you'd create specific secret roles
        assert decision.allowed is False, "Viewer should not access secrets"

        # Superadmin should have access
        role_manager.assign_role("admin@example.com", "superadmin")
        context.principal_id = "admin@example.com"
        decision = role_manager.authorize(context)
        assert decision.allowed is True, "Superadmin should access all secrets"


# Performance benchmarks


@pytest.mark.skip(reason="Requires PostgreSQL and Redis running")
class TestPerformanceBenchmarks:
    """Performance benchmarks for optimized components."""

    @pytest.mark.asyncio
    async def test_cache_performance(self, database_pool):
        """Benchmark query cache performance."""
        # Insert test data
        for i in range(100):
            await database_pool.execute(
                "INSERT INTO test_vms (name, status) VALUES ($1, $2)",
                f"bench-vm-{i}",
                "running",
            )

        query = "SELECT * FROM test_vms WHERE status = $1 LIMIT 50"

        # Uncached query
        start = time.time()
        await database_pool.fetch(query, "running", use_cache=False)
        uncached_time = (time.time() - start) * 1000

        # Cached query (first call)
        await database_pool.fetch(query, "running", use_cache=True)

        # Cached query (cache hit)
        start = time.time()
        await database_pool.fetch(query, "running", use_cache=True)
        cached_time = (time.time() - start) * 1000

        # Cache should be significantly faster
        speedup = uncached_time / cached_time if cached_time > 0 else 0
        print(
            f"Cache speedup: {speedup:.2f}x ({uncached_time:.2f}ms -> {cached_time:.2f}ms)"
        )

        assert cached_time < uncached_time, "Cache should be faster than DB query"
