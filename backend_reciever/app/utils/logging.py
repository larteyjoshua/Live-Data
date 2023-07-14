from loguru import logger
# Set the log format
logger.add(
    "logs.log",
    rotation="500 MB",
    format="{time} - {level} - {message}",
    level="DEBUG",
    backtrace=True,
    diagnose=True,
    enqueue=True
)

log = logger
