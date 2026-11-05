"""
core/config.py — Application settings loaded from environment / .env file.

Phase 0: only the settings that Phase 0 actually uses are present.
Later phases will extend this module; they must not break existing fields.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration object.  Values are loaded from environment variables
    or from a ``.env`` file in the working directory (lowest priority).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── LLM provider ──────────────────────────────────────────────────────────
    llm_provider: str = Field(
        default="fake",
        description=(
            "Which LLM backend to use.  "
            "Allowed: fake | gemini | groq | openrouter | ollama.  "
            "Phase 0 default is 'fake' (no external calls)."
        ),
    )

    # ── Application ───────────────────────────────────────────────────────────
    app_env: str = Field(default="development")
    log_level: str = Field(default="INFO")

    # ── Privacy ───────────────────────────────────────────────────────────────
    block_on_identifier: bool = Field(
        default=True,
        description=(
            "When True, requests containing obvious personal identifiers "
            "(phone, email, long digit strings) are blocked before any "
            "external LLM call."
        ),
    )

    # ── API keys (all optional; only needed when a real provider is chosen) ───
    # Added here as optional so the config object can carry them once decided.
    # Phase 0: these are never read because llm_provider == 'fake'.
    gemini_api_key: str | None = Field(default=None)
    groq_api_key: str | None = Field(default=None)
    openrouter_api_key: str | None = Field(default=None)
    ollama_base_url: str = Field(default="http://localhost:11434")

    # ── Database (Phase 2+) ───────────────────────────────────────────────────
    database_url: str | None = Field(default=None)

    # ── ChromaDB (Phase 1+) ───────────────────────────────────────────────────
    chroma_path: str = Field(default="./data/chroma")


# Module-level singleton — import and use ``settings`` everywhere.
settings = Settings()

