from typing import Any, List

from alembic.ddl import oracle
from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session

from app.schemas.role_schema import *
from app.models.role import Role
from app.models.rolePermision import RolePermission
from app.models.permission_model import Permission


class RoleRepo():
        def __init__(self,db:Session) :
                self.db = db
        def create_role(self,data : CreateRole , organisation_id : uuid.UUID ) -> None :
                

            role = Role(    name = data.name,
                            description = data.description,
                            organisation_id = organisation_id
                            )
                
            try :
                    self.db.add(role)
                    self.db.commit()
            except Exception : 
                       self.db.rollback()
                       raise
        
        def create_permision(self,data : CreatePermision): #permision can only create by SuperAdmin

                permission = self.db.query(Permission).filter(Permission.name == data.name).first()
                if not permission:
                       raise
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
        def create_role_permission(self,role_id: int  ,permission : int ):#ORG_Admin can create role permision
               
              rolepermission = (

                        self.db.query(RolePermission).filter(
                        RolePermission.role_id == role_id,
                        RolePermission.permission_id == permission_id,
                        ).first())

              if rolepermission :
                     raise ValueError("role permision already exist ")
              rolepermission = RolePermission(role_id = data.role_id,
                                              permission_id = data.permission_id)

        def get_role_permission(self, role_id: int):
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



        def get_role(self,role_name : str , organisation_id : uuid.UUID ) -> Role:
            role = self.db.query(Role.id).filter(Role.name == role_name,
                                              Role.organization_id == organisation_id).first()

            return  role

        def get_all_role(self,organisation_id : uuid.UUID ) -> List[Role] :
            role = self.db.query(Role).filtter(Role.organization_id == organisation_id).all()
            return role


        def get_permission(self,permission_name: str ) -> ColumnElement[Any]:
            permission = self.db.query(Permission.id).filter(Permission.name == permission_name).first()
            return permission[0]

