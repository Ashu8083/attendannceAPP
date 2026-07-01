from datetime import datetime,date
import uuid

from pydantic import BaseModel, ConfigDict

from app.enums.attandance_status import AttendanceStatus
from app.enums.work_mode import WorkMode


class PunchInSchema(BaseModel):
    employee_id: uuid.UUID
    work_mode: WorkMode

class PunchOutSchema(BaseModel):
    employee_id: uuid.UUID

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
    punchin_time: datetime | None = None
    punchout_time: datetime | None = None
    work_mode: WorkMode | None = None
    date: date