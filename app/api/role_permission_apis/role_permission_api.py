import uuid

from fastapi import APIRouter ,Depends
from typing import List
from fastapi import  Request
from app.auth.permission_check import PermissionChecker
from app.dependancy.service_dependancy import get_role_service
from app.schemas.role_schema import CreateRole, CreatePermision, PermissionResponse, ListOFPermissions
from app.service.role_services.role_creation_service import RoleService
from app.core.logging_config import logger

permission_router: APIRouter = APIRouter(prefix="/role",tags=["role"])


# @permission_router.get("/get-all-permission/{role_name}/{organisation_id}")
# def get_all_permission(role_name : str, organisation_id : uuid.UUID,
#                        role_service = Depends(get_role_service) )  :

#     return role_service.get_all_permission(role_name,organisation_id)

@permission_router.post("/create-role-organisation/{organisation_id}")
def create_role(data : CreateRole,organisation_id :uuid.UUID, role_service = Depends(get_role_service)) :
    return role_service.create_role(data ,organisation_id)

@permission_router.post("/create-role")
def create_role(data : CreateRole,request : Request, role_service = Depends(get_role_service)) :
    return role_service.create_role(data ,organisation_id = request.state.auth.organisation_id)

# @permission_router.post("/create-system-role")
# def create_system_role(date: CreateRole,requet: Request):
#     logger.info("new role crate ")


# @permission_router.delete("/remove-permission")
# def remove_permission(self,data):
#     return

# @permission_router.put("/update-permission")
# def update_permission(self,data):
#     return

@permission_router.get("/get-all-permission",response_model= List[PermissionResponse])
def  get_all_permission( role_service = Depends(get_role_service)) :

     return role_service.get_all_permission()
@permission_router.get("/get-all-system-permission",response_model= List[PermissionResponse])
def get_all_system_permission(role_service : RoleService = Depends(get_role_service)):
    return role_service.get_all_system_permission()

@permission_router.post("/create-permission")
def create_permission(data : CreatePermision ,role_service : RoleService = Depends(get_role_service)) :
    return role_service.create_permission(data)

@permission_router.post("/create-role-permission",dependencies = [Depends(PermissionChecker("role"))])
def creat_role_permission(data : CreateRole,request : Request ,permissions : ListOFPermissions,permission_service = Depends(get_role_service)) :
    return permission_service.create_role_permission(role_creation_schema= data,organisation_id = request.state.auth.organisation_id ,permissions = permissions)

@permission_router.post("/assign-role",dependencies = [Depends(PermissionChecker("role"))])
def assign_role_employee():
    return