from sqlalchemy.orm import Session,joinedload

from app.models import Employee
from app.models.user_models import User
import uuid
from app.enums.role_enums import UserRole

from app.enums.user_status_enums import UserStatus

from app.repo.organisation_repo import Organisation
from app.schemas.user import UserCreation,UserUpdate
from app.repo.organisation_repo import OrganisationRepo
from app.repo.user_device_repo import UserDeviceDetailRepo
from app.enums.role_enums import UserRoleUpdated
from app.exceptions.custom_exception import UserNotFound
from app.enums.scops import AccountType
from app.core.logging_config import logger

#for adding organisation admin only 
# repo are only made for communicate with db 
class UserRepo:

    def __init__(self , db : Session):
        self.db = db

    def get_user_by_email(self,user_email : str):
        user = self.db.query(User).filter(User.email ==user_email).first()
        return user

    def get_user(self, user_id: uuid.UUID):
        return (
            self.db.query(User)
            .options(
                joinedload(User.employee)
                .joinedload(Employee.role)
            )
            .filter(User.id == user_id, User.status == UserStatus.ACTIVE)
            .first()
        )
    def create_user_as_employee(self,full_name,email,organisation_id):
            user = User(
                 full_name = full_name,
                 email = email,
                 organisation_id = organisation_id,
                 account_type = AccountType.SYSTEM,
                 status = UserStatus.ACTIVE
            )
            logger.info("Trying to creating user for Employee with Info %s",user)
            self.db.add(user)
            self.db.flush()
            return user
        
    def create_user(self,data:UserCreation,organisation_id):
            
            user = User(
                 full_name = data.full_name,
                 organisation_id = organisation_id,
                 email = data.email,
                 account_type = data.account_type,
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
        user_id = self.db.query(User.id).filter(User.email == email).scalar()
        return user_id

    def get_user_by_id(self,id : uuid.UUID):
        user = self.db.query(User).filter(User.id == id).first()
        return user

    def create_user_device(self, ):
        return

    def get_user_status_by_id(self,id : uuid.UUID):
        user_status = self.db.query(User.status).filter(User.id == id).first()
        return user_status

    def suspend_user(self,user_id: uuid.UUID):
        user =self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFound(str(user_id))
        user.status = UserStatus.SUSPENDED
        try:
            self.db.commit()
            self.db.refresh(user)
        except Exception as e :
            raise
        return user

