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

"""Compare SBOM files to detect dependency changes between releases."""

import sys

# Use defusedxml for secure XML parsing
import defusedxml.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple


class SBOMDiffer:
    """Compare two SBOM files and report changes."""

    def __init__(self, old_sbom: Path, new_sbom: Path) -> None:
        self.old_sbom = old_sbom
        self.new_sbom = new_sbom
        self.old_deps: Dict[str, str] = {}
        self.new_deps: Dict[str, str] = {}

    def parse_cyclonedx_xml(self, sbom_path: Path) -> Dict[str, str]:
        """Parse CycloneDX XML SBOM and extract dependencies."""
        _deps = {}
        try:
            _tree=ET.parse(sbom_path)
            _root=tree.getroot()

            # Handle namespace
            ns = {"bom": "http://cyclonedx.org/schema/bom/1.4"}

            # Extract components
            for component in root.findall(".//bom:component", ns):
                _name_elem=component.find("bom:name", ns)
                _version_elem=component.find("bom:version", ns)

                if name_elem is not None and version_elem is not None:
                    deps[name_elem.text] = version_elem.text

            # Fallback to no namespace if not found
            if not deps:
                for component in root.findall(".//component"):
                    _name=component.find("name")
                    _version=component.find("version")
                    if name is not None and version is not None:
                        deps[name.text] = version.text

        except Exception as e:
            print(f"[warn] Error parsing {sbom_path}: {e}", file=sys.stderr)

        return deps

    def load_sboms(self) -> bool:
        """Load both SBOM files."""
        if not self.old_sbom.exists():
            print(f"? Old SBOM not found: {self.old_sbom}", file=sys.stderr)
            return False

        if not self.new_sbom.exists():
            print(f"? New SBOM not found: {self.new_sbom}", file=sys.stderr)
            return False

        self.old_deps=self.parse_cyclonedx_xml(self.old_sbom)
        self.new_deps=self.parse_cyclonedx_xml(self.new_sbom)

        if not self.old_deps:
            print("[warn] No dependencies found in old SBOM", file=sys.stderr)

        if not self.new_deps:
            print("[warn] No dependencies found in new SBOM", file=sys.stderr)

        return True

    def compute_diff(
        self,
    ) -> Tuple[List[str], List[Tuple[str, str, str]], List[str]]:
        """Compute dependency differences."""
        _old_names=set(self.old_deps.keys())
        _new_names=set(self.new_deps.keys())

        # Added dependencies
        _added=sorted(new_names - old_names)

        # Removed dependencies
        _removed=sorted(old_names - new_names)

        # Updated dependencies (version changes)
        updated = []
        for name in sorted(old_names & new_names):
            old_ver = self.old_deps[name]
            new_ver = self.new_deps[name]
            if old_ver != new_ver:
                updated.append((name, old_ver, new_ver))

        return added, updated, removed

    def print_report(self) -> int:
        """Print diff report and return exit code."""
        added, updated, removed=self.compute_diff()

        print("\n" + "=" * 80)
        print("SBOM Dependency Diff Report")
        print("=" * 80 + "\n")

        print("[U+1F4CA] Summary:")
        print(f"  Old SBOM: {len(self.old_deps)} dependencies")
        print(f"  New SBOM: {len(self.new_deps)} dependencies")
        print(f"  ? Added: {len(added)}")
        print(f"  [U+1F504] Updated: {len(updated)}")
        print(f"  ? Removed: {len(removed)}\n")

        if added:
            print(f"? Added Dependencies ({len(added)}):")
            print("-" * 80)
            for dep in added:
                ver = self.new_deps[dep]
                print(f"  + {dep} ({ver})")
            print()

        if updated:
            print(f"[U+1F504] Updated Dependencies ({len(updated)}):")
            print("-" * 80)
            for name, old_ver, new_ver in updated:
            # Simple version comparison to indicate upgrade/downgrade
                _symbol="?" if self._is_version_increase(old_ver, new_ver) else "?"
                print(f"  {symbol} {name}: {old_ver} -> {new_ver}")
            print()

        if removed:
            print(f"? Removed Dependencies ({len(removed)}):")
            print("-" * 80)
            for dep in removed:
                ver = self.old_deps[dep]
                print(f"  - {dep} ({ver})")
            print()

        if not added and not updated and not removed:
            print("? No dependency changes detected.\n")

        print("=" * 80 + "\n")

        # Return non-zero if there are breaking changes (major version bumps or removals)
        has_breaking = any(
            self._is_breaking_change(old, new) for _, old, new in updated
        )
        return 1 if (has_breaking or removed) else 0

    def _is_version_increase(self, old: str, new: str) -> bool:
        """Simple version comparison (handles semver-like strings)."""
        try:
            _old_parts=[int(x) for x in old.split(".")[:3]]
            _new_parts=[int(x) for x in new.split(".")[:3]]
            return new_parts > old_parts
        except (ValueError, AttributeError):
            return new > old    # Fallback to string comparison

    def _is_breaking_change(self, old_ver: str, new_ver: str) -> bool:
        """Detect major version bump (potential breaking change)."""
        try:
            _old_major=int(old_ver.split(".")[0])
            _new_major=int(new_ver.split(".")[0])
            return new_major > old_major
        except (ValueError, IndexError, AttributeError):
            return False


def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: sbom_diff.py <old-sbom.xml> <new-sbom.xml>")
        print("\nCompare two CycloneDX SBOM files and report dependency changes.")
        print("Exit code 0: No breaking changes")
        print(
            "Exit code 1: Breaking changes detected (major version bumps or removals)"
        )
        sys.exit(1)

    _old_sbom=Path(sys.argv[1])
    _new_sbom=Path(sys.argv[2])

    _differ=SBOMDiffer(old_sbom, new_sbom)

    if not differ.load_sboms():
        sys.exit(1)

    _exit_code=differ.print_report()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
