"""
tests/unit/test_privacy.py — Tests for core/privacy.py.

Covers identifier detection and log redaction.
"""

from __future__ import annotations

import pytest

from app.core.privacy import contains_identifier, redact_for_log


class TestContainsIdentifier:
    # ── True cases (should be detected) ──────────────────────────────────────

    def test_detects_10_digit_mobile(self) -> None:
        assert contains_identifier("my number is 9876543210")

    def test_detects_india_country_code(self) -> None:
        assert contains_identifier("call me at +919876543210")

    def test_detects_email(self) -> None:
        assert contains_identifier("contact me at patient@example.com")

    def test_detects_aadhaar_plain(self) -> None:
        assert contains_identifier("my aadhaar is 1234 5678 9012")

    def test_detects_aadhaar_dashed(self) -> None:
        assert contains_identifier("aadhaar: 1234-5678-9012")

    def test_detects_long_digit_string(self) -> None:
        assert contains_identifier("my id is 1234567890123")

    # ── False cases (normal medical text, should not be blocked) ─────────────

    def test_ignores_normal_symptom_text(self) -> None:
        assert not contains_identifier("I have had a headache for 3 days, mild pain")

    def test_ignores_short_numbers(self) -> None:
        assert not contains_identifier("my temperature is 38.5 degrees")

    def test_ignores_medication_dose(self) -> None:
        assert not contains_identifier("take 500mg twice daily")


class TestRedactForLog:
    def test_redacts_email(self) -> None:
        result = redact_for_log("email me at user@test.com please")
        assert "[EMAIL]" in result
        assert "user@test.com" not in result

    def test_redacts_phone(self) -> None:
        result = redact_for_log("call 9876543210 for appointment")
        assert "[PHONE]" in result

    def test_redacts_aadhaar(self) -> None:
        result = redact_for_log("aadhaar 1234 5678 9012 is mine")
        assert "[AADHAAR]" in result

    def test_plain_text_unchanged(self) -> None:
        text = "I have a headache for 3 days"
        assert redact_for_log(text) == text

