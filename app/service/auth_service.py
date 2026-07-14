import logging
from urllib import response

from fastapi import BackgroundTasks
from sqlalchemy import true
from datetime import date, time, timedelta


from app.auth.auth_cntx import AuthContext
from app.enums.employee_status import EmployeeStatus
from app.enums.role_enums import UserRole
from app.models import Employee, Role
from app.repo import user_device_repo, employee_repo, role_repo
from app.repo.AuthRepo import AuthRepo
from app.repo.employee_repo import EmployeeRepo
from app.repo.role_repo import RolePermissionRepo
from app.repo.user_repo import UserRepo
from app.repo.user_device_repo import UserDeviceDetailRepo
from app.schemas.otp_schema import OTPSchema
from app.core.otpgenerate import generate_otp_for_user
from app.core.logging_config import  logger
from app.security import jwt_handler
from app.security.jwt_handler import create_access_token, create_refresh_token
from app.security.jwt_handler import verify_access_token, decode_token
from app.email.service import email_service
from app.exceptions.custom_exception import *



class AuthService:
    def __init__(self,  auth_repo : AuthRepo , user_repo : UserRepo , user_device : UserDeviceDetailRepo , employee_repo : EmployeeRepo ,role_repo :RolePermissionRepo):
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        self.user_device_repo = user_device
        self.employee_repo = employee_repo
        self.role_repo = role_repo



    def verify_otp(self,otp_schema : OTPSchema) : ## letter it will replace by redis

        logger.info(f"verify otp for user {otp_schema.user_email}")

        user = self.user_repo.get_user_by_email(otp_schema.user_email)
        employee_id = None
        if not user:
            raise UserNotFound(f"User with email {otp_schema.user_email} not found")

        otp = self.auth_repo.get_otp(user.id)
        if not otp :
             raise Exception(f"otp not found or invalid")
        if otp.otp != otp_schema.otp :
            raise Exception(f"otp not found or invalid")
        permissions = set()
        if user.role == UserRole.USER:
            employee_id = user.employee.id
            for rp in user.employee.role.role_permissions:
                permissions.add(rp.permission.name)
                print(permissions)
        if user.role in {UserRole.ADMIN or UserRole.SUPER_ADMIN}:
            permissions = ()


        access_token = create_access_token(user.id,user_role= user.role,organisation_id= user.organisation_id, employee_id = employee_id)

        if not access_token :
         raise Exception(f"access_token not generated for user {user.id} : {otp_schema.user_email}")
        refresh_token = create_refresh_token(user.id,user_role= user.role,organisation_id= user.organisation_id ) ## store the refresh token in userdevice
        if not refresh_token :
            raise Exception(f"access_token not generated for user {user.id} : {otp_schema.user_email}")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "permission_list" : permissions,
        }

    async def generate_otp_service(self,user_email,background_task :BackgroundTasks ):
        user_id = self.user_repo.get_id_by_email(user_email)
        if not user_id:
            raise UserNotFound(f"User with email {user_email} not found")
        otp = generate_otp_for_user()
        otp_model = self.auth_repo.create_otp(user_id, otp)
        if not otp_model:
            logger.error(f"otp model for user {user_id} not created")
            raise UserNotFound(f"User with email {user_email} not found")

        # background_task.add_task(
        #     email_service.send_otp,
        #     email=user_email,
        #     otp=otp_model.otp,
        # )
        return otp_model

    def verify_access_token(self,token):

        payload = decode_token(token)
        user = self.user_repo.get_user(payload["user_id"])

        if not user:
            raise UserNotFound(f"User with email {payload['email']} not found")
        if user.role == UserRole.USER:
            employee = user.employee

            if  employee.emplopyee_status != EmployeeStatus.ACTIVE:
                raise EmployeeIsInactive
            if employee.role is None:
                raise Exception("Employee role not assigned")

            permissions = set()
            for rp in employee.role.role_permissions :
                permissions.add(rp.permission.name)

            auth  = AuthContext(
                                user_id=user.id,
                                organisation_id=user.organisation_id,
                                system_role=user.role.value,
                                employee_id=user.employee.id if user.employee else None,
                                permissions=permissions,
                                )
        if user.role in  {UserRole.ADMIN or UserRole.SUPER_ADMIN}:
            auth = AuthContext(
                user_id = user.id,
                organiasation_id = user.organisation_id,
                system_role = user.role.value,
                employee_id =  None,
                permissions = set(),
            )
        logger.info(f"auth model for user {user.id} has permissions of {permissions}")

        return auth













