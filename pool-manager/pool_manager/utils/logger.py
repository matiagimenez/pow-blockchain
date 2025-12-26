import sys

from loguru import logger as logger_


def configure_logger():
    logger_.remove()
    logger_.add(
        sys.stdout,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        serialize=False,
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )
    return logger_


logger = configure_logger()
