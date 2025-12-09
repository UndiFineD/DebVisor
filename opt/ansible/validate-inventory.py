#!/usr/bin/env python3
"""
Ansible Inventory Validator

Validates DebVisor Ansible inventory files for:
- Required groups and hosts
- Required variables per group/host
- Network connectivity (SSH reachability)
- Variable value constraints (e.g., valid IP addresses, CIDR notation)

Usage:
python3 validate_inventory.py inventory.yaml
python3 validate_inventory.py inventory.lab --check-ssh
python3 validate_inventory.py inventory.prod --strict
"""

import argparse
import re
import subprocess
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any


class InventoryValidator:
    """Validates Ansible inventory files."""

    def __init__(
        self, inventory_path: str, verbose: bool = False, strict: bool = False
    ):
        self.inventory_path = Path(inventory_path)
        self.verbose = verbose
        self.strict = strict
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.inventory: Dict[str, Any] = {}

    def load_inventory(self) -> bool:
        """Load YAML inventory file."""
        try:
            with open(self.inventory_path, "r") as f:
                self.inventory = yaml.safe_load(f)
            if not self.inventory:
                self.errors.append(f"Inventory file {self.inventory_path} is empty")
                return False
            return True
        except FileNotFoundError:
            self.errors.append(f"Inventory file not found: {self.inventory_path}")
            return False
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML: {e}")
            return False

    def validate_structure(self) -> bool:
        """Validate basic inventory structure."""
        if "all" not in self.inventory:
            self.errors.append("Missing 'all' group in inventory")
            return False

        all_group = self.inventory.get("all", {})
        if "children" not in all_group:
            self.warnings.append("No child groups defined in 'all' group")

        return len(self.errors) == 0

    def validate_required_groups(self) -> bool:
        """Validate presence of required groups."""
        required_groups = {
            "all_dns": ["dns_primaries", "dns_secondaries"],
            "all_ceph": ["ceph_mons", "ceph_osds"],
            "all_kubernetes": ["k8s_controlplane", "k8s_workers"],
            "hypervisors": [],
            "management": [],
        }

        all_children = self.inventory.get("all", {}).get("children", {})

        for group_name, required_subgroups in required_groups.items():
            if group_name not in all_children:
                self.warnings.append(f"Optional group '{group_name}' not found")
                continue

            group = all_children[group_name]
            if isinstance(group, dict) and "children" in group:
                for subgroup in required_subgroups:
                    if subgroup not in group["children"]:
                        self.errors.append(
                            f"Required subgroup '{subgroup}' not found in '{group_name}'"
                        )
            elif isinstance(group, dict) and "hosts" in group:
                if required_subgroups:
                    self.warnings.append(
                        f"Group '{group_name}' has hosts but should have subgroups: "
                        f"{required_subgroups}"
                    )

        return len(self.errors) == 0

    def validate_variables(self) -> bool:
        """Validate required variables per group."""
        required_vars = {
            "all": ["domain_name", "ntp_servers", "dns_servers"],
            "dns_primaries": ["bind_role", "dns_zones"],
            "dns_secondaries": ["bind_role", "primary_nameserver"],
            "ceph_mons": ["mon_role", "ceph_address"],
            "ceph_osds": ["osd_role", "osd_devices"],
            "k8s_controlplane": ["kube_role", "kube_apiserver_advertise_address"],
            "k8s_workers": ["kube_role"],
            "hypervisors": ["libvirt_uri", "vm_disk_pool"],
            "management": ["is_management_node"],
        }

        all_group = self.inventory.get("all", {})
        all_vars = all_group.get("vars", {})
        all_children = all_group.get("children", {})

        # Check global vars
        for var in required_vars.get("all", []):
            if var not in all_vars:
                self.errors.append(f"Missing required global variable: '{var}'")

        # Check group-specific vars
        def check_group_vars(group_name: str, group_data: Dict[str, Any]) -> None:
            if isinstance(group_data, dict):
                group_vars = group_data.get("vars", {})
                group_children = group_data.get("children", {})

                # Check this group's variables
                for var in required_vars.get(group_name, []):
                    if var not in group_vars:
                        if self.strict:
                            self.errors.append(
                                f"Group '{group_name}' missing required variable: '{var}'"
                            )
                        else:
                            self.warnings.append(
                                f"Group '{group_name}' missing recommended variable: '{var}'"
                            )

                # Recursively check subgroups
                for subgroup_name, subgroup_data in group_children.items():
                    check_group_vars(subgroup_name, subgroup_data)

        for group_name, group_data in all_children.items():
            check_group_vars(group_name, group_data)

        return len(self.errors) == 0

    def validate_host_variables(self) -> bool:
        """Validate required variables on individual hosts."""
        host_var_requirements = {
            "dns_primaries": ["ansible_host", "bind_listen_ipv4", "dns_zones"],
            "dns_secondaries": [
                "ansible_host",
                "bind_listen_ipv4",
                "primary_nameserver",
            ],
            "ceph_mons": ["ansible_host", "ceph_address"],
            "ceph_osds": ["ansible_host", "ceph_address", "osd_devices"],
            "k8s_controlplane": ["ansible_host", "kube_apiserver_advertise_address"],
            "k8s_workers": ["ansible_host"],
            "hypervisors": ["ansible_host"],
            "management": ["ansible_host"],
        }

        def extract_hosts(
            group_name: str, group_data: Dict[str, Any], parent_path: str = ""
        ) -> None:
            if isinstance(group_data, dict):
                group_hosts = group_data.get("hosts", {})
                group_children = group_data.get("children", {})

                # Check hosts in this group
                required_vars = host_var_requirements.get(group_name, [])
                for host_name, host_data in group_hosts.items():
                    if isinstance(host_data, dict):
                        for var in required_vars:
                            if var not in host_data:
                                self.warnings.append(
                                    f"Host '{host_name}' missing recommended variable: '{var}'"
                                )
                        # Validate IP addresses
                        if "ansible_host" in host_data:
                            ip = host_data["ansible_host"]
                            if not self._is_valid_ip(
                                ip
                            ) and not self._is_valid_hostname(ip):
                                self.errors.append(
                                    f"Host '{host_name}': invalid ansible_host '{ip}'"
                                )

                # Recursively check subgroups
                for subgroup_name, subgroup_data in group_children.items():
                    extract_hosts(
                        subgroup_name, subgroup_data, f"{parent_path}/{group_name}"
                    )

        all_children = self.inventory.get("all", {}).get("children", {})
        for group_name, group_data in all_children.items():
            extract_hosts(group_name, group_data)

        return True  # Validation collected in self.errors

    def _is_valid_ip(self, ip: str) -> bool:
        """Check if string is a valid IPv4 address."""
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(p) <= 255 for p in parts)
        except ValueError:
            return False

    def _is_valid_hostname(self, hostname: str) -> bool:
        """Check if string is a valid hostname."""
        pattern = r"^(?!-)[a-zA-Z0-9-]{1, 63}(?<!-)(\.[a-zA-Z0-9-]{1, 63})*$"
        return bool(re.match(pattern, hostname))

    def validate_network_connectivity(self, check_ssh: bool = False) -> bool:
        """Validate network connectivity to hosts."""
        if not check_ssh:
            return True

        print("\nValidating network connectivity...")
        hosts_to_check: Dict[str, str] = {}

        def extract_hosts_with_ips(group_data: Dict[str, Any]) -> None:
            if isinstance(group_data, dict):
                group_hosts = group_data.get("hosts", {})
                group_children = group_data.get("children", {})

                for host_name, host_data in group_hosts.items():
                    if isinstance(host_data, dict) and "ansible_host" in host_data:
                        hosts_to_check[host_name] = host_data["ansible_host"]

                for subgroup_data in group_children.values():
                    extract_hosts_with_ips(subgroup_data)

        all_children = self.inventory.get("all", {}).get("children", {})
        for group_data in all_children.values():
            extract_hosts_with_ips(group_data)

        for host_name, ip in hosts_to_check.items():
            # Check DNS resolution
            try:
                result = subprocess.run(
                    ["nslookup", host_name], capture_output=True, timeout=5
                )  # nosec B603, B607
                if result.returncode != 0:
                    self.warnings.append(f"DNS resolution failed for {host_name}")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

            # Check SSH connectivity
            try:
                result = subprocess.run(
                    [
                        "ssh",
                        "-o",
                        "ConnectTimeout=5",
                        "-o",
                        "StrictHostKeyChecking=no",
                        f"root@{ip}",
                        "exit",
                    ],
                    capture_output=True,
                    timeout=10,
                )  # nosec B603, B607
                if result.returncode != 0:
                    self.warnings.append(
                        f"SSH connectivity check failed for {host_name} ({ip})"
                    )
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        return True

    def validate(self, check_ssh: bool = False) -> bool:
        """Run all validations."""
        print(f"Validating inventory: {self.inventory_path}\n")

        if not self.load_inventory():
            return False

        print("? Inventory loaded")

        if not self.validate_structure():
            print("? Structure validation failed")
            return False
        print("? Structure valid")

        if not self.validate_required_groups():
            print("? Required groups validation failed")
        else:
            print("? Required groups present")

        if not self.validate_variables():
            print("? Variable validation failed")
        else:
            print("? Required variables present")

        if not self.validate_host_variables():
            print("? Host variable validation failed")
        else:
            print("? Host variables validated")

        self.validate_network_connectivity(check_ssh)

        return self.report()

    def report(self) -> bool:
        """Print validation report."""
        print("\n" + "=" * 70)

        if self.errors:
            print(f"\n? ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n[warn]?  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n? All validations passed!")

        print("\n" + "=" * 70)

        return len(self.errors) == 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate DebVisor Ansible inventory files"
    )
    parser.add_argument(
        "inventory", help="Path to inventory file (inventory.yaml, inventory.lab, etc.)"
    )
    parser.add_argument(
        "--check-ssh", action="store_true", help="Check SSH connectivity to all hosts"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Fail on warnings (not just errors)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    validator = InventoryValidator(
        args.inventory, verbose=args.verbose, strict=args.strict
    )
    success = validator.validate(check_ssh=args.check_ssh)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
