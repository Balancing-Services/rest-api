"""Generic flattening of nested API responses into flat row dicts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


@dataclass(frozen=True)
class EndpointConfig:
    """Describes how to flatten a specific API response.

    Attributes:
        group_fields: attribute names on each data[] group to extract as columns.
        items_field: attribute name holding the nested list (e.g. "prices", "volumes", "bids").
        item_fields: attribute names on each nested item to extract as columns.
    """

    group_fields: tuple[str, ...]
    items_field: str
    item_fields: tuple[str, ...]


def _extract_value(obj: Any, field: str) -> Any:
    """Pull a value from an attrs/dataclass object, converting enums and datetimes to strings."""
    val = getattr(obj, field)
    if isinstance(val, Enum):
        return val.value
    if isinstance(val, datetime):
        return val.isoformat()
    return val


def flatten_response(data: list[Any], config: EndpointConfig) -> list[dict[str, Any]]:
    """Flatten a list of data groups into a flat list of row dicts.

    Each group contains metadata fields and a nested list of items.
    The output denormalizes each item row by prepending the group metadata.
    """
    rows: list[dict[str, Any]] = []
    for group in data:
        group_values = {field: _extract_value(group, field) for field in config.group_fields}
        items = getattr(group, config.items_field)
        for item in items:
            row = dict(group_values)
            for field in config.item_fields:
                if field == "period":
                    period = getattr(item, "period")
                    row["periodStartAt"] = period.start_at.isoformat()
                    row["periodEndAt"] = period.end_at.isoformat()
                else:
                    row[field] = _extract_value(item, field)
            rows.append(row)
    return rows


# ── Endpoint configurations ────────────────────────────────────────────────

IMBALANCE_PRICES = EndpointConfig(
    group_fields=("area", "eic_code", "currency", "direction"),
    items_field="prices",
    item_fields=("period", "price"),
)

IMBALANCE_VOLUMES = EndpointConfig(
    group_fields=("area", "eic_code"),
    items_field="volumes",
    item_fields=("period", "average_power_mw", "direction"),
)

ENERGY_ACTIVATED = EndpointConfig(
    group_fields=("area", "eic_code", "reserve_type", "direction", "activation_type", "standard_product"),
    items_field="volumes",
    item_fields=("period", "volume"),
)

ENERGY_OFFERED = EndpointConfig(
    group_fields=("area", "eic_code", "reserve_type", "direction", "activation_type", "standard_product"),
    items_field="volumes",
    item_fields=("period", "volume"),
)

ENERGY_PRICES = EndpointConfig(
    group_fields=("area", "eic_code", "reserve_type", "direction", "activation_type", "currency", "standard_product"),
    items_field="prices",
    item_fields=("period", "price"),
)

ENERGY_BIDS = EndpointConfig(
    group_fields=("area", "eic_code", "reserve_type", "direction", "currency", "standard_product"),
    items_field="bids",
    item_fields=("period", "volume", "price"),
)

CAPACITY_BIDS = EndpointConfig(
    group_fields=("area", "eic_code", "reserve_type", "direction", "currency"),
    items_field="bids",
    item_fields=("period", "capacity", "price", "status"),
)

CAPACITY_PRICES = EndpointConfig(
    group_fields=("area", "eic_code", "reserve_type", "direction", "currency", "procured_at"),
    items_field="prices",
    item_fields=("period", "price"),
)

CAPACITY_PROCURED = EndpointConfig(
    group_fields=("area", "eic_code", "reserve_type", "direction", "procured_at"),
    items_field="volumes",
    item_fields=("period", "volume"),
)

CAPACITY_CROSS_ZONAL = EndpointConfig(
    group_fields=("from_area", "from_eic_code", "to_area", "to_eic_code", "reserve_type"),
    items_field="volumes",
    item_fields=("period", "volume"),
)
