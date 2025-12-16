# Improvements: `agent_backend.py`

## Fixed
- Add unit tests for `llm_chat_via_github_models` (mocking requests). (Fixed) [2025-12-16]
  * TestGitHubModelsRetry: 2 tests for retry logic and auth error handling
- Add retry logic for network requests. (Fixed) [2025-12-16]
  * Exponential backoff with configurable max retries (default 2)
  * Retry only on transient errors (Timeout, ConnectionError), not auth errors
  * Comprehensive error categorization and logging
- Add environment variable handling tests. (Fixed) [2025-12-16]
  * TestEnvironmentVariableHandling: 3 tests for backend selection and configuration
- Add comprehensive error logging without token leakage. (Fixed) [2025-12-16]
  * TestErrorLogging: 2 tests for error context and security

## Suggested improvements
- [ ] Support streaming responses.
- [ ] Add cost estimation for API-based backends (track tokens, calculate cost).
- [ ] Implement graceful degradation: fall back to local models if API unavailable.
- [ ] Add response validation: ensure AI output contains expected content types.
- [ ] Cache responses for identical prompts across runs.
- [ ] Add integration tests with real GitHub Models API.
- [ ] Support custom model endpoints and authentication methods.
- [ ] Add metrics collection: request count, latency, error rates per backend.
- [ ] Implement circuit breaker pattern for failing backends.
- [ ] Add timeout configuration per backend type.
