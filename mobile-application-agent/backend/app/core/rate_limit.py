from collections import defaultdict
from time import monotonic


class RateLimiter:
    def __init__(self) -> None:
        self._requests: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str, limit: int) -> bool:
        now = monotonic()
        recent = [stamp for stamp in self._requests[key] if now - stamp < 60]
        self._requests[key] = recent
        if len(recent) >= limit:
            return False
        recent.append(now)
        return True


rate_limiter = RateLimiter()
