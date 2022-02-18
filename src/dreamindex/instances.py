"""
Defines publicly visible classes
"""

import datetime
from dreamindex.logging import logged, get_file_logger
from os.path import dirname


class Base:
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        repr_string = f'<{self.__class__.__name__} instance with '
        for attribute in self.__dict__:
            repr_string += f'{attribute}={self.__getattribute__(attribute)}, '
        return repr_string.rstrip(', ')+'>'


@logged
class User(Base):
    def __init__(self, user_name, user_id):
        super().__init__()
        self.name = user_name
        self.user_id = user_id
        self.avatar = f'{dirname(__file__)}/static/img/avatars/{user_id}.png'


@logged
class Article(Base):
    def __init__(self, id_, title, content, views=0, likes=0, comments=()):
        super().__init__()
        self.id = id_
        self.title = title
        self.content = content
        self.views = views
        self.likes = likes
        self.comments = list(comments)
        self.type = 'None'
        self.default_summary = self.get_summary()
        self.logger.debug(f'New {self.type} instance created (title={title}).')

    @property
    def raw_content(self):
        pass # TODO: do something to strip off the html style.

    @property
    def num_comments(self):
        return len(self.comments)

    def get_summary(self, length=150):
        # TODO: Need to make sure that HTML code doesn't get cut off - an auto-updating raw_text attribute?
        return self.content[:length]


@logged
class Dream(Article):
    def __init__(self, id_, title, content, author: User, views=0, likes=0, comments=(), fan_art_ids=(), characters=()):
        super().__init__(id_, title, content, views, likes, comments)
        self.author = author
        self.num_fan_arts = len(fan_art_ids)
        self.fan_art_ids = list(fan_art_ids)
        self.characters = list(characters)
        self.type = 'Dream'


@logged
class FanArt(Article):
    def __init__(self, id_, title, content, father_dream_id, father_dream_author:User, author: User, views=0, likes=0, comments=()):
        super().__init__(id_, title, content, views, likes, comments)
        self.father_dream_id = father_dream_id
        self.father_dream_author = father_dream_author
        self.author = author
        self.type = "FanArt"


@logged
class Character(Base):
    def __init__(self, character_name, character_description):
        super().__init__()
        self.name = character_name
        self.description = character_description


@logged
class Comment(Base):
    def __init__(self, id_: int, author: User, content: str, publish_time: str, secondary_comments=()):
        """
        Creates a comment instance
        :param id_: Comment ID
        :param author: Author of the
        :param content: Comment content
        :param secondary_comments: A list containing Comment instances
        """
        super().__init__()
        self.id = id_
        self.author = author
        self.content = content
        self._publish_time = publish_time
        self.secondary_comments = list(secondary_comments)

    @property
    def num_secondary_comments(self):
        return len(self.secondary_comments)

    @property
    def publish_time(self):
        return datetime.datetime.fromisoformat(self._publish_time)


@logged
class DreamComment(Comment):
    def __init__(self, id_, author: User, content, father_dream_id: int, publish_time: str):
        super().__init__(id_, author, content, publish_time)
        self.article_type = 'dream'
        self.father_dream_id = father_dream_id


@logged
class FanArtComment(Comment):
    def __init__(self, id_, author: User, content, father_fan_art_id: int, publish_time: str):
        super().__init__(id_, author, content, publish_time)
        self.article_type = 'fanart'
        self.father_fan_art_id = father_fan_art_id
