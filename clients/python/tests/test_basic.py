"""
Basic tests for the Balancing Services Python client.

These tests verify that the generated client has the expected structure
and can be instantiated correctly.
"""

from balancing_services import AuthenticatedClient, Client
from balancing_services.api.default import (
    get_balancing_capacity_bids,
    get_balancing_capacity_prices,
    get_balancing_capacity_procured_volumes,
    get_balancing_energy_activated_volumes,
    get_balancing_energy_bids,
    get_balancing_energy_prices,
    get_imbalance_prices,
    get_imbalance_total_volumes,
)
from balancing_services.models import (
    ActivationType,
    Area,
    BidStatus,
    Currency,
    Direction,
    ImbalanceDirection,
    ReserveType,
    TotalImbalanceDirection,
)


class TestClientInstantiation:
    """Test that clients can be created correctly."""

    def test_create_unauthenticated_client(self):
        """Test creating an unauthenticated client."""
        client = Client(base_url="https://api.balancing.services/v1")
        assert client._base_url == "https://api.balancing.services/v1"

    def test_create_authenticated_client(self):
        """Test creating an authenticated client."""
        client = AuthenticatedClient(
            base_url="https://api.balancing.services/v1", token="test_token"
        )
        assert client._base_url == "https://api.balancing.services/v1"
        assert client.token == "test_token"

    def test_create_authenticated_client_with_custom_timeout(self):
        """Test creating an authenticated client with custom timeout."""
        client = AuthenticatedClient(
            base_url="https://api.balancing.services/v1", token="test_token", timeout=30.0
        )
        assert client._base_url == "https://api.balancing.services/v1"
        assert client._timeout == 30.0


class TestAPIEndpointsExist:
    """Test that all expected API endpoints are available."""

    def test_imbalance_endpoints_exist(self):
        """Test that imbalance endpoints are available."""
        assert hasattr(get_imbalance_prices, "sync_detailed")
        assert hasattr(get_imbalance_prices, "asyncio_detailed")
        assert hasattr(get_imbalance_total_volumes, "sync_detailed")
        assert hasattr(get_imbalance_total_volumes, "asyncio_detailed")

    def test_balancing_energy_endpoints_exist(self):
        """Test that balancing energy endpoints are available."""
        assert hasattr(get_balancing_energy_activated_volumes, "sync_detailed")
        assert hasattr(get_balancing_energy_activated_volumes, "asyncio_detailed")
        assert hasattr(get_balancing_energy_prices, "sync_detailed")
        assert hasattr(get_balancing_energy_prices, "asyncio_detailed")
        assert hasattr(get_balancing_energy_bids, "sync_detailed")
        assert hasattr(get_balancing_energy_bids, "asyncio_detailed")

    def test_balancing_capacity_endpoints_exist(self):
        """Test that balancing capacity endpoints are available."""
        assert hasattr(get_balancing_capacity_bids, "sync_detailed")
        assert hasattr(get_balancing_capacity_bids, "asyncio_detailed")
        assert hasattr(get_balancing_capacity_prices, "sync_detailed")
        assert hasattr(get_balancing_capacity_prices, "asyncio_detailed")
        assert hasattr(get_balancing_capacity_procured_volumes, "sync_detailed")
        assert hasattr(get_balancing_capacity_procured_volumes, "asyncio_detailed")


class TestEnums:
    """Test that all expected enums are available with correct values."""

    def test_area_enum(self):
        """Test Area enum."""
        assert Area.EE == "EE"
        assert Area.FI == "FI"
        assert Area.LV == "LV"
        # Verify it's a comprehensive enum
        assert len(Area) >= 40  # At least 40 areas as per spec

    def test_reserve_type_enum(self):
        """Test ReserveType enum."""
        assert ReserveType.FCR == "FCR"
        assert ReserveType.AFRR == "aFRR"
        assert ReserveType.MFRR == "mFRR"
        assert ReserveType.RR == "RR"

    def test_direction_enum(self):
        """Test Direction enum."""
        assert Direction.UP == "up"
        assert Direction.DOWN == "down"

    def test_imbalance_direction_enum(self):
        """Test ImbalanceDirection enum."""
        assert ImbalanceDirection.POSITIVE == "positive"
        assert ImbalanceDirection.SYMMETRIC == "symmetric"
        assert ImbalanceDirection.NEGATIVE == "negative"

    def test_total_imbalance_direction_enum(self):
        """Test TotalImbalanceDirection enum."""
        assert TotalImbalanceDirection.SURPLUS == "surplus"
        assert TotalImbalanceDirection.DEFICIT == "deficit"
        assert TotalImbalanceDirection.BALANCED == "balanced"

    def test_currency_enum(self):
        """Test Currency enum."""
        assert Currency.EUR == "EUR"
        assert Currency.BGN == "BGN"

    def test_activation_type_enum(self):
        """Test ActivationType enum."""
        assert ActivationType.DIRECT == "direct"
        assert ActivationType.SCHEDULED == "scheduled"
        assert ActivationType.NOT_APPLICABLE == "not_applicable"

    def test_bid_status_enum(self):
        """Test BidStatus enum."""
        assert BidStatus.OFFERED == "offered"
        assert BidStatus.ACCEPTED == "accepted"


class TestClientConfiguration:
    """Test client configuration options."""

    def test_custom_base_url(self):
        """Test that custom base URL is respected."""
        client = Client(base_url="https://custom.example.com/api")
        assert client._base_url == "https://custom.example.com/api"

    def test_client_has_with_headers_method(self):
        """Test that client has method to add headers."""
        client = AuthenticatedClient(
            base_url="https://api.balancing.services/v1", token="test_token"
        )
        assert hasattr(client, "with_headers")

    def test_authenticated_client_includes_token(self):
        """Test that authenticated client has token configured."""
        client = AuthenticatedClient(
            base_url="https://api.balancing.services/v1", token="test_token_12345"
        )
        assert client.token == "test_token_12345"
        assert client.prefix == "Bearer"
        assert client.auth_header_name == "Authorization"
