from enum import Enum


class BidStatus(str, Enum):
    ACCEPTED = "accepted"
    OFFERED = "offered"

    def __str__(self) -> str:
        return str(self.value)
