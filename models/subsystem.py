import sqlite3
from typing import List
from uuid import uuid4

from models.alter import Alter


class Subsystem:
    """
    The Subsystem class does not have a direct equivalent in the database.
    Instead, the collection of members is created by reading the member database.
    """

    def __init__(self, uuid: str) -> None:
        """
        Constructor method for this class
        """

        self.uuid: str = str(uuid4())
        self.alters: List[str] = list()

        self._load(uuid)

    def _load(self, uuid: str) -> None:
        if not exists(uuid):
            raise NameError("Alter does not exist")

        conn = sqlite3.connect("data/alter.db")
        curs = conn.cursor()
        command = f"""
                SELECT * FROM alter WHERE parentSubsystem='{uuid}';
                """
        curs.execute(command)
        alters = curs.fetchall()[0]
        conn.close()

        self._uuid = uuid
        self.alters = list(map(Alter, alters))

    # @todo: add_alter, remove_alter, delete(destroy_members=False)


def new() -> Subsystem:
    """
    Create a new instance
    :return: The new Subsystem
    """

    # generate a new uuid
    new_uuid = str(uuid4())

    # connect to the database and create a subsystem
    conn = sqlite3.connect("data/subsystem.db")
    curs = conn.cursor()
    command = f"""
        INSERT INTO alter (uuid)
        VALUES ('{new_uuid}')
        """
    curs.execute(command)
    conn.commit()
    conn.close()

    # return the new instance
    return Subsystem(new_uuid)


def exists(uuid: str) -> bool:
    conn = sqlite3.connect("data/subsystem.db")
    curs = conn.cursor()
    command = f"""
    SELECT * FROM subsystem WHERE uuid='{uuid}';
    """
    curs.execute(command)
    results = curs.fetchall()
    conn.close()

    return len(results) >= 1
