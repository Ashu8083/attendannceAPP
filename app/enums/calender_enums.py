from enum import Enum

class HolidayType(str, Enum):

    NATIONAL = 'NATIONAL'
    ORGANIZATION = 'ORGANIZATION'
    OTHER = 'OTHER'


class HolidayStatus(str, Enum):
    CANCELED = 'CANCELED'
    SUSPENDED = 'SUSPENDED'
    ACTIVE = 'ACTIVE'

