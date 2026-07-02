import uuid

from fastapi import APIRouter ,Depends
from typing import List
from app.dependancy.service_dependancy import get_role_service
from app.schemas.role_schema import CreateRole, CreatePermision, PermissionResponse, ListOFPermissions
from app.service.role_services.role_creation_service import RoleService

permission_router: APIRouter = APIRouter()


@permission_router.get("/get-all-permission/{role_name}/{organisation_id}")
def get_all_permission(role_name : str, organisation_id : uuid.UUID,
                       role_service = Depends(get_role_service) )  :

    return role_service.get_all_permission(role_name,organisation_id)

@permission_router.post("/create-role/{organisation_id}")
def create_role(data : CreateRole,organisation_id :uuid.UUID, role_service = Depends(get_role_service)) :
    return role_service.create_role(data ,organisation_id)



@permission_router.delete("/remove-permission")
def remove_permission(self,data):
    return

@permission_router.put("/update-permission")
def update_permission(self,data):
    return

@permission_router.get("/get-all-permission",response_model= List[PermissionResponse])
def get_all_permission( role_service = Depends(get_role_service)) :

     return role_service.get_all_permission()

# @permission_router.post("/create-permission")
# def create_permission(data : CreatePermision ,role_service : RoleService = Depends(get_role_service)) :
#     return role_service.create_permission(data)

@permission_router.post("/create-role-permission/{organisation_id}")
def creat_role_permission(data : CreateRole,permissions : ListOFPermissions,organisation_id : uuid.UUID,permission_service = Depends(get_role_service)) :
    return permission_service.create_role_permission(role_creation_schema= data,organisation_id = organisation_id ,permissions = permissions)