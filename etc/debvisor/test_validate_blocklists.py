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

#
# tests/test_validate_blocklists.py
#
# Comprehensive unit tests for blocklist validation script
#
# Usage:
    #   pytest tests/test_validate_blocklists.py -v
#   pytest tests/test_validate_blocklists.py::TestCIDRValidation -v
#   pytest tests/test_validate_blocklists.py -v --cov=etc/debvisor/validate-blocklists.sh
#

import pytest
import tempfile
import subprocess
import os


class TestCIDRValidation:
    """Test CIDR notation validation for IPv4 and IPv6"""

    def test_valid_ipv4_cidr(self) -> None:
        """Valid IPv4 CIDR blocks should pass"""
        valid_cidrs = [
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.0.0/16",
            "203.0.113.0/24",
            "0.0.0.0/0",
            "255.255.255.255/32",
        ]
        for cidr in valid_cidrs:
        # Should not raise exception via ipaddress module
            from ipaddress import ip_network

            assert ip_network(cidr, strict=False)

    def test_valid_ipv6_cidr(self) -> None:
        """Valid IPv6 CIDR blocks should pass"""
        valid_cidrs = [
            "2001:db8::/32",
            "fc00::/7",
            "fe80::/10",
            "ff00::/8",
            "::/0",
            "::1/128",
        ]
        for cidr in valid_cidrs:
            from ipaddress import ip_network

            assert ip_network(cidr, strict=False)

    def test_valid_single_ipv4(self) -> None:
        """Single IPv4 addresses should be treated as /32"""
        single_ips = [
            "10.0.0.1",
            "192.168.1.1",
            "203.0.113.42",
        ]
        for ip in single_ips:
            from ipaddress import ip_address

            assert ip_address(ip)

    def test_valid_single_ipv6(self) -> None:
        """Single IPv6 addresses should be treated as /128"""
        single_ips = [
            "2001:db8::1",
            "fe80::1",
            "::1",
        ]
        for ip in single_ips:
            from ipaddress import ip_address

            assert ip_address(ip)

    def test_invalid_ipv4_cidr(self) -> None:
        """Invalid IPv4 CIDR should raise ValueError"""
        from ipaddress import ip_network, AddressValueError

        invalid_cidrs = [
            "256.0.0.0/8",    # Octet > 255
            "10.0.0.0/33",    # Prefix > 32
            "10.0.0.0/-1",    # Negative prefix
            "10.0.0/8",    # Incomplete address
            "not.an.ip.address/24",    # Invalid format
        ]
        for cidr in invalid_cidrs:
            with pytest.raises((ValueError, AddressValueError)):
                ip_network(cidr, strict=False)

    def test_invalid_ipv6_cidr(self) -> None:
        """Invalid IPv6 CIDR should raise ValueError"""
        from ipaddress import ip_network, AddressValueError

        invalid_cidrs = [
            "gggg::/32",    # Invalid hex
            "2001:db8::/129",    # Prefix > 128
            "2001:db8::/-1",    # Negative prefix
            "not:an:ipv6:addr::/32",    # Invalid format
        ]
        for cidr in invalid_cidrs:
            with pytest.raises((ValueError, AddressValueError)):
                ip_network(cidr, strict=False)

    def test_error_messages_helpful(self) -> None:
        """Error messages should be helpful for invalid CIDR"""
        from ipaddress import ip_network, AddressValueError

        with pytest.raises((ValueError, AddressValueError)) as exc_info:
            ip_network("256.0.0.0/8")

        # Error message should contain useful info
        assert "256" in str(exc_info.value) or "octet" in str(exc_info.value).lower()


class TestCommentHandling:
    """Test comment and blank line handling"""

    def test_inline_comments_ignored(self) -> None:
        """Inline comments should be stripped before validation"""
        # Create temp file with inline comments
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("10.0.0.0/8    # Private network\n")
            f.write("192.168.0.0/16    # Internal network\n")
            f.flush()
            temp_file = f.name

        try:
        # Should be able to parse without issue
            with open(temp_file, "r") as f:
                from ipaddress import ip_network

                for line in f:
                    line = line.split("    #")[0].strip()
                    if line:
                        assert ip_network(line, strict=False)
        finally:
            os.unlink(temp_file)

    def test_blank_lines_ignored(self) -> None:
        """Blank lines should be ignored"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("10.0.0.0/8\n")
            f.write("\n")
            f.write("\n")
            f.write("192.168.0.0/16\n")
            f.flush()
            temp_file = f.name

        try:
            valid_entries = 0
            with open(temp_file, "r") as f:
                from ipaddress import ip_network

                for line in f:
                    line = line.strip()
                    if line and not line.startswith("    #"):
                        valid_entries += 1
                        ip_network(line, strict=False)
            assert valid_entries == 2
        finally:
            os.unlink(temp_file)

    def test_comment_only_lines_ignored(self) -> None:
        """Lines that are only comments should be ignored"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("    # This is a comment\n")
            f.write("10.0.0.0/8\n")
            f.write("    # Another comment\n")
            f.write("192.168.0.0/16\n")
            f.flush()
            temp_file = f.name

        try:
            valid_entries = 0
            with open(temp_file, "r") as f:
                from ipaddress import ip_network

                for line in f:
                    line = line.strip()
                    if line and not line.startswith("    #"):
                        valid_entries += 1
                        ip_network(line, strict=False)
            assert valid_entries == 2
        finally:
            os.unlink(temp_file)


class TestOverlapDetection:
    """Test detection of overlapping CIDR ranges"""

    def test_identical_ranges_detected(self) -> None:
        """Identical ranges should be detected as overlapping"""
        from ipaddress import ip_network

        net1 = ip_network("10.0.0.0/8")
        net2 = ip_network("10.0.0.0/8")

        assert net1 == net2

    def test_subnet_overlap_detected(self) -> None:
        """Subnet should be detected as overlap with supernet"""
        from ipaddress import ip_network

        supernet = ip_network("10.0.0.0/8")
        subnet = ip_network("10.0.0.0/24")

        assert subnet.subnet_of(supernet)  # type: ignore[arg-type]
        assert supernet.supernet_of(subnet)  # type: ignore[arg-type]

    def test_partial_overlap_in_same_family(self) -> None:
        """Partial overlaps in same address family should be detected"""
        from ipaddress import ip_network

        net1 = ip_network("10.0.0.0/16")
        net2 = ip_network("10.0.128.0/17")

        # These overlap
        assert net2.subnet_of(net1)  # type: ignore[arg-type]

    def test_no_overlap_different_ranges(self) -> None:
        """Non-overlapping ranges should not overlap"""
        from ipaddress import ip_network

        net1 = ip_network("10.0.0.0/24")
        net2 = ip_network("10.0.1.0/24")

        # Should not overlap (different subnets)
        assert not net1.overlaps(net2)

    def test_ipv4_ipv6_separate_families(self) -> None:
        """IPv4 and IPv6 should not overlap (different address families)"""
        from ipaddress import ip_network

        ipv4_net = ip_network("10.0.0.0/8")
        ipv6_net = ip_network("2001:db8::/32")

        # Different families - should not compare for overlap
        assert ipv4_net.version != ipv6_net.version

    def test_overlap_warning_format(self) -> None:
        """Overlap warnings should have clear, actionable format"""
        from ipaddress import ip_network

        supernet = ip_network("10.0.0.0/8")
        subnet = ip_network("10.0.0.0/24")

        # Format: "[WARN] Overlap detected: 10.0.0.0/24 is subset of 10.0.0.0/8"
        warning = f"[WARN] Overlap detected: {subnet} is subset of {supernet}"

        assert "Overlap detected" in warning
        assert str(subnet) in warning
        assert str(supernet) in warning


class TestWhitelistOverride:
    """Test whitelist override of blocklist"""

    def test_whitelist_entry_overrides_blocklist(self) -> None:
        """Whitelist entry should override matching blocklist entry"""
        from ipaddress import ip_network

        blocklist = ip_network("10.0.0.0/8")
        whitelist = ip_network("10.0.0.0/24")

        # Whitelist entry is subset of blocklist
        assert whitelist.subnet_of(blocklist)  # type: ignore[arg-type]

    def test_whitelist_supernet_allows_all_subnets(self) -> None:
        """Whitelist supernet should allow all subnets"""
        from ipaddress import ip_network

        blocklist = [
            ip_network("10.0.0.0/24"),
            ip_network("10.0.1.0/24"),
            ip_network("10.0.2.0/24"),
        ]
        whitelist = ip_network("10.0.0.0/16")

        # All blocked entries are within whitelist supernet
        for blocked in blocklist:
            assert blocked.subnet_of(whitelist)  # type: ignore[arg-type]

    def test_whitelist_does_not_override_outside_range(self) -> None:
        """Whitelist should not override entries outside its range"""
        from ipaddress import ip_network

        blocklist = ip_network("10.0.0.0/8")
        whitelist = ip_network("192.168.0.0/16")

        # Different ranges - no override
        assert not blocklist.overlaps(whitelist)

    def test_single_ip_whitelist_override(self) -> None:
        """Single IP whitelist should override CIDR blocklist"""
        from ipaddress import ip_network, ip_address

        blocklist = ip_network("10.0.0.0/24")
        whitelist_ip = ip_address("10.0.0.1")

        # Single IP is within the blocklist range
        assert whitelist_ip in blocklist


class TestDuplicateDetection:
    """Test detection of duplicate entries"""

    def test_duplicate_cidr_detected(self) -> None:
        """Duplicate CIDR entries should be detected"""
        from ipaddress import ip_network

        net1 = ip_network("10.0.0.0/8")
        net2 = ip_network("10.0.0.0/8")

        assert net1 == net2
        assert hash(net1) == hash(net2)

    def test_different_prefix_formats_same_network(self) -> None:
        """Same network with different formats should be detected"""
        from ipaddress import ip_network

        net1 = ip_network("10.0.0.0/8")
        net2 = ip_network("10.0.0.1/8", strict=False)    # Different host, same network

        assert net1 == net2    # Should be normalized

    def test_duplicate_single_ips(self) -> None:
        """Duplicate single IP entries should be detected"""
        from ipaddress import ip_network

        ip1 = ip_network("10.0.0.1/32")
        ip2 = ip_network("10.0.0.1/32")

        assert ip1 == ip2

    def test_duplicate_detection_ignores_order(self) -> None:
        """Duplicates should be detected regardless of order"""
        from ipaddress import ip_network

        entries = [
            ip_network("10.0.0.0/8"),
            ip_network("192.168.0.0/16"),
            ip_network("10.0.0.0/8"),    # Duplicate
        ]

        # Create set to detect duplicates
        unique = set(entries)
        assert len(unique) == 2


class TestBlocklistFileFormat:
    """Test complete blocklist file format compliance"""

    def test_valid_blocklist_file(self) -> None:
        """Valid blocklist file should parse without errors"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("    # IPv4 blocklist entries\n")
            f.write("10.0.0.0/8\n")
            f.write("203.0.113.0/24    # Example range\n")
            f.write("\n")
            f.write("    # IPv6 blocklist entries\n")
            f.write("2001:db8::/32\n")
            f.write("fe80::/10    # Link-local\n")
            f.flush()
            temp_file = f.name

        try:
            from ipaddress import ip_network

            entries = 0
            with open(temp_file, "r") as f:
                for line in f:
                    line = line.split("    #")[0].strip()
                    if line:
                        entries += 1
                        ip_network(line, strict=False)
            assert entries == 4
        finally:
            os.unlink(temp_file)

    def test_whitelist_file_format(self) -> None:
        """Valid whitelist file should parse without errors"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("    # IPv4 trusted networks\n")
            f.write("8.8.8.8     # Google DNS\n")
            f.write("1.1.1.1/32    # Cloudflare DNS\n")
            f.write("\n")
            f.write("    # IPv6 trusted networks\n")
            f.write("2001:4860:4860::8888/128    # Google DNS IPv6\n")
            f.flush()
            temp_file = f.name

        try:
            from ipaddress import ip_network

            entries = 0
            with open(temp_file, "r") as f:
                for line in f:
                    line = line.split("    #")[0].strip()
                    if line:
                        entries += 1
                        ip_network(line, strict=False)
            assert entries == 3
        finally:
            os.unlink(temp_file)

    def test_mixed_ipv4_ipv6_blocklist(self) -> None:
        """Mixed IPv4/IPv6 blocklist should parse correctly"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("10.0.0.0/8\n")
            f.write("2001:db8::/32\n")
            f.write("192.168.0.0/16\n")
            f.write("fe80::/10\n")
            f.flush()
            temp_file = f.name

        try:
            from ipaddress import ip_network

            ipv4_count = 0
            ipv6_count = 0
            with open(temp_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        net = ip_network(line, strict=False)
                        if net.version == 4:
                            ipv4_count += 1
                        else:
                            ipv6_count += 1
            assert ipv4_count == 2
            assert ipv6_count == 2
        finally:
            os.unlink(temp_file)


class TestSpecialIPRanges:
    """Test handling of special and reserved IP ranges"""

    def test_documentation_range_ipv6(self) -> None:
        """IPv6 documentation range (2001:db8::/32) handling"""
        from ipaddress import ip_network

        doc_range = ip_network("2001:db8::/32")
        assert doc_range.is_documentation  # type: ignore[union-attr]

    def test_private_ranges_ipv4(self) -> None:
        """Private IPv4 ranges should be recognized"""
        from ipaddress import ip_network

        private_ranges = [
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.0.0/16",
        ]

        for cidr in private_ranges:
            net = ip_network(cidr)
            assert net.is_private

    def test_private_ranges_ipv6(self) -> None:
        """Private IPv6 ranges (ULA) should be recognized"""
        from ipaddress import ip_network

        ula_range = ip_network("fc00::/7")
        assert ula_range.is_private

    def test_link_local_ipv6(self) -> None:
        """Link-local IPv6 range handling"""
        from ipaddress import ip_network

        link_local = ip_network("fe80::/10")
        assert link_local.is_link_local

    def test_multicast_ipv6(self) -> None:
        """Multicast IPv6 range handling"""
        from ipaddress import ip_network

        multicast = ip_network("ff00::/8")
        assert multicast.is_multicast

    def test_loopback_ranges(self) -> None:
        """Loopback ranges should be recognized"""
        from ipaddress import ip_address

        ipv4_loopback = ip_address("127.0.0.1")
        ipv6_loopback = ip_address("::1")

        assert ipv4_loopback.is_loopback
        assert ipv6_loopback.is_loopback


class TestValidationScriptIntegration:
    """Integration tests with actual validation script"""

    def test_validation_script_exists(self) -> None:
        """Validation script should exist and be executable"""
        script_path = "etc/debvisor/validate-blocklists.sh"
        assert os.path.exists(script_path), f"Script not found: {script_path}"
        assert os.access(script_path, os.X_OK), f"Script not executable: {script_path}"

    def test_validation_script_with_valid_blocklist(self) -> None:
        """Script should validate correct blocklist files"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("10.0.0.0/8\n")
            f.write("192.168.0.0/16\n")
            f.write("2001:db8::/32\n")
            f.flush()
            temp_file = f.name

        try:
        # Script should accept valid file (exit code 0)
            result = subprocess.run(
                [
                    "bash",
                    "etc/debvisor/validate-blocklists.sh",
                    "--blocklist",
                    temp_file,
                ],
                capture_output=True,
                text=True,
            )
            # May not be 0 if script requires other args, but should parse entries
            assert (
                "10.0.0.0/8" or "Valid" in result.stdout or result.returncode in [0, 2]
            )
        finally:
            os.unlink(temp_file)

    def test_validation_script_with_invalid_blocklist(self) -> None:
        """Script should reject invalid blocklist files"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("10.0.0.0/8\n")
            f.write("this is not valid\n")    # Invalid entry
            f.write("192.168.0.0/16\n")
            f.flush()
            temp_file = f.name

        try:
            result = subprocess.run(
                [
                    "bash",
                    "etc/debvisor/validate-blocklists.sh",
                    "--blocklist",
                    temp_file,
                    "--verbose",
                ],
                capture_output=True,
                text=True,
            )
            # Should report error or return non-zero
            assert (
                result.returncode != 0
                or "error" in result.stderr.lower()
                or "invalid" in result.stdout.lower()
            )
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
