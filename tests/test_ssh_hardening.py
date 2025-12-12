import unittest
from opt.services.security.ssh_hardening import SSHHardeningManager, SSHSecurityLevel

class TestSSHHardening(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = SSHHardeningManager(config_path="/tmp/ssh")

    def test_basic_security_config(self) -> None:
        self.manager.set_security_level(SSHSecurityLevel.BASIC)
        config = self.manager.generate_sshd_config()
        self.assertIn("PermitRootLogin prohibit-password", config)
        self.assertIn("PasswordAuthentication yes", config)

    def test_hardened_security_config(self) -> None:
        self.manager.set_security_level(SSHSecurityLevel.HARDENED)
        config = self.manager.generate_sshd_config()
        self.assertIn("PermitRootLogin no", config)
        self.assertIn("PasswordAuthentication no", config)
        self.assertIn("Ciphers chacha20-poly1305@openssh.com, aes256-gcm@openssh.com", config)

    def test_mfa_config_integration(self) -> None:
    # Check if MFA settings are reflected in the config
        self.manager.enable_mfa(True)
        config = self.manager.generate_sshd_config()

        self.assertIn("AuthenticationMethods publickey, keyboard-interactive", config)
        self.assertIn("KbdInteractiveAuthentication yes", config)
        self.assertIn("UsePAM yes", config)
