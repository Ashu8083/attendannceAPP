import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.enums.leave_status import LeaveStatus


# Employee applies for leave
class LeaveCreate(BaseModel):
    employee_id: uuid.UUID | None
    start_date: date
    end_date: date
    reason: str = Field(min_length=5, max_length=300)


# Manager/Admin approves or rejects leave
class LeaveApprovalStatus(BaseModel):
    status: LeaveStatus


# Update leave before it is approved
class LeaveUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = Field(default=None, min_length=5, max_length=500)


# Response schema
class LeaveResponse(BaseModel):
    id: uuid.UUID
    start_date: date
    end_date: date
    reason: str
    status: LeaveStatus
    approved_by: Optional[uuid.UUID] = None
    approved_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
class LeaveApproval(BaseModel):
    leave_id : uuid.UUID
    employee_id: uuid.UUID

class LeaveRecordResponse(BaseModel):
    employee_code : str
    leave_response : LeaveResponse