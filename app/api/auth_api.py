from fastapi import APIRouter,Depends
from app.dependancy.service_dependancy import get_auth_service
from app.service.auth_service import AuthService
from app.schemas.otp_schema import OTPSchema



auth_router = APIRouter()

@auth_router.post("/otp-login/{email}")
def get_otp_login(email : str   , auth_service : AuthService  = Depends(get_auth_service)):


    return auth_service.generate_otp_service(email)
@auth_router.post("/otp-verify/")
def verify_otp(otp_schema : OTPSchema ,auth_service : AuthService = Depends(get_auth_service)):

    return auth_service.verify_otp(otp_schema)

