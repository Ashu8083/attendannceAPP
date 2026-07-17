from datetime import time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ShiftCreate(BaseModel):
    name: str = Field(..., max_length=22)
    organisation_id: UUID
    start_time: time
    end_time: time
    grace_minutes: int = Field(..., ge=0)


class ShiftUpdate(BaseModel):
    name: str | None = Field(None, max_length=22)
    start_time: time | None = None
    end_time: time | None = None
    grace_minutes: int | None = Field(None, ge=0)


class ShiftResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # id: int
    name: str
    organisation_id: UUID
    start_time: time
    end_time: time
    grace_minutes: int