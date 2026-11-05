"""
tests/unit/test_config.py — Tests for core/config.py.

Phase 0 checklist item: "Tests: config loads".
"""

from __future__ import annotations

import os

import pytest

from app.core.config import Settings


class TestSettingsDefaults:
    """Settings constructed with no environment variables set."""

    def test_llm_provider_default(self) -> None:
        s = Settings()
        assert s.llm_provider == "fake"

    def test_app_env_default(self) -> None:
        s = Settings()
        assert s.app_env == "development"

    def test_log_level_default(self) -> None:
        s = Settings()
        assert s.log_level == "INFO"

    def test_block_on_identifier_default(self) -> None:
        s = Settings()
        assert s.block_on_identifier is True

    def test_optional_keys_are_none(self) -> None:
        s = Settings()
        assert s.gemini_api_key is None
        assert s.groq_api_key is None
        assert s.openrouter_api_key is None
        assert s.database_url is None


class TestSettingsFromEnv:
    """Settings reads values from environment variables."""

    def test_llm_provider_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("LLM_PROVIDER", "fake")
        s = Settings()
        assert s.llm_provider == "fake"

    def test_log_level_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        s = Settings()
        assert s.log_level == "DEBUG"

    def test_block_on_identifier_false(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("BLOCK_ON_IDENTIFIER", "false")
        s = Settings()
        assert s.block_on_identifier is False

