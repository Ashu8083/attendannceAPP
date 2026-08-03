from typing import Optional
from uuid import UUID
from pydantic import BaseModel,EmailStr

from datetime import date,datetime

from app.enums.employee_status import EmployeeStatus
from app.enums.user_status_enums import UserStatus
from app.models.employee_models import Employee

class CreateEmployeeDetails(BaseModel):
    # employee_code : str
    dob :date
    gender : str
    marital_status: str
    address : str
    city :str
    state :str

class CreateEmployee(BaseModel) :  

    full_name : str
    email : EmailStr
    # password_hash : str

    employee_code : str |None
    employee_status : EmployeeStatus

    department : str | None
    designation : str | None
    join_date : date


    employee_details : CreateEmployeeDetails
class CreateExistingEmployee(BaseModel):
    full_name : str
    email : EmailStr
    employee_code: str
    employee_status: EmployeeStatus


class create_employee_exising_user(CreateEmployee):

    email : EmailStr
    employee_code : str
    employee_status : EmployeeStatus
    organisation_id : UUID



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



class EmployeeResponse(BaseModel):

    full_name: str
    email: EmailStr
    password_hash: str
    employee_code: str

    department: str
    designation: str
    role_id: str

    join_date: date
    dob: date
    gender: str
    marital_status: str
    address: str
    city: str
    state: str

    model_config = {
        "from_attributes": True
    }


class CreateEmployeeDocument(BaseModel):
    full_name : str
    email : EmailStr
    photo_url: str
    aadhaar_document_url:str
    pan_document_url: str
    resume_url:str
    model_config = {
        "from_attributes": True
    }

class CreateEmployeeDocumentResponse(BaseModel):
    full_name : str
    email : EmailStr
    photo_url: str
    aadhaar_document_url:str
    pan_document_url: str
    resume_url:str
    model_config = {
        "from_attributes": True
    }




class EmployeeDetailsUpdate(BaseModel):
    dob: date
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

class EmployeeDetailsResponce(BaseModel):
    
    dob: date
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

    model_config ={
        "from_attributes": True
    }


class CreateAdminEmployee(BaseModel):
    full_name: str
    email: EmailStr
    # password_hash : str
    employee_code: str | None
    employee_status: EmployeeStatus
    department: str | None
    designation: str | None
    join_date: date