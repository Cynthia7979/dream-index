from dreamindex import database_handling, db  # To change database location, edit __init__.py

db.setup()
# The following is for filling information into test database.
db.cur.executemany("""
INSERT INTO User VALUES (1, "Number One User");
INSERT INTO Dream VALUES (1, "Number One Dream", 1, "2021-10-20 13:25:12.929", "Content", 0, 0, 0);
INSERT INTO Dream VALUES (2, "Number Two Dream", 1, "2021-10-20 13:25:13.929", "Content", 0, 0, 0);
INSERT INTO Dream VALUES (3, "Number Three Dream", 1, "2021-10-20 13:25:14.000", "Content", 0, 0, 0);
INSERT INTO Dream VALUES (4, "Number Four Dream", 1, "2021-10-20 13:25:15.929", "Content", 0, 0, 0);
INSERT INTO Dream VALUES (5, "Number Five Dream", 1, "2021-10-20 13:25:16.929", "Content", 0, 0, 0);
""")
