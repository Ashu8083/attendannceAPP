from datetime import datetime,time
from pydantic import  BaseModel,EmailStr



class OTPSchema(BaseModel):
    otp: str
    user_email: EmailStr





# class CreateOTPSchema(BaseModel):
#     email: EmailStr
#     otp: int
#     expire_time: time
#     is_expire : bool = False

