"""
tests/unit/test_fake_llm.py — Tests for llm/fake.py.

Phase 0 checklist item: "Tests: FakeLLM returns scripted output".
"""

from __future__ import annotations

from app.llm.base import LLMProvider, Message
from app.llm.fake import FakeLLM


class TestFakeLLMProtocol:
    def test_satisfies_llm_provider_protocol(self) -> None:
        assert isinstance(FakeLLM(), LLMProvider)


class TestFakeLLMGenerate:
    def test_returns_default_response_when_no_script(self) -> None:
        llm = FakeLLM(default_response="default answer")
        response = llm.generate([Message(role="user", content="hello")])
        assert response.content == "default answer"

    def test_scripted_trigger_matched_case_insensitive(self) -> None:
        llm = FakeLLM(
            script=[{"trigger": "headache", "response": '{"symptoms": ["headache"]}'}]
        )
        response = llm.generate(
            [Message(role="user", content="I have a Headache for 3 days")]
        )
        assert response.content == '{"symptoms": ["headache"]}'

    def test_first_matching_trigger_wins(self) -> None:
        llm = FakeLLM(
            script=[
                {"trigger": "fever", "response": "fever response"},
                {"trigger": "headache", "response": "headache response"},
            ]
        )
        # Both triggers present — first entry wins.
        response = llm.generate(
            [Message(role="user", content="I have fever and headache")]
        )
        assert response.content == "fever response"

    def test_no_match_returns_default(self) -> None:
        llm = FakeLLM(
            script=[{"trigger": "fever", "response": "fever response"}],
            default_response="fallback",
        )
        response = llm.generate([Message(role="user", content="something else")])
        assert response.content == "fallback"

    def test_response_has_correct_provider_and_model(self) -> None:
        llm = FakeLLM(model_name="test-model")
        response = llm.generate([Message(role="user", content="hi")])
        assert response.provider == "fake"
        assert response.model == "test-model"

    def test_latency_ms_is_non_negative(self) -> None:
        llm = FakeLLM()
        response = llm.generate([Message(role="user", content="hi")])
        assert response.latency_ms >= 0.0

    def test_multiple_messages_concatenated_for_matching(self) -> None:
        llm = FakeLLM(
            script=[{"trigger": "chest pain", "response": "emergency"}]
        )
        messages = [
            Message(role="system", content="You are an assistant."),
            Message(role="user", content="I have chest pain"),
        ]
        response = llm.generate(messages)
        assert response.content == "emergency"

    def test_add_script_entry_at_runtime(self) -> None:
        llm = FakeLLM()
        llm.add_script_entry("asthma", "asthma response")
        response = llm.generate([Message(role="user", content="asthma attack")])
        assert response.content == "asthma response"

    def test_clear_script_reverts_to_default(self) -> None:
        llm = FakeLLM(
            script=[{"trigger": "fever", "response": "fever response"}],
            default_response="fallback",
        )
        llm.clear_script()
        response = llm.generate([Message(role="user", content="fever")])
        assert response.content == "fallback"

    def test_set_default_changes_default_response(self) -> None:
        llm = FakeLLM(default_response="old")
        llm.set_default("new default")
        response = llm.generate([Message(role="user", content="nothing matches")])
        assert response.content == "new default"

    def test_json_schema_accepted_and_ignored(self) -> None:
        """json_schema is part of the protocol; FakeLLM must accept it."""
        llm = FakeLLM(default_response="ok")
        response = llm.generate(
            [Message(role="user", content="hi")],
            json_schema={"type": "object"},
        )
        assert response.content == "ok"

    def test_timeout_accepted_and_ignored(self) -> None:
        """timeout is part of the protocol; FakeLLM must accept it."""
        llm = FakeLLM(default_response="ok")
        response = llm.generate(
            [Message(role="user", content="hi")],
            timeout=5.0,
        )
        assert response.content == "ok"

