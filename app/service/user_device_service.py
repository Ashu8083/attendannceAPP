from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.token import Token
from app.repo.user_device_repo import UserDeviceDetailRepo
from app.repo.user_device_repo import UserDeviceCreate
from app.core.logging_config import logger
from app.db.UnitOfWork import UnitOfWork
from app.enums.token_schema import TokenSchema
from app.repo.token_repo import TokenRepo
from app.repo.user_repo import UserRepo


class UserDeviceAndTokenService:
    def __init__(self,user_device_repo : UserDeviceDetailRepo ,token_repo : TokenRepo):
        self.user_device_repo=user_device_repo

        self.token_repo=token_repo

    def create_user_device_and_token(self,user_id : UUID ,create_user_device: UserDeviceCreate, token_schema : TokenSchema):

        user_device = self.user_device_repo.get_user_active_device(user_id= user_id, device_unique_id= create_user_device.device_unique_id)
        create_token = []
        if  user_device:
            user_device.last_login = datetime.now()
            token_in_db = self.token_repo.get_user_active_token(user_id=user_device.user_id)
            if token_in_db:
                token_in_db.is_revoked = True
                self.token_repo.revoke_token(token=token_in_db)

            token : Token = Token(
                    user_id = token_schema.user_id,
                    device_id = user_device.id,
                    refresh_token = token_schema.refresh_token,
                    expires_at = token_schema.expires_at,
                            )
            create_token = self.token_repo.create(token=token)

        if not  user_device:
            user_device = self.user_device_repo.create_user_device(user_id=user_id, userdevice=create_user_device)
            if not user_device:
                logger.info("User device not created".format(user_device))
            token_in_db = self.token_repo.get_user_active_token(user_id=user_device.user_id)
            if token_in_db:
                token_in_db.is_revoked = True
                self.token_repo.revoke_token(token=token_in_db)

            token: Token = Token(
                user_id=token_schema.user_id,
                device_id=user_device.id,
                refresh_token=token_schema.refresh_token,
                expires_at=token_schema.expires_at,
            )
            create_token = self.token_repo.create(token=token)
            logger.info("new refresh token created {}".format(token.user_id))
            logger.info(f"Created new user device for user {user_id}")
        return user_device,create_token


    def get_user_device(self,user_id):
        return




