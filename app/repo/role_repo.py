from typing import Any, List
from uuid import UUID

from alembic.ddl import oracle
from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session, InstrumentedAttribute

from app.models import role, Role, Permission
from app.schemas.role_schema import *
from app.models.role import Role
from app.models.rolePermision import RolePermission
from app.models.permission_model import Permission

from app.core.logging_config import logger


class RolePermissionRepo:
        def __init__(self,db:Session) :
                self.db = db
        def create_role(self,data : CreateRole , organisation_id : uuid.UUID ) -> Role | None:
            role = Role(    organization_id = organisation_id,
                            name = data.name,
                            description = data.description
                            )
            logger.info("user create role for organisation %s and role details %s", organisation_id,role)
            try :
                    self.db.add(role)
                    self.db.commit()
                    self.db.refresh(role)
            except Exception as e :
                       self.db.rollback()
                       logger.exception("role creation rollback due to %s",e)
                       raise e
            return role
        
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

        def create_role_permission(self,role_id: int  ,permission_id : int ):#ORG_Admin can create role permission
               
              permission = (
                        self.db.query(RolePermission).filter(
                        RolePermission.role_id == role_id,
                        RolePermission.permission_id == permission_id,
                        ).first())

              if permission :
                     raise ValueError("role permission already exist ")
              permission = RolePermission(role_id = role_id,
                                          permission_id = permission_id)
              
              logger.info("user create role_permission %s", permission,)

              self.db.add(permission)
              self.db.commit()
              self.db.refresh(permission)
              return permission

        def get_role_permission(self, role_id: uuid.UUID) -> List[RolePermission] :
            role_permissions = (
                self.db.query(RolePermission)
                .filter(RolePermission.role_id == role_id)
                .all()
            )
            permission_names = [
                rp.permission.permission_name
                for rp in role_permissions
            ]

            return permission_names


        def get_role(self,role_name : str , organisation_id : uuid.UUID ) -> InstrumentedAttribute[UUID] | None:

            return   self.db.query(Role.id).filter(Role.name == role_name,
                                                    Role.organization_id == organisation_id).first()
        def get_role_details(self,role_name : str , organisation_id : uuid.UUID ) -> InstrumentedAttribute[UUID] | None:

            return   self.db.query(Role).filter(Role.name == role_name,
                                                    Role.organization_id == organisation_id).first()

        def get_all_role(self,organisation_id : uuid.UUID ) -> list[Any] | list[type[Role]]:
            role = self.db.query(Role).filter(Role.organization_id == organisation_id).all()
            if not role :
               return []
            return role


        def get_permission(self,permission_name: str ) -> type[Permission] | None:
            permission = (
                self.db.query(Permission)
                .filter(Permission.name == permission_name)
                .first()
            )
            return permission
        def get_all_permission(self) -> list[Any] | list[type[Permission]]:
            return self.db.query(Permission).filter(Permission.assignable == True,
                                                    Permission.scope ==PermissionScopEnumUpdate.ORGANIZATION ).all()

        def get_all_system_permission(self) -> list[Any] | list[type[Permission]]:
            return self.db.query(Permission).filter(Permission.assignable == False,
                                                    Permission.scope ==PermissionScopEnumUpdate.SYSTEM).all()




        # def get_permission_assign_to_role(self,role_id : uuid.UUID ) -> type[Permission] | None:
