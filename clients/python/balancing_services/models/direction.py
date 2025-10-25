from enum import Enum


class Direction(str, Enum):
    DOWN = "down"
    SYMMETRIC = "symmetric"
    UP = "up"

    def __str__(self) -> str:
        return str(self.value)
