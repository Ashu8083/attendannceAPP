from enum import Enum


class DepartmentStatusEnum (str, Enum):
    ACTIVATE = 'ACTIVATE'
    DEACTIVATE = 'DEACTIVATE'
    DELETED = 'DELETED'
