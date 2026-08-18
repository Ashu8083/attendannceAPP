from fastapi import Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.database import SessionLocal

from app.repo.AuthRepo import AuthRepo
from app.repo.user_repo import UserRepo
from app.repo.user_device_repo import UserDeviceDetailRepo
from app.repo.RolePermissionRepo.organisation_role_permission import (
    OrganisationLevelRolePermissionsRepo
)
from app.repo.RolePermissionRepo.system_role_permission_repo import (
    SystemRoleRepo
)
from app.repo.token_repo import TokenRepo

from app.service.auth_service import AuthService
from app.service.user_device_service import UserDeviceAndTokenService

from app.exceptions.custom_exception import TokenInValid


bearer_scheme = HTTPBearer()


async def get_current_auth(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    token = credentials.credentials
    db_session = SessionLocal()
    try:
        auth_service = AuthService(
            db=db_session,
            auth_repo=AuthRepo(db_session),
            user_repo=UserRepo(db_session),
            system_role_repo=SystemRoleRepo(db_session),
            token_repo=TokenRepo(db_session),
            user_device_repo=UserDeviceDetailRepo(db_session),
            user_device_and_token_service=UserDeviceAndTokenService(
                user_device_repo=UserDeviceDetailRepo(db_session),
                token_repo=TokenRepo(db_session)
            ),
            org_role_repo=OrganisationLevelRolePermissionsRepo(
                db_session
            )
        )
        auth = auth_service.verify_access_token(token)
        if auth is None:
            raise TokenInValid()
        # Store authentication information
        request.state.auth = auth
        # Return authenticated information
        return auth
    finally:
        db_session.close()