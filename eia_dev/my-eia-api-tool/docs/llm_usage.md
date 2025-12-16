# LLM Usage with the EIA API Tool

## Overview

This document provides guidance on how to integrate the EIA API tool with language models, enabling users to query energy data using natural language. The integration allows for seamless interaction with the API, making it accessible for users who may not have programming experience.

## Setting Up the Environment

1. **Create a Codespace**: Go to the [GitHub repository](https://github.com/joelwwiggins/eia_dev) and create a Codespace on the main branch.
2. **Install Dependencies**: In the terminal, run the following command to install the required packages:
   ```
   pip install -r my-eia-api-tool/requirements.txt
   ```

## Launching the API Server

To start the API server, execute the following command in the terminal:
```
uvicorn src.server:app --reload --port 8000
```
The server will run locally, typically accessible at `http://localhost:8000`.

## Launching the MCP Server (stdio)

To expose EIA tools to an MCP-capable LLM host (Claude Desktop / IDE MCP clients), run:

```bash
export EIA_API_KEY=your_api_key_here
python -m src.mcp_server
```

This starts an MCP server over stdio and exposes tools like `eia_fetch`.

## Testing With Ollama (Open Source)

Ollama doesn't speak MCP directly, so this repo includes a small bridge that lets an Ollama model call MCP tools.

1. Install Ollama and pull a model (example):

```bash
ollama pull llama3.2
```

2. Run a tool-enabled chat (bridge starts the MCP server automatically):

```bash
cd my-eia-api-tool
export EIA_API_KEY=your_api_key_here
python examples/ollama_mcp_chat.py --model llama3.2 \
   --prompt "Use tools to fetch a small EIA sample for 2023."
```

Notes:
- Set `OLLAMA_HOST` if your Ollama daemon is not at `http://127.0.0.1:11434`.
- The bridge uses the MCP stdio server at `python -m src.mcp_server`.

## Querying Data via Language Models

### Example Integration

1. **Define the Tool**: In your language model interface (e.g., Grok), define a custom tool for querying the EIA API:
   - **Tool Name**: `eia_query`
   - **Description**: "Query EIA.gov data via MCP server"
   - **Parameters**: Use the schema defined in `eia_api_schema.json`, such as:
     ```json
     {
       "category": "string",
       "year": "integer"
     }
     ```

2. **Prompting the Model**: Use natural language prompts to query data. For example:
   ```
   What's the US natural gas production in 2023? Use the eia_query tool with category='natural-gas' and year=2023.
   ```

### Example Code Snippet

Here’s a simple example of how to query the API using Python:

```python
import requests

def query_eia(category, year):
    response = requests.get(f"http://localhost:8000/query?category={category}&year={year}")
    return response.json()

# Example usage
data = query_eia("natural-gas", 2023)
print(data)
```

## Testing the Integration

To ensure that the integration works correctly, you can run the built-in tests provided in the project. In the terminal, execute:
```
pytest my-eia-api-tool/tests/test_integration.py
```
This will verify that the API calls function as expected.

## Conclusion

Integrating the EIA API tool with language models allows for intuitive data queries using natural language. By following the steps outlined in this document, users can easily set up the environment, launch the API server, and start querying energy data effectively.