import logging
import sys
from datetime import datetime
from os.path import dirname

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)7s | %(message)s')
root_logger = logging.getLogger("DreamIndex")
root_logger.setLevel(logging.DEBUG)
_handlers = (
    logging.FileHandler(
        dirname(__file__)+f"/logs/dreamindex_log_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    ),
    # logging.StreamHandler(sys.stdout)
)


def config_handlers(logger: logging.Logger):
    for handler in _handlers:
        logger.addHandler(handler)
    root_logger.debug(f"Added handlers for {logger.name}")


def get_file_logger(name):
    logger = logging.getLogger(name)
    config_handlers(logger)
    return logger


# Logged decorator
# copied from my other project ~Cynthia
def logged(cls):
    class_name = cls.__name__
    logger = logging.getLogger(f'DreamIndex.{class_name}')
    logger.setLevel(logging.DEBUG)
    config_handlers(logger)
    setattr(cls, 'logger', logger)
    return cls
