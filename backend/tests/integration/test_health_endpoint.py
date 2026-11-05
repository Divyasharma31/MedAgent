"""
tests/integration/test_health_endpoint.py — Tests for GET /health.

Phase 0 checklist item: "Tests: /health returns ok".
Uses httpx TestClient (no running server needed).
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


class TestHealthEndpoint:
    def test_returns_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200

    def test_status_is_ok(self, client: TestClient) -> None:
        data = client.get("/health").json()
        assert data["status"] == "ok"

    def test_llm_provider_is_fake(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # The default provider is 'fake' in the test environment.
        data = client.get("/health").json()
        assert data["llm_provider"] == "fake"

    def test_phase_field_present(self, client: TestClient) -> None:
        data = client.get("/health").json()
        assert "phase" in data
        assert data["phase"] == "0-foundations"

    def test_app_env_field_present(self, client: TestClient) -> None:
        data = client.get("/health").json()
        assert "app_env" in data

    def test_response_schema_matches(self, client: TestClient) -> None:
        data = client.get("/health").json()
        required_keys = {"status", "llm_provider", "app_env", "phase"}
        assert required_keys.issubset(data.keys())

