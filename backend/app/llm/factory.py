"""
llm/factory.py — Provider factory.

Returns the ``LLMProvider`` instance for the configured ``LLM_PROVIDER``.
Agents call ``get_provider()`` once at startup or per-request; they never
import concrete provider classes directly.

Phase 0: only 'fake' is wired.  Real adapters (gemini, groq, openrouter,
ollama) are added in Phase 1/2 once §16.1 is resolved.
"""

from __future__ import annotations

from app.core.config import settings
from app.core.errors import ProviderNotFoundError
from app.llm.base import LLMProvider


def get_provider() -> LLMProvider:
    """
    Return a ready-to-use ``LLMProvider`` based on ``settings.llm_provider``.

    Raises
    ------
    ProviderNotFoundError
        When ``settings.llm_provider`` is not recognised.
    """
    provider_name = settings.llm_provider.lower().strip()

    if provider_name == "fake":
        from app.llm.fake import FakeLLM

        return FakeLLM()

    # ── Real providers: added in Phase 1/2 after §16.1 is decided ────────────
    # if provider_name == "gemini":
    #     from app.llm.gemini import GeminiProvider
    #     return GeminiProvider()
    #
    # if provider_name == "groq":
    #     from app.llm.groq import GroqProvider
    #     return GroqProvider()
    #
    # if provider_name == "openrouter":
    #     from app.llm.openrouter import OpenRouterProvider
    #     return OpenRouterProvider()
    #
    # if provider_name == "ollama":
    #     from app.llm.ollama import OllamaProvider
    #     return OllamaProvider()

    raise ProviderNotFoundError(
        f"Unknown LLM_PROVIDER value: '{provider_name}'.  "
        f"Allowed values in Phase 0: fake.  "
        f"Real providers are added in Phase 1/2 after the provider decision."
    )

