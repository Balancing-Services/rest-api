from enum import Enum


class Currency(str, Enum):
    BGN = "BGN"
    EUR = "EUR"

    def __str__(self) -> str:
        return str(self.value)
