from __future__ import annotations

import os
from typing import Any, Dict, Optional

from mcp.server import FastMCP

from src.api import EIAApiError, get_data


def _require_api_key() -> str:
    api_key = os.getenv("EIA_API_KEY")
    if not api_key:
        raise ValueError("EIA_API_KEY is not set")
    return api_key


mcp = FastMCP(
    name="eia-mcp",
    instructions=(
        "Tools for querying the U.S. EIA API (v2). "
        "Prefer `eia_fetch` for exact endpoints + params."
    ),
)


@mcp.tool()
def eia_fetch(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    timeout_s: float = 30.0,
) -> Dict[str, Any]:
    """Fetch raw JSON from an EIA API v2 endpoint.

    `endpoint` may be provided with or without a leading `v2/`.
    """

    try:
        return get_data(
            endpoint=endpoint,
            api_key=_require_api_key(),
            params=params,
            timeout_s=timeout_s,
        )
    except EIAApiError as exc:
        # Preserve status code context in the error message that MCP hosts surface.
        detail = exc.response_text or str(exc)
        raise RuntimeError(f"EIA API error {exc.status_code}: {detail}") from exc


@mcp.tool()
def eia_list_datasets(timeout_s: float = 30.0) -> Dict[str, Any]:
    """Return dataset metadata from the EIA API.

    Note: availability/shape depends on EIA API v2.
    """

    return eia_fetch("datasets", params=None, timeout_s=timeout_s)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
