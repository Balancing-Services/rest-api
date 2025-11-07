from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.period import Period


T = TypeVar("T", bound="BalancingCapacityPrice")


@_attrs_define
class BalancingCapacityPrice:
    """
    Attributes:
        period (Period):
        price (float): Price per MW per hour in the specified currency Example: 12.5.
    """

    period: Period
    price: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period.to_dict()

        price = self.price

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "price": price,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.period import Period

        d = dict(src_dict)
        period = Period.from_dict(d.pop("period"))

        price = d.pop("price")

        balancing_capacity_price = cls(
            period=period,
            price=price,
        )

        balancing_capacity_price.additional_properties = d
        return balancing_capacity_price

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
