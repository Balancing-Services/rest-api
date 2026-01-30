from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.area import Area
from ..models.eic_code import EicCode
from ..models.reserve_type import ReserveType

if TYPE_CHECKING:
    from ..models.balancing_capacity_volume import BalancingCapacityVolume


T = TypeVar("T", bound="CrossZonalVolumes")


@_attrs_define
class CrossZonalVolumes:
    """
    Attributes:
        from_area (Area): Area code
        from_eic_code (EicCode): Energy Identification Code (EIC)
        to_area (Area): Area code
        to_eic_code (EicCode): Energy Identification Code (EIC)
        reserve_type (ReserveType): Reserve type
        volumes (list[BalancingCapacityVolume]):
    """

    from_area: Area
    from_eic_code: EicCode
    to_area: Area
    to_eic_code: EicCode
    reserve_type: ReserveType
    volumes: list[BalancingCapacityVolume]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_area = self.from_area.value

        from_eic_code = self.from_eic_code.value

        to_area = self.to_area.value

        to_eic_code = self.to_eic_code.value

        reserve_type = self.reserve_type.value

        volumes = []
        for volumes_item_data in self.volumes:
            volumes_item = volumes_item_data.to_dict()
            volumes.append(volumes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fromArea": from_area,
                "fromEicCode": from_eic_code,
                "toArea": to_area,
                "toEicCode": to_eic_code,
                "reserveType": reserve_type,
                "volumes": volumes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.balancing_capacity_volume import BalancingCapacityVolume

        d = dict(src_dict)
        from_area = Area(d.pop("fromArea"))

        from_eic_code = EicCode(d.pop("fromEicCode"))

        to_area = Area(d.pop("toArea"))

        to_eic_code = EicCode(d.pop("toEicCode"))

        reserve_type = ReserveType(d.pop("reserveType"))

        volumes = []
        _volumes = d.pop("volumes")
        for volumes_item_data in _volumes:
            volumes_item = BalancingCapacityVolume.from_dict(volumes_item_data)

            volumes.append(volumes_item)

        cross_zonal_volumes = cls(
            from_area=from_area,
            from_eic_code=from_eic_code,
            to_area=to_area,
            to_eic_code=to_eic_code,
            reserve_type=reserve_type,
            volumes=volumes,
        )

        cross_zonal_volumes.additional_properties = d
        return cross_zonal_volumes

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
