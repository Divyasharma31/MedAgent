"""
llm/fake.py — FakeLLM implementation for tests and Phase 0.

FakeLLM never makes network calls.  It returns scripted responses that tests
inject via ``script``.  When no script matches, it returns a safe default.

Usage in tests::

    from app.llm.fake import FakeLLM
    llm = FakeLLM(script=[{"trigger": "headache", "response": '{"symptoms":[]}'}])
    response = llm.generate([Message(role="user", content="headache for 3 days")])
    assert "symptoms" in response.content
"""

from __future__ import annotations

import time
from typing import Any

from app.llm.base import LLMProvider, LLMResponse, Message


class FakeLLM:
    """
    Deterministic LLM stub — zero external calls, fully scriptable.

    Implements the ``LLMProvider`` protocol via duck typing (no inheritance
    needed because the protocol is structural / runtime-checkable).

    Parameters
    ----------
    script:
        Optional list of ``{"trigger": str, "response": str}`` dicts.
        The first entry whose ``trigger`` appears in the concatenated message
        content is returned.  If none matches, ``default_response`` is used.
    default_response:
        Returned when no script entry matches.
    model_name:
        Reported in ``LLMResponse.model`` for tracing.
    """

    def __init__(
        self,
        script: list[dict[str, str]] | None = None,
        default_response: str = '{"status": "ok", "data": "fake response"}',
        model_name: str = "fake-llm-v0",
    ) -> None:
        self._script: list[dict[str, str]] = script or []
        self._default = default_response
        self._model = model_name

    def generate(
        self,
        messages: list[Message],
        *,
        json_schema: dict[str, Any] | None = None,
        timeout: float = 30.0,
    ) -> LLMResponse:
        """
        Return a scripted response without any network or disk I/O.

        ``json_schema`` is accepted but ignored — tests that need JSON output
        should script the exact JSON string they want.
        ``timeout`` is accepted but ignored.
        """
        combined = " ".join(m.content for m in messages).lower()
        t0 = time.perf_counter()

        content = self._default
        for entry in self._script:
            if entry["trigger"].lower() in combined:
                content = entry["response"]
                break

        latency_ms = (time.perf_counter() - t0) * 1000

        return LLMResponse(
            content=content,
            model=self._model,
            provider="fake",
            usage={},
            latency_ms=latency_ms,
        )

    # ── Convenience helpers used in tests ────────────────────────────────────

    def add_script_entry(self, trigger: str, response: str) -> None:
        """Append a new scripted entry at runtime (useful in test fixtures)."""
        self._script.append({"trigger": trigger, "response": response})

    def clear_script(self) -> None:
        """Remove all scripted entries so only the default is returned."""
        self._script.clear()

    def set_default(self, response: str) -> None:
        """Replace the default response."""
        self._default = response


# Satisfy the LLMProvider protocol at import time so a bad signature is caught
# early (the runtime_checkable check below runs only once).
assert isinstance(FakeLLM(), LLMProvider), (
    "FakeLLM does not satisfy the LLMProvider protocol — check method signatures."
)

