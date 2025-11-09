from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.area import Area
from ..models.currency import Currency
from ..models.direction import Direction
from ..models.eic_code import EicCode
from ..models.reserve_type import ReserveType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.balancing_capacity_price import BalancingCapacityPrice


T = TypeVar("T", bound="BalancingCapacityPrices")


@_attrs_define
class BalancingCapacityPrices:
    """
    Attributes:
        area (Area): Area code
        eic_code (EicCode): Energy Identification Code (EIC)
        reserve_type (ReserveType): Reserve type
        direction (Direction): Balancing direction
        currency (Currency): Currency code
        prices (list[BalancingCapacityPrice]):
        procured_at (datetime.datetime | None | Unset): **EXPERIMENTAL**: Timestamp when the capacity was procured
            (allocation time or gate closure time).
            Used to distinguish different auctions (e.g., yearly vs hourly, or multiple procurement rounds).
            This field is experimental and may be changed or removed without a deprecation period.
             Example: 2024-08-15T14:30:00Z.
    """

    area: Area
    eic_code: EicCode
    reserve_type: ReserveType
    direction: Direction
    currency: Currency
    prices: list[BalancingCapacityPrice]
    procured_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        area = self.area.value

        eic_code = self.eic_code.value

        reserve_type = self.reserve_type.value

        direction = self.direction.value

        currency = self.currency.value

        prices = []
        for prices_item_data in self.prices:
            prices_item = prices_item_data.to_dict()
            prices.append(prices_item)

        procured_at: None | str | Unset
        if isinstance(self.procured_at, Unset):
            procured_at = UNSET
        elif isinstance(self.procured_at, datetime.datetime):
            procured_at = self.procured_at.isoformat()
        else:
            procured_at = self.procured_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "area": area,
                "eicCode": eic_code,
                "reserveType": reserve_type,
                "direction": direction,
                "currency": currency,
                "prices": prices,
            }
        )
        if procured_at is not UNSET:
            field_dict["procuredAt"] = procured_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.balancing_capacity_price import BalancingCapacityPrice

        d = dict(src_dict)
        area = Area(d.pop("area"))

        eic_code = EicCode(d.pop("eicCode"))

        reserve_type = ReserveType(d.pop("reserveType"))

        direction = Direction(d.pop("direction"))

        currency = Currency(d.pop("currency"))

        prices = []
        _prices = d.pop("prices")
        for prices_item_data in _prices:
            prices_item = BalancingCapacityPrice.from_dict(prices_item_data)

            prices.append(prices_item)

        def _parse_procured_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                procured_at_type_0 = isoparse(data)

                return procured_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        procured_at = _parse_procured_at(d.pop("procuredAt", UNSET))

        balancing_capacity_prices = cls(
            area=area,
            eic_code=eic_code,
            reserve_type=reserve_type,
            direction=direction,
            currency=currency,
            prices=prices,
            procured_at=procured_at,
        )

        balancing_capacity_prices.additional_properties = d
        return balancing_capacity_prices

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
