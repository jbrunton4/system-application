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

        self._uuid: str = str(uuid4())
        self.name: str = str()
        self.description: str = str()
        self.profile_picture_url: str = str()
        self.alters: List[Alter] = list()

        self._load(uuid)

    def _load(self, uuid: str) -> None:
        if not exists(uuid):
            raise NameError("Subsystem does not exist")

        conn = sqlite3.connect("data/subsystems.db")
        conn.row_factory = sqlite3.Row  # for dict output
        curs = conn.cursor()
        command = f"""
                SELECT * FROM subsystems WHERE uuid='{uuid}';
                """
        curs.execute(command)
        result = curs.fetchall()[0]
        conn.close()

        self._uuid = uuid
        self.name = result["name"]
        self.description = result["description"]
        self.profile_picture_url = result["profilePictureUrl"]

        # get the alters in the subsystem
        conn = sqlite3.connect("data/alters.db")
        curs = conn.cursor()
        command = f"""
                SELECT * FROM alters WHERE parentSubsystem='{uuid}';
                """
        curs.execute(command)
        try:
            alters = curs.fetchall()[0]
        except IndexError:
            conn.close()
            return
        conn.close()
        self.alters = list(map(Alter, alters))

    def get_uuid(self) -> str:
        return self._uuid

    def save(self):
        conn = sqlite3.connect("data/subsystems.db")
        curs = conn.cursor()
        command = f"""
                UPDATE subsystems
                SET ( 
                    uuid='{self._uuid}',
                    name='{self.name}',
                    description='{self.description}',
                    profilePicture='{self.profile_picture_url}'
                ) WHERE uuid='{self._uuid}';
                """
        curs.execute(command)
        conn.commit()
        conn.close()


def exists(uuid: str) -> bool:
    conn = sqlite3.connect("data/subsystems.db")
    curs = conn.cursor()
    command = f"""
    SELECT * FROM subsystems WHERE uuid='{uuid}';
    """
    curs.execute(command)
    results = curs.fetchall()
    conn.close()

    return len(results) >= 1
