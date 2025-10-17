def get_data(endpoint, api_key):
    import requests

    url = f"https://api.eia.gov/{endpoint}"
    headers = {"Content-Type": "application/json"}
    params = {"api_key": api_key}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(
            f"Error: {response.status_code}, URL: {url}, Response: {response.text}"
        )

    return response.json()
