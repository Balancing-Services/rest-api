"""
Basic usage example for the Balancing Services Python client.

This example demonstrates:
- Creating an authenticated client
- Fetching imbalance prices
- Processing the response data

Usage:
    python basic_usage.py --api-token YOUR_API_TOKEN
    python basic_usage.py  # Uses default placeholder token that you can replace with your actual token
"""

import argparse
from datetime import datetime, timedelta, timezone
from balancing_services import AuthenticatedClient
from balancing_services.api.default import get_imbalance_prices
from balancing_services.models import Area


def main():
    parser = argparse.ArgumentParser(description="Fetch imbalance prices from Balancing Services API")
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

    # Fetch imbalance prices for Estonia for yesterday (full day)
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today - timedelta(days=1)
    yesterday_end = today

    response = get_imbalance_prices.sync_detailed(
        client=client,
        area=Area.EE,
        period_start_at=yesterday_start,
        period_end_at=yesterday_end,
    )

    # Check if the request was successful
    if response.status_code == 200:
        data = response.parsed

        print(f"Queried period: {data.queried_period.start_at} to {data.queried_period.end_at}")
        print(f"Has more data: {data.has_more}")
        print()

        # Process each imbalance price group
        for imbalance_prices in data.data:
            print(f"Area: {imbalance_prices.area.value}")
            print(f"EIC Code: {imbalance_prices.eic_code.value}")
            print(f"Direction: {imbalance_prices.direction.value}")
            print(f"Currency: {imbalance_prices.currency.value}")
            print("Prices:")

            # Print individual prices for each period
            for price in imbalance_prices.prices:
                print(f"  {price.period.start_at} to {price.period.end_at}: {price.price} {imbalance_prices.currency.value}/MWh")
            print()

    elif response.status_code == 401:
        print("Authentication failed. Please check your API token.")
    elif response.status_code == 400:
        error = response.parsed
        print(f"Bad request: {error.detail if hasattr(error, 'detail') else 'Invalid parameters'}")
    else:
        print(f"Error {response.status_code}: {response.content}")


if __name__ == "__main__":
    main()
