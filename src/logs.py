import logging
import sys

def get_logger():
    logger = logging.getLogger("__main__")
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s-%(name)s-%(levelname)s-%(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger