"""
app/main.py — FastAPI application entry point.

Phase 0: mounts only the /health router.
Later phases register additional routers (chat, documents) without changing
this file's structure.

Startup behaviour:
- Logging is configured first.
- The LLM provider is instantiated to validate the LLM_PROVIDER setting and
  fail fast if the value is unknown.  In Phase 0 this means confirming that
  'fake' resolves correctly.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.core.config import settings
from app.core.errors import CDSSError
from app.core.logging import configure_logging, get_logger
from app.llm.factory import get_provider

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    """Run startup and shutdown logic."""
    configure_logging()
    logger.info("Starting Healthcare CDSS — Phase 0 (Foundations)")
    logger.info("LLM provider: %s | env: %s", settings.llm_provider, settings.app_env)

    # Fail fast if the provider is misconfigured.
    try:
        provider = get_provider()
        logger.info("LLM provider instantiated: %s", type(provider).__name__)
    except CDSSError as exc:
        logger.critical("Failed to instantiate LLM provider: %s", exc)
        raise

    yield

    logger.info("Shutting down Healthcare CDSS")


app = FastAPI(
    title="Healthcare CDSS",
    description=(
        "Agentic Clinical Decision Support System — academic research prototype. "
        "NOT for clinical use. Synthetic data only."
    ),
    version="0.0.1",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(health_router)
# Phase 2+: app.include_router(chat_router, prefix="/api/v1")
# Phase 4+: app.include_router(documents_router, prefix="/api/v1")

