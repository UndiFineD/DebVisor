"""Compatibility package.

The codebase stores runtime modules under `opt/`.
Tests and some tooling import `services.*`, so this package provides a stable
import path that re-exports those modules.
"""
