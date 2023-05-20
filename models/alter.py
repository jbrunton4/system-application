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
        conn = sqlite3.connect("data/alter.db")
        curs = conn.cursor()
        command = f"""
        UPDATE alter
        SET uuid='{self.get_uuid()}',
            name='{self.name}',
            pronouns='{self.pronouns}',
            age='{self.age}',
            autoAge='{self.auto_age}',
            ageCategory='{self.age_category}',
            roles='{self.roles}',
            themeColour='{self.theme_colour}',
            profilePictureUrl='{self.profile_picture_url}',
            bannerUrl='{self.banner_url}',
            startTag='{self.start_tag}',
            endTag='{self.end_tag}',
            typingQuirk='{self.typing_quirk}',
            description='{self.description}'
        ) WHERE uuid='{self.get_uuid()}';
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

        conn = sqlite3.connect("data/alter.db")
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        command = f"""
                SELECT * FROM alter WHERE uuid='{uuid}';
                """
        curs.execute(command)
        row = curs.fetchall()[0]
        result = dict(zip(row.keys(), row))
        conn.close()

        self._uuid = result["uuid"]
        self.name = result["name"]
        self.pronouns = result["pronouns"]
        self.age = result["age"]
        self.auto_age = result["autoAge"]
        self.age_category = result["ageCategory"]
        self.roles = result["roles"]
        self.theme_colour = result["themeColour"]
        self.profile_picture_url = result["profilePictureUrl"]
        self.banner_url = result["bannerUrl"]
        self.start_tag = result["startTag"]
        self.end_tag = result["endTag"]
        self.typing_quirk = result["typingQuirk"]
        self.description = result["description"]

    # @todo: delete()


def new(new_name: str) -> Alter:
    """
    Create a new instance
    :param new_name: The username to create
    :return: A new session token lasting 30 days
    """

    # generate a new uuid
    new_uuid = str(uuid4())

    # connect to the database and create a user
    conn = sqlite3.connect("data/alter.db")
    curs = conn.cursor()
    command = f"""
    INSERT INTO alter (uuid, name)
    VALUES ('{new_uuid}', '{new_name}')
    """
    curs.execute(command)
    conn.commit()
    conn.close()

    # return the new instance
    return Alter(new_name)


def create(new_name: str) -> Alter:
    """
    Alias for alter.new
    :param new_name: The username to create
    :return: The new User
    """
    return new(new_name)


def exists(uuid: str) -> bool:
    conn = sqlite3.connect("data/alter.db")
    curs = conn.cursor()
    command = f"""
    SELECT * FROM alter WHERE uuid='{uuid}';
    """
    curs.execute(command)
    results = curs.fetchall()
    conn.close()

    return len(results) >= 1

# @todo: is_subsys_alter