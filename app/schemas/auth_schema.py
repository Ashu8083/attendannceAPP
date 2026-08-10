from pydantic import BaseModel, EmailStr


class AuthResponse(BaseModel):

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in : int
    permission_list: list[str]

class VerifyOtpResponse(BaseModel):

    success: bool
    message: str
    auth: AuthResponse


class RefreshAccessToken(BaseModel):
    user_email  :EmailStr
    refresh_token : str
    device_unique_id : str
    device_type: str
    fcm_token: str


