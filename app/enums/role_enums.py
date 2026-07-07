from enum import Enum 

class UserRole(str, Enum):

    ADMIN = "ADMIN"
    USER = "USER"
    ORG_ADMIN = "ORG_ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"