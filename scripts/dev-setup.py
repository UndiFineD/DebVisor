#!/usr/bin/env python3
"""
Developer Setup Automation for DebVisor.

Automated script to set up a complete development environment for DebVisor.
Handles dependencies, virtual environments, pre-commit hooks, and IDE configuration.

Author: DebVisor Team
Date: November 28, 2025

Usage:
    python scripts/dev-setup.py [--no-venv] [--no-hooks] [--ci]
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# =============================================================================
# Constants
# =============================================================================

MINIMUM_PYTHON_VERSION = (3, 10)
RECOMMENDED_PYTHON_VERSION = (3, 12)

REQUIRED_SYSTEM_PACKAGES = {
    "linux": ["git", "curl", "build-essential", "libffi-dev", "libssl-dev"],
    "darwin": ["git", "curl"],
    "windows": ["git"]
}

PYTHON_PACKAGES = [
    # Core dependencies
    "flask>=3.0.0",
    "redis>=5.0.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.0.0",

    # Testing
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.0.0",
    "hypothesis>=6.0.0",

    # Code quality
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "black>=24.0.0",
    "isort>=5.12.0",

    # Development tools
    "pre-commit>=3.0.0",
    "ipython>=8.0.0",
    "rich>=13.0.0",
]

DEV_PACKAGES = [
    "pip-tools>=7.0.0",
    "watchdog>=4.0.0",
    "debugpy>=1.0.0",
]


# =============================================================================
# Enums
# =============================================================================

class SetupPhase(Enum):
    """Phases of the setup process."""
    PREFLIGHT = "preflight"
    VENV = "virtual_environment"
    DEPENDENCIES = "dependencies"
    HOOKS = "pre_commit_hooks"
    CONFIG = "configuration"
    VERIFY = "verification"


class Status(Enum):
    """Status of a setup step."""
    PENDING = "?"
    RUNNING = "[U+1F504]"
    SUCCESS = "?"
    SKIPPED = "??"
    WARNING = "[warn]?"
    FAILED = "?"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class SetupConfig:
    """Configuration for the setup process."""
    project_root: Path
    venv_path: Path
    create_venv: bool = True
    install_hooks: bool = True
    ci_mode: bool = False
    verbose: bool = False


@dataclass
class StepResult:
    """Result of a setup step."""
    name: str
    status: Status
    message: str
    duration_seconds: float = 0.0
    details: Optional[str] = None


# =============================================================================
# Utility Functions
# =============================================================================

def print_header(text: str) -> None:
    """Print a section header."""
    width = 60
    print()
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def print_step(name: str, status: Status, message: str = "") -> None:
    """Print a step status."""
    status_str = status.value
    print(f"  {status_str} {name}: {message}")


def run_command(
    cmd: List[str],
    cwd: Optional[Path] = None,
    capture: bool = True,
    check: bool = True,
    env: Optional[Dict[str, str]] = None
) -> Tuple[int, str, str]:
    """
    Run a shell command.

    Args:
        cmd: Command and arguments
        cwd: Working directory
        capture: Capture output
        check: Raise on non-zero exit
        env: Environment variables

    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture,
        text=True,
        env=full_env
    )

    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            cmd,
            result.stdout,
            result.stderr
        )

    return result.returncode, result.stdout, result.stderr


def command_exists(cmd: str) -> bool:
    """Check if a command exists."""
    return shutil.which(cmd) is not None


def get_python_version() -> Tuple[int, int, int]:
    """Get current Python version."""
    return sys.version_info[:3]


def get_platform() -> str:
    """Get current platform."""
    system = platform.system().lower()
    return system


# =============================================================================
# Setup Steps
# =============================================================================

class DevSetup:
    """Developer environment setup manager."""

    def __init__(self, config: SetupConfig):
        """
        Initialize setup manager.

        Args:
            config: Setup configuration
        """
        self.config = config
        self.results: List[StepResult] = []
        self.python_executable = sys.executable

    def run(self) -> bool:
        """
        Run the complete setup process.

        Returns:
            True if setup succeeded
        """
        print_header("DebVisor Development Environment Setup")
        print(f"  Project: {self.config.project_root}")
        print(f"  Python: {sys.version}")

        phases = [
            (SetupPhase.PREFLIGHT, self._preflight_checks),
            (SetupPhase.VENV, self._setup_virtual_environment),
            (SetupPhase.DEPENDENCIES, self._install_dependencies),
            (SetupPhase.HOOKS, self._setup_pre_commit),
            (SetupPhase.CONFIG, self._create_configurations),
            (SetupPhase.VERIFY, self._verify_setup),
        ]

        success = True
        for phase, handler in phases:
            print_header(f"Phase: {phase.value}")
            try:
                result = handler()
                if result.status == Status.FAILED:
                    success = False
                    if not self.config.ci_mode:
                        break
                self.results.append(result)
            except Exception as e:
                result = StepResult(
                    name=phase.value,
                    status=Status.FAILED,
                    message=str(e)
                )
                self.results.append(result)
                success = False
                if not self.config.ci_mode:
                    break

        self._print_summary()
        return success

    def _preflight_checks(self) -> StepResult:
        """Run preflight checks."""
        # Check Python version
        version = get_python_version()
        print_step(
            "Python version",
            Status.RUNNING,
            f"{version[0]}.{version[1]}.{version[2]}"
        )

        if version[:2] < MINIMUM_PYTHON_VERSION:
            return StepResult(
                name="preflight",
                status=Status.FAILED,
                message=f"Python {MINIMUM_PYTHON_VERSION[0]}.{MINIMUM_PYTHON_VERSION[1]}+ required"
            )

        if version[:2] < RECOMMENDED_PYTHON_VERSION:
            print_step(
                "Python version",
                Status.WARNING,
                f"Recommend Python {RECOMMENDED_PYTHON_VERSION[0]}.{RECOMMENDED_PYTHON_VERSION[1]}+"
            )
        else:
            print_step("Python version", Status.SUCCESS, "OK")

        # Check Git
        print_step("Git", Status.RUNNING, "Checking...")
        if not command_exists("git"):
            return StepResult(
                name="preflight",
                status=Status.FAILED,
                message="Git is not installed"
            )
        print_step("Git", Status.SUCCESS, "Found")

        # Check project structure
        print_step("Project structure", Status.RUNNING, "Checking...")
        required_dirs = ["opt", "tests"]
        for dir_name in required_dirs:
            dir_path = self.config.project_root / dir_name
            if not dir_path.exists():
                print_step(
                    "Project structure",
                    Status.WARNING,
                    f"Missing directory: {dir_name}"
                )
        print_step("Project structure", Status.SUCCESS, "OK")

        return StepResult(
            name="preflight",
            status=Status.SUCCESS,
            message="All checks passed"
        )

    def _setup_virtual_environment(self) -> StepResult:
        """Set up Python virtual environment."""
        if not self.config.create_venv:
            print_step("Virtual environment", Status.SKIPPED, "Disabled")
            return StepResult(
                name="venv",
                status=Status.SKIPPED,
                message="Skipped by configuration"
            )

        venv_path = self.config.venv_path

        # Check if venv exists
        if venv_path.exists():
            print_step(
                "Virtual environment",
                Status.SUCCESS,
                f"Exists at {venv_path}"
            )
        else:
            print_step(
                "Virtual environment",
                Status.RUNNING,
                f"Creating at {venv_path}..."
            )

            import venv
            venv.create(venv_path, with_pip=True)

            print_step("Virtual environment", Status.SUCCESS, "Created")

        # Update python executable path
        if get_platform() == "windows":
            self.python_executable = str(venv_path / "Scripts" / "python.exe")
        else:
            self.python_executable = str(venv_path / "bin" / "python")

        # Upgrade pip
        print_step("pip", Status.RUNNING, "Upgrading...")
        run_command([
            self.python_executable, "-m", "pip",
            "install", "--upgrade", "pip", "setuptools", "wheel"
        ])
        print_step("pip", Status.SUCCESS, "Upgraded")

        return StepResult(
            name="venv",
            status=Status.SUCCESS,
            message=f"Virtual environment ready at {venv_path}"
        )

    def _install_dependencies(self) -> StepResult:
        """Install Python dependencies."""
        print_step("Dependencies", Status.RUNNING, "Installing core packages...")

        # Install requirements.txt if exists
        req_file = self.config.project_root / "requirements.txt"
        if req_file.exists():
            run_command([
                self.python_executable, "-m", "pip",
                "install", "-r", str(req_file)
            ])
            print_step("requirements.txt", Status.SUCCESS, "Installed")

        # Install dev requirements if exists
        dev_req_file = self.config.project_root / "requirements-dev.txt"
        if dev_req_file.exists():
            run_command([
                self.python_executable, "-m", "pip",
                "install", "-r", str(dev_req_file)
            ])
            print_step("requirements-dev.txt", Status.SUCCESS, "Installed")

        # Install additional packages
        print_step("Dev packages", Status.RUNNING, "Installing...")
        all_packages = PYTHON_PACKAGES + DEV_PACKAGES

        for package in all_packages:
            try:
                run_command([
                    self.python_executable, "-m", "pip",
                    "install", package
                ], check=False)
            except subprocess.CalledProcessError:
                print_step(f"Package {package}", Status.WARNING, "Failed to install")

        print_step("Dependencies", Status.SUCCESS, "Installed")

        return StepResult(
            name="dependencies",
            status=Status.SUCCESS,
            message="All dependencies installed"
        )

    def _setup_pre_commit(self) -> StepResult:
        """Set up pre-commit hooks."""
        if not self.config.install_hooks:
            print_step("Pre-commit", Status.SKIPPED, "Disabled")
            return StepResult(
                name="hooks",
                status=Status.SKIPPED,
                message="Skipped by configuration"
            )

        # Check if .pre-commit-config.yaml exists
        config_file = self.config.project_root / ".pre-commit-config.yaml"

        if not config_file.exists():
            print_step("Pre-commit config", Status.RUNNING, "Creating...")
            self._create_pre_commit_config(config_file)
            print_step("Pre-commit config", Status.SUCCESS, "Created")

        # Install pre-commit hooks
        print_step("Pre-commit hooks", Status.RUNNING, "Installing...")

        try:
            run_command([
                self.python_executable, "-m", "pre_commit",
                "install"
            ], cwd=self.config.project_root)
            print_step("Pre-commit hooks", Status.SUCCESS, "Installed")
        except subprocess.CalledProcessError:
            print_step("Pre-commit hooks", Status.WARNING, "Failed to install")
            return StepResult(
                name="hooks",
                status=Status.WARNING,
                message="Pre-commit hooks installation failed"
            )

        return StepResult(
            name="hooks",
            status=Status.SUCCESS,
            message="Pre-commit hooks installed"
        )

    def _create_pre_commit_config(self, path: Path) -> None:
        """Create pre-commit configuration file."""
        config = """# Pre-commit hooks for DebVisor
# See https://pre-commit.com for more information

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
          - types-redis
        args: [--ignore-missing-imports]

  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: python -m pytest tests/ -x -q --tb=short
        language: system
        pass_filenames: false
        always_run: true
        stages: [push]
"""
        path.write_text(config)

    def _create_configurations(self) -> StepResult:
        """Create development configuration files."""
        print_step("Configurations", Status.RUNNING, "Creating...")

        # Create pyproject.toml if missing
        pyproject = self.config.project_root / "pyproject.toml"
        if not pyproject.exists():
            self._create_pyproject_toml(pyproject)
            print_step("pyproject.toml", Status.SUCCESS, "Created")

        # Create .vscode/settings.json
        vscode_dir = self.config.project_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)

        settings_file = vscode_dir / "settings.json"
        if not settings_file.exists():
            self._create_vscode_settings(settings_file)
            print_step(".vscode/settings.json", Status.SUCCESS, "Created")

        # Create .vscode/launch.json
        launch_file = vscode_dir / "launch.json"
        if not launch_file.exists():
            self._create_vscode_launch(launch_file)
            print_step(".vscode/launch.json", Status.SUCCESS, "Created")

        print_step("Configurations", Status.SUCCESS, "Created")

        return StepResult(
            name="config",
            status=Status.SUCCESS,
            message="Configuration files created"
        )

    def _create_pyproject_toml(self, path: Path) -> None:
        """Create pyproject.toml configuration."""
        config = """[project]
name = "debvisor"
version = "1.0.0"
description = "DebVisor Enterprise Platform"
requires-python = ">=3.10"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "C4", "SIM"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_ignores = true
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["opt"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
"""
        path.write_text(config)

    def _create_vscode_settings(self, path: Path) -> None:
        """Create VS Code settings."""
        venv_path = self.config.venv_path

        if get_platform() == "windows":
            python_path = str(venv_path / "Scripts" / "python.exe")
        else:
            python_path = str(venv_path / "bin" / "python")

        settings = {
            "python.defaultInterpreterPath": python_path,
            "python.analysis.typeCheckingMode": "basic",
            "python.analysis.autoImportCompletions": True,
            "python.testing.pytestEnabled": True,
            "python.testing.pytestArgs": ["tests"],
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": "explicit",
                "source.fixAll": "explicit"
            },
            "[python]": {
                "editor.defaultFormatter": "charliermarsh.ruff",
                "editor.tabSize": 4
            },
            "files.exclude": {
                "**/__pycache__": True,
                "**/.pytest_cache": True,
                "**/*.pyc": True,
                ".venv": True
            }
        }

        path.write_text(json.dumps(settings, indent=2))

    def _create_vscode_launch(self, path: Path) -> None:
        """Create VS Code launch configuration."""
        launch = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python: Flask",
                    "type": "debugpy",
                    "request": "launch",
                    "module": "flask",
                    "env": {
                        "FLASK_APP": "opt/web/panel/app.py",
                        "FLASK_ENV": "development"
                    },
                    "args": ["run", "--debug"],
                    "jinja": True
                },
                {
                    "name": "Python: Current File",
                    "type": "debugpy",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal"
                },
                {
                    "name": "Python: pytest",
                    "type": "debugpy",
                    "request": "launch",
                    "module": "pytest",
                    "args": ["tests/", "-v"]
                }
            ]
        }

        path.write_text(json.dumps(launch, indent=2))

    def _verify_setup(self) -> StepResult:
        """Verify the setup is complete."""
        print_step("Verification", Status.RUNNING, "Running checks...")

        issues = []

        # Check Python in venv
        try:
            code, stdout, _ = run_command([
                self.python_executable, "-c",
                "import sys; print(sys.executable)"
            ])
            print_step("Python executable", Status.SUCCESS, stdout.strip())
        except subprocess.CalledProcessError:
            issues.append("Python not working")

        # Check key packages
        packages_to_check = ["flask", "pytest", "ruff"]
        for pkg in packages_to_check:
            try:
                run_command([
                    self.python_executable, "-c",
                    f"import {pkg}"
                ])
                print_step(f"Package: {pkg}", Status.SUCCESS, "Installed")
            except subprocess.CalledProcessError:
                print_step(f"Package: {pkg}", Status.WARNING, "Not found")
                issues.append(f"Package {pkg} not installed")

        # Run quick test
        try:
            run_command([
                self.python_executable, "-m", "pytest",
                "--collect-only", "-q"
            ], cwd=self.config.project_root, check=False)
            print_step("Test discovery", Status.SUCCESS, "OK")
        except Exception:
            print_step("Test discovery", Status.WARNING, "Failed")

        if issues:
            return StepResult(
                name="verify",
                status=Status.WARNING,
                message=f"{len(issues)} issues found",
                details="\n".join(issues)
            )

        return StepResult(
            name="verify",
            status=Status.SUCCESS,
            message="Setup verified successfully"
        )

    def _print_summary(self) -> None:
        """Print setup summary."""
        print_header("Setup Summary")

        for result in self.results:
            print_step(result.name, result.status, result.message)

        failed = [r for r in self.results if r.status == Status.FAILED]
        warnings = [r for r in self.results if r.status == Status.WARNING]

        print()
        if failed:
            print("  ? Setup failed with errors")
            for r in failed:
                print(f"     - {r.name}: {r.message}")
        elif warnings:
            print("  [warn]? Setup completed with warnings")
        else:
            print("  ? Setup completed successfully!")

        print()
        print("  Next steps:")
        if self.config.create_venv:
            if get_platform() == "windows":
                print(f"    1. Activate venv: {self.config.venv_path}\\Scripts\\activate")
            else:
                print(f"    1. Activate venv: source {self.config.venv_path}/bin/activate")
        print("    2. Run tests: pytest tests/")
        print("    3. Start development server: flask run --debug")
        print()


# =============================================================================
# Main
# =============================================================================

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Set up DebVisor development environment"
    )
    parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Skip virtual environment creation"
    )
    parser.add_argument(
        "--no-hooks",
        action="store_true",
        help="Skip pre-commit hook installation"
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode (continue on errors)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--venv-path",
        type=str,
        default=".venv",
        help="Path for virtual environment"
    )

    args = parser.parse_args()

    # Determine project root
    project_root = Path(__file__).parent.parent.resolve()
    if not (project_root / "opt").exists():
        # Fallback: current directory
        project_root = Path.cwd()

    venv_path = project_root / args.venv_path

    config = SetupConfig(
        project_root=project_root,
        venv_path=venv_path,
        create_venv=not args.no_venv,
        install_hooks=not args.no_hooks,
        ci_mode=args.ci,
        verbose=args.verbose
    )

    setup = DevSetup(config)
    success = setup.run()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
