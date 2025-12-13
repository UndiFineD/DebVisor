# Code Issues Report: tests\test_integration_suite.py
Generated: 2025-12-13T14:42:57.898403
Source: tests\test_integration_suite.py

## Issues Summary
Total: 41 issues found

| Line | Column | Tool | Code | Severity | Message |
|------|--------|------|------|----------|---------|
| 53 | 0 | bandit | `B106` | LOW | Possible hardcoded password: 'dev-only-token' |
| 134 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 135 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 139 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 140 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 141 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 159 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 163 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 167 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 180 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 181 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 210 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 211 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 218 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 219 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 274 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 279 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 331 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 332 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 363 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 374 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 375 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 379 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 403 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 432 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 447 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 448 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 449 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 450 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 451 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 496 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 509 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 510 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 525 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 526 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 527 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 570 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 574 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 601 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 607 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| 654 | 0 | bandit | `B101` | LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## Implementation Status
Items marked below as fixed:


## Fix Proposals

**41 issues to fix:**


### Issue at Line 53

**Tool:** bandit | **Code:** `B106` | **Severity:** LOW

**Message:** Possible hardcoded password: 'dev-only-token'

**Context:**
```
@pytest.fixture(scope="function")
async def vault_client() -> None:  # type: ignore[misc]
    """Initialize Vault client for testing."""
    config = VaultConfig(
        _url = "http://127.0.0.1:8200",
        _auth_method = AuthMethod.TOKEN,
        _token = "dev-only-token",
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 134

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
            },
        )

        assert metadata.version == 1
        assert metadata.path == "integration/test/db_password"

        # Read secret
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 135

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        )

        assert metadata.version == 1
        assert metadata.path == "integration/test/db_password"

        # Read secret
        secret = vault_client.read_secret("integration/test/db_password")
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 139

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        # Read secret
        secret = vault_client.read_secret("integration/test/db_password")
        assert secret is not None
        assert secret["username"] == "testuser"
        assert secret["password"] == "secret123"

```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 140

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        # Read secret
        secret = vault_client.read_secret("integration/test/db_password")
        assert secret is not None
        assert secret["username"] == "testuser"
        assert secret["password"] == "secret123"

    def test_secret_rotation(self, vault_client):
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 141

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        secret = vault_client.read_secret("integration/test/db_password")
        assert secret is not None
        assert secret["username"] == "testuser"
        assert secret["password"] == "secret123"

    def test_secret_rotation(self, vault_client):
        """Test secret rotation workflow."""
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 159

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
            _new_data = {"api_key": "rotated_key"},
        )

        assert new_metadata.version == 2

        # Read new version
        secret = vault_client.read_secret(path)
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 163

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        # Read new version
        secret = vault_client.read_secret(path)
        assert secret["api_key"] == "rotated_key"

        # Read old version
        old_secret = vault_client.read_secret(path, version=1)
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 167

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        # Read old version
        old_secret = vault_client.read_secret(path, version=1)
        assert old_secret["api_key"] == "initial_key"

    def test_secret_listing(self, vault_client):
        """Test listing secrets in a path."""
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 180

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        # List secrets
        secrets = vault_client.list_secrets("integration/test/list")
        assert len(secrets) >= 3
        assert any("secret_0" in s for s in secrets)


```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 181

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        # List secrets
        secrets = vault_client.list_secrets("integration/test/list")
        assert len(secrets) >= 3
        assert any("secret_0" in s for s in secrets)


@pytest.mark.skip(reason="Requires Vault and RBAC services running")
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 210

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        )

        decision = role_manager.authorize(context)
        assert decision.allowed is True
        assert len(decision.matched_permissions) > 0

        # Test user management permission (should be denied)
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 211

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        decision = role_manager.authorize(context)
        assert decision.allowed is True
        assert len(decision.matched_permissions) > 0

        # Test user management permission (should be denied)
        context.resource_type = ResourceType.USER
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 218

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        context.action = Action.DELETE

        decision = role_manager.authorize(context)
        assert decision.allowed is False
        assert len(decision.matched_permissions) == 0

    def test_conditional_permissions(self, role_manager):
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 219

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        decision = role_manager.authorize(context)
        assert decision.allowed is False
        assert len(decision.matched_permissions) == 0

    def test_conditional_permissions(self, role_manager):
        """Test time-based and IP-based conditional permissions."""
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 274

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        )

        decision = role_manager.authorize(context)
        assert decision.allowed is True

        # Test from external IP (should be denied)
        context.client_ip = "8.8.8.8"
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 279

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        # Test from external IP (should be denied)
        context.client_ip = "8.8.8.8"
        decision = role_manager.authorize(context)
        assert decision.allowed is False

    def test_permission_inheritance(self, role_manager):
        """Test role hierarchy and permission inheritance."""
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 331

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
            for p in all_permissions
        )

        assert has_vm_read is True
        assert has_snapshot_create is True


```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 332

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        )

        assert has_vm_read is True
        assert has_snapshot_create is True


@pytest.mark.skip(reason="Requires PostgreSQL and Redis running")
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 363

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
            _use_cache = True,
        )

        assert len(result1) >= 1

        # Second query (cache hit)
        start_time = time.time()
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 374

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        )
        cache_time = (time.time() - start_time) * 1000

        assert result1 == result2
        assert cache_time < 10    # Cache should be much faster

        # Verify cache hit in stats
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 375

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        cache_time = (time.time() - start_time) * 1000

        assert result1 == result2
        assert cache_time < 10    # Cache should be much faster

        # Verify cache hit in stats
        cache_stats = database_pool.cache.get_stats()
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 379

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        # Verify cache hit in stats
        cache_stats = database_pool.cache.get_stats()
        assert cache_stats["cache_hits"] > 0

    @pytest.mark.asyncio
    async def test_async_operations(self, database_pool):
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 403

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
            "async@example.com",
        )

        assert result[0]["count"] >= 10

    @pytest.mark.asyncio
    async def test_index_creation(self, database_pool):
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 432

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        # Check query stats
        stats = database_pool.get_query_stats()
        assert stats["total_queries"] > 0

    @pytest.mark.asyncio
    async def test_query_metrics(self, database_pool):
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 447

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        # Get statistics
        stats = database_pool.get_query_stats()

        assert stats["total_queries"] >= 5
        assert stats["avg_execution_time_ms"] > 0
        assert stats["p50_ms"] >= 0
        assert stats["p95_ms"] >= 0
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 448

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        stats = database_pool.get_query_stats()

        assert stats["total_queries"] >= 5
        assert stats["avg_execution_time_ms"] > 0
        assert stats["p50_ms"] >= 0
        assert stats["p95_ms"] >= 0
        assert stats["p99_ms"] >= 0
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 449

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        assert stats["total_queries"] >= 5
        assert stats["avg_execution_time_ms"] > 0
        assert stats["p50_ms"] >= 0
        assert stats["p95_ms"] >= 0
        assert stats["p99_ms"] >= 0

```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 450

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        assert stats["total_queries"] >= 5
        assert stats["avg_execution_time_ms"] > 0
        assert stats["p50_ms"] >= 0
        assert stats["p95_ms"] >= 0
        assert stats["p99_ms"] >= 0


```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 451

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        assert stats["avg_execution_time_ms"] > 0
        assert stats["p50_ms"] >= 0
        assert stats["p95_ms"] >= 0
        assert stats["p99_ms"] >= 0


@pytest.mark.skip(reason="Requires Vault, PostgreSQL, and Redis running")
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 496

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        )

        decision = role_manager.authorize(context)
        assert decision.allowed is True, "User should be authorized to create VM"

        # Step 4: Create VM in database
        await database_pool.execute(
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 509

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        # Step 5: Retrieve DB credentials from Vault
        db_creds = vault_client.read_secret("workflow/db/credentials")
        assert db_creds is not None
        assert db_creds["username"] == "workflow_user"

        # Step 6: Update VM status
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 510

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        # Step 5: Retrieve DB credentials from Vault
        db_creds = vault_client.read_secret("workflow/db/credentials")
        assert db_creds is not None
        assert db_creds["username"] == "workflow_user"

        # Step 6: Update VM status
        await database_pool.execute(
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 525

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
            "vm-workflow-001",
        )

        assert vm is not None
        assert vm["status"] == "running"
        assert vm["owner"] == principal_id

```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 526

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        )

        assert vm is not None
        assert vm["status"] == "running"
        assert vm["owner"] == principal_id

    @pytest.mark.asyncio
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 527

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        assert vm is not None
        assert vm["status"] == "running"
        assert vm["owner"] == principal_id

    @pytest.mark.asyncio
    async def test_secret_rotation_workflow(self, vault_client, database_pool):
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 570

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        import json

        tags = json.loads(vm["tags"])
        assert tags["secret_version"] == 2

        # Verify new secret
        secret = vault_client.read_secret(path)
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 574

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        # Verify new secret
        secret = vault_client.read_secret(path)
        assert secret["api_key"] == "rotated_key_v2"

    def test_rbac_with_secrets(self, vault_client, role_manager):
        """Test RBAC authorization for secret access."""
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 601

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```

        # Note: This will fail because viewer doesn't have SECRET permissions
        # In production, you'd create specific secret roles
        assert decision.allowed is False, "Viewer should not access secrets"

        # Superadmin should have access
        role_manager.assign_role("admin@example.com", "superadmin")
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 607

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        role_manager.assign_role("admin@example.com", "superadmin")
        context.principal_id = "admin@example.com"
        decision = role_manager.authorize(context)
        assert decision.allowed is True, "Superadmin should access all secrets"


# Performance benchmarks
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

### Issue at Line 654

**Tool:** bandit | **Code:** `B101` | **Severity:** LOW

**Message:** Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

**Context:**
```
        # Only enforce timing comparison if uncached time is above minimum threshold
        # to avoid flaky failures on fast hardware or CI variance
        if uncached_time >= MIN_TIMING_THRESHOLD_MS:
            assert (
                cached_time <= uncached_time * CACHE_TIMING_TOLERANCE
            ), f"Cache should be faster: {cached_time:.2f}ms <= {uncached_time * CACHE_TIMING_TOLERANCE:.2f}ms"
        else:
```

**Proposal:**
- Review the issue message above
- Consider the context code
- Apply the appropriate fix (e.g., fix linting error, add type hints, improve security)
- Ensure the fix aligns with the codebase style and the context.md guidelines

---

## Implementation Progress

To mark an issue as fixed, add the issue code to the line below with a ✅ emoji:

**Fixed Issues:** (none yet)

---
*Updated: (auto-populated by coding expert)*
