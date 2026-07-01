from typing import Optional

from pydantic import BaseModel,EmailStr

from datetime import date,datetime

from app.enums.employee_status import EmployeeStatus
from app.enums.user_status_enums import UserStatus
from app.models.employee_models import Employee

class CreateEmployee(BaseModel) :  

    full_name : str
    email : EmailStr
    password_hash : str
    employee_code : str


    department : str
    designation : str
    role_id : str
    user_status :UserStatus

    join_date : date
    emplopyee_status : EmployeeStatus

    dob :date
    gender : str
    marital_status: str
    address : str
    city :str
    state :str

class EmployeeDetails(BaseModel):
    employee_code : str
    dob :date
    gender : str
    marital_status: str
    address : str
    city :str
    state :str
    

class CreateEmployeeDocuments(BaseModel):
    employee_code: str
    photo_url : str
    aadhaar_document_url : str
    pancard_documents_url : str
    resume_url :str



class EmployeeUpdate(BaseModel):
    user_name :str
    employee_code :str
    emplopyee_status : EmployeeStatus
    email : EmailStr
    password_hash : str
    emplopyee_code :str
    department : str
    designation : str
    join_date : date
    emplopyee_status : EmployeeStatus

class EmployeeStatusUpdate(BaseModel):

    employee_status :EmployeeStatus

class EmployeeDetailsUpdate(BaseModel):

    dob :date
    gender : Optional[str] = None
    marital_status: Optional[str] = None
    address : Optional[str] = None
    city :Optional[str] = None
    state :Optional[str] = None