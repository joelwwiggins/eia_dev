# My EIA API Tool

## Overview
My EIA API Tool is a Python application that interacts with the eia.gov API to retrieve energy information. This tool allows users to easily access data from the U.S. Energy Information Administration.

## Project Structure
```
my-eia-api-tool
├── src
│   ├── main.py        # Entry point of the application
│   └── api.py         # Functions to handle API requests
├── requirements.txt    # Project dependencies
├── .env                # Environment variables
└── README.md           # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd my-eia-api-tool
   ```




2. **Install the required dependencies:**

4. **Set up the environment variables:**
   Create a `.env` file in the root directory and add your API key:
   ```
   API_KEY=your_api_key_here
   ```

## Usage

To run the application, execute the following command:
```bash
python src/main.py
```

## API Information
The application interacts with the U.S. Energy Information Administration (EIA) API, which provides access to a wide range of energy data. For more information about the available endpoints and data, visit [eia.gov](https://www.eia.gov/).
