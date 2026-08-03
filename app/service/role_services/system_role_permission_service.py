from typing import List, Any
from uuid import UUID

from app.exceptions.custom_exception import (
    RoleAlreadyExist,
    RoleNotFound,
    PermissionNotFound, UserNotFound,
)
from app.models.system_roles import SystemRoles
from app.models.system_role_permission import SystemRolePermissions
from app.repo.RolePermissionRepo.system_role_permission_repo import SystemRoleRepo
from app.schemas.role_schema import (
    CreateRoleSchema,
    ListOFPermissions,
)
from app.repo.user_repo import UserRepo
from app.enums.scops import AccountType



class SystemRoleService:
    def __init__(self, repo: SystemRoleRepo,user_repo: UserRepo):
        self.repo = repo
        self.user_repo = user_repo

    # -------------------------
    # Role
    # -------------------------

    def create_role(self, data: CreateRoleSchema) -> SystemRoles:
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

        role_permissions = []

        for permission_data in permissions.permissions:

            permission = self.repo.get_permission(permission_data.name)

            if not permission:
                raise PermissionNotFound(permission_data.name)

            role_permissions.append(
                SystemRolePermissions(
                    system_roles_id=role.id,
                    permission_id=permission.id,
                )
            )

        self.repo.create_role_permissions_system(role_permissions)

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

    def assign_sytem_role_permission (self,user_email, user_role,permission_list):

        role = self.repo.get_role(user_role)
        if not role:
            raise RoleNotFound(role_name=user_role)
        user = self.user_repo.get_user(user_email)
        if not user:
            raise UserNotFound(user_email=user_email)
        if user.account_type == AccountType.ORGANISATION:
            raise ValueError("User have no Access to  System")


