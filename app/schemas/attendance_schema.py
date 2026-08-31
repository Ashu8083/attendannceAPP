from datetime import datetime,time,date
import uuid

from pydantic import BaseModel, ConfigDict

from app.enums.attandance_status import AttendanceStatus
from app.enums.work_mode import WorkMode




class PunchInOutSchema(BaseModel):
    employee_latitude: float
    employee_longitude: float

class AttendanceResponse(BaseModel):

    id: uuid.UUID
    employee_id: uuid.UUID
    organisation_id: uuid.UUID
    attendance_date: date
    model_config = ConfigDict(from_attributes=True)

class AttendanceUpdate(BaseModel):

    employee_code: str
    status: AttendanceStatus | None = None
    punchin_time: time | None = None
    punchout_time: time | None = None
    work_mode: WorkMode | None = None
    date: date