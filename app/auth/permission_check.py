from fastapi import Request,HTTPException,status

from app.enums.employee_status import EmployeeStatus


class PermissionChecker:

    def __init__(self,permission : str ):
        self.permission = permission

    def __call__(self,request: Request):

        permissions = request.state.auth.permissions

        if self.permission not in permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Permission denied",)

