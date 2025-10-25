import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.area import Area
from ..models.direction import Direction
from ..models.eic_code import EicCode
from ..models.reserve_type import ReserveType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.balancing_capacity_volume import BalancingCapacityVolume


T = TypeVar("T", bound="BalancingCapacityVolumes")


@_attrs_define
class BalancingCapacityVolumes:
    """
    Attributes:
        area (Area): Area code
        eic_code (EicCode): Energy Identification Code (EIC)
        reserve_type (ReserveType): Reserve type
        direction (Direction): Balancing direction
        volumes (list['BalancingCapacityVolume']):
        procured_at (Union[Unset, datetime.datetime]): **EXPERIMENTAL**: Timestamp when the capacity was procured
            (allocation time or gate closure time).
            Used to distinguish different auctions (e.g., yearly vs hourly, or multiple procurement rounds).
            This field is experimental and may be changed or removed without a deprecation period.
             Example: 2024-08-15T14:30:00Z.
    """

    area: Area
    eic_code: EicCode
    reserve_type: ReserveType
    direction: Direction
    volumes: list["BalancingCapacityVolume"]
    procured_at: Unset | datetime.datetime = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        area = self.area.value

        eic_code = self.eic_code.value

        reserve_type = self.reserve_type.value

        direction = self.direction.value

        volumes = []
        for volumes_item_data in self.volumes:
            volumes_item = volumes_item_data.to_dict()
            volumes.append(volumes_item)

        procured_at: Unset | str = UNSET
        if not isinstance(self.procured_at, Unset):
            procured_at = self.procured_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "area": area,
                "eicCode": eic_code,
                "reserveType": reserve_type,
                "direction": direction,
                "volumes": volumes,
            }
        )
        if procured_at is not UNSET:
            field_dict["procuredAt"] = procured_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.balancing_capacity_volume import BalancingCapacityVolume

        d = dict(src_dict)
        area = Area(d.pop("area"))

        eic_code = EicCode(d.pop("eicCode"))

        reserve_type = ReserveType(d.pop("reserveType"))

        direction = Direction(d.pop("direction"))

        volumes = []
        _volumes = d.pop("volumes")
        for volumes_item_data in _volumes:
            volumes_item = BalancingCapacityVolume.from_dict(volumes_item_data)

            volumes.append(volumes_item)

        _procured_at = d.pop("procuredAt", UNSET)
        procured_at: Unset | datetime.datetime
        if isinstance(_procured_at, Unset):
            procured_at = UNSET
        else:
            procured_at = isoparse(_procured_at)

        balancing_capacity_volumes = cls(
            area=area,
            eic_code=eic_code,
            reserve_type=reserve_type,
            direction=direction,
            volumes=volumes,
            procured_at=procured_at,
        )

        balancing_capacity_volumes.additional_properties = d
        return balancing_capacity_volumes

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
