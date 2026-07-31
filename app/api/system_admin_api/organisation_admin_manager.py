from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.dependancy.service_dependancy import get_employee_service
from app.schemas.employee_schema import(CreateEmployee,
                                        EmployeeResponse)

from app.service.employee_services import EmployeeService
from app.auth.permission_check import PermissionChecker
from app.models import Employee
from app.schemas.employee_schema import CreateAdminEmployee

admin_employee_route = APIRouter(prefix="/organisation_admin",tags=["Organisation Admin"])

@admin_employee_route.post("/create-organisation-admin/{organisation_code}" ) #dependencies=[Depends(PermissionChecker("admin.manager","SYSTEM"))])
async def create_organisation_admin(admin_schema: CreateAdminEmployee, organisation_code :str ,employee_service : EmployeeService = Depends(get_employee_service)):

     return await employee_service.create_admin_service(organisation_code = organisation_code , admin_schema=admin_schema)

@admin_employee_route.put("/assign-admin/{organisation_id}")
def assign_admin(employee_code:str,organisation_code :str,employee_service : EmployeeService = Depends(get_employee_service) ):
    return employee_service.assign_admin(organisation_code ,employee_code)

# @admin_employee_route.delete("/remove-admin/{organisation_id}")
# def remove_admi

@admin_employee_route.post("/create-employee-existing-user")
def create_employee(employee: CreateEmployee,):
    return
