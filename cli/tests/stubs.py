"""Shared test fixtures."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

# ── Lightweight stubs that mimic the attrs-based API models ──────────────


class StubEnum(str, Enum):
    VALUE_A = "A"
    VALUE_B = "B"


@dataclass
class StubPeriod:
    start_at: datetime
    end_at: datetime


@dataclass
class StubPriceItem:
    period: StubPeriod
    price: float


@dataclass
class StubVolumeItem:
    period: StubPeriod
    volume: float


@dataclass
class StubImbalanceVolumeItem:
    period: StubPeriod
    average_power_mw: float
    direction: StubEnum


@dataclass
class StubBidItem:
    period: StubPeriod
    volume: float
    price: float


@dataclass
class StubCapacityBidItem:
    period: StubPeriod
    capacity: float
    price: float
    status: StubEnum


# ── Stub groups ──────────────────────────────────────────────────────────


@dataclass
class StubImbalancePricesGroup:
    area: StubEnum
    eic_code: str
    currency: StubEnum
    direction: StubEnum
    prices: list[StubPriceItem]


@dataclass
class StubImbalanceVolumesGroup:
    area: StubEnum
    eic_code: str
    volumes: list[StubImbalanceVolumeItem]


@dataclass
class StubEnergyVolumesGroup:
    area: StubEnum
    eic_code: str
    reserve_type: StubEnum
    direction: StubEnum
    activation_type: StubEnum
    standard_product: bool
    volumes: list[StubVolumeItem]


@dataclass
class StubEnergyPricesGroup:
    area: StubEnum
    eic_code: str
    reserve_type: StubEnum
    direction: StubEnum
    activation_type: StubEnum
    currency: StubEnum
    standard_product: bool
    prices: list[StubPriceItem]


@dataclass
class StubEnergyBidsGroup:
    area: StubEnum
    eic_code: str
    reserve_type: StubEnum
    direction: StubEnum
    currency: StubEnum
    standard_product: bool
    bids: list[StubBidItem]


@dataclass
class StubCapacityBidsGroup:
    area: StubEnum
    eic_code: str
    reserve_type: StubEnum
    direction: StubEnum
    currency: StubEnum
    bids: list[StubCapacityBidItem]


@dataclass
class StubCapacityPricesGroup:
    area: StubEnum
    eic_code: str
    reserve_type: StubEnum
    direction: StubEnum
    currency: StubEnum
    procured_at: datetime | None
    prices: list[StubPriceItem]


@dataclass
class StubCapacityVolumesGroup:
    area: StubEnum
    eic_code: str
    reserve_type: StubEnum
    direction: StubEnum
    procured_at: datetime | None
    volumes: list[StubVolumeItem]


@dataclass
class StubCrossZonalGroup:
    from_area: StubEnum
    from_eic_code: str
    to_area: StubEnum
    to_eic_code: str
    reserve_type: StubEnum
    volumes: list[StubVolumeItem]


# ── Helpers ──────────────────────────────────────────────────────────────

PERIOD = StubPeriod(
    start_at=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    end_at=datetime(2025, 1, 1, 1, 0, 0, tzinfo=timezone.utc),
)
