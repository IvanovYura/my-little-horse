from logging import Logger, getLogger, StreamHandler, INFO, Formatter
import sys

LOG_FORMAT = "%(asctime)s\t%(levelname)s\t%(message)s"


def init_logger(level: int, handler: StreamHandler) -> Logger:
    """
    Returns logger with output to STDOUT
    """
    logger = getLogger()
    logger.setLevel(level)

    logger.addHandler(handler)
    formatter = Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)

    return logger


logger = init_logger(INFO, StreamHandler(sys.stdout))
