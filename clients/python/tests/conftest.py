"""
Pytest configuration and fixtures for testing the Balancing Services client.
"""

import pytest

from balancing_services import AuthenticatedClient


@pytest.fixture
def test_client():
    """Fixture providing a test client instance."""
    return AuthenticatedClient(
        base_url="https://api.balancing.services/v1", token="test_token_12345"
    )


@pytest.fixture
def sample_imbalance_prices_response():
    """Sample response data for imbalance prices."""
    return {
        "queriedPeriod": {"startAt": "2025-01-01T00:00:00Z", "endAt": "2025-01-02T00:00:00Z"},
        "data": [
            {
                "area": "EE",
                "eicCode": "10Y1001A1001A39I",
                "currency": "EUR",
                "direction": "positive",
                "prices": [
                    {
                        "period": {
                            "startAt": "2025-01-01T00:00:00Z",
                            "endAt": "2025-01-01T01:00:00Z",
                        },
                        "price": 45.50,
                    },
                    {
                        "period": {
                            "startAt": "2025-01-01T01:00:00Z",
                            "endAt": "2025-01-01T02:00:00Z",
                        },
                        "price": 48.75,
                    },
                ],
            }
        ],
        "nextCursor": None,
        "hasMore": False,
    }


@pytest.fixture
def sample_error_response():
    """Sample error response in RFC 7807 Problem Details format."""
    return {
        "type": "invalid-parameter",
        "title": "Invalid Parameter",
        "status": 400,
        "detail": "The area parameter value is not valid",
    }
