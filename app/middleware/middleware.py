import time
import logging
from urllib import response
from urllib.request import Request


from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        start = time.time()
        logger.info(
            f"{request.method} {request.url.path} started"

        )
        resonse = await call_next(request)
        duration = time.time()-start

        logger.info(
            f"{request.method} {request.url.path}"
            f"status = {response.status_code}"
            f"duration = {duration}"
        )

        return resonse
