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

handler = colorlog.StreamHandler()

handler.addFilter(LoggingFilter())

handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(asctime)s | %(request_id)s | %(levelname)s | %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(handler)