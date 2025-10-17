import pytest
from unittest.mock import patch, MagicMock
from src.api import get_data


def test_get_data_success():
    """Test successful API call"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}

    with patch("src.api.requests.get", return_value=mock_response) as mock_get:
        result = get_data("test/endpoint", "fake_key")
        assert result == {"data": "test"}
        mock_get.assert_called_once()


def test_get_data_failure():
    """Test API call failure"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not found"

    with patch("src.api.requests.get", return_value=mock_response) as mock_get:
        with pytest.raises(Exception, match="Error: 404"):
            get_data("test/endpoint", "fake_key")
