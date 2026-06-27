from sqlalchemy.orm import Session

from app.schemas.role_schema import *
from app.models.role import Role
from app.models.rolePermision import RolePermission
from app.models.permission_model import Permission


class RoleRepo():
        def __init__(self,db:Session) :
                self.db = db
        def create_role(self,data : CreateRole):
                
            existing_role = (
                            self.db.query(Role)
                            .filter(
                            Role.organisation_id == data.organisation_id,
                             Role.name == data.name,
                            ).first()
                )

            if existing_role:
                raise ValueError("Role already exists")
            role = Role(name = data.name,
                            description = data.description,
                            organisation_id = data.organisation_id)
                
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
        def role_permission(self,data : RolePermission):#ORG_Admin can create role permision
               
              rolepermission = (

                        self.db.query(RolePermission).filter(
                        RolePermission.role_id == data.role_id,
                        RolePermission.permission_id == data.permission_id,
                        ).first())

              if rolepermission :
                     raise ValueError("role permision already exist ")
              rolepermission = RolePermission(role_id = data.role_id,
                                              permission_id = data.permission_id)

