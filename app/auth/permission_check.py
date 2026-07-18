from fastapi import Request,HTTPException,status

from app.enums.employee_status import EmployeeStatus


class PermissionChecker:

    def __init__(self,permission : str , account_scope : str ):
        self.permission = permission
        self.account_scope = account_scope

    def __call__(self,request: Request):

        permissions = request.state.auth.permissions
        account_scope = request.state.auth.account_scope

        if self.permission not in permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Permission denied",)
        if self.account_scope == account_scope:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Permission denied",)


