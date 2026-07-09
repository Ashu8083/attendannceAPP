from fastapi import  APIRouter,Depends,Request
from datetime import  date

from app.core.logging_config import logger
from app.dependancy.service_dependancy import get_attendance_service
from app.schemas.attendance_schema import AttendanceUpdate,AttendanceResponse
from app.auth.permission_check import PermissionChecker
from app.service.attendance_service import AttendanceService

attendance_manager = APIRouter(prefix="/attendance-manage",tags=["attendance management"])


@attendance_manager.put("/update",response_model=AttendanceResponse,dependencies=[Depends(PermissionChecker("attendance.update"))])
def update_attendance(request : Request, attendance_update_schema : AttendanceUpdate , attendance_service : AttendanceService = Depends(get_attendance_service) ):
    attendance_update = attendance_service.update_employee_attendance(organisation_id= request.state.auth.organisation_id,attendance_update_schema = attendance_update_schema)
    if attendance_update:
        logger.info(f"attendance updated by {request.state.auth.user_id} from {request.state.auth.organisation_id} organisation  for {attendance_update_schema.dict()}")

    return attendance_update
@attendance_manager.get("/abesent-list",dependencies=[Depends(PermissionChecker("attendance.view"))])
def absent_list(attendance_date :date ,request : Request,attendance_service : AttendanceService = Depends(get_attendance_service) ):
    absent_list  =attendance_service.absent_employee(
        attendance_date = attendance_date,organisation_id = request.state.auth.organisation_id
    )
    return absent_list
@attendance_manager.post("/mark-absent",response_model=AttendanceResponse,dependencies=[Depends(PermissionChecker("attendance.update"))])
def mark_absent(attendance_date :date ,employee_code : str,request : Request,attendance_service : AttendanceService = Depends(get_attendance_service)):

    return attendance_service.marked_absent_employee(organisation_id= request.state.auth.organisation_id, employee_code = employee_code , attendance_date = attendance_date)

@attendance_manager.delete("/delete-attendance",response_model=AttendanceResponse,dependencies=[Depends(PermissionChecker("attendance.update"))])
def delete_attendance():
    return