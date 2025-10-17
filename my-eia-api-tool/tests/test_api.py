from src.api import get_data
from unittest.mock import patch, MagicMock
import pytest
import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_get_data_success():
    """Test successful API call"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = get_data("test/endpoint", "fake_key")
        assert result == {"data": "test"}
        mock_get.assert_called_once()


def test_get_data_failure():
    """Test API call failure"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not found"

    with patch("requests.get", return_value=mock_response) as mock_get:
        with pytest.raises(Exception, match="Error: 404"):
            get_data("test/endpoint", "fake_key")


@pytest.mark.integration
def test_eia_api_returns_data():
    """Integration test: Test that the EIA API returns actual data"""
    # Try to load .env file if dotenv is available
    try:
        from pathlib import Path
        from dotenv import load_dotenv

        load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")
    except ImportError:
        pass  # dotenv not installed, rely on environment variables

    api_key = os.getenv("EIA_API_KEY")

    if not api_key:
        pytest.skip("EIA_API_KEY not set in environment")

    # Use a simple endpoint that should return data
    endpoint = "v2/total-energy/data/"

    # Call the real API
    result = get_data(endpoint, api_key)

    # Verify we got data back
    assert result is not None
    assert isinstance(result, dict)
    assert "response" in result

    # Check that we have data in the response
    response = result.get("response", {})
    assert "data" in response
    assert len(response["data"]) > 0

    print(
        f"\nSuccessfully retrieved {len(response['data'])} records from EIA API")
