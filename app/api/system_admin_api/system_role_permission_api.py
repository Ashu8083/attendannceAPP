from typing import List

from fastapi import APIRouter, Depends

from app.auth.permission_check import PermissionChecker
from app.dependancy.service_dependancy import get_role_system_role_service
from app.schemas.role_schema import SystemRoleResponse  as SystemRoles
from app.schemas.role_schema import PermissionResponse
from app.schemas.role_schema import (
    CreateRoleSchema,
    ListOFPermissions,
)
from app.service.role_services.system_role_permission_service import (
    SystemRoleService,
)

system_role_router = APIRouter(
    prefix="/system-roles",
    tags=["System Roles"],
)


# --------------------------------------------------
# Role APIs
# --------------------------------------------------

@system_role_router.post(
    "",
    response_model=SystemRoles,
    dependencies=[Depends(PermissionChecker("system_role.create","SYSTEM"))],
)
def create_role(data: CreateRoleSchema,service: SystemRoleService = Depends(get_role_system_role_service)):
    return service.create_role(data)

@system_role_router.get(
    "",
    response_model=List[SystemRoles],
    dependencies=[Depends(PermissionChecker("system_role.view","SYSTEM"))],
)
def get_all_roles(
    service: SystemRoleService = Depends(get_role_system_role_service),
):
    return service.get_all_roles()


@system_role_router.get(
    "/{role_name}",
    response_model=SystemRoles,
    dependencies=[Depends(PermissionChecker("system_role.view","SYSTEM"))],
)
def get_role(
    role_name: str,
    service: SystemRoleService = Depends(get_role_system_role_service),
):
    return service.get_role_details(role_name)


@system_role_router.delete(
    "/{role_name}",
    dependencies=[Depends(PermissionChecker("system_role.delete","SYSTEM"))],
)
def delete_role(
    role_name: str,
    service: SystemRoleService = Depends(get_role_system_role_service),
):
    service.delete_role(role_name)

    return {
        "message": "Role deleted successfully"
    }


# --------------------------------------------------
# Role Permission APIs
# --------------------------------------------------

@system_role_router.post(
    "/{role_name}/permissions",
    dependencies=[Depends(PermissionChecker("system_role.permission.assign","SYSTEM"))],
)
def assign_permissions(
    role_name: str,
    permissions: ListOFPermissions,
    service: SystemRoleService = Depends(get_role_system_role_service),
):
    return service.create_role_permissions(
        role_name=role_name,
        permissions=permissions,
    )


@system_role_router.get(
    "/{role_name}/permissions",
    response_model=List[str],
    dependencies=[Depends(PermissionChecker("system_role.permission.view","SYSTEM"))],
)
def get_role_permissions(
    role_name: str,
    service: SystemRoleService = Depends(get_role_system_role_service),
):
    return service.get_role_permissions(role_name)


# --------------------------------------------------
# Permission APIs
# --------------------------------------------------

@system_role_router.get(
    "/permissions/all",
    response_model=List[PermissionResponse],
    dependencies=[Depends(PermissionChecker("permission.view","SYSTEM"))],
)
def get_all_system_permissions(
    service: SystemRoleService = Depends(get_role_system_role_service),
):
    return service.get_all_system_permissions()