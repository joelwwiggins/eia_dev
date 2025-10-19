from typing import Any, Dict
import requests

EIA_API_BASE_URL = "https://api.eia.gov/v2"

def get_data(endpoint: str, api_key: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Fetch data from the EIA API.

    Args:
        endpoint (str): The API endpoint to query.
        api_key (str): The API key for authentication.
        params (Dict[str, Any], optional): Additional query parameters.

    Returns:
        Dict[str, Any]: The JSON response from the API.
    """
    url = f"{EIA_API_BASE_URL}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    params = params or {}
    params['api_key'] = api_key

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    return response.json()