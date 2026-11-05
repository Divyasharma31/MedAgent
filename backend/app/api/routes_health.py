"""
api/routes_health.py — /health endpoint.

Returns the application's current status and the configured LLM provider.
No medical content, no agent calls, no database access in Phase 0.
"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    llm_provider: str
    app_env: str
    phase: str


@router.get("/health", response_model=HealthResponse, summary="Liveness check")
def health() -> HealthResponse:
    """
    Returns 200 when the service is running.

    - ``status``: always ``"ok"`` if the service is reachable.
    - ``llm_provider``: the configured provider (e.g. ``"fake"``).
    - ``app_env``: ``"development"`` or ``"production"``.
    - ``phase``: the current implementation phase.
    """
    return HealthResponse(
        status="ok",
        llm_provider=settings.llm_provider,
        app_env=settings.app_env,
        phase="0-foundations",
    )

