from enum import Enum


class ReserveType(str, Enum):
    AFRR = "aFRR"
    FCR = "FCR"
    MFRR = "mFRR"
    RR = "RR"

    def __str__(self) -> str:
        return str(self.value)
