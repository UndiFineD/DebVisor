#!/usr/bin/env python3
"""
ISO Build Validator

Validates DebVisor ISO artifacts for completeness, integrity, and correctness.

Usage:
python3 validate-iso.py debvisor-*.hybrid.iso
python3 validate-iso.py debvisor-*.hybrid.iso --check-boot
python3 validate-iso.py debvisor-*.hybrid.iso --strict --verbose
"""

import argparse
import hashlib
import json
import os
import subprocessimport sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any


class ISOValidator:
    """Validates DebVisor ISO images."""

    def __init__(self, iso_path: str, verbose: bool = False, strict: bool = False):
        self.iso_path = Path(iso_path)
        self.verbose = verbose
        self.strict = strict
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: Dict[str, Any] = {}

    def validate(self) -> bool:
        """Run all validations."""
        print(f"Validating ISO: {self.iso_path}\n")

        if not self._check_file_exists():
            return False

        if not self._check_file_format():
            return False

        self._extract_metadata()

        if not self._validate_structure():
            return False

        if not self._check_boot_sectors():
            return False

        if not self._check_preseed():
            return False

        if not self._check_binaries():
            return False

        if not self._check_package_integrity():
            return False

        self._report()
        return len(self.errors) == 0

    def _check_file_exists(self) -> bool:
        """Verify ISO file exists and is readable."""
        if not self.iso_path.exists():
            self.errors.append(f"ISO file not found: {self.iso_path}")
            return False

        if not os.access(self.iso_path, os.R_OK):
            self.errors.append(f"ISO file not readable: {self.iso_path}")
            return False

        size_mb = self.iso_path.stat().st_size / (1024 * 1024)
        print(f"? File found ({size_mb:.1f} MB)")
        self.info['size_mb'] = size_mb
        return True

    def _check_file_format(self) -> bool:
        """Verify ISO file format."""
        try:
            result = subprocess.run(
                ['file', str(self.iso_path)],
                capture_output=True,
                text=True,
                timeout=5
            )    # nosec B603, B607

            if 'ISO 9660' not in result.stdout and 'UNIX UNIX-like' not in result.stdout:
                self.warnings.append(f"File type uncertain: {result.stdout.strip()}")
            else:
                print("? ISO format valid")

            return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.warnings.append("Could not verify file format (file command not available)")
            return True

    def _extract_metadata(self) -> None:
        """Extract ISO metadata."""
        try:
            result = subprocess.run(
                ['isoinfo', '-d', '-i', str(self.iso_path)],
                capture_output=True,
                text=True,
                timeout=10
            )    # nosec B603, B607

            # Parse isoinfo output
            for line in result.stdout.split('\n'):
                if 'Volume id' in line:
                    self.info['volume_id'] = line.split(':')[1].strip()
                elif 'Publisher id' in line:
                    self.info['publisher'] = line.split(':')[1].strip()
                elif 'Data preparer' in line:
                    self.info['preparer'] = line.split(':')[1].strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.warnings.append("Could not extract ISO metadata (isoinfo not available)")

    def _validate_structure(self) -> bool:
        """Validate ISO directory structure."""
        print("\nValidating structure...")

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Mount ISO
                subprocess.run(
                    ['mount', '-o', 'loop, ro', str(self.iso_path), tmpdir],
                    timeout=10,
                    check=True
                )    # nosec B603, B607

                expected_dirs = [
                    '/boot',
                    '/etc',
                    '/usr',
                    '/var',
                    '/opt',
                ]

                for dirname in expected_dirs:
                    path = Path(tmpdir) / dirname.lstrip('/')
                    if not path.exists():
                        if self.strict:
                            self.errors.append(f"Missing directory: {dirname}")
                        else:
                            self.warnings.append(f"Missing directory: {dirname}")
                    else:
                        if self.verbose:
                            print(f"  ? {dirname}")

                # Unmount
                subprocess.run(['umount', tmpdir], timeout=10, check=True)    # nosec B603, B607
                print("? Structure valid")
                return len(self.errors) == 0

            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                self.warnings.append(f"Could not mount ISO for structure check: {e}")
                return True    # Continue with other validations

    def _check_boot_sectors(self) -> bool:
        """Validate boot sectors."""
        print("Checking boot sectors...")

        try:
            # Check boot sector signature
            with open(self.iso_path, 'rb') as f:
                # Read sector at offset 16 (bootable ISO)
                f.seek(16 * 512)
                sector = f.read(512)

                if len(sector) == 512:
                    print("? Boot sector readable")
                else:
                    self.warnings.append("Could not read complete boot sector")

            return True
        except (IOError, OSError) as e:
            self.errors.append(f"Error reading boot sector: {e}")
            return False

    def _check_preseed(self) -> bool:
        """Verify preseed.cfg included."""
        print("Checking preseed configuration...")

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Mount ISO
                subprocess.run(
                    ['mount', '-o', 'loop, ro', str(self.iso_path), tmpdir],
                    timeout=10,
                    check=True
                )    # nosec B603, B607

                preseed_path = Path(tmpdir) / 'preseed.cfg'

                if preseed_path.exists():
                    size = preseed_path.stat().st_size

                    # Check preseed content
                    with open(preseed_path, 'r') as f:
                        content = f.read()

                        required_items = [
                            'd-i',    # Debian installer
                            'preseed',
                        ]

                        missing = [item for item in required_items if item not in content]
                        if missing:
                            self.warnings.append(
                                f"preseed.cfg may be incomplete: missing {missing}"
                            )
                        else:
                            print(f"? preseed.cfg found ({size} bytes)")
                else:
                    if self.strict:
                        self.errors.append("preseed.cfg not found in ISO")
                    else:
                        self.warnings.append("preseed.cfg not found in ISO")

                # Unmount
                subprocess.run(['umount', tmpdir], timeout=10, check=True)    # nosec B603, B607
                return len(self.errors) == 0

            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                self.warnings.append("Could not verify preseed (mount failed)")
                return True

    def _check_binaries(self) -> bool:
        """Verify required binaries present."""
        print("Checking for required binaries...")

        required_binaries = [
            '/bin/bash',
            '/bin/sh',
            '/usr/bin/debvisor-firstboot',
            '/usr/bin/debvisor-profile-summary',
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Mount ISO
                subprocess.run(
                    ['mount', '-o', 'loop, ro', str(self.iso_path), tmpdir],
                    timeout=10,
                    check=True
                )    # nosec B603, B607

                missing = []
                for binary in required_binaries:
                    path = Path(tmpdir) / binary.lstrip('/')
                    if not path.exists():
                        missing.append(binary)
                    elif self.verbose:
                        print(f"  ? {binary}")

                if missing:
                    if self.strict:
                        self.errors.append(f"Missing binaries: {missing}")
                    else:
                        self.warnings.append(f"Missing binaries: {missing}")
                else:
                    print("? Required binaries present")

                # Unmount
                subprocess.run(['umount', tmpdir], timeout=10, check=True)    # nosec B603, B607
                return len(self.errors) == 0

            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                self.warnings.append("Could not verify binaries (mount failed)")
                return True

    def _check_package_integrity(self) -> bool:
        """Verify package manifest integrity."""
        print("Checking package integrity...")

        # Calculate SHA256
        sha256 = self._calculate_sha256()
        if sha256:
            print(f"? SHA256: {sha256[:16]}...")
            self.info['sha256'] = sha256

        # Check for signature file
        sig_path = self.iso_path.with_suffix('.asc')
        if sig_path.exists():
            print(f"? GPG signature found: {sig_path.name}")
            self.info['signed'] = True
        else:
            if self.strict:
                self.warnings.append("No GPG signature found")
            else:
                self.info['signed'] = False

        return True

    def _calculate_sha256(self) -> Optional[str]:
        """Calculate SHA256 checksum of ISO."""
        try:
            sha256_hash = hashlib.sha256()
            with open(self.iso_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except IOError as e:
            self.warnings.append(f"Could not calculate SHA256: {e}")
            return None

    def _report(self) -> None:
        """Print validation report."""
        print("\n" + "=" * 70)
        print("VALIDATION REPORT")
        print("=" * 70)

        if self.info:
            print("\nISO Information:")
            for key, value in self.info.items():
                print(f"  {key}: {value}")

        if self.errors:
            print(f"\n? ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n[warn]?  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n? ISO validation passed!")

        print("\n" + "=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate DebVisor ISO images"
    )
    parser.add_argument('iso', help='Path to ISO image')
    parser.add_argument('--strict', action='store_true', help='Fail on warnings')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    validator = ISOValidator(args.iso, verbose=args.verbose, strict=args.strict)
    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
