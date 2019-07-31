from enum import Enum


class S(Enum):
    IDLE = 1
    IDLE_CONFIRM = 2
    ERROR = 3
    BUSY = 4
    BUSY_USER = 5
