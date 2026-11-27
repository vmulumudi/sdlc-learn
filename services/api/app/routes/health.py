import asyncio

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.cache import redis
from app.config import settings
from app.db import engine

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    """Liveness: "is the process alive?" Checks NO dependencies.

    If this checked Postgres, a DB blip would make ACA restart every replica in a loop,
    which fixes nothing and makes the outage worse.
    """
    return {"status": "ok", "version": settings.app_version, "commit": settings.git_sha}


@router.get("/readyz")
async def readyz() -> JSONResponse:
    """Readiness: "should this replica receive traffic?" Fails only on HARD dependencies.

    Postgres is hard (no data, no API). Redis is a cache: reported, but never fails
    readiness, because the API still works (slower) without it.
    """
    checks: dict[str, str] = {}
    try:
        async with asyncio.timeout(2):
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except Exception as exc:  # noqa: BLE001 - report any failure, never crash the probe
        checks["postgres"] = f"error: {type(exc).__name__}"
    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["redis"] = f"degraded: {type(exc).__name__}"

    ready = checks["postgres"] == "ok"
    return JSONResponse(
        {"status": "ready" if ready else "not-ready", "checks": checks},
        status_code=200 if ready else 503,
    )
