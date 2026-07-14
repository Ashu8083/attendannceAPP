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


class RolePermissionRepo:
        def __init__(self,db:Session) :
                self.db = db
        def create_role(self,data : CreateRole , organisation_id : uuid.UUID ) -> Role | None:
            role = Role(    organization_id = organisation_id,
                            name = data.name,
                            description = data.description
                            )
            try :
                    self.db.add(role)
                    self.db.commit()
                    self.db.refresh(role)
            except Exception as e :
                       self.db.rollback()
                       raise e
            return role
        
        def create_permission(self, data : CreatePermision): #permission can only create by SuperAdmin

                permission = self.db.query(Permission).filter(Permission.name == data.name).first()
                if  permission:
                       raise ValueError("permission already exist ")
                permission = Permission(name = data.name,
                                        description = data.description)
                try : 
                       self.db.add(permission)
                       self.db.commit()
                       self.db.refresh(permission)
                except Exception:
                        self.db.rollback()
                        raise
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
            print(permission_names)
            return permission_names


        def get_role(self,role_name : str , organisation_id : uuid.UUID ) -> InstrumentedAttribute[UUID] | None:

            return   self.db.query(Role.id).filter(Role.name == role_name,
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
            return self.db.query(Permission).filter(Permission.assignable == False,
                                                    Permission.scope ==PermissionScopEnum.ORGANIZATION ).all()


        # def get_permission_assign_to_role(self,role_id : uuid.UUID ) -> type[Permission] | None:
