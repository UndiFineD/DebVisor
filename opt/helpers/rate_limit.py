import time
import os
from typing import Callable, Any, Dict

try:
    import redis

    _HAS_REDIS = True
except Exception:
    _HAS_REDIS = False


class _InMemoryStore:
    def __init__(self) -> None:
        self.store: Dict[str, Dict[str, int]] = {}

    def incr(self, key: str) -> int:
        now = int(time.time())
        bucket = self.store.setdefault(key, {"count": 0, "ts": now})
        if bucket["ts"] != now:
            bucket["count"] = 0
            bucket["ts"] = now
        bucket["count"] += 1
        return bucket["count"]

    def get(self, key: str) -> Dict[str, int]:
        return self.store.get(key, {"count": 0, "ts": int(time.time())})


def _get_client() -> Any:
    if _HAS_REDIS:
        url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            return redis.Redis.from_url(url)
        except Exception:
            pass  # nosec B110
    return _InMemoryStore()


def sliding_window_limiter(
    identifier_func: Callable[[], str], limit: int, window_seconds: int
) -> Callable[..., Any]:
    """Decorator implementing a simple sliding window rate limiter.

    identifier_func: returns a string key (e.g., IP or username)
    limit: max requests per window
    window_seconds: size of window in seconds
    """
    client = _get_client()

    def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        from functools import wraps
        from flask import jsonify

        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = identifier_func()
            now = int(time.time())
            bucket_key = f"rl:{key}:{now // window_seconds}"

            try:
                count = (
                    client.incr(bucket_key)
                    if isinstance(client, _InMemoryStore)
                    else client.incr(bucket_key)
                )
            except Exception:
                count = 0

            if count > limit:
                return (
                    jsonify(
                        {
                            "error": "Rate limit exceeded",
                            "identifier": key,
                            "limit": limit,
                            "window_seconds": window_seconds,
                        }
                    ),
                    429,
                )
            return f(*args, **kwargs)

        return wrapper

    return decorator
