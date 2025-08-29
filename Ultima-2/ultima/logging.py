import logging
import sys

from ultima.shared_arrtibs import APP_NAME

logger = logging.getLogger(APP_NAME)


def configure_logger(debug: int = 0) -> None:
    log_level = logging.DEBUG if debug == 1 else logging.INFO
    logger.setLevel(log_level)

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(log_level)

    formatter = logging.Formatter("%(message)s")

    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.propagate = False


configure_logger(0)
