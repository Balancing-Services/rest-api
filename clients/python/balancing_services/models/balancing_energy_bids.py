from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.area import Area
from ..models.currency import Currency
from ..models.direction import Direction
from ..models.eic_code import EicCode
from ..models.reserve_type import ReserveType

if TYPE_CHECKING:
    from ..models.energy_bid import EnergyBid


T = TypeVar("T", bound="BalancingEnergyBids")


@_attrs_define
class BalancingEnergyBids:
    """
    Attributes:
        area (Area): Area code
        eic_code (EicCode): Energy Identification Code (EIC)
        reserve_type (ReserveType): Reserve type
        direction (Direction): Balancing direction
        currency (Currency): Currency code
        standard_product (bool): Indicates if this is a European standard balancing product Example: True.
        bids (list['EnergyBid']):
    """

    area: Area
    eic_code: EicCode
    reserve_type: ReserveType
    direction: Direction
    currency: Currency
    standard_product: bool
    bids: list["EnergyBid"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        area = self.area.value

        eic_code = self.eic_code.value

        reserve_type = self.reserve_type.value

        direction = self.direction.value

        currency = self.currency.value

        standard_product = self.standard_product

        bids = []
        for bids_item_data in self.bids:
            bids_item = bids_item_data.to_dict()
            bids.append(bids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "area": area,
                "eicCode": eic_code,
                "reserveType": reserve_type,
                "direction": direction,
                "currency": currency,
                "standardProduct": standard_product,
                "bids": bids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.energy_bid import EnergyBid

        d = dict(src_dict)
        area = Area(d.pop("area"))

        eic_code = EicCode(d.pop("eicCode"))

        reserve_type = ReserveType(d.pop("reserveType"))

        direction = Direction(d.pop("direction"))

        currency = Currency(d.pop("currency"))

        standard_product = d.pop("standardProduct")

        bids = []
        _bids = d.pop("bids")
        for bids_item_data in _bids:
            bids_item = EnergyBid.from_dict(bids_item_data)

            bids.append(bids_item)

        balancing_energy_bids = cls(
            area=area,
            eic_code=eic_code,
            reserve_type=reserve_type,
            direction=direction,
            currency=currency,
            standard_product=standard_product,
            bids=bids,
        )

        balancing_energy_bids.additional_properties = d
        return balancing_energy_bids

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
