import json
import uuid
from datetime import datetime,date
from fastapi import Request, UploadFile, File, Security, Form

from fastapi import  APIRouter
from fastapi import  Depends
from fastapi.responses import JSONResponse
from starlette import status

from fastapi.security import HTTPBearer
from app.auth.permission_check import PermissionChecker
from app.models.attendance_record_model import Attendance
from app.dependancy.service_dependancy import get_attendance_service
from app.schemas.attendance_schema import PunchInOutSchema, AttendanceResponse, AttendanceUpdate
from app.service import attendance_service
from app.service.attendance_service import AttendanceService


bearer_scheme = HTTPBearer()
attendance_router = APIRouter(prefix="/employee/attendance",tags=["Employee Attendance"])


@attendance_router.post("/punch-in"
                    )
                    # ,dependencies=[Depends(PermissionChecker("employee.self.punchIn","ORGANISATION"))])

async def punch_in_attendance(request: Request,
                              punch_in: str = Form(...),
                              face_image: UploadFile = File(...),
                              credentials=Security(bearer_scheme),
                              attendance_service : AttendanceService = Depends(get_attendance_service)  ):
    image_bytes = await face_image.read()
    data = PunchInOutSchema(
        **json.loads(punch_in)
    )
    attendance : Attendance = attendance_service.get_today_employee_attendance(employee_id = request.state.auth.employee_id,organisation_id = request.state.auth.organisation_id)
    if not attendance:
        return  await attendance_service.punch_in_attendance(employee_id = request.state.auth.employee_id
                                                             ,organisation_id = request.state.auth.organisation_id
                                                             ,punch_in_out_schema=data
                                                             ,face_image=image_bytes,)

    return JSONResponse(content="you are already punchin",
                 status_code=status.HTTP_201_CREATED)


@attendance_router.post("/punch-out"
                        ,response_model=AttendanceResponse)
                        # ,dependencies=[Depends(PermissionChecker("employee.self.punchOut","ORGANISATION"))])
async def punch_out_attendance(
                        request: Request,
                        punch_out: str = Form(...),
                        image_file : UploadFile = File(...),
                        credentials=Security(bearer_scheme),
                        attendance_service : AttendanceService = Depends(get_attendance_service) ):
    data = PunchInOutSchema(
        **json.loads(punch_out)
    )

    attendacne = (attendance_service
                  .get_today_employee_attendance(employee_id = request.state.auth.employee_id
                                                 ,organisation_id = request.state.auth.organisation_id))
    if attendacne.is_punchout :
        return JSONResponse(content="today attendance already taken")
    image_bytes = await image_file.read()
    return attendance_service.punch_out_attendance(employee_id = request.state.auth.employee_id,organisation_id = request.state.auth.organisation_id,face_image=image_bytes,punch_out=data)





@attendance_router.get("/self-attendance",response_model=AttendanceResponse,dependencies=[Depends(PermissionChecker("employee.self.view","ORGANISATION"))])
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