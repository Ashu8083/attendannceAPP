from sqlalchemy.orm import Session
from models.user_models import User

class UserRepo:

    def __init__(self , db : Session):
        self.db = db
    def get_employee_by_email(self,user_email : str):
        return(
            self.db.query(User).filter(User.email ==user_email ).first()
        )
