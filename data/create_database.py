import sqlite3

# users database
conn = sqlite3.connect("data/users.db")
curs = conn.cursor()
command = """
CREATE TABLE users (
    discordId STRING PRIMARY KEY,
    profilePictureUrl STRING,
    systemName STRING
);"""
curs.execute(command)
conn.commit()
conn.close()

# alters database
conn = sqlite3.connect("data/alters.db")
curs = conn.cursor()
command = """
CREATE TABLE alters (
    uuid STRING PRIMARY KEY,
    parentUser STRING,
    parentSubsystem STRING,
    name STRING,
    pronouns STRING,
    age STRING,
    autoAge BOOLEAN,
    roles STRING,
    profilePictureUrl STRING,
    startTag STRING,
    endTag STRING,
    description STRING
);"""
curs.execute(command)
conn.commit()
conn.close()

# subsystems database
conn = sqlite3.connect("data/subsystems.db")
curs = conn.cursor()
command = """
CREATE TABLE subsystems (
    uuid STRING PRIMARY KEY;
    name STRING,
    parentUser STRING,
    description STRING,
    profilePictureUrl STRING
);"""
