from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.balancing_energy_prices import BalancingEnergyPrices
    from ..models.period import Period


T = TypeVar("T", bound="BalancingEnergyPricesResponse")


@_attrs_define
class BalancingEnergyPricesResponse:
    """
    Attributes:
        queried_period (Period):
        data (list['BalancingEnergyPrices']):
        has_more (bool): Indicates whether there are more results available
        next_cursor (Union[None, Unset, str]): Cursor to fetch the next page of results. Null if no more results.
            Example: v1:AAAAAYwBAgMEBQYHCAkKCw==.
    """

    queried_period: "Period"
    data: list["BalancingEnergyPrices"]
    has_more: bool
    next_cursor: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        queried_period = self.queried_period.to_dict()

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        has_more = self.has_more

        next_cursor: None | Unset | str
        if isinstance(self.next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queriedPeriod": queried_period,
                "data": data,
                "hasMore": has_more,
            }
        )
        if next_cursor is not UNSET:
            field_dict["nextCursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.balancing_energy_prices import BalancingEnergyPrices
        from ..models.period import Period

        d = dict(src_dict)
        queried_period = Period.from_dict(d.pop("queriedPeriod"))

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = BalancingEnergyPrices.from_dict(data_item_data)

            data.append(data_item)

        has_more = d.pop("hasMore")

        def _parse_next_cursor(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor", UNSET))

        balancing_energy_prices_response = cls(
            queried_period=queried_period,
            data=data,
            has_more=has_more,
            next_cursor=next_cursor,
        )

        balancing_energy_prices_response.additional_properties = d
        return balancing_energy_prices_response

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
