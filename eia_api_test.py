import requests

# Test EIA API with a short response
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('EIA_API_KEY')
url = f'https://api.eia.gov/v2/series?api_key={api_key}&series_id=ELEC.GEN.ALL-US-99.M'

response = requests.get(url)
data = response.json()

# Limit output to first few characters for testing
print(f'Response (shortened): {str(data)[:100]}...')