"""
Pagination example for the Balancing Services Python client.

This example demonstrates:
- Using pagination for large datasets
- Iterating through multiple pages
- Working with cursors

Usage:
    python pagination_example.py --api-token YOUR_API_TOKEN
    python pagination_example.py  # Uses default placeholder token that you can replace with your actual token
"""

import argparse
from datetime import datetime, timedelta, timezone
from balancing_services import AuthenticatedClient
from balancing_services.api.default import get_balancing_energy_bids
from balancing_services.models import Area, ReserveType


def main():
    parser = argparse.ArgumentParser(description="Fetch paginated balancing energy bids")
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

    # Fetch balancing energy bids with pagination for yesterday
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today - timedelta(days=1)
    yesterday_end = today

    area = Area.EE
    reserve_type = ReserveType.AFRR
    page_size = 100

    print(f"Fetching balancing energy bids for {area.value}, reserve type: {reserve_type.value}")
    print(f"Period: {yesterday_start} to {yesterday_end}")
    print()

    cursor = None
    page_number = 1
    total_bid_groups = 0
    total_bids = 0

    # Iterate through all pages
    while True:
        print(f"Fetching page {page_number}...")

        response = get_balancing_energy_bids.sync_detailed(
            client=client,
            area=area,
            period_start_at=yesterday_start,
            period_end_at=yesterday_end,
            reserve_type=reserve_type,
            cursor=cursor,
            limit=page_size,
        )

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.content}")
            break

        data = response.parsed
        total_bid_groups += len(data.data)

        # Process the current page
        for bid_group in data.data:
            print(f"  Area: {bid_group.area.value}, Direction: {bid_group.direction.value}")
            print(f"  Reserve Type: {bid_group.reserve_type.value}")
            print(f"  Standard Product: {bid_group.standard_product}")
            print(f"  Number of bids: {len(bid_group.bids)}")

            total_bids += len(bid_group.bids)

            # Show first few bids as examples
            for i, bid in enumerate(bid_group.bids[:3]):
                print(f"    Bid {i + 1}: {bid.volume} MW @ {bid.price} {bid_group.currency.value}/MWh")
                print(f"           Period: {bid.period.start_at} to {bid.period.end_at}")

            if len(bid_group.bids) > 3:
                print(f"    ... and {len(bid_group.bids) - 3} more bids")
            print()

        # Check if there are more pages
        if not data.has_more:
            print("No more pages available.")
            break

        # Get the cursor for the next page
        cursor = data.next_cursor
        if not cursor:
            print("No cursor provided for next page.")
            break

        page_number += 1

    print(f"\nSummary:")
    print(f"  Total pages fetched: {page_number}")
    print(f"  Total bid groups: {total_bid_groups}")
    print(f"  Total bids: {total_bids}")


if __name__ == "__main__":
    main()
