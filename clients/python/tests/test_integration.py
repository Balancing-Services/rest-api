"""
Integration tests using respx to mock HTTP responses.
"""

from datetime import datetime, timezone

import pytest
import respx
from httpx import Response

from balancing_services import AuthenticatedClient
from balancing_services.api.default import (
    get_balancing_energy_bids,
    get_imbalance_prices,
)
from balancing_services.models import Area, ReserveType


@pytest.fixture
def authenticated_client():
    """Create an authenticated client for testing."""
    return AuthenticatedClient(
        base_url="https://api.balancing.services/v1",
        token="test_token_12345"
    )


@pytest.fixture
def mock_imbalance_prices_response():
    """Mock response data for imbalance prices."""
    return {
        "queriedPeriod": {
            "startAt": "2025-01-01T00:00:00Z",
            "endAt": "2025-01-02T00:00:00Z"
        },
        "hasMore": False,
        "data": [
            {
                "area": "EE",
                "eicCode": "10Y1001A1001A39I",
                "direction": "positive",
                "currency": "EUR",
                "prices": [
                    {
                        "period": {
                            "startAt": "2025-01-01T00:00:00Z",
                            "endAt": "2025-01-01T01:00:00Z"
                        },
                        "price": 45.5
                    }
                ]
            }
        ]
    }


@pytest.fixture
def mock_balancing_energy_bids_response():
    """Mock response data for balancing energy bids."""
    return {
        "queriedPeriod": {
            "startAt": "2025-01-01T00:00:00Z",
            "endAt": "2025-01-02T00:00:00Z"
        },
        "hasMore": True,
        "nextCursor": "v1:AAAAAYwBAgMEBQYHCAkKCw==",
        "data": [
            {
                "area": "EE",
                "eicCode": "10Y1001A1001A39I",
                "reserveType": "aFRR",
                "direction": "up",
                "standardProduct": "15MIN",
                "currency": "EUR",
                "bids": [
                    {
                        "period": {
                            "startAt": "2025-01-01T00:00:00Z",
                            "endAt": "2025-01-01T00:15:00Z"
                        },
                        "volume": 10.5,
                        "price": 25.0,
                        "status": "accepted"
                    }
                ]
            }
        ]
    }


@respx.mock
def test_get_imbalance_prices_success(authenticated_client, mock_imbalance_prices_response):
    """Test successful imbalance prices request."""
    route = respx.get(
        "https://api.balancing.services/v1/imbalance/prices"
    ).mock(return_value=Response(200, json=mock_imbalance_prices_response))

    response = get_imbalance_prices.sync_detailed(
        client=authenticated_client,
        area=Area.EE,
        period_start_at=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        period_end_at=datetime(2025, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
    )

    assert response.status_code == 200
    assert response.parsed is not None
    assert response.parsed.has_more is False
    assert len(response.parsed.data) == 1
    assert response.parsed.data[0].area == Area.EE


@respx.mock
def test_get_imbalance_prices_unauthorized(authenticated_client):
    """Test unauthorized response (401)."""
    error_response = {
        "type": "unauthorized",
        "title": "Unauthorized",
        "status": 401,
        "detail": "Invalid or missing authentication token"
    }

    route = respx.get(
        "https://api.balancing.services/v1/imbalance/prices"
    ).mock(return_value=Response(401, json=error_response))

    response = get_imbalance_prices.sync_detailed(
        client=authenticated_client,
        area=Area.EE,
        period_start_at=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        period_end_at=datetime(2025, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
    )

    assert response.status_code == 401
    assert response.parsed is not None
    assert response.parsed.status == 401


@respx.mock
def test_get_imbalance_prices_bad_request(authenticated_client):
    """Test bad request response (400)."""
    error_response = {
        "type": "invalid-parameter",
        "title": "Bad Request",
        "status": 400,
        "detail": "Invalid period range"
    }

    route = respx.get(
        "https://api.balancing.services/v1/imbalance/prices"
    ).mock(return_value=Response(400, json=error_response))

    response = get_imbalance_prices.sync_detailed(
        client=authenticated_client,
        area=Area.EE,
        period_start_at=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        period_end_at=datetime(2025, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
    )

    assert response.status_code == 400
    assert response.parsed is not None
    assert response.parsed.detail == "Invalid period range"


@respx.mock
def test_get_balancing_energy_bids_pagination(authenticated_client, mock_balancing_energy_bids_response):
    """Test pagination with balancing energy bids."""
    route = respx.get(
        "https://api.balancing.services/v1/balancing/energy/bids"
    ).mock(return_value=Response(200, json=mock_balancing_energy_bids_response))

    response = get_balancing_energy_bids.sync_detailed(
        client=authenticated_client,
        area=Area.EE,
        period_start_at=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        period_end_at=datetime(2025, 1, 2, 0, 0, 0, tzinfo=timezone.utc),
        reserve_type=ReserveType.AFRR,
        limit=100
    )

    assert response.status_code == 200
    assert response.parsed is not None
    assert response.parsed.has_more is True
    assert response.parsed.next_cursor == "v1:AAAAAYwBAgMEBQYHCAkKCw=="
    assert len(response.parsed.data) == 1


@respx.mock
def test_authentication_header_included(authenticated_client, mock_imbalance_prices_response):
    """Test that authentication header is included in requests."""
    route = respx.get(
        "https://api.balancing.services/v1/imbalance/prices",
        headers={"Authorization": "Bearer test_token_12345"}
    ).mock(return_value=Response(200, json=mock_imbalance_prices_response))

    response = get_imbalance_prices.sync_detailed(
        client=authenticated_client,
        area=Area.EE,
        period_start_at=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        period_end_at=datetime(2025, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
    )

    assert response.status_code == 200
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_async_get_imbalance_prices(authenticated_client, mock_imbalance_prices_response):
    """Test async request for imbalance prices."""
    route = respx.get(
        "https://api.balancing.services/v1/imbalance/prices"
    ).mock(return_value=Response(200, json=mock_imbalance_prices_response))

    response = await get_imbalance_prices.asyncio_detailed(
        client=authenticated_client,
        area=Area.EE,
        period_start_at=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        period_end_at=datetime(2025, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
    )

    assert response.status_code == 200
    assert response.parsed is not None
    assert len(response.parsed.data) == 1
