"""MCP stdio server exposing EIA API tools.

This server uses the Model Context Protocol (MCP) Python SDK and wraps the existing
EIA API helper in `api.get_data`.

Tools exposed:
- eia_get_data(endpoint: str, params?: dict) -> dict

Environment:
- EIA_API_KEY must be set (optionally via my-eia-api-tool/.env)
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import the existing API helper from the same package directory
from .api import get_data


# Initialize .env once at import time so clients launching the server get env vars.
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")


mcp = FastMCP("eia-api")


@mcp.tool()
def eia_get_data(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Fetch data from the EIA API.

    Args:
        endpoint: Path under https://api.eia.gov/, e.g., "v2/total-energy/data/".
        params: Additional query parameters (excluding api_key) to send with the request.

    Returns:
        Parsed JSON response as a dictionary.
    """
    api_key = os.getenv("EIA_API_KEY")
    if not api_key:
        raise ValueError(
            "EIA_API_KEY is not set. Please add it to my-eia-api-tool/.env or your environment."
        )

    return get_data(endpoint, api_key, extra_params=params)


if __name__ == "__main__":
    # Run the MCP server over stdio. An MCP client will typically spawn this process.
    mcp.run()
