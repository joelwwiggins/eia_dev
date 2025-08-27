import os
from dotenv import load_dotenv
from api import get_data

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv('EIA_API_KEY')

if api_key:
    # Example API endpoint (replace with actual endpoint as needed)
    endpoint = 'v2/seriesid/ELEC.GEN.ALL-AK-99.A/data/'
    
    # Call the function to get data from the API
    response_data = get_data(endpoint, api_key)
    
    # Print the response data
    print(response_data)
else:
    print("API key not found. Please set it in the .env file.")