import colorlogx.logger as colorlogx
import DBConnectionManagerPostgres as db_conn_manager
import functools


logger = colorlogx.get_logger("DBConnectionManagerPostgres")


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

    def get_access_permissions(self, user_id):
        ...

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