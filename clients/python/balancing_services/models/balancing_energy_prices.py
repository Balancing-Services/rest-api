from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.activation_type import ActivationType
from ..models.area import Area
from ..models.currency import Currency
from ..models.direction import Direction
from ..models.eic_code import EicCode
from ..models.reserve_type import ReserveType

if TYPE_CHECKING:
    from ..models.balancing_energy_price import BalancingEnergyPrice


T = TypeVar("T", bound="BalancingEnergyPrices")


@_attrs_define
class BalancingEnergyPrices:
    """
    Attributes:
        area (Area): Area code
        eic_code (EicCode): Energy Identification Code (EIC)
        reserve_type (ReserveType): Reserve type
        direction (Direction): Balancing direction
        activation_type (ActivationType): Activation type (only applicable for mFRR)
        currency (Currency): Currency code
        standard_product (bool): Indicates if this is a European standard balancing product Example: True.
        prices (list['BalancingEnergyPrice']):
    """

    area: Area
    eic_code: EicCode
    reserve_type: ReserveType
    direction: Direction
    activation_type: ActivationType
    currency: Currency
    standard_product: bool
    prices: list["BalancingEnergyPrice"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        area = self.area.value

        eic_code = self.eic_code.value

        reserve_type = self.reserve_type.value

        direction = self.direction.value

        activation_type = self.activation_type.value

        currency = self.currency.value

        standard_product = self.standard_product

        prices = []
        for prices_item_data in self.prices:
            prices_item = prices_item_data.to_dict()
            prices.append(prices_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "area": area,
                "eicCode": eic_code,
                "reserveType": reserve_type,
                "direction": direction,
                "activationType": activation_type,
                "currency": currency,
                "standardProduct": standard_product,
                "prices": prices,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.balancing_energy_price import BalancingEnergyPrice

        d = dict(src_dict)
        area = Area(d.pop("area"))

        eic_code = EicCode(d.pop("eicCode"))

        reserve_type = ReserveType(d.pop("reserveType"))

        direction = Direction(d.pop("direction"))

        activation_type = ActivationType(d.pop("activationType"))

        currency = Currency(d.pop("currency"))

        standard_product = d.pop("standardProduct")

        prices = []
        _prices = d.pop("prices")
        for prices_item_data in _prices:
            prices_item = BalancingEnergyPrice.from_dict(prices_item_data)

            prices.append(prices_item)

        balancing_energy_prices = cls(
            area=area,
            eic_code=eic_code,
            reserve_type=reserve_type,
            direction=direction,
            activation_type=activation_type,
            currency=currency,
            standard_product=standard_product,
            prices=prices,
        )

        balancing_energy_prices.additional_properties = d
        return balancing_energy_prices

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
