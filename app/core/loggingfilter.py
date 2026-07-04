import logging
from app.core.request_context import request_id_ctx

class LoggingFilter(logging.Filter):

    def filter(self, record):
        record.request_id = request_id_ctx.get()
        return True