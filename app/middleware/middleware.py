import time
import uuid

import jwt
from fastapi import Request, Depends
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.security.jwt_handler import decode_token
from app.core.logging_config import logger
from app.core.request_context import request_id_ctx
from app.dependancy.service_dependancy import  get_user_service
from app.service import user_service
from app.db.database import SessionLocal
from app.service.user_service import UserService


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
            "/otp-login",
            "/otp-verify",
            "/docs",
            "/openapi.json",
            "/redoc"
        ]

        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        auth_header = request.headers.get("Authorization") # extract the token from header
        if not auth_header:
            return JSONResponse( content={"message": "Missing Authorization header"},
                                status_code= status.HTTP_401_UNAUTHORIZED)


        scheme , token = auth_header.split() # split the token from the bearer
        if scheme != "Bearer":
            return JSONResponse(
                content={"message": "Invalid Authorization header"},
                status_code=status.HTTP_401_UNAUTHORIZED)



        try:
            paylod = decode_token(token) #the decode will done here
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                content={"message": "Token has expired or Invalid Authorization Header"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )


        # user session create for verify the user from db
        try :
            user_service = UserService(db_session)
            user = user_service.get_user_by_id(uuid.UUID(paylod["user_id"]))
        finally:
            db_session.close()

        if  not user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "User does not exist"},
            )


        # user payload attach to the  request
        request.state.userpayload = paylod


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