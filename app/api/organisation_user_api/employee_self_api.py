import cv2
import numpy as np
from fastapi import APIRouter, Depends, Request, File, UploadFile, Security
from fastapi.security import HTTPBearer

from app.schemas.employee_schema import Employee, EmployeeResponse
from app.api.organisation_admin_api.employee_api import get_employee_service
from app.auth.permission_check import PermissionChecker
from app.service.employee_services import EmployeeService
from app.service.employee_face_service import EmployeeFaceService
from app.dependancy.service_dependancy import get_employee_face_service



employee_self_router = APIRouter(
    prefix="/organisation-user/employee",
    tags=["organisation-user/employee"]
)
bearer_scheme = HTTPBearer()
@employee_self_router.get("/employee",response_model= EmployeeResponse)
def get_employee_api(request : Request ,employee_service: EmployeeService = Depends(get_employee_service)):
    return employee_service.get_employee_by_empID_service(organisation_id=request.state.auth.organisation_id,employee_id=request.state.auth.employee_id)


@employee_self_router.post("/employee-face-register")
async def register_employee_face(request : Request,credentials=Security(bearer_scheme), image_file : UploadFile = File(...), employee_face_service: EmployeeFaceService = Depends(get_employee_face_service)):


    image_bytes = await image_file.read()
    # Store embedding in PostgreSQL

    await employee_face_service.register_employee_face(
        image_bytes,request
    )

    return {"messsage" : "Employee registered successfully"}

@employee_self_router.post("/employee-face-verify")
async def verify_employee_face(request : Request,credentials=Security(bearer_scheme), image_file : UploadFile = File(...), employee_face_service: EmployeeFaceService = Depends(get_employee_face_service)):

    image_bytes = await image_file.read()
    data = await employee_face_service.verify_employee_face(
    request,image_bytes
    )
    return {"messsage" : "Employee verified successfully",
            "content": data }


