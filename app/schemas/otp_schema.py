from datetime import datetime,time
from pydantic import  BaseModel,EmailStr
from app.schemas.user_device_schema import CreateUserDeviceSchema
from app.schemas.userdevice_schema import UserDeviceCreate


class OTPSchema(BaseModel):
    otp: str
    user_email: EmailStr
    user_device: UserDeviceCreate

# class CreateOTPSchema(BaseModel):
#     email: EmailStr
#     otp: int
#     expire_time: time
#     is_expire : bool = False

