"""Tests for the generic flatten_response function."""

from __future__ import annotations

from stubs import (
    PERIOD,
    StubBidItem,
    StubCapacityBidItem,
    StubCapacityBidsGroup,
    StubCrossZonalGroup,
    StubEnergyBidsGroup,
    StubEnergyPricesGroup,
    StubEnergyVolumesGroup,
    StubEnum,
    StubImbalancePricesGroup,
    StubImbalanceVolumeItem,
    StubImbalanceVolumesGroup,
    StubPriceItem,
    StubVolumeItem,
)

from balancing_services_cli.flatten import (
    CAPACITY_BIDS,
    CAPACITY_CROSS_ZONAL,
    ENERGY_ACTIVATED,
    ENERGY_BIDS,
    ENERGY_PRICES,
    IMBALANCE_PRICES,
    IMBALANCE_VOLUMES,
    flatten_response,
)


def test_flatten_imbalance_prices():
    groups = [
        StubImbalancePricesGroup(
            area=StubEnum.VALUE_A,
            eic_code="10X1001A1001A39Y",
            currency=StubEnum.VALUE_B,
            direction=StubEnum.VALUE_A,
            prices=[StubPriceItem(period=PERIOD, price=45.5)],
        )
    ]
    rows = flatten_response(groups, IMBALANCE_PRICES)
    assert len(rows) == 1
    row = rows[0]
    assert row["area"] == "A"
    assert row["eic_code"] == "10X1001A1001A39Y"
    assert row["currency"] == "B"
    assert row["direction"] == "A"
    assert row["price"] == 45.5
    assert row["periodStartAt"] == "2025-01-01T00:00:00+00:00"
    assert row["periodEndAt"] == "2025-01-01T01:00:00+00:00"


def test_flatten_imbalance_volumes():
    groups = [
        StubImbalanceVolumesGroup(
            area=StubEnum.VALUE_A,
            eic_code="10X",
            volumes=[
                StubImbalanceVolumeItem(period=PERIOD, average_power_mw=100.0, direction=StubEnum.VALUE_B),
            ],
        )
    ]
    rows = flatten_response(groups, IMBALANCE_VOLUMES)
    assert len(rows) == 1
    assert rows[0]["average_power_mw"] == 100.0
    assert rows[0]["direction"] == "B"


def test_flatten_energy_activated():
    groups = [
        StubEnergyVolumesGroup(
            area=StubEnum.VALUE_A,
            eic_code="10X",
            reserve_type=StubEnum.VALUE_B,
            direction=StubEnum.VALUE_A,
            activation_type=StubEnum.VALUE_B,
            standard_product=True,
            volumes=[StubVolumeItem(period=PERIOD, volume=50.0)],
        )
    ]
    rows = flatten_response(groups, ENERGY_ACTIVATED)
    assert len(rows) == 1
    assert rows[0]["volume"] == 50.0
    assert rows[0]["standard_product"] is True


def test_flatten_energy_prices():
    groups = [
        StubEnergyPricesGroup(
            area=StubEnum.VALUE_A,
            eic_code="10X",
            reserve_type=StubEnum.VALUE_B,
            direction=StubEnum.VALUE_A,
            activation_type=StubEnum.VALUE_B,
            currency=StubEnum.VALUE_A,
            standard_product=False,
            prices=[StubPriceItem(period=PERIOD, price=30.0)],
        )
    ]
    rows = flatten_response(groups, ENERGY_PRICES)
    assert len(rows) == 1
    assert rows[0]["price"] == 30.0


def test_flatten_energy_bids():
    groups = [
        StubEnergyBidsGroup(
            area=StubEnum.VALUE_A,
            eic_code="10X",
            reserve_type=StubEnum.VALUE_B,
            direction=StubEnum.VALUE_A,
            currency=StubEnum.VALUE_A,
            standard_product=True,
            bids=[StubBidItem(period=PERIOD, volume=10.0, price=20.0)],
        )
    ]
    rows = flatten_response(groups, ENERGY_BIDS)
    assert len(rows) == 1
    assert rows[0]["volume"] == 10.0
    assert rows[0]["price"] == 20.0


def test_flatten_capacity_bids():
    groups = [
        StubCapacityBidsGroup(
            area=StubEnum.VALUE_A,
            eic_code="10X",
            reserve_type=StubEnum.VALUE_B,
            direction=StubEnum.VALUE_A,
            currency=StubEnum.VALUE_B,
            bids=[StubCapacityBidItem(period=PERIOD, capacity=5.0, price=15.0, status=StubEnum.VALUE_A)],
        )
    ]
    rows = flatten_response(groups, CAPACITY_BIDS)
    assert len(rows) == 1
    assert rows[0]["capacity"] == 5.0
    assert rows[0]["status"] == "A"


def test_flatten_cross_zonal():
    groups = [
        StubCrossZonalGroup(
            from_area=StubEnum.VALUE_A,
            from_eic_code="10X_FROM",
            to_area=StubEnum.VALUE_B,
            to_eic_code="10X_TO",
            reserve_type=StubEnum.VALUE_A,
            volumes=[StubVolumeItem(period=PERIOD, volume=200.0)],
        )
    ]
    rows = flatten_response(groups, CAPACITY_CROSS_ZONAL)
    assert len(rows) == 1
    assert rows[0]["from_area"] == "A"
    assert rows[0]["to_area"] == "B"
    assert rows[0]["volume"] == 200.0


def test_flatten_empty_data():
    rows = flatten_response([], IMBALANCE_PRICES)
    assert rows == []


def test_flatten_multiple_groups_and_items():
    groups = [
        StubImbalancePricesGroup(
            area=StubEnum.VALUE_A,
            eic_code="10X1",
            currency=StubEnum.VALUE_B,
            direction=StubEnum.VALUE_A,
            prices=[
                StubPriceItem(period=PERIOD, price=10.0),
                StubPriceItem(period=PERIOD, price=20.0),
            ],
        ),
        StubImbalancePricesGroup(
            area=StubEnum.VALUE_B,
            eic_code="10X2",
            currency=StubEnum.VALUE_A,
            direction=StubEnum.VALUE_B,
            prices=[
                StubPriceItem(period=PERIOD, price=30.0),
            ],
        ),
    ]
    rows = flatten_response(groups, IMBALANCE_PRICES)
    assert len(rows) == 3
    assert rows[0]["area"] == "A"
    assert rows[0]["price"] == 10.0
    assert rows[1]["area"] == "A"
    assert rows[1]["price"] == 20.0
    assert rows[2]["area"] == "B"
    assert rows[2]["price"] == 30.0
