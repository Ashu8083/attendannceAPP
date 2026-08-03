from typing import List, Any

from app.schemas.role_schema import  *

from app.exceptions.custom_exception import(
                                            RoleAlreadyExist,
                                            RoleNotFound,
                                            PermissionAlreadyExist,
                                            PermissionNotFound,
                                            RolePermissionNotFound
)
from app.repo.RolePermissionRepo.role_repo import RolePermissionRepo

from uuid import UUID

from app.models.permission_model import Permission


# For creating Permission  Only

class RoleService:
    def __init__(self,role_repo : RolePermissionRepo) -> None:
        self.role_repo : RolePermissionRepo = role_repo
#
#     def get_role_details(self,organisation_id : UUID,role_name :str):
#         role_details = self.role_repo.get_role_details( role_name = role_name ,organisation_id= organisation_id,)
#         if not role_details :
#             raise RoleNotFound(role_name=role_name)
#         return
#
#     def create_role(self,data : CreateRole,organisation_id : uuid.UUID ) ->  Role|None :
#         role = self.role_repo.get_role_details(organisation_id= organisation_id , role_name=data.name)
#         if role:
#             raise RoleAlreadyExist
#         role = self.role_repo.create_role(data , organisation_id)
#         return role
#
#     def create_role_permission(self,role_creation_schema : CreateRole ,organisation_id : uuid.UUID, permissions : ListOFPermissions ) -> Role:
#
#          role = self.role_repo.get_role(role_creation_schema.name,organisation_id )
#          if not role :
#              role = self.role_repo.create_role(role_creation_schema,organisation_id)
#
#          for permission in permissions.permissions:
#
#              permission_id = self.role_repo.get_permission(permission)
#              if permission_id :
#                  role_permission = self.role_repo.create_role_permission(role.id,permission_id.id)
#                  return  role_permission


    def create_permission (self,create_permission_schema : CreatePermision) :

         permission = self.role_repo.create_permission(create_permission_schema)
         return permission

    def create_list_permission(
            self,
            schema: CreateListOfPermissions
    ):

        names = [p.name for p in schema.permissions]

        existing = self.role_repo.get_permissions_by_names(names)

        existing_names = {p.name for p in existing}

        permission_models = []

        for permission in schema.permissions:

            if permission.name in existing_names:
                continue

            permission_models.append(
                Permission(
                    name=permission.name,
                    description=permission.description,
                    scope=permission.scope,
                    assignable=permission.assignable,
                )
            )

        if permission_models:
            return self.role_repo.create_permissions(permission_models)

        return []
#     def get_all_roles (self,organisation_id : uuid.UUID ) -> list[Role] :
#
#         role = self.role_repo.get_role(organisation_id )
#         if not role :
#             raise RolePermissionNotFound
#
#         return role
#
#     def get_role_permissions(
#             self,
#             role_name: str,
#             organisation_id: uuid.UUID
#     ) -> List[str]:
#         role = self.role_repo.get_role(role_name, organisation_id)
#         if not role:
#             raise RolePermissionNotFound
#         return self.role_repo.get_role_permission(role.id)
#
#     def get_all_permission(self) -> List[Any] | None :
#         all_permission = self.role_repo.get_all_permission()
#         if not all_permission:
#             raise PermissionNotFound
#
#         return  all_permission
#     def get_all_system_permission(self)-> List[Any] |None :
#         all_system_permission = self.role_repo.get_all_system_permission()
#
#         return all_system_permission
#
#
#     # def create_permission(self,data : CreatePermision) -> Permission :
#     #     permission = self.role_repo.get_permission(permission_name= data.name)
#     #     if not permission:
#     #         raise
#     #     return permission
#
#
#
#
#
