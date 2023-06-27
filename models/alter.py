from uuid import uuid4
import sqlite3


class Alter:

    def __init__(self, uuid: str) -> None:
        """
        Constructor method for this class
        """

        self._uuid: str = str(uuid4())

        self.name: str = str()
        self.pronouns: str = str()
        self.age: int = int()
        self.auto_age: bool = bool()
        self.age_category: str = str()
        self.roles: str = str()
        self.theme_colour: str = str()
        self.profile_picture_url: str = str()
        self.banner_url: str = str()
        self.start_tag: str = str()
        self.end_tag: str = str()
        self.typing_quirk: str = str()
        self.description: str = str()

        self._load(uuid)

    def save(self) -> None:
        # initialise the SQL connector
        conn = sqlite3.connect("data/alters.db")
        curs = conn.cursor()
        command = f"""
        UPDATE alters
        SET name='{self.name}',
            pronouns='{self.pronouns}',
            age='{self.age}',
            autoAge='{self.auto_age}',
            roles='{self.roles}',
            profilePictureUrl='{self.profile_picture_url}',
            startTag='{self.start_tag}',
            endTag='{self.end_tag}',
            description='{self.description}'
         WHERE uuid='{self.get_uuid()}';
        """
        curs.execute(command)
        conn.commit()
        conn.close()

    def get_uuid(self) -> str:
        return self._uuid

    def _load(self, uuid: str) -> None:
        """
        Load a UUID's data from the database
        :param uuid: The UUID to query
        :return: None
        """

        if not exists(uuid):
            raise NameError("Alter does not exist")

        conn = sqlite3.connect("data/alters.db")
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        command = f"""
                SELECT * FROM alters WHERE uuid='{uuid}';
                """
        curs.execute(command)
        row = curs.fetchall()[0]
        result = dict(zip(row.keys(), row))
        conn.close()

        self._uuid = result["uuid"]
        self.name = result["name"]
        self.pronouns = result["pronouns"]
        self.age = result["age"]
        self.autoAge = result["autoAge"]
        self.roles = result["roles"]
        self.profile_picture_url = result["profilePictureUrl"]
        self.start_tag = result["startTag"]
        self.end_tag = result["endTag"]
        self.description = result["description"]

    def delete(self) -> None:
        """
        Deletes this instance from the database
        :return: None
        """

        conn = sqlite3.connect("data/alters.db")
        curs = conn.cursor()
        command = f"""
                            DELETE FROM alters WHERE uuid='{self._uuid}';
                            """
        curs.execute(command)
        conn.commit()
        conn.close()

    def is_subsys_alter(self) -> bool:
        conn = sqlite3.connect("data/alters.db")
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        command = f"""
                        SELECT * FROM alters WHERE uuid='{self._uuid}';
                        """
        curs.execute(command)
        row = curs.fetchall()[0]
        result = dict(zip(row.keys(), row))
        conn.close()

        return result["parentSubsystem"] is None or result["parentSubsystem"] == "None"

    def remove_from_subsys(self) -> None:
        conn = sqlite3.connect("data/alters.db")
        curs = conn.cursor()
        command = f"""
                        UPDATE alters
                        SET ( 
                            parentSubsystem='{None}'
                        ) WHERE uuid='{self._uuid}';
                        """
        curs.execute(command)
        conn.commit()
        conn.close()


def exists(uuid: str) -> bool:
    conn = sqlite3.connect("data/alters.db")
    curs = conn.cursor()
    command = f"""
    SELECT * FROM alters WHERE uuid='{uuid}';
    """
    curs.execute(command)
    results = curs.fetchall()
    conn.close()

    return len(results) >= 1
