
import uuid
from fastapi import  APIRouter
from fastapi import  Depends
from fastapi.responses import JSONResponse
from starlette import status

from app.models.attendance_record_model import Attendance
from app.dependancy.service_dependancy import get_attendance_service
from app.schemas.attendance_schema import PunchInSchema, AttendanceResponse, PunchOutSchema, AttendanceUpdate
from app.service import attendance_service
from app.service.attendance_service import AttendanceService

attendance_router = APIRouter()


@attendance_router.post("/punch-in/{organisation_id}",response_model=AttendanceResponse)

def punch_in_attendance(punch_in :PunchInSchema, organisation_id : uuid.UUID,attendance_service : AttendanceService = Depends(get_attendance_service) ):
    attendance : Attendance = attendance_service.get_today_employee_attendance(punch_in.employee_id,organisation_id)
    print(f"inside the model {attendance}")
    if not attendance:
        return attendance_service.punch_in_attendance(punch_in,organisation_id)


    return JSONResponse(content="you are already punchin",
                 status_code=status.HTTP_201_CREATED)


@attendance_router.post("/punch-out/{organisation_id}",response_model=AttendanceResponse)
def punch_out_attendance(punch_out :PunchOutSchema,organisation_id : uuid.UUID,attendance_service : AttendanceService = Depends(get_attendance_service) ):
    attendacne = attendance_service.get_today_employee_attendance(organisation_id,punch_out.employee_id)
    if attendacne.is_punchout :
        return JSONResponse(content="today attendance already taken")
    return attendance_service.punch_out_attendance(punch_out,organisation_id)

@attendance_router.put("/update-employee-attendance/{organisation_id}")
def update_employee_attendance(
        organisation_id : uuid.UUID,
        attendance_update : AttendanceUpdate,
        service : AttendanceService = Depends(get_attendance_service)
):
    return service.update_employee_attendance(organisation_id,attendance_update)

@attendance_router.delete("/employee-attendance",response_model=AttendanceResponse)
def employee_attendance(
):
    return

@attendance_router.get("/today-attendance/{organisation_id}")
def get_employee_attendance(organisation_id : uuid.UUID ,attendance_service: AttendanceService = Depends(get_attendance_service)):
    return attendance_service.get_today_attendace(organisation_id)