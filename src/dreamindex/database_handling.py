"""
Connects the code to the SQLite database.

Junction tables were not used for comment linking,
    because article-comment is a one-to-many relationship
    and can be retrieved by querying the comment table itself.

For article-character, however, junction tables were used because it is a
    one-to-many relationship (so was author-character).

On Naming:
    Use PascalCasing for tables and column names,
    fish_bone_casing for all variables,
    pk_TableName for primary key columns in join tables,
    and UPPERCASE abbreviations (e.g. ID, dreamID)

PublishTime Format: YYYY-MM-DD HH:MM:SS.SSS

Refer to the following link for additional naming conventions:
https://stackoverflow.com/questions/7662/database-table-and-column-naming-conventions
"""
from dreamindex.logging import logged, get_file_logger
from dreamindex.instances import *
import sqlite3
import os


@logged
class Database:
    def __init__(self, database_path):
        self.database_path = database_path
        self.write_lock = False  # TODO: Finish this lock when needed
        self._connet()
        self.logger.info(f"Database instance on {self.database_path} is created.")

    def get_dreams(self, sort='PublishTime', order='desc', condition="", count=1):
        result = self._perform_query(table='Dream', sort=sort, order=order, condition=condition, count=count)
        dreams = []
        for row in result:
            dream_id, title, author_id, publish_time, content, likes, num_comments, views = row
            comments = self.get_comments('dream', dream_id)
            author = self.get_user(user_id=author_id)
            fan_arts = self.get_fan_arts(condition=f'FatherDreamID={dream_id}')
            dreams.append(Dream(title, content, author, views, likes, comments, fan_arts))
        return dreams

    def get_comments(self, article_type, id_, count=None):
        """
        Retrieves the comments for an article
        :param article_type: String. Either 'dream' or 'fanart'
        :param id_: The article's ID
        :param count: Number of comments to get (excluding secondary ones)
        :return: A list containing Comment instances
        """
        article_type = 'Dream' if article_type == 'dream' else 'FanArt'
        result = self._perform_query(
            table=f'{article_type}Comment',
            sort='PublishTime',
            condition=f'Father{article_type}ID={id_}',
            count=count
        )
        comments = []
        for comment_row in result:
            comment_id, author_id, comment_content, _father_dream_id, publish_time = comment_row
            secondary_comments = []
            sec_com_result = self._perform_query(
                table=f'Secondary{article_type}Comment',
                sort='PublishTime',
                condition=f'FatherCommentID={comment_row[0]}'
            )
            for sec_com_row in sec_com_result:
                sec_comment_id, sec_author_id, sec_comment_content, _, sec_publish_time = sec_com_row
                secondary_comments.append(Comment(
                    sec_comment_id, self.get_user(user_id=sec_author_id), sec_comment_content, sec_publish_time
                ))
            comments.append(Comment(
                comment_id, self.get_user(user_id=author_id), comment_content, publish_time,
                secondary_comments=secondary_comments
            ))
        return comments

    def get_fan_arts(self, sort='PublishTime', order='desc', condition="", count=1, card=False):
        result = self._perform_query(
            table='FanArt',
            sort=sort,
            order=order,
            condition=condition,
            count=count
        )
        fan_arts = []
        for fan_art_row in result:
            fan_art_id, fan_art_title, father_dream_id, author_id, publish_time, fan_art_content, \
                number_of_likes, number_of_comments, number_of_views = fan_art_row
            fan_arts.append(FanArt(
                id_=fan_art_id,
                title=fan_art_title,
                content=fan_art_content,
                father_dream=self.get_dreams(condition=f'DreamID={father_dream_id}'),
                author=self.get_user(user_id=author_id),
                views=number_of_views,
                likes=number_of_likes,
                comments=self.get_comments('fanart', fan_art_id)
            ))
        return fan_arts

    def get_user(self, user_id=None, user_name=None):
        assert user_id or user_name, 'You must pass EITHER username or user ID.'
        user = User(*(self._perform_query(
            table='User',
            sort='UserName',
            condition=f'UserID={user_id}' if user_id else f'UserName={user_name}',
            count=1
        )[0]))  # Gets the first (and only) user in the result and maps it to all args
        return user

    def _perform_query(self, table, columns='*', condition='', sort='', order='desc', count=None):
        query_string = f"""SELECT {str(columns) if columns != '*' else '*'} FROM {table}
                                {'WHERE ' + condition if condition else ''}
                                {'ORDER BY ' + sort + ' ' + order.upper() if sort else ''}
                                {'LIMIT '+str(count) if count else ''}
                ;"""
        self.logger.debug(f"New query: {query_string}")
        self.cur.execute(query_string)
        return self.cur.fetchall()

    def _connet(self):
        self.conn = sqlite3.connect(self.database_path, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("""PRAGMA foreign_keys = ON;""")

    def _disconnect(self):
        self.conn.commit()
        self.conn.close()

    def setup(self, overwrite=False):
        """
        Creates necessary tables.
        :param overwrite: Create a completely new database.
        :return: None
        """
        if overwrite and input(f"Are you sure you want to overwrite the database ({self.database_path})? y/N ").lower() == 'y':
            self.logger.warning(f"Overwriting database!")
            self._disconnect()
            open(self.database_path, 'w')
            self._connet()
        try:
            self.logger.debug('Creating tables: Dream and FanArt tables')
            # Notes:
            #   NumberOfComments needs to be manually incremented every time a new comment is created
            #   Content is raw HTML
            self.cur.execute("""CREATE TABLE Dream (
                        DreamID             INTEGER PRIMARY KEY AUTOINCREMENT,
                        Title               TEXT    NOT NULL,
                        AuthorID            INT     NOT NULL,
                        PublishTime         TEXT    NOT NULL,
                        Content             TEXT    NOT NULL,
                        NumberOfLikes       INT     DEFAULT 0,
                        NumberOfComments    INT     DEFAULT 0,
                        NumberOfViews       INT     DEFAULT 0,
                        FOREIGN KEY (AuthorID) REFERENCES User (UserID)
                    );""")
            self.cur.execute("""CREATE TABLE FanArt (
                        FanArtID            INTEGER PRIMARY KEY AUTOINCREMENT,
                        Title               TEXT    NOT NULL,
                        FatherDreamID       INT     NOT NULL,
                        AuthorID            INT     NOT NULL,
                        PublishTime         TEXT    NOT NULL,
                        Content             TEXT    NOT NULL,
                        NumberOfLikes       INT     DEFAULT 0,
                        NumberOfComments    INT     DEFAULT 0,
                        NumberOfViews       INT     DEFAULT 0,
                        FOREIGN KEY (FatherDreamID) REFERENCES Dream (DreamID),
                        FOREIGN KEY (AuthorID)      REFERENCES User (UserID)
                    );""")

            self.logger.debug('Creating tables: User table')
            self.conn.execute("""CREATE TABLE User (
                        UserID              INTEGER PRIMARY KEY AUTOINCREMENT,
                        UserName            TEXT    NOT NULL
                    );""")
            # User avatar should be stored with filename UserID.

            self.logger.debug('Creating tables: Character table')
            self.cur.execute("""CREATE TABLE Character (
                        CharacterID         INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name                TEXT    NOT NULL,
                        Description         TEXT    NOT NULL,
                        AuthorID            INT     NOT NULL,
                        FOREIGN KEY (AuthorID) REFERENCES User (UserID)
                    );""")

            self.logger.debug('Creating tables: Dream-Character junction table')
            # Create junction tables for dream-character and author-character relationships
            self.cur.execute("""CREATE TABLE DreamCharacterJoin (
                        DreamID             INT     NOT NULL,
                        CharacterID         INT     NOT NULL,
                        FOREIGN KEY (DreamID)       REFERENCES Dream (DreamID),
                        FOREIGN KEY (CharacterID)   REFERENCES Character (CharacterID)
                        CONSTRAINT pk_DreamCharacterJoin PRIMARY KEY (DreamID, CharacterID)
                    );""")

            self.logger.debug('Creating tables: Comment tables')
            # Create junction tables for comments and secondary comments (replies)
            self.cur.execute("""CREATE TABLE DreamComment (
                        CommentID           INTEGER PRIMARY KEY AUTOINCREMENT,
                        AuthorID            INT     NOT NULL,
                        Content             TEXT    NOT NULL,
                        FatherDreamID       INT     NOT NULL,
                        PublishTime         TEXT    NOT NULL,
                        FOREIGN KEY (AuthorID) REFERENCES User (UserID),
                        FOREIGN KEY (FatherDreamID) REFERENCES Dream (DreamID)
                    );""")
            self.cur.execute("""CREATE TABLE SecondaryDreamComment (
                        SecondaryCommentID  INTEGER PRIMARY KEY AUTOINCREMENT,
                        AuthorID            INT     NOT NULL,
                        Content             TEXT    NOT NULL,
                        FatherCommentID     INT     NOT NULL,
                        PublishTime         TEXT    NOT NULL,
                        FOREIGN KEY (AuthorID) REFERENCES User (UserID),
                        FOREIGN KEY (FatherCommentID) REFERENCES DreamComment (CommentID)
                    );""")
            self.cur.execute("""CREATE TABLE FanArtComment (
                        CommentID           INTEGER PRIMARY KEY AUTOINCREMENT,
                        AuthorID            INT     NOT NULL,
                        Content             TEXT    NOT NULL,
                        FatherFanArtID      INT     NOT NULL,
                        PublishTime T       EXT     NOT NULL,
                        FOREIGN KEY (AuthorID) REFERENCES User (UserID),
                        FOREIGN KEY (FatherFanArtID) REFERENCES FanArt (FanArtID)
                    );""")
            self.cur.execute("""CREATE TABLE SecondaryFanArtComment (
                        SecondaryCommentID  INTEGER PRIMARY KEY AUTOINCREMENT,
                        AuthorID            INT     NOT NULL,
                        Content             TEXT    NOT NULL,
                        FatherCommentID     INT     NOT NULL,
                        PublishTime         TEXT    NOT NULL,
                        FOREIGN KEY (AuthorID) REFERENCES Users (UserID),
                        FOREIGN KEY (FatherCommentID) REFERENCES FanArtComment (CommentID) 
                    );""")

            self.conn.commit()
        except sqlite3.OperationalError as e:
            self.logger.error(f'An unexpected error occurred: {str(e)}, setup process is interrupted. ')
            self.logger.info('Tip: If you want to overwrite the database, use setup(True).')
        self.logger.info('Database setup completed.')
