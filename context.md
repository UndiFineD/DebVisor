# DebVisor Context

## Structure

Tab size is 4 spaces

## Overall Purpose

DebVisor is a Debian 13-based mini hyper-converged hypervisor distro.
It is containers-first (Docker/Kubernetes), with VMs supported for
legacy and special-case workloads. The goal is a turnkey ISO that you
boot, install via a curses (ncurses) installer, and end up with:
KVM/libvirt + bridges + Cockpit web UI
CephFS-first (with optional ZFS or mixed Ceph+ZFS)
Docker + Kubernetes (kubeadm, containerd, Calico)
Opinionated defaults and automated first-boot provisioning.
Key entry points:
README.md - high-level description, profiles, and ISO build quickstart.
Makefile + build-debvisor.sh - one-shot live-build wrapper to produce the ISO.
DebVisor_initial.md - now just a stub table listing canonical file locations.

## Installer & Image Build
