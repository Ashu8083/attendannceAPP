import json
import uuid
from datetime import datetime,date
from fastapi import Request, UploadFile, File, Security, Form

from fastapi import  APIRouter
from fastapi import  Depends
from fastapi.responses import JSONResponse
from starlette import status
from fastapi import Query
from fastapi.security import HTTPBearer
from app.auth.permission_check import PermissionChecker
from app.models.attendance_record_model import Attendance
from app.dependancy.service_dependancy import get_attendance_service
from app.schemas.attendance_schema import PunchInOutSchema, AttendanceResponse, AttendanceUpdate
from app.service import attendance_service
from app.core.logging_config import logger
from app.service.attendance_service import AttendanceService
from app.schemas.faceRegister import EmployeeFaceReg
from app.schemas.commonResponse import CommonResponse, PaginatedResponse

bearer_scheme = HTTPBearer()
attendance_router = APIRouter(prefix="/employee/attendance",tags=["Employee Attendance"])


@attendance_router.post(
    "/punch-in",
    response_model=CommonResponse[AttendanceResponse],
    status_code=status.HTTP_201_CREATED
)
async def punch_in_attendance(
    request: Request,
    employee_latitude: float,
    employee_longitude: float,
    face_image: UploadFile = File(...),
    credentials=Security(bearer_scheme),
    attendance_service: AttendanceService = Depends(get_attendance_service)
):
    image_bytes = await face_image.read()

    attendance = attendance_service.get_today_employee_attendance(
        employee_id=request.state.auth.employee_id,
        organisation_id=request.state.auth.organisation_id
    )

    if not attendance:
        attendance = await attendance_service.punch_in_attendance(
            employee_id=request.state.auth.employee_id,
            organisation_id=request.state.auth.organisation_id,
            employee_latitude=employee_latitude,
            employee_longitude=employee_longitude,
            face_image=image_bytes
        )

        return CommonResponse(
            message="Punch in successfully",
            data=attendance
        )

    return CommonResponse(
        message="Today's attendance already exists",
        data=attendance
    )


@attendance_router.post(
    "/punch-out",
    response_model=CommonResponse[AttendanceResponse]
)
async def punch_out_attendance(
    request: Request,
    employee_latitude: float,
    employee_longitude: float,
    image_file: UploadFile = File(...),
    credentials=Security(bearer_scheme),
    attendance_service: AttendanceService = Depends(get_attendance_service)
):

    attendacne = (attendance_service
                  .get_today_employee_attendance(employee_id = request.state.auth.employee_id
                                                 ,organisation_id = request.state.auth.organisation_id))
    if attendacne.is_punchout :
        return JSONResponse(content="today attendance already taken")
    image_bytes = await image_file.read()
    attendance_punch_out = attendance_service.punch_out_attendance(employee_id = request.state.auth.employee_id,organisation_id = request.state.auth.organisation_id,
                                                             employee_latitude = employee_latitude,
                                                             employee_longitude = employee_longitude,face_image=image_bytes)

    return CommonResponse(
        message="Punch out attendance successfully punched",
        data=attendance_punch_out,
    )




@attendance_router.get(
    "/self-attendance",
    response_model=CommonResponse[AttendanceResponse],
)
    # dependencies=[
    #     Depends(PermissionChecker("employee:view", "ORGANISATION"))
    # ]

def attendance_view(
    request: Request,
    attendance_date: date,
    attendance_service: AttendanceService = Depends(get_attendance_service)
):
    data = attendance_service.get_employee_attendance_by_date(
        attendance_date,
        organisation_id=request.state.auth.organisation_id,
        employee_id=request.state.auth.employee_id
    )
    return CommonResponse(
        message="Attendance fetched successfully",
        data=data
    )
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
    return


@attendance_router.get(
    "/employee/month-attendance",
    response_model=CommonResponse[list[AttendanceResponse]],
    # dependencies=[
    #     Depends(
    #         PermissionChecker(
    #             "employee.view",
    #             "ORGANISATION"
    #         )
    #     )
    # ]
)
def get_employee_month_attendance(
    request: Request,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    attendance_service: AttendanceService = Depends(
        get_attendance_service
    )
):
    data = attendance_service.get_employee_month_attendance(
        month=month,
        year=year,
        page=page,
        page_size=page_size,
        organisation_id=request.state.auth.organisation_id,
        employee_id=request.state.auth.employee_id
    )

    return CommonResponse(
        message="Monthly attendance fetched successfully",
        data=data
    )