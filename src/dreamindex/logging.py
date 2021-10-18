import logging
import datetime
from os.path import dirname

root_logger = logging.getLogger("Dream Index")
root_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(dirname(__file__)+"/logs/")

def get_file_logger(name):
    return logging.getLogger(name)


# Logged decorator
# copied from my other project ~Cynthia
def logged(cls, fname):
    class_name = cls.__name__
    logger = logging.getLogger('Tool-Program.{}.{}'.format(fname, cls))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.propagate = False
    setattr(cls, 'logger', logger)
    return cls
