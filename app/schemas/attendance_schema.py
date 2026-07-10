from datetime import datetime,time,date
import uuid

from pydantic import BaseModel, ConfigDict

from app.enums.attandance_status import AttendanceStatus
from app.enums.work_mode import WorkMode




class PunchInOutSchema(BaseModel):
    employee_latitude: float
    employee_longitude: float

class AttendanceResponse(BaseModel):
    employee_code: str
    attendance_date: datetime
    punchin_time: datetime | None
    punchout_time: datetime | None
    status: AttendanceStatus
    work_mode: WorkMode

    model_config = ConfigDict(from_attributes=True)

class AttendanceUpdate(BaseModel):

    employee_code: str
    status: AttendanceStatus | None = None
    punchin_time: time | None = None
    punchout_time: time | None = None
    work_mode: WorkMode | None = None
    date: date