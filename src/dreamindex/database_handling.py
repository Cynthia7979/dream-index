"""
Connects the code to the SQLite database.

This database uses junction tables for comments. This means that for any article (dream/fanart),
its comments can be assessed by querying all article-comment relationships with the appropriate id
in the DreamCommentLink or FanArtComments table.

On Naming:
Use PascalCasing for tables and column names,
fish_bone_casing for all variables,
and UPPERCASE abbreviations (e.g. ID, dreamID)

Refer to the following link for additional naming conventions:
https://stackoverflow.com/questions/7662/database-table-and-column-naming-conventions
"""
import sqlite3

DATABASE_PATH = "./databases/test_database.db"


class Database:
    def __init__(self, database_path=DATABASE_PATH):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()

    def setup(self):
        self.cur.execute("""CREATE TABLE Dream (
            ID INT PRIMARY KEY,
            Title VARCHAR(255),
            Content VARCHAR(8192),
            NumberOfLikes INT DEFAULT 0,
            NumberOfComments INT DEFAULT 0,
            AuthorID 
        );""")

        self.cur.execute("""CREATE TABLE Comment (
            ID INT PRIMARY KEY,
            AuthorID INT REFERENCES Users (user_id),
            
        );""")

        self.cur.execute("""CREATE TABLE DreamCommentLink (
            DreamID INT REFERENCES Dream (dream_id),
            CommentID INT REFERENCES Comment (comment_id),
            CONSTRAINT pk_DreamCommentLink PRIMARY KEY (dream_id, comment_id)
        );""")
