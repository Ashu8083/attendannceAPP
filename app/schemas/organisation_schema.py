from pydantic import BaseModel

from datetime import date,datetime

from enums.employee_status import EmployeeStatus
from models.employee_models import Employee

class CreateOrganisation(BaseModel) :  
    organisation_name :str
    employee_code :str
    organisation_status : EmployeeStatus
    

class OrgnisationDetails(BaseModel):

    organisation_name :str
    employee_code :str
    organisation_status : EmployeeStatus

class OrganisationUpdateStatus(BaseModel):
    organisation_name :str
    organisation_status : EmployeeStatus