from sqlalchemy.orm import Session

from app.models.organisation_role import OrganisationRoles
from app.models.organisation_role_permission import OrganisationLevelRolePermissions
from app.models.permission_model import Permission


class DefaultRolePermissionService:

    DEFAULT_ROLES = [
        {
            "name": "Admin",
            "description": "Full access to the organization",
        },
        {
            "name": "HR",
            "description": "Manage employees and leave",
        },
        {
            "name": "Manager",
            "description": "Manage team attendance and leave",
        },
        {
            "name": "Employee",
            "description": "Basic employee access",
        },
    ]

    DEFAULT_ROLE_PERMISSIONS = {
        "Admin": [
            "*",
        ],

        "HR": [
            "employee:create",
            "employee:view",
            "employee:update",

            "department:create",
            "department:view",
            "department:update",

            "leave:view",
            "leave:approve",
            "leave:reject",

            "shift:view",
            "attendance:view",
        ],

        "Manager": [
            "employee:view",

            "leave:view",
            "leave:approve",

            "attendance:view",

            "shift:view",
        ],

        "Employee": [
            "attendance:checkin",
            "attendance:checkout",

            "leave:apply",
            "leave:view",

            "employee:view",
        ],
    }

    def __init__(self, db: Session):
        self.db = db

    def create_default_roles(self, organisation_id):
        """
        Creates default organisation roles and assigns permissions.
        """

        created_roles = []

        try:

            # -------------------------
            # Create Roles
            # -------------------------
            for role_data in self.DEFAULT_ROLES:

                role = OrganisationRoles(
                    role_name=role_data["name"],
                    description=role_data["description"],
                    organisation_id=organisation_id,
                )

                self.db.add(role)
                created_roles.append(role)

            # Generate IDs without commit
            self.db.flush()

            # -------------------------
            # Assign Permissions
            # -------------------------

            mappings = []

            for role in created_roles:

                permission_names = self.DEFAULT_ROLE_PERMISSIONS.get(
                    role.role_name,
                    [],
                )

                # Admin -> every permission
                if "*" in permission_names:

                    permissions = self.db.query(Permission).all()

                else:

                    permissions = (
                        self.db.query(Permission)
                        .filter(
                            Permission.name.in_(permission_names)
                        )
                        .all()
                    )

                for permission in permissions:

                    mappings.append(

                        OrganisationLevelRolePermissions(
                            organisation_role_id=role.id,
                            permission_id=permission.id,
                        )

                    )

            self.db.add_all(mappings)

            self.db.commit()

            for role in created_roles:
                self.db.refresh(role)

            return created_roles

        except Exception:

            self.db.rollback()
            raise