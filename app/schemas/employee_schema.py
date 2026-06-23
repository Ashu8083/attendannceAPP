from pydantic import BaseModel

from datetime import date,datetime

from enums.employee_status import EmployeeStatus
from models.employee_models import Employee

class CreateEmployee(BaseModel) :  

    emplopyee_code :str
    department : str
    designation : str
    join_date : date
    emplopyee_status : EmployeeStatus

class EmployeDetails(BaseModel):

    user_name : str
    employee_code :str
    department : str
    designation : str
    join_date :date
    employee_status :EmployeeStatus

class EmployeeUpdateStatus(BaseModel):
    user_name :str
    employee_code :str
    emplopyee_status : EmployeeStatus