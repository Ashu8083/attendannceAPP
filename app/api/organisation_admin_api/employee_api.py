import uuid
from urllib import request

from fastapi import APIRouter, Request, Security
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from app.auth.permission_check import PermissionChecker
from app.schemas.employee_schema import *
from app.service.employee_services import EmployeeService
from app.dependancy.service_dependancy import get_employee_service

employee_router = APIRouter(prefix="/employees",tags=["employees"])
bearer_scheme = HTTPBearer()

@employee_router.get("/create-employee-employeecode")
def create_employee_code(
    request : Request,
    credentials=Security(bearer_scheme),
    employee_service : EmployeeService = Depends(get_employee_service),
):
    employee_code = employee_service.generate_employee_code_by_organisation_id(oranisation_id= request.state.auth.organisation_id)
    return employee_code

@employee_router.post("/create-employee",response_model=EmployeeResponse)
async def create_employee(
    data : CreateEmployee ,
    request : Request,
    credentials=Security(bearer_scheme),
    employee_service : EmployeeService = Depends (get_employee_service),
  
    ):
    employee = await employee_service.create_employee_service(organisation_id=request.state.auth.organisation_id, employee_schema=data)
    
    return employee

@employee_router.get("/get-employee",response_model=EmployeeDetailsResponce,dependencies=[Depends(PermissionChecker("employee.view","ORGANISATION"))])
def get_employee(
    employee_code: str,
    request : Request,
    employee_service : EmployeeService = Depends(get_employee_service)
):
    employee = employee_service.get_employee_service(organisation_id= request.state.auth.oranisation_id ,employee_code= employee_code)
    if not employee:
        return JSONResponse(content = "Employee not found"
                     ,status_code=400)
    return employee


@employee_router.put("/update-employee-details/{employee_code}",dependencies=[Depends(PermissionChecker("employee.update","ORGANISATION"))])
def update_employee(
    employee_code :str ,
    employee_data : EmployeeDetailsUpdate,
    request : Request,
    employee_service : EmployeeService = Depends(get_employee_service)
):
    return employee_service.update_employee_service(organisation_id= request.state.auth.oranisation_id,employeeDetailsSchema= employee_data, employee_code= employee_code)

@employee_router.put("/update-employee-status/{employee_code}",dependencies=[Depends(PermissionChecker("employee.update","ORGANISATION"))])
def update_employee_status(
        employee_code : str,
        request : Request,
        employee_data: EmployeeStatusUpdate,
        employee_service : EmployeeService = Depends(get_employee_service)
):

    return employee_service.update_employee_status_service(organisation_id= request.state.auth.oranisation_id,employee_status_update=employee_data,employee_code=employee_code)

@employee_router.delete("/delete-employee/{employee_code}",dependencies=[Depends(PermissionChecker("employee.delete","ORGANISATION"))])
def delete_employee(
        employee_code : str,
        employee_service : EmployeeService = Depends(get_employee_service)
):

    return employee_service.delete_employee_service()

@employee_router.get("/get-all-employees",dependencies=[Depends(PermissionChecker("employee.view","ORGANISATION"))])
def get_employee_service(
        request : Request,
        employee_service : EmployeeService = Depends(get_employee_service)
):
    return employee_service.get_all_employee_service(organisation_id= request.state.auth.organisation_id)


#=================================================================================================
##=====================================     Assign Role       ====================================
##================================================================================================

@employee_router.post("/assign-role-to-employee",
                      response_model=EmployeeDetailsResponce)
def assign_role_to_employee(
        employee_code : str,
        role_name : str,
        credentials=Security(bearer_scheme),
        employee_service : EmployeeService = Depends(get_employee_service)
):
    responses_dv = employee_service.assign_role_to_employee(
        organisation_id= request.state.auth.organisation_id,
        employee_code= employee_code,
        organisation_role_name = role_name
    )
    return responses_dv


