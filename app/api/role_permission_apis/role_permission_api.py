import uuid

from fastapi import APIRouter ,Depends

from app.dependancy.service_dependancy import get_role_service

permission_router: APIRouter = APIRouter()


@permission_router.get("/get-all-permission/{role_name}/{organisation_id}")
def get_all_permission(role_name : str, organisation_id : uuid.UUID,
                       role_service = Depends(get_role_service()) )  :

    return role_service.get_all_permission(role_name,organisation_id)

@permission_router.post("create-role")
def create_role(self,data):
    return


@permission_router.delete("/remove-permission")
def remove_permission(self,data):
    return

@permission_router.put("/update-permission")
def update_permission(self,data):
    return

@permission_router.get("/create-permission")
def get_permission(self,data):
    return