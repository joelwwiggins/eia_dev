from fastapi import FastAPI
import requests
import os

app = FastAPI()

@app.get("/query")
def query_eia(category: str, year: int):
    api_key = os.getenv("EIA_API_KEY")
    if not api_key:
        return {"error": "API key not found. Please set the EIA_API_KEY environment variable."}
    
    response = requests.get(f"https://api.eia.gov/v2/{category}?api_key={api_key}&data[]=value&start={year}&end={year}")
    
    if response.status_code != 200:
        return {"error": f"Failed to fetch data: {response.status_code}"}
    
    return response.json()

# Example usage for LLM integration
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)