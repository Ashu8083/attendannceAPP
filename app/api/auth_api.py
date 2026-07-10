from fastapi import APIRouter, Depends, Form, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from fastapi import  status

from app.dependancy.service_dependancy import get_auth_service
from app.service.auth_service import AuthService
from app.schemas.otp_schema import OTPSchema



auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.post("/otp-login")
async def get_otp_login(back_ground_task : BackgroundTasks ,email : str = Form(...) ,auth_service : AuthService  = Depends(get_auth_service)):
    auth = await auth_service.generate_otp_service(email,background_task=back_ground_task)
    if not auth:
        raise
    return JSONResponse(status_code=status.HTTP_200_OK, content="Otp sent successfully")
@auth_router.post("/otp-verify")
def verify_otp(otp_schema : OTPSchema ,auth_service : AuthService = Depends(get_auth_service)):
    return auth_service.verify_otp(otp_schema)

