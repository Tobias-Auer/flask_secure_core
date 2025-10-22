import colorlogx.logger as colorlogx
import functools


logger = colorlogx.get_logger("DBMethodsPostgres")


def db_error_handler(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            logger.error(f"Database error in {method.__name__}: {e}")
            if self.conn:
                self.conn.rollback()
            raise

    return wrapper


def decorate_all_db_methods(cls):
    blacklist = ["close"]
    for attr_name, attr_value in cls.__dict__.items():
        if (
            callable(attr_value)
            and not attr_name.startswith("__")
            and attr_name not in blacklist
        ):
            setattr(cls, attr_name, db_error_handler(attr_value))
    return cls


@decorate_all_db_methods
class DBMethods:
    def __init__(self, connection_manager):
        self.__connection_manager = connection_manager
        self.__conn = self.__connection_manager.get_db_conn()
        self.__cursor = self.__conn.cursor()

    def get_access_permissions_by_id(self, user_id):
        self.__cursor.execute(
            "SELECT access_level FROM fsl.users WHERE id = %s", (user_id,)
        )
        result = self.__cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def get_access_permission_by_username(self, username):
        self.__cursor.execute(
            "SELECT access_level FROM fsl.users WHERE username = %s", (username,)
        )
        result = self.__cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def authenticateAdmin(self, username, password):
        return username == "admin" and password == "admin"

    def authenticateUser(self, username, password):
        from ..utils import verify_password

        """"
        Return True if the username and password are correct, False otherwise.
        """
        self.__cursor.execute(
            "SELECT password FROM fsl.users WHERE username = %s", (username,)
        )
        result = self.__cursor.fetchone()
        if result is None:
            return False
        stored_password = result[0]
        return verify_password(stored_password, password)

    def create_user(self, username, password, access_level=3):
        from ..utils import hash_password

        hashed_password = hash_password(password)
        self.__cursor.execute(
            "INSERT INTO fsl.users (username, password, access_level) VALUES (%s, %s, %s)",
            (username, hashed_password, access_level),
        )
        self.__conn.commit()
        return self.__cursor.lastrowid

    def get_user_id_by_username(self, username):
        self.__cursor.execute(
            "SELECT id FROM fsl.users WHERE username = %s", (username,)
        )
        result = self.__cursor.fetchone()
        if result is None:
            self.logger.error(f"Could not find user ID for username: {username}")
            return None
        return result[0]

    def get_all_user_data_in_json(self):
        self.__cursor.execute(
            """SELECT 
                u.username,
                u.display_name,
                a.display_name AS role,
                u.last_login,
                u.created_at,
                u.is_active
                FROM fsl.users AS u
                LEFT JOIN fsl.access_level_info AS a
                ON u.access_level = a.id;
            """
        )
        rows = self.__cursor.fetchall()
        users = []
        for row in rows:
            user = {
                "username": row[0],
                "display_name": row[1] if row[1] else "-",
                "role": row[2],
                "lastLogin": row[3].strftime("%H:%M, %d.%m.%Y") if row[3] else None,
                "created": row[4].strftime("%H:%M, %d.%m.%Y") if row[4] else None,
                "status": "Enabled" if row[5] else "Disabled",
                "email": "no@db.entry",
            }
            users.append(user)
        # return json.dumps(users)
        return users

    def create_user(
        self, username,
        display_name,
        password,
        access_level,
        is_active=True
    ):
        from ..utils import hash_password

        hashed_password = hash_password(password)
        self.__cursor.execute(
            "SELECT id FROM fsl.access_level_info WHERE display_name = %s", (access_level,)
        )
        result = self.__cursor.fetchone()
        print("Access level check result:", result)
        if result is None:
            return ValueError(f"Access level ID {access_level} does not exist.")
        self.__cursor.execute(
            """INSERT INTO fsl.users 
            (username, display_name, password, access_level, is_active) 
            VALUES (%s, %s, %s, %s, %s)""",
            (username, display_name, hashed_password, result, is_active),
        )

        self.__conn.commit()
        print("User created:", username)
        return self.__cursor.lastrowid
    
    
    def close(self):
        if self.__cursor:
            self.__cursor.close()
            self.__cursor = None
        if self.__conn:
            self.__connection_manager.release_connection(self.__conn)
            self.__conn = None
        if self.__connection_manager:
            self.__connection_manager = None


# TODO: This 👇
class Preferences:
    def __init__(self, connection_manager):
        self.__connection_manager = connection_manager

    def get(self, key, default=None):
        # Placeholder for getting preferences from the database
        ...

    def set(self, key, value):
        # Placeholder for setting preferences in the database
        ...

    def close(self):
        # Placeholder for closing any resources if needed
        pass
