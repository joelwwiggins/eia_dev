from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

EIA_API_BASE_URL = "https://api.eia.gov/v2"


class EIAApiError(RuntimeError):
    def __init__(self, status_code: int, message: str, response_text: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


def _normalize_endpoint(endpoint: str) -> str:
    endpoint = endpoint.strip()
    endpoint = endpoint.lstrip("/")
    if endpoint.startswith("v2/"):
        endpoint = endpoint[len("v2/") :]
    return endpoint


def get_data(
    endpoint: str,
    api_key: str,
    params: Optional[Dict[str, Any]] = None,
    *,
    timeout_s: float = 30.0,
) -> Dict[str, Any]:
    """Fetch data from the EIA API.

    Args:
        endpoint (str): The API endpoint to query.
        api_key (str): The API key for authentication.
        params (Dict[str, Any], optional): Additional query parameters.

    Returns:
        Dict[str, Any]: The JSON response from the API.
    """
    endpoint = _normalize_endpoint(endpoint)
    base_url = os.getenv("EIA_API_BASE_URL", EIA_API_BASE_URL).rstrip("/")
    url = f"{base_url}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    params = params or {}
    params['api_key'] = api_key

    response = requests.get(url, headers=headers, params=params, timeout=timeout_s)

    if response.status_code != 200:
        raise EIAApiError(
            status_code=response.status_code,
            message=f"EIA API error: {response.status_code}",
            response_text=response.text,
        )

    return response.json()