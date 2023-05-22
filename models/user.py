from uuid import uuid4
from models.alter import Alter
from models.subsystem import Subsystem
import sqlite3

from typing import List


class User:

    def __init__(self, discord_id: str = None) -> None:
        """
        Constructor for the User class
        """

        self.discord_id: str = str()
        self.profile_picture_url: str = str()
        self.system_name: str = str()
        self.alters: List[Alter] = list()
        self.subsystems: List[Subsystem] = list()

        if discord_id is not None:
            self._load(discord_id)

    def _load(self, discord_id: str) -> None:

        # ensure that the user exists
        assert exists(discord_id), NameError("User does not exist")

        # get the info
        conn = sqlite3.connect("data/users.db")
        conn.row_factory = sqlite3.Row  # for dict output
        curs = conn.cursor()
        command = f"""
                SELECT * FROM users WHERE discordId='{discord_id}';
                """
        curs.execute(command)
        row = curs.fetchall()[0]
        result = dict(zip(row.keys(), row))
        conn.close()

        self.profile_picture_url = result["profilePictureUrl"]
        self.system_name = result["systemName"]

        # get all alters in the system
        conn = sqlite3.connect("data/alters.db")
        conn.row_factory = sqlite3.Row  # for dict output
        curs = conn.cursor()
        command = f"""
        SELECT * FROM alters WHERE parentUser='{discord_id}';
        """
        curs.execute(command)
        try:
            row = curs.fetchall()[0]
            result = dict(zip(row.keys(), row))
            conn.close()

            print(result) # @todo: add result to self.alters
        except IndexError:
            self.alters = []

        # get all the subsystems
        conn = sqlite3.connect("data/subsystems.db")
        conn.row_factory = sqlite3.Row  # for dict output
        curs = conn.cursor()
        command = f"""
            SELECT * FROM subsystems WHERE parentUser='{discord_id}';
            """
        curs.execute(command)
        try:
            row = curs.fetchall()[0]
            result = dict(zip(row.keys(), row))
            conn.close()

            print(result)  # @todo: Add result to self.subsystems
        except IndexError:
            self.subsystems = []

        # @todo: in load, add method to get subsyss

    def create_alter(self, new_alter_name: str) -> None:

        # create the new alter

        # generate a new uuid
        new_uuid = str(uuid4())

        # connect to the database and create a user
        conn = sqlite3.connect("data/alters.db")
        curs = conn.cursor()
        command = f"""
            INSERT INTO alters (uuid, parentUser, name)
            VALUES ('{new_uuid}', '{self.discord_id}', '{new_alter_name}')
            """
        curs.execute(command)
        conn.commit()
        conn.close()

        self.alters.append(Alter(new_uuid))

    def remove_alter(self, alter_uuid: str) -> None:

        # remove from this instance
        for alter in self.alters:
            if alter.get_uuid() == alter_uuid:
                self.alters.remove(alter)

        # delete from database
        Alter(alter_uuid).delete()

    def save(self) -> None:
        # initialise the SQL connector
        conn = sqlite3.connect("data/users.db")
        curs = conn.cursor()
        command = f"""
        UPDATE users
        SET (
            discordId='{self.discord_id}',
            profilePictureUrl='{self.profile_picture_url}',
            systemName='{self.system_name}'
        ) WHERE discordId='{self.discord_id}';
        """
        curs.execute(command)
        conn.commit()
        conn.close()

    def delete(self):
        """
        Deletes this instance from the database
        :return: None
        """
        conn = sqlite3.connect("data/user.db")
        curs = conn.cursor()
        command = f"""
            DELETE FROM users WHERE discordId='{self.discord_id}';
            """
        curs.execute(command)
        conn.commit()
        conn.close()

        # @todo: Also delete child alters and subsyss

    # @todo: add_alter, remove_alter, add_subsystem, remove_subsystem


def new(new_discord_id: str) -> User:

    # check that the username is not taken
    if exists(new_discord_id):
        raise NameError("Username taken")

    # connect to the database and create a user
    conn = sqlite3.connect("data/users.db")
    curs = conn.cursor()
    command = f"""
    INSERT INTO users (discordId)
    VALUES ('{new_discord_id}')
    """
    curs.execute(command)
    conn.commit()
    conn.close()

    # return the new instance
    return User(new_discord_id)


def create(new_discord_id: str) -> User:
    return new(new_discord_id)


def exists(discord_id: str) -> bool:
    conn = sqlite3.connect("data/users.db")
    curs = conn.cursor()
    command = f"""
    SELECT * FROM users WHERE discordId='{discord_id}';
    """
    curs.execute(command)
    results = curs.fetchall()
    conn.close()

    return len(results) >= 1
