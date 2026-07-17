from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.dependancy.service_dependancy import get_employee_service
from app.schemas.employee_schema import(CreateEmployee,
                                        EmployeeResponse)

from app.service.employee_services import EmployeeService
from app.auth.permission_check import PermissionChecker


employee_route = APIRouter(prefix="organisation_admin",tags=["Organisation Admin"])

@employee_route.post("/create-organisation-admin/{organisation_code}", response_model=EmployeeResponse , dependencies=[Depends(PermissionChecker(""))])
def create_organisation_admin(employee: CreateEmployee, organisation_code :str ,employee_service : EmployeeService = Depends(get_employee_service)):

    return employee_service.create_employee_service_by_organisation_code(organisation_code = organisation_code , employee_schema=employee)


