from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.total_imbalance_direction import TotalImbalanceDirection

if TYPE_CHECKING:
    from ..models.period import Period


T = TypeVar("T", bound="TotalImbalanceVolume")


@_attrs_define
class TotalImbalanceVolume:
    """
    Attributes:
        period (Period):
        average_power_mw (float): Average power in MW during the period Example: 60.5.
        direction (TotalImbalanceDirection): Total imbalance volume direction (ENTSO-E regulatory terminology):
            - surplus: Generation exceeds consumption (D > 0, positive imbalance)
            - deficit: Consumption exceeds generation (D < 0, negative imbalance)
            - balanced: Generation equals consumption (D = 0)
    """

    period: "Period"
    average_power_mw: float
    direction: TotalImbalanceDirection
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period.to_dict()

        average_power_mw = self.average_power_mw

        direction = self.direction.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "averagePowerMW": average_power_mw,
                "direction": direction,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.period import Period

        d = dict(src_dict)
        period = Period.from_dict(d.pop("period"))

        average_power_mw = d.pop("averagePowerMW")

        direction = TotalImbalanceDirection(d.pop("direction"))

        total_imbalance_volume = cls(
            period=period,
            average_power_mw=average_power_mw,
            direction=direction,
        )

        total_imbalance_volume.additional_properties = d
        return total_imbalance_volume

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
