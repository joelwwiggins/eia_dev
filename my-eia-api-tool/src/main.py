import os
from pathlib import Path
from dotenv import load_dotenv
from api import get_data

# Load environment variables from the project .env file (my-eia-api-tool/.env)
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# Retrieve the API key from environment variables
api_key = os.getenv('EIA_API_KEY')

if api_key:
    # Example API endpoint (replace with actual endpoint as needed)
    endpoint = 'v2/seriesid/TOTAL.TETCBUS.M/data/'
    
    # Call the function to get data from the API
    response_data = get_data(endpoint, api_key)
    
    # Print the response data
    print(response_data)
else:
    print("API key not found. Please set it in the .env file.")