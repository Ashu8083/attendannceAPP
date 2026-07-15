from pydantic import BaseModel

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
    