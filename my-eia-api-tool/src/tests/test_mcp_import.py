import importlib
import pytest


def test_import_mcp_server_module():
    # Skip gracefully if MCP SDK isn't installed in the active environment
    try:
        import mcp  # noqa: F401
    except Exception:  # broad to handle envs lacking MCP
        pytest.skip("mcp package not available; skipping MCP import smoke test")

    module = importlib.import_module('src.mcp_server')
    assert hasattr(module, 'mcp')
