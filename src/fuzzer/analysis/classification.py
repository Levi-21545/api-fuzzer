from enum import Enum, auto

class Anomaly(Enum):
    SERVER_ERROR = auto()
    SUCCESS_CONTRADICTION = auto()
    UNEXPECTED_SUCCESS = auto()
    ERROR_CONTRADICTION = auto()
    UNEXPECTED_ERROR_STATUS = auto()
    EXPECTED_FAILURE = auto()
    CONFORMANT_SUCCESS = auto()


class AnomalySeverity(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
