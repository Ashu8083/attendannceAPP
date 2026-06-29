from typing import Optional

from pydantic import BaseModel,EmailStr,ConfigDict

from datetime import date

from app.enums.user_status_enums import UserStatus
from app.enums.role_enums import UserRole
from app.schemas.organisation_schema import OrganisationNameResponse


class UserCreation(BaseModel): # for only org_admin creation 
    full_name : str
    email : EmailStr
    organisation_code : str
    role : Optional[UserRole] = UserRole.USER


class UserUpdate(BaseModel):
    full_name :Optional[str] = None
    email : Optional[EmailStr] = None
    password_hash : Optional[str] = None
    organisation_code : Optional[str] = None
    role : Optional[str] = None
    join_date :Optional[date] = None

class UserStatusUpdate(BaseModel):
    status : UserStatus

class UserUpdatePassword(BaseModel):
    email :EmailStr
    password_hash : str

class UserDetailsRespone(BaseModel):
    full_name :str
    email : EmailStr
    role : UserRole
    status : UserStatus

    organisation :OrganisationNameResponse
    model_config =ConfigDict(from_attributes=True)




    