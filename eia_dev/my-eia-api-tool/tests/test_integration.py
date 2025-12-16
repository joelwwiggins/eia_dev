from fastapi.testclient import TestClient
import pytest
import os
from unittest.mock import patch

from src.server import app

client = TestClient(app)

def test_query_eia_success():
    """Test successful query behavior (no network)."""
    os.environ["EIA_API_KEY"] = "test-key"
    with patch("src.server.get_data", return_value={"ok": True, "response": {"data": []}}) as mocked:
        response = client.get("/query?category=natural-gas&year=2023")
        assert response.status_code == 200
        assert response.json()["ok"] is True
        mocked.assert_called_once()

def test_query_eia_failure():
    """Test that upstream errors map to HTTP status codes."""
    os.environ["EIA_API_KEY"] = "test-key"
    from src.api import EIAApiError

    with patch(
        "src.server.get_data",
        side_effect=EIAApiError(status_code=404, message="EIA API error: 404", response_text="Not found"),
    ):
        response = client.get("/query?category=invalid-category&year=2023")
        assert response.status_code == 404

def test_query_eia_no_api_key():
    """Test behavior when API key is not provided"""
    os.environ.pop("EIA_API_KEY", None)  # Remove API key if set
    response = client.get("/query?category=natural-gas&year=2023")
    assert response.status_code == 403

def test_query_eia_empty_response():
    """Server should pass through empty datasets without error."""
    os.environ["EIA_API_KEY"] = "test-key"
    with patch("src.server.get_data", return_value={"response": {"data": []}}):
        response = client.get("/query?category=empty-category&year=2023")
        assert response.status_code == 200
        assert response.json()["response"]["data"] == []