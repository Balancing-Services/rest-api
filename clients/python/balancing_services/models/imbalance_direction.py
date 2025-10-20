from enum import Enum


class ImbalanceDirection(str, Enum):
    NEGATIVE = "negative"
    POSITIVE = "positive"
    SYMMETRIC = "symmetric"

    def __str__(self) -> str:
        return str(self.value)
