import time
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.repo.user_device_repo import UserDeviceDetailRepo
from app.repo.RolePermissionRepo.organisation_role_permission import OrganisationLevelRolePermissionsRepo
from app.repo.RolePermissionRepo.system_role_permission_repo import SystemRoleRepo
from app.core.logging_config import logger
from app.core.request_context import request_id_ctx
from app.db.database import SessionLocal
from app.repo.AuthRepo import AuthRepo
from app.repo.user_repo import UserRepo
from app.repo.employee_repo import EmployeeRepo
from app.repo.user_device_repo import UserDeviceDetailRepo
from app.service.auth_service import AuthService

from app.service.user_device_service import UserDeviceAndTokenService
from app.repo.token_repo import TokenRepo


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())

        request.state.request_id = request_id # request id for each request create

        token_request_id = request_id_ctx.set(request_id)

        start = time.perf_counter()

        logger.info(
            f"{request.method} {request.url.path} started"
        )

        db_session = SessionLocal()

        PUBLIC_ROUTES = [   # all the public api , which are not going throuh the security
            "/auth/otp-login",
            "/auth/otp-verify",
            "/auth/refresh-access-token",
            "/docs",
            "/openapi.json",
            "/favicon.ico",
            "/redoc",
            "/email/test",
        ]

        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        auth_header = request.headers.get("Authorization") # extract the token from header
        if not auth_header:
            return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "error": {
                "code": "MISSING_AUTHORIZATION_HEADER",
                "message": "Missing Authorization header",
            },
        },
    )
        scheme , token = auth_header.split() # split the token from the bearer
        if scheme != "Bearer":
            return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "error": {
                "code": "MISSING_AUTHORIZATION_HEADER",
                "message": "Missing Authorization header",
            },
        },

    )
        if not token:
            return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "error": {
                "code": "MISSING_TOKEN",
                "message": "Missing Session",
            },
        },

    )

        auth_service = AuthService(db= db_session,
                                   auth_repo=AuthRepo(db_session)
                                   , user_repo=UserRepo(db_session)
                                   ,system_role_repo=SystemRoleRepo(db_session),
                                   token_repo=TokenRepo(db_session),
                                   user_device_repo=UserDeviceDetailRepo(db_session)
                                   ,user_device_and_token_service=UserDeviceAndTokenService(user_device_repo = UserDeviceDetailRepo(db_session)
                                                                                            , token_repo = TokenRepo(db_session)),
                                   org_role_repo= OrganisationLevelRolePermissionsRepo(db_session))
        auth =   auth_service.verify_access_token(token)
        if auth is None:
            raise
        request.state.auth = auth
        try:
            response = await call_next(request)

            duration = time.perf_counter() - start

            logger.info(
                f"{request.method} {request.url.path} "
                f"status={response.status_code} "
                f"duration={duration:.3f}s"
            )

            return response

        finally:
            request_id_ctx.reset(token_request_id)