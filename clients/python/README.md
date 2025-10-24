# Balancing Services Python Client

Python client library for the [Balancing Services REST API](https://api.balancing.services). Access European electricity balancing market data with a modern, type-safe Python interface.

## Features

- **Type-safe**: Full type hints for better IDE support and code quality
- **Modern Python**: Built with httpx and attrs for async support and clean data models
- **Auto-generated**: Generated from the official OpenAPI specification
- **Comprehensive**: Access to all API endpoints and data models
- **Well-documented**: Inline documentation and usage examples

## Installation

```bash
uv pip install balancing-services
```

Or with pip:

```bash
pip install balancing-services
```

For development, install from source:

```bash
cd clients/python
uv pip install -e .
```

## Quick Start

```python
from balancing_services import AuthenticatedClient
from balancing_services.api.default import get_imbalance_prices
from balancing_services.models import Area
from datetime import datetime

# Create an authenticated client
client = AuthenticatedClient(
    base_url="https://api.balancing.services/v1",
    token="YOUR_API_TOKEN"
)

# Get imbalance prices for Estonia
response = get_imbalance_prices.sync_detailed(
    client=client,
    area=Area.EE,
    period_start_at=datetime.fromisoformat("2025-01-01T00:00:00Z"),
    period_end_at=datetime.fromisoformat("2025-01-02T00:00:00Z")
)

if response.status_code == 200:
    data = response.parsed
    print(f"Query period: {data.queried_period.start_at} to {data.queried_period.end_at}")
    for imbalance_prices in data.data:
        print(f"Area: {imbalance_prices.area}, Direction: {imbalance_prices.direction}")
        for price in imbalance_prices.prices:
            print(f"  {price.period.start_at}: {price.price} {imbalance_prices.currency}")
```

## Authentication

To obtain an API token:
- **Email:** info@balancing.services
- **Website:** https://balancing.services

Include your token when creating the client:

```python
from balancing_services import AuthenticatedClient

client = AuthenticatedClient(
    base_url="https://api.balancing.services/v1",
    token="YOUR_API_TOKEN"
)
```

## Usage Examples

### Get Balancing Energy Bids with Pagination

```python
from balancing_services import AuthenticatedClient
from balancing_services.api.default import get_balancing_energy_bids
from balancing_services.models import Area, ReserveType
from datetime import datetime

client = AuthenticatedClient(base_url="https://api.balancing.services/v1", token="YOUR_TOKEN")

# First page
response = get_balancing_energy_bids.sync_detailed(
    client=client,
    area=Area.EE,
    period_start_at=datetime.fromisoformat("2025-01-01T00:00:00Z"),
    period_end_at=datetime.fromisoformat("2025-01-02T00:00:00Z"),
    reserve_type=ReserveType.AFRR,
    limit=100
)

if response.status_code == 200:
    data = response.parsed
    print(f"Has more: {data.has_more}")

    # Process first page
    for bid_group in data.data:
        for bid in bid_group.bids:
            print(f"Bid: {bid.volume} MW @ {bid.price} {bid_group.currency}")

    # Get next page if available
    if data.has_more and data.next_cursor:
        next_response = get_balancing_energy_bids.sync_detailed(
            client=client,
            area=Area.EE,
            period_start_at=datetime.fromisoformat("2025-01-01T00:00:00Z"),
            period_end_at=datetime.fromisoformat("2025-01-02T00:00:00Z"),
            reserve_type=ReserveType.AFRR,
            cursor=data.next_cursor,
            limit=100
        )
```

### Async Usage

```python
import asyncio
from balancing_services import AuthenticatedClient
from balancing_services.api.default import get_imbalance_prices
from balancing_services.models import Area
from datetime import datetime

async def fetch_prices():
    client = AuthenticatedClient(
        base_url="https://api.balancing.services/v1",
        token="YOUR_TOKEN"
    )

    response = await get_imbalance_prices.asyncio_detailed(
        client=client,
        area=Area.EE,
        period_start_at=datetime.fromisoformat("2025-01-01T00:00:00Z"),
        period_end_at=datetime.fromisoformat("2025-01-02T00:00:00Z")
    )

    if response.status_code == 200:
        return response.parsed
    return None

# Run async function
prices = asyncio.run(fetch_prices())
```

### Error Handling

```python
from balancing_services import AuthenticatedClient
from balancing_services.api.default import get_imbalance_prices
from balancing_services.models import Area
from datetime import datetime

client = AuthenticatedClient(base_url="https://api.balancing.services/v1", token="YOUR_TOKEN")

response = get_imbalance_prices.sync_detailed(
    client=client,
    area=Area.EE,
    period_start_at=datetime.fromisoformat("2025-01-01T00:00:00Z"),
    period_end_at=datetime.fromisoformat("2025-01-02T00:00:00Z")
)

if response.status_code == 200:
    data = response.parsed
    # Process successful response
elif response.status_code == 400:
    error = response.parsed
    print(f"Bad request: {error.detail}")
elif response.status_code == 401:
    print("Authentication failed - check your API token")
elif response.status_code == 429:
    print("Rate limited - please retry later")
else:
    print(f"Error {response.status_code}: {response.content}")
```

## Data Models

All response and request models are fully typed using attrs. Key models include:

- `ImbalancePricesResponse`, `ImbalanceTotalVolumesResponse`
- `BalancingEnergyVolumesResponse`, `BalancingEnergyPricesResponse`, `BalancingEnergyBidsResponse`
- `BalancingCapacityBidsResponse`, `BalancingCapacityPricesResponse`, `BalancingCapacityVolumesResponse`
- Enums: `Area`, `ReserveType`, `Direction`, `Currency`, `ActivationType`, `BidStatus`

## Development

### Regenerating the Client

The client is generated from the OpenAPI specification. To regenerate:

```bash
cd clients/python
./generate.sh
```

### Running Tests

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=balancing_services --cov-report=html
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy balancing_services
```

## Troubleshooting

### Authentication Errors (401)

**Problem:** Receiving 401 Unauthorized responses

**Solutions:**
- Verify your API token is correct
- Check that the token is being passed to `AuthenticatedClient`
- Ensure your token hasn't expired (contact support if needed)

### Bad Request Errors (400)

**Problem:** Receiving 400 Bad Request responses

**Common causes:**
- Invalid date range (end date before start date)
- Date range too large
- Invalid area code or reserve type
- Malformed datetime strings

**Solution:** Check the error detail in the response for specific information:
```python
if response.status_code == 400:
    error = response.parsed
    print(f"Error detail: {error.detail}")
```

### Empty Results

**Problem:** Receiving 200 OK but no data

**Possible reasons:**
- No data available for the requested period
- Data not yet published for recent periods
- Requesting data for a period before data collection started

**Solution:** Try a different time period or check if data exists for your area

### Timeout Issues

**Problem:** Requests timing out

**Solutions:**
- Increase the client timeout:
```python
client = AuthenticatedClient(
    base_url="https://api.balancing.services/v1",
    token="YOUR_TOKEN",
    timeout=30.0  # Increase from default
)
```
- Reduce the date range in your request
- Use pagination for large datasets

### Type Errors with Enums

**Problem:** Type errors when passing area or reserve type

**Solution:** Use the provided enum classes:
```python
from balancing_services.models import Area, ReserveType

# Correct
area=Area.EE

# Incorrect
area="EE"  # String might work but not type-safe
```

## Documentation

- **API Documentation:** https://api.balancing.services/v1/documentation
- **OpenAPI Spec:** [openapi.yaml](../../openapi.yaml)
- **Main Repository:** https://github.com/balancing-services/rest-api

## Support

- **Website:** https://balancing.services
- **Email:** info@balancing.services
- **Issues:** [GitHub Issues](https://github.com/balancing-services/rest-api/issues)

## License

MIT License - see [LICENSE](../../LICENSE) for details.

## Changelog

See [CHANGELOG.md](../../CHANGELOG.md) for version history and changes.
