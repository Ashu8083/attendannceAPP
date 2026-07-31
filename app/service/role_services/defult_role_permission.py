
from app.models.organisation_role import OrganisationRoles

DEFAULT_ROLE_PERMISSIONS = {
    "Admin": [
        "*"
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
        "attendance:view"
    ],

    "Manager": [
        "employee:view",

        "leave:view",
        "leave:approve",

        "attendance:view",

        "shift:view"
    ],

    "Employee": [
        "attendance:checkin",
        "attendance:checkout",

        "leave:apply",
        "leave:view",

        "employee:view"
    ]
}
def create_default_role(organisation_id):
    DEFAULT_ROLES = [
        {
            "name": "Admin",
            "description": "Full access to the organization"
        },
        {
            "name": "HR",
            "description": "Manage employees and leave"
        },
        {
            "name": "Manager",
            "description": "Manage team attendance and leave"
        },
        {
            "name": "Employee",
            "description": "Basic employee access"
        }
    ]
    roles = []
    for role in DEFAULT_ROLES:
        roles.append(
            OrganisationRoles(
                role_name=role["name"],
                description=role["description"],
                organisation_id=organisation_id
        )
    )
    return roles


