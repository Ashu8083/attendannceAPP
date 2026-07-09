import uuid
from fastapi import APIRouter,Depends,Request

from app.auth.permission_check import PermissionChecker
from app.schemas.department_schema import  DepartmentCreate
from app.dependancy.service_dependancy import get_department_service
from app.service import department_service

department_router = APIRouter(prefix="/department",tags=["department"])

@department_router.get("/get-department/{department_name}")
def get_departments( request : Request ,department_name :str,department_service = Depends(get_department_service)):
    departments = department_service.get_department(department_name,organisation_id= request.state.auth.organisation_id)
    return departments

@department_router.post("/create-department}",dependencies=[Depends(PermissionChecker("department"))])
def create_department(request, Request ,department_schema : DepartmentCreate,department_service = Depends(get_department_service)):
    return department_service.create_department(department_schema,organisation_id= request.state.auth.organisation_id)

@department_router.put("/department",dependencies=[Depends(PermissionChecker("department"))])
def soft_delete_department(request, Requet ,department_name : str  , department_service = Depends(get_department_service)):
    return department_service.soft_delete_department(department_name,oranisation_id=request.state.auth.oranisation_id)
@department_router.get("/get-all-department",dependencies=[Depends(PermissionChecker("department"))])
def get_all_departments(request : Request,department_service = Depends(get_department_service)):
    return department_service.get_all_department(organisation_id= request.state.auth.organisation_id)





