from src.api import get_data
import os

def main():
    # Load the API key from environment variables
    api_key = os.getenv("EIA_API_KEY")
    
    if not api_key:
        print("EIA_API_KEY not set in environment. Please set it to continue.")
        return

    # Define the endpoint and parameters for the query
    endpoint = "v2/total-energy/data/"
    parameters = {
        "category": "natural-gas",
        "year": 2023
    }

    # Perform the API query
    try:
        result = get_data(endpoint, api_key, params=parameters)
        print("Query Result:", result)
    except Exception as e:
        print("An error occurred while querying the EIA API:", str(e))

if __name__ == "__main__":
    main()