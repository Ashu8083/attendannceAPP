from enum import Enum


class AccountType(str, Enum):
    SYSTEM = 'SYSTEM'
    ORGANISATION = 'ORGANISATION'


class RoleScops(str, Enum):
    SYSTEM = 'SYSTEM'
    ORGANISATION = 'ORGANISATION'