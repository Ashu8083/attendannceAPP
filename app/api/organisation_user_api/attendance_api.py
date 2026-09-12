import json
import uuid
from datetime import datetime, date
from fastapi import Request, UploadFile, File, Security, Form, APIRouter, Depends, Query, status
from fastapi.security import HTTPBearer

from app.dependancy.service_dependancy import get_attendance_service
from app.schemas.attendance_schema import (
    PunchInOutSchema,
    AttendanceResponse,
    AttendanceUpdate,
    EmployeeAttendanceMonthResponse,
)
from app.service.attendance_service import AttendanceService
from app.enums.attandance_status import TypeAttendance
from app.core.response_helper import CommonJSONResponse

bearer_scheme = HTTPBearer()
attendance_router = APIRouter(prefix="/employee/attendance", tags=["Employee Attendance"])


@attendance_router.post(
    "/punch-in",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def punch_in_attendance(
    request: Request,
    employee_latitude: float,
    employee_longitude: float,
    face_image: UploadFile = File(...),
    credentials=Security(bearer_scheme),
    attendance_service: AttendanceService = Depends(get_attendance_service),
):
    image_bytes = await face_image.read()

    existing_attendance = attendance_service.get_today_employee_attendance(
        employee_id=request.state.auth.employee_id,
        organisation_id=request.state.auth.organisation_id,
    )

    if not existing_attendance:
        attendance, storage_path = await attendance_service.punch_in_attendance(
            employee_id=request.state.auth.employee_id,
            organisation_id=request.state.auth.organisation_id,
            employee_latitude=employee_latitude,
            employee_longitude=employee_longitude,
            face_image=image_bytes,
        )
        return CommonJSONResponse(
            message="Punch-in successful",
            content={
                "punchin_time": attendance.punchin_time,
                "punchout_time": attendance.punchout_time,
                "face_profile": storage_path,
            },
            status_code=status.HTTP_201_CREATED,
        )

    return CommonJSONResponse(
        message="Attendance Already Punched",
        content={
            "punchin_time": existing_attendance.punchin_time,
            "punchout_time": existing_attendance.punchout_time,
        },
        status_code=status.HTTP_400_BAD_REQUEST,
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
    attendance_service: AttendanceService = Depends(get_attendance_service),
):
    existing_attendance = attendance_service.get_today_employee_attendance(
        employee_id=request.state.auth.employee_id,
        organisation_id=request.state.auth.organisation_id,
    )
    if not existing_attendance:
        return CommonJSONResponse(
            message="No punch-in record found for today",
            content=None,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if existing_attendance.is_punchout:
        return CommonJSONResponse(
            message="Attendance Already Punched Out",
            content={
                "punchin_time": existing_attendance.punchin_time,
                "punchout_time": existing_attendance.punchout_time,
            },
        )

    image_bytes = await face_image.read()
    attendance_punch_out, storage_path = await attendance_service.punch_out_attendance(
        employee_id=request.state.auth.employee_id,
        organisation_id=request.state.auth.organisation_id,
        employee_latitude=employee_latitude,
        employee_longitude=employee_longitude,
        face_image=image_bytes,
    )
    return CommonJSONResponse(
        message="Punch-out successful",
        content={
            "punchin_time": attendance_punch_out.punchin_time,
            "punchout_time": attendance_punch_out.punchout_time,
            "face_profile": storage_path,
        },
    )


@attendance_router.get(
    "/today",
    response_model=AttendanceResponse,
)
@attendance_router.get(
    "/today-attendance",
    response_model=AttendanceResponse,
)
def get_today_attendance(
    request: Request,
    attendance_service: AttendanceService = Depends(get_attendance_service),
):
    attendance = attendance_service.get_today_employee_attendance(
        employee_id=request.state.auth.employee_id,
        organisation_id=request.state.auth.organisation_id,
    )
    if not attendance:
        return CommonJSONResponse(
            message="No attendance record found for today",
            content=None,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    punchin_face = None
    punchout_face = None
    if hasattr(attendance, "attendance_evidence") and attendance.attendance_evidence:
        for ev in attendance.attendance_evidence:
            if ev.type == TypeAttendance.CHECKIN:
                punchin_face = ev.face_profile_url
            elif ev.type == TypeAttendance.CHECKOUT:
                punchout_face = ev.face_profile_url

    attendance_data = {
        "punchin_time": attendance.punchin_time,
        "punchout_time": attendance.punchout_time,
        "face_profile": punchin_face or punchout_face,
        "is_punchin": attendance.is_punchin,
        "is_punchout": attendance.is_punchout,
        "status": attendance.status,
        "work_mode": attendance.work_mode,
        "attendance_date": attendance.attendance_date,
    }
    return CommonJSONResponse(
        message="Today attendance retrieved successfully",
        content=attendance_data,
    )


from app.helperFunction.date_parser import parse_date_query


@attendance_router.get(
    "/self-attendance",
    response_model=AttendanceResponse,
)
def attendance_view(
    request: Request,
    attendance_date: date = Depends(parse_date_query),
    attendance_service: AttendanceService = Depends(get_attendance_service),
):
    attendance = attendance_service.get_employee_attendance_by_date(
        attendance_date,
        organisation_id=request.state.auth.organisation_id,
        employee_id=request.state.auth.employee_id,
    )
    if not attendance:
        return CommonJSONResponse(
            message=f"No attendance record found for {attendance_date}",
            content=None,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    punchin_face = None
    punchout_face = None
    if hasattr(attendance, "attendance_evidence") and attendance.attendance_evidence:
        for ev in attendance.attendance_evidence:
            if ev.type == TypeAttendance.CHECKIN:
                punchin_face = ev.face_profile_url
            elif ev.type == TypeAttendance.CHECKOUT:
                punchout_face = ev.face_profile_url

    return CommonJSONResponse(
        message="Attendance retrieved successfully",
        content={
            "punchin_time": attendance.punchin_time,
            "punchout_time": attendance.punchout_time,
            "face_profile": punchin_face or punchout_face,
            "is_punchin": attendance.is_punchin,
            "is_punchout": attendance.is_punchout,
            "status": attendance.status,
            "work_mode": attendance.work_mode,
            "attendance_date": attendance.attendance_date,
        },
    )


@attendance_router.get(
    "/employee/month-attendance",
    response_model=EmployeeAttendanceMonthResponse,
)
def get_employee_month_attendance(
    request: Request,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
    page: int | None = Query(None, ge=1),
    page_size: int | None = Query(None, ge=1, le=100),
    attendance_service: AttendanceService = Depends(get_attendance_service),
):
    return attendance_service.get_employee_month_attendance(
        month=month,
        year=year,
        page=page,
        page_size=page_size,
        organisation_id=request.state.auth.organisation_id,
        employee_id=request.state.auth.employee_id,
    )