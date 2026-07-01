from ast import List

from app.models import RolePermission, role
from app.models.role import Role
from app.schemas.role_schema import  *
from app .repo.role_repo import RoleRepo

class RoleService:
    def __init__(self,role_repo : RoleRepo):
        self.role_repo = role_repo

    def get_role_description(self):
        return

    def create_role_permission(self,role_creation_schema : CreateRole ,organisation_id : uuid.UUID, permissions ) -> Role:

         role = self.role_repo.get_role(organisation_id ,role_creation_schema)
         if not role :
             role = self.role_repo.create_role(role_creation_schema,organisation_id)

         for permission in permissions:

             permission_id = self.role_repo.get_permission(permission)
             if permission_id :
                 role_permission = self.role_repo.create_role_permission(role.id,permission_id)

    def create_permission (self,create_permission_schema : CreatePermision) :
        permission = self.role_repo.get_permission(create_permission_schema.name)
        if permission :
            return None
        permission = self.role_repo.create_permision(create_permission_schema)
        return permission
    def get_all_roles (self,organisation_id : uuid.UUID ) -> List[Role] :

        role = self.role_repo.get_role(organisation_id )
        return role

    def get_role_permissions(
            self,
            role_name: str,
            organisation_id: uuid.UUID
    ) -> List[str]:
        role = self.role_repo.get_role(role_name, organisation_id)
        if not role:
            return []
        return self.role_repo.get_role_permission(role.id)






