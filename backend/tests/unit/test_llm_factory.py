"""
tests/unit/test_llm_factory.py — Tests for llm/factory.py.

Phase 0 checklist item: "Tests: factory returns FakeLLM".
"""

from __future__ import annotations

import pytest

from app.core.errors import ProviderNotFoundError
from app.llm.base import LLMProvider
from app.llm.factory import get_provider
from app.llm.fake import FakeLLM


class TestGetProvider:
    def test_fake_provider_returned_by_default(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LLM_PROVIDER", "fake")
        # Re-import settings so monkeypatch takes effect.
        import importlib
        import app.core.config as cfg_mod

        importlib.reload(cfg_mod)
        import app.llm.factory as factory_mod

        importlib.reload(factory_mod)
        provider = factory_mod.get_provider()
        assert isinstance(provider, FakeLLM)

    def test_returned_provider_satisfies_protocol(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LLM_PROVIDER", "fake")
        import importlib
        import app.core.config as cfg_mod

        importlib.reload(cfg_mod)
        import app.llm.factory as factory_mod

        importlib.reload(factory_mod)
        provider = factory_mod.get_provider()
        assert isinstance(provider, LLMProvider)

    def test_unknown_provider_raises(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LLM_PROVIDER", "not_a_real_provider")
        import importlib
        import app.core.config as cfg_mod

        importlib.reload(cfg_mod)
        import app.llm.factory as factory_mod

        importlib.reload(factory_mod)
        with pytest.raises(ProviderNotFoundError):
            factory_mod.get_provider()

