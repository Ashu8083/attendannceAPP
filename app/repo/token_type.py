from sqlalchemy.orm import Session

from app.models.token import Token


class TokenRepo():
    def __init__(self,db:Session):
        self.db = db

    def create(self,token: Token):
        self.db.add(token)
        return token
    def get_by_token(self,token: Token):
        return self.db.query(Token).filter(Token.token == token).first()

    def get_token_by_device_id(self,device_id: str):
        return self.db.query(Token).filter(Token.device_id == device_id).first()

    def delete_by_token(self,token: Token):
        self.db.delete(token)
        self.db.commit()
        return token
    def update_token(self,token : Token):
        self.db.commit()
        return token








