import uuid
from datetime import datetime,date

from pydantic import BaseModel

from enums.employee_status import EmployeeStatus


class EmployeeCreate(BaseModel):

    full_name: str
    email :str

    department_id : int
    team_id : uuid.UUID
    organization_branch_id : uuid.UUID
    role_id : uuid.UUID

    supervisor :uuid.UUID
    employee_status : EmployeeStatus

    shift_id : uuid.UUID
    join_date : date


class EmployeeUpdate(BaseModel):

    full_name: str |None = None
    email :str |None = None

    department_id: int |None = None
    team_id: uuid.UUID |None = None
    organization_branch_id: uuid.UUID |None = None

    supervisor: uuid.UUID |None = None
    employee_status: EmployeeStatus |None = None

    shift_id: uuid.UUID |None = None
    join_date: date |None = None


class EmployeeSearchFilter (BaseModel):

    full_name: str |None = None
    email : str |None = None
    department_id : int |None = None
    team_id : uuid.UUID |None = None
    organization_branch_id : uuid.UUID |None = None
    supervisor : uuid.UUID |None = None
    employee_code : str |None = None



class FillEmployeeDetails(BaseModel):

    full_name: str
    dob : date
    gender : str
    marital_status : str
    street : str
    city : str
    state : str

class EmployeeDetailsUpdate(BaseModel):

    full_name : str |None = None
    dob: date |None = None
    gender: str |None = None
    marital_status: str |None = None
    street: str |None = None
    city: str |None = None
    state: str |None = None










