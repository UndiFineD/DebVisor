"""
Tests for Hypervisor CLI Xen Support.
"""
from unittest.mock import patch, MagicMockfrom opt.hvctl_enhanced import HypervisorCLI


@patch("subprocess.run")
def test_xen_connection_uri(mock_run):
    cli = HypervisorCLI(dry_run=False, verbose=True, hypervisor="xen")

    # Mock successful execution
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

    cli.list_vms()

    # Verify virsh was called with -c xen:///system
    args, _ = mock_run.call_args
    cmd = args[0]
    assert cmd[0] == "virsh"
    assert cmd[1] == "-c"
    assert cmd[2] == "xen:///system"


@patch("subprocess.run")
def test_kvm_default_uri(mock_run):
    cli = HypervisorCLI(dry_run=False, verbose=True, hypervisor="kvm")

    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

    cli.list_vms()

    args, _ = mock_run.call_args
    cmd = args[0]
    assert cmd[0] == "virsh"
    assert cmd[1] == "-c"
    assert cmd[2] == "qemu:///system"
