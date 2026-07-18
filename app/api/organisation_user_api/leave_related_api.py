from fastapi import  APIRouter,Depends,Request

from app.auth.permission_check import PermissionChecker
from app.models import LeaveRequest
from app.schemas.leave_request_schema import LeaveCreate, LeaveResponse
from app.dependancy.service_dependancy import get_leave_service
from app.service import leave_service
from app.service.leave_service import LeaveService
from app.schemas.leave_request_schema import LeaveCreate, LeaveResponse

leave_request_router = APIRouter(
    prefix="/leave-request",
    tags=["leave-request"],
)
@leave_request_router.post("/request-leave",response_model=LeaveResponse,dependencies=[Depends(PermissionChecker("leave.request.view","ORGANISATION"))])
def create_leave_request(leave_request_schema : LeaveCreate,request : Request, leave_service: LeaveService = Depends(get_leave_service))  :
    leave_request_schema = leave_request_schema.employee_id == request.state.auth.employee_id
    return  leave_service.apply_leave(leave_request_schema)

@leave_request_router.get("/leave-list",response_model=LeaveResponse,dependencies=[Depends(PermissionChecker("leave.self.request","ORGANISATION"))])
def get_employee_leave_list(request: Request, leave_service: LeaveService = Depends(get_leave_service)) :
    return leave_service.get_employee_leave(request.state.auth.employee_id,organisation_id=request.state.auth.organisation_id)

