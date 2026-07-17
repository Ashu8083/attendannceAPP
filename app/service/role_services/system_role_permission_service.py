from typing import List, Any
from uuid import UUID

from app.exceptions.custom_exception import (
    RoleAlreadyExist,
    RoleNotFound,
    PermissionNotFound,
)
from app.models.system_roles import SystemRoles
from app.repo.RolePermissionRepo.system_role_permission_repo import SystemRoleRepo
from app.schemas.role_schema import (
    CreateRole,
    ListOFPermissions,
)


class SystemRoleService:
    def __init__(self, repo: SystemRoleRepo):
        self.repo = repo

    # -------------------------
    # Role
    # -------------------------

    def create_role(self, data: CreateRole) -> SystemRoles:
        role = self.repo.get_role(data.name)

        if role:
            raise RoleAlreadyExist(role_name=data.name)

        return self.repo.create_role(data)

    def get_role_details(self, role_name: str) -> SystemRoles:
        role = self.repo.get_role(role_name)

        if not role:
            raise RoleNotFound(role_name=role_name)

        return role

    def get_all_roles(self) -> List[SystemRoles]:
        return self.repo.get_all_roles()

    def delete_role(self, role_name: str) -> bool:
        role = self.repo.get_role(role_name)

        if not role:
            raise RoleNotFound(role_name=role_name)

        self.repo.delete_role(role)

        return True

    # -------------------------
    # Role Permission
    # -------------------------

    def create_role_permissions(
        self,
        role_name: str,
        permissions: ListOFPermissions,
    ) -> SystemRoles:

        role = self.repo.get_role(role_name)

        if not role:
            raise RoleNotFound(role_name=role_name)

        for permission_name in permissions.permissions:

            permission = self.repo.get_permission(permission_name)

            if not permission:
                raise PermissionNotFound(permission_name)

            self.repo.create_role_permission(
                role.id,
                permission.id,
            )

        return role

    def get_role_permissions(
        self,
        role_name: str,
    ) -> List[str]:

        role = self.repo.get_role(role_name)

        if not role:
            raise RoleNotFound(role_name=role_name)

        return self.repo.get_role_permissions(role.id)

    # -------------------------
    # Permission
    # -------------------------

    def get_all_system_permissions(self) -> List[Any]:
        return self.repo.get_all_system_permissions()