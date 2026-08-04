from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from app.enums.device_type_enum import DeviceType



class CreateUserDeviceSchema(BaseModel):

    device_type : DeviceType
    firebaseFCMToken : str
    user_device_unique_id: UUID

class UserCheckDeviceSchema(BaseModel):
    account_type : str
    firebaseFCMToken : str
    user_device_unique_id: UUID
    last_login_at: datetime
    is_active: bool