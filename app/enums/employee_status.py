from pydantic import BaseModel
from enum import Enum

class EmployeeStatus(str,Enum):
     ACTIVE = "ACTIVE"
     SUSPENDED = "SUSPENDED"
     DELETE = "DELETE"


