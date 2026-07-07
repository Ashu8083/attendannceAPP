import uuid

from app.enums.user_status_enums import UserStatus
from app.repo.user_repo import UserRepo
from app.repo.organisation_repo import OrganisationRepo
from app.service.organisation_service import OrganisationService



from app.schemas.user import UserCreation,UserStatusUpdate,UserUpdate,UserUpdatePassword


class UserService():
    def __init__(self,userrepo: UserRepo , organisation_repo : OrganisationRepo):
        self.userrepo = userrepo
        self.organisation_repo = organisation_repo

    def create_user_service(self,user_data : UserCreation):

        user = self.userrepo.get_user_by_email(user_email= user_data.email)
        organisation_id = self.organisation_repo.get_organisation_id(organisation_code=user_data.organisation_code)
        print (organisation_id)
        if  user:
               return ("user already exist")
        user = self.userrepo.create_user(user_data,organisation_id)
        print (user)
        return user

    def get_user(self,user_email :str ):
        user = self.userrepo.get_user_by_email(user_email)
        if not user:
           print( "user not found")
        return user
    def get_user_status(self,user_email:str,data: UserStatusUpdate):

        user = self.userrepo.get_user_by_email(user_email)
        if not user:
            raise ValueError("user not found")
              
            
        user = self.userrepo.updateUser(data)   
        return user
    def update_user(self,user_email : str ,data: UserUpdate):

        user = self.userrepo.get_user_by_email(user_email)
        if not user:
            raise ValueError ("user not found")
                
        return self.userrepo.updateUser(data)

    def get_user_by_id(self,user_id :uuid.UUID):
        return self.userrepo.get_user_by_id(user_id)

    def get_user(self,user_id : uuid.UUID):
        if not self.userrepo.get_user_by_id(user_id):
            raise ValueError("user not found")
        user_status = self.userrepo.sta
        if user_status != UserStatus.ACTIVE:
            raise ValueError("user is Inactive")
        return self.userrepo.get_user(user_id)



