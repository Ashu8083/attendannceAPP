from fastapi import  APIRouter, Depends, Request

from app.schemas.employee_schema import Employee, EmployeeResponse
from app.api.organisation_admin_api.employee_api import get_employee_service
from app.auth.permission_check import PermissionChecker
from app.service.employee_services import EmployeeService

employee_self_router = APIRouter(
    prefix="/organisation-user/employee",
    tags=["organisation-user/employee"]
)
@employee_self_router.get("/employee",response_model= EmployeeResponse,dependencies=[Depends(PermissionChecker("employee.self.view","ORGANISATION"))])
def get_employee_api(request : Request ,employee_service: EmployeeService = Depends(get_employee_service)):
    return employee_service.get_employee_by_empID_service(organisation_id=request.state.auth.organisation_id,employee_id=request.state.auth.employee_id)
