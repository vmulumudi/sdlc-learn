from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All config comes from environment variables (12-factor).

    Locally: compose.yaml sets them. In Azure: Container App env vars / Key Vault refs.
    The defaults only work against the local compose stack.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://app:app-local-only@localhost:5432/sdlc"
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_seconds: int = 60
    # Stamped in by CI/CD at build/deploy time; /healthz reports them so a smoke
    # test can prove *which* build is actually serving traffic.
    app_version: str = "0.0.0-local"
    git_sha: str = "unknown"


settings = Settings()
