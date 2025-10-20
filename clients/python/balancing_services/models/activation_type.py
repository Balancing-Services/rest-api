from enum import Enum


class ActivationType(str, Enum):
    DIRECT = "direct"
    NOT_APPLICABLE = "not_applicable"
    SCHEDULED = "scheduled"

    def __str__(self) -> str:
        return str(self.value)
