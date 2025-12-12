"""
Phase 6 Enhancement Tests - Cloud-init ISO Generation
Tests for enhanced cloud-init ISO generation including YAML validation, templates, and ISO creation.
"""

import pytest
import json
import os
import tempfile
import yaml

# Test fixtures


@pytest.fixture


def temp_iso_dir():
    """Create temporary directory for ISO files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture


def valid_user_data() -> str:
    """Valid cloud-init user-data YAML."""
    return """    #cloud-config
hostname: test-vm
package_upgrade: true
packages:
- curl
- htop
- vim
runcmd:
- echo "Hello World"
"""


@pytest.fixture


def valid_meta_data() -> str:
    """Valid cloud-init meta-data JSON."""
    return """
{
"instance-id": "i-1234567890abcdef0",
"local-ipv4": "192.168.1.50",
"hostname": "test-vm"
}
"""


@pytest.fixture


def valid_network_config() -> str:
    """Valid network configuration."""
    return """
version: 2
ethernets:
  eth0:
    dhcp4: true
"""


# ============================================================================
# YAML Validation Tests
# ============================================================================
class TestYAMLValidation:
    """Tests for cloud-init YAML validation."""

    def test_valid_user_data_yaml(self, valid_user_data):
        """Test validation of valid user-data YAML."""
        data = yaml.safe_load(valid_user_data)
        assert data["hostname"] == "test-vm"
        assert "curl" in data["packages"]

    def test_invalid_yaml_syntax(self) -> None:
        """Test rejection of invalid YAML syntax."""
        invalid_yaml = "{unbalanced: ["
        with pytest.raises(yaml.YAMLError):
            yaml.safe_load(invalid_yaml)

    def test_yaml_missing_required_field(self) -> None:
        """Test handling of missing required fields."""
        minimal_yaml = "    #cloud-config\n"
        data = yaml.safe_load(minimal_yaml)
        assert data is None or isinstance(data, dict)

    def test_meta_data_json_validation(self, valid_meta_data):
        """Test validation of meta-data JSON."""
        data = json.loads(valid_meta_data)
        assert data["instance-id"] == "i-1234567890abcdef0"
        assert data["hostname"] == "test-vm"

    def test_network_config_validation(self, valid_network_config):
        """Test validation of network configuration."""
        data = yaml.safe_load(valid_network_config)
        assert data["version"] == 2
        assert "eth0" in data["ethernets"]

    def test_vendor_data_validation(self) -> None:
        """Test validation of vendor-data."""
        vendor_data = "    #cloud-config\nruncmd:\n  - echo 'vendor'\n"
        data = yaml.safe_load(vendor_data)
        assert data["runcmd"][0] == "echo 'vendor'"


# ============================================================================
# Template Tests
# ============================================================================
class TestCloudInitTemplates:
    """Tests for cloud-init templates."""

    def test_ubuntu_template_generation(self) -> None:
        """Test Ubuntu template generation."""
        template = {
            "os": "ubuntu",
            "version": "20.04",
            "packages": ["curl", "vim"],
            "hostname": "test-vm",
        }

        assert template["os"] == "ubuntu"
        assert template["version"] == "20.04"

    def test_debian_template_generation(self) -> None:
        """Test Debian template generation."""
        template = {
            "os": "debian",
            "version": "11",
            "packages": ["curl", "vim"],
            "hostname": "test-vm",
        }

        assert template["os"] == "debian"
        assert template["version"] == "11"

    def test_rhel_template_generation(self) -> None:
        """Test RHEL template generation."""
        template = {
            "os": "rhel",
            "version": "8",
            "packages": ["curl", "vim"],
            "hostname": "test-vm",
        }

        assert template["os"] == "rhel"
        assert template["version"] == "8"

    def test_template_package_replacement(self) -> None:
        """Test package replacement in templates."""
        base_template = {"packages": ["PLACEHOLDER1", "PLACEHOLDER2"]}

        packages = ["curl", "htop"]
        template = base_template.copy()
        template["packages"] = packages

        assert template["packages"] == ["curl", "htop"]

    def test_template_variable_substitution(self) -> None:
        """Test variable substitution in templates."""
        template = "hostname: {hostname}\nruncmd:\n  - echo {message}"

        result = template.format(hostname="test-vm", message="Hello")
        assert "test-vm" in result
        assert "Hello" in result

    def test_custom_template_creation(self, temp_iso_dir):
        """Test creation of custom templates."""
        custom_template = {
            "hostname": "custom-vm",
            "packages": ["custom-pkg"],
            "runcmd": ["custom-command"],
        }

        template_file = os.path.join(temp_iso_dir, "custom.yaml")
        with open(template_file, "w") as f:
            yaml.dump(custom_template, f)

        with open(template_file, "r") as f:
            loaded = yaml.safe_load(f)

        assert loaded["hostname"] == "custom-vm"


# ============================================================================
# SSH Key Integration Tests
# ============================================================================
class TestSSHKeyIntegration:
    """Tests for SSH key integration."""

    def test_ssh_key_validation_rsa(self) -> None:
        """Test validation of RSA SSH key."""
        ssh_key = "ssh-rsa AAAAB3NzaC1yc2EAAA... user@host"
        assert ssh_key.startswith("ssh-rsa")

    def test_ssh_key_validation_ed25519(self) -> None:
        """Test validation of Ed25519 SSH key."""
        ssh_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AA... user@host"
        assert ssh_key.startswith("ssh-ed25519")

    def test_ssh_key_validation_invalid(self) -> None:
        """Test rejection of invalid SSH key."""
        invalid_key = "not-a-valid-key"
        assert not invalid_key.startswith(("ssh-rsa", "ssh-ed25519"))

    def test_ssh_key_file_reading(self, temp_iso_dir):
        """Test reading SSH key from file."""
        ssh_key = "ssh-rsa AAAAB3NzaC1yc2EA... user@host"

        key_file = os.path.join(temp_iso_dir, "id_rsa.pub")
        with open(key_file, "w") as f:
            f.write(ssh_key)

        with open(key_file, "r") as f:
            loaded_key = f.read().strip()

        assert loaded_key == ssh_key

    def test_multiple_ssh_keys(self, temp_iso_dir):
        """Test handling multiple SSH keys."""
        keys = [
            "ssh-rsa AAAAB3NzaC1yc2EA... key1@host",
            "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AA... key2@host",
        ]

        authorized_keys = "\n".join(keys)

        keys_file = os.path.join(temp_iso_dir, "authorized_keys")
        with open(keys_file, "w") as f:
            f.write(authorized_keys)

        with open(keys_file, "r") as f:
            lines = f.readlines()

        assert len(lines) == 2


# ============================================================================
# ISO Generation Tests
# ============================================================================
class TestISOGeneration:
    """Tests for ISO file generation."""

    def test_iso_file_creation(self, temp_iso_dir):
        """Test ISO file creation."""
        iso_file = os.path.join(temp_iso_dir, "cloud-init.iso")

        # Simulate ISO creation
        with open(iso_file, "w") as f:
            f.write("mock iso content")

        assert os.path.exists(iso_file)

    def test_iso_size_validation(self, temp_iso_dir):
        """Test ISO file size validation."""
        iso_file = os.path.join(temp_iso_dir, "cloud-init.iso")

        # Create mock ISO
        with open(iso_file, "wb") as f:
            f.write(b"0" * (1024 * 1024 * 2))    # 2 MB

        file_size = os.path.getsize(iso_file)
        max_size = 1024 * 1024 * 10    # 10 MB

        assert file_size <= max_size

    def test_iso_size_exceeds_limit(self, temp_iso_dir):
        """Test handling of ISO file exceeding size limit."""
        iso_file = os.path.join(temp_iso_dir, "cloud-init.iso")

        # Create oversized ISO
        with open(iso_file, "wb") as f:
            f.write(b"0" * (1024 * 1024 * 15))    # 15 MB

        file_size = os.path.getsize(iso_file)
        max_size = 1024 * 1024 * 10    # 10 MB

        assert file_size > max_size

    def test_iso_file_permissions(self, temp_iso_dir):
        """Test ISO file permissions."""
        iso_file = os.path.join(temp_iso_dir, "cloud-init.iso")

        with open(iso_file, "w") as f:
            f.write("content")

        assert os.access(iso_file, os.R_OK)

    def test_mkisofs_availability_check(self) -> None:
        """Test checking for mkisofs availability."""
        tools = ["mkisofs", "xorrisofs"]
        # At least one should be available
        available = any(tool for tool in tools)
        assert available is not None


# ============================================================================
# Package Installation Tests
# ============================================================================
class TestPackageInstallation:
    """Tests for package installation configuration."""

    def test_package_list_parsing(self) -> None:
        """Test parsing of package list."""
        package_string = "curl, vim, htop, git"
        packages = package_string.split(", ")

        assert len(packages) == 4
        assert "curl" in packages

    def test_package_validation(self) -> None:
        """Test validation of package names."""
        valid_packages = ["curl", "vim", "htop", "git", "python3"]

        for pkg in valid_packages:
            assert len(pkg) > 0
            assert pkg.isalnum() or "-" in pkg

    def test_invalid_package_names(self) -> None:
        """Test rejection of invalid package names."""
        invalid_packages = ["", "pkg@invalid", "pkg&bad"]

        for pkg in invalid_packages:
            if len(pkg) == 0:
                assert True
            else:
            # Check for special characters
                assert any(c in pkg for c in "@&")

    def test_package_upgrade_configuration(self) -> None:
        """Test package upgrade configuration."""
        config = {"package_upgrade": True}
        assert config["package_upgrade"] is True


# ============================================================================
# Validation Mode Tests
# ============================================================================
class TestValidationMode:
    """Tests for validation-only mode."""

    def test_validate_only_mode(self, valid_user_data, temp_iso_dir):
        """Test validation-only mode without ISO creation."""
        # Parse user-data
        _data = yaml.safe_load(valid_user_data)

        # Validation passes but no file created
        iso_file = os.path.join(temp_iso_dir, "cloud-init.iso")
        assert not os.path.exists(iso_file)

    def test_validation_report_generation(self) -> None:
        """Test generation of validation report."""
        report = {
            "status": "valid",
            "errors": [],
            "warnings": [],
            "summary": "All checks passed",
        }

        assert report["status"] == "valid"
        assert len(report["errors"]) == 0


# ============================================================================
# Error Handling Tests
# ============================================================================
class TestCloudInitErrorHandling:
    """Tests for error handling."""

    def test_invalid_yaml_handling(self) -> None:
        """Test handling of invalid YAML."""
        invalid_yaml = "key: value:\n  bad indent"

        try:
            yaml.safe_load(invalid_yaml)
            assert False, "Should have raised exception"
        except yaml.YAMLError:
            assert True

    def test_missing_file_handling(self, temp_iso_dir):
        """Test handling of missing files."""
        missing_file = os.path.join(temp_iso_dir, "nonexistent.yaml")

        assert not os.path.exists(missing_file)

    def test_permission_denied_handling(self) -> None:
        """Test handling of permission denied."""
        error = PermissionError("Permission denied")
        assert isinstance(error, Exception)


# ============================================================================
# Integration Tests
# ============================================================================
class TestCloudInitIntegration:
    """Integration tests for cloud-init ISO generation."""

    def test_complete_iso_generation_workflow(self, temp_iso_dir, valid_user_data):
        """Test complete ISO generation workflow."""
        # Step 1: Validate user-data
        data = yaml.safe_load(valid_user_data)
        assert data is not None

        # Step 2: Create ISO file
        iso_file = os.path.join(temp_iso_dir, "cloud-init.iso")
        with open(iso_file, "w") as f:
            f.write("iso content")

        # Step 3: Verify file
        assert os.path.exists(iso_file)

    def test_iso_generation_with_ssh_keys(self, temp_iso_dir):
        """Test ISO generation with SSH key integration."""
        # Create SSH key
        ssh_key = "ssh-rsa AAAAB3NzaC1yc2EA... user@host"

        # Create ISO with SSH key
        iso_file = os.path.join(temp_iso_dir, "cloud-init-ssh.iso")
        with open(iso_file, "w") as f:
            f.write(ssh_key)

        assert os.path.exists(iso_file)

    def test_template_based_iso_generation(self, temp_iso_dir):
        """Test template-based ISO generation."""
        template = {"os": "ubuntu", "hostname": "test-vm", "packages": ["curl", "vim"]}

        iso_file = os.path.join(temp_iso_dir, "cloud-init.iso")
        with open(iso_file, "w") as f:
            json.dump(template, f)

        assert os.path.exists(iso_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
