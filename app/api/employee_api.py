import uuid

from fastapi import  APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse

from app.schemas.employee_schema import *
from app.service.employee_services import EmployeeService
from app.dependancy.service_dependancy import get_employee_service

employee_router = APIRouter()

@employee_router.post("/create-employee/{organisation_id}")
def create_employee(
    data : CreateEmployee ,
    organisation_id: uuid.UUID,
    employee_service : EmployeeService = Depends (get_employee_service),
  
    ):
    employee = employee_service.createEmployee_service(organisation_id=organisation_id, employee_schema=data)
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


@employee_router.put("/update-employee-details/{employee_code}")
def update_employee(
    employee_code :str ,
    employee_data : EmployeeDetailsUpdate,
    employee_service : EmployeeService = Depends(get_employee_service)
):
    organisation_id = "test_id"
    return employee_service.update_employee_service(organisation_id= organisation_id,employeeDetailsSchema= employee_data, employee_code= employee_code)

@employee_router.put("/update-employee-status/{employee_code}")
def update_employee_status(
        employee_code : str,
        employee_data: EmployeeStatusUpdate,
        employee_service : EmployeeService = Depends(get_employee_service)
):
    organisation_id = "test_id"
    return employee_service.update_employee_status_service(organisation_id= organisation_id,employee_status_update=employee_data,employee_code=employee_code)

@employee_router.delete("/delete-employee/{employee_code}")
def delete_employee(
        employee_code : str,
        employee_service : EmployeeService = Depends(get_employee_service)
):
    organisation_id = "test_id"
    return employee_service.delete_employee_service()

@employee_router.get("/get-all-employees/{organisation_id}")
def get_employee_service(
        organisation_id : uuid.UUID ,
        employee_service : EmployeeService = Depends(get_employee_service)
):
    return employee_service.get_all_employee_service(organisation_id= organisation_id)