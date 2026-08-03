from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse



from app.dependancy.service_dependancy import get_user_service
from app.schemas.user import UserCreation,UserDetailsRespone,UserStatusUpdate,UserStatus,UserUpdate
from app.service.user_service import UserService

user_router = APIRouter(prefix="/user",tags=["user"])

@user_router.post("/create-user",response_model=UserDetailsRespone)
def create_user(user_data : UserCreation,
                service : UserService = Depends(get_user_service) ):
    
    return service.create_user_service(user_data)
    

@user_router.put("/update-user",)
def update_user():
    return

@user_router.get("/get-user/{user_email}",response_model=UserDetailsRespone)
def get_user(user_email : str,
                service : UserService = Depends(get_user_service) ):
    return service.get_user(user_email)

@user_router.get("/user-status")
def get_user_status():
    return

@user_router.post("/get_user_role_permissions")
def get_user_role_permissions(useremail : str,):
    return

@user_router.get("/get-user-by-account-scope",response_model=list[UserDetailsRespone])
def get_user_account_scope(account_scope : str, service: UserService = Depends(get_user_service)):
    return service.get_user_by_account_scope(account_scope)

@user_router.post("/assign-user-role")
def assign_user_role(user_id , user_role ,service : UserService = Depends(get_user_service)):
    return service.assign_role_user(user_id,user_role)



