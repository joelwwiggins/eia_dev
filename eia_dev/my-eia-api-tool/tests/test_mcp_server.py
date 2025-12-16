from __future__ import annotations

import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import anyio
import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


class _StubEiaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        # API key must be present for our stub (mirrors expected usage).
        if qs.get("api_key", [""])[0] != "test-key":
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "missing api_key"}).encode("utf-8"))
            return

        if parsed.path == "/v2/test/endpoint":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"ok": True, "echo": {"foo": qs.get("foo", [None])[0]}}).encode(
                    "utf-8"
                )
            )
            return

        if parsed.path == "/v2/datasets":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"response": {"datasets": []}}).encode("utf-8"))
            return

        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": "not found"}).encode("utf-8"))

    def log_message(self, format, *args):  # noqa: A003
        # Keep test output clean.
        return


@pytest.mark.integration
def test_mcp_stdio_server_can_call_tool():
    """Spawn the MCP stdio server and call `eia_fetch` end-to-end."""

    httpd = HTTPServer(("127.0.0.1", 0), _StubEiaHandler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    async def run():
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        env = {
            **os.environ,
            "EIA_API_KEY": "test-key",
            "EIA_API_BASE_URL": f"http://127.0.0.1:{port}/v2",
        }

        server = StdioServerParameters(
            command=sys.executable,
            args=["-m", "src.mcp_server"],
            cwd=project_root,
            env=env,
        )

        async with stdio_client(server) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                tools = await session.list_tools()
                tool_names = {t.name for t in tools.tools}
                assert "eia_fetch" in tool_names

                result = await session.call_tool(
                    "eia_fetch",
                    {"endpoint": "test/endpoint", "params": {"foo": "bar"}},
                )

                assert result.isError is False
                payload = result.structuredContent
                if payload and isinstance(payload, dict) and "result" in payload:
                    payload = payload["result"]

                if not payload:
                    # Some MCP hosts/versions return tool output as JSON-encoded text content.
                    text_items = [c for c in result.content if getattr(c, "type", None) == "text"]
                    assert text_items, "Expected tool output as text content"
                    payload = json.loads(text_items[0].text)

                assert payload["ok"] is True
                assert payload["echo"]["foo"] == "bar"

    try:
        anyio.run(run)
    finally:
        httpd.shutdown()
