# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:0.12 AS uv

# ---------- base: deps installed with uv from the lockfile ----------
FROM python:3.14-slim AS base
COPY --from=uv /uv /usr/local/bin/uv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 10001 --create-home app \
    && mkdir -p /models-cache && chown app /models-cache
WORKDIR /app
COPY pyproject.toml uv.lock ./

# ---------- dev: dev deps + hot reload on mounted sources ----------
FROM base AS dev
RUN uv sync --frozen
COPY app/ app/
USER app
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=5 \
  CMD curl -fs http://localhost:8000/health || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---------- prod ----------
FROM base AS prod
RUN uv sync --frozen --no-dev
COPY app/ app/
USER app
EXPOSE 8000
ENV AI_ENV=prod
HEALTHCHECK --interval=15s --timeout=3s --start-period=30s --retries=5 \
  CMD curl -fs http://localhost:8000/health || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
