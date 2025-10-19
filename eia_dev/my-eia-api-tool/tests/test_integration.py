from fastapi.testclient import TestClient
import pytest
import os
from src.server import app  # Assuming your FastAPI app is defined in server.py

client = TestClient(app)

def test_query_eia_success():
    """Test successful query to the EIA API"""
    api_key = os.getenv("EIA_API_KEY")
    if not api_key:
        pytest.skip("EIA_API_KEY not set in environment")

    response = client.get("/query?category=natural-gas&year=2023")
    assert response.status_code == 200
    assert "data" in response.json()

def test_query_eia_failure():
    """Test failure case for the EIA API query"""
    response = client.get("/query?category=invalid-category&year=2023")
    assert response.status_code == 404  # Assuming the API returns 404 for invalid categories

def test_query_eia_no_api_key():
    """Test behavior when API key is not provided"""
    os.environ.pop("EIA_API_KEY", None)  # Remove API key if set
    response = client.get("/query?category=natural-gas&year=2023")
    assert response.status_code == 403  # Assuming the API returns 403 for missing API key

def test_query_eia_empty_response():
    """Test handling of empty response from the EIA API"""
    api_key = os.getenv("EIA_API_KEY")
    if not api_key:
        pytest.skip("EIA_API_KEY not set in environment")

    response = client.get("/query?category=empty-category&year=2023")  # Assuming this category returns no data
    assert response.status_code == 200
    assert response.json() == {"data": []}  # Assuming the expected response format for no data