from datetime import datetime,time,date
import uuid

from pydantic import BaseModel, ConfigDict

from app.enums.attandance_status import AttendanceStatus
from app.enums.work_mode import WorkMode

class PunchInOutSchema(BaseModel):
    employee_latitude: float
    employee_longitude: float

class PunchInAndPunchOutResponseSchema(BaseModel):
   punchIn_time: time | None = None
   punchout_time: time | None = None

class AttendanceResponse(BaseModel):

    punchin_time: time | None
    punchout_time: time | None
    face_profile  : str | None
    model_config = ConfigDict(from_attributes=True)

class EmployeeAttendanceByMonth(BaseModel):

    employee_code: str
    attendance_date: date
    punchin_time: time | None = None
    punchout_time: time | None = None
    punchin_face_profile: str | None = None
    punchout_face_profile: str | None = None

class EmployeeAttendanceMonthResponse(BaseModel):
    data: list[EmployeeAttendanceByMonth]
    page: int
    page_size: int
    total: int

class AttendanceUpdate(BaseModel):

    employee_code: str
    status: AttendanceStatus | None = None
    punchin_time: time | None = None
    punchout_time: time | None = None
    work_mode: WorkMode | None = None
    date: date