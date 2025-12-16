from __future__ import annotations

from examples.ollama_mcp_chat import _extract_tool_calls


def test_extract_tool_calls_tool_calls_list():
    msg = {
        "tool_calls": [
            {
                "id": "call_1",
                "type": "function",
                "function": {"name": "eia_fetch", "arguments": {"endpoint": "datasets"}},
            }
        ]
    }
    calls = _extract_tool_calls(msg)
    assert len(calls) == 1
    assert calls[0]["function"]["name"] == "eia_fetch"


def test_extract_tool_calls_function_call_single():
    msg = {"function_call": {"name": "eia_fetch", "arguments": {"endpoint": "datasets"}}}
    calls = _extract_tool_calls(msg)
    assert len(calls) == 1
    assert calls[0]["function"]["name"] == "eia_fetch"


def test_extract_tool_calls_none():
    msg = {"content": "hello"}
    assert _extract_tool_calls(msg) == []
