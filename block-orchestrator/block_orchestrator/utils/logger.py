from loguru import logger
import sys

def configure_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        serialize=False,
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )
    return logger


logger = configure_logger()