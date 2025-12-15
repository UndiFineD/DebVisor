# Improvements for `agent_test_utils.py`

● I'll analyze the current state of `agent_test_utils.py` and improve the improvement suggestions
   by examining the actual code.

● Now let me check how this utility is being used in test files to provide more context-aware
   improvements:

● Now let me check if there are any environment variables being used in the tests:

● Let me use the create approach since I need write permissions:

● I cannot make file modifications due to permission restrictions. Let me provide you with the
   improved improvements content that should replace the current file:

   ## Enhanced Improvements for `agent_test_utils.py`

   Here's a comprehensive, actionable improvement document:

   ---

   # Improvements: `agent_test_utils.py`

   ## High-Priority Improvements

   ### 1. Add Module Docstring
   **Impact**: Documentation & Maintainability
   **Effort**: Low

   Add a comprehensive module-level docstring explaining:
   - Purpose: utilities for testing agent scripts with non-standard filenames (e.g.,
   `agent-changes.py`)
   - Key functions: `agent_dir_on_path()` and `load_agent_module()`
   - Usage patterns with examples
   - Why `sys.path` manipulation is necessary (hyphenated filenames)

   **Example**:
   ```python
   """Test utilities for DebVisor agent scripts.

   Provides helpers for testing agent modules with non-standard Python filenames
   (e.g., `agent-changes.py`, `agent-coder.py`).

   Key utilities:
   - `agent_dir_on_path()`: Context manager to temporarily add agent dir to sys.path
   - `load_agent_module()`: Load agent modules by filename, handling invalid identifiers

   Example:
       with agent_dir_on_path():
           mod = load_agent_module("agent-changes.py")
           agent = mod.ChangesAgent("output.md")
   """
   ```

   ### 2. Add Environment Isolation Helper ⚠️ **CRITICAL**
   **Impact**: Test Reliability
   **Effort**: Medium
   **Priority**: High (prevents test pollution)

   Currently, only `test_base_agent.py` explicitly cleans environment variables with
   `monkeypatch.delenv()`. Other tests inherit `DV_AGENT_*` and `GITHUB_*` variables from the
   developer's shell, causing inconsistent behavior.

   **Add this context manager/fixture**:
   ```python
   @contextmanager
   def isolated_agent_env(clean_vars: bool = True, **overrides):
       """Isolate agent environment variables for testing.

       Args:
           clean_vars: If True, temporarily remove all DV_AGENT_* and GITHUB_* vars
           **overrides: Environment variables to set during the test

       Example:
           with isolated_agent_env(DV_AGENT_BACKEND="copilot"):
               agent.run()  # Runs with clean env + only specified vars
       """
       import os
       agent_prefixes = ("DV_AGENT_", "GITHUB_")
       saved_env = {}

       if clean_vars:
           for key in list(os.environ.keys()):
               if any(key.startswith(prefix) for prefix in agent_prefixes):
                   saved_env[key] = os.environ.pop(key)

       for key, value in overrides.items():
           saved_env.setdefault(key, os.environ.get(key))
           os.environ[key] = value

       try:
           yield
       finally:
           for key in overrides:
               if saved_env.get(key) is None:
                   os.environ.pop(key, None)
               else:
                   os.environ[key] = saved_env[key]

           if clean_vars:
               for key, value in saved_env.items():
                   if key not in overrides:
                       os.environ[key] = value
   ```

   **Affected variables**: `DV_AGENT_BACKEND`, `DV_AGENT_MODEL`, `DV_AGENT_VERBOSITY`,
   `DV_AGENT_MAX_CONTEXT_CHARS`, `DV_AGENT_REPO_ROOT`, `DV_AGENT_SYSTEM_PROMPT`, `GITHUB_TOKEN`,
   `GITHUB_MODELS_BASE_URL`, `GITHUB_MODELS_MODEL`

   ### 3. Add Logging/Diagnostics to `load_agent_module()`
   **Impact**: Debuggability
   **Effort**: Low

   ```python
   def load_agent_module(filename: str, module_name: str | None = None,
                         verbose: bool = False) -> ModuleType:
       """Load an agent module from scripts/agent by filename.

       Args:
           verbose: If True, print diagnostic info about module loading
       """
       path = AGENT_DIR / filename
       if verbose:
           print(f"[load_agent_module] Loading: {path}")

       if not path.exists():
           if verbose:
               available = [f.name for f in AGENT_DIR.glob("agent*.py") if not
   f.name.startswith("test_")]
               print(f"[load_agent_module] Available: {available[:5]}")
           raise FileNotFoundError(path)

       # ... rest with additional diagnostics
   ```

   ## Medium-Priority Improvements

   ### 4. Enhance Error Messages
   **Impact**: Developer Experience
   **Effort**: Low

   ```python
   if not path.exists():
       available = [f.name for f in AGENT_DIR.glob("*.py") if not f.name.startswith("test_")]
       raise FileNotFoundError[:5](
           f"Agent module not found: {filename}\n"
           f"  Path: {path}\n"
           f"  Available modules: {', '.join(sorted(available))}..."
       )

   if spec is None or spec.loader is None:
       raise RuntimeError(
           f"Unable to load spec for {path}\n"
           f"  This may indicate a syntax error or invalid Python file."
       )
   ```

   ### 5. Add Module Caching (Optional)
   **Impact**: Performance (test suite speedup)
   **Effort**: Medium

   ```python
   _MODULE_CACHE: dict[str, ModuleType] = {}

   def load_agent_module(filename: str, module_name: str | None = None,
                         use_cache: bool = False) -> ModuleType:
       """Load an agent module, optionally from cache."""
       if use_cache and filename in _MODULE_CACHE:
           return _MODULE_CACHE[filename]

       # ... existing load logic ...

       if use_cache:
           _MODULE_CACHE[filename] = module
       return module

   def clear_module_cache():
       """Clear the module cache (useful between test runs)."""
       _MODULE_CACHE.clear()
   ```

   ## Low-Priority / Architectural Considerations

   ### 6. Regarding `sys.path` Manipulation
   **Status**: Keep current approach ✅

   The suggestion to "avoid `sys.path.insert(...)`" is **not applicable** here because:

   1. **Hyphenated filenames**: `agent-changes.py`, `agent-errors.py` are NOT valid Python
   identifiers
   2. **Standalone scripts**: These are CLI tools, not a traditional package
   3. **Context manager provides safety**: `agent_dir_on_path()` properly cleans up `sys.path`
   4. **Widely used**: 10 test modules depend on this pattern

   **Alternative approaches considered** (all inferior):
   - Rename to `agent_changes.py` → Breaks CLI conventions/backwards compatibility
   - Full package restructure → Excessive for standalone scripts
   - `runpy.run_path()` → Loses module caching and import semantics

   **Recommendation**: Document WHY `sys.path` manipulation is necessary in module docstring (see
   #1).

   ### 7. Consider Pytest Plugin (Future)
   **Effort**: High

   If this pattern grows, consider a `conftest.py` pytest plugin that provides:
   - `@pytest.fixture` for `agent_dir_on_path`
   - `@pytest.fixture` for `isolated_agent_env`
   - Auto-discovery of agent modules

   ## Testing Recommendations

   Add tests for the utilities themselves:
   ```python
   # test_agent_test_utils.py
   def test_isolated_agent_env_cleans_up_on_exception():
       os.environ["DV_AGENT_TEST"] = "value"
       with pytest.raises(RuntimeError):
           with isolated_agent_env(clean_vars=True):
               os.environ["DV_AGENT_TEST2"] = "temp"
               raise RuntimeError("test")
       assert "DV_AGENT_TEST" not in os.environ
       assert "DV_AGENT_TEST2" not in os.environ

   def test_load_agent_module_with_invalid_filename():
       with pytest.raises(FileNotFoundError, match="nonexistent"):
           load_agent_module("nonexistent.py")
   ```

   ## Summary

   | Priority | Improvement | Impact | Effort |
   |----------|-------------|--------|--------|
   | **HIGH** | Environment isolation helper | Prevent test pollution | Medium |
   | **HIGH** | Module docstring | Clarity & maintainability | Low |
   | Medium | Enhanced error messages | Developer experience | Low |
   | Medium | Diagnostic logging | Debuggability | Low |
   | Low | Module caching | Performance (minor) | Medium |

   ## Notes
   - **File**: `scripts/agent/agent_test_utils.py`
   - **Last reviewed**: 2025-12-15
   - **Current usage**: 10 test modules (`test_agent-*.py`, `test_base_agent.py`)
   - **Current issues**: No critical bugs, but environment isolation is a testing best practice gap

   ---

   The key improvements focus on:
   1. **Test isolation** (environment variables) - most critical
   2. **Documentation** (module docstring explaining design choices)
   3. **Debuggability** (better error messages and optional logging)

   The original suggestion to avoid `sys.path` manipulation has been **reframed** as "document why
   it's necessary" rather than removed, since it's a pragmatic solution for the hyphenated filename
    problem.
