from sqlalchemy.orm import Session
from app.models.user_models import User
import uuid
from app.enums.role_enums import UserRole

from app.enums.user_status_enums import UserStatus

from app.repo.organisation_repo import Organisation
from app.schemas.user import UserCreation,UserUpdate
from app.repo.organisation_repo import OrganisationRepo
from app.repo.user_device_repo import UserDeviceDetailRepo


#for adding organisation admin only 
# repo are only made for communicate with db 
class UserRepo:

    def __init__(self , db : Session):
        self.db = db

    def get_user_by_email(self,user_email : str):
        user = self.db.query(User).filter(User.email ==user_email).first()
        return user
    
    def create_user_as_employee(self,full_name,email,organisation_id):
            user = User(
                 full_name = full_name,
                 email = email,
                 organisation_id = organisation_id,
                 role = UserRole.EMPLOYEE,
                 status = UserStatus.ACTIVE
            )
            try :
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
            except Exception as e :
                 self.db.rollback()
                 raise e

            return user
        
    def create_user(self,data:UserCreation,organisation_id):
            
            user = User(
                 full_name = data.full_name,
                 organisation_id = organisation_id,
                 email = data.email,
                 role = data.role
            )
            try:
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
            except Exception as e:
                self.db.rollback()
                print(e)
                raise e
            print(user.email)
            return user

    def updateUser(self,data:UserUpdate):
         
        user =  self.db.query(User).filter(User.full_name == data.email).first()    
      
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():

         setattr(user, field, value)

        self.db.commit()

        self.db.refresh(user)

        return user
    def get_id_by_email(self,email):
        user_id = self.db.query(User.id).filter(User.email == email).first()
        return user_id[0]

    def get_user_by_id(self,id : uuid.UUID):
        user = self.db.query(User).filter(User.id == id).first()

    def create_user_device(self, ):
        return