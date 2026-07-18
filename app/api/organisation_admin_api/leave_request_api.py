from fastapi import APIRouter,Depends,Request

from app.auth.permission_check import PermissionChecker
from app.models import LeaveRequest
from app.schemas.leave_request_schema import *
from app.dependancy.service_dependancy import get_leave_service
from app.schemas.leave_request_schema import LeaveRecordResponseList
from app.service.leave_service import LeaveService

leave_manage_router = APIRouter(prefix="/leave-management", tags=["Leave Management"])

@leave_manage_router.get("/leave-approval/pending", response_model=List[type[LeaveResponseWithEmployeeCode]], dependencies=[Depends(PermissionChecker("leave.view","ORGANISATION"))])
def get_pending_leaves(request : Request , leave_record_service = Depends(get_leave_service)):
    return leave_record_service.get_pending_leaves(organisation_id= request.state.auth.organisation_id)

@leave_manage_router.get("/leave-approval/pending/{employee_code}", response_model=LeaveRecordResponseList,dependencies=[Depends(PermissionChecker("leave.view","ORGANISATION"))])
def get_employee_leave_by_employee_id(request: Request ,employee_code : str, leave_request_service :LeaveService = Depends(get_leave_service)) -> LeaveRecordResponseList:
    return leave_request_service.get_employee_pending_leave(employee_code =employee_code ,organisation_id= request.state.organisation_id)


@leave_manage_router.get("/leave-approval/approve/{department}", response_model=LeaveResponseWithEmployeeCode,dependencies=[Depends(PermissionChecker("leave.approve","ORGANISATION"))])
def get_approved_leave() -> LeaveRequest:
    return LeaveRequest()
@leave_manage_router.get("/leave-approval/rejected", response_model=LeaveResponse,dependencies=[Depends(PermissionChecker("leave.reject","ORGANISATION"))])
def get_rejected_leave(employee_id : int) -> LeaveRequest:
    return LeaveRequest()

@leave_manage_router.get("/leave-approval/{department_name}", response_model=LeaveResponseWithEmployeeCode,dependencies=[Depends(PermissionChecker("leave.veiw","ORGANISATION"))])
def get_leave_by_department_id(department_name : str,request : Request, leave_request_service = Depends(get_leave_service)) :
    return leave_request_service.get_leave_by_department_id(department_name ,request.state.auth.organisation_id)

@leave_manage_router.put("/leave-update/{employee_code}", response_model=LeaveResponse,dependencies=[Depends(PermissionChecker("leave.update","ORGANISATION"))])
def update_leave(employee_code : str) -> LeaveRequest:
    return LeaveRequest()
@leave_manage_router.put("/leave-approval/{employee_code}", response_model=LeaveResponse)
def approve_leave(employee_code : str) -> LeaveRequest:
    return LeaveRequest()



