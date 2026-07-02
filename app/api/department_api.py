import uuid
from fastapi import APIRouter,Depends

from app.schemas.department_schema import  DepartmentCreate
from app.dependancy.service_dependancy import get_department_service
from app.service import department_service

department_router = APIRouter()

@department_router.get("/get-department/{oranisation_id}/{department_name}")
def get_departments(organisation_id: uuid.UUID, department_name :str,department_service = Depends(get_department_service)):
    departments = department_service.get_department(department_name,organisation_id= organisation_id)
    return departments

@department_router.post("/create-department/{oranisation_id}")
def create_department(department_schema : DepartmentCreate,organisation_id : uuid.UUID,department_service = Depends(get_department_service)):
    return department_service.create_department(department_schema,organisation_id= organisation_id)

@department_router.put("/department/{organisation_id}")
def soft_delete_department(department_name : str , organisation_id : uuid.UUID , department_service = Depends(get_department_service)):
    return department_service.soft_delete_department(department_name,oranisation_id=organisation_id)
@department_router.get("/get-all-department/{organisation_id}")
def get_all_departments(organisation_id : uuid.UUID,department_service = Depends(get_department_service)):
    return department_service.get_all_department(organisation_id=organisation_id)



