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
import sqlite3
import os


@logged
class Database:
    def __init__(self, database_path):
        self.database_path = database_path
        self._connet()
        self.logger.info(f"Database instance on {self.database_path} is created.")

    def _connet(self):
        self.conn = sqlite3.connect(self.database_path)
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
                        ID INT PRIMARY KEY,
                        Title TEXT,
                        AuthorID INT REFERENCES User (ID),
                        PublishTime TEXT NOT NULL,
                        Content TEXT,
                        NumberOfLikes INT DEFAULT 0,
                        NumberOfComments INT DEFAULT 0,
                        NumberOfViews INT DEFAULT 0
                    );""")
            self.cur.execute("""CREATE TABLE FanArt (
                        ID INT PRIMARY KEY,
                        Title TEXT,
                        FatherDreamID INT REFERENCES Dream (ID),
                        AuthorID INT REFERENCES User (ID),
                        PublishTime TEXT NOT NULL,
                        Content TEXT,
                        NumberOfLikes INT DEFAULT 0,
                        NumberOfComments INT DEFAULT 0
                    );""")

            self.logger.debug('Creating tables: Character junction tables')
            # Create junction tables for dream-character and author-character relationships
            self.cur.execute("""CREATE TABLE DreamCharacterJoin (
                        DreamID INT REFERENCES Dream (ID),
                        CharacterID INT REFERENCES Character (ID),
                        CONSTRAINT pk_DreamCharacterJoin PRIMARY KEY (DreamID, CharacterID)
                    );""")
            self.cur.execute("""CREATE TABLE AuthorCharacterJoin (
                        AuthorID INT REFERENCES Dream (ID),
                        CharacterID INT REFERENCES Character (ID),
                        CONSTRAINT pk_AuthorCharacterJoin PRIMARY KEY (AuthorID, CharacterID)
                    );""")

            self.logger.debug('Creating tables: Comment junction tables')
            # Create junction tables for comments and secondary comments (replies)
            self.cur.execute("""CREATE TABLE DreamComment (
                        ID INT PRIMARY KEY,
                        AuthorID INT REFERENCES User (ID),
                        Content TEXT NOT NULL,
                        FatherDreamID INT REFERENCES Dream (ID) NOT NULL,
                        PublishTime TEXT NOT NULL
                    );""")
            self.cur.execute("""CREATE TABLE SecondaryDreamComment (
                        ID INT PRIMARY KEY,
                        AuthorID INT REFERENCES Users (ID),
                        Content TEXT NOT NULL,
                        FatherCommentID INT REFERENCES DreamComment (ID) NOT NULL,
                        PublishTime TEXT NOT NULL
                    );""")
            self.cur.execute("""CREATE TABLE FanArtComment (
                        ID INT PRIMARY KEY,
                        AuthorID INT REFERENCES User (ID),
                        Content TEXT NOT NULL,
                        FatherFanArtID INT REFERENCES FanArt (ID) NOT NULL,
                        PublishTime TEXT NOT NULL
                    );""")
            self.cur.execute("""CREATE TABLE SecondaryFanArtComment (
                        ID INT PRIMARY KEY,
                        AuthorID INT REFERENCES Users (ID),
                        Content TEXT NOT NULL,
                        FatherCommentID INT REFERENCES FanArtComment (ID) NOT NULL,
                        PublishTime TEXT NOT NULL
                    );""")

            self.conn.commit()
        except sqlite3.OperationalError as e:
            self.logger.error(f'An unexpected error occurred: {str(e)}, setup process is interrupted. ')
            self.logger.info('Tip: If you want to overwrite the database, use setup(True).')
        self.logger.info('Database setup completed.')
