
import uuid
from datetime import datetime,date
from fastapi import  Request

from fastapi import  APIRouter
from fastapi import  Depends
from fastapi.responses import JSONResponse
from starlette import status
from fastapi import UploadFile, File

from app.auth.permission_check import PermissionChecker
from app.models.attendance_record_model import Attendance
from app.dependancy.service_dependancy import get_attendance_service
from app.schemas.attendance_schema import PunchInOutSchema, AttendanceResponse, AttendanceUpdate
from app.service import attendance_service
from app.service.attendance_service import AttendanceService

attendance_router = APIRouter(prefix="/employee/attendance",tags=["attendance"])


@attendance_router.post("/punch-in"
                    ,response_model=AttendanceResponse
                    ,dependencies=[Depends(PermissionChecker("employee.self.punchIn"))])

async def punch_in_attendance(request: Request,image: UploadFile = File(...),attendance_service : AttendanceService = Depends(get_attendance_service)  ):
    attendance : Attendance = attendance_service.get_today_employee_attendance(employee_id = request.state.auth.employee_id,organisation_id = request.state.auth.organisation_id)
    image_byte = await image.read()
    if not attendance:
        return attendance_service.punch_in_attendance(employee_id = request.state.auth.employee_id,organisation_id = request.state.auth.organisation_id,image = image_byte)

    return JSONResponse(content="you are already punchin",
                 status_code=status.HTTP_201_CREATED)




@attendance_router.post("/punch-out"
                        ,response_model=AttendanceResponse
                        ,dependencies=[Depends(PermissionChecker("employee.self.punchOut"))])
def punch_out_attendance(punch_out :PunchInOutSchema
                          ,request: Request
                          ,image: UploadFile = File(...)
                          ,attendance_service : AttendanceService = Depends(get_attendance_service) ):
    
    attendacne = (attendance_service
                  .get_today_employee_attendance(punch_out.employee_id
                                                 ,organisation_id = request.state.auth.organisation_id))
    if attendacne.is_punchout :
        return JSONResponse(content="today attendance already taken")
    return attendance_service.punch_out_attendance(punch_out,organisation_id = request.state.auth.organisation_id)




@attendance_router.get("/attendance",dependencies=[Depends(PermissionChecker("employee.self.view"))])
def attendance_view(request : Request,attendance_date : date, attendance_service : AttendanceService = Depends(get_attendance_service)):

    return attendance_service.get_employee_attendance_by_date(attendance_date,organisation_id = request.state.auth.organisation_id, employee_id = request.state.auth.employee_id)









# @attendance_router.put("/update-employee-attendance/{organisation_id}"
#                         ,dependencies=[Depends(PermissionChecker("employee.update"))])
# def update_employee_attendance(
#         organisation_id : uuid.UUID,
#         attendance_update : AttendanceUpdate,
#         service : AttendanceService = Depends(get_attendance_service)
# ):
#     return service.update_employee_attendance(organisation_id,attendance_update)

# @attendance_router.delete("/employee-attendance",response_model=AttendanceResponse)
# def employee_attendance(
# ):
#     return

# @attendance_router.get("/today-attendance/{organisation_id}"
#                         ,dependencies=[Depends(PermissionChecker("employee.today"))])
# def get_employee_attendance(organisation_id : uuid.UUID ,attendance_service: AttendanceService = Depends(get_attendance_service)):
#     return attendance_service.get_today_attendace(organisation_id = request.state.auth.organisation_id)