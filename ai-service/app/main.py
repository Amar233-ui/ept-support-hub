"""EPT Support Hub AI service.

Internal only: called by the backend, never exposed through the public reverse proxy.
Endpoints planned (see docs/ai.md): /classify, /suggest-assignee, /correlate, /transcribe,
/embeddings/reindex.
"""

from fastapi import FastAPI

from app import __version__
from app.config import get_settings
from app.routers import health

settings = get_settings()

app = FastAPI(
    title="EPT Support Hub — AI service",
    version=__version__,
    # Interactive docs only in dev.
    docs_url="/docs" if settings.env == "dev" else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.env == "dev" else None,
)

app.include_router(health.router)
