from typing import List

from fastapi import status
from fastapi import APIRouter, Depends, Request

from app.auth.permission_check import PermissionChecker
from app.dependancy.service_dependancy import (
    get_organisation_role_service,
)
from app.schemas.role_schema import OrganisationRoleResponse as OrganisationRoles
from app.schemas.role_schema import PermissionResponse
from app.schemas.role_schema import (
    CreateRoleSchema,
    ListOFPermissions,
)
from app.service.role_services.organisation_role_permission_service import (
    OrganisationRolePermissionService,
)
from app.core.response_helper import CommonJSONResponse

role_management_router = APIRouter(
    prefix="/organisation-role-management",
    tags=["Organisation Role Management"],
)


# --------------------------------------------------
# Role APIs
# --------------------------------------------------

@role_management_router.post(
    "/create-role",
    dependencies=[Depends(PermissionChecker("role.manager","ORGANISATION"))],
)
def create_role(
    role_schema: CreateRoleSchema,
    request: Request,
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    return service.create_role(
        organisation_id=request.state.auth.organisation_id,
        role_schema=role_schema,
    )


@role_management_router.get(
    "/get-all-role",
    response_model=List[OrganisationRoles],
    dependencies=[Depends(PermissionChecker("role.view","ORGANISATION"))],
)
def get_all_roles(
    request: Request,
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    roles = service.get_all_roles(organisation_id=request.state.auth.organisation_id)
    return CommonJSONResponse(
        status_code=status.HTTP_200_OK,
        content=roles,
        message="roles fetched successfully",
    )

@role_management_router.get(
    "/get-role-by-name/{role_name}",
    response_model=OrganisationRoles,
    dependencies=[Depends(PermissionChecker("role.view","ORGANISATION"))],
)
def get_role(
    role_name: str,
    request: Request,
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    role = service.get_role(
        organisation_id=request.state.auth.organisation_id,
        role_name=role_name,
    )
    return CommonJSONResponse(
        content=role,
        message="role fetched successfully",
        status_code=status.HTTP_200_OK,

    )
# --------------------------------------------------
# Role Permission APIs
# --------------------------------------------------
@role_management_router.post(
    "/assign-permission-role/{role_name}/permissions",
    response_model=OrganisationRoles,
    dependencies=[Depends(PermissionChecker("role.manager","ORGANISATION"))],
)
def assign_permissions(
    role_name: str,
    permissions: ListOFPermissions,
    request: Request,
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    permissions  = service.assign_permissions(
        organisation_id=request.state.auth.organisation_id,
        role_name=role_name,
        permissions=permissions,
    )
    return CommonJSONResponse(
        status_code=status.HTTP_200_OK,
        content=permissions,
        message="permissions fetched successfully",
    )
@role_management_router.get(
    "/roles/{role_name}/permissions",
    response_model=List[str],
    dependencies=[Depends(PermissionChecker("role.view","ORGANISATION"))],
)
def get_role_permissions(
    role_name: str,
    request: Request,
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    role_permissions= service.get_all_permission_for_role(
        organisation_id=request.state.auth.organisation_id,
        role_name=role_name,
    )
    return  CommonJSONResponse(
        content=role_permissions,
        message="RolePermission fetched successfully",
        status_code=status.HTTP_200_OK,
    )
# --------------------------------------------------
# Permission APIs
# --------------------------------------------------

@role_management_router.get(
    "/get-all-permissions",
    response_model=List[PermissionResponse],
    dependencies=[Depends(PermissionChecker("role.view","ORGANISATION"))],
)
def get_organisation_permissions(
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    permissions = service.get_all_permission_organisation()
    return CommonJSONResponse(
        content=permissions,
        message="permissions fetched successfully",
        status_code=status.HTTP_200_OK,
    )
