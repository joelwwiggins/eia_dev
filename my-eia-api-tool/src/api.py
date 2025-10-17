def get_data(endpoint, api_key, extra_params=None):
    """Call the EIA API and return JSON.

    Args:
        endpoint (str): Path under https://api.eia.gov/, e.g., 'v2/total-energy/data/'.
        api_key (str): EIA API key.
        extra_params (dict | None): Additional query parameters to include (excluding api_key).

    Returns:
        dict: Parsed JSON response.
    """
    import requests

    url = f"https://api.eia.gov/{endpoint}"
    headers = {"Content-Type": "application/json"}
    params = {"api_key": api_key}

    if isinstance(extra_params, dict):
        # Merge extra params without overwriting api_key inadvertently
        params.update({k: v for k, v in extra_params.items() if v is not None})

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(
            f"Error: {response.status_code}, URL: {url}, Response: {response.text}"
        )

    return response.json()
