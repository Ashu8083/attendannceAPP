from typing import Any, List
from uuid import UUID

from alembic.ddl import oracle
from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session, InstrumentedAttribute

from app.models import  Permission
from app.schemas.role_schema import *

from app.models.permission_model import Permission

from app.core.logging_config import logger
#

class RolePermissionRepo:
        def __init__(self,db:Session) :
                self.db = db
        def create_permission(self, data : CreatePermision): #permission can only create by SuperAdmin

                logger.info("user creating permision")
                permission = self.db.query(Permission).filter(Permission.name == data.name).first()
                if  permission:
                       raise ValueError("permission already exist ")
                permission = Permission(name = data.name,
                                        description = data.description,
                                        scope = data.scope,
                                        assignable = data.assignable
                                         )
                logger.info("permission create %s",permission)
                try :
                       self.db.add(permission)
                       self.db.commit()
                       self.db.refresh(permission)
                except Exception as e:
                        self.db.rollback()
                        logger.exception("permission creation rollback due to %s",e)
                        raise e
                return permission

        def create_permissions(self, permissions: list[Permission]):
            self.db.add_all(permissions)
            self.db.commit()

            for permission in permissions:
                self.db.refresh(permission)

            return permissions

#
        def get_permissions_by_names(self, names: list[str]) -> list[Permission]:
            return (
                self.db.query(Permission)
                .filter(Permission.name.in_(names))
                .all()
            )

        def create_default_role(self, role):
            self.db.add_all(role)
            self.db.flush()
            self.db.refresh(role)

            return role

        def get_all_permissions(self) -> list[Permission]:
            permissions = []
            permissions = self.db.query(Permission).all()
            return permissions



