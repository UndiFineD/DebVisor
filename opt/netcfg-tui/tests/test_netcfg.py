import os
import sys
import unittest  # type: ignore[syntax]
from netcfg_tui import (
    InterfaceConfig,
    BridgeConfig,
    write_networkd,
    write_netplan,
    preflight_checks,
    validate_ipv4_address,
    validate_cidr,
    validate_dns_servers,
)
from unittest.mock import patch, MagicMock, mock_open

# Mock curses before importing netcfg_tui
sys.modules["curses"] = MagicMock()

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestValidation(unittest.TestCase):
    def test_validate_ipv4_address(self):
        self.assertTrue(validate_ipv4_address("192.168.1.1")[0])
        self.assertFalse(validate_ipv4_address("256.1.1.1")[0])
        self.assertFalse(validate_ipv4_address("abc")[0])
        self.assertFalse(validate_ipv4_address("")[0])

    def test_validate_cidr(self):
        self.assertTrue(validate_cidr("192.168.1.1", 24)[0])
        self.assertTrue(validate_cidr("10.0.0.1", 0)[0])
        self.assertTrue(validate_cidr("10.0.0.1", 32)[0])
        self.assertFalse(validate_cidr("192.168.1.1", 33)[0])
        self.assertFalse(validate_cidr("192.168.1.1", -1)[0])
        self.assertFalse(validate_cidr("abc", 24)[0])

    def test_validate_dns_servers(self):
        self.assertTrue(validate_dns_servers(["8.8.8.8", "1.1.1.1"])[0])
        self.assertTrue(validate_dns_servers([])[0])
        self.assertFalse(validate_dns_servers(["8.8.8.8", "abc"])[0])


class TestNetCfg(unittest.TestCase):
    def test_interface_config_summary(self):
        cfg = InterfaceConfig("eth0", "wired")
        self.assertIn("eth0 (wired) dhcp", cfg.summary())

        cfg.method = "static"
        cfg.address = "192.168.1.10"
        self.assertIn("192.168.1.10/24", cfg.summary())

    def test_bridge_config_summary(self):
        br = BridgeConfig("br0")
        self.assertIn("br0 (bridge) dhcp", br.summary())

        br.stp = False
        self.assertIn("stp=off", br.summary())

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_write_networkd(self, mock_makedirs, mock_file):
        cfg = InterfaceConfig("eth0", "wired")
        cfg.method = "static"
        cfg.address = "10.0.0.1"

        write_networkd([cfg], "/tmp/out")

        # Check if files were written
        # We expect 10-eth0.network
        mock_file.assert_called()
        handle = mock_file()
        handle.write.assert_called()

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_write_netplan(self, mock_makedirs, mock_file):
        cfg = InterfaceConfig("eth0", "wired")
        write_netplan([cfg], "/tmp/out")

        mock_file.assert_called()
        handle = mock_file()
        handle.write.assert_called()

    @patch("os.geteuid", create=True)
    @patch("os.path.exists")
    @patch("subprocess.run")
    def test_preflight_checks_networkd(self, mock_run, mock_exists, mock_geteuid):
        mock_geteuid.return_value = 0
        mock_exists.return_value = True    # /etc/systemd/network exists
        mock_run.return_value.returncode = 0    # systemctl is-active success

        errors = preflight_checks("networkd")
        self.assertEqual(errors, [])

    @patch("os.geteuid", create=True)
    @patch("subprocess.run")
    def test_preflight_checks_root_fail(self, mock_run, mock_geteuid):
        mock_geteuid.return_value = 1000
        errors = preflight_checks("networkd")
        self.assertIn("Must run as root to apply configuration.", errors)


if __name__ == "__main__":
    unittest.main()
