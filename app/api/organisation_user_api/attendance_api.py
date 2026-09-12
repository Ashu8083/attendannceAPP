import json
import uuid
from datetime import datetime,date
from fastapi import Request, UploadFile, File, Security, Form

from fastapi import  APIRouter
from fastapi import  Depends
from starlette import status
from fastapi import Query
from fastapi.security import HTTPBearer
from app.dependancy.service_dependancy import get_attendance_service
from app.schemas.attendance_schema import PunchInOutSchema, AttendanceResponse, AttendanceUpdate, \
    EmployeeAttendanceMonthResponse
from app.service.attendance_service import AttendanceService
from app.schemas.faceRegister import EmployeeFaceReg
from app.core.response_helper import CommonJSONResponse

bearer_scheme = HTTPBearer()
attendance_router = APIRouter(prefix="/employee/attendance",tags=["Employee Attendance"])


@attendance_router.post(
    "/punch-in",
    response_model= AttendanceResponse,
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
        attendance_response = AttendanceResponse.model_validate(attendance)
        return CommonJSONResponse(
            message="punch-in successfully",
            data=attendance_response,
        )

    return CommonJSONResponse(
        message="Attendance Already Punched",

    )



@attendance_router.post(
    "/punch-out",
    response_model=AttendanceResponse,
)
async def punch_out_attendance(
    request: Request,
    employee_latitude: float,
    employee_longitude: float,
    face_image: UploadFile = File(...),
    credentials=Security(bearer_scheme),
    attendance_service: AttendanceService = Depends(get_attendance_service)
):

    attendacne = (attendance_service
                  .get_today_employee_attendance(employee_id = request.state.auth.employee_id
                                                 ,organisation_id = request.state.auth.organisation_id))
    if attendacne.is_punchout :
        attendance_response = AttendanceResponse.model_validate(attendacne)
        return CommonJSONResponse(
            message="Attendance Already Punched",
            content=attendance_response,
        )
    image_bytes = await face_image.read()
    attendance_punch_out = attendance_service.punch_out_attendance(employee_id = request.state.auth.employee_id
                                                                   ,organisation_id = request.state.auth.organisation_id,
                                                                    employee_latitude = employee_latitude,
                                                                    employee_longitude = employee_longitude
                                                                   ,face_image=image_bytes)
    attendance_response = AttendanceResponse.model_validate(attendance_punch_out)
    return CommonJSONResponse(
        message="Punch-out successfully",
        content=attendance_response,
    )


@attendance_router.get(
    "/self-attendance",
    response_model=AttendanceResponse,
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
    return


@attendance_router.get(
    "/employee/month-attendance",
    response_model=EmployeeAttendanceMonthResponse,
    # dependencies=[
    #     Depends(
    #         PermissionChecker(
    #             "employee.view",
    #             "ORGANISATION"
    #         )
    #     )
    # ]
)
@attendance_router.post(
    "/employee/month-attendance",
    response_model=EmployeeAttendanceMonthResponse,
)
def get_employee_month_attendance(
    request: Request,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
    page: int | None = Query(None, ge=1),
    page_size: int | None = Query(None, ge=1, le=100),
    attendance_service: AttendanceService = Depends(
        get_attendance_service
    ),
):
    return attendance_service.get_employee_month_attendance(
        month=month,
        year=year,
        page=page,
        page_size=page_size,
        organisation_id=request.state.auth.organisation_id,
        employee_id=request.state.auth.employee_id,
    )