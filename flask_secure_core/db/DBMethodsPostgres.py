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
        if callable(attr_value) and not attr_name.startswith("__") and attr_name not in blacklist:
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
            (username, hashed_password, access_level)
        )
        self.__conn.commit()
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