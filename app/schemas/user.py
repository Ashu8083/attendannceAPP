from typing import Optional

from pydantic import BaseModel,EmailStr,ConfigDict

from datetime import date

from app.enums.user_status_enums import UserStatus
from app.enums.role_enums import UserRole
from app.schemas.organisation_schema import OrganisationNameResponse
from app.enums.role_enums import UserRoleUpdated
from app.enums.scops import AccountType


class UserCreation(BaseModel): # for only org_admin creation 
    full_name : str
    email : EmailStr
    organisation_code : str | None
    role_name : Optional[str] = "SYSTEM_VIEWER"
    account_type : Optional[AccountType] = AccountType.ORGANISATION



class UserUpdate(BaseModel):
    full_name :Optional[str] = None
    email : Optional[EmailStr] = None
    password_hash : Optional[str] = None
    organisation_code : Optional[str] = None
    account_type: Optional[AccountType] = AccountType.SYSTEM
    join_date :Optional[date] = None

class UserStatusUpdate(BaseModel):
    status : UserStatus

class UserUpdatePassword(BaseModel):
    email :EmailStr
    password_hash : str

class UserDetailsRespone(BaseModel):
    full_name :str
    email : EmailStr
    account_type: Optional[AccountType]
    status : UserStatus

    organisation :OrganisationNameResponse
    model_config =ConfigDict(from_attributes=True)






    