from fastapi import FastAPI
import requests
import os

app = FastAPI()

@app.get("/query")
def query_eia(category: str, year: int):
    api_key = os.getenv("EIA_API_KEY")
    if not api_key:
        return {"error": "API key not provided."}

    response = requests.get(f"https://api.eia.gov/v2/{category}?api_key={api_key}&data[]=value&start={year}&end={year}")
    
    if response.status_code != 200:
        return {"error": f"Error fetching data: {response.status_code}"}
    
    return response.json()

# Run with: uvicorn server:app --reload