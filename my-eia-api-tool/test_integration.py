#!/usr/bin/env python3
"""
Simple integration test to verify the EIA API returns data
"""
from api import get_data
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_eia_api():
    """Test that the EIA API returns actual data"""
    # Read API key directly from .env file
    env_file = Path(__file__).parent / ".env"
    api_key = None

    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith("EIA_API_KEY="):
                    api_key = line.strip().split("=", 1)[1]
                    break

    if not api_key:
        print("ERROR: EIA_API_KEY not found in .env file")
        return False

    print(f"Testing EIA API with key: {api_key[:8]}...")

    # Use a simple endpoint that should return data
    endpoint = "v2/total-energy/data/"

    print(f"Calling endpoint: {endpoint}")

    try:
        # Call the real API
        result = get_data(endpoint, api_key)

        # Verify we got data back
        assert result is not None, "Result is None"
        assert isinstance(
            result, dict), f"Result is not a dict, got {type(result)}"
        assert "response" in result, "No 'response' key in result"

        # Check that we have data in the response
        response = result.get("response", {})
        assert "data" in response, "No 'data' key in response"
        data_count = len(response["data"])
        assert data_count > 0, "No data records returned"

        print(f"\n✅ SUCCESS: Retrieved {data_count} records from EIA API")
        print(f"\nFirst record sample:")
        first_record = response['data'][0]
        for key, value in list(first_record.items())[:5]:
            print(f"  {key}: {value}")

        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_eia_api()
    sys.exit(0 if success else 1)
