import time

from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import settings

# One client (with its own connection pool) per process. Short timeouts so a dead
# Redis fails fast instead of hanging requests.
redis = Redis.from_url(
    settings.redis_url,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
)

# Minimal circuit breaker. Without it, every request pays the full timeout while Redis
# is down ("cache outage = site-wide slowness"). After one failure we skip Redis for
# BREAKER_SECONDS, then try again.
BREAKER_SECONDS = 30
_open_until = 0.0


def _trip() -> None:
    global _open_until
    _open_until = time.monotonic() + BREAKER_SECONDS


async def cache_get(key: str) -> str | None:
    if time.monotonic() < _open_until:
        return None
    try:
        return await redis.get(key)
    except RedisError:
        _trip()
        return None


async def cache_set(key: str, value: str, ttl: int) -> None:
    if time.monotonic() < _open_until:
        return
    try:
        await redis.set(key, value, ex=ttl)
    except RedisError:
        _trip()
