# Contributing to DebVisor

Thank you for your interest in contributing to DebVisor! This document provides guidelines and information for contributors.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
1. [Getting Started](#getting-started)
1. [Development Setup](#development-setup)
1. [Code Style Guidelines](#code-style-guidelines)
1. [Testing Requirements](#testing-requirements)
1. [Pull Request Process](#pull-request-process)
1. [Documentation Standards](#documentation-standards)
1. [Security Considerations](#security-considerations)

---

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be respectful**: Treat all contributors with respect and professionalism
- **Be inclusive**: Welcome contributions from everyone, regardless of background
- **Be constructive**: Provide helpful feedback and be open to receiving it
- **Be patient**: Remember that contributors have varying levels of experience

---

## Getting Started

### Prerequisites

- Python 3.10+ (3.12 recommended)
- Git
- Docker and Docker Compose (for testing)
- Linux environment (native or WSL2 for Windows)

### Quick Start

```bash

# Clone the repository
git clone https://github.com/your-org/debvisor.git
cd debvisor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# or
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```text

---

## Development Setup

### Python Environment

```bash

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```text

### IDE Configuration

**VS Code** (Recommended):

```json
// .vscode/settings.json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter"
    }
}
```text

### Environment Variables

Create a `.env` file for local development:

```bash

# .env
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///dev.db
SECRET_KEY=dev-secret-key-change-in-production
DEBVISOR_SIGNING_KEY=test-signing-key
LOG_LEVEL=DEBUG
```text

---

## Code Style Guidelines

### Python Code Style

We follow [PEP 8](https://pep8.org/) with the following specifics:

1. **Formatter**: Black with line length 88
1. **Import sorting**: isort with Black compatibility
1. **Type hints**: Required for all public functions
1. **Docstrings**: Google-style docstrings for all public APIs

```python

# Good example
from typing import Optional, List, Dict, Any

def process_nodes(
    node_ids: List[str],
    options: Optional[Dict[str, Any]] = None,
    timeout: float = 30.0
) -> Dict[str, bool]:
    """
    Process a list of nodes with the given options.

    Args:
        node_ids: List of node identifiers to process
        options: Optional processing options
        timeout: Operation timeout in seconds

    Returns:
        Dictionary mapping node_id to success status

    Raises:
        TimeoutError: If operation exceeds timeout
        NodeNotFoundError: If a node_id is invalid

    Example:
        >>> results = process_nodes(["node-1", "node-2"])
        >>> print(results)
        {'node-1': True, 'node-2': True}
    """
    # Implementation
    pass
```text

### File Organization

```text
opt/
+-- services/          # Business logic services
|   +-- __init__.py
|   +-- backup_manager.py
|   +-- resilience.py
+-- web/
|   +-- panel/         # Web application
|       +-- app.py
|       +-- routes/
|       +-- templates/
+-- core/              # Core utilities
    +-- unified_backend.py
```text

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Modules | lowercase_underscore | `backup_manager.py` |
| Classes | PascalCase | `BackupManager` |
| Functions | lowercase_underscore | `create_backup()` |
| Constants | UPPERCASE | `MAX_RETRIES` |
| Private | Leading underscore | `_internal_helper()` |

---

## Testing Requirements

### Test Structure

```text
tests/
+-- conftest.py           # Shared fixtures
+-- test_backup_service.py
+-- test_cache.py
+-- benchmarks/           # Performance tests
|   +-- test_performance.py
+-- integration/          # Integration tests
    +-- test_api.py
```text

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch

class TestBackupManager:
    """Tests for BackupManager class."""

    @pytest.fixture
    def manager(self):
        """Create BackupManager instance."""
        return BackupManager(config=test_config)

    def test_create_backup_success(self, manager):
        """Test successful backup creation."""
        # Arrange
        mock_storage = Mock()

        # Act
        result = manager.create_backup("test-vm", storage=mock_storage)

        # Assert
        assert result.success is True
        assert result.backup_id is not None
        mock_storage.write.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_backup(self, manager):
        """Test async backup operation."""
        result = await manager.create_backup_async("test-vm")
        assert result.success is True
```text

### Test Coverage Requirements

- **Minimum coverage**: 80% for new code
- **Critical paths**: 95% for security and data handling
- Run coverage report: `pytest --cov=opt --cov-report=html`

### Running Tests

```bash

# Run all tests
pytest

# Run with coverage
pytest --cov=opt --cov-report=term-missing

# Run specific test file
pytest tests/test_backup_service.py

# Run tests matching pattern
pytest -k "backup"

# Run with verbose output
pytest -v

# Run only fast tests (skip integration)
pytest -m "not integration"
```text

---

## Pull Request Process

### Before Submitting

1. **Create an issue** describing the change (for non-trivial changes)
1. **Fork the repository** and create a feature branch
1. **Write tests** for new functionality
1. **Update documentation** if needed
1. **Run the full test suite** locally

### Branch Naming

```text
feature/add-backup-encryption
bugfix/fix-cache-invalidation
docs/update-api-documentation
refactor/improve-error-handling
```text

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
feat(backup): add AES-256 encryption support

- Add encryption option to BackupConfig
- Implement encrypt_stream() and decrypt_stream()
- Add tests for encryption roundtrip

Closes #123
```text

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### PR Template

```markdown

## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass locally
- [ ] Integration tests pass locally
- [ ] New tests added for changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-reviewed the code
- [ ] Added necessary documentation
- [ ] No new warnings generated

```text

### Review Process

1. **Automated checks**: CI must pass (lint, tests, security scan)
1. **Code review**: At least one maintainer approval required
1. **Documentation review**: For public API changes
1. **Merge**: Squash merge to main branch

---

## Documentation Standards

### Code Documentation

```python
class CacheManager:
    """
    Manages multi-tier caching for DebVisor services.

    This class provides a unified interface for L1 (in-memory) and
    L2 (Redis) caching with automatic fallback and invalidation.

    Attributes:
        l1_cache: In-memory LRU cache
        l2_cache: Redis-backed distributed cache
        metrics: Cache performance metrics

    Example:
        >>> manager = CacheManager(redis_url="redis://localhost:6379")
        >>> await manager.set("key", {"data": "value"}, ttl=3600)
        >>> value = await manager.get("key")
    """
```text

### Markdown Documentation

- Use clear headings and structure
- Include code examples
- Keep line length under 100 characters
- Use relative links for internal references

### API Documentation

- All public endpoints must have OpenAPI documentation
- Include request/response examples
- Document error codes and conditions

---

## Security Considerations

### Sensitive Data

- **Never** commit secrets, keys, or credentials
- Use environment variables for configuration
- Mark sensitive fields in logs: `logger.info("User %s authenticated", user.id)`

### Security Review

Changes touching these areas require security review:

- Authentication/authorization
- Cryptographic operations
- User input handling
- Network communication
- File system operations

### Reporting Vulnerabilities

For security vulnerabilities, please email: <security@debvisor.io>

Do not open public issues for security concerns.

---

## Questions?

- **General questions**: Open a Discussion
- **Bug reports**: Open an Issue
- **Feature requests**: Open an Issue with `[Feature]` prefix
- **Security issues**: Email <security@debvisor.io>

Thank you for contributing to DebVisor! [U+1F389]
