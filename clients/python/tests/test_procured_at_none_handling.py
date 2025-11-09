"""Tests for handling None/null values in procuredAt field."""
import datetime
from typing import Any
from balancing_services.models.balancing_capacity_prices import BalancingCapacityPrices
from balancing_services.models.balancing_capacity_volumes import BalancingCapacityVolumes
from balancing_services.types import UNSET


class TestBalancingCapacityPricesNoneHandling:
    """Test that BalancingCapacityPrices handles procuredAt being None."""

    def test_procured_at_is_none(self):
        """Test parsing when procuredAt is explicitly null in JSON."""
        result = make_prices({"procuredAt": None})

        # This should NOT crash
        assert result.procured_at is None

    def test_procured_at_is_missing(self):
        """Test parsing when procuredAt is absent from response."""
        result = make_prices()

        # procuredAt should be UNSET when missing
        assert result.procured_at is UNSET

    def test_procured_at_is_valid(self):
        """Test parsing when procuredAt has a valid timestamp."""
        result = make_prices({"procuredAt": "2024-12-31T23:00:00Z"})

        # procuredAt should be a datetime object
        assert isinstance(result.procured_at, datetime.datetime)
        assert result.procured_at.year == 2024
        assert result.procured_at.month == 12


class TestBalancingCapacityVolumesNoneHandling:
    """Test that BalancingCapacityVolumes handles procuredAt being None."""

    def test_procured_at_is_none(self):
        """Test parsing when procuredAt is explicitly null in JSON."""
        result = make_volumes({"procuredAt": None})

        # This should NOT crash
        assert result.procured_at is None

    def test_procured_at_is_missing(self):
        """Test parsing when procuredAt is absent from response."""
        result = make_volumes()

        # procuredAt should be UNSET when missing
        assert result.procured_at is UNSET

    def test_procured_at_is_valid(self):
        """Test parsing when procuredAt has a valid timestamp."""
        result = make_volumes({"procuredAt": "2024-12-31T23:00:00Z"})

        # procuredAt should be a datetime object
        assert isinstance(result.procured_at, datetime.datetime)


# Helper methods

def make_prices(overrides: dict[str, Any] | None = None) -> BalancingCapacityPrices:
    """Create BalancingCapacityPrices with happy-path defaults.

    Args:
        overrides: Dictionary of fields to override/add to base data.
                  Pass {"procuredAt": None} to test null values.
                  Omit or pass None to test with procuredAt missing.

    Returns:
        BalancingCapacityPrices instance parsed from test data.
    """
    if overrides is None:
        overrides = {}

    base_data = {
        "area": "DE",
        "eicCode": "10YDE-VE-------2",
        "reserveType": "FCR",
        "direction": "up",
        "currency": "EUR",
        "prices": [],
    }
    data = {**base_data, **overrides}
    return BalancingCapacityPrices.from_dict(data)


def make_volumes(overrides: dict[str, Any] | None = None) -> BalancingCapacityVolumes:
    """Create BalancingCapacityVolumes with happy-path defaults.

    Args:
        overrides: Dictionary of fields to override/add to base data.
                  Pass {"procuredAt": None} to test null values.
                  Omit or pass None to test with procuredAt missing.

    Returns:
        BalancingCapacityVolumes instance parsed from test data.
    """
    if overrides is None:
        overrides = {}

    base_data = {
        "area": "DE",
        "eicCode": "10YDE-VE-------2",
        "reserveType": "FCR",
        "direction": "up",
        "volumes": [],
    }
    data = {**base_data, **overrides}
    return BalancingCapacityVolumes.from_dict(data)
