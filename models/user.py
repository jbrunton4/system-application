from uuid import uuid4
from secrets import token_urlsafe
from time import time
import sqlite3

from typing import List


class User:

    def __init__(self, username: str = None) -> None:
        """
        Constructor for the User class
        """

        self.display_name: str = str()
        self.description: str = str()
        self.subsystems: List[str] = list()
        self.members: List[str] = list()
        self.profile_picture_url: str = str()
        self.banner_url: str = str()
        self.theme_colour: str = str()

        self._uuid: str = str(uuid4())
        self._username: str = str()
        self._password: str = str()
        self._session_tokens: dict = dict()

        if username is not None:
            self._load(username)

    def _load(self, username: str) -> None:
        """
        Loads information from the database
        :param username: The username to query
        :return: None
        """

        if not exists(username):
            raise NameError("User does not exist")

        conn = sqlite3.connect("data/user.db")
        conn.row_factory = sqlite3.Row  # for dict output
        curs = conn.cursor()
        command = f"""
        SELECT * FROM user WHERE username='{username}';
        """
        curs.execute(command)
        row = curs.fetchall()[0]
        result = dict(zip(row.keys(), row))
        conn.close()

        self.uuid = result["uuid"]
        self._username = result["username"]
        self.description = result["description"]
        self.profile_picture_url = result["profilePictureUrl"]
        self.banner_url = result["bannerUrl"]
        self.theme_colour = result["themeColour"]
        self._password = result["password"]

        # @todo: in load, add method to get members inc subsyss

    def save(self) -> None:
        # initialise the SQL connector
        conn = sqlite3.connect("data/user.db")
        curs = conn.cursor()
        command = f"""
        UPDATE user
        SET uuid='{self.get_uuid()}',
            username='{self.get_username()}',
            description='{self.description}',
            profilePictureUrl='{self.profile_picture_url}',
            bannerUrl='{self.banner_url}',
            themeColour='{self.theme_colour}',
            password='{self._password}'
        ) WHERE uuid='{self.get_uuid()}';
        """
        curs.execute(command)
        conn.commit()
        conn.close()

    def get_username(self) -> str:
        """
        Getter method for private property self._username
        :return: This instance's username
        """
        return self._username

    def get_uuid(self) -> str:
        """
        Getter method for private property self._uuid
        :return: This instance's uuid
        """
        return self._uuid

    def validate_password(self, password_attempt: str) -> bool:
        """
        Checks a password attempt against this instance's private attr password
        :param password_attempt: The password attempt to compare
        :return: True if matches, else False
        """
        return password_attempt == self._password

    def validate_session_token(self, token_attempt: str) -> bool:
        """
        Check if a given token is valid for this account
        :param token_attempt: The token attempt to compare
        :return: True if valid, else False
        """
        if token_attempt in self._session_tokens:
            return self._session_tokens[token_attempt] <= time()
        return False

    def create_session_token(self, expires_seconds: int = 155_250_000) -> str:
        """
        Creates and stores a session token
        :param expires_seconds: The number of seconds after which the token should exite
        :return: The session token as a string
        """
        # create the new token
        new_token = token_urlsafe()
        self._session_tokens[new_token] = time() + expires_seconds
        self.save()
        return new_token

    def revoke_session_token(self, token: str) -> None:
        del self._session_tokens[token]
        self.save()

    def clear_session_tokens(self) -> None:
        self._session_tokens = {}
        self.save()

    def delete(self):
        """
        Deletes this instance from the database
        :return: None
        """
        conn = sqlite3.connect("data/user.db")
        curs = conn.cursor()
        command = f"""
            DELETE FROM user WHERE uuid='{self.get_uuid()}';
            """
        curs.execute(command)
        conn.commit()
        conn.close()

    # @todo: add_alter, remove_alter, add_subsystem, remove_subsystem


def new(new_username: str, new_password: str) -> User:
    """
    Create a new instance
    :param new_username: The username to create
    :param new_password: The password to create
    :return: A new session token lasting 30 days
    """

    # check that the username is not taken
    if exists(new_username):
        raise NameError("Username taken")

    # generate a new uuid
    new_uuid = str(uuid4())

    # connect to the database and create a user
    conn = sqlite3.connect("data/user.db")
    curs = conn.cursor()
    command = f"""
    INSERT INTO user (uuid, username, password)
    VALUES ('{new_uuid}', '{new_username}', '{new_password}')
    """
    curs.execute(command)
    conn.commit()
    conn.close()

    # return the new instance
    return User(new_username)


def create(new_username: str, new_password: str) -> User:
    """
    Alias for user.new
    :param new_username: The username to create
    :param new_password: The password to create
    :return: The new User
    """
    return new(new_username, new_password)


def exists(username: str) -> bool:
    conn = sqlite3.connect("data/user.db")
    curs = conn.cursor()
    command = f"""
    SELECT * FROM user WHERE username='{username}';
    """
    curs.execute(command)
    results = curs.fetchall()
    conn.close()

    return len(results) >= 1
