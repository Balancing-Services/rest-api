import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Period")


@_attrs_define
class Period:
    """
    Attributes:
        start_at (datetime.datetime): Start of the period (UTC) Example: 2025-01-01T00:00:00Z.
        end_at (datetime.datetime): End of the period (UTC) Example: 2025-01-01T01:00:00Z.
    """

    start_at: datetime.datetime
    end_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_at = self.start_at.isoformat()

        end_at = self.end_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "startAt": start_at,
                "endAt": end_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_at = isoparse(d.pop("startAt"))

        end_at = isoparse(d.pop("endAt"))

        period = cls(
            start_at=start_at,
            end_at=end_at,
        )

        period.additional_properties = d
        return period

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
