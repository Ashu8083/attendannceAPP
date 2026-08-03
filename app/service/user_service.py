import uuid

from fastapi import Depends

from app.enums.user_status_enums import UserStatus
from app.repo.user_repo import UserRepo
from app.repo.organisation_repo import OrganisationRepo
from app.service.organisation_service import OrganisationService



from app.schemas.user import UserCreation,UserStatusUpdate,UserUpdate,UserUpdatePassword
from app.core.logging_config import logger
from app.db.UnitOfWork import UnitOfWork
from sqlalchemy.orm import Session
from app.exceptions.custom_exception import UserNotFound, EmailAlreadyExists
from app.repo.RolePermissionRepo.system_role_permission_repo import SystemRoleRepo
from app.db.database import get_db
from migrations.versions.af6bf093104a_initial_migration import depends_on


class UserService:
    def __init__(self,userrepo: UserRepo ,
                 organisation_repo : OrganisationRepo ,
                 system_role_permission : SystemRoleRepo,
                 db : Session
                 ):
        self.db  = db
        self.userrepo = userrepo
        self.organisation_repo = organisation_repo
        self.system_role_permission_repo :SystemRoleRepo = system_role_permission

    def create_user_service(self,user_data : UserCreation):

        user = self.userrepo.get_user_by_email(user_email= user_data.email)
        organisation_id = self.organisation_repo.get_organisation_id(user_data.organisation_code)
        role_id = self.system_role_permission_repo.get_role(role_name= user_data.role_name)
        print (organisation_id)
        if  user:
               raise EmailAlreadyExists
        with UnitOfWork(self.db):
            user = self.userrepo.create_user(user_data,organisation_id)
            system_role_permission = self.system_role_permission_repo.create_system_role(user.id,system_role_id=role_id)
        print (user,system_role_permission)

        logger.info("< ------- user created  with role ---------  >")

        return user

    def get_user(self,user_email :str ):
        user = self.userrepo.get_user_by_email(user_email)
        if not user:
           logger.info("user not found")
           raise UserNotFound(user_email)
        return user

    def get_user_by_account_scope(self, account_scope: str):
        users = self.userrepo.get_users_by_account_scope(account_scope)
        return users
    def get_user_status(self,user_email:str,data: UserStatusUpdate):

        user = self.userrepo.get_user_by_email(user_email)
        if not user:
            raise ValueError("user not found")
              
            
        user = self.userrepo.updateUser(data)   
        return user
    def update_user(self,user_email : str ,data: UserUpdate):

        user = self.userrepo.get_user_by_email(user_email)
        if not user:
            raise ValueError ("user not found")
                
        return self.userrepo.updateUser(data)

    def get_user_by_id(self,user_id :uuid.UUID):
        return self.userrepo.get_user_by_id(user_id)

    def assign_role_user(self,user_id: uuid.UUID, role_name: str):
        user = self.userrepo.get_user_by_id(user_id)
        if not user:
            raise ValueError("user not found")
        role_id = self.system_role_permission_repo.get_role_id(role_name)
        logger.info(f"assigning role {role_id}")

        role = self.system_role_permission_repo.create_system_role(user_id,system_role_id=role_id)
        self.db.commit()

        return {
            "user" : user.full_name,
            "role" : role
        }




        return

    # def get_user(self,user_id : uuid.UUID):
    #     if not self.userrepo.get_user_by_id(user_id):
    #         raise ValueError("user not found")
    #     user_status = self.userrepo.sta
    #     if user_status != UserStatus.ACTIVE:
    #         raise ValueError("user is Inactive")
    #     return self.userrepo.get_user(user_id)



