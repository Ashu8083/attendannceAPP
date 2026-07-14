import time
import uuid

import jwt
from fastapi import Request, Depends
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.enums.role_enums import UserRole
from app.models import UserDeviceDetails
from app.repo.AuthRepo import AuthRepo
from app.repo.employee_repo import EmployeeRepo
from app.repo.organisation_repo import OrganisationRepo
from app.repo.role_repo import RolePermissionRepo
from app.repo.user_device_repo import UserDeviceDetailRepo
from app.repo.user_repo import UserRepo
from app.security.jwt_handler import decode_token
from app.core.logging_config import logger
from app.core.request_context import request_id_ctx
from app.dependancy.service_dependancy import  get_user_service
from app.service import user_service
from app.db.database import SessionLocal
from app.service.role_services.role_creation_service import RoleService
from app.service.user_service import UserService
from app.service.auth_service import AuthService
from app.exceptions.custom_exception import MissingAuthorizationHeader,MissingToken


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
            "/docs",
            "/openapi.json",
            "/redoc",
            "/email/test"
        ]

        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        auth_header = request.headers.get("Authorization") # extract the token from header
        if not auth_header:
            raise MissingAuthorizationHeader
        scheme , token = auth_header.split() # split the token from the bearer
        if scheme != "Bearer":
            raise  MissingAuthorizationHeader
        if not token:
            raise MissingToken

        auth_service = AuthService(auth_repo=AuthRepo(db_session),user_repo=UserRepo(db_session),employee_repo=EmployeeRepo(db_session),user_device=(UserDeviceDetailRepo(db_session)))

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