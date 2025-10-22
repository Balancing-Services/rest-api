import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.period import Period


T = TypeVar("T", bound="BalancingCapacityVolume")


@_attrs_define
class BalancingCapacityVolume:
    """
    Attributes:
        period (Period):
        volume (float): Volume in MW Example: 50.0.
        procured_at (Union[Unset, datetime.datetime]): **EXPERIMENTAL**: Timestamp when the capacity was procured
            (allocation time or gate closure time).
            Used to distinguish different auctions (e.g., yearly vs hourly, or multiple procurement rounds).
            This field is experimental and may be changed or removed without a deprecation period.
             Example: 2024-08-15T14:30:00Z.
    """

    period: "Period"
    volume: float
    procured_at: Unset | datetime.datetime = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period.to_dict()

        volume = self.volume

        procured_at: Unset | str = UNSET
        if not isinstance(self.procured_at, Unset):
            procured_at = self.procured_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "volume": volume,
            }
        )
        if procured_at is not UNSET:
            field_dict["procuredAt"] = procured_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.period import Period

        d = dict(src_dict)
        period = Period.from_dict(d.pop("period"))

        volume = d.pop("volume")

        _procured_at = d.pop("procuredAt", UNSET)
        procured_at: Unset | datetime.datetime
        if isinstance(_procured_at, Unset):
            procured_at = UNSET
        else:
            procured_at = isoparse(_procured_at)

        balancing_capacity_volume = cls(
            period=period,
            volume=volume,
            procured_at=procured_at,
        )

        balancing_capacity_volume.additional_properties = d
        return balancing_capacity_volume

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
