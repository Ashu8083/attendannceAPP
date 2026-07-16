from enum import Enum

class PermissionScopEnum(str, Enum):
    ORGANIZATION = "organization"
    SYSTEM_ADMIN = "system_admin"

class PermissionScopEnumUpdate(str, Enum):
    ORGANIZATION = "ORGANISATION"
    SYSTEM = "SYSTEM"