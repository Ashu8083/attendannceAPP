from typing import List

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

role_management_router = APIRouter(
    prefix="/organisation-role-management",
    tags=["Organisation Role Management"],
)


# --------------------------------------------------
# Role APIs
# --------------------------------------------------

@role_management_router.post(
    "/roles",
    dependencies=[Depends(PermissionChecker("role.manager"))],
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
    "/roles",
    response_model=List[OrganisationRoles],
    dependencies=[Depends(PermissionChecker("role.view"))],
)
def get_all_roles(
    request: Request,
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    return service.get_all_roles(
        organisation_id=request.state.auth.organisation_id,
    )


@role_management_router.get(
    "/roles/{role_name}",
    response_model=OrganisationRoles,
    dependencies=[Depends(PermissionChecker("role.view"))],
)
def get_role(
    role_name: str,
    request: Request,
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    return service.get_role(
        organisation_id=request.state.auth.organisation_id,
        role_name=role_name,
    )


# --------------------------------------------------
# Role Permission APIs
# --------------------------------------------------

@role_management_router.post(
    "/roles/{role_name}/permissions",
    dependencies=[Depends(PermissionChecker("role.manager"))],
)
def assign_permissions(
    role_name: str,
    permissions: ListOFPermissions,
    request: Request,
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    return service.assign_permissions(
        organisation_id=request.state.auth.organisation_id,
        role_name=role_name,
        permissions=permissions,
    )


@role_management_router.get(
    "/roles/{role_name}/permissions",
    response_model=List[str],
    dependencies=[Depends(PermissionChecker("role.view"))],
)
def get_role_permissions(
    role_name: str,
    request: Request,
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    return service.get_all_permission_for_role(
        organisation_id=request.state.auth.organisation_id,
        role_name=role_name,
    )


# --------------------------------------------------
# Permission APIs
# --------------------------------------------------

@role_management_router.get(
    "/permissions",
    response_model=List[PermissionResponse],
    dependencies=[Depends(PermissionChecker("role.view"))],
)
def get_organisation_permissions(
    service: OrganisationRolePermissionService = Depends(
        get_organisation_role_service
    ),
):
    return service.get_all_permission_organisation()