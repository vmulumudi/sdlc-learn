# ---- build stage: resolve and install dependencies into /app/.venv ----
FROM python:3.12-slim AS build
# Copy the uv binary from its official image instead of pip-installing it.
COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /usr/local/bin/uv
# COMPILE_BYTECODE: faster cold start (matters for ACA scale-from-zero).
# LINK_MODE=copy: real files in the venv, so it survives the COPY to the next stage.
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app
# Lockfiles first, source later: the slow dependency layer is cached until uv.lock changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .

# ---- runtime stage: no uv, no build tools, non-root ----
FROM python:3.12-slim
RUN useradd --create-home --uid 10001 app
WORKDIR /app
COPY --from=build --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
USER 10001
EXPOSE 8000
# Same image runs the API (default) or migrations (`alembic upgrade head`, as an ACA Job).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
