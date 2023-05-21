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
        alters = curs.fetchall()[0]
        conn.close()
        self.alters = list(map(Alter, alters))

    def delete(self, destroy_members: bool = False) -> None:
        """
        Deletes this instance
        :param destroy_members: Whether to destroy the members, or move them to being in the top level system
        :return: None
        """

        # destroy or reassign members
        if destroy_members:
            for alter in self.alters:
                alter.delete()  # @todo: move this method into User
        else:
            conn = sqlite3.connect("data/alters.db")
            curs = conn.cursor()
            command = f"""
            UPDATE alters
            SET (
                parentSubsystem='{None}'
            ) WHERE parentSubsystem='{self._uuid}';
            """
            curs.execute(command)
            conn.close()

        # delete the subsystem itself
        conn = sqlite3.connect("data/subsystems.db")
        curs = conn.cursor()
        command = f"""
                    DELETE FROM subsystems WHERE uuid='{self._uuid}';
                    """
        curs.execute(command)
        conn.commit()
        conn.close()

    def create_alter(self, new_alter_name: str) -> None:

        # generate a new uuid
        new_uuid = str(uuid4())

        # connect to the database and create a user
        conn = sqlite3.connect("data/alters.db")
        curs = conn.cursor()
        command = f"""
                    INSERT INTO alters (uuid, parentUser, parentSubsystem, name)
                    VALUES ('{new_uuid}', '{self.parent_user.discord_id}', '{self._uuid}', '{new_alter_name}')
                    """
        curs.execute(command)  # @todo: instead of this, make optional subsys arg in alter.new()
        conn.commit()
        conn.close()

        self.alters.append(Alter(new_uuid))

    # @todo: add_alter, remove_alter, delete(destroy_members=False)
    def remove_alter(self, alter_uuid: str, destroy: bool = False):

        for alter in self.alters:
            if alter.get_uuid() == alter_uuid:

                if destroy:
                    alter.delete()

                self.alters.remove(alter)
                self.parent_user.remove_alter(alter.get_uuid())  # @todo: User.remove_alter()
                self.parent_user.save()

        self.save()  # @todo: self.save()

    def save(self):
        conn = sqlite3.connect("data/subsystems.db")
        curs = conn.cursor()
        command = f"""
                UPDATE subsystems
                SET ( 
                    uuid='{self._uuid}',
                    parentUser='{self.parent_user}'
                    name='{self.name}',
                    description='{self.description}',
                    profilePicture='{self.profile_picture_url}'
                ) WHERE uuid='{self._uuid}';
                """
        curs.execute(command)
        conn.commit()
        conn.close()


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
