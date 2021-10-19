"""
Defines publicly visible classes
"""

from dreamindex.logging import logged, get_file_logger


@logged
class Article:
    def __init__(self):
        pass


@logged
class Dream(Article):
    def __init__(self):
        super().__init__()


@logged
class FanArt(Article):
    def __init__(self):
        super().__init__()

