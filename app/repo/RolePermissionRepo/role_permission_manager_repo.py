from sqlalchemy.orm import Session
import uuid
from models import Employee, EmployeeRoles, OrganisationRoles, OrganisationLevelRolePermissions

class RolePermissionManagerRepo:

    def __init__(self,db : Session):
        self.db = db

    def assign_role_to_employee(self, role_id, employee_id):
        employee_role = EmployeeRoles(
            employee_id = employee_id,
            organisation_roles_id = role_id
        )
        self.db.add(employee_role)
        self.db.commit()
        self.db.refresh(employee_role)

        return employee_role

    def employee_roles(self,
                           employee_id):
        employee_roles = (self.db.query(EmployeeRoles)
        .join(
            OrganisationRoles,
            EmployeeRoles.organisation_id == Employee.employee_code
        ).filter(
            EmployeeRoles.employee_id == employee_id
        )).all()
        return employee_roles

    def all_permission_base_on_role(self, employee_id):
        permissions = (
            self.db.query(OrganisationLevelRolePermissions)
            .join(
                OrganisationRoles,
                OrganisationLevelRolePermissions.organisation_role_id
                == OrganisationRoles.id
            )
            .join(
                EmployeeRoles,
                EmployeeRoles.organisation_roles_id
                == OrganisationRoles.id
            )
            .filter(
                EmployeeRoles.employee_id == employee_id
            )
            .all()
        )
        return permissions

    def unassign_role_employee(self, employee_id, role_id):
        self.db.query(EmployeeRoles).filter(EmployeeRoles.employee_id == employee_id,
                                            EmployeeRoles.organisation_roles_id == role_id).delete()
        self.db.commit()
        return

    def create_role_permission(self,organisation_role_id,permission_id,organisation_id):

        organisation_role = OrganisationLevelRolePermissions(
                                            organisation_role_id = organisation_role_id,
                                            permission_id = permission_id,
                                                             )
        self.db.add(organisation_role)
        self.db.refresh(organisation_role)

        return organisation_role

    def create_role_name(self,role_name : str , description :str
                         ,organisation_id :uuid.UUID,branch_id : uuid.UUID):
        organisation = OrganisationRoles(
            role_name = role_name ,
            description = description,
            organisation_id = organisation_id,
            branch_id = branch_id
        )
        self.db.add(organisation)
        self.db.flush()
        self.db.refresh(organisation)

        return organisation

    def update_role_permissions(
            self,
            organisation_role_id,
            permission_ids,
    ):
        # Remove existing permissions
        self.db.query(OrganisationLevelRolePermissions).filter(
            OrganisationLevelRolePermissions.organisation_role_id
            == organisation_role_id
        ).delete(synchronize_session=False)
        # Create new permission mappings
        permissions = [
            OrganisationLevelRolePermissions(
                organisation_role_id=organisation_role_id,
                permission_id=permission_id,
            )
            for permission_id in permission_ids
        ]
        self.db.bulk_save_objects(permissions)
        self.db.commit()
        return permissions
