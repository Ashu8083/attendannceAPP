from datetime import datetime
from urllib import request

from cryptography.fernet import InvalidToken
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.repo.user_device_repo import UserDeviceDetailRepo
from app.auth.auth_cntx import AuthContext
from app.enums.employee_status import EmployeeStatus
from app.enums.role_enums import UserRole
from app.repo.AuthRepo import AuthRepo
from app.repo.employee_repo import EmployeeRepo
from app.repo.RolePermissionRepo.organisation_role_permission import OrganisationLevelRolePermissionsRepo
from app.repo.RolePermissionRepo.system_role_permission_repo import SystemRoleRepo
from app.repo.user_repo import UserRepo

from app.schemas.otp_schema import OTPSchema
from app.schemas.auth_schema import AuthResponse
from app.core.otpgenerate import generate_otp_for_user
from app.security.jwt_handler import create_access_token, create_refresh_token
from app.security.jwt_handler import decode_token
from app.email.service import email_service
from app.exceptions.custom_exception import *
from app.enums.scops import AccountType
from app.models import User
from app.schemas.userdevice_schema import UserDeviceCreate
from app.repo.token_repo import TokenRepo
from app.db.UnitOfWork import UnitOfWork
from app.models.token import Token
from app.schemas.user_device_schema import CreateUserDeviceSchema
from app.service.user_device_service import UserDeviceAndTokenService
from app.enums.token_schema import TokenSchema
from app.schemas.auth_schema import RefreshAccessToken


class AuthService:
    def __init__(self,
                 db: Session,
                 auth_repo: AuthRepo,
                 user_repo: UserRepo,
                 system_role_repo: SystemRoleRepo,
                 token_repo :TokenRepo,
                 user_device_repo: UserDeviceDetailRepo,
                 user_device_and_token_service : UserDeviceAndTokenService,
                 org_role_repo: OrganisationLevelRolePermissionsRepo):
        self.db = db
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.org_role_repo = org_role_repo
        self.sys_role_repo = system_role_repo,
        self.user_device_repo = user_device_repo
        self.user_device_and_token_service = user_device_and_token_service

    def verify_otp(self, otp_schema: OTPSchema,user_device : CreateUserDeviceSchema ):  ## letter it will replace by redis_config
        logger.info(f"verify otp for user {otp_schema.user_email}")
        user = self.user_repo.get_user_by_email(otp_schema.user_email)
        if not user:
            raise UserNotFound(f"User with email {otp_schema.user_email} not found")
        otp = self.auth_repo.get_otp(user.id)
        logger.info(f"otp for user id :{otp.user_id}")
        if not otp:
            raise OtpInValid
        if otp.otp != otp_schema.otp:
            raise OtpInValid

        permissions = set()
        employee_id = None
        if user.account_type == AccountType.ORGANISATION:
            employee = user.employee
            if employee:
                for employee_role in employee.employee_roles:
                    role = employee_role.role
                    if not role:
                        continue
                    for role_permission in role.organisation_role_permissions:
                        if role_permission.permission:
                            permissions.add(
                                role_permission.permission.name
                            )

        elif user.account_type == AccountType.SYSTEM:
            if user.user_role and user.user_role.system_roles:
                role = user.user_role.system_roles
                for rp in role.system_role_permissions:
                    permissions.add(rp.permission.name)

        access_token = create_access_token(user.id, user_role=user.account_type, organisation_id=user.organisation_id,
                                           employee_id=employee_id)
        if not access_token:
            raise Exception(f"access_token not generated for user {user.id} : {otp_schema.user_email}")

        refresh_token = create_refresh_token(user.id, user_role=user.account_type,
                                             organisation_id=user.organisation_id)
        user_device_schema = UserDeviceCreate(
            device_type= user_device.device_type,
            device_unique_id= user_device.device_unique_id,
            firebaseFCM_token= user_device.firebaseFCM_token
        )
        token = TokenSchema(
            user_id = user.id,

            device_id=None,
            refresh_token=refresh_token[1],
            expires_at=refresh_token[0]
        )
        with UnitOfWork(self.db):
             otp = otp
             self.user_device_and_token_service.create_user_device_and_token(user.id, user_device_schema, token)
             logger.debug(f"Created new user device for user {user.id}")
             logger.info(f"Created new user device for user {user.id}")
             logger.info(f"Created new user token for user {user.id}")

        ## store the refresh token in user device
        if not refresh_token:
            raise Exception(f"access_token not generated for user {user.id} : {otp_schema.user_email}")

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token[1],
            token_type="Bearer",
            expires_in=3600,
            permission_list=list(permissions)
        )

    def logout(self,user_email, device_unique : str ) -> None:
        user_id = self.user_repo.get_id_by_email(user_email)
        if not user_id:
            raise UserNotFound(f"User with email {user_email} not found")
        refresh_token,user_device = self.user_device_and_token_service.make_logout_and_revoke_refresh_token(user_id,device_unique)
        with UnitOfWork(self.db):
            refresh_token
            user_device
        logger.info("user got logged out from the system user_id :{}".format(user_id) )
        return user_device


    async def generate_otp_service(self, user_email, background_task: BackgroundTasks):
        user_id = self.user_repo.get_id_by_email(user_email)

        if not user_id:
            raise UserNotFound(f"User with email {user_email} not found")

        otp = generate_otp_for_user()
        otp_model = self.auth_repo.create_otp(user_id, otp)

        if not otp_model:
            logger.error(f"otp model for user {user_id} not created")
            raise UserNotFound(f"User with email {user_email} not found")

        background_task.add_task(
            email_service.send_otp,
            email=user_email,
            otp=otp_model.otp,
        )
        logger.info(otp_model)
        return otp_model

    def refresh_access_token(self, authSchema : RefreshAccessToken):
        refresh_token = authSchema.refresh_token
        user_email = authSchema.user_email

        logger.info(f"refresh service start for  {user_email} ")
        user = self.user_repo.get_user_by_email(user_email)

        logger.info(f"email in the user table{user.email} ")
        if not user.id:
            raise UserNotFound(f"User with email {user_email} not found")
        device = self.user_device_repo.get_user_active_device(user.id,authSchema.device_unique_id)
        logger.info(f"device for user {user.id} : {device.id} ,device_unique_id :{device.device_unique_id}")
        db_store_refresh_token = self.token_repo.get_user_active_token(user.id,device_id=device.id)
        if not db_store_refresh_token:
            logger.info(f"refresh token model not found for user {user.id} ")
            raise TokenInValid

        if not db_store_refresh_token.refresh_token == refresh_token :
            logger.info(f"refresh token for user {user.id} not matched ")
            raise TokenInValid
        db_store_refresh_token.is_revoked = True

        permissions = set()
        employee_id = None

        if user.account_type == AccountType.ORGANISATION:
            employee = user.employee
            if employee:
                for employee_role in employee.employee_roles:
                    role = employee_role.role
                    if not role:
                        continue
                    for role_permission in role.organisation_role_permissions:
                        if role_permission.permission:
                            permissions.add(
                                role_permission.permission.name
                            )
        elif user.account_type == AccountType.SYSTEM:
            if user.user_role and user.user_role.system_roles:
                role = user.user_role.system_roles
                for rp in role.system_role_permissions:
                    permissions.add(rp.permission.name)
        access_token = create_access_token(user.id, user_role=user.account_type, organisation_id=user.organisation_id,
                                           employee_id=employee_id)
        if not access_token:
            raise Exception(f"access_token not generated for user {user.id} ")
        refresh_token = create_refresh_token(user.id, user_role=user.account_type,
                                             organisation_id=user.organisation_id)
        logger.info(f"device token  {authSchema.device_unique_id} ")
        token = Token(
            user_id=user.id,
            device_id=device.id,
            refresh_token=refresh_token[1],
            expires_at=refresh_token[0]
        )
        with UnitOfWork(self.db):

            self.token_repo.create(token)
            logger.debug(f"Created new user device for user {user.id}")
            logger.info(f"Created new user device for user {user.id}")
            logger.info(f"Created new user token for user {user.id}")

        ## store the refresh token in user device
        if not refresh_token:
            raise Exception(f"token not generated for user {user.id}")

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token[1],
            token_type="Bearer",
            expires_in=3600,
            permission_list=list(permissions)
        )
    def verify_access_token(self, token) :
        auth = AuthContext
        payload = decode_token(token)
        user = self.user_repo.get_user_by_id(payload["user_id"])

        if not user:
            raise UserNotFound()
        user_role = ""
        permissions = set()
        employee_id = None

        if user.account_type == AccountType.ORGANISATION:
            employee = user.employee
            if employee:
                for employee_role in employee.employee_roles:
                    role = employee_role.role
                    if not role:
                        continue
                    for role_permission in role.organisation_role_permissions:
                        if role_permission.permission:
                            permissions.add(
                                role_permission.permission.name
                            )
        elif user.account_type == AccountType.SYSTEM:
            if user.user_role and user.user_role.system_roles:
                role = user.user_role.system_roles
                for rp in role.system_role_permissions:
                    permissions.add(rp.permission.name)

        auth = AuthContext(
                user_id=user.id,
                organisation_id=user.organisation_id,
                system_role=user.account_type.value,
                employee_id=user.employee.id if user.employee else None,
                permissions=permissions,
                )

        # logger.info(f"auth model for user {user.id} has permissions of {permissions} for user role {user_role}")

        return auth

    def verify_refresh_token(self, token) -> AuthContext:
        token = self.token_repo.get_by_token(token)
        if not token:
            raise
        if token.expires_at < datetime.now():
            raise
        if token.is_revoked is True:
            raise

        payload = decode_token(token)
        user = self.user_repo.get_user(payload["user_id"])
        if not user:
            raise UserNotFound(f"User with email {payload['email']} not found")
        user_role = ""
        permissions = set()

        if user.account_type == AccountType.ORGANISATION:
            role = user.employee.employee_roles.role
            for rp in role.organisation_role_permissions:
                permissions.add(rp.permission.name)
            logger.info(permissions)
            employee_id = user.employee.employee_id

        if user.account_type == AccountType.SYSTEM:
            role = user.user_role.system_roles
            for rp in role.system_role_permissions:
                permissions.add(rp.permission.name)
            employee_id = None
        access_token = create_access_token(user.id, user_role=user.account_type, organisation_id=user.organisation_id,
                                           employee_id=employee_id)

        refresh_token = create_refresh_token(user.id, user_role=user.account_type,
                                             organisation_id=user.organisation_id)
        user_device_schema = UserDeviceCreate(
            device_type="app",  # <---- change it letter
            device_unique_id="letter will add",  # < -----------
            firebaseFCM_token="letter will add",
        )
        with UnitOfWork(self.db):
            user_device = self.user_device_repo.create_user_device(user.id, user_device_schema)
            logger.info(f"user device unique id{user_device.id}")
            logger.info(f"user device unique id{user_device.device_unique_id}")
            if not user_device:
                raise ValueError("device not created")
            token = Token(
                device_id=user_device.id,
                refresh_token=refresh_token[1],
                expires_at=refresh_token[0]
            )
            refresh_token = self.token_repo.create(token)

        ## store the refresh token in user device
       

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token[1],
            token_type="Bearer",
            expires_in=3600,
            permission_list=list(permissions)
        )












