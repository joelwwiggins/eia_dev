# eia_dev Project

This repository is a development tool focused on the U.S. Energy Information Administration (EIA) API, designed to facilitate easy access to energy data from eia.gov. The project provides a custom API tool that proxies EIA data into a structured format for easier querying and integration with language models.

## Project Structure

- **my-eia-api-tool/**: Contains the main application code and resources.
  - **src/**: Source code for the API tool.
    - **server.py**: Entry point for the FastAPI application, defining routes for querying EIA data.
    - **api.py**: Core logic for interacting with the EIA API, including data fetching and processing.
    - **types/**: Contains data models and types used throughout the application.
  - **tests/**: Unit and integration tests for the application.
    - **test_api.py**: Unit tests for API functions.
    - **test_integration.py**: Integration tests for overall functionality.
  - **examples/**: Example scripts demonstrating usage of the API tool.
    - **basic_query.py**: Example of performing a basic query against the EIA API.
    - **llm_integration.py**: Example of integrating the API tool with a language model.
  - **docs/**: Documentation for users.
    - **quickstart.md**: Quickstart guide for setting up and using the API tool.
    - **llm_usage.md**: Guide on using the API tool with language models.
  - **requirements.txt**: Lists dependencies required for the project.

- **.devcontainer/**: Configuration for development environments.
  - **devcontainer.json**: Settings for the development container.

- **.github/**: GitHub workflows for continuous integration.
  - **workflows/**: Contains CI configuration files.
    - **ci.yml**: Defines the continuous integration workflow.

## Getting Started

To get started with the project, follow these steps:

1. **Clone the Repository**:
   ```
   git clone https://github.com/joelwwiggins/eia_dev.git
   cd eia_dev
   ```

2. **Set Up Development Environment**:
   You can use GitHub Codespaces or set up a local environment. If using Codespaces, it will automatically configure the environment.

3. **Install Dependencies**:
   ```
   pip install -r my-eia-api-tool/requirements.txt
   ```

4. **Run the API Server**:
   ```
   python my-eia-api-tool/src/server.py
   ```

5. **Access API Documentation**:
   Open your browser and navigate to `http://localhost:8000/docs` to view the API documentation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.