"""
llm/base.py — LLMProvider protocol and shared data types.

Every agent imports only this module and the factory.  Concrete provider
implementations (gemini.py, groq.py, etc.) are added in Phase 1/2 once the
real provider is chosen (§16.1).

Design rules (§7):
- ``LLMProvider`` is a structural protocol (runtime-checkable).
- ``generate`` accepts a JSON schema so agents can request structured output.
- ``FakeLLM`` lives in fake.py and is the only implementation in Phase 0.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass
class Message:
    """A single turn in a conversation passed to an LLM."""

    role: str  # "system" | "user" | "assistant"
    content: str


@dataclass
class LLMResponse:
    """Typed return value from every provider's ``generate`` call."""

    content: str
    """Raw text content returned by the model."""

    model: str
    """The model identifier used for this call (for logging)."""

    provider: str
    """The provider name, e.g. 'fake', 'gemini'."""

    usage: dict[str, int] = field(default_factory=dict)
    """Token-usage metadata if the provider supplies it, else empty."""

    latency_ms: float = 0.0
    """Wall-clock time for this call in milliseconds."""


@runtime_checkable
class LLMProvider(Protocol):
    """
    Structural protocol that every LLM backend must satisfy.

    Agents depend only on this protocol.  The concrete class is injected
    via ``llm.factory.get_provider()``.
    """

    def generate(
        self,
        messages: list[Message],
        *,
        json_schema: dict[str, Any] | None = None,
        timeout: float = 30.0,
    ) -> LLMResponse:
        """
        Send ``messages`` to the model and return a typed response.

        Parameters
        ----------
        messages:
            Ordered list of conversation turns.
        json_schema:
            When provided, the provider should request structured JSON output
            matching this schema (best-effort; not all providers support it).
        timeout:
            Maximum seconds to wait before raising ``TimeoutError``.
        """
        ...

