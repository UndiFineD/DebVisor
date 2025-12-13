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
opt/config/validate-packages.py - Validate package availability in Debian repositories

Purpose: Verify all packages in .list.chroot files are available in target distribution
and architecture before building the ISO.

Usage:
    python3 validate-packages.py --dist bookworm --arch amd64
    python3 validate-packages.py --dist trixie --arch arm64 --verbose
    python3 validate-packages.py --dist trixie --arch amd64 --json > packages.json
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any


class PackageValidator:
    """Validate Debian packages against repository."""

    # Debian suite mappings for architecture support
    DEBIAN_SUITES={
        "bookworm": "stable",
        "trixie": "testing",
        "sid": "unstable",
        "bookworm-backports": "backports",
    }

    SUPPORTED_ARCHS={"amd64", "arm64", "i386", "armh", "ppc64el", "s390x"}

    def __init__(self, dist: str, arch: str, verbose: bool=False) -> None:
        """Initialize validator.

        Args:
            dist: Debian distribution (bookworm, trixie, sid)
            arch: Architecture (amd64, arm64, i386, armhf, ppc64el, s390x)
            verbose: Enable verbose output
        """
        self.dist=dist
        self.arch=arch
        self.verbose=verbose
        self.packages: Dict[str, Dict[str, Any]] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.missing_packages: Set[str] = set()
        self.conditional_packages: Set[str] = set()

    def parse_package_lists(self) -> List[Path]:
        """Parse all .list.chroot files in current directory.

        Returns:
            List of Path objects for .list.chroot files
        """
        _config_dir=Path(".")
        _list_files=list(config_dir.glob("*.list.chroot"))  # type: ignore[name-defined]

        if not list_files:  # type: ignore[name-defined]
            self.errors.append("No .list.chroot files found in current directory")
            return []

        if self.verbose:
            print(f"Found {len(list_files)} package list files:")  # type: ignore[name-defined]
            for f in sorted(list_files):  # type: ignore[name-defined]
                print(f"  - {f.name}")

        return sorted(list_files)  # type: ignore[name-defined]

    def load_packages(self, listfiles: List[Path]) -> Set[str]:
        """Load all packages from list files.

        Args:
            list_files: List of .list.chroot file paths

        Returns:
            Set of unique package names
        """
        _packages=set()  # type: ignore[var-annotated]

        for list_file in list_files:  # type: ignore[name-defined]
            try:
                with open(list_file, "r") as f:
                    for line in f:
                        _line=line.strip()
                        # Skip comments and empty lines
                        if not line or line.startswith("    #"):
                            continue
                        # Extract package name (may have conditions like 'package !i386')
                        _pkg_name=re.split(r"\s+", line)[0]
                        if pkg_name:  # type: ignore[name-defined]
                            packages.add(pkg_name)  # type: ignore[name-defined]
                            if self.verbose:
                                print(f"  Loaded: {pkg_name} (from {list_file.name})")  # type: ignore[name-defined]
            except Exception as e:
                self.errors.append(f"Error reading {list_file.name}: {e}")

        return packages  # type: ignore[name-defined]

    def validate_architecture(self) -> bool:
        """Validate that architecture is supported.

        Returns:
            True if architecture is valid
        """
        if self.arch not in self.SUPPORTED_ARCHS:
            self.errors.append(
                f"Architecture '{self.arch}' not supported. "
                f"Choose from: {', '.join(sorted(self.SUPPORTED_ARCHS))}"
            )
            return False
        return True

    def validate_distribution(self) -> bool:
        """Validate that distribution is supported.

        Returns:
            True if distribution is valid
        """
        if self.dist not in self.DEBIAN_SUITES:
            self.errors.append(
                f"Distribution '{self.dist}' not recognized. "
                f"Choose from: {', '.join(sorted(self.DEBIAN_SUITES.keys()))}"
            )
            return False
        return True

    def check_package_in_apt(self, package: str) -> Tuple[bool, str]:
        """Check if package exists in APT cache for distribution/arch.

        This checks the local apt cache first, then queries apt-cache.

        Args:
            package: Package name to check

        Returns:
            Tuple of (exists: bool, status: str)
        """
        try:
        # Use apt-cache to check availability
            # This works if apt is available and cache is up to date
            result=subprocess.run(  # type: ignore[call-overload]
                ["apt-cache", "policy", package],
                _capture_output=True,
                _text=True,
                _timeout=10,
            )    # nosec B603, B607

            if result.returncode != 0:
                return False, "apt-cache error"

            # Check if package appears in policy output
            if f"{package}:" in result.stdout or f"{package} " in result.stdout:
            # Parse policy output to check architecture availability
                if self.arch in result.stdout or "all" in result.stdout:
                    return True, "available"
                else:
                    return False, f"not available for {self.arch}"
            else:
                return False, "not found in cache"

        except FileNotFoundError:
            return False, "apt-cache not available"
        except subprocess.TimeoutExpired:
            return False, "apt-cache timeout"
        except Exception as e:
            return False, f"error: {e}"

    def validate_packages(self, packages: Set[str]) -> Dict[str, List[str]]:
        """Validate all packages.

        Args:
            packages: Set of package names to validate

        Returns:
            Dictionary with results organized by status
        """
        results: Dict[str, List[str]] = {
            "available": [],
            "missing": [],
            "conditional": [],
            "optional": [],
            "unknown": [],
        }

        _total=len(packages)
        print(f"\nValidating {total} packages for {self.dist}/{self.arch}...")  # type: ignore[name-defined]

        for i, pkg in enumerate(sorted(packages), 1):
            _status=f"({i}/{total})"  # type: ignore[name-defined]

            # Check for conditional packages (e.g., architecture-specific)
            if re.search(r"[!]", pkg) or re.search(r"[amd64|arm64|i386]", pkg):
                results["conditional"].append(pkg)
                print(f"  [warn]?  {pkg} {status} (architecture-conditional)")  # type: ignore[name-defined]
                continue

            # Check for optional profile-specific packages
            if self._is_optional_package(pkg):
                results["optional"].append(pkg)
                if self.verbose:
                    print(f"  ??  {pkg} {status} (profile-specific)")  # type: ignore[name-defined]
                continue

            # Check availability
            exists, msg=self.check_package_in_apt(pkg)

            if exists:
                results["available"].append(pkg)
                if self.verbose:
                    print(f"  ? {pkg} {status} - {msg}")  # type: ignore[name-defined]
            else:
                results["missing"].append(pkg)
                print(f"  ? {pkg} {status} - {msg}")  # type: ignore[name-defined]
                self.errors.append(f"Package not found: {pkg}")

        return results

    def _is_optional_package(self, pkg: str) -> bool:
        """Check if package is optional/conditional.

        Args:
            pkg: Package name

        Returns:
            True if package is conditional/optional
        """
        _optional_patterns=[
            r"ceph-",    # Ceph packages (only if ceph profile)
            r"zfs",    # ZFS packages (only if zfs/mixed profile)
            r"kubeadm",    # Kubernetes (only if k8s enabled)
            r"kubelet",    # Kubernetes
            r"kubectl",    # Kubernetes
            r"grpc-tools",    # RPC addon
            r"prometheus",    # Monitoring addon
            r"grafana",    # Monitoring addon
        ]
        return any(
            re.search(pattern, pkg, re.IGNORECASE) for pattern in optional_patterns  # type: ignore[name-defined]
        )

    def generate_report(self, results: Dict[str, List[str]]) -> str:
        """Generate validation report.

        Args:
            results: Validation results from validate_packages()

        Returns:
            Formatted report string
        """
        _report_lines=[
            "?" * 80,
            "PACKAGE VALIDATION REPORT",
            "?" * 80,
            f"Distribution: {self.dist}",
            f"Architecture: {self.arch}",
            "",
            "SUMMARY",
            "-" * 80,
            f"? Available:         {len(results['available']):4d} packages",
            f"[warn]?  Conditional:       {len(results['conditional']):4d} packages",
            f"??  Optional:          {len(results['optional']):4d} packages",
            f"? Missing:           {len(results['missing']):4d} packages",
            f"? Unknown:           {len(results['unknown']):4d} packages",
            "",
        ]

        # Add errors
        if self.errors:
            report_lines.extend(  # type: ignore[name-defined]
                [
                    "ERRORS",
                    "-" * 80,
                ]
            )
            for error in self.errors:
                report_lines.append(f"  * {error}")  # type: ignore[name-defined]
            report_lines.append("")  # type: ignore[name-defined]

        # Add warnings
        if self.warnings:
            report_lines.extend(  # type: ignore[name-defined]
                [
                    "WARNINGS",
                    "-" * 80,
                ]
            )
            for warning in self.warnings:
                report_lines.append(f"  * {warning}")  # type: ignore[name-defined]
            report_lines.append("")  # type: ignore[name-defined]

        # Overall validation status
        report_lines.extend(  # type: ignore[name-defined]
            [
                "VALIDATION STATUS",
                "-" * 80,
            ]
        )

        if not self.errors:
            report_lines.append("? PASS - All packages validated successfully")  # type: ignore[name-defined]
            if self.warnings:
                report_lines.append(f"   ({len(self.warnings)} warnings)")  # type: ignore[name-defined]
        else:
            report_lines.append(f"? FAIL - {len(self.errors)} validation errors found")  # type: ignore[name-defined]

        report_lines.append("?" * 80)  # type: ignore[name-defined]

        return "\n".join(report_lines)  # type: ignore[name-defined]

    def run(self) -> int:
        """Run complete validation pipeline.

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        print("Starting package validation...")

        # Validate inputs
        if not self.validate_distribution():
            print("\n".join(self.errors))
            return 1

        if not self.validate_architecture():
            print("\n".join(self.errors))
            return 1

        # Parse package lists
        _list_files=self.parse_package_lists()
        if not list_files:  # type: ignore[name-defined]
            print("\n".join(self.errors))
            return 1

        # Load packages
        _packages=self.load_packages(list_files)  # type: ignore[name-defined]
        print(f"Loaded {len(packages)} unique packages")  # type: ignore[name-defined]

        # Validate each package
        _results=self.validate_packages(packages)  # type: ignore[name-defined]

        # Generate report
        _report=self.generate_report(results)  # type: ignore[name-defined]
        print(report)  # type: ignore[name-defined]

        # Return exit code based on errors
        return 1 if self.errors else 0


def main() -> None:
    """Main entry point."""
    parser=argparse.ArgumentParser(  # type: ignore[call-arg]
        _description="Validate Debian packages for DebVisor ISO build"
    )
    parser.add_argument(
        "--dist", default="bookworm", help="Debian distribution (bookworm, trixie, sid)"
    )
    parser.add_argument(
        "--arch",
        _default="amd64",
        _help="Architecture (amd64, arm64, i386, armhf, ppc64el, s390x)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    _args=parser.parse_args()

    # Run validator
    _validator=PackageValidator(args.dist, args.arch, args.verbose)  # type: ignore[name-defined]
    _exit_code=validator.run()  # type: ignore[name-defined]

    # Output JSON if requested
    if args.json:  # type: ignore[name-defined]
        json_output={
            "distribution": args.dist,  # type: ignore[name-defined]
            "architecture": args.arch,  # type: ignore[name-defined]
            "errors": validator.errors,  # type: ignore[name-defined]
            "warnings": validator.warnings,  # type: ignore[name-defined]
            "exit_code": exit_code,  # type: ignore[name-defined]
        }
        print(json.dumps(json_output, indent=2))

    sys.exit(exit_code)  # type: ignore[name-defined]


if _name__== "__main__":  # type: ignore[name-defined]
    main()
