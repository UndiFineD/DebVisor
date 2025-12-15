# Changelog

- 2025-12-15: Added utilities for legacy agent tests (safe path-loading of agent modules, including hyphenated filenames).

## [2025-12-15]
- Added detailed logging for module loading.
- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports. (Fixed)
