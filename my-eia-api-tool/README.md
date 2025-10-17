# My EIA API Tool

## Overview
My EIA API Tool is a Python application that interacts with the eia.gov API to retrieve energy information. This tool now also exposes a Model Context Protocol (MCP) stdio server so MCP-compatible clients can call it as a tool.

## Project Structure
```
my-eia-api-tool
├── src
│   ├── main.py           # Example CLI-style usage
│   ├── api.py            # Functions to handle API requests
│   └── mcp_server.py     # MCP stdio server exposing eia_get_data
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables
└── README.md             # Project documentation
```

## Setup

1. Clone and enter the project directory.
2. Create and activate a Python 3.10+ environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` in the project root and add your EIA key:
   ```ini
   EIA_API_KEY=your_api_key_here
   ```

## Usage

### Run as a script
```bash
python src/main.py
```

### Run as an MCP server (stdio)
Launch the server (your MCP client typically spawns this):
```bash
python -m src.mcp_server
```

The server exposes one tool:
- `eia_get_data(endpoint: str, params?: dict)`

Example tool call (conceptual, actual invocation depends on your MCP client):
- name: `eia_get_data`
- arguments:
  ```json
  {
    "endpoint": "v2/total-energy/data/",
    "params": { "frequency": "monthly", "data[0]": "value" }
  }
  ```

## API Information
The application interacts with the U.S. Energy Information Administration (EIA) API, which provides access to a wide range of energy data. For more information about the available endpoints and data, visit [eia.gov](https://www.eia.gov/).
