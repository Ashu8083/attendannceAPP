from typing import List

from fastapi import HTTPException, status

from uuid import UUID


from app.repo.RolePermissionRepo.organisation_role_permission import OrganisationLevelRolePermissionsRepo
from app.models.organisation_role import OrganisationRoles
from app.schemas.role_schema import CreateRoleSchema
from app.models.permission_model import Permission


class OrganisationRolePermissionService:
    def __init__(self, org_role_permission_repo : OrganisationLevelRolePermissionsRepo):
        self.repo : OrganisationLevelRolePermissionsRepo = org_role_permission_repo

    def create_role(self,organisation_id :UUID, role_schema : CreateRoleSchema):
        role = self.repo.get_role(role_name=role_schema.name, organisation_id=organisation_id)
        if role:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        role = self.repo.create_role(role_schema, organisation_id=organisation_id)

        return role
    def get_role(self,organisation_id :UUID, role_name) -> OrganisationRoles | None:
        role = self.repo.get_role_details(role_name=role_name, organisation_id=organisation_id)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return role
    def get_all_roles(self,organisation_id :UUID) -> List[type[OrganisationRoles]] | None:
        all_role = self.repo.get_all_role(organisation_id=organisation_id)
        if not all_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No roles found please create one first")
        return all_role

    def get_all_permission_for_role(self,organisation_id : UUID,role_name: str):
        role_id  = self.repo.get_role(role_name=role_name, organisation_id=organisation_id)
        if not role_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No roles found please create one first")
        permissions = self.repo.get_role_permission(role_id)
        return permissions

    def get_all_permission_organisation(self)->List[type[Permission]] | None:
        permissions = self.repo.get_all_permission_organisation()
        if not permissions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
        return permissions

    def create_role_permision(self,organisation_role_id :UUID,permission_id : int ):

        role_permission = self.repo.create_role_permission(organisation_role_id=organisation_role_id, permission_id=permission_id)
        return role_permission

    def default_role_permission(self,organisation_id :UUID):
        admin_permission = self.repo.get_all_role(organisation_id=organisation_id)
        if not admin_permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
