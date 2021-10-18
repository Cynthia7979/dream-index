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
import sqlite3
import os


class Database:
    def __init__(self, database_path):
        print(os.getcwd())
        print(os.path.exists(database_path), database_path, os.path._getfullpathname(database_path))
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()

    def setup(self):
        # Create article tables
        # Notes:
        #   NumberOfComments needs to be incremented every time a new comment is created
        #   Content is raw HTML
        self.cur.execute("""CREATE TABLE Dream (
                    ID INT PRIMARY KEY,
                    Title TEXT,
                    AuthorID INT REFERENCES User (user_id),
                    PublishTime TEXT NOT NULL,
                    Content TEXT,
                    NumberOfLikes INT DEFAULT 0,
                    NumberOfComments INT DEFAULT 0,
                    NumberOfViews INT DEFAULT 0
                );""")
        self.cur.execute("""CREATE TABLE FanArt (
                    ID INT PRIMARY KEY,
                    Title TEXT,
                    FatherDreamID INT REFERENCES Dream (dream_id),
                    AuthorID INT REFERENCES User (user_id),
                    PublishTime TEXT NOT NULL,
                    Content TEXT,
                    NumberOfLikes INT DEFAULT 0,
                    NumberOfComments INT DEFAULT 0
                );""")

        # Create junction tables for dream-character and author-character relationships
        self.cur.execute("""CREATE TABLE DreamCharacterJoin (
                    DreamID INT REFERENCES Dream (dream_id),
                    CharacterID INT REFERENCES Character (character_id),
                    CONSTRAINT pk_DreamCharacterJoin PRIMARY KEY (dream_id, character_id)
                );""")
        self.cur.execute("""CREATE TABLE AuthorCharacterJoin (
                    AuthorID INT REFERENCES Dream (author_id),
                    CharacterID INT REFERENCES Character (character_id),
                    CONSTRAINT pk_AuthorCharacterJoin PRIMARY KEY (author_id, character_id)
                );""")

        # Create junction tables for comments and secondary comments (replies)
        self.cur.execute("""CREATE TABLE DreamComment (
                    ID INT PRIMARY KEY,
                    AuthorID INT REFERENCES User (user_id),
                    Content TEXT NOT NULL,
                    FatherDreamID INT REFERENCES Comment (father_dream_id) NOT NULL,
                    PublishTime TEXT NOT NULL
                );""")
        self.cur.execute("""CREATE TABLE SecondaryDreamComment (
                    ID INT PRIMARY KEY,
                    AuthorID INT REFERENCES Users (user_id),
                    Content TEXT NOT NULL,
                    FatherCommentID INT REFERENCES DreamComment (father_comment_id) NOT NULL,
                    PublishTime TEXT NOT NULL
                );""")
        self.cur.execute("""CREATE TABLE FanArtComment (
                    ID INT PRIMARY KEY,
                    AuthorID INT REFERENCES User (user_id),
                    Content TEXT NOT NULL,
                    FatherFanArtID INT REFERENCES Comment (father_fan_art_id) NOT NULL,
                    PublishTime TEXT NOT NULL
                );""")
        self.cur.execute("""CREATE TABLE SecondaryFanArtComment (
                    ID INT PRIMARY KEY,
                    AuthorID INT REFERENCES Users (user_id),
                    Content TEXT NOT NULL,
                    FatherCommentID INT REFERENCES FanArtComment (father_comment_id) NOT NULL,
                    PublishTime TEXT NOT NULL
                );""")
