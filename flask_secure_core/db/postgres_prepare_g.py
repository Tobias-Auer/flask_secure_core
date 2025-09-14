import colorlogx.logger as colorlogx

logger = colorlogx.get_logger("utils")

from flask import g
from flask_secure_core.db.DBMethodsPostgres import DBMethods as DBMethods_Postgres, Preferences as Preferences_Postgres
from ..get_conn import get_connection_manager


def init_db_obj():
    if "db_cursor" not in g:
        connection_manager = get_connection_manager()
        g.db_obj = DBMethods_Postgres(connection_manager)
        g.preferences = Preferences_Postgres(connection_manager)
        # TODO: implement a proper get preferences class
        # TODO: make db init a decorator
    if not g.get("db_obj", None):
        logger.error("No database connection available.")
        return False
    return True