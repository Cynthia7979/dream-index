-- Dummy Users
INSERT INTO User VALUES (1, "Number One User");

-- Dummy Dreams
INSERT INTO Dream VALUES (1, "Number One Dream", 1, "2021-10-20 13:25:12.929", "Content", 0, 0, 0);
INSERT INTO Dream VALUES (2, "Number Two Dream", 1, "2021-10-20 13:25:13.929", "Content", 0, 0, 0);
INSERT INTO Dream VALUES (3, "Number Three Dream", 1, "2021-10-20 13:25:14.000", "Content", 0, 0, 0);
INSERT INTO Dream VALUES (4, "Number Four Dream", 1, "2021-10-20 13:25:15.929", "Content", 0, 0, 0);
INSERT INTO Dream VALUES (5, "Number Five Dream", 1, "2021-10-20 13:25:16.929", "Content", 0, 0, 0);

-- Dummy FanArts
INSERT INTO FanArt VALUES (1, "Fan Art 1", 1, 1, "2021-10-20 13:25:16.929", "Content 1", 0, 0, 0);
INSERT INTO FanArt VALUES (2, "Fan Art 2", 2, 1, "2021-10-20 13:25:17.929", "Content 2", 0, 0, 0);
INSERT INTO FanArt VALUES (3, "Fan Art 3", 3, 1, "2021-10-20 13:25:18.929", "Content 3", 0, 0, 0);
INSERT INTO FanArt VALUES (4, "Fan Art 4", 4, 1, "2021-10-20 13:25:19.929", "Content 4", 0, 0, 0);
INSERT INTO FanArt VALUES (5, "Fan Art 5", 5, 1, "2021-10-20 13:25:20.929", "Content 5", 0, 0, 0);

-- Dummy Comments
INSERT INTO DreamComment VALUES (1, 1, "Comment1Dream", 1, "2021-10-20 13:25:16.929");
INSERT INTO SecondaryDreamComment VALUES (1, 1, "Comment1Dream", 1, "2021-10-20 13:25:16.929");
INSERT INTO FanArtComment VALUES (1, 1, "Comment1FanArt", 1, "2021-10-20 13:25:16.929");
INSERT INTO SecondaryFanArtComment VALUES (1, 1, "Comment1FanArt", 1, "2021-10-20 13:25:16.929");

-- Dummy Characters and Links
INSERT INTO Character VALUES (1, "Character 1", "Character description one", 1);
INSERT INTO DreamCharacterJoin VALUES (1, 1);