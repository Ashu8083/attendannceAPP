import logging
from urllib import response

from sqlalchemy import true


from datetime import date, time, timedelta

from app.repo import user_device_repo
from app.repo.AuthRepo import AuthRepo
from app.repo.user_repo import UserRepo
from app.repo.user_device_repo import UserDeviceDetailRepo
from app.schemas.otp_schema import OTPSchema
from app.core.otpgenerate import generate_otp_for_user
from app.core.logging_config import  logger
from app.security.jwt_handler import create_access_token, create_refresh_token


class AuthService:
    def __init__(self,  auth_repo : AuthRepo , user_repo : UserRepo , user_device : UserDeviceDetailRepo  ):
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        self.user_device_repo = user_device


    def verify_otp(self,otp_schema : OTPSchema) : ## letter it will replace by redis

        user = self.user_repo.get_user_by_email(otp_schema.user_email)
        if not user:
            raise Exception(f"User with email {otp_schema.user_email} not fx und")

        otp = self.auth_repo.get_otp(user.id)
        if not otp :
             raise Exception(f"otp not found or invalid")
        if otp.otp != otp_schema.otp :
            raise Exception(f"otp not found or invalid")
        access_token = create_access_token(user.id,user_role= user.role,organisation_id= user.organisation_id )
        refresh_token = create_refresh_token(user.id,user_role= user.role,organisation_id= user.organisation_id ) ## store the refresh token in userdevice
                                                                                                                 # table in db
        token_store = user_device_repo.ce
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 3600,
        }

    def generate_otp_service(self,user_email ):
        user_id = self.user_repo.get_id_by_email(user_email)
        if not user_id:
            raise Exception(f"User with email {user_email} not fx und")
        otp = generate_otp_for_user()
        otp_model = self.auth_repo.create_otp(user_id, otp)
        if not otp_model:
            logger.error(f"otp model for user {user_id} not created")
            raise Exception(f"otp creation error")
        return otp_model.otp












