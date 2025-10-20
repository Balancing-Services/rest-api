"""
Error handling example for the Balancing Services Python client.

This example demonstrates:
- Handling different error responses
- Working with RFC 7807 Problem Details
- Implementing retry logic

Usage:
    python error_handling.py --api-token YOUR_API_TOKEN
    python error_handling.py  # Uses default placeholder token that you can replace with your actual token
"""

import argparse
import random
import time
from balancing_services import AuthenticatedClient
from balancing_services.api.default import get_balancing_capacity_prices


def fetch_with_retry(client, area, reserve_type, period_start, period_end, max_retries=3, backoff_factor=2):
    """
    Fetch balancing capacity prices with retry logic for rate limiting.

    Args:
        client: Authenticated client instance
        area: Area enum value
        reserve_type: ReserveType enum value
        period_start: Start datetime (datetime object or ISO 8601 string)
        period_end: End datetime (datetime object or ISO 8601 string)
        max_retries: Maximum number of retry attempts
        backoff_factor: Exponential backoff multiplier

    Returns:
        Parsed response data if successful, None otherwise
    """

    for attempt in range(max_retries + 1):
        print(f"Attempt {attempt + 1} of {max_retries + 1}...")

        response = get_balancing_capacity_prices.sync_detailed(
            client=client,
            area=area,
            period_start_at=period_start,
            period_end_at=period_end,
            reserve_type=reserve_type,
        )

        # Success
        if response.status_code == 200:
            print("Success!")
            return response.parsed

        # Authentication error
        elif response.status_code == 401:
            print("Error: Authentication failed. Please check your API token.")
            return None

        # Validation error
        elif response.status_code == 400:
            error = response.parsed
            if hasattr(error, "detail"):
                print(f"Error: Bad request - {error.detail}")
                if hasattr(error, "type"):
                    print(f"  Error type: {error.type}")
            else:
                print("Error: Bad request - Invalid parameters")
            return None

        # Forbidden
        elif response.status_code == 403:
            error = response.parsed
            print(f"Error: Access forbidden - {error.detail if hasattr(error, 'detail') else 'Insufficient permissions'}")
            return None

        # Not found
        elif response.status_code == 404:
            error = response.parsed
            print(f"Error: Resource not found - {error.detail if hasattr(error, 'detail') else 'Resource not found'}")
            return None

        # Rate limited - retry with backoff
        elif response.status_code == 429:
            if attempt < max_retries:
                wait_time = (backoff_factor**attempt) * (0.5 + random.random())
                print(f"Rate limited. Waiting {wait_time:.2f} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                print("Error: Rate limit exceeded and max retries reached.")
                return None

        # Server error - retry
        elif response.status_code >= 500:
            error = response.parsed
            error_msg = error.detail if hasattr(error, "detail") else "Server error"
            if attempt < max_retries:
                wait_time = (backoff_factor**attempt) * (0.5 + random.random())
                print(f"Server error ({response.status_code}): {error_msg}")
                print(f"Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                continue
            else:
                print(f"Error: Server error ({response.status_code}) and max retries reached.")
                return None

        # Unknown error
        else:
            print(f"Error: Unexpected status code {response.status_code}")
            print(f"Response: {response.content}")
            return None

    return None


def main():
    from dateutil.parser import isoparse
    from balancing_services.models import Area, ReserveType

    parser = argparse.ArgumentParser(description="Demonstrate error handling with retry logic")
    parser.add_argument(
        "--api-token",
        default="YOUR_API_TOKEN",
        help="API token for authentication (default: YOUR_API_TOKEN)",
    )
    args = parser.parse_args()

    # Create an authenticated client
    client = AuthenticatedClient(
        base_url="https://api.balancing.services/v1", token=args.api_token
    )

    # Fetch data with retry logic
    data = fetch_with_retry(
        client,
        area=Area.EE,
        reserve_type=ReserveType.AFRR,
        period_start=isoparse("2025-01-01T00:00:00Z"),
        period_end=isoparse("2025-01-02T00:00:00Z"),
        max_retries=3
    )

    if data:
        print(f"\nQueried period: {data.queried_period.start_at} to {data.queried_period.end_at}")
        print(f"Number of price groups: {len(data.data)}")

        for price_group in data.data:
            print(f"\nArea: {price_group.area.value}")
            print(f"Reserve Type: {price_group.reserve_type.value}")
            print(f"Direction: {price_group.direction.value}")
            print(f"Number of prices: {len(price_group.prices)}")

            # Show first few prices
            for i, price in enumerate(price_group.prices[:3]):
                print(f"  {price.period.start_at}: {price.price} {price_group.currency.value}/MW/h")

            if len(price_group.prices) > 3:
                print(f"  ... and {len(price_group.prices) - 3} more prices")
    else:
        print("\nFailed to fetch data after all retry attempts.")


if __name__ == "__main__":
    main()
