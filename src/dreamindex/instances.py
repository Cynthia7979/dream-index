"""
Defines publicly visible classes
"""

from dreamindex.logging import logged, get_file_logger
from os.path import dirname


@logged
class User:
    def __init__(self, user_name, user_id):
        self.name = user_name
        self.user_id = user_id
        self.avatar = f'{dirname(__file__)}/static/img/avatars/{user_id}.png'


@logged
class Article:
    def __init__(self, title, content, views=0, likes=0, comments=()):
        self.title = title
        self.content = content
        self.views = views
        self.likes = likes
        self.comments = comments
        self.logger.debug(f'New {self.__class__.__name__} instance created (title={title}).')

    @property
    def raw_content(self):
        pass # do something to strip off the html style.

    def get_summary(self, length=150):
        # TODO: Need to make sure that HTML code doesn't get cut off - an auto-updating raw_text attribute?
        return self.content[:length]


@logged
class DreamCard(Article):
    def __init__(self, title, content, views=0, likes=0, comments=(), num_fan_arts=0):
        super().__init__(title, content, views, likes, comments)
        self.num_fan_arts = num_fan_arts


@logged
class FanArtCard(Article):
    def __init__(self, title, content, father_dream_title, views=0, likes=0, comments=()):
        super().__init__(title, content, views, likes, comments)
        self.father_dream = DreamCard(title=father_dream_title, content='')


@logged
class Dream(DreamCard):
    def __init__(self, title, content, author: User, views=0, likes=0, comments=(), fan_arts=()):
        super().__init__(title, content, views, likes, comments)
        self.author = author
        self.num_fan_arts = len(fan_arts)
        self.fan_arts = fan_arts


@logged
class FanArt(FanArtCard):
    def __init__(self, title, content, father_dream, author: User, views=0, likes=0, comments=()):
        super().__init__(title, content, '', views, likes, comments)
        self.father_dream = father_dream
        self.author = author

