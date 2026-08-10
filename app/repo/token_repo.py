from sqlalchemy.orm import Session
from uuid import  UUID
from app.models.token import Token
from app.core.logging_config import logger


class TokenRepo():
    def __init__(self,db:Session):
        self.db = db

    def create(self,token: Token):
        self.db.add(token)
        return token

    def get_user_active_token(
            self,
            user_id: UUID,
            device_id: UUID
    ):
        logger.info(
            f"Getting active token for user {user_id} with device {device_id}"
        )
        refresh_model = (
            self.db.query(Token)
            .filter(
                Token.user_id == user_id,
                Token.device_id == device_id,
                Token.is_revoked.is_(False)
            )
            .first()
        )
        if not refresh_model:
            logger.info(
                f"No active token found for user {user_id} "
                f"and device {device_id}"
            )
            return None
        logger.info(
            f"Active token found: {refresh_model.id}"
        )
        logger.info(
            f"Token revoked: {refresh_model.is_revoked}"
        )
        return refresh_model


    def get_user_tokens(self,user_id: UUID):
        token = self.db.query(Token).filter(Token.user_id == user_id).all()
        return token
    def revoke_token(self,token: Token):
        try:
            self.db.add(token)
            self.db.commit()
            self.db.refresh(token)
            logger.info(f"revoked token {token.id}")
        except Exception as e:
            self.db.rollback()
            logger.error("token revoke error {} for token {} ",format(e) ,format(token.id))
        return token
    def get_token_by_device_id(self,device_id: str):
        return self.db.query(Token).filter(Token.device_id == device_id).first()

    def delete_by_token(self,token: Token):
        self.db.delete(token)
        self.db.commit()
        return token
    def update_token(self,token : Token):
        self.db.commit()
        return token








