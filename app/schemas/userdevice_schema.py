import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserDeviceCreate(BaseModel):

    device_type: str
    device_unique_id: str
    firebaseFCM_token: str


class UserDeviceUpdate(BaseModel):
    firebaseFCM_token: Optional[str] = None
    refresh_token_id: Optional[uuid.UUID] = None
    is_login: Optional[bool] = None
    last_login: Optional[datetime] = None
    logout_time: Optional[datetime] = None


class UserDeviceResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    device_type: str
    device_unique_id: str
    firebaseFCM_token: str
    refresh_token_id: uuid.UUID
    last_login: Optional[datetime] = None
    logout_time: Optional[datetime] = None
    is_login: bool

    model_config = ConfigDict(from_attributes=True)