import uuid
from app.repo.user_repo import UserRepo
from app.service.organisation_service import OrganisationService



from app.schemas.user import UserCreation,UserStatusUpdate,UserUpdate,UserUpdatePassword


class UserService():
    def __init__(self,userrepo: UserRepo):
        self.userrepo = userrepo
    def create_user_service(self,user_data : UserCreation):

        user = self.userrepo.get_user_by_email(user_email= user_data.email)
        organisation = OrganisationService.get_organisation(user_data.organisation_code)
        if not user:
            raise {
                "user already exist"
            }
        user = self.userrepo.create_user(user_data)
    def get_user(self,user_email :str ):

        user = self.userrepo.get_user_by_email(user_email)

        if not user:
            raise{
                "user not found"
            }

        return user
    def get_user_status(self,user_email:str,data: UserStatusUpdate):

        user = self.userrepo.get_user_by_email(user_email)
        if not user:
            raise{
                "user not found"
            }
        user = self.userrepo.updateUser(data)   

        return user
    def update_user(self,user_email : str ,data: UserUpdate):

        user = self.userrepo.get_user_by_email(user_email)

        if not user:
            raise{
                "user not found"
            }
        return self.userrepo.updateUser(data)
    

