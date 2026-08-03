# import logging
#
#
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#
#     )
# logger = logging.getLogger(__name__)


import logging
import colorlog

from app.core.loggingfilter import LoggingFilter

# handler = colorlog.StreamHandler()
#
# handler.addFilter(LoggingFilter())
#
# handler.setFormatter(
#     colorlog.ColoredFormatter(
#         "%(asctime)s | %(request_id)s | %(levelname)s | %(message)s",
#         log_colors={
#             "DEBUG": "cyan",
#             "INFO": "green",
#             "WARNING": "yellow",
#             "ERROR": "red",
#             "CRITICAL": "bold_red",
#         },
#     )
# )
#
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# logger.handlers.clear()
# logger.addHandler(handler)

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

app_handler = RotatingFileHandler(
    filename=f"{LOG_DIR}/app.log",
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5
)
app_handler.setFormatter(formatter)

error_handler = RotatingFileHandler(
    filename=f"{LOG_DIR}/error.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=5
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

logger = logging.getLogger("attendance")
logger.setLevel(logging.INFO)
logger.addHandler(app_handler)
logger.addHandler(error_handler)