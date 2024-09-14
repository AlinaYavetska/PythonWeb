import logging
from logging.handlers import RotatingFileHandler


def init_logger() -> None:
    log_format = "%(asctime)s - %(levelname)s - [%(name)s:%(lineno)d] - %(message)s"
    logging.basicConfig(
        level=logging.INFO, format=log_format, handlers=[]
    )
    file_handler = RotatingFileHandler(
        "./logs/myapp.log", maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger("").addHandler(file_handler)