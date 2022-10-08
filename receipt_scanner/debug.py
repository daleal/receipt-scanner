import logging


def configure_logger(debug: bool) -> None:
    if debug:
        logging.basicConfig(level=logging.DEBUG)
