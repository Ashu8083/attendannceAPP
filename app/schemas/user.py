from pydantic import BaseModel,EmailStr

from datetime import date

from enums.user_status_enums import UserStatus

class UserCreation(BaseModel): # for only org_admin creation 
    full_name : str
    email : EmailStr
    organisation_name : str


class UserUpdate(BaseModel):
    full_name :str
    email : EmailStr
    password_hash : str
    organisation_name : str
    role : str
    join_date :date

class UserStatusUpdate(BaseModel):
    status : UserStatus

class UserUpdatePassword(BaseModel):
    email :EmailStr
    password_hash : str

class UserDetailsRespone(BaseModel):
    full_name :str
    email : EmailStr
    organisation_name : str
    role : str
    status : str




    