import sqlite3

# users database
conn = sqlite3.connect("data/user.db")
curs = conn.cursor()
command = """
CREATE TABLE user (
    uuid STRING PRIMARY KEY,
    username STRING,
    description STRING,
    profilePictureUrl STRING,
    bannerUrl STRING,
    themeColour STRING,
    password STRING
);"""
curs.execute(command)
conn.commit()
conn.close()

# alters database
conn = sqlite3.connect("data/alter.db")
curs = conn.cursor()
command = """
CREATE TABLE alter (
    uuid STRING PRIMARY KEY,
    name STRING,
    pronouns STRING,
    age INTEGER,
    autoAge BOOLEAN,
    ageCategory STRING,
    roles STRING,
    themeColour STRING,
    profilePictureUrl STRING,
    bannerUrl STRING,
    startTag STRING,
    endTag STRING,
    typingQuirk STRING,
    description STRING,
    parentAccount STRING,
    parentSubsystem STRING
);"""
curs.execute(command)
conn.commit()
conn.close()

# tokens database
conn = sqlite3.connect("data/token.db")
curs = conn.cursor()
command = """
CREATE TABLE token (
    uuid STRING PRIMARY KEY,
    token STRING,
    expires FLOAT,
    parentAccount STRING
);"""