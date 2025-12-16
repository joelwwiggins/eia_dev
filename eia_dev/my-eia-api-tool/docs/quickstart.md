# Quickstart Guide for my-eia-api-tool

Welcome to the quickstart guide for the my-eia-api-tool! This guide will help you set up and run the API tool to access data from the U.S. Energy Information Administration (EIA).

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)

## Getting Started

1. **Clone the Repository**

   Open your terminal and clone the repository:

   ```
   git clone https://github.com/joelwwiggins/eia_dev.git
   cd eia_dev/my-eia-api-tool
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   Create a virtual environment to manage dependencies:

   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the required packages using pip:

   ```
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root of the `my-eia-api-tool` directory and add your EIA API key:

   ```
   EIA_API_KEY=your_api_key_here
   ```

5. **Run the API Server**

   Start the FastAPI server:

   ```
   uvicorn src.server:app --reload --port 8000
   ```

   The server will start running on `http://localhost:8000`.

6. **Access the API Documentation**

   Open your web browser and navigate to `http://localhost:8000/docs` to view the interactive API documentation.

## Making API Calls

You can now make API calls to the EIA data endpoints. Use the provided examples in the `examples` directory to see how to query data.

## Next Steps

Explore the `docs` directory for more detailed usage instructions and integration examples with language models.

If you want to connect an MCP-capable LLM host, run the stdio MCP server:

```bash
export EIA_API_KEY=your_api_key_here
python -m src.mcp_server
```

Happy querying!