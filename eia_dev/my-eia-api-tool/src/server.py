import os

from fastapi import FastAPI, HTTPException

from src.api import EIAApiError, get_data

app = FastAPI()

@app.get("/query")
def query_eia(category: str, year: int):
    api_key = os.getenv("EIA_API_KEY")
    if not api_key:
        raise HTTPException(status_code=403, detail="EIA_API_KEY not set")

    try:
        return get_data(
            endpoint=category,
            api_key=api_key,
            params={"data[]": ["value"], "start": year, "end": year},
        )
    except EIAApiError as exc:
        detail = exc.response_text or str(exc)
        raise HTTPException(status_code=exc.status_code, detail=detail) from exc

# Run with: uvicorn server:app --reload