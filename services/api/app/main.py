from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.cache import redis
from app.config import settings
from app.db import engine
from app.routes import health, notes


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    # Shutdown: close pools cleanly so ACA's scale-in / revision swap doesn't leave
    # half-open connections on Postgres (it has a hard connection limit on small SKUs).
    await redis.aclose()
    await engine.dispose()


app = FastAPI(title="sdlc-learn API", version=settings.app_version, lifespan=lifespan)
app.include_router(health.router)
app.include_router(notes.router)
