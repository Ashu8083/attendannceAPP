import uuid
from urllib import request

from fastapi import  APIRouter,Request,Security
from fastapi import Depends
from fastapi.responses import JSONResponse

from app.auth.permission_check import PermissionChecker
from app.schemas.employee_schema import *
from app.service.employee_services import EmployeeService
from app.dependancy.service_dependancy import get_employee_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

damage_router = APIRouter(prefix="/damage_controll",tags=["DamageController"])

bearer_scheme = HTTPBearer()


@damage_router.post("/add-exiting-employee")
def add_employee_to_organisation(organisation_code :str,
                                 user_email:EmailStr,
                                 employee_details: CreateEmployeeDetails,
                                 credentials=Security(bearer_scheme),
                                 employee_service : EmployeeService = Depends(get_employee_service)) :


    return employee_service.add_existing_user_to_organisation(organisation_code= organisation_code,user_email= user_email,employee_detail_schema = employee_details)

@damage_router.post("/generate-employee-code")#dependencies=[Depends(PermissionChecker("employee.create","ORGANISATION"))])
def generate_employee_code(organisation_code :str,
                           credentials=Security(bearer_scheme),
                           employee_service :EmployeeService = Depends(get_employee_service)) -> str :

    return employee_service.generate_employee_code(organisation_code)


