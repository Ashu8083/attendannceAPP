from fastapi import APIRouter, Depends, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi import  status
from fastapi.encoders import jsonable_encoder

from app.dependancy.service_dependancy import get_auth_service
from app.service.auth_service import AuthService
from app.schemas.otp_schema import OTPSchema



auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.post("/otp-login")
async def get_otp_login(back_ground_task : BackgroundTasks ,email : str = Form(...) ,auth_service : AuthService  = Depends(get_auth_service)):
    auth = await auth_service.generate_otp_service(email,background_task=back_ground_task)
    if not auth:
        raise
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "OTP sent successfully"
        }
    )
    
@auth_router.post("/otp-verify")
def verify_otp(otp_schema : OTPSchema ,auth_service : AuthService = Depends(get_auth_service)):
    auth_response = auth_service.verify_otp(otp_schema)
    return  JSONResponse(
                                status_code=200,
                                content= jsonable_encoder({
                                                        "success": True,
                                                        "message": "Verified",
                                                        "auth": auth_response
                                                    })

    )

