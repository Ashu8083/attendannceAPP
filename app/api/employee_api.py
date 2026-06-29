from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse

from app.schemas.employee_schema import *
from app.service.employee_services import EmployeeService
from app.dependancy.service_dependancy import get_employee_service

employee_router = APIRouter()

@employee_router.post("/create-employee",response_model=EmployeeDetails)
def create_employee( 
    data : CreateEmployee ,
    employee_service : EmployeeService = Depends (get_employee_service)
    ):
    organisation_id = "testid" 
    employee = employee_service.createEmployee_service(organisation_id = organisation_id ,employeeSchema= data)
    if not employee: 
        return JSONResponse(
            content = "Something Went Wrong",
            status_code = 500
        )
    return employee

@employee_router.get("/get-employee",response_model=EmployeeDetails)
def get_employee(
    employee_code: str,
    employee_service : EmployeeService = Depends(get_employee_service)
):
    organisation_id  = "testid"
    employee = employee_service.get_employee_service(organisation_id= organisation_id ,employee_code= employee_code)
    if not employee:
        return JSONResponse(content = "Employee not found"
                     ,status_code=400)
    return employee



