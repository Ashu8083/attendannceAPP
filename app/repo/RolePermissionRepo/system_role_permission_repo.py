from typing import List

import uuid
from sqlalchemy.orm import Session

from app.core.logging_config import logger
from app.models.permission_model import Permission
from app.models.system_roles import SystemRoles
from app.models.system_role_permission import SystemRolePermissions
from app.schemas.role_schema import CreateRole
from app.enums.permission_scop import PermissionScopEnumUpdate


class SystemRoleRepo:
    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # Role
    # -------------------------

    def create_role(self, data: CreateRole) -> SystemRoles:
        role = SystemRoles(
            role_name=data.name,
            description=data.description,
        )

        logger.info("Creating system role: %s", data.name)

        try:
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)
        except Exception:
            self.db.rollback()
            logger.exception("Failed to create system role")
            raise

        return role

    def get_role(self, role_name: str) -> SystemRoles | None:
        return (
            self.db.query(SystemRoles)
            .filter(SystemRoles.role_name == role_name)
            .first()
        )

    def get_role_by_id(self, role_id: uuid.UUID) -> SystemRoles | None:
        return (
            self.db.query(SystemRoles)
            .filter(SystemRoles.id == role_id)
            .first()
        )

    def get_all_roles(self) -> List[SystemRoles]:
        return self.db.query(SystemRoles).all()

    def delete_role(self, role: SystemRoles) -> None:
        self.db.delete(role)
        self.db.commit()

    # -------------------------
    # Permission
    # -------------------------

    def get_permission(self, permission_name: str) -> Permission | None:
        return (
            self.db.query(Permission)
            .filter(Permission.name == permission_name)
            .first()
        )

    def get_all_system_permissions(self) -> List[Permission]:
        return (
            self.db.query(Permission)
            .filter(
                Permission.scope == PermissionScopEnumUpdate.SYSTEM
            )
            .all()
        )

    # -------------------------
    # Role Permission
    # -------------------------

    def create_role_permission(
        self,
        role_id: uuid.UUID,
        permission_id: uuid.UUID,
    ) -> SystemRolePermissions:

        role_permission = (
            self.db.query(SystemRolePermissions)
            .filter(
                SystemRolePermissions.system_role_id == role_id,
                SystemRolePermissions.permission_id == permission_id,
            )
            .first()
        )

        if role_permission:
            return role_permission

        role_permission = SystemRolePermissions(
            system_role_id=role_id,
            permission_id=permission_id,
        )

        self.db.add(role_permission)
        self.db.commit()
        self.db.refresh(role_permission)

        return role_permission

    def get_role_permissions(
        self,
        role_id: uuid.UUID,
    ) -> List[str]:

        role_permissions = (
            self.db.query(SystemRolePermissions)
            .filter(
                SystemRolePermissions.system_role_id == role_id
            )
            .all()
        )

        return [
            rp.permission.name
            for rp in role_permissions
        ]