from fastapi import Request,HTTPException,status
from app.core.logging_config import logger
from app.enums.employee_status import EmployeeStatus


class PermissionChecker:

    def __init__(self,permission : str , account_scope : str ):
        self.permission = permission
        self.account_scope = account_scope

    def __call__(self,request: Request):

        permissions = []
        try:
            permissions = request.state.auth.permissions
            account_scope = request.state.auth.account_scope
        except Exception as e:
            logger.error(f"error occure while fetching permission in auth {e}")
            raise

        finally:
            if self.permission not in permissions:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Permission denied",)
            if self.account_scope == account_scope:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Permission denied",)


