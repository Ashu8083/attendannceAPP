from fastapi import BackgroundTasks

from app.auth.auth_cntx import AuthContext
from app.enums.employee_status import EmployeeStatus
from app.enums.role_enums import UserRole
from app.repo.AuthRepo import AuthRepo
from app.repo.employee_repo import EmployeeRepo
from app.repo.RolePermissionRepo.organisation_role_permission import OrganisationLevelRolePermissionsRepo
from app.repo.RolePermissionRepo.system_role_permission_repo import  SystemRoleRepo
from app.repo.user_repo import UserRepo
from app.repo.user_device_repo import UserDeviceDetailRepo
from app.schemas.otp_schema import OTPSchema
from app.schemas.auth_schema import AuthResponse
from app.core.otpgenerate import generate_otp_for_user
from app.security.jwt_handler import create_access_token, create_refresh_token
from app.security.jwt_handler import decode_token
from app.email.service import email_service
from app.exceptions.custom_exception import *
from app.enums.scops import AccountType



class AuthService:
    def __init__(self,  auth_repo : AuthRepo , user_repo : UserRepo ,system_role_repo :SystemRoleRepo , org_role_repo : OrganisationLevelRolePermissionsRepo):
        self.auth_repo = auth_repo
        self.user_repo = user_repo


        self.org_role_repo = org_role_repo
        self.sys_role_repo =  system_role_repo



    def verify_otp(self,otp_schema : OTPSchema) : ## letter it will replace by redis_config

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
        if user.role in {UserRole.ADMIN,UserRole.SUPER_ADMIN}:
            permissions = ()


        access_token = create_access_token(user.id,user_role= user.role,organisation_id= user.organisation_id, employee_id = employee_id)

        if not access_token :
         raise Exception(f"access_token not generated for user {user.id} : {otp_schema.user_email}")
        refresh_token = create_refresh_token(user.id,user_role= user.role,organisation_id= user.organisation_id ) ## store the refresh token in userdevice
        if not refresh_token :
            raise Exception(f"access_token not generated for user {user.id} : {otp_schema.user_email}")

        return AuthResponse(
            access_token = access_token,
            refresh_token = refresh_token[1],
            token_type = "Bearer",
            expires_in =  3600,
            permission_list = list(permissions)
        )
            
        

    async def generate_otp_service(self,user_email,background_task :BackgroundTasks ):
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
        return otp_model

    def verify_access_token(self,token) -> AuthContext:

        payload = decode_token(token)
        user = self.user_repo.get_user(payload["user_id"])

        if not user:
            raise UserNotFound()
        user_role = ""
        if user.account_type == AccountType.ORGANISATION:

            employee :Employee = user.employee

            if  employee.emplopyee_status != EmployeeStatus.ACTIVE:
                raise EmployeeIsInactive
            if employee.employee_roles is None:
                raise Exception("Employee role not assigned")

            permissions = set()
            for rp in employee.employee_roles.organisation_permissions :
                permissions.add(rp.permission.name)

            auth  = AuthContext(
                                user_id=user.id,
                                organisation_id=user.organisation_id,
                                system_role=user.account_type.value,
                                employee_id=user.employee.id if user.employee else None,
                                permissions=permissions,
                                )
            user_role = employee.employee_roles.role.name
        if user.account_type == AccountType.SYSTEM:

            if user.system_role is None:
                raise Exception("System role not assigned")
            permissions = set()
            for rp in user.system_roles.system_role_permissions :
                permissions.add(rp.permission.name)
            auth = AuthContext(
                user_id = user.id,
                organiasation_id = None,
                system_role = user.account_type.value,
                employee_id =  None,
                permissions = permissions,
            )
            user_role = user.system_roles.system_role.name
        logger.info(f"auth model for user {user.id} has permissions of {permissions} for user role {user_role}")

        return auth













