from sqlalchemy.orm import Session
from app.models.user_models import User

from app.repo.organisation_repo import Organisation
from app.schemas.user import UserCreation,UserUpdate
from app.repo.organisation_repo import OrganisationRepo

class UserRepo:

    def __init__(self , db : Session):
        self.db = db

    def get_user_by_email(self,user_email : str):
        return(
            self.db.query(User).filter(User.email ==user_email ).first()
        )
    
    def create_user(self,data : UserCreation):
            user = User(
                 full_name = data.full_name,
                 organisation_id = data.organisation_id,
                 email = data.email,
                 password_hash = data.password,
                 role = data.role,
                 user_status = data.userStatus
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            return user

    def updateUser(self,data:UserUpdate):
         
        user =  self.db.query(User).filter(User.full_name == data.email).first()
        if not user :
             return 
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():

         setattr(user, field, value)

        self.db.commit()

        self.db.refresh(user)

        return user