from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

import anyio
import httpx
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


def _ollama_host() -> str:
    return os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")


def _to_ollama_tools(mcp_tools: Any) -> List[Dict[str, Any]]:
    """Convert MCP tool definitions to Ollama `tools` (OpenAI-style function tools)."""
    tools: List[Dict[str, Any]] = []
    for t in mcp_tools:
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description or "",
                    # MCP tool.inputSchema is already JSON Schema.
                    "parameters": t.inputSchema or {"type": "object"},
                },
            }
        )
    return tools


def _extract_tool_calls(ollama_message: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return tool calls in a tolerant way across Ollama versions."""
    # Newer ollama returns tool_calls on message.
    tool_calls = ollama_message.get("tool_calls")
    if isinstance(tool_calls, list):
        return tool_calls
    # Some versions may return `function_call` (single).
    fc = ollama_message.get("function_call")
    if isinstance(fc, dict):
        return [
            {
                "id": "call_0",
                "type": "function",
                "function": {"name": fc.get("name"), "arguments": fc.get("arguments", {})},
            }
        ]
    return []


async def _ollama_chat(
    client: httpx.AsyncClient,
    model: str,
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"model": model, "messages": messages, "stream": False}
    if tools is not None:
        payload["tools"] = tools
    resp = await client.post(f"{_ollama_host()}/api/chat", json=payload, timeout=60.0)
    resp.raise_for_status()
    return resp.json()


async def run_chat(model: str, prompt: str) -> int:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "src.mcp_server"],
        cwd=project_root,
        env=os.environ.copy(),
    )

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tool_list = await session.list_tools()
            ollama_tools = _to_ollama_tools(tool_list.tools)

            messages: List[Dict[str, Any]] = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant for EIA.gov data. "
                        "Use the provided tools when you need live EIA API results. "
                        "If EIA_API_KEY is missing, ask the user to set it."
                    ),
                },
                {"role": "user", "content": prompt},
            ]

            async with httpx.AsyncClient() as http:
                # First model response (may contain tool calls)
                r1 = await _ollama_chat(http, model=model, messages=messages, tools=ollama_tools)
                msg1 = r1.get("message", {})
                messages.append(msg1)

                tool_calls = _extract_tool_calls(msg1)
                if not tool_calls:
                    # No tool call; print assistant reply and exit.
                    print(msg1.get("content", ""))
                    return 0

                # Execute tool calls via MCP and feed results back to Ollama.
                for call in tool_calls:
                    fn = (call.get("function") or {})
                    name = fn.get("name")
                    arguments = fn.get("arguments")
                    if isinstance(arguments, str):
                        try:
                            arguments = json.loads(arguments)
                        except json.JSONDecodeError:
                            arguments = {"_raw": arguments}
                    if arguments is None:
                        arguments = {}

                    result = await session.call_tool(name, arguments)
                    structured = result.structuredContent
                    if isinstance(structured, dict) and "result" in structured:
                        structured = structured["result"]

                    # Ollama expects tool results as role=tool with tool_call_id.
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call.get("id", name),
                            "content": json.dumps(structured or {"content": [c.model_dump() for c in result.content]}),
                        }
                    )

                r2 = await _ollama_chat(http, model=model, messages=messages, tools=ollama_tools)
                msg2 = r2.get("message", {})
                print(msg2.get("content", ""))
                return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Chat with Ollama using MCP tools.")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "llama3.2"))
    parser.add_argument(
        "--prompt",
        default="What's US natural gas production in 2023?",
        help="User prompt to send to the model.",
    )
    args = parser.parse_args()

    if not os.getenv("EIA_API_KEY"):
        print("EIA_API_KEY is not set. Export it first.", file=sys.stderr)
        return 2

    return anyio.run(run_chat, args.model, args.prompt)


if __name__ == "__main__":
    raise SystemExit(main())
