from enum import Enum 

class UserRole(str, Enum):

    ADMIN = "ADMIN"
    ORG_ADMIN = "ORG_ADMIN"
    HR = "HR"
    MANAGER = "MANAGER"
    TEAM_LEAD = "TEAM_LEAD"
    ACCOUNTANT = "ACCOUNTANT"
    EMPLOYEE = "EMPLOYEE"