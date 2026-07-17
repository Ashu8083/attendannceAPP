from typing import Any, List
from uuid import UUID

from alembic.ddl import oracle
from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session, InstrumentedAttribute

from app.models import role, OrganisationRoles, Permission
from app.schemas.role_schema import *
from app.models.organisation_role import OrganisationRoles
from app.models.organisation_role_permission import OrganisationLevelRolePermissions
from app.models.permission_model import Permission

from app.core.logging_config import logger
from models import OrganisationRoles



class PermissionRepo:
    def __init__(self, db):
        self.db = db
    def create_permission(self, data: CreatePermision):  # permission can only create by SuperAdmin

        logger.info("user creating permision")
        permission = self.db.query(Permission).filter(Permission.name == data.name).first()
        if permission:
            raise ValueError("permission already exist ")
        permission = Permission(name=data.name,
                                description=data.description,
                                scope=data.scope,
                                assignable=data.assignable
                                )
        logger.info("permission create %s", permission)
        try:
            self.db.add(permission)
            self.db.commit()
            self.db.refresh(permission)
        except Exception as e:
            self.db.rollback()
            logger.exception("permission creation rollback due to %s", e)
            raise e
        return permission