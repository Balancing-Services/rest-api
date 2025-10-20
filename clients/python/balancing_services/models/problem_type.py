from enum import Enum


class ProblemType(str, Enum):
    FORBIDDEN = "forbidden"
    INTERNAL_ERROR = "internal-error"
    INVALID_PARAMETER = "invalid-parameter"
    MISSING_PARAMETER = "missing-parameter"
    NOT_IMPLEMENTED = "not-implemented"
    RATE_LIMITED = "rate-limited"
    UNAUTHORIZED = "unauthorized"

    def __str__(self) -> str:
        return str(self.value)
