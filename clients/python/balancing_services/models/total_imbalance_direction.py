from enum import Enum


class TotalImbalanceDirection(str, Enum):
    BALANCED = "balanced"
    DEFICIT = "deficit"
    SURPLUS = "surplus"

    def __str__(self) -> str:
        return str(self.value)
