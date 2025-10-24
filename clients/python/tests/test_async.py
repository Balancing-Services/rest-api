"""
Async tests for the Balancing Services Python client.
"""


import pytest

from balancing_services import AuthenticatedClient
from balancing_services.api.default import (
    get_balancing_energy_prices,
    get_imbalance_prices,
)


class TestAsyncClient:
    """Test async functionality of the client."""

    @pytest.mark.asyncio
    async def test_async_client_creation(self):
        """Test that async client can be created."""
        client = AuthenticatedClient(
            base_url="https://api.balancing.services/v1",
            token="test_token"
        )
        async_httpx_client = client.get_async_httpx_client()
        assert async_httpx_client is not None

    @pytest.mark.asyncio
    async def test_async_client_cleanup(self):
        """Test that async client can be properly closed."""
        client = AuthenticatedClient(
            base_url="https://api.balancing.services/v1",
            token="test_token"
        )
        async_client = client.get_async_httpx_client()

        await async_client.aclose()

        assert async_client.is_closed

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test async context manager usage."""
        client = AuthenticatedClient(
            base_url="https://api.balancing.services/v1",
            token="test_token"
        )

        async with client.get_async_httpx_client() as async_client:
            assert not async_client.is_closed

        assert async_client.is_closed


class TestAsyncEndpoints:
    """Test that async endpoint methods exist and are callable."""

    @pytest.mark.asyncio
    async def test_imbalance_prices_async_detailed_exists(self):
        """Test that async detailed method exists for imbalance prices."""
        assert hasattr(get_imbalance_prices, "asyncio_detailed")
        assert callable(get_imbalance_prices.asyncio_detailed)

    @pytest.mark.asyncio
    async def test_imbalance_prices_async_exists(self):
        """Test that async method exists for imbalance prices."""
        assert hasattr(get_imbalance_prices, "asyncio")
        assert callable(get_imbalance_prices.asyncio)

    @pytest.mark.asyncio
    async def test_balancing_energy_prices_async_exists(self):
        """Test that async methods exist for balancing energy prices."""
        assert hasattr(get_balancing_energy_prices, "asyncio_detailed")
        assert hasattr(get_balancing_energy_prices, "asyncio")
