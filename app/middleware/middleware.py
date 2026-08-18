import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging_config import logger
from app.core.request_context import request_id_ctx


class RequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        token_request_id = request_id_ctx.set(request_id)
        start = time.perf_counter()
        logger.info(
            f"{request.method} {request.url.path} started"
        )
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