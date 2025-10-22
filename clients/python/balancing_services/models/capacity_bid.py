from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bid_status import BidStatus

if TYPE_CHECKING:
    from ..models.period import Period


T = TypeVar("T", bound="CapacityBid")


@_attrs_define
class CapacityBid:
    """
    Attributes:
        period (Period):
        capacity (float): Bid capacity in MW Example: 50.
        price (float): Bid price per MW per hour in the specified currency Example: 12.5.
        status (BidStatus): Status of a capacity bid:
            - offered: Bid was offered but not accepted
            - accepted: Bid was accepted (at least partially accepted)
    """

    period: "Period"
    capacity: float
    price: float
    status: BidStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period.to_dict()

        capacity = self.capacity

        price = self.price

        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "capacity": capacity,
                "price": price,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.period import Period

        d = dict(src_dict)
        period = Period.from_dict(d.pop("period"))

        capacity = d.pop("capacity")

        price = d.pop("price")

        status = BidStatus(d.pop("status"))

        capacity_bid = cls(
            period=period,
            capacity=capacity,
            price=price,
            status=status,
        )

        capacity_bid.additional_properties = d
        return capacity_bid

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
