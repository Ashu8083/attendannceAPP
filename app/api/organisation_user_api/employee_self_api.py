import cv2
import numpy as np
from fastapi import APIRouter, Depends, Request, File, UploadFile, Security,status
from fastapi.security import HTTPBearer
from starlette.responses import JSONResponse

from app.schemas.employee_schema import Employee, EmployeeResponse
from app.auth.permission_check import PermissionChecker
from app.service.employee_services import EmployeeService
from app.service.employee_face_service import EmployeeFaceService
from app.dependancy.service_dependancy import get_employee_face_service,get_employee_service



employee_self_router = APIRouter(
    prefix="/organisation-user",
    tags=["organisation-user/"]
)
bearer_scheme = HTTPBearer()
@employee_self_router.get("/employee",response_model= EmployeeResponse)
def get_self_by_employee_api(request : Request ,employee_service: EmployeeService = Depends(get_employee_service)):
    return (employee_service.
            get_employee_by_empID_service(organisation_id=request.state.auth.organisation_id,
                                          employee_id=request.state.auth.employee_id))



@employee_self_router.get("/employee-profile-image")
def get_employee_face_url(request : Request,employee_service: EmployeeService = Depends(get_employee_service)):
    return (employee_service.
            get_employee_profile_picture(employee_id=request.state.auth.employee_id))


@employee_self_router.post("/employee-face-register")
async def register_employee_face(request : Request,credentials=Security(bearer_scheme), image_file : UploadFile = File(...), employee_face_service: EmployeeFaceService = Depends(get_employee_face_service)):

    image_bytes = await image_file.read()
    # Store embedding in PostgreSQL
    await employee_face_service.register_employee_face(
        image_bytes,request
    )
    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "message": "Face successfully registered",
        }
    )

@employee_self_router.post("/employee-face-verify")
async def verify_employee_face(request : Request, image_file : UploadFile = File(...), employee_face_service: EmployeeFaceService = Depends(get_employee_face_service)):

    image_bytes = await image_file.read()
    data = await employee_face_service.verify_employee_face(
    request,image_bytes
    )
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": data,
        }
    )

