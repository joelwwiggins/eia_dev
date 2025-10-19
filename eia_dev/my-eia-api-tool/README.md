# My EIA API Tool

## Overview
The My EIA API Tool is a development tool designed to interact with the U.S. Energy Information Administration (EIA) API. It provides a simple interface for querying EIA data and is structured to facilitate integration with language models for natural language queries.

## Project Structure
- **src/**: Contains the source code for the API server and core logic.
  - **server.py**: Entry point for the FastAPI application.
  - **api.py**: Core logic for interacting with the EIA API.
  - **types/**: Contains data models and types used throughout the application.
  
- **tests/**: Contains unit and integration tests for the application.
  - **test_api.py**: Unit tests for API functions.
  - **test_integration.py**: Integration tests for overall functionality.

- **examples/**: Provides example scripts demonstrating usage.
  - **basic_query.py**: Example of performing a basic query against the EIA API.
  - **llm_integration.py**: Example of integrating the API tool with a language model.

- **docs/**: Documentation for users.
  - **quickstart.md**: Quickstart guide for setting up and using the API tool.
  - **llm_usage.md**: Guide on using the API tool with language models.

- **requirements.txt**: Lists the dependencies required for the project.

## Getting Started

### Prerequisites
- Python 3.7 or higher
- pip

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/joelwwiggins/eia_dev.git
   cd eia_dev/my-eia-api-tool
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the API Server
To start the API server, run:
```
python src/server.py
```
The server will be accessible at `http://localhost:8000`.

### Usage Examples
Refer to the `examples/` directory for scripts demonstrating how to use the API tool for basic queries and integration with language models.

## Testing
To run the tests, use:
```
pytest tests/
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.